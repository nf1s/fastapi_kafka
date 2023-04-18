from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from kafka import KafkaProducer
import json

app = FastAPI()
producer = KafkaProducer(bootstrap_servers='kafka:29092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

items = {}

# Create an item
@app.post("/items/")
async def create_item(item: Item):
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item.id] = item
    producer.send('test.events', {"action": "create", "item": item.dict()})
    return item


# Update an item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    producer.send('test.events', {"action": "update", "item": item.dict()})
    return item

# Delete an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    producer.send('test.events', {"action": "delete", "item_id": item_id})
    return {"result": "Item deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
