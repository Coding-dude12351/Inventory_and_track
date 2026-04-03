from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductResponse

products_router = APIRouter()

@products_router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@products_router.get("/", response_model=list[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products