import logging
from typing import Dict, List, Optional, Sequence
from urllib.parse import urlparse, urlunparse

import requests

logger = logging.getLogger(__name__)


def derive_entity_counts_url(gms_base_or_publish_url: str) -> str:
    """Map a GMS base or .../openapi/v1/billing/usage URL → entities/counts."""
    parsed = urlparse(gms_base_or_publish_url)
    path = parsed.path or ""
    marker = "/openapi/v1/"
    idx = path.find(marker)
    if idx >= 0:
        new_path = path[: idx + len(marker)] + "entities/counts"
    else:
        new_path = "/openapi/v1/entities/counts"
    return urlunparse(parsed._replace(path=new_path, params="", query="", fragment=""))


def fetch_entity_counts(
    url: str,
    authorization: str,
    entity_types: Sequence[str],
    timeout_seconds: float = 30.0,
) -> Optional[List[Dict]]:
    """GET OpenAPI entity counts; returns counts list or None on failure.

    ``authorization`` is the full ``Authorization`` header value (e.g.
    ``Bearer <token>`` or DataHub system ``Basic <id>:<secret>``).
    """
    params = [("types", t) for t in entity_types]
    headers = {"Authorization": authorization, "Accept": "application/json"}
    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=timeout_seconds
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        logger.warning("OpenAPI entity counts fallback failed: %s", exc)
        return None
    counts = payload.get("counts") if isinstance(payload, dict) else None
    if not isinstance(counts, list):
        logger.warning("OpenAPI entity counts response missing counts list")
        return None
    return counts


def resolve_counts_url(
    configured: Optional[str],
    gms_publish_url: Optional[str],
    gms_server: Optional[str] = None,
) -> Optional[str]:
    """Prefer explicit recipe URLs; else derive from graph ``server`` (default GMS)."""
    if configured:
        return configured
    if gms_publish_url:
        return derive_entity_counts_url(gms_publish_url)
    if gms_server:
        return derive_entity_counts_url(gms_server)
    return None
