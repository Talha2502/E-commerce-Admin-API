from sqlalchemy.orm import Session
from typing import List, Optional

from ecommerce_admin_api.app.models.product import Product
from ecommerce_admin_api.app.schemas import products as schemas


def get_product(db: Session, product_id: int):
    """Get a product by ID"""
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_sku(db: Session, sku: str):
    """Find a product by its SKU"""
    return db.query(Product).filter(Product.sku == sku).first()


def get_products(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None
):
    """Get products with optional category filter"""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
        
    return query.offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    """Add a new product"""
    # create product from schema
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        sku=product.sku
    )
    
    # add to db
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    """Update a product's details"""
    # get the product
    db_product = get_product(db, product_id)
    
    # update fields that are set
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    # save changes
    db.commit()
    db.refresh(db_product)
    
    return db_product


def delete_product(db: Session, product_id: int):
    """Remove a product"""
    db_product = get_product(db, product_id)
    db.delete(db_product)
    db.commit()