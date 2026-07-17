"""Network-specific helpers for the v2 SDK."""

PRODUCTION_BASE_URL = "https://plato.so"


def is_production_base_url(base_url: str) -> bool:
    """Return whether a client base URL targets the production Plato API."""
    normalized_url = base_url.rstrip("/")
    if normalized_url.endswith("/api"):
        normalized_url = normalized_url[:-4]
    return normalized_url == PRODUCTION_BASE_URL
