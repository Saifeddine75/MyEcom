import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    id:int
    name:str
    price:int

class Products(BaseModel):
    products: List[Product]



app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

memory_db = {"products": []}


@app.get("/product", response_model=Product)
def get_product():
    return Product(id=0, name="Bonjour", price=100)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)