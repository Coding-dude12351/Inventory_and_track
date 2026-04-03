from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PaymentBase(BaseModel):
    sale_id: int
    amount: float
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)
