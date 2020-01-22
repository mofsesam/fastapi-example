from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl, IPvAnyAddress, ValidationError
from typing import List

from starlette.responses import StreamingResponse

import json
import os
import logging
from datetime import datetime

from sesamutils import sesam_logger, VariablesConfig

# Define data models
class Item(BaseModel):
    id: str
    description: str = None
    URL: HttpUrl
    IP: IPvAnyAddress = None

# Init app and logger
app = FastAPI()
logger = logging.getLogger(__name__)

# Check environoment variables
# Default values can be given to optional environment variables by the use of tuples
required_env_vars = ["PORT"]
optional_env_vars = [("LOG_LEVEL", "INFO")] 
config = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)
    
if not config.validate():
    logger.error("Environment variables do not validate. Exiting system.")
    raise ValueError('Environment variables do not validate. PORT value not set.')

# Routings
# Sesam expects, and gets, a JSON list as response and enteties with _id defined.
# async def is strictly only of importance if you use an async function/method inside the function. It is only
# used here to flag that FastAPI support it

# The root. The simplest example. 
@app.get("/")
def read_root() -> List:
    return [{"_id": "Hello1", "Hello": "World"}]

# A routing path, with a path-argument item_id (integer) and query string parameter, since (string)
# Query string since, is optional.
@app.get("/items/{item_id}")
def read_item(item_id: int, since: str = None) -> List:
    return [{"_id": item_id, "since": since}]

# This route expects a POST payload that is a JSON list of items that validate to Item data models
# the payload will be validated with the data model. 
@app.post("/items/")
async def create_item(*,items: List[Item]) -> List:
    return_list = []
    for i in items:
        i_dict = i.dict()
        i_dict["_id"] = i_dict["id"]
        return_list.append(i_dict)
    return return_list

# This example shows a more generic handeling of POST payload
@app.post("/generic/")
async def create_item(*,generic: List[dict]) -> List:
    return_list = []
    for d in generic:
        if 'id' in d:
            d["_id"] = d["id"]
        else:
            logger.error("Missing id: " + str(d))
        return_list.append(d)
    return return_list

# This example shows a streaming response
@app.get("/stream/items/{item_id}")
def stream_items(item_id: int, step: int = 1) -> List:
    return StreamingResponse(stream_as_json({"_id": f"StreamItem{i}", 
            "datetime": str(datetime.now())} for i in range(0,item_id,step)),
        media_type="application/json; charset=utf-8")

# Helper functions

def stream_as_json(generator_function):
    """Helper generator to support streaming to Sesam"""
    first = True
    yield '['
    for item in generator_function:
        if not first:
            yield ','
        else:
            first = False
        yield json.dumps(item)
    yield ']'
