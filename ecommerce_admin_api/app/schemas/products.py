from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    sku: str


class ProductCreate(ProductBase):
    # used when creating products
    pass


class ProductUpdate(BaseModel):
    # partial updates allowed
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None


class Product(ProductBase):
    # complete product info with id and timestamps
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True