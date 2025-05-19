from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ecommerce_admin_api.app.database import Base


class Inventory(Base):
    # inventory table
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)  # current stock
    reorder_level = Column(Integer, default=10)  # when to reorder
    last_restock_date = Column(DateTime, nullable=True)
    warehouse = Column(String(100), default="main")  # storage location
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # back reference to product
    product = relationship("Product", back_populates="inventory")