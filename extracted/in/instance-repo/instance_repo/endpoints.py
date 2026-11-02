"""Package-private compatibility seams for data-plane endpoint routing.

Network selection is intentionally not part of the public SDK API. Route
planning lives in :mod:`instance_repo._routing` and is consumed internally.
"""
from __future__ import annotations

from ._routing import _plan_acr_route


def _private_acr_host(host: str) -> str:
    """Return the normalized private ACR host used by the pre-routing store."""
    return _plan_acr_route(host).private_endpoint
