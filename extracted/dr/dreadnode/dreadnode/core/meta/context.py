import os
import typing as t
from abc import ABC, abstractmethod

from dreadnode.core.exceptions import warn_at_user_stacklevel
from dreadnode.core.types.common import UNSET, AnyDict, Unset
from dreadnode.tracing.span import current_task_span, find_span_by_type


class ContextWarning(UserWarning):
    """Warning for issues during context resolution."""


class Context(ABC):
    """
    The abstract base class for all runtime dependency injection markers.

    Subclasses must implement the `resolve` method, which contains the logic
    for retrieving a value by name.
    """

    def __init__(
        self,
        *,
        default: t.Any | Unset = UNSET,
        required: bool = True,
    ):
        self.required = required
        self.default = default
        self._param_name: str | Unset = UNSET
        self._adapter: t.Callable[[t.Any], t.Any] | None = None

    def __repr__(self) -> str:
        parts = [
            f"name='{self._param_name!r}'",
            f"required={self.required!r}",
        ]
        if self.default is not UNSET:
            parts.append(f"default={self.default!r}")
        return f"Context({', '.join(parts)})"

    @abstractmethod
    def _resolve(self) -> t.Any:
        """
        Resolves the dependency's value.

        Returns:
            The resolved value for the dependency.
        """
        ...

    def _raise_missing_value(self) -> t.NoReturn:
        raise TypeError(f"{self!r} did not resolve to a value")

    def adapt(self, adapter: t.Callable[[t.Any], t.Any]) -> "Context":
        """
        Applies an adapter to the value after resolution.

        Args:
            adapter: A function to process the resolved value.
        """
        self._adapter = adapter
        return self

    def resolve(self) -> t.Any:
        """
        Resolves the dependency's value, handling required/default logic and warnings.

        Returns:
            The resolved value for the dependency, or the default if not found and not required.
        """
        error_name = self._param_name or f"{self!r}"
        try:
            resolved = self._resolve()
            if resolved is UNSET and self.required:
                self._raise_missing_value()
            if self._adapter and resolved is not UNSET:
                resolved = self._adapter(resolved)
        except Exception as e:
            if (resolved := self.default) is UNSET:
                if self.required:
                    raise TypeError(f"Missing required dependency: '{error_name}'") from e
                resolved = None
                warn_at_user_stacklevel(f"Failed to resolve '{error_name}': {e}", ContextWarning)

        return resolved


class CurrentRun(Context):
    """
    Retrieve the current task span from the current context (backwards compat alias).
    """

    def _resolve(self) -> t.Any:
        if (task := current_task_span.get()) is None:
            raise RuntimeError("CurrentRun() must be used inside an active task")
        return task


class CurrentTask(Context):
    """
    Retrieve the current task span from the current context.
    """

    def _resolve(self) -> t.Any:
        if (task := current_task_span.get()) is None:
            raise RuntimeError("CurrentTask() must be used inside an active task")
        return task


class ParentTask(Context):
    """
    Retrieve the parent of the current task span from the current context.
    """

    def _resolve(self) -> t.Any:
        if (task := current_task_span.get()) is None:
            raise RuntimeError("ParentTask() must be used inside an active task")
        if (parent := task.parent_task) is None:
            raise RuntimeError("ParentTask() must be used inside a nested task")
        return parent


# =============================================================================
# Typed Span Context - Domain-specific context markers
# =============================================================================

SpanContextSource = t.Literal["input", "output", "param"]
SpanContextScope = t.Literal["task", "agent", "eval", "study"]


class TypedSpanContext(Context):
    """
    A Context marker for a dynamic value from a specific span type.

    This allows scorers and other components to declaratively access inputs, outputs,
    and parameters of agents, evaluations, or studies without needing to be explicitly
    passed them.
    """

    # Map user-friendly scope names to span type attributes
    SCOPE_TO_TYPE: t.ClassVar[dict[str, str | None]] = {
        "task": None,  # Current task, no search needed
        "agent": "agent",
        "eval": "evaluation",
        "study": "study",
    }

    def __init__(
        self,
        name: str | None,
        source: SpanContextSource,
        scope: SpanContextScope,
        *,
        default: t.Any | Unset = UNSET,
        required: bool = True,
    ) -> None:
        """
        Args:
            name: The name of the value to retrieve.
            source: The source to retrieve from ('input', 'output', 'param').
            scope: The span type scope ('task', 'agent', 'eval', 'study').
            default: A default value if the named value is not found.
            required: Whether the context is required or not.
        """
        super().__init__(default=default, required=required)

        self.ref_name = name
        self.source = source
        self.scope = scope

    def __repr__(self) -> str:
        parts = [
            f"name='{self.ref_name or '<first>'}'",
            f"source='{self.source}'",
            f"scope='{self.scope}'",
            f"required={self.required!r}",
        ]
        if self.default is not UNSET:
            parts.append(f"default={self.default!r}")
        return f"TypedSpanContext({', '.join(parts)})"

    def _resolve(self) -> t.Any:
        # Find the target span based on scope
        if self.scope == "task":
            target_span = current_task_span.get()
        else:
            span_type = self.SCOPE_TO_TYPE[self.scope]
            target_span = find_span_by_type(span_type) if span_type else None

        if target_span is None:
            raise RuntimeError(f"No active '{self.scope}' span in context.")

        # Get the value container based on source
        value_container: AnyDict = {}
        if self.source == "input":
            value_container = target_span.inputs
        elif self.source == "output":
            value_container = target_span.outputs
        elif self.source == "param":
            value_container = target_span.params

        # Find the value
        container_key = self.ref_name or next(iter(value_container.keys()), None)

        if container_key is None:
            raise RuntimeError(
                f"Could not select first key from empty '{self.source}' container in '{self.scope}' span."  # noqa: S608 - diagnostic string only, not executed as SQL
            )

        try:
            return value_container[container_key]
        except (KeyError, AttributeError) as e:
            available = list(value_container.keys()) if value_container else []
            raise RuntimeError(
                f"{self.source.capitalize()} '{self.ref_name}' not found in '{self.scope}' span. "
                f"Available: {available}"
            ) from e


