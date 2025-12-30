import datetime
import os
from typing import Dict, List, Optional

import httpx
from cachetools import TTLCache

API_BASE = "https://api.phish.net/v5"
API_KEY = os.getenv("PHISHNET_API_KEY", "demo")

# Caches tuned per spec
recent_cache = TTLCache(maxsize=128, ttl=900)  # 15 minutes
show_detail_cache = TTLCache(maxsize=512, ttl=86400)  # 24 hours
venue_cache = TTLCache(maxsize=256, ttl=604800)  # 7 days


async def fetch_json(path: str) -> Dict:
    url = f"{API_BASE}/{path}.json"
    params = {"apikey": API_KEY}
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data") or []


def normalize_show(obj: Dict) -> Dict:
    return {
        "showdate": obj.get("showdate"),
        "venue": obj.get("venue"),
        "city": obj.get("city"),
        "state": obj.get("state"),
        "country": obj.get("country"),
        "showid": obj.get("showid"),
    }


async def recent_shows() -> List[Dict]:
    key = "recent"
    if key in recent_cache:
        return recent_cache[key]
    year = datetime.datetime.utcnow().year
    items = await fetch_json(f"shows/showyear/{year}") or []
    if not items:
        items = await fetch_json(f"shows/showyear/{year - 1}") or []
    items = sorted(items, key=lambda x: x.get("showdate"), reverse=True)
    recent_cache[key] = [normalize_show(s) for s in items[:50]]
    return recent_cache[key]


async def get_show_detail(showdate: str) -> Dict:
    if showdate in show_detail_cache:
        return show_detail_cache[showdate]
    show_data = await fetch_json(f"shows/showdate/{showdate}")
    setlist_data = await fetch_json(f"setlists/showdate/{showdate}")
    normalized_show = normalize_show(show_data[0] if show_data else {"showdate": showdate})
    result = {
        "show": normalized_show,
        "setlist_raw": setlist_data,
    }
    show_detail_cache[showdate] = result
    return result


async def search_year(year: str) -> List[Dict]:
    return [normalize_show(s) for s in await fetch_json(f"shows/showyear/{year}")]


async def search_by_kind(kind: str, query: str) -> List[Dict]:
    if kind == "venue":
        return await search_venue(query)
    if kind == "year":
        return await search_year(query)
    path = f"shows/{kind}/{query}"
    shows = await fetch_json(path)
    if shows:
        return [normalize_show(s) for s in shows]
    if kind in {"city", "state", "country"}:
        venues = await fetch_json(f"venues/{kind}/{query}")
        results: List[Dict] = []
        for v in venues:
            vids = v.get("venueid")
            if not vids:
                continue
            v_shows = await fetch_json(f"shows/venueid/{vids}")
            results.extend(normalize_show(s) for s in v_shows)
        return results
    return []


async def search_venue(query: str) -> List[Dict]:
    cache_key = f"venue:{query}"
    if cache_key in venue_cache:
        return venue_cache[cache_key]
    results: List[Dict] = []
    if query.isdigit():
        results = [normalize_show(s) for s in await fetch_json(f"shows/venueid/{query}")]
    else:
        slug_path = f"venues/slug/{query}"
        name_path = f"venues/name/{query}"
        venues = await fetch_json(slug_path)
        if not venues:
            venues = await fetch_json(name_path)
        if venues:
            for v in venues:
                vid = v.get("venueid")
                if vid:
                    v_shows = await fetch_json(f"shows/venueid/{vid}")
                    results.extend(normalize_show(s) for s in v_shows)
        else:
            raise ValueError(
                "No venue match. Exact venue search may not be supported; try venue ID."
            )
    venue_cache[cache_key] = results
    return results
