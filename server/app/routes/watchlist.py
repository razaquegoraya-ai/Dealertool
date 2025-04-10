from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from ..models.listing import Listing as ListingModel, ListingInDB

router = APIRouter()

@router.get("/", response_model=List[ListingInDB])
def get_watchlist(db: Session = Depends(get_db)):
    listings = db.query(ListingModel).filter(ListingModel.is_watchlisted == True).all()
    return listings

@router.post("/{listing_id}")
def add_to_watchlist(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    listing.is_watchlisted = True
    db.commit()
    return {"message": "Listing added to watchlist"}

@router.delete("/{listing_id}")
def remove_from_watchlist(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    listing.is_watchlisted = False
    db.commit()
    return {"message": "Listing removed from watchlist"} 