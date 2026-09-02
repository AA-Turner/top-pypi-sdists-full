"""Helpers for emitting RESOURCE_CHANGED events from tool implementations.

Tools call ``emit_fs_changed(...)`` (or ``emit_resource_changed(...)`` for the
generic primitive) after successfully mutating a resource the client may
care about. Both helpers fetch the request emitter via the matrx-connect
context API and gracefully no-op when none is available — tests and batch
runs can call mutating tools without owning a streaming response.

Why these helpers exist instead of inlining the call:

  - The lookup chain (``try_get_app_context`` → ``ctx.emitter``) is the same
    everywhere; centralizing keeps it DRY.
  - The "no emitter? no problem" graceful degrade is enforced once, not
    re-implemented per tool.
  - Future kinds (``cld_files``, ``sandbox.cwd``, …) get a one-line helper
    here rather than repeating the AppContext dance at every emit site.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from matrx_connect import try_get_app_context
from matrx_connect.context.events import ResourceAction

logger = logging.getLogger(__name__)


def _current_sandbox_id() -> str | None:
    """Read SANDBOX_ID from the process env. Set by the matrx-sandbox
    orchestrator when matrx-ai runs INSIDE a spawned sandbox (the
    "sandbox-mode" path); None when matrx-ai runs as the central aidream
    backend (multi-tenant) — there is no single sandbox in that case.
    """
    return os.environ.get("SANDBOX_ID") or None


async def emit_resource_changed(
    *,
    kind: str,
    action: ResourceAction,
    resource_id: str,
    metadata: dict[str, Any] | None = None,
    sandbox_id: str | None = None,
    user_id: str | None = None,
) -> None:
    """Emit a generic RESOURCE_CHANGED event into the active request stream.

    No-ops silently when no AppContext is active (e.g., a tool unit test or a
    background batch job). Logs at DEBUG so dev runs can see the no-op when
    emit failures are unexpected.

    ``sandbox_id`` defaults to the SANDBOX_ID env var so callers don't have
    to thread it through every tool. Pass ``sandbox_id=""`` to override and
    suppress the env-fallback.
    """
    app_ctx = try_get_app_context()
    if app_ctx is None or app_ctx.emitter is None:
        logger.debug("emit_resource_changed skipped — no active emitter")
        return

    if sandbox_id is None:
        sandbox_id = _current_sandbox_id()
    elif sandbox_id == "":
        sandbox_id = None

    if user_id is None:
        # AppContext.user_id is required on a real request; tolerate missing
        # for test contexts that synthesize a partial AppContext.
        user_id = getattr(app_ctx, "user_id", None) or None

    await app_ctx.emitter.send_resource_changed(
        kind=kind,
        action=action,
        resource_id=resource_id,
        sandbox_id=sandbox_id,
        user_id=user_id,
        metadata=metadata or {},
    )


async def emit_fs_changed(
    *,
    action: ResourceAction,
    path: str,
    is_dir: bool = False,
    metadata: dict[str, Any] | None = None,
    sandbox_id: str | None = None,
) -> None:
    """Emit RESOURCE_CHANGED for a filesystem path. Convenience wrapper —
    sets ``kind`` to ``fs.directory`` or ``fs.file`` and uses the path as
    the resource_id. Common metadata keys used by clients today: ``size``,
    ``checksum``, ``mtime``, and ``previous_id`` (for moves/renames)."""
    await emit_resource_changed(
        kind="fs.directory" if is_dir else "fs.file",
        action=action,
        resource_id=path,
        metadata=metadata,
        sandbox_id=sandbox_id,
    )
