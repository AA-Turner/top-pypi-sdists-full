"""Shared engine: builds the generated API handles + the storage helper.

The API classes and models come from the clean, auto-generated ``istari_digital_client._generated``
packages (no hand edits). They share the single overloaded common files at the
``istari`` top level (``ApiClient``, ``Configuration``). Storage upload/download is
hand-written orchestration over ``istari_digital_core`` (the ``StorageHelper``).
Built once per client and shared with every manager (SDK_REDESIGN.md §5).
"""

from __future__ import annotations

from collections import OrderedDict
from functools import cached_property
from typing import Any, Hashable, Tuple

# A cached listing: the per-page item lists (page boundaries preserved) plus the
# server-reported total, enough to rebuild the exact chained ``Page`` sequence.
_CachedListing = Tuple[list[list[Any]], "int | None"]

import istari_digital_client.identity.v2.models as identity_v2_models
from istari_digital_client.identity.v2.api.identity_v2_api import IdentityV2Api
from istari_digital_client.sdk._api_client import ApiClient
from istari_digital_client.sdk._configuration import Configuration, ConfigurationError
from istari_digital_client.sdk._generated.storage_api.api.storage_api import StorageApi
from istari_digital_client.sdk._generated.v2.api.v2_api import V2Api
from istari_digital_client.sdk._generated.v3.api.v3_api import V3Api
from istari_digital_client.sdk._identity.auth.identity_service import (
    IdentityApiVersion,
    parse_identity_api_version,
)
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

    @cached_property
    def identity_api_client(self) -> ApiClient:
        """HTTP client bound to the identity-service, carrying identity hashes and models only.

        Requires identity-service's v2 API (``identity_api_version`` ``"v2"``, or
        ``"auto"`` against a server that serves ``/api/v2``) and identity-service auth;
        either missing raises :class:`ConfigurationError` before any key request.

        Identity models must be the only ones searched: several names, ``Tenant``
        among them, also exist in the registry packages with different fields.
        """
        resolved = self.config.resolved_identity_api_version()
        if resolved is not IdentityApiVersion.V2:
            setting = parse_identity_api_version(self.config.identity_api_version)
            raise ConfigurationError(
                "admin.identity calls the identity-service v2 API and is unavailable while "
                f"identity_api_version is {setting.value!r}"
                + (
                    " and the identity-service does not serve /api/v2"
                    if setting is IdentityApiVersion.AUTO
                    else ""
                )
                + " (ISTARI_IDENTITY_API_VERSION)"
            )
        base_url = self.config._identity_service_base_url()
        if self.config._identity_service_client is None or base_url is None:
            raise ConfigurationError(
                "admin.identity needs identity-service auth: set "
                "ISTARI_DIGITAL_IDENTITY_SERVICE_ENABLED=true with a credentials secret, and "
                "ISTARI_DIGITAL_API_URL (gateway) or ISTARI_IDENTITY_URL (direct)"
            )
        return ApiClient(
            self.config,
            spec_ids=(IdentityV2Api._SPEC_ID,),
            base_url=base_url,
            model_packages=(identity_v2_models,),
        )

    @cached_property
    def identity_v2_api(self) -> IdentityV2Api:
        """Generated identity-service v2 API handle."""
        return IdentityV2Api(config=self.config, api_client=self.identity_api_client)

    def close(self) -> None:
        """Release the shared HTTP connection pools. Idempotent."""
        self._api_client.close()
        if "identity_api_client" in self.__dict__:
            self.identity_api_client.close()
