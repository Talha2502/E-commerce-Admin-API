from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta

from ecommerce_admin_api.app.database import get_db
from ecommerce_admin_api.app.schemas import sales as schemas
from ecommerce_admin_api.app.services import sales as service

# setup router
router = APIRouter(
    prefix="/sales",
    tags=["sales"]
)


@router.post("/", response_model=schemas.Sale, status_code=status.HTTP_201_CREATED)
def record_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    """Record a new sale"""
    return service.create_sale(db=db, sale=sale)


@router.get("/", response_model=List[schemas.Sale])
def get_sales(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    channel: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get sales with various filters
    """
    return service.get_sales(
        db=db, 
        skip=skip, 
        limit=limit, 
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        category=category,
        channel=channel
    )


@router.get("/analytics/revenue", response_model=schemas.SaleAnalytics)
def get_revenue_analytics(
    period: str = Query(..., description="daily, weekly, monthly, or yearly"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    channel: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get revenue analytics by period
    """
    if not start_date:
        # default to last 30 days if not specified
        start_date = datetime.now().date() - timedelta(days=30)
    
    if not end_date:
        end_date = datetime.now().date()
        
    return service.get_revenue_analytics(
        db=db,
        period=period,
        start_date=start_date,
        end_date=end_date,
        category=category,
        channel=channel
    )


@router.get("/analytics/compare", response_model=List[schemas.SaleAnalytics])
def compare_revenue(
    period1_start: date,
    period1_end: date,
    period2_start: date,
    period2_end: date,
    category: Optional[str] = None,
    channel: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Compare revenue between two periods
    """
    return service.compare_revenue(
        db=db,
        period1_start=period1_start,
        period1_end=period1_end,
        period2_start=period2_start,
        period2_end=period2_end,
        category=category,
        channel=channel
    )


@router.get("/by-product", response_model=List[schemas.SaleAnalytics])
def get_sales_by_product(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top selling products
    """
    if not start_date:
        # default to last 30 days
        start_date = datetime.now().date() - timedelta(days=30)
    
    if not end_date:
        end_date = datetime.now().date()
        
    return service.get_sales_by_product(
        db=db,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )


@router.get("/by-category", response_model=List[schemas.SaleAnalytics])
def get_sales_by_category(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get sales by product category
    """
    if not start_date:
        # default to last 30 days
        start_date = datetime.now().date() - timedelta(days=30)
    
    if not end_date:
        end_date = datetime.now().date()
        
    return service.get_sales_by_category(
        db=db,
        start_date=start_date,
        end_date=end_date
    )