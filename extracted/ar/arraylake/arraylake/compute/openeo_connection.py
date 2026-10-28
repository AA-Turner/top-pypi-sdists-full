"""Helpers for ``Client.get_openeo_connection``.

Loaded only when the optional ``openeo`` dependency is installed.
"""

import logging
from typing import Any

from openeo.rest.auth.auth import BearerAuth

from arraylake.token import get_fresh_id_token


class CachedLoginBearerAuth(BearerAuth):  # type: ignore[misc,unused-ignore]  # untyped requests.AuthBase base in older openeo
    """Bearer auth from the cached ``al auth login`` session, refreshed before it expires.

    The token is re-read (and refreshed if needed) on every request, so long-running openEO
    sessions outlive a single ID token. openeo only sends a connection's auth to its own root
    URL, never to result asset hosts.
    """

    def __init__(self, service_uri: str):
        self.service_uri = service_uri
        super().__init__(bearer=get_fresh_id_token(service_uri))

    def __call__(self, req: Any) -> Any:
        # Keep `bearer` current too: openeo's job manager reads it to authenticate side requests.
        self.bearer = get_fresh_id_token(self.service_uri)
        return super().__call__(req)


class _UnknownOtherDimensionFilter(logging.Filter):
    """Drop openeo's warning about Arraylake's non-spatial, non-temporal dimensions (e.g. ``lead_time``).

    openeo logs ``Unknown dimension type 'other'`` on every ``load_collection``; such dimensions are
    still handled correctly.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage() != "Unknown dimension type 'other'"


def silence_unknown_dimension_warning() -> None:
    """Install the filter on openeo's metadata logger, once."""
    logger = logging.getLogger("openeo.metadata")
    if not any(isinstance(f, _UnknownOtherDimensionFilter) for f in logger.filters):
        logger.addFilter(_UnknownOtherDimensionFilter())
