from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class InventoryBase(BaseModel):
    product_id: int
    quantity: int
    reorder_level: int = 10
    warehouse: str = "main"


class InventoryCreate(InventoryBase):
    # used when creating inventory entries
    pass


class InventoryUpdate(BaseModel):
    # partial updates
    quantity: Optional[int] = None
    reorder_level: Optional[int] = None
    warehouse: Optional[str] = None


class Inventory(InventoryBase):
    # complete inventory with id and timestamps
    id: int
    last_restock_date: Optional[datetime] = None
    updated_at: datetime
    
    class Config:
        orm_mode = True