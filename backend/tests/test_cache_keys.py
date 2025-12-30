import pytest

from app import phishnet_client


@pytest.mark.asyncio
async def test_recent_shows_cache(monkeypatch):
    phishnet_client.recent_cache.clear()
    calls = {"count": 0}

    async def fake_fetch(path):
        calls["count"] += 1
        return [
            {"showdate": "2024-01-01"},
            {"showdate": "2024-01-02"},
        ]

    monkeypatch.setattr(phishnet_client, "fetch_json", fake_fetch)

    first = await phishnet_client.recent_shows()
    second = await phishnet_client.recent_shows()

    assert first == second
    assert calls["count"] == 1


@pytest.mark.asyncio
async def test_show_detail_cache(monkeypatch):
    phishnet_client.show_detail_cache.clear()
    calls = {"count": 0}

    async def fake_fetch(path):
        calls["count"] += 1
        if "setlists" in path:
            return []
        return [{"showdate": "2024-01-01", "venue": "Test"}]

    monkeypatch.setattr(phishnet_client, "fetch_json", fake_fetch)

    detail1 = await phishnet_client.get_show_detail("2024-01-01")
    detail2 = await phishnet_client.get_show_detail("2024-01-01")

    assert detail1 == detail2
    assert calls["count"] == 2  # one for show, one for setlist
