"""The authoring surface: ``Workflow`` and ``@workflow.step``.

A workflow is a module-level object, one per file, living in a capability's
``workflows/`` directory — symmetric with ``workers/`` and ``agents/``.

Nothing here executes a step. This module only records what the author declared;
:mod:`dreadnode.workflows.compile` reads those declarations plus the type
annotations to derive the graph.
"""

import inspect
import typing as t

from dreadnode_workflow_core.events import WorkflowEvent

if t.TYPE_CHECKING:
    from dreadnode.workflows.context import Ctx

__all__ = ["StepDef", "Workflow"]

MIN_SUCCESS_ALL = "all"
DEFAULT_MATERIALIZATION_CAP = 25
"""PRD §19 D-14. Overridable per step; the push warns above 10."""


class StepFn(t.Protocol):
    """An async function with the stable name required by workflow topology."""

    __name__: str

    def __call__(self, *args: t.Any, **kwargs: t.Any) -> t.Awaitable[t.Any]: ...


class StepDef:
    """One authored step, before compilation.

    Holds the function and the decorator arguments. The consumed and emitted
    event types are *not* resolved here — that is compile's job, so that a
    partially-written module still imports.
    """

    __slots__ = (
        "fn",
        "key",
        "materialization_cap",
        "max_concurrency",
        "min_success",
        "retries",
        "timeout_sec",
        "title",
    )

    def __init__(
        self,
        fn: StepFn,
        *,
        title: str | None = None,
        max_concurrency: int | None = None,
        retries: int = 0,
        min_success: int | t.Literal["all"] | None = None,
        materialization_cap: int | None = None,
        timeout_sec: int | None = None,
    ) -> None:
        self.fn = fn
        self.key = fn.__name__
        self.title = title or _humanize(fn.__name__)
        self.max_concurrency = max_concurrency
        self.retries = retries
        self.min_success = min_success
        self.materialization_cap = materialization_cap
        self.timeout_sec = timeout_sec

    @property
    def doc(self) -> str | None:
        return inspect.getdoc(self.fn)

    def __call__(self, ctx: "Ctx", *args: t.Any, **kwargs: t.Any) -> t.Awaitable[t.Any]:
        """Steps stay directly callable, which keeps them unit-testable."""
        return self.fn(ctx, *args, **kwargs)

    def __repr__(self) -> str:
        return f"<StepDef {self.key}>"


class Workflow:
    """A declared workflow. One per module.

    Args:
        name: Identifier within the capability. Referenced as
            ``<capability>/<name>`` by the CLI and API.
        input: A Pydantic model describing the run input. Its JSON Schema is
            lifted into the topology and used to validate ``--input``.
        timeout_sec: Run-level ceiling. A run exceeding it is terminated and
            marked failed.
        title: Template for naming a run, with ``{field}`` placeholders drawn
            from the input model — e.g. ``"{github_url}"``. Deliberately data
            rather than a function: the *platform* renders it at run creation,
            so a run started through the API still gets a name without anything
            executing capability code. Placeholders are checked against the
            input model at compile time. Defaults to the first required string
            field, then to a short run id.
    """

    def __init__(
        self,
        *,
        name: str,
        input: type[t.Any],
        timeout_sec: int | None = None,
        title: str | None = None,
    ) -> None:
        self.name = name
        self.input = input
        self.timeout_sec = timeout_sec
        self.title = title
        self.steps: dict[str, StepDef] = {}

    @t.overload
    def step(self, fn: StepFn) -> StepDef: ...

    @t.overload
    def step(
        self,
        *,
        title: str | None = ...,
        max_concurrency: int | None = ...,
        retries: int = ...,
        min_success: int | t.Literal["all"] | None = ...,
        materialization_cap: int | None = ...,
        timeout_sec: int | None = ...,
    ) -> t.Callable[[StepFn], StepDef]: ...

    def step(
        self,
        fn: StepFn | None = None,
        *,
        title: str | None = None,
        max_concurrency: int | None = None,
        retries: int = 0,
        min_success: int | t.Literal["all"] | None = None,
        materialization_cap: int | None = None,
        timeout_sec: int | None = None,
    ) -> StepDef | t.Callable[[StepFn], StepDef]:
        """Register a step.

        Args:
            title: Display name. Defaults to a humanized function name.
            max_concurrency: Cap on simultaneous executions of this step within
                one run. Replaces the hand-rolled semaphore. Per-run, not
                per-runtime (PRD build plan §B.5).
            retries: Extra attempts for a *plain* step. Ignored for agent steps
                in Release 1, which are pinned to one attempt — retrying an LLM
                session non-durably doubles spend with no lease to fence stale
                writes.
            min_success: Only meaningful on a join. Fails the run before the
                join body runs if fewer siblings succeeded. Defaults to 1;
                ``"all"`` restores strict behavior.
            materialization_cap: Ceiling on fan-out width for a step returning a
                list. Defaults to 25.
            timeout_sec: Per-step ceiling. Exceeding it is a node failure with
                ``failure_class="timeout"``.
        """

        def register(inner: StepFn) -> StepDef:
            _require_async(inner)
            if inner.__name__ in self.steps:
                raise ValueError(f"duplicate step {inner.__name__!r} in workflow {self.name!r}")
            declared = StepDef(
                inner,
                title=title,
                max_concurrency=max_concurrency,
                retries=retries,
                min_success=min_success,
                materialization_cap=materialization_cap,
                timeout_sec=timeout_sec,
            )
            self.steps[declared.key] = declared
            return declared

        if fn is not None:
            return register(fn)
        return register

    def __repr__(self) -> str:
        return f"<Workflow {self.name!r} steps={len(self.steps)}>"


def _require_async(fn: t.Any) -> None:
    if not inspect.iscoroutinefunction(fn):
        raise TypeError(f"workflow step {getattr(fn, '__name__', fn)!r} must be an async function")


def _humanize(key: str) -> str:
    return key.replace("_", " ").title()


def _is_event_type(annotation: t.Any) -> bool:
    return isinstance(annotation, type) and issubclass(annotation, WorkflowEvent)
