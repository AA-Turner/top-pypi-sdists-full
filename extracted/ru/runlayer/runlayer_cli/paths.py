"""Path utilities for Runlayer CLI."""

import os
from pathlib import Path


def get_runlayer_dir() -> Path:
    """
    Get the base Runlayer configuration directory.

    Returns:
        Path to ~/.runlayer directory
    """
    return Path.home() / ".runlayer"


def strip_reported_path_prefix(value: str | None) -> str | None:
    """Strip the ``RUNLAYER_STRIP_PATH_PREFIX`` mount prefix from a reported path.

    Containerized scans bind-mount the host filesystem under a prefix (e.g.
    ``/host``) and point ``HOME`` at the mounted copy, so every path the scan
    derives — config paths, project paths, skill/plugin install paths — carries
    the container-only prefix. Submitting those verbatim would make findings
    show ``/host/home/alice/...`` instead of the real host path and diverge from
    a native scan of the same machine. The container entrypoint sets
    ``RUNLAYER_STRIP_PATH_PREFIX`` to the mount prefix; unset (every non-container
    deployment) this is a no-op. Applied only to scan-DERIVED path fields, never
    to values parsed out of config file content.
    """
    prefix = os.environ.get("RUNLAYER_STRIP_PATH_PREFIX")
    if not prefix or not value:
        return value
    prefix = prefix.rstrip("/")
    if not prefix:
        return value
    if value == prefix:
        return "/"
    if value.startswith(prefix + "/"):
        return value[len(prefix) :]
    return value
