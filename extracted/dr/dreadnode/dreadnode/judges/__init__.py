"""Outcome judging primitives.

Public surface:

- `OutcomeJudgement` — wire-format verdict envelope.
- `JudgeContext` — input bag passed to `OutcomeJudge.evaluate`.
- `OutcomeJudge` — abstract base class.
- `TrajectoryOutcomeJudge` — v1 agentic judge with trajectory-navigation tools.
- `TrajectoryViewer` — bundled trajectory-inspection toolset.
- `MaxStepsExhaustedError` — raised when an agentic judge runs out of steps.
- `VerdictParseError` — raised when the judge's verdict can't be parsed.

See `docs/later/OUTCOME_JUDGE.MD` for the design rationale.
"""

from .outcome import (
    JudgeContext,
    MaxStepsExhaustedError,
    OutcomeJudge,
    OutcomeJudgement,
    VerdictParseError,
)
from .trajectory import DEFAULT_JUDGE_SYSTEM_PROMPT, TrajectoryOutcomeJudge
from .trajectory_tools import TrajectoryViewer

__all__ = [
    "DEFAULT_JUDGE_SYSTEM_PROMPT",
    "JudgeContext",
    "MaxStepsExhaustedError",
    "OutcomeJudge",
    "OutcomeJudgement",
    "TrajectoryOutcomeJudge",
    "TrajectoryViewer",
    "VerdictParseError",
]
