"""Jira instance metadata discovery via the Atlassian SDK serverInfo endpoint.

Provides ``get_instance_metadata()`` which queries ``rest/api/latest/serverInfo``,
normalizes the response to a 6-key dict, and caches the result at
``.agdt/cache/jira-discovery.json``. The function never raises — all failures
return ``None``.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agentic_devtools.state import _get_git_repo_root
from agentic_devtools.tools.jira import JiraConfig

__all__ = ["get_instance_metadata", "load_cached_instance_metadata"]

_REQUIRED_KEYS = frozenset({"version", "versionNumbers", "deploymentType", "buildNumber", "baseUrl", "discoveredUtc"})

_CACHE_FILENAME = "jira-discovery.json"


def _get_cache_path() -> Path | None:
    """Resolve the cache file path: ``<repo_root>/.agdt/cache/jira-discovery.json``.

    Returns ``None`` when the git repo root cannot be determined.
    """
    git_root = _get_git_repo_root()
    if git_root is None:
        return None
    return git_root / ".agdt" / "cache" / _CACHE_FILENAME


def _schema_has_required_keys(data: dict[str, Any]) -> bool:
    """Check that *data* contains all 6 required metadata keys.

    A key present with a ``None`` value is valid; a missing key is not.
    """
    return _REQUIRED_KEYS.issubset(data.keys())


def load_cached_instance_metadata() -> dict[str, Any] | None:
    """Load cached Jira instance metadata from the cache file.

    Returns the cached dict when the file exists, is valid JSON, and contains
    all 6 required keys. Returns ``None`` otherwise (missing file, malformed
    JSON, schema violation).
    """
    cache_path = _get_cache_path()
    if cache_path is None:
        return None
    try:
        raw = cache_path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    if not _schema_has_required_keys(data):
        return None
    return data


def _fetch_server_info(config: JiraConfig | None = None) -> dict[str, Any] | None:
    """Call the Jira serverInfo endpoint via the SDK and normalize the response.

    Args:
        config: Optional :class:`~agentic_devtools.tools.jira.JiraConfig` resolved
            by the caller (e.g. from the connectivity preflight). When provided,
            the SDK client is built with the same credentials and TLS settings used
            for the probe so the two operations share a single auth path. When
            *None*, credentials are resolved from the environment via the existing
            helper functions.

    Returns the normalized 6-key dict on success, or ``None`` on any failure
    (ImportError, connection error, HTTP error, malformed response).
    """
    try:
        from agentic_devtools.cli.jira.sdk import build_jira_client  # noqa: PLC0415
    except ImportError:
        return None

    try:
        client = build_jira_client(config=config)
        response = client.get("rest/api/latest/serverInfo")
    except Exception:  # noqa: BLE001
        return None

    if not isinstance(response, dict):
        return None

    # Normalize the response to the 6-key schema
    version = response.get("version")
    version_numbers = response.get("versionNumbers")
    deployment_type = response.get("deploymentType")
    build_number = response.get("buildNumber")  # may be absent → None
    base_url = response.get("baseUrl")

    # version, versionNumbers, deploymentType, baseUrl are required to be non-None
    if version is None or version_numbers is None or deployment_type is None or base_url is None:
        return None

    return {
        "version": version,
        "versionNumbers": version_numbers,
        "deploymentType": deployment_type,
        "buildNumber": build_number,  # None is valid
        "baseUrl": base_url,
        "discoveredUtc": datetime.now(tz=timezone.utc).isoformat(),
    }


def _write_cache(metadata: dict[str, Any]) -> None:
    """Atomically write *metadata* to the cache file.

    Creates the ``.agdt/cache/`` directory if missing. On failure, emits a
    warning to stderr but does not raise.
    """
    cache_path = _get_cache_path()
    if cache_path is None:
        return

    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write: write to temp file in the same directory, then replace
        fd, temp_file = tempfile.mkstemp(dir=str(cache_path.parent), suffix=".tmp", prefix=".jira-discovery-")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
                f.write("\n")
            os.replace(temp_file, str(cache_path))
        except Exception:
            # Clean up temp file on failure
            try:
                os.unlink(temp_file)
            except OSError:
                pass
            raise
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ Cache write failed ({exc})", file=sys.stderr)


def get_instance_metadata(force_refresh: bool = False, config: JiraConfig | None = None) -> dict[str, Any] | None:
    """Discover Jira instance metadata via the serverInfo endpoint.

    When *force_refresh* is ``False`` (the default), returns cached metadata if
    available. When ``True``, bypasses the cache and makes a fresh network call.

    Args:
        force_refresh: When ``True``, bypass the cache and query the server.
        config: Optional :class:`~agentic_devtools.tools.jira.JiraConfig` resolved
            by the caller. When provided, the same credentials and TLS settings used
            for the connectivity preflight are forwarded to the SDK client so the
            probe and discovery share a single auth path. Ignored on cache hits.

    Returns a 6-key dict on success or ``None`` on any failure. **Never raises.**
    """
    try:
        if not force_refresh:
            cached = load_cached_instance_metadata()
            if cached is not None:
                return cached

        metadata = _fetch_server_info(config=config)
        if metadata is None:
            return None

        _write_cache(metadata)
        return metadata
    except Exception:  # noqa: BLE001
        return None