# =============================================================================
# Task Context Markers (current task)
# =============================================================================


def TaskInput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str | None = None, *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an input from the current task.

    Args:
        name: The name of the input. If None, uses the first input logged.
        default: A default value if the named input is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "input", "task", default=default, required=required)


def TaskOutput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str = "output", *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an output from the current task.

    Args:
        name: The name of the output.
        default: A default value if the named output is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "output", "task", default=default, required=required)


# =============================================================================
# Agent Context Markers
# =============================================================================


def AgentInput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str | None = None, *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an input from the nearest agent span.

    Args:
        name: The name of the input. If None, uses the first input logged.
        default: A default value if the named input is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "input", "agent", default=default, required=required)


def AgentOutput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str = "output", *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an output from the nearest agent span.

    Args:
        name: The name of the output.
        default: A default value if the named output is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "output", "agent", default=default, required=required)


def AgentParam(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str, *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference a parameter from the nearest agent span.

    Args:
        name: The name of the parameter.
        default: A default value if the named parameter is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "param", "agent", default=default, required=required)


# =============================================================================
# Evaluation Context Markers
# =============================================================================


def EvalInput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str | None = None, *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an input from the nearest evaluation span.

    Args:
        name: The name of the input. If None, uses the first input logged.
        default: A default value if the named input is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "input", "eval", default=default, required=required)


def EvalOutput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str = "output", *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an output from the nearest evaluation span.

    Args:
        name: The name of the output.
        default: A default value if the named output is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "output", "eval", default=default, required=required)


def EvalParam(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str, *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference a parameter from the nearest evaluation span.

    Args:
        name: The name of the parameter.
        default: A default value if the named parameter is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "param", "eval", default=default, required=required)


# =============================================================================
# Study Context Markers
# =============================================================================


def StudyInput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str | None = None, *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an input from the nearest study span.

    Args:
        name: The name of the input. If None, uses the first input logged.
        default: A default value if the named input is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "input", "study", default=default, required=required)


def StudyOutput(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str = "output", *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference an output from the nearest study span.

    Args:
        name: The name of the output.
        default: A default value if the named output is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "output", "study", default=default, required=required)


def StudyParam(  # noqa: N802 - public marker factory intentionally uses CamelCase
    name: str, *, default: t.Any | Unset = UNSET, required: bool = True
) -> TypedSpanContext:
    """
    Reference a parameter from the nearest study span.

    Args:
        name: The name of the parameter.
        default: A default value if the named parameter is not found.
        required: Whether the context is required.
    """
    return TypedSpanContext(name, "param", "study", default=default, required=required)


# =============================================================================
# Dataset Context Marker
# =============================================================================


class DatasetField(Context):
    """
    A Context marker for a value from the full dataset sample row
    for the current evaluation task.
    """

    def __init__(self, name: str, *, default: t.Any | Unset = UNSET, required: bool = True):
        super().__init__(default=default, required=required)
        self.ref_name = name

    def __repr__(self) -> str:
        return f"DatasetField(name='{self.ref_name}')"

    def _resolve(self) -> t.Any:
        from dreadnode.evaluations.evaluation import current_dataset_row

        if (row := current_dataset_row.get()) is None:
            raise RuntimeError("DatasetField() can only be used within an active Eval.")

        try:
            return row[self.ref_name]
        except Exception as e:
            available = list(row.keys())
            raise RuntimeError(
                f"Field '{self.ref_name}' not found in dataset sample. "
                f"Available fields: {available}"
            ) from e


# =============================================================================
# Trial/Optimization Context Markers
# =============================================================================


class CurrentTrial(Context):
    """
    Retrieve the current trial during an optimization study.
    """

    def _resolve(self) -> t.Any:
        from dreadnode.optimization.study import current_trial

        if (trial := current_trial.get()) is None:
            raise RuntimeError("CurrentTrial() must be used inside an active optimization study.")

        return trial


class TrialCandidate(Context):
    """
    Retrieve the candidate of the current trial during an optimization study.
    """

    def _resolve(self) -> t.Any:
        from dreadnode.optimization.study import current_trial

        if (trial := current_trial.get()) is None:
            raise RuntimeError("TrialCandidate() must be used inside an active optimization study.")

        return trial.candidate


class TrialOutput(Context):
    """
    Retrieve the evaluation result of the current trial during an optimization study.
    """

    def _resolve(self) -> t.Any:
        from dreadnode.optimization.study import current_trial

        if (trial := current_trial.get()) is None:
            raise RuntimeError("TrialOutput() must be used inside an active optimization study.")

        return trial.evaluation_result


class TrialScore(Context):
    """
    Retrieve the score of the current trial during an optimization study.
    """

    def _resolve(self) -> t.Any:
        from dreadnode.optimization.study import current_trial

        if (trial := current_trial.get()) is None:
            raise RuntimeError("TrialScore() must be used inside an active optimization study.")

        return trial.score


# =============================================================================
# Environment Context Marker
# =============================================================================


class EnvVar(Context):
    """
    A Context marker for an environment variable.
    """

    def __init__(self, name: str, *, default: t.Any | Unset = UNSET, required: bool = True):
        super().__init__(default=default, required=required)
        self.var_name = name

    def __repr__(self) -> str:
        return f"EnvVar(name='{self.var_name}')"

    def _resolve(self) -> t.Any:
        return os.environ[self.var_name]
