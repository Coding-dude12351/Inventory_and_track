from pydantic import BaseModel

class InventorySummary(BaseModel):
    total_products_types: int
    total_items_in_stock: int
    total_estimated_value: float

class SalesSummary(BaseModel):
    total_sales_count: int
    total_revenue: float
