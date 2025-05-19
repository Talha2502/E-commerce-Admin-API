from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from typing import List, Optional
from datetime import date, timedelta

from ecommerce_admin_api.app.models.sale import Sale
from ecommerce_admin_api.app.models.product import Product
from ecommerce_admin_api.app.schemas import sales as schemas


def create_sale(db: Session, sale: schemas.SaleCreate):
    """Record a new sale"""
    # calculate total
    total_amount = sale.quantity * sale.unit_price
    
    # create sale record
    db_sale = Sale(
        product_id=sale.product_id,
        quantity=sale.quantity,
        unit_price=sale.unit_price,
        total_amount=total_amount,
        channel=sale.channel
    )
    
    # add to db
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    return db_sale


def get_sales(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None,
    channel: Optional[str] = None
):
    """Get sales with various filters"""
    # start with base query
    query = db.query(Sale)
    
    # apply date range filter
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    
    if end_date:
        # include the entire end date
        next_day = end_date + timedelta(days=1)
        query = query.filter(Sale.sale_date < next_day)
    
    # filter by product
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    
    # filter by channel
    if channel:
        query = query.filter(Sale.channel == channel)
    
    # filter by category (requires join)
    if category:
        query = query.join(Product).filter(Product.category == category)
    
    # get results
    return query.offset(skip).limit(limit).all()


def get_revenue_analytics(
    db: Session,
    period: str,
    start_date: date,
    end_date: date,
    category: Optional[str] = None,
    channel: Optional[str] = None
):
    """Get revenue analytics by period"""
    # base query to sum sales and count quantity
    query = db.query(
        func.sum(Sale.total_amount).label("total_sales"),
        func.sum(Sale.quantity).label("total_quantity")
    )
    
    # apply date range filter
    next_day = end_date + timedelta(days=1)
    query = query.filter(and_(
        Sale.sale_date >= start_date,
        Sale.sale_date < next_day
    ))
    
    # filter by channel
    if channel:
        query = query.filter(Sale.channel == channel)
    
    # filter by category (requires join)
    if category:
        query = query.join(Product).filter(Product.category == category)
    
    # execute query
    result = query.first()
    
    # create response object
    return {
        "total_sales": result.total_sales or 0,
        "total_quantity": result.total_quantity or 0,
        "period": period
    }


def compare_revenue(
    db: Session,
    period1_start: date,
    period1_end: date,
    period2_start: date,
    period2_end: date,
    category: Optional[str] = None,
    channel: Optional[str] = None
):
    """Compare revenue between two periods"""
    # get revenue for period 1
    period1 = get_revenue_analytics(
        db=db,
        period="period1",
        start_date=period1_start,
        end_date=period1_end,
        category=category,
        channel=channel
    )
    
    # get revenue for period 2
    period2 = get_revenue_analytics(
        db=db,
        period="period2",
        start_date=period2_start,
        end_date=period2_end,
        category=category,
        channel=channel
    )
    
    # return both periods for comparison
    return [period1, period2]


def get_sales_by_product(
    db: Session,
    start_date: date,
    end_date: date,
    limit: int = 10
):
    """Get top selling products"""
    # query to get sales by product
    query = db.query(
        Sale.product_id,
        func.sum(Sale.total_amount).label("total_sales"),
        func.sum(Sale.quantity).label("total_quantity")
    )
    
    # apply date range filter
    next_day = end_date + timedelta(days=1)
    query = query.filter(and_(
        Sale.sale_date >= start_date,
        Sale.sale_date < next_day
    ))
    
    # group by product and order by sales
    query = query.group_by(Sale.product_id).order_by(
        func.sum(Sale.total_amount).desc()
    )
    
    # limit to top products
    results = query.limit(limit).all()
    
    # format results
    return [
        {
            "product_id": result.product_id,
            "total_sales": result.total_sales,
            "total_quantity": result.total_quantity,
            "period": f"{start_date} to {end_date}"
        }
        for result in results
    ]


def get_sales_by_category(
    db: Session,
    start_date: date,
    end_date: date
):
    """Get sales by product category"""
    # query to get sales by category
    query = db.query(
        Product.category,
        func.sum(Sale.total_amount).label("total_sales"),
        func.sum(Sale.quantity).label("total_quantity")
    )
    
    # apply date range filter
    next_day = end_date + timedelta(days=1)
    query = query.filter(and_(
        Sale.sale_date >= start_date,
        Sale.sale_date < next_day
    ))
    
    # join with products and group by category
    query = query.join(Product).group_by(Product.category).order_by(
        func.sum(Sale.total_amount).desc()
    )
    
    # get results
    results = query.all()
    
    # format results
    return [
        {
            "category": result.category,
            "total_sales": result.total_sales,
            "total_quantity": result.total_quantity,
            "period": f"{start_date} to {end_date}"
        }
        for result in results
    ]