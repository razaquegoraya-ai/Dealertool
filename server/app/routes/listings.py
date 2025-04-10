from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from ..db import get_db
from ..models.listing import Listing as ListingModel, ListingCreate, ListingUpdate, ListingInDB
from ..services.scraper import scrape_mobile_de
from ..services.scoring import score_listing

router = APIRouter()

class ScanParams(BaseModel):
    max_price: float = 20000
    max_mileage: int = 150000
    radius: int = 300

@router.post("/", response_model=ListingInDB)
def create_listing(listing: ListingCreate, db: Session = Depends(get_db)):
    db_listing = ListingModel(**listing.model_dump())
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@router.get("/", response_model=List[ListingInDB])
def get_listings(db: Session = Depends(get_db)):
    listings = db.query(ListingModel).all()
    return listings

@router.get("/{listing_id}", response_model=ListingInDB)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.put("/{listing_id}", response_model=ListingInDB)
def update_listing(listing_id: int, listing: ListingUpdate, db: Session = Depends(get_db)):
    db_listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    update_data = listing.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_listing, key, value)
    
    db.commit()
    db.refresh(db_listing)
    return db_listing

@router.delete("/{listing_id}")
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted"}

@router.get("/scan")
async def scan_listings(
    max_price: float = Query(20000, description="Maximum price in euros"),
    max_mileage: int = Query(150000, description="Maximum mileage in kilometers"),
    radius: int = Query(300, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    """
    Scan mobile.de for new listings based on criteria
    """
    try:
        listings = await scrape_mobile_de(max_price, max_mileage, radius)
        return {"listings": listings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{listing_id}/score")
async def get_listing_score(
    listing_id: int,
    db: Session = Depends(get_db)
):
    """
    Get score and recommendation for a specific listing
    """
    try:
        score, recommendation = await score_listing(listing_id)
        return {
            "score": score,
            "recommendation": recommendation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 