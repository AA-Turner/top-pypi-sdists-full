"""Durable, file_id-addressed render/download URLs — the private-file lane.

THE LAW (Arman, 2026-08-21 + 2026-08-26): **nothing returns a signed URL.**
A client addresses a file by ``file_id``. Public files render via the
permanent CDN URL (``cdn.py``). Private files render via the durable,
never-expiring route this module builds::

    {files_public_base}/files/{file_id}/download?inline=1     (render)
    {files_public_base}/files/{file_id}/download              (attachment)

The route is authenticated (Bearer header for API callers; the browser
session cookie minted by ``POST /files/session`` for ``<img>``/``<video>``
bindings — see matrx-connect ``middleware/session_cookie.py``). The URL
itself carries nothing but the id: it cannot expire, cannot leak a grant,
and is safe to persist anywhere.

A presigned S3 URL remains legal in exactly three lanes, none of which go
through this module:
  1. provider handoff — ``resolve_media_async`` minting ``resolved_url``
     for one third-party call, consumed immediately;
  2. the user-created share link (``/share/{token}`` streams bytes; the
     token IS the auth);
  3. row-less ephemeral scratch (staged previews, pdf-compress output) —
     there is no file row, so id-addressing is impossible by construction;
     those fields are named ``ephemeral_url`` and expire by design.

Base-URL resolution order:
  1. ``matrx_files.configure(files_public_base_url=...)`` (host injection)
  2. the ``PUBLIC_URL`` setting/env — every Matrx server already declares
     its own public base under this name (aidream REQUIRED_ENV).
When neither is set the builders return ``None`` and callers degrade to a
null ``url`` — loudly logged once, because a private file with no URL is
a wiring bug at startup, not a runtime condition.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

_warned_unconfigured = False


def _setting(name: str) -> str | None:
    try:
        from matrx_utils import settings

        for candidate in (name, name.lower()):
            value = getattr(settings, candidate, None)
            if value:
                return str(value)
    except Exception:
        pass
    import os

    return os.environ.get(name) or None


def files_public_base_url() -> str | None:
    """The public base URL durable file routes are served from, no trailing slash."""
    try:
        from .._config import get_config, is_configured

        if is_configured():
            configured = getattr(get_config(), "files_public_base_url", None)
            if configured:
                return str(configured).rstrip("/")
    except Exception:
        pass
    env = _setting("PUBLIC_URL")
    if env:
        return env.rstrip("/")
    global _warned_unconfigured
    if not _warned_unconfigured:
        _warned_unconfigured = True
        logger.error(
            "matrx-files: no files_public_base_url configured and PUBLIC_URL is unset — "
            "durable render URLs for private files cannot be built. Pass "
            "matrx_files.configure(files_public_base_url=...) at startup."
        )
    return None


def durable_inline_url(file_id: str) -> str | None:
    """Never-expiring, browser-bindable render URL for a file id."""
    base = files_public_base_url()
    if not base or not file_id:
        return None
    return f"{base}/files/{file_id}/download?inline=1"


def durable_download_url(file_id: str) -> str | None:
    """Never-expiring attachment-disposition URL for a file id."""
    base = files_public_base_url()
    if not base or not file_id:
        return None
    return f"{base}/files/{file_id}/download"


__all__ = ["files_public_base_url", "durable_inline_url", "durable_download_url"]
