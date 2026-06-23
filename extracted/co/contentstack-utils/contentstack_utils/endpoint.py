"""
Endpoint resolution for Contentstack services across all regions.

Reads a bundled regions.json (src/assets/regions.json) and resolves
the correct base URL for any region + service combination. No runtime
HTTP calls — the file is shipped with the package and updated via
``python scripts/refresh_regions.py``.
"""

import json
import os
import re
import urllib.request
from typing import Dict, Optional, Union

_REGIONS_URL = "https://artifacts.contentstack.com/regions.json"
_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
_REGIONS_FILE = os.path.join(_ASSETS_DIR, "regions.json")


class Endpoint:
    """
    Resolve Contentstack service URLs for any region.

    All public methods are static — no instantiation required.

    Example::

        from contentstack_utils import Endpoint

        # Full URL
        url = Endpoint.get_contentstack_endpoint("na", "contentDelivery")
        # → "https://cdn.contentstack.io"

        # Host only (strip https://) — useful for SDK setHost() calls
        host = Endpoint.get_contentstack_endpoint("eu", "contentDelivery", omit_https=True)
        # → "eu-cdn.contentstack.com"

        # All endpoints for a region
        all_endpoints = Endpoint.get_contentstack_endpoint("azure-na")
        # → {"contentDelivery": "...", "contentManagement": "...", ...}
    """

    # Module-level cache — loaded once per Python process, shared across all calls.
    _regions_data: Optional[Dict] = None

    @staticmethod
    def get_contentstack_endpoint(
        region: str = "us",
        service: str = "",
        omit_https: bool = False,
    ) -> Union[str, Dict[str, str]]:
        """
        Resolve a Contentstack service endpoint URL for the given region.

        :param region:
            Region ID or any accepted alias (case-insensitive, ``-`` and ``_``
            are interchangeable). Examples: ``'na'``, ``'us'``, ``'eu'``,
            ``'AWS-NA'``, ``'azure_eu'``, ``'gcp-na'``.
            Defaults to ``'us'`` (AWS North America).
        :param service:
            Optional service key. When provided, a single URL string is
            returned. When omitted, a dict of **all** service URLs is returned.
            Valid keys include: ``'contentDelivery'``, ``'contentManagement'``,
            ``'auth'``, ``'graphqlDelivery'``, ``'preview'``, ``'images'``,
            ``'assets'``, ``'automate'``, ``'launch'``, ``'developerHub'``,
            ``'brandKit'``, ``'genAI'``, ``'personalizeManagement'``,
            ``'personalizeEdge'``, ``'composableStudio'``, ``'assetManagement'``.
        :param omit_https:
            When ``True``, strips the ``https://`` (or ``http://``) scheme from
            every returned URL. Useful when passing the host to an SDK that
            constructs its own URLs (e.g. ``stack.set_host(host)``).
        :returns:
            - A ``str`` URL when *service* is specified.
            - A ``dict[str, str]`` mapping service keys → URLs when *service*
              is omitted.
        :raises ValueError:
            If *region* is an empty string.
        :raises LookupError:
            If *region* does not match any known region ID or alias, or if
            *service* is not present in the resolved region's endpoint map.
        :raises RuntimeError:
            If the bundled ``regions.json`` cannot be read or is malformed.

        Examples::

            Endpoint.get_contentstack_endpoint("na", "contentDelivery")
            # → "https://cdn.contentstack.io"

            Endpoint.get_contentstack_endpoint("eu", "contentDelivery", omit_https=True)
            # → "eu-cdn.contentstack.com"

            Endpoint.get_contentstack_endpoint("azure-na")
            # → {"contentDelivery": "https://...", ...}
        """
        if not region:
            raise ValueError("Empty region provided. Please put valid region.")

        data = Endpoint._load_regions()
        normalized = region.strip().lower()

        if not normalized:
            raise ValueError("Empty region provided. Please put valid region.")
        region_row = Endpoint._find_region_by_id_or_alias(data["regions"], normalized)

        if region_row is None:
            raise LookupError(f"Invalid region: {region}")

        if service:
            endpoints = region_row["endpoints"]
            if service not in endpoints:
                raise LookupError(
                    f'Service "{service}" not found for region "{region_row["id"]}"'
                )
            url = endpoints[service]
            return Endpoint._strip_https(url) if omit_https else url

        endpoints = dict(region_row["endpoints"])
        return Endpoint._strip_https_from_map(endpoints) if omit_https else endpoints


    getContentstackEndpoint = get_contentstack_endpoint

    @staticmethod
    def reset_cache() -> None:
        """
        Clear the in-memory region cache.

        Intended for testing only — forces the next call to re-read
        ``regions.json`` from disk.
        """
        Endpoint._regions_data = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_regions() -> Dict:
        """
        Load and cache regions data.

        Resolution order:
          1. In-memory cache (zero I/O after the first call in a process)
          2. Bundled ``contentstack_utils/assets/regions.json`` on disk
          3. Live download from ``artifacts.contentstack.com`` (fallback when
             the file is absent — e.g. an editable install without assets)
        """
        if Endpoint._regions_data is not None:
            return Endpoint._regions_data

        if not os.path.exists(_REGIONS_FILE):
            Endpoint._download_and_save(_REGIONS_FILE)

        if not os.path.exists(_REGIONS_FILE):
            raise RuntimeError(
                "contentstack_utils: regions.json not found and could not be downloaded. "
                "Run 'python scripts/refresh_regions.py' and ensure network access."
            )

        try:
            with open(_REGIONS_FILE, "r", encoding="utf-8") as fh:
                raw = fh.read()
        except OSError as exc:
            raise RuntimeError(
                f"contentstack_utils: Could not read regions.json: {exc}"
            ) from exc

        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "contentstack_utils: regions.json is corrupt. "
                "Run 'python scripts/refresh_regions.py' to re-download it."
            ) from exc

        if not isinstance(decoded, dict) or "regions" not in decoded:
            raise RuntimeError(
                "contentstack_utils: regions.json is corrupt. "
                "Run 'python scripts/refresh_regions.py' to re-download it."
            )

        Endpoint._regions_data = decoded
        return Endpoint._regions_data

    @staticmethod
    def _download_and_save(dest: str) -> None:
        """
        Fetch regions.json from the Contentstack CDN and write it to *dest*.

        Silent on failure — the caller decides whether a missing file is fatal.
        """
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            with urllib.request.urlopen(_REGIONS_URL, timeout=30) as resp:
                data = resp.read().decode("utf-8")
        except Exception:
            return

        try:
            decoded = json.loads(data)
        except json.JSONDecodeError:
            return

        if isinstance(decoded, dict) and "regions" in decoded:
            with open(dest, "w", encoding="utf-8") as fh:
                fh.write(data)

    @staticmethod
    def _find_region_by_id_or_alias(
        regions: list, normalized_input: str
    ) -> Optional[Dict]:
        """
        Find a region by its ``id`` field first, then by any alias.

        Both passes are case-insensitive (caller must pass a lowercased string).
        Two-pass approach mirrors the PHP implementation: ID match wins over alias
        match, which avoids surprising behaviour when a future alias happens to
        collide with another region's canonical ID.
        """
        # Pass 1 — exact id match
        for row in regions:
            if row["id"] == normalized_input:
                return row

        # Pass 2 — alias match
        for row in regions:
            for alias in row.get("alias", []):
                if alias.lower() == normalized_input:
                    return row

        return None

    @staticmethod
    def _strip_https(url: str) -> str:
        """Strip ``https://`` or ``http://`` from the start of a URL."""
        return re.sub(r"^https?://", "", url)

    @staticmethod
    def _strip_https_from_map(endpoints: Dict[str, str]) -> Dict[str, str]:
        """Return a new dict with the scheme stripped from every URL value."""
        return {key: Endpoint._strip_https(url) for key, url in endpoints.items()}
