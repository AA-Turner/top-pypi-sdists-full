"""``search_stock_images`` — reusable stock-photo search (Unsplash).

A plain async function with no graph/AppContext coupling, so any caller — an LLM
tool, a workflow node, a script — can fetch real photos for a query. The host
supplies the Unsplash key (``UNSPLASH_ACCESS_KEY`` env, or an explicit override);
end users never need their own. Attribution fields are surfaced because the
Unsplash licence requires crediting the photographer.

This is the single source of the Unsplash HTTP + parse logic. The matrx-graph
``media.stock_image.search`` node delegates here (see
``graph_nodes/stock_image_actions.py``) — do not duplicate the call elsewhere.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"


def resolve_unsplash_key(explicit: str | None = None) -> str | None:
    """Explicit override first, then the host process ``UNSPLASH_ACCESS_KEY``."""
    if explicit:
        return explicit
    return os.environ.get("UNSPLASH_ACCESS_KEY")


def parse_stock_image_item(item: dict[str, Any]) -> dict[str, Any]:
    """Map one raw Unsplash search result into a provider-agnostic dict."""
    urls = item.get("urls") or {}
    user = item.get("user") or {}
    user_links = user.get("links") or {}
    return {
        "url_full": str(urls.get("full") or urls.get("raw") or ""),
        "url_regular": str(urls.get("regular") or urls.get("full") or ""),
        "url_thumb": str(urls.get("thumb") or urls.get("small") or ""),
        "width": int(item.get("width") or 0),
        "height": int(item.get("height") or 0),
        "description": item.get("description") or item.get("alt_description"),
        "photographer_name": user.get("name") or None,
        "photographer_url": user_links.get("html") or None,
        "source": "unsplash",
        "source_id": str(item.get("id") or ""),
    }


async def search_stock_images(
    query: str,
    *,
    api_key: str | None = None,
    per_page: int = 5,
    page: int = 1,
    orientation: str = "any",
    color: str | None = None,
    timeout: float = 20.0,
) -> dict[str, Any]:
    """Search Unsplash. Returns a dict with ``status`` (success|error), ``images``
    (list of parsed dicts), ``total``, ``total_pages``, ``query`` and ``error``.

    Never raises for an empty/blank query or a missing key — those degrade to a
    structured ``status="error"`` result so optional-enrichment callers can skip.
    """
    q = (query or "").strip()
    if not q:
        return {
            "status": "error",
            "images": [],
            "total": 0,
            "total_pages": 0,
            "query": "",
            "error": "No query provided — stock image search skipped.",
        }

    key = resolve_unsplash_key(api_key)
    if not key:
        return {
            "status": "error",
            "images": [],
            "total": 0,
            "total_pages": 0,
            "query": q,
            "error": (
                "No Unsplash key available — host should set UNSPLASH_ACCESS_KEY "
                "or pass api_key. Get a host key at https://unsplash.com/developers."
            ),
        }

    params: dict[str, Any] = {"query": q, "per_page": per_page, "page": page}
    if orientation and orientation != "any":
        params["orientation"] = orientation
    if color:
        params["color"] = color
    headers = {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"}

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(UNSPLASH_SEARCH_URL, params=params, headers=headers)
        if response.status_code >= 400:
            return {
                "status": "error",
                "images": [],
                "total": 0,
                "total_pages": 0,
                "query": q,
                "error": f"Unsplash returned {response.status_code}: {response.text[:200]}",
            }
        data = response.json()
    except httpx.HTTPError as e:
        return {
            "status": "error",
            "images": [],
            "total": 0,
            "total_pages": 0,
            "query": q,
            "error": f"HTTP error: {type(e).__name__}: {e}",
        }

    images: list[dict[str, Any]] = []
    for item in data.get("results", []):
        try:
            images.append(parse_stock_image_item(item))
        except Exception:  # noqa: BLE001 — defensive against provider shape drift
            continue

    return {
        "status": "success",
        "images": images,
        "total": int(data.get("total", 0) or 0),
        "total_pages": int(data.get("total_pages", 0) or 0),
        "query": q,
        "error": None,
    }
