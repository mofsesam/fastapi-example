from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import StreamingResponse
import json

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

app = FastAPI()

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
async def create_item(item: Item):
    return [item]

@app.get("/")
def read_root():
    return [{"Hello": "World"}]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return [{"item_id": item_id, "q": q}]

@app.get("/stream/items/{item_id}")
def stream_items(item_id: int, step: int = 1):
    return StreamingResponse(stream_as_json({f"Val{i}": i} for i in range(0,item_id,step)),
        media_type="application/json; charset=utf-8")

