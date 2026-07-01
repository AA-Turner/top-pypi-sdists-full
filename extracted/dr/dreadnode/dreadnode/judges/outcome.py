"""Outcome judging primitives.

The wire-format envelope (`OutcomeJudgement`), the per-evaluation input bag
(`JudgeContext`), and the abstract `OutcomeJudge` interface. Implementations
live in sibling modules — see `trajectory.py` for the v1
`TrajectoryOutcomeJudge`. The platform consumes the envelope and never sees
inside the implementation.
"""

import abc
import typing as t
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from dreadnode.agents.trajectory import Trajectory


class OutcomeJudgement(BaseModel):
    """Wire-format verdict produced by an ``OutcomeJudge``.

    Stable, minimal, and implementation-agnostic. The platform consumes this
    envelope; the judge that produced it is a private detail. New judge kinds
    do not require changes to this shape.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    passed: bool
    score: float | None = None
    reason: str = Field(min_length=1)
    metrics: dict[str, float | int] = Field(default_factory=dict)
    metadata: dict[str, t.Any] = Field(default_factory=dict)


class JudgeContext(BaseModel):
    """Everything an ``OutcomeJudge.evaluate`` call receives.

    A bag, not a hierarchy. Judges read what they need and ignore the rest.
    The v1 `TrajectoryOutcomeJudge` requires `trajectory`; future filesystem
    judges will require `working_dir`.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    trajectory: Trajectory | None = None
    task_context: dict[str, t.Any] = Field(default_factory=dict)
    working_dir: Path | None = None


class OutcomeJudge(abc.ABC):
    """Abstract primitive. One method, one return type.

    Concrete subclasses implement `evaluate(context) -> OutcomeJudgement`.
    The judge knows nothing about how it was invoked, where the trajectory
    came from, or who will read the verdict.
    """

    @abc.abstractmethod
    async def evaluate(self, context: JudgeContext) -> OutcomeJudgement: ...


class MaxStepsExhaustedError(RuntimeError):
    """Raised when an agentic judge exhausts its step budget without emitting
    a parseable verdict.

    Fail-loud (P7): the platform surfaces this as `status="errored"` rather
    than synthesizing a pass/fail verdict.
    """


class VerdictParseError(ValueError):
    """Raised when the judge's response can't be parsed into a verdict.

    Distinct from generic `ValueError` so the CLI can categorize errors
    correctly: missing-trajectory is a config error, malformed-verdict
    is a parse error.
    """


__all__ = [
    "JudgeContext",
    "MaxStepsExhaustedError",
    "OutcomeJudge",
    "OutcomeJudgement",
    "VerdictParseError",
]
