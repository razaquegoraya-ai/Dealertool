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

def test_create_listing(client, db):
    response = client.post(
        "/api/listings/",
        json={
            "title": "Test Car",
            "description": "Test Description",
            "price": 25000,
            "status": "active"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Car"
    assert data["price"] == 25000

def test_get_listings(client, db):
    response = client.get("/api/listings/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_listing(client, db):
    # First create a listing
    create_response = client.post(
        "/api/listings/",
        json={
            "title": "Test Car 2",
            "description": "Test Description 2",
            "price": 30000,
            "status": "active"
        }
    )
    listing_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/listings/{listing_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Car 2"
    assert data["price"] == 30000

def test_update_listing(client, db):
    # First create a listing
    create_response = client.post(
        "/api/listings/",
        json={
            "title": "Test Car 3",
            "description": "Test Description 3",
            "price": 35000,
            "status": "active"
        }
    )
    listing_id = create_response.json()["id"]
    
    # Then update it
    response = client.put(
        f"/api/listings/{listing_id}",
        json={
            "title": "Updated Car",
            "description": "Updated Description",
            "price": 40000,
            "status": "active"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Car"
    assert data["price"] == 40000

def test_delete_listing(client, db):
    # First create a listing
    create_response = client.post(
        "/api/listings/",
        json={
            "title": "Test Car 4",
            "description": "Test Description 4",
            "price": 45000,
            "status": "active"
        }
    )
    listing_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/api/listings/{listing_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/listings/{listing_id}")
    assert get_response.status_code == 404 