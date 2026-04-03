from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.sales.models import Sale
from app.sales.schemas import SaleCreate, SaleResponse
from app.products.models import Product
from app.customers.models import Customer

sales_router = APIRouter()

@sales_router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    # 1. Check if customer exists
    db_customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # 2. Check if product exists
    db_product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 3. Check for sufficient quantity
    if db_product.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient product quantity")
    
    # 4. Calculate total price
    total_price = db_product.price * sale.quantity
    
    # 5. Create sale record
    db_sale = Sale(
        customer_id=sale.customer_id,
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_price=total_price
    )
    
    # 6. Update product quantity
    db_product.quantity -= sale.quantity
    
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@sales_router.get("/", response_model=List[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()
