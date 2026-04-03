# Trigger reload
from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from app.database import engine, Base
from app.auth import auth_router
from app.customers import customers_router
from app.products import products_router
from app.sales import sales_router
from app.payments import payments_router
from app.reports import reports_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory & Dept Tracking")
router = APIRouter()

@app.get("/health")
async def index():
    return {"status": "ok"}

# showing directory, make sure to create __init__.py, and route.py in each folder
app.include_router(auth_router,prefix='/auth', tags=['auth'])
app.include_router(customers_router, prefix='/customers', tags=['customers'])
app.include_router(products_router, prefix='/products', tags=['products'])
app.include_router(sales_router, prefix='/sales', tags=['sales'])
app.include_router(payments_router, prefix='/payments', tags=['payments'])
app.include_router(reports_router, prefix='/reports', tags=['reports'])