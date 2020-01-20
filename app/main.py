from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from starlette.responses import StreamingResponse

import json
import os
import logging

from sesamutils import sesam_logger, VariablesConfig

# Define data models
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Init app and logger
app = FastAPI()
logger = logging.getLogger(__name__)
# logger = sesam_logger('fastapi-example', app=app, timestamp=True) # Not working

# Check environoment variables
# Default values can be given to optional environment variables by the use of tuples
required_env_vars = ["PORT"]
optional_env_vars = [("LOG_LEVEL", "INFO")] 
config = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)
    
if not config.validate():
    logger.error("Environment variables do not validate. Exiting system.")
    # os.sys.exit(1) # Infinit respawn

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


@app.post("/items/")
async def create_item(*,items: List[Item]) -> List:
    return items

@app.get("/")
def read_root() -> List:
    return [{"Hello": "World"}]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None) -> List:
    return [{"item_id": item_id, "q": q}]

@app.get("/stream/items/{item_id}")
def stream_items(item_id: int, step: int = 1) -> List:
    return StreamingResponse(stream_as_json({f"Val{i}": i} for i in range(0,item_id,step)),
        media_type="application/json; charset=utf-8")

