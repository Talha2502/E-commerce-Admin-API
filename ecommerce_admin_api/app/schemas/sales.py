from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class SaleBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    channel: str


class SaleCreate(SaleBase):
    # for creating sales records
    pass


class Sale(SaleBase):
    # complete sale info
    id: int
    total_amount: float
    sale_date: datetime
    
    class Config:
        orm_mode = True


class SaleAnalytics(BaseModel):
    # for returning sales analytics
    total_sales: float
    total_quantity: int
    period: str