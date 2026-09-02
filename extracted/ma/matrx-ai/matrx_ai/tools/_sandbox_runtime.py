"""Sandbox runtime detection — shared by filesystem / shell / code tools.

When matrx-ai runs INSIDE a matrx-sandbox container (i.e., the
``matrx-sandbox:aidream`` image with ``mtx aidream serve`` started), the
container itself IS the user/project boundary. Adding a synthetic
``<user_id>/<project_id>`` prefix on top of every path is wrong here:
the agent's home is ``/home/agent``, the working copy of aidream is
``/home/agent/aidream``, and that's where the user actually wants tools
to operate.

This module exposes a single decision point — ``sandbox_mode_active()`` —
so every tool implementation that resolves a path or working dir gets
consistent behaviour. Sandbox mode is the ``sandbox`` role from the unified
host-identity resolver (``matrx_utils.runtime_env``), which auto-detects the
sandbox via the ``/opt/aidream-template`` marker that only the
``matrx-sandbox:aidream`` image bakes in.

Outside a sandbox (the central aidream backend), tools keep their existing
multi-tenant scoping under ``WORKSPACE_BASE/<user_id>/<project_id>/``.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def sandbox_mode_active() -> bool:
    from matrx_utils import get_runtime_env

    return get_runtime_env().is_sandbox


def workspace_base() -> Path:
    """Root of the workspace tree — sandbox-aware.

    In sandbox mode the agent's home (``/home/agent``) is the natural root.
    Outside sandbox mode the legacy ``/tmp/workspaces`` default is preserved
    so multi-tenant aidream behaves exactly as before.
    """
    if sandbox_mode_active():
        return Path(os.environ.get("TOOL_WORKSPACE_BASE", "/home/agent"))
    return Path(os.environ.get("TOOL_WORKSPACE_BASE", "/tmp/workspaces"))


def scoped_base_for(user_id: str, project_id: str | None) -> Path:
    """Return the per-tool root for a given user/project.

    Sandbox: the workspace base directly (no synthetic nesting — the
    container is the boundary). Outside sandbox: legacy
    ``<base>/<user_id>/<project_id>`` layout for tenant isolation.
    """
    base = workspace_base()
    if sandbox_mode_active():
        return base
    base = base / user_id
    if project_id:
        base = base / project_id
    return base
