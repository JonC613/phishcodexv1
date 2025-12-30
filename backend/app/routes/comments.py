import hashlib
import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from app.db import get_session
from app.models import Comment, CommentCreate, CommentRead

router = APIRouter(prefix="/api")

RATE_LIMIT = 10
WINDOW_SECONDS = 3600
_rate_cache: dict[str, list[float]] = {}


def _hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode()).hexdigest()


def _check_rate(ip: str):
    now = time.time()
    entries = [t for t in _rate_cache.get(ip, []) if now - t < WINDOW_SECONDS]
    if len(entries) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    entries.append(now)
    _rate_cache[ip] = entries


@router.get("/shows/{showdate}/comments", response_model=List[CommentRead])
async def list_comments(showdate: str, session: Session = Depends(get_session)):
    stmt = select(Comment).where(Comment.showdate == showdate).order_by(Comment.created_at.desc())
    results = session.exec(stmt).all()
    return [CommentRead(**c.dict()) for c in results]


@router.post("/shows/{showdate}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    showdate: str,
    payload: CommentCreate,
    request: Request,
    session: Session = Depends(get_session),
):
    client_ip = request.client.host if request.client else "unknown"
    ip_hash = _hash_ip(client_ip)
    _check_rate(ip_hash)
    if not payload.body.strip():
        raise HTTPException(status_code=400, detail="Body is required")
    comment = Comment(showdate=showdate, display_name=payload.display_name, body=payload.body.strip(), ip_hash=ip_hash)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return CommentRead(**comment.dict())
