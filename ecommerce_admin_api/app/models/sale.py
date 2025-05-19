from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ecommerce_admin_api.app.database import Base


class Sale(Base):
    # sales tracking
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)  # price at time of sale
    total_amount = Column(Float)
    sale_date = Column(DateTime, default=func.now())
    channel = Column(String(50))  # amazon, walmart, etc
    
    # link back to product
    product = relationship("Product", back_populates="sales")