"""Tool-dispatch ceilings — host-bound `platform.feature_knob` values (feature ``agents.tool_dispatch``).

Authority: ``common-docs/policies/limits-are-knobs-agents-set-them.md`` — a
behavioural ceiling is a registry row an admin turns, never a constant nobody
can see. The executor's dispatch deadline used to be the literal ``120.0`` on
``ToolDefinition.timeout_seconds``, and on 2026-09-12 23:23 that constant is
what stopped the Masterwork Conductor from re-teaching a desk's Writer: the
``workflow_plan build_agent`` call runs a meta-agent, which needs longer than
two minutes, and nobody could raise the ceiling without a deploy.

This package must not import aidream, so the host injects a ONE-ARGUMENT reader
(``key -> value``) — aidream binds ``knob_raw_sync("agents.tool_dispatch", key)``
in ``package_integration`` — and every read below goes through it, live, so
turning the row takes effect within the host's knob cache TTL and no deploy.

======================== ========= =============================================
key                      start     meaning
======================== ========= =============================================
default_timeout_seconds  120       the dispatch deadline for a tool whose own
                                   row declares no ``guardrail_config.timeout_seconds``.
per_tool_timeout_seconds {…}       per-tool overrides by tool NAME, for the
                                   handful of tools whose honest ceiling is not
                                   the default. Seeded with
                                   ``{"workflow_plan": 300}`` — its
                                   ``build_agent`` action runs the agent-builder
                                   meta-agent end to end.
======================== ========= =============================================

Seeded by ``db/migrations/0671_agents_tool_dispatch_timeout_knobs.sql``
(2026-09-13, review due 2026-12-13). Standalone posture: with no host bound,
each read answers with the mirror the call site declares beside a ``KNOB
MIRROR`` comment naming the row, announced once per process so a host that
forgot to bind is never mistaken for one that did.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

FEATURE = "agents.tool_dispatch"

DEFAULT_TIMEOUT_SECONDS_KEY = "default_timeout_seconds"
PER_TOOL_TIMEOUT_SECONDS_KEY = "per_tool_timeout_seconds"

#: KNOB MIRROR of platform.feature_knob "agents.tool_dispatch" "default_timeout_seconds"
DEFAULT_TIMEOUT_SECONDS_MIRROR = 120.0
#: KNOB MIRROR of platform.feature_knob "agents.tool_dispatch" "per_tool_timeout_seconds"
PER_TOOL_TIMEOUT_SECONDS_MIRROR: dict[str, float] = {"workflow_plan": 300.0}

_reader: Callable[[str], Any] | None = None
_announced = False
_failed: set[str] = set()


def configure_tool_dispatch_knobs(reader: Callable[[str], Any] | None) -> None:
    """Bind the host's reader (``key -> value`` for feature ``agents.tool_dispatch``).
    ``None`` unbinds it, restoring the standalone posture."""
    global _reader, _announced
    _reader = reader
    _announced = False
    _failed.clear()


def tool_dispatch_knob(key: str, mirror: Any) -> Any:
    """The live value of ``agents.tool_dispatch.<key>`` through the host, or the
    declared mirror when no host is bound (announced once)."""
    global _announced
    if _reader is None:
        if not _announced:
            _announced = True
            print(
                "[matrx_ai] no host knob reader bound for 'agents.tool_dispatch'; using the "
                "package's mirrored defaults (bind one with configure_tool_dispatch_knobs())",
                file=sys.stderr,
            )
        return mirror
    try:
        return _reader(key)
    except Exception as exc:  # noqa: BLE001 — announced, never a crashed read
        if key not in _failed:
            _failed.add(key)
            print(
                f"[matrx_ai] host knob reader failed for {FEATURE!r}.{key!r}: {exc!r}; "
                f"using the mirrored default {mirror!r} until the host primes the "
                f"feature (aidream: prime_knob_features(*SYNC_READ_FEATURES))",
                file=sys.stderr,
            )
        return mirror


def _positive_float(raw: Any, mirror: float) -> float:
    try:
        value = float(str(raw).strip().strip('"'))
    except (TypeError, ValueError):
        return mirror
    return value if value > 0 else mirror


def dispatch_timeout_ceiling(tool_name: str) -> float:
    """The dispatch deadline for ``tool_name`` when its own row declares none.

    A per-tool override wins over the default; neither ever raises — a knob read
    that cannot answer falls back to its announced mirror, because a tool call
    must not fail over an unreadable ceiling.
    """
    per_tool = tool_dispatch_knob(
        PER_TOOL_TIMEOUT_SECONDS_KEY, PER_TOOL_TIMEOUT_SECONDS_MIRROR
    )
    if isinstance(per_tool, dict) and tool_name in per_tool:
        return _positive_float(
            per_tool[tool_name],
            PER_TOOL_TIMEOUT_SECONDS_MIRROR.get(tool_name, DEFAULT_TIMEOUT_SECONDS_MIRROR),
        )
    return _positive_float(
        tool_dispatch_knob(DEFAULT_TIMEOUT_SECONDS_KEY, DEFAULT_TIMEOUT_SECONDS_MIRROR),
        DEFAULT_TIMEOUT_SECONDS_MIRROR,
    )


__all__ = [
    "DEFAULT_TIMEOUT_SECONDS_KEY",
    "DEFAULT_TIMEOUT_SECONDS_MIRROR",
    "FEATURE",
    "PER_TOOL_TIMEOUT_SECONDS_KEY",
    "PER_TOOL_TIMEOUT_SECONDS_MIRROR",
    "configure_tool_dispatch_knobs",
    "dispatch_timeout_ceiling",
    "tool_dispatch_knob",
]
