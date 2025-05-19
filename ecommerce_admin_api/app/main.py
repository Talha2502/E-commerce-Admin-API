import sys
import os

# Add the project root to the Python path to make imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ecommerce_admin_api.app.routers import products, inventory, sales
from ecommerce_admin_api.app.models import product, inventory, sale
from ecommerce_admin_api.app.database import engine, Base

# create tables in database
Base.metadata.create_all(bind=engine)

# initialize app
app = FastAPI(title="E-commerce Admin API")

# setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(products.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")
app.include_router(sales.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to E-commerce Admin API"}