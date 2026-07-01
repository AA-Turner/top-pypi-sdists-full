from __future__ import annotations

import abc
import inspect
import typing as t
from dataclasses import dataclass, field

import typing_extensions as te

from dreadnode.optimization.result import (
    OptimizationEvaluation,
    normalize_optimization_evaluation,
)

if t.TYPE_CHECKING:
    from dreadnode.optimization.api import Optimization
    from dreadnode.optimization.events import OptimizationEvent

CandidateT = te.TypeVar("CandidateT", default=t.Any)
SideInfo = dict[str, t.Any]
EvaluatorResult = (
    OptimizationEvaluation
    | tuple[float, SideInfo]
    | float
    | t.Awaitable[OptimizationEvaluation | tuple[float, SideInfo] | float]
)


@dataclass
class OptimizationEvaluationBatch:
    """Batch evaluation data returned by Dreadnode-native adapters."""

    outputs: list[t.Any] = field(default_factory=list)
    scores: list[float] = field(default_factory=list)
    trajectories: list[t.Any] | None = None
    objective_scores: list[dict[str, float]] | None = None


class OptimizationDependencyError(ImportError):
    """Raised when an optimization backend dependency is unavailable."""


class OptimizationBackendError(RuntimeError):
    """Raised when an optimization backend cannot execute a request."""


class OptimizationEvaluator(t.Protocol[CandidateT]):
    """Callable used to score a text candidate."""

    def __call__(self, candidate: CandidateT, /, *args: t.Any) -> EvaluatorResult: ...


class OptimizationAdapter(t.Protocol[CandidateT]):
    """Adapter contract for systems that need batched evaluation and reflection."""

    def seed_candidate(self) -> CandidateT: ...

    def evaluate(
        self,
        batch: list[t.Any],
        candidate: CandidateT,
        *,
        capture_traces: bool = False,
    ) -> OptimizationEvaluationBatch | t.Awaitable[OptimizationEvaluationBatch]: ...

    def make_reflective_dataset(
        self,
        candidate: CandidateT,
        eval_batch: OptimizationEvaluationBatch,
        components_to_update: list[str],
    ) -> dict[str, list[dict[str, t.Any]]]: ...


class OptimizationBackend(abc.ABC, t.Generic[CandidateT]):
    """Base interface for optimization backends."""

    @abc.abstractmethod
    async def stream(
        self,
        optimization: Optimization[CandidateT],
    ) -> t.AsyncGenerator[OptimizationEvent[CandidateT], None]:
        yield


def normalize_evaluation_result(
    result: OptimizationEvaluation | tuple[float, SideInfo] | float,
) -> OptimizationEvaluation:
    """Normalize evaluator return values into a single Dreadnode shape."""
    if isinstance(result, tuple):
        score, side_info = result
        return OptimizationEvaluation(score=float(score), side_info=dict(side_info))  # ty: ignore[no-matching-overload] - side_info is a generic mapping
    return normalize_optimization_evaluation(result)


def invoke_with_supported_args(
    callback: t.Callable[..., t.Any],
    *args: t.Any,
    **kwargs: t.Any,
) -> t.Any:
    """Invoke a callback while trimming unsupported positional args."""
    try:
        signature = inspect.signature(callback)
    except (TypeError, ValueError):
        return callback(*args, **kwargs)

    parameters = list(signature.parameters.values())
    if any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in parameters):
        return callback(*args, **kwargs)

    positional_capacity = len(
        [
            param
            for param in parameters
            if param.kind
            in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ]
    )
    return callback(*args[:positional_capacity], **kwargs)
