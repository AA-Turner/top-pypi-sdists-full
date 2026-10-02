"""Shared engine: builds the generated API handles + the storage helper.

The API classes and models come from the clean, auto-generated ``istari_digital_client._generated``
packages (no hand edits). They share the single overloaded common files at the
``istari`` top level (``ApiClient``, ``Configuration``). Storage upload/download is
hand-written orchestration over ``istari_digital_core`` (the ``StorageHelper``).
Built once per client and shared with every manager (SDK_REDESIGN.md §5).
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Hashable, Tuple

# A cached listing: the per-page item lists (page boundaries preserved) plus the
# server-reported total, enough to rebuild the exact chained ``Page`` sequence.
_CachedListing = Tuple[list[list[Any]], "int | None"]

from istari_digital_client.sdk._api_client import ApiClient
from istari_digital_client.sdk._configuration import Configuration
from istari_digital_client.sdk._generated.storage_api.api.storage_api import StorageApi
from istari_digital_client.sdk._generated.v2.api.v2_api import V2Api
from istari_digital_client.sdk._generated.v3.api.v3_api import V3Api
from istari_digital_client.sdk._storage.helper import StorageHelper


class _ListingCache:
    """Process-local, bounded cache of assembled branch resource listings.

    Opt-in (``Istari(config, list_cache=True)``). Keyed by
    ``(branch_id, snapshot_id, filters)`` so it auto-invalidates when a branch
    advances (a commit gives the branch a new ``snapshot_id`` → new key). Any
    mutating API call in the process clears the whole cache (see
    ``_Manager._call``); writes are rare, so a blunt clear is cheaper than
    tracking which listings a write touched. Stores the assembled list of rich
    items, not raw payloads.
    """

    # ponytail: last-8-branches LRU by entry count; raise _MAX if branch fan-out grows.
    _MAX = 8

    def __init__(self) -> None:
        self._data: "OrderedDict[Hashable, _CachedListing]" = OrderedDict()

    def get(self, key: Hashable) -> _CachedListing | None:
        """Return the cached listing for ``key`` (marking it MRU), or None."""
        value = self._data.get(key)
        if value is not None:
            self._data.move_to_end(key)
        return value

    def put(self, key: Hashable, value: _CachedListing) -> None:
        """Store ``value`` under ``key`` as most-recently-used, evicting the LRU entry."""
        self._data[key] = value
        self._data.move_to_end(key)
        while len(self._data) > self._MAX:
            self._data.popitem(last=False)

    def clear(self) -> None:
        """Drop every cached listing (called on any mutating API call)."""
        self._data.clear()


class _Engine:
    """Holds the generated API handles + the storage helper, shared by managers."""

    def __init__(self, config: Configuration, *, list_cache: bool = False) -> None:
        """Build the shared HTTP client and the generated v2/v3 + storage handles.

        ``list_cache`` opts this client into the process-local branch-listing
        cache (default off — a true no-op for every other consumer).
        """
        self.config = config
        self._api_client = ApiClient(
            config, spec_ids=(V2Api._SPEC_ID, V3Api._SPEC_ID, StorageApi._SPEC_ID)
        )
        # v3 backs the resources tree; v2 backs the cross-cutting access / control-tag
        # / infosec capabilities (no v3 mutation endpoints exist for those).
        self.v3_api = V3Api(config=config, api_client=self._api_client)
        self.v2_api = V2Api(config=config, api_client=self._api_client)
        # storage_api is needed directly by IstariAdmin.tenants for tenant management
        self.storage_api = StorageApi(config=config, api_client=self._api_client)
        self.storage = StorageHelper(self.storage_api)
        self.listing_cache: _ListingCache | None = (
            _ListingCache() if list_cache else None
        )

    def close(self) -> None:
        """Release the shared HTTP connection pool. Idempotent."""
        self._api_client.close()
