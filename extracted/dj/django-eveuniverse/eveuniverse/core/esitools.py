"""Tools for interacting with ESI."""

from bravado.exception import HTTPError

from eveuniverse.providers import esi


def is_esi_online() -> bool:
    """Reports whether the Eve servers are online."""
    try:
        status = esi.client.Status.get_status().results(ignore_cache=True)
        if status.get("vip"):
            return False
    except (AttributeError, HTTPError):
        return False
    return True
