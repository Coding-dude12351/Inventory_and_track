from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.payments.models import Payment
from app.payments.schemas import PaymentCreate, PaymentResponse
from app.sales.models import Sale

payments_router = APIRouter()

@payments_router.post("/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    # 1. Check if sale exists
    db_sale = db.query(Sale).filter(Sale.id == payment.sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # 2. Create payment record
    db_payment = Payment(**payment.model_dump())
    
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@payments_router.get("/", response_model=List[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()

@payments_router.get("/sale/{sale_id}", response_model=List[PaymentResponse])
def get_payments_for_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
        
    payments = db.query(Payment).filter(Payment.sale_id == sale_id).all()
    return payments
