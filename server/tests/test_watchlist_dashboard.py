import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.listing import Listing as ListingModel
from app.db import SessionLocal, engine, Base

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    # Create test database tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_watchlist_operations(client, db):
    # First create a listing
    create_response = client.post(
        "/api/listings/",
        json={
            "title": "Watchlist Test Car",
            "description": "Watchlist Test Description",
            "price": 50000,
            "status": "active"
        }
    )
    listing_id = create_response.json()["id"]
    
    # Add to watchlist
    response = client.post(f"/api/watchlist/{listing_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Listing added to watchlist"
    
    # Get watchlist
    watchlist_response = client.get("/api/watchlist/")
    assert watchlist_response.status_code == 200
    watchlist_data = watchlist_response.json()
    assert len(watchlist_data) > 0
    assert any(item["id"] == listing_id for item in watchlist_data)
    
    # Remove from watchlist
    remove_response = client.delete(f"/api/watchlist/{listing_id}")
    assert remove_response.status_code == 200
    assert remove_response.json()["message"] == "Listing removed from watchlist"

def test_dashboard_stats(client, db):
    # Create some test listings
    for i in range(3):
        client.post(
            "/api/listings/",
            json={
                "title": f"Dashboard Test Car {i}",
                "description": f"Dashboard Test Description {i}",
                "price": 10000 * (i + 1),
                "status": "active"
            }
        )
    
    # Add one to watchlist
    listings = client.get("/api/listings/").json()
    client.post(f"/api/watchlist/{listings[0]['id']}")
    
    # Test dashboard stats
    stats_response = client.get("/api/dashboard/stats")
    assert stats_response.status_code == 200
    stats_data = stats_response.json()
    assert stats_data["total_listings"] >= 3
    assert stats_data["watchlisted"] >= 1
    assert stats_data["active_listings"] >= 3
    
    # Test price stats
    price_stats_response = client.get("/api/dashboard/price-stats")
    assert price_stats_response.status_code == 200
    price_data = price_stats_response.json()
    assert price_data["min_price"] > 0
    assert price_data["max_price"] > price_data["min_price"]
    assert price_data["average_price"] > 0 