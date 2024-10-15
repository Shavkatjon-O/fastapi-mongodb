import os
import uvicorn

from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from bson import ObjectId


load_dotenv(find_dotenv())

MONGODB_URL = os.environ.get("MONGODB_URL")

app = FastAPI()

client = AsyncIOMotorClient(MONGODB_URL)
db = client.database
collection = db.collection


class Item(BaseModel):
    title: str
    description: str = None
    price: float


def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "description": item["description"],
        "price": item["price"],
    }

# List items
@app.get("/items/")
async def items_list():
    items = []
    async for item in collection.find():
        items.append(item_helper(item))
    return items


# Create item
@app.post("/items/", response_model=dict)
async def items_create(item: Item):
    item_dict = item.dict()
    result = await collection.insert_one(item_dict)
    item_new = await collection.find_one({"_id": result.inserted_id})
    return item_helper(item_new)


# Get item
@app.get("/items/{item_id}/")
async def items_get(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_helper(item)


# Update item
@app.put("/items/{item_id}/")
async def items_update(item_id: str, item: Item):
    result = await collection.update_one(
        {"_id": ObjectId(item_id)}, {"$set": item.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    item_updated = await collection.find_one({"_id": ObjectId(item_id)})
    return item_helper(item_updated)


# Delete item
@app.delete("/items/{item_id}/")
async def items_delete(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)