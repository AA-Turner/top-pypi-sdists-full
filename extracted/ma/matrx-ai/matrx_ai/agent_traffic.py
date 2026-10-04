"""THE AGENT-TRAFFIC MARKER — the one way our own agents, scripts and test browsers say
"this request is ours, not a visitor's".

Why (Arman, 2026-10-03): 46 anonymous guest accounts were minted that day and 40 were only
GUESSED to be bots from their user agent. Every tool we own now carries this marker and every
reader trusts it before any heuristic:

* guest mint (``db/_guest_registry_impl.py``) — ``traffic_kind = "agent"`` and an
  ``app_metadata.test_fixture`` expiry on the anonymous user, so the persona sweeper
  (``aidream/testing/fixture_sweep.py``) deletes it after ``auth.guest_identity /
  agent_guest_ttl_days``.
* every script and test client — sends ``agent_traffic_headers("<tool name>")``.

It LABELS, never gates: nothing is refused for carrying it or for lacking it (the user-agent
heuristics stay as the fallback).

Twin: matrx-frontend ``lib/agent-traffic/marker.ts`` — same constant name, same values.
``pnpm check:agent-traffic-marker`` (matrx-frontend) fails when the two drift, and when a tool in
either repo makes requests without the marker.
"""

from __future__ import annotations

import re
from collections.abc import Mapping

MATRX_AGENT_TRAFFIC: Mapping[str, str] = {
    # Request header for scripts, curl, Python clients and Playwright extra_http_headers.
    "header": "X-Matrx-Agent-Traffic",
    # First-party cookie for browsers that cannot set headers (the Claude browser pane).
    "cookie": "matrx_agent_traffic",
    # app_metadata.test_fixture.suite stamped on a guest our agent minted.
    "fixtureSuite": "agent-traffic",
}

_UNSAFE = re.compile(r"[^A-Za-z0-9._:/-]+")


def agent_traffic_value(tool: str) -> str:
    """The value a tool sends: its own name, so a trace says WHICH tool it was."""
    cleaned = _UNSAFE.sub("-", tool.strip())[:80]
    return cleaned or "agent"


def agent_traffic_headers(tool: str) -> dict[str, str]:
    """``{"X-Matrx-Agent-Traffic": <tool>}`` — merge into any request's headers."""
    return {MATRX_AGENT_TRAFFIC["header"]: agent_traffic_value(tool)}


def agent_traffic_of(headers: Mapping[str, str] | None, cookies: Mapping[str, str] | None = None) -> str | None:
    """The marker on a request (header first, then cookie); ``None`` = not marked.

    ``headers`` lookups are case-insensitive for plain dicts too.
    """
    if headers:
        wanted = MATRX_AGENT_TRAFFIC["header"].lower()
        for name, value in headers.items():
            if name.lower() == wanted and value and value.strip():
                return agent_traffic_value(value)
    if cookies:
        value = cookies.get(MATRX_AGENT_TRAFFIC["cookie"])
        if value and value.strip():
            return agent_traffic_value(value)
    return None
