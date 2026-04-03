from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SaleBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
    total_price: float
    sale_date: datetime

    model_config = ConfigDict(from_attributes=True)
