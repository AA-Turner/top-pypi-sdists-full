"""Injection seam for GenAI observability on the harness worker.

``HarnessTurnObservability`` is the host extension point: a host installs an
implementation at startup with ``register_harness_turn_observability`` and the
turn-execution path reads it with ``get_harness_turn_observability``. Its
strictness -- plain header maps only, no host-specific identity type or tracing
backend -- is documented on the protocol itself. The default is a no-op, so a
worker that installs nothing traces nothing.

``TurnScopeBinder`` is SDK-internal glue around an installed contract, not a host
extension point; it is not held to the protocol's host-agnostic contract.

The installed implementation is a process global read from workflow code; this is
sound because the module is a sandbox passthrough package, so workflow code sees
the same object the host installed.
"""

import contextlib
from collections.abc import Mapping
from contextlib import AbstractAsyncContextManager
from typing import Protocol

from mistralai.vibe.harness.runtime.genai import GenAIAgentIdentity, GenAIOperationObserver, GenAIRootTraceParent
from mistralai.vibe_agents.session_workflow.commands import CommandObservability

__all__ = [
    "HarnessTurnObservability",
    "ObserverOnlyTurnObservability",
    "TurnScopeBinder",
    "genai_trace_parent",
    "get_harness_turn_observability",
    "register_harness_turn_observability",
]


class HarnessTurnObservability(Protocol):
    """Host-supplied GenAI observability for one harness worker.

    Identity is passed as an already-built header map, so no host-specific identity
    type crosses into this package. The caller gates eligibility, so ``bind_turn``
    is only called when a scope should be bound.
    """

    def bind_turn(self, *, headers: Mapping[str, str]) -> AbstractAsyncContextManager[None]:
        """Bind the identity scope for one host call; ``headers`` are always present."""
        ...

    def session_genai_observer(self) -> GenAIOperationObserver | None:
        """Return the workflow-side observer for agent/tool spans, or ``None``."""
        ...


class _NoopHarnessTurnObservability:
    """Default implementation: binds nothing and installs no observer."""

    def bind_turn(self, *, headers: Mapping[str, str]) -> AbstractAsyncContextManager[None]:
        del headers
        return contextlib.nullcontext()

    def session_genai_observer(self) -> GenAIOperationObserver | None:
        return None


class ObserverOnlyTurnObservability:
    """Fixed observer with no identity binding.

    For hosts that attribute identity ingest-side (e.g. from a service-account
    token) rather than stamping it from per-turn headers, so ``bind_turn`` is a
    no-op while the observer still feeds the provider.
    """

    def __init__(self, observer: GenAIOperationObserver) -> None:
        self._observer = observer

    def bind_turn(self, *, headers: Mapping[str, str]) -> AbstractAsyncContextManager[None]:
        del headers
        return contextlib.nullcontext()

    def session_genai_observer(self) -> GenAIOperationObserver:
        return self._observer


_NOOP: HarnessTurnObservability = _NoopHarnessTurnObservability()
_impl: HarnessTurnObservability = _NOOP


def register_harness_turn_observability(impl: HarnessTurnObservability) -> None:
    """Install the process-global harness observability implementation."""

    global _impl
    _impl = impl


def get_harness_turn_observability() -> HarnessTurnObservability:
    """Return the installed implementation, or the no-op default."""

    return _impl


class TurnScopeBinder:
    """Binds the per-turn identity scope for one session binding.

    Wraps an installed ``HarnessTurnObservability`` with the single eligibility
    gate (bind only for an eligible turn that has identity headers). Eligibility is
    passed in as a bool, keeping this free of any wire type.
    """

    def __init__(self, impl: HarnessTurnObservability, headers: Mapping[str, str] | None) -> None:
        self._impl = impl
        self._headers = headers

    def scope(self, *, eligible: bool) -> AbstractAsyncContextManager[None]:
        """Bind only for an eligible turn that has identity headers; otherwise a no-op."""
        if not (eligible and self._headers):
            return contextlib.nullcontext()
        return self._impl.bind_turn(headers=self._headers)


def genai_trace_parent(
    observability: CommandObservability | None,
    *,
    session_id: str,
    turn_id: str,
    agent: GenAIAgentIdentity | None,
) -> GenAIRootTraceParent | None:
    """Map a command's serialized trace context to its Turn's Harness GenAI parent."""

    if observability is None:
        return None
    return GenAIRootTraceParent.for_turn(
        enabled=observability.dora_tracing_enabled,
        traceparent=observability.traceparent,
        tracestate=observability.tracestate,
        conversation_id=observability.conversation_id,
        session_id=session_id,
        turn_id=turn_id,
        agent=agent,
    )
