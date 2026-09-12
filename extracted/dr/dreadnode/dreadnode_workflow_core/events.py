"""Typed events that flow between workflow steps.

A :class:`WorkflowEvent` is the unit of data flow *and* the unit of the graph: a
step declares what it consumes as its event parameter and what it may emit as
its return annotation, and the edges are derived from those types. See
``plans/workflows-prd.md`` §8.

Four distinct concepts use the word "event" in this codebase. This module owns
exactly one of them — the durable, per-run, step-to-step object. It is never
published on the runtime event bus; see PRD §9.5.
"""

import typing as t

from pydantic import BaseModel, ConfigDict, Field

# PEP 646 star-syntax (`Generic[*Ts]`) needs 3.11; the typing_extensions forms
# work from 3.10, which the platform still supports. typing_extensions is
# already a pydantic dependency, so this costs nothing.
from typing_extensions import TypeVarTuple, Unpack

T = t.TypeVar("T")
Ts = TypeVarTuple("Ts")

__all__ = [
    "ApprovalDecision",
    "ApprovalOutcome",
    "ApprovalRequest",
    "Collect",
    "FailureClass",
    "NodeFailure",
    "StartEvent",
    "StopEvent",
    "WorkflowEvent",
]

FailureClass = t.Literal["error", "timeout", "cancelled", "lost", "cap_exceeded"]
ApprovalOutcome = t.Literal["allow_once", "allow_session", "deny"]


class WorkflowEvent(BaseModel):
    """Base class for every object that flows between steps.

    Subclass it with typed fields; the field set becomes the payload carried by
    the edge, and is recorded as an ``event_emitted`` fact.
    """

    model_config = ConfigDict(extra="forbid")


class StartEvent(WorkflowEvent, t.Generic[T]):
    """The workflow entry point. Exactly one step may consume it."""

    input: T


class StopEvent(WorkflowEvent, t.Generic[T]):
    """Terminates the run with a result."""

    result: T


class ApprovalRequest(WorkflowEvent):
    """Emitted by a step to suspend the run pending a human decision."""

    summary: str
    payload: dict[str, t.Any] = Field(default_factory=dict)


class ApprovalDecision(WorkflowEvent):
    """The recorded decision that wakes a suspended run."""

    outcome: ApprovalOutcome
    decided_by: str | None = None
    note: str | None = None

    @property
    def allowed(self) -> bool:
        return self.outcome in ("allow_once", "allow_session")


class NodeFailure(BaseModel):
    """One sibling of a fan-out that did not produce an event."""

    node: str
    ordinal: int
    failure_class: FailureClass
    error: str | None = None


class Collect(t.Generic[Unpack[Ts]]):
    """A declarative join.

    As an annotation, ``Collect[E]`` means "run once, when every sibling event
    from the fan-out has *settled*". ``Collect[A, B]`` waits on several distinct
    event types, which is how a fork (a tuple return) is rejoined.

    At runtime the parameter is this container, carrying both sides of a partial
    failure. The author's code decides what a degraded result means; the
    ``min_success`` step argument is the declarative guard.
    """

    __slots__ = ("failed", "ok")

    def __init__(
        self,
        ok: t.Sequence[WorkflowEvent] = (),
        failed: t.Sequence[NodeFailure] = (),
    ) -> None:
        self.ok: list[t.Any] = list(ok)
        self.failed: list[NodeFailure] = list(failed)

    def __iter__(self) -> t.Iterator[t.Any]:
        """Iterating yields successes only, so the common path reads naturally."""
        return iter(self.ok)

    def __len__(self) -> int:
        """Successes only — ``len(reports)`` is the count you can use."""
        return len(self.ok)

    def __bool__(self) -> bool:
        return bool(self.ok)

    @t.overload
    def get(self, event_type: type[T]) -> T: ...

    @t.overload
    def get(self, event_type: type[T], *, required: bool) -> T | None: ...

    def get(self, event_type: type[T], *, required: bool = True) -> T | None:
        """Return the single collected event of ``event_type``.

        For multi-type joins (``Collect[A, B]``), where exactly one event of each
        declared type is expected.
        """
        matches = [e for e in self.ok if isinstance(e, event_type)]
        if not matches:
            if required:
                raise KeyError(f"no collected event of type {event_type.__name__}")
            return None
        return t.cast("T", matches[0])

    def all_of(self, event_type: type[T]) -> list[T]:
        """Return every collected event of ``event_type``."""
        return [e for e in self.ok if isinstance(e, event_type)]

    def __repr__(self) -> str:
        return f"Collect(ok={len(self.ok)}, failed={len(self.failed)})"
