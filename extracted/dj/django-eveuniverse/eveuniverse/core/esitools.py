"""Tools for interacting with ESI."""

from esi.exceptions import HTTPClientError, HTTPServerError

from eveuniverse.providers import esi


def is_esi_online() -> bool:
    """Reports whether the Eve servers are online."""
    try:
        status = esi.client.Status.GetStatus().result(use_etag=False, use_cache=False)
        if status.vip:
            return False

    except (AttributeError, HTTPServerError, HTTPClientError):
        return False

    return True
