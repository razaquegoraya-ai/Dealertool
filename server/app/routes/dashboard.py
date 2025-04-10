from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from ..models.listing import Listing as ListingModel

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_listings = db.query(ListingModel).count()
    watchlisted = db.query(ListingModel).filter(ListingModel.is_watchlisted == True).count()
    active_listings = db.query(ListingModel).filter(ListingModel.status == "active").count()
    
    return {
        "total_listings": total_listings,
        "watchlisted": watchlisted,
        "active_listings": active_listings
    }

@router.get("/price-stats")
def get_price_stats(db: Session = Depends(get_db)):
    # Get average price
    avg_price = db.query(ListingModel).filter(ListingModel.price.isnot(None)).with_entities(
        func.avg(ListingModel.price)
    ).scalar() or 0
    
    # Get min and max prices
    min_price = db.query(ListingModel).filter(ListingModel.price.isnot(None)).with_entities(
        func.min(ListingModel.price)
    ).scalar() or 0
    
    max_price = db.query(ListingModel).filter(ListingModel.price.isnot(None)).with_entities(
        func.max(ListingModel.price)
    ).scalar() or 0
    
    return {
        "average_price": round(float(avg_price), 2),
        "min_price": round(float(min_price), 2),
        "max_price": round(float(max_price), 2)
    }

@router.post("/margin-forecast")
def get_margin_forecast(
    purchase_price: float,
    target_margin: float,
    db: Session = Depends(get_db)
):
    """
    Calculate potential selling price based on purchase price and target margin
    """
    try:
        # Get average price for similar listings
        avg_price = db.query(ListingModel).filter(
            ListingModel.price.isnot(None),
            ListingModel.price >= purchase_price * 0.8,
            ListingModel.price <= purchase_price * 1.2
        ).with_entities(
            func.avg(ListingModel.price)
        ).scalar() or purchase_price

        # Calculate target selling price
        target_price = purchase_price * (1 + target_margin/100)
        
        # Calculate potential profit
        potential_profit = target_price - purchase_price
        
        return {
            "purchase_price": purchase_price,
            "target_margin": target_margin,
            "target_price": round(target_price, 2),
            "potential_profit": round(potential_profit, 2),
            "market_average": round(float(avg_price), 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 