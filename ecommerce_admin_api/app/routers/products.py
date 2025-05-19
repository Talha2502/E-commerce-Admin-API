from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ecommerce_admin_api.app.database import get_db
from ecommerce_admin_api.app.schemas import products as schemas
from ecommerce_admin_api.app.services import products as service

# setup router
router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to the system"""
    return service.create_product(db=db, product=product)


@router.get("/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, category: str = None, db: Session = Depends(get_db)):
    """Get all products, can filter by category"""
    return service.get_products(db=db, skip=skip, limit=limit, category=category)


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = service.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """Update product details"""
    db_product = service.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return service.update_product(db=db, product_id=product_id, product=product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Remove a product"""
    db_product = service.get_product(db=db, product_id=product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    service.delete_product(db=db, product_id=product_id)
    return None