# Dealer Tool

A comprehensive web application for car dealers to manage listings, track watchlists, and analyze market data.

## Features

- **Listings Management**: Add, edit, and delete vehicle listings
- **Watchlist**: Track vehicles of interest
- **Dashboard**: View market analysis and margin calculations
- **Search**: Find vehicles by make, model, year, and price range
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### Frontend
- React
- TypeScript
- Tailwind CSS
- Axios
- React Router

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dealer-tool.git
cd dealer-tool
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head
```

3. Set up the frontend:
```bash
cd client
npm install
```

### Running the Application

1. Start the backend server:
```bash
# From the root directory
uvicorn app.main:app --reload
```

2. Start the frontend development server:
```bash
# From the client directory
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Testing

### Backend Tests
```bash
# From the root directory
pytest
```

### Frontend Tests
```bash
# From the client directory
npm test
```

## Project Structure

```
dealer-tool/
├── alembic/              # Database migrations
├── app/                  # Backend application
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── schemas/         # Pydantic schemas
│   └── main.py          # FastAPI application
├── client/              # Frontend application
│   ├── public/          # Static files
│   ├── src/             # React source code
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── types/       # TypeScript types
│   └── package.json     # Frontend dependencies
├── tests/               # Backend tests
└── requirements.txt     # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/dealer-tool](https://github.com/yourusername/dealer-tool)
