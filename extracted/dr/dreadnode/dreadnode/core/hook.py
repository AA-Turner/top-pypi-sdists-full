import functools
import inspect
import typing as t

import typing_extensions as te

from dreadnode.core.metric import MetricSeries

if t.TYPE_CHECKING:
    from dreadnode.agents.events import AgentEvent, AgentEventT
    from dreadnode.agents.reactions import Reaction
    from dreadnode.core.conditions import Condition
    from dreadnode.core.scorer import Scorer

# TypeVar for event types - default to AgentEvent
AgentEventT = te.TypeVar("AgentEventT", bound="AgentEvent", default="AgentEvent")  # ty: ignore[invalid-assignment]

# Legacy type alias for backward compatibility
EventCondition = t.Callable[[AgentEventT], bool]


class Hook(t.Generic[AgentEventT]):
    """
    Decorator class to mark a function or method as a hook.

    Can be used in three ways:

    1. Standalone async function (direct hook):
        @hook(GenerationStep)
        async def my_hook(event: GenerationStep) -> Reaction | None:
            ...

    2. With conditions and scorers:
        @hook(GenerationStep, when=[quality.above(0.5)], scorers=[safety])
        async def gated_hook(event: GenerationStep) -> Reaction | None:
            # event.metrics["quality"] and event.metrics["safety"] available
            ...

    3. Factory function (returns hook):
        @hook(AgentError)
        def backoff_on_error(max_tries: int = 5) -> Hook:
            async def inner(event: AgentError) -> Reaction | None:
                ...
            return inner

    4. Class method:
        class MyHooks:
            @hook(GenerationStep)
            async def my_hook(self, event: GenerationStep) -> Reaction | None:
                ...

    Attributes:
        func: The hook function.
        event_type: The event type to listen for.
        when: List of conditions that gate hook execution. Conditions are
            evaluated in order. ScoringConditions attach metrics as side effects.
        scorers: List of scorers to run and attach metrics (after conditions pass).
        condition: (Deprecated) Legacy single condition.
    """

    def __init__(
        self,
        func: t.Callable[..., t.Any],
        event_type: type[AgentEventT],
        *,
        condition: "EventCondition[AgentEventT] | None" = None,
        when: "list[Condition[AgentEventT]] | Condition[AgentEventT] | None" = None,
        scorers: "list[Scorer[AgentEventT]] | None" = None,
    ):
        self.func = func
        self.event_type = event_type
        self.condition = condition  # Legacy condition support
        self.when: list[Condition[AgentEventT]] = (
            [when] if when is not None and not isinstance(when, list) else (when or [])  # ty: ignore[invalid-assignment]
        )
        self.scorers: list[Scorer[AgentEventT]] = scorers or []
        self.__name__: str = getattr(func, "__name__", repr(func))

    def __call__(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        """
        Call the hook.

        For direct async hooks: passes the event and filters by type/condition.
        For factory functions: passes args to create the inner hook (sync).
        """
        # Check if this is being called with an event (direct hook pattern)
        from dreadnode.agents.events import AgentEvent

        if args and isinstance(args[0], AgentEvent):
            return self._handle_event(args[0])

        # Otherwise, this is a factory function being called with config args
        return self.func(*args, **kwargs)

    async def _handle_event(self, event: "AgentEvent") -> "Reaction | None":
        """Handle an event asynchronously."""
        # 1. Type check
        if not isinstance(event, self.event_type):
            return None

        # Skip ReactStep when listening to AgentStep to prevent hooks from
        # reacting to their own reactions. Use @hook(ReactStep) explicitly
        # if you need to handle reaction events.
        from dreadnode.agents.events import AgentStep, ReactStep

        if self.event_type is AgentStep and isinstance(event, ReactStep):
            return None

        # 2. Evaluate conditions in order
        # Legacy condition support
        if self.condition is not None:
            condition_result = self.condition(event)
            if inspect.isawaitable(condition_result):
                condition_result = await condition_result
            if not condition_result:
                return None

        # New when conditions (may attach metrics as side effects)
        for cond in self.when:
            passed = await cond.evaluate(event)
            if not passed:
                return None

        # 3. Run scorers and attach metrics
        for scorer in self.scorers:
            metric = await scorer.score(event)
            if hasattr(event, "metrics"):
                series = event.metrics.setdefault(scorer.name, MetricSeries())
                step = getattr(event, "step", 0)
                series.append(value=metric.value, step=step)

        # 4. Run hook body
        result = self.func(event)
        if inspect.isawaitable(result):
            return await result
        return result

    def __get__(self, obj: t.Any, objtype: type | None = None) -> "Hook[AgentEventT]":
        """Descriptor protocol — return a ``Hook`` bound to ``obj``.

        Symmetric with :meth:`ToolMethod.__get__`: class access returns
        the descriptor itself (so introspection works), instance access
        returns a fresh ``Hook`` whose ``func`` is the original method
        with ``self`` pre-bound. The bound hook routes through
        :meth:`_handle_event` like every other hook, so the
        type-check / conditions / scorers chain has exactly one
        implementation.
        """
        if obj is None:
            return self

        bound_func = functools.partial(self.func, obj)
        bound = Hook(
            bound_func,
            self.event_type,
            condition=self.condition,
            when=self.when,
            scorers=self.scorers,
        )
        bound.__name__ = self.__name__
        return bound


def hook(
    event_type: type[AgentEventT],
    condition: EventCondition[AgentEventT] | None = None,
    *,
    when: "list[Condition[AgentEventT]] | Condition[AgentEventT] | None" = None,
    scorers: "list[Scorer[AgentEventT]] | None" = None,
) -> "t.Callable[[t.Callable[..., t.Awaitable[Reaction | None]]], Hook[AgentEventT]]":
    """
    Decorator to mark a method as hook.

    Args:
        event_type: The event type to listen for.
        condition: (Deprecated) Legacy single condition. Use `when` instead.
        when: List of conditions that gate hook execution. Conditions are
            evaluated in order. ScoringConditions attach metrics as side effects.
        scorers: List of scorers to run and attach metrics (after conditions pass).

    Examples:
        ```python
        # Basic hook
        @hook(GenerationStep)
        async def observe(event: GenerationStep) -> None:
            print(f"Generated: {event.content}")

        # Hook with scoring condition
        @hook(GenerationStep, when=[quality.above(0.5)])
        async def high_quality_only(event: GenerationStep) -> None:
            # Only runs if quality > 0.5
            # event.metrics["quality"] available
            ...

        # Hook with multiple conditions and scorers
        @hook(
            GenerationStep,
            when=[quality.above(0.5), tool_called("bash")],
            scorers=[safety, toxicity],
        )
        async def gated_with_metrics(event: GenerationStep) -> Reaction | None:
            # Runs if quality > 0.5 AND tool is bash
            # Metrics: quality, safety, toxicity all attached
            if event.metrics["safety"].value < 0.5:
                return Fail("Unsafe")
            return None
        ```
    """

    def decorator(func: "t.Callable[..., t.Awaitable[Reaction | None]]") -> Hook[AgentEventT]:
        return Hook(func, event_type, condition=condition, when=when, scorers=scorers)

    return decorator
