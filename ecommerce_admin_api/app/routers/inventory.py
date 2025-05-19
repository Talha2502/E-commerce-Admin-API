from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ecommerce_admin_api.app.database import get_db
from ecommerce_admin_api.app.schemas import inventory as schemas
from ecommerce_admin_api.app.services import inventory as service

# setup router
router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)


@router.get("/", response_model=List[schemas.Inventory])
def get_inventory(skip: int = 0, limit: int = 100, warehouse: str = None, db: Session = Depends(get_db)):
    """Get all inventory items, can filter by warehouse"""
    return service.get_inventory(db=db, skip=skip, limit=limit, warehouse=warehouse)


@router.get("/low-stock", response_model=List[schemas.Inventory])
def get_low_stock(db: Session = Depends(get_db)):
    """Get items with stock below reorder level"""
    return service.get_low_stock(db=db)


@router.put("/{product_id}", response_model=schemas.Inventory)
def update_inventory(product_id: int, inventory: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    """Update inventory levels"""
    db_inventory = service.get_inventory_by_product(db=db, product_id=product_id)
    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory for this product not found"
        )
    return service.update_inventory(db=db, product_id=product_id, inventory=inventory)


@router.post("/restock", response_model=schemas.Inventory)
def restock_inventory(restock: schemas.InventoryUpdate, product_id: int, db: Session = Depends(get_db)):
    """Record inventory restock"""
    db_inventory = service.get_inventory_by_product(db=db, product_id=product_id)
    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory for this product not found"
        )
    return service.restock_inventory(db=db, product_id=product_id, restock=restock)


@router.get("/history/{product_id}")
def get_inventory_history(product_id: int, db: Session = Depends(get_db)):
    """Get inventory change history for a product"""
    return service.get_inventory_history(db=db, product_id=product_id)