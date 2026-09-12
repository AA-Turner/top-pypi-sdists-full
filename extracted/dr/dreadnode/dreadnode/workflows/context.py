"""The ``Ctx`` handle a step uses to reach agents, the workspace, and logging.

Deliberately small. Events flow through parameters and return values; ``ctx`` is
for the cross-cutting handles that do not belong in an event payload.

This module defines the *contract*. The runtime host supplies the implementation
(see ``dreadnode.workflows.host``); tests can supply their own, which is why this
is a Protocol rather than a concrete class.
"""

import typing as t
from pathlib import Path

if t.TYPE_CHECKING:
    from dreadnode.workflows.workflow import StepDef

__all__ = ["AgentResult", "Ctx", "ToolCall"]

T = t.TypeVar("T")


class ToolCall(t.Protocol):
    """One tool invocation observed during an agent turn."""

    @property
    def name(self) -> str: ...

    @property
    def arguments(self) -> dict[str, t.Any]: ...


class AgentResult(t.Protocol):
    """The result of one ``ctx.agent(...)`` invocation."""

    @property
    def output(self) -> str: ...

    @property
    def tool_calls(self) -> list[ToolCall]: ...

    @property
    def session_id(self) -> str:
        """Links this node to its transcript.

        Recorded as a fact at agent *start*, not on completion — so a node that
        fails or times out mid-agent still links to its partial transcript
        (build plan §B.3).
        """
        ...

    def parse(self, model: type[T]) -> T: ...


class Ctx(t.Protocol):
    """Five members, plus the runtime-bus bridge."""

    @property
    def input(self) -> t.Any:
        """The workflow's typed input."""
        ...

    @property
    def workspace(self) -> Path:
        """A run-scoped directory shared across steps.

        Release 1: local to the runtime host process. A run-scoped *shared*
        workspace across separately-sandboxed steps is deferred, which is why a
        pipeline that passes filesystem paths between steps is runtime-host-only
        until it lands (build plan §B.2).
        """
        ...

    def result(self, step: "StepDef | str") -> t.Any:
        """The event emitted by a completed upstream step.

        Returns the *most recently completed* execution of that step. The wording
        is load-bearing: in a DAG there is only one, but bounded loops would make
        several, and defining it as "the" output today would silently change
        meaning later.

        It is a compile error to reference a step with fan-out cardinality —
        ``ctx.result(specialist)`` is ambiguous when there are five. Use a
        ``Collect[...]`` join instead.
        """
        ...

    async def agent(
        self,
        name: str,
        prompt: str,
        *,
        model: str | None = None,
        max_steps: int | None = None,
        labels: dict[str, str] | None = None,
    ) -> AgentResult:
        """Run an agent as a sub-unit of this step.

        A plain library call — a step may call it zero, one, or many times with
        arbitrary Python around it, which is why an agent is not a special node
        kind.
        """
        ...

    def log(self, message: str, **fields: t.Any) -> None:
        """Structured step log, surfaced on the node in the UI."""
        ...

    def publish_runtime_event(self, kind: str, payload: dict[str, t.Any]) -> None:
        """Put a *runtime-bus* event on the wire, for external reactors.

        Named to read as what it is, and deliberately distinct from *returning* a
        workflow event, which advances the graph. Best-effort: the bus is bounded
        and drops slow subscribers.
        """
        ...
