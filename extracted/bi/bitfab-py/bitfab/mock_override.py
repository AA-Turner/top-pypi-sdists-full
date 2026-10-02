"""Selective mock overrides for replay.

A mock override injects a custom value into a specific span (node) during
replay: the matched span short-circuits its real execution and returns the
value the override produces, so downstream real code runs against the
substituted output. This is a third mock mode alongside "run real code" and
"replay recorded output" (see :data:`bitfab.replay.MockStrategy`).

An override can be a ``(match, value)`` pair or one global resolver invoked for
every child span. ``match`` runs on structural metadata only
(:class:`SpanNodeMeta`). ``value`` is EITHER a flat value injected directly
(``value={"label": "refund"}``) OR a callable invoked with a
:class:`MockOverrideCtx` (``node``, ``inputs``, ``kwargs``,
``get_original_output``) whose return value is injected. A caller who genuinely
wraps it: ``value=lambda ctx: the_fn``. A global resolver routes on
``ctx.node.trace_function_key`` and returns :data:`NO_MOCK_OVERRIDE` to decline
the current span.

:attr:`MockOverrideCtx.get_original_output` is SYNCHRONOUS (the TypeScript SDK's
is async). Under a ``marked``/override replay the recorded output is fetched
lazily by ``externalSpanId`` on first access, so a call may block on a short HTTP
request; ``mock="all"`` carries every output inline and never fetches.

Event-loop note: replay offloads that blocking fetch OFF the event loop for
async spans, so concurrent items (``asyncio.gather``) are not stalled. A
SYNCHRONOUS span tagged ``mock_on_replay`` (or matched by an override), when
invoked from an async replay root, cannot offload: it does the fetch on the loop
thread and briefly serializes concurrent items. Make such a span ``async``, or
use ``mock="all"`` (eager, no per-span fetch), to avoid it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal, Union


class _NoMockOverride:
    def __repr__(self) -> str:
        return "NO_MOCK_OVERRIDE"


NO_MOCK_OVERRIDE = _NoMockOverride()
"""Return from an override resolver to continue to the next override or base strategy."""


@dataclass(frozen=True)
class SpanNodeMeta:
    """Structural identity of a span during replay, passed to a match predicate.

    Carries no output payload: matching runs on structural metadata only.

    Attributes:
        trace_function_key: The ``@span`` key of the executing span (its
            code-side identity).
        span_name: Resolved span name (``options.name`` or the function name,
            falling back to ``trace_function_key``).
        type: Span type, e.g. "llm", "agent", "tool", "custom".
        original_span_id: The id of this span in the original (replayed) trace,
            when it exists in that trace's tree. ``None`` when the live span has
            no recorded counterpart (e.g. a span the changed code newly
            introduced).
        variant: The value set with ``node(variant=...)`` that tells apart
            calls sharing this span name, or ``None`` when the call has none.
    """

    trace_function_key: str
    span_name: str
    type: str
    original_span_id: str | None = None
    variant: str | None = None


@dataclass
class MockOverrideCtx:
    """Context passed to a callable override ``value`` for a matched span.

    Attributes:
        node: The matched span's structural metadata.
        inputs: The live positional args passed to the wrapped function this
            run, as a list.
        kwargs: The live keyword args passed to the wrapped function this run,
            as a dict (empty when the call used none).
        get_original_output: A zero-argument callable returning this span's ORIGINAL
            recorded output (deserialized). Synchronous; the first call may
            fetch the output lazily and is memoized for the replay item. Raises
            if the span has no recorded counterpart in the replayed trace.
    """

    node: SpanNodeMeta
    inputs: list[Any]
    kwargs: dict[str, Any]
    get_original_output: Callable[[], Any]


# Selects which spans an override applies to. Runs on structural metadata.
NodeMatcher = Callable[[SpanNodeMeta], bool]

# The injected value for a matched span. Either a flat value (used directly) or
# a callable invoked with a MockOverrideCtx whose return value is injected.
# Full replacement: the resolved value IS the span's output (no merge with the
# recorded output).
MockValue = Union[Callable[[MockOverrideCtx], Any], Any]

# Invoked for every child span. Route on ``ctx.node.trace_function_key`` and
# return ``NO_MOCK_OVERRIDE`` when this resolver declines the span.
MockOverrideResolver = Callable[[MockOverrideCtx], Any]


@dataclass(frozen=True)
class MockOverride:
    """One (match, value) pair.

    Attributes:
        match: Predicate over a :class:`SpanNodeMeta`; the first override whose
            ``match`` returns True wins for a given span.
        value: The injected value for a matched span, a flat value or a callable
            (see :data:`MockValue`).
    """

    match: NodeMatcher
    value: MockValue


MockOverrideInput = Union[MockOverride, MockOverrideResolver]


def normalize_mock_overrides(
    mock_override: Union[
        MockOverrideInput,
        list[MockOverrideInput],
    ]
    | None,
) -> list[MockOverride]:
    """Normalize an override pair, global resolver, list, or ``None``.

    Order is preserved so the first matching entry that does not return
    ``NO_MOCK_OVERRIDE`` wins downstream.
    """
    if mock_override is None:
        return []
    if isinstance(mock_override, MockOverride):
        return [mock_override]
    if callable(mock_override):
        return [MockOverride(match=lambda _node: True, value=mock_override)]
    normalized: list[MockOverride] = []
    for override in mock_override:
        if isinstance(override, MockOverride):
            normalized.append(override)
        elif callable(override):
            normalized.append(MockOverride(match=lambda _node: True, value=override))
        else:
            raise TypeError(
                "mock_override entries must be MockOverride objects or callable "
                "global resolvers"
            )
    return normalized


# What a replay mock replaced on a span, and where the replacement came from.
# Reported alongside ``mocked`` so a trace can say how a span was produced
# rather than only that it was not re-run.
#
# ``MockTarget`` is "output" for every mock today: both the recorded-output path
# and an override short-circuit the call. "input" is reserved for substituting a
# span's arguments and letting the real code run.
MockTarget = Literal["output", "input"]

# "recorded" is the original trace's own value; "override" is one the caller
# supplied via ``mock_override`` / ``register_mock_override``. Deliberately not
# "dynamic": an override value may be a flat constant.
MockSource = Literal["recorded", "override"]
