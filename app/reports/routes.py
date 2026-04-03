from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.reports.schemas import InventorySummary, SalesSummary
from app.products.models import Product
from app.sales.models import Sale

reports_router = APIRouter()

@reports_router.get("/inventory", response_model=InventorySummary)
def get_inventory_report(db: Session = Depends(get_db)):
    # Calculate totals directly from the database
    total_types = db.query(func.count(Product.id)).scalar() or 0
    total_items = db.query(func.sum(Product.quantity)).scalar() or 0
    
    # Calculate total value (sum of quantity * price for each product)
    total_value = db.query(func.sum(Product.quantity * Product.price)).scalar() or 0.0
    
    return InventorySummary(
        total_products_types=total_types,
        total_items_in_stock=total_items,
        total_estimated_value=total_value
    )

@reports_router.get("/sales", response_model=SalesSummary)
def get_sales_report(db: Session = Depends(get_db)):
    # Calculate sales aggregates
    total_sales = db.query(func.count(Sale.id)).scalar() or 0
    total_revenue = db.query(func.sum(Sale.total_price)).scalar() or 0.0
    
    return SalesSummary(
        total_sales_count=total_sales,
        total_revenue=total_revenue
    )
