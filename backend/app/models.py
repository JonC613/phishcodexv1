from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlmodel import Column, DateTime, SQLModel, String


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    showdate: str = Field(index=True, sa_column=Column(String, nullable=False))
    display_name: Optional[str] = Field(default=None, sa_column=Column(String, nullable=True))
    body: str = Field(sa_column=Column(String, nullable=False))
    ip_hash: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(
        default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=False))
    )


class CommentCreate(BaseModel):
    display_name: Optional[str] = None
    body: str


class CommentRead(BaseModel):
    id: int
    showdate: str
    display_name: Optional[str] = None
    body: str
    created_at: datetime


class ShowCard(BaseModel):
    showdate: str
    venue: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    showid: Optional[int] = None


class PaginatedShows(BaseModel):
    items: List[ShowCard]
    next_cursor: Optional[str]


class Song(BaseModel):
    title: str
    position: int


class SetlistSet(BaseModel):
    name: str
    songs: List[Song]


class ShowDetailResponse(BaseModel):
    show: ShowCard
    setlist: List[SetlistSet]
    relisten: dict


class RelistenSongResponse(BaseModel):
    mapping_status: str
    relisten_url: Optional[str]
    fallback_url: str
    track_found: bool
    fallback_show: bool
