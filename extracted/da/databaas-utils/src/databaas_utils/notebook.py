"""Former name of :mod:`databaas_utils.user`, kept so existing notebooks keep working.

New code imports from ``databaas_utils.user``.
"""

from __future__ import annotations

from databaas_utils.user import (
    get_catalog,
    get_index,
    get_settings,
    get_store,
    get_zarr_group,
)

__all__ = [
    "get_catalog",
    "get_index",
    "get_settings",
    "get_store",
    "get_zarr_group",
]
