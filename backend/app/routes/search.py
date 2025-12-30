from fastapi import APIRouter, HTTPException, Query

from app.models import PaginatedShows, ShowCard
from app import phishnet_client

router = APIRouter(prefix="/api")

PAGE_SIZE = 10


@router.get("/search", response_model=PaginatedShows)
async def search_shows(kind: str = Query("recent"), q: str = Query(""), cursor: str | None = None):
    try:
        if kind == "recent" or not q:
            shows = await phishnet_client.recent_shows()
        else:
            shows = await phishnet_client.search_by_kind(kind, q)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    start = int(cursor) if cursor else 0
    end = start + PAGE_SIZE
    items = shows[start:end]
    next_cursor = str(end) if end < len(shows) else None
    return PaginatedShows(items=[ShowCard(**s) for s in items], next_cursor=next_cursor)
