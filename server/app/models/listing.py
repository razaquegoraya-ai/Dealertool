from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from pydantic import BaseModel, ConfigDict
from ..db import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    status = Column(String, default="active")
    is_watchlisted = Column(Boolean, default=False)
    mileage = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    url = Column(String, nullable=True)
    seller_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(String, nullable=True)
    score = Column(Integer, nullable=True)
    recommendation = Column(String, nullable=True)

class ListingBase(BaseModel):
    title: str
    description: str
    price: float
    status: str = "active"

class ListingCreate(ListingBase):
    pass

class ListingUpdate(ListingBase):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    status: str | None = None

class ListingInDB(ListingBase):
    id: int
    is_watchlisted: bool = False
    
    model_config = ConfigDict(from_attributes=True) 