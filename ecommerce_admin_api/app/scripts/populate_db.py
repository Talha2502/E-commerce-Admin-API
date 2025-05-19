import sys
import os
import random
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from sqlalchemy.orm import Session
from ecommerce_admin_api.app.database import SessionLocal, engine, Base
from ecommerce_admin_api.app.models.product import Product
from ecommerce_admin_api.app.models.inventory import Inventory
from ecommerce_admin_api.app.models.sale import Sale

# create tables
Base.metadata.create_all(bind=engine)

# sample data
products = [
    {
        "name": "Wireless Earbuds",
        "description": "Noise-cancelling wireless earbuds with long battery life",
        "price": 79.99,
        "category": "Electronics",
        "sku": "ELEC-001"
    },
    {
        "name": "Smart Watch",
        "description": "Fitness tracking smartwatch with heart rate monitor",
        "price": 149.99,
        "category": "Electronics",
        "sku": "ELEC-002"
    },
    {
        "name": "Bluetooth Speaker",
        "description": "Portable waterproof bluetooth speaker",
        "price": 59.99,
        "category": "Electronics",
        "sku": "ELEC-003"
    },
    {
        "name": "Cotton T-Shirt",
        "description": "Comfortable 100% cotton t-shirt",
        "price": 19.99,
        "category": "Clothing",
        "sku": "CLTH-001"
    },
    {
        "name": "Denim Jeans",
        "description": "Classic straight fit denim jeans",
        "price": 49.99,
        "category": "Clothing",
        "sku": "CLTH-002"
    },
    {
        "name": "Running Shoes",
        "description": "Lightweight running shoes with cushioned soles",
        "price": 89.99,
        "category": "Footwear",
        "sku": "FOOT-001"
    },
    {
        "name": "Coffee Maker",
        "description": "Programmable coffee maker with timer",
        "price": 69.99,
        "category": "Kitchen",
        "sku": "KTCH-001"
    },
    {
        "name": "Blender",
        "description": "High-speed blender for smoothies and soups",
        "price": 49.99,
        "category": "Kitchen",
        "sku": "KTCH-002"
    },
    {
        "name": "Yoga Mat",
        "description": "Non-slip yoga mat with carrying strap",
        "price": 29.99,
        "category": "Fitness",
        "sku": "FITN-001"
    },
    {
        "name": "Dumbbells Set",
        "description": "Set of adjustable dumbbells for home workouts",
        "price": 119.99,
        "category": "Fitness",
        "sku": "FITN-002"
    }
]

# sales channels
channels = ["Amazon", "Walmart", "Direct", "eBay"]

# function to populate database
def populate_db():
    db = SessionLocal()
    try:
        # check if products already exist
        existing = db.query(Product).first()
        if existing:
            print("Database already contains data. Skipping population.")
            return
        
        # add products
        db_products = []
        for product_data in products:
            product = Product(**product_data)
            db.add(product)
            db_products.append(product)
        
        # commit to get product IDs
        db.commit()
        
        # add inventory for each product
        for product in db_products:
            inventory = Inventory(
                product_id=product.id,
                quantity=random.randint(10, 100),
                reorder_level=random.randint(5, 20),
                warehouse="main"
            )
            db.add(inventory)
        
        # commit inventory
        db.commit()
        
        # generate sales data (last 90 days)
        today = datetime.now().date()
        for day in range(90):
            sale_date = today - timedelta(days=day)
            # multiple sales per day
            for _ in range(random.randint(5, 15)):
                product = random.choice(db_products)
                quantity = random.randint(1, 5)
                unit_price = product.price * (1 - random.uniform(0, 0.2))  # random discount
                channel = random.choice(channels)
                
                sale = Sale(
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_amount=quantity * unit_price,
                    sale_date=sale_date,
                    channel=channel
                )
                db.add(sale)
        
        # final commit
        db.commit()
        print("Database populated successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Populating database with sample data...")
    populate_db()