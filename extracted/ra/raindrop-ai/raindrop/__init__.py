"""Raindrop AI Python SDK.

Two equivalent ways to use the SDK:

Instance-based (multiple projects per process, matches the JS/Go/Rust/Java
SDKs)::

    from raindrop import Raindrop

    rd = Raindrop(api_key="...", project_id="support-agent")
    rd.track_ai(user_id="u1", event="chat", input="q", output="a")

Module-level (the long-standing API; a process-wide default client)::

    import raindrop.analytics as raindrop

    raindrop.init(api_key="...")
    raindrop.track_ai(user_id="u1", event="chat", input="q", output="a")

Exports resolve lazily (PEP 562) so ``import raindrop`` alone stays free of
import-time side effects — the analytics/tracing stack only loads when first
accessed.
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover - typing only
    from raindrop.client import Raindrop
    from raindrop.handoff import TraceContext
    from raindrop.interaction import Interaction
    from raindrop.models import Attachment
    from raindrop.subagent import SubagentDispatch, SubagentRun

__all__ = [
    "Raindrop",
    "Interaction",
    "Attachment",
    # Detached async sub-agents (see raindrop.handoff for the contract).
    "TraceContext",
    "SubagentDispatch",
    "SubagentRun",
]


def __getattr__(name: str) -> Any:
    if name == "Raindrop":
        from raindrop.client import Raindrop

        return Raindrop
    if name == "Interaction":
        from raindrop.interaction import Interaction

        return Interaction
    if name == "Attachment":
        from raindrop.models import Attachment

        return Attachment
    if name == "TraceContext":
        from raindrop.handoff import TraceContext

        return TraceContext
    if name in ("SubagentDispatch", "SubagentRun"):
        from raindrop import subagent

        return getattr(subagent, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
