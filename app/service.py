from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Inventory
from .cache import InventoryCache

class InventoryService:
    def __init__(self, cache=None):
        self.cache = cache or InventoryCache()

    def create(self, db: Session, sku, warehouse_id, quantity):
        item = Inventory(sku=sku, warehouse_id=warehouse_id, quantity=quantity)
        db.add(item)
        db.commit()
        db.refresh(item)
        self.cache.delete(self.key(sku, warehouse_id))
        return item

    def get(self, db: Session, sku, warehouse_id):
        key = self.key(sku, warehouse_id)
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        item = db.scalar(select(Inventory).where(
            Inventory.sku == sku, Inventory.warehouse_id == warehouse_id
        ))
        if item is None:
            return None
        data = {"id": item.id, "sku": item.sku, "warehouse_id": item.warehouse_id, "quantity": item.quantity}
        self.cache.set(key, data)
        return data

    def update_stock(self, db: Session, sku, warehouse_id, delta):
        item = db.scalar(select(Inventory).where(
            Inventory.sku == sku, Inventory.warehouse_id == warehouse_id
        ).with_for_update())
        if item is None:
            return None
        new_quantity = item.quantity + delta
        if new_quantity < 0:
            raise ValueError("insufficient stock")
        item.quantity = new_quantity
        db.commit()
        db.refresh(item)
        self.cache.delete(self.key(sku, warehouse_id))
        return item

    @staticmethod
    def key(sku, warehouse_id):
        return f"inventory:{warehouse_id}:{sku}"
