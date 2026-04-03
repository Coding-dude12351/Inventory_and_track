from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False) # e.g., "cash", "card"
    payment_date = Column(DateTime, default=datetime.utcnow)

    sale = relationship("app.sales.models.Sale")
