from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import listings, watchlist, dashboard
from .db import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DealerTool API",
    description="API for car market analysis and dealer tools",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers with correct prefixes
app.include_router(listings.router, prefix="/api/listings", tags=["listings"])
app.include_router(watchlist.router, prefix="/api/watchlist", tags=["watchlist"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Dealer Tool API"} 