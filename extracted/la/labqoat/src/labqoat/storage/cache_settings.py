"""Resolve explicit runtime caches and persistent local-development defaults."""

import os
from pathlib import Path

from labqoat.storage.shared_asset_cache import SharedAssetCache


class CacheSettings:
    """Select storage independently from any worker's temporary view directory."""

    @staticmethod
    def worker(fallback: Path) -> SharedAssetCache:
        """Use the runtime-mounted node cache or an explicitly owned private fallback.

        `LABQOAT_CACHE_VERIFY=always` marks a cache shared with other runs, whose contents are hashed on every use.
        """
        root = Path(os.environ.get("LABQOAT_CACHE_DIR", str(fallback))).expanduser()
        maximum = int(os.environ.get("LABQOAT_CACHE_BYTES", str(10 * 1024 * 1024 * 1024)))
        shared = os.environ.get("LABQOAT_CACHE_VERIFY") == "always"
        return SharedAssetCache(
            root.resolve(), maximum_bytes=maximum, temporary_root=fallback.resolve(), verify_always=shared
        )

    @staticmethod
    def local() -> SharedAssetCache:
        """Share a per-user content cache across projects and local workloads."""
        base = Path(os.environ.get("XDG_CACHE_HOME", str(Path.home() / ".cache")))
        return CacheSettings.worker(base / "labqoat" / "assets")
