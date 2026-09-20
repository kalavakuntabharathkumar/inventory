import os
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .schemas import InventoryCreate, InventoryOut, StockUpdate
from .service import InventoryService

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Real-Time Inventory Sync API")
service = InventoryService()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/inventory", response_model=InventoryOut)
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    existing = service.get(db, payload.sku, payload.warehouse_id)
    if existing:
        raise HTTPException(409, "Inventory record already exists")
    return service.create(db, payload.sku, payload.warehouse_id, payload.quantity)

@app.get("/inventory/{warehouse_id}/{sku}", response_model=InventoryOut)
def get_inventory(warehouse_id: str, sku: str, db: Session = Depends(get_db)):
    item = service.get(db, sku, warehouse_id)
    if item is None:
        raise HTTPException(404, "Inventory record not found")
    return item

@app.patch("/inventory/{warehouse_id}/{sku}", response_model=InventoryOut)
def update_inventory(warehouse_id: str, sku: str, payload: StockUpdate, db: Session = Depends(get_db)):
    try:
        item = service.update_stock(db, sku, warehouse_id, payload.delta)
    except ValueError as exc:
        raise HTTPException(409, str(exc))
    if item is None:
        raise HTTPException(404, "Inventory record not found")
    return item
