from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(80), index=True)
    warehouse_id: Mapped[str] = mapped_column(String(50), index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
