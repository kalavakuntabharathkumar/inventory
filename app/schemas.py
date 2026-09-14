from pydantic import BaseModel, Field

class InventoryCreate(BaseModel):
    sku: str
    warehouse_id: str
    quantity: int = Field(ge=0)

class InventoryOut(InventoryCreate):
    id: int
    model_config = {"from_attributes": True}

class StockUpdate(BaseModel):
    delta: int
