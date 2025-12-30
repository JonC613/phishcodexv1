from collections import defaultdict
from typing import List

from fastapi import APIRouter, Query

from app import phishnet_client, relisten
from app.models import RelistenSongResponse, SetlistSet, ShowCard, ShowDetailResponse, Song

router = APIRouter(prefix="/api")


@router.get("/shows/{showdate}", response_model=ShowDetailResponse)
async def get_show(showdate: str):
    data = await phishnet_client.get_show_detail(showdate)
    show = ShowCard(**data["show"])
    setlist_raw: List[dict] = data.get("setlist_raw") or []
    grouped: dict[str, List[Song]] = defaultdict(list)
    for entry in setlist_raw:
        set_name = entry.get("set") or "Set"
        grouped[set_name].append(
            Song(title=entry.get("song") or "Unknown", position=len(grouped[set_name]) + 1)
        )
    setlist_sets = [SetlistSet(name=k, songs=v) for k, v in grouped.items()]
    return ShowDetailResponse(
        show=show,
        setlist=setlist_sets,
        relisten={"show_url": relisten.build_show_url(showdate)},
    )


@router.get("/shows/{showdate}/relisten/song", response_model=RelistenSongResponse)
async def map_song_relisten(showdate: str, title: str = Query(...), index: int = Query(0)):
    mapping = await relisten.fetch_relisten_song_url(showdate, title, position=index)
    return RelistenSongResponse(**mapping)
