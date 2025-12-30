import re
from typing import Optional

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://relisten.net/phish"


def normalize_title(title: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "", title.lower())
    return normalized


def build_show_url(showdate: str) -> str:
    parts = showdate.split("-")
    if len(parts) != 3:
        return BASE_URL
    year, month, day = parts
    return f"{BASE_URL}/{year}/{month}/{day}"


async def fetch_relisten_song_url(showdate: str, title: str, position: int = 0) -> dict:
    show_url = build_show_url(showdate)
    fallback_url = show_url
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(show_url)
            resp.raise_for_status()
    except Exception:
        return {
            "mapping_status": "fallback_show",
            "relisten_url": None,
            "fallback_url": fallback_url,
            "track_found": False,
            "fallback_show": True,
        }

    soup = BeautifulSoup(resp.text, "lxml")
    anchors = soup.find_all("a", href=True)
    matches = [a for a in anchors if normalize_title(a.text) == normalize_title(title)]
    if matches and position < len(matches):
        relisten_url = "https://relisten.net" + matches[position]["href"]
        return {
            "mapping_status": "track_found",
            "relisten_url": relisten_url,
            "fallback_url": fallback_url,
            "track_found": True,
            "fallback_show": False,
        }
    if matches:
        relisten_url = "https://relisten.net" + matches[-1]["href"]
        return {
            "mapping_status": "track_found",
            "relisten_url": relisten_url,
            "fallback_url": fallback_url,
            "track_found": True,
            "fallback_show": False,
        }
    return {
        "mapping_status": "fallback_show",
        "relisten_url": None,
        "fallback_url": fallback_url,
        "track_found": False,
        "fallback_show": True,
    }
