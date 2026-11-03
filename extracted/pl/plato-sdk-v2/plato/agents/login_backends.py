"""Agent package → login backend mapping.

Each agent package image ships one specific login protocol:

- ``claude-code``, ``gemini-cli``, ``codex`` ship the ``agent-browser`` CLI.
  Pre-agent login replays recorded flows through that CLI so cookies land in
  the per-env session stores the agent later reads from.
- ``computer-use-agent`` (and any other visual CUA image) ships Chrome with
  a CDP endpoint on :9224. Pre-agent login connects Playwright over CDP and
  drives the login flow in the same browser the agent will later see.

This mapping is a *fact about the image* (what binaries/services it ships),
not a user preference — so it lives in the SDK rather than being declared
per-world or per-config.
"""

from __future__ import annotations

from typing import Literal

LoginBackend = Literal["cdp", "agent_browser"]

_PACKAGE_LOGIN_BACKENDS: dict[str, LoginBackend] = {
    "claude-code": "agent_browser",
    "gemini-cli": "agent_browser",
    "codex": "agent_browser",
    "computer-use-agent": "cdp",
}


def resolve_login_backend(package: str | None) -> LoginBackend | None:
    """Return the login protocol for ``package`` (e.g. ``"claude-code:latest"``).

    Returns ``None`` for empty/unknown packages so callers can fall back or
    raise with a clear message.
    """
    if not package:
        return None
    prefix = package.split(":", 1)[0]
    return _PACKAGE_LOGIN_BACKENDS.get(prefix)
