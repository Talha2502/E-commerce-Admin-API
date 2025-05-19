from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime

from ecommerce_admin_api.app.models.inventory import Inventory
from ecommerce_admin_api.app.schemas import inventory as schemas


def get_inventory_by_product(db: Session, product_id: int):
    """Get inventory for a specific product"""
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()


def get_inventory(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    warehouse: Optional[str] = None
):
    """Get inventory with optional warehouse filter"""
    query = db.query(Inventory)
    
    if warehouse:
        query = query.filter(Inventory.warehouse == warehouse)
        
    return query.offset(skip).limit(limit).all()


def get_low_stock(db: Session):
    """Get items with stock below reorder level"""
    return db.query(Inventory).filter(
        Inventory.quantity < Inventory.reorder_level
    ).all()


def update_inventory(db: Session, product_id: int, inventory: schemas.InventoryUpdate):
    """Update inventory details"""
    # get inventory
    db_inventory = get_inventory_by_product(db, product_id)
    
    # update fields that are set
    update_data = inventory.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inventory, key, value)
    
    # save changes
    db.commit()
    db.refresh(db_inventory)
    
    return db_inventory


def restock_inventory(db: Session, product_id: int, restock: schemas.InventoryUpdate):
    """Record inventory restock"""
    # get inventory
    db_inventory = get_inventory_by_product(db, product_id)
    
    # increment quantity if provided
    if restock.quantity:
        db_inventory.quantity += restock.quantity
    
    # update last restock date
    db_inventory.last_restock_date = datetime.now()
    
    # update other fields if provided
    if restock.reorder_level:
        db_inventory.reorder_level = restock.reorder_level
    
    if restock.warehouse:
        db_inventory.warehouse = restock.warehouse
    
    # save changes
    db.commit()
    db.refresh(db_inventory)
    
    return db_inventory


def get_inventory_history(db: Session, product_id: int):
    """
    Get inventory change history
    Note: This would require a separate table to track history
    For now, returning placeholder
    """
    # TODO: Implement inventory history tracking
    return {"message": "Inventory history tracking to be implemented"}