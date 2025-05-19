from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ecommerce_admin_api.app.database import Base


class Product(Base):
    # table name
    __tablename__ = "products"
    
    # basic product fields
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    category = Column(String(100), index=True)
    sku = Column(String(50), unique=True)  # unique product code
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # link to other tables - will setup these later
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    sales = relationship("Sale", back_populates="product")