# Phish Show Finder

A minimal Phish.net-style v1 app to browse Phish shows, view setlists, open ReListen audio, and leave anonymous comments.

## Stack
- Backend: FastAPI, SQLModel, Postgres, httpx, cachetools
- Frontend: React (Vite), TypeScript, Fluent UI v9
- Infra: Docker Compose with web (Nginx + static assets), api, db

## Prerequisites
- Docker + Docker Compose

## Getting started
1. Copy the environment template and add your Phish.net API key:
   ```bash
   cp .env.example .env
   ```
2. Build and run everything:
   ```bash
   docker compose up --build
   ```
3. Frontend is available at http://localhost:5173 and proxies `/api` to the backend.

## Running backend tests locally
```bash
cd backend
pip install -r requirements.txt
pytest
```

## API highlights
- `GET /api/search?kind=year&q=1998` - search shows
- `GET /api/shows/{showdate}` - show detail + setlist
- `GET /api/shows/{showdate}/relisten/song?title=Tweezer&index=0` - map track to ReListen
- `GET/POST /api/shows/{showdate}/comments` - anonymous comments per show

## Notes
- In-memory caching honors separate TTLs for recent shows (15m), show detail (24h), and venue lookups (7d).
- Rate limiting for comments: max 10 comments per hour per IP hash.
