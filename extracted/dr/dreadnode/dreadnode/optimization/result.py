import json
import typing as t
from dataclasses import dataclass, field
from pathlib import Path
from statistics import mean

from dreadnode.optimization.trial import CandidateT, Trial

if t.TYPE_CHECKING:
    import pandas as pd

    from dreadnode.evaluations.result import EvalResult

StudyStopReason = t.Literal[
    "max_trials_reached",
    "stop_condition_met",
    "search_exhausted",
    "error",
    "unknown",
]


@dataclass
class OptimizationEvaluation:
    """Normalized evaluator output for optimize_anything."""

    score: float | None = None
    scores: dict[str, float] = field(default_factory=dict)
    side_info: dict[str, t.Any] = field(default_factory=dict)
    evaluation_result: "EvalResult[t.Any, t.Any] | None" = None
    traces: t.Any = None


def normalize_optimization_evaluation(value: t.Any) -> OptimizationEvaluation:
    """Normalize evaluator output into an OptimizationEvaluation."""
    if isinstance(value, OptimizationEvaluation):
        return value

    if isinstance(value, int | float):
        return OptimizationEvaluation(score=float(value))

    if isinstance(value, dict):
        known_fields = {"score", "scores", "side_info", "evaluation_result", "traces"}
        if known_fields.intersection(value):
            score = value.get("score")
            raw_scores = value.get("scores")
            scores = (
                {
                    str(key): float(item)
                    for key, item in raw_scores.items()
                    if isinstance(key, str) and isinstance(item, int | float)
                }
                if isinstance(raw_scores, dict)
                else {}
            )
            if score is None and scores:
                score = mean(scores.values())
            return OptimizationEvaluation(
                score=float(score) if isinstance(score, int | float) else None,
                scores=scores,
                side_info=value.get("side_info", {})
                if isinstance(value.get("side_info"), dict)
                else {},
                evaluation_result=value.get("evaluation_result"),
                traces=value.get("traces"),
            )

        scores = {
            str(key): float(item)
            for key, item in value.items()
            if isinstance(key, str) and isinstance(item, int | float)
        }
        return OptimizationEvaluation(
            score=mean(scores.values()) if scores else None,
            scores=scores,
        )

    raise TypeError(
        "Optimization evaluators must return a number, a score mapping, or "
        "an OptimizationEvaluation-compatible mapping."
    )


@dataclass
class OptimizationResult(t.Generic[CandidateT]):
    """Result of a Dreadnode optimize_anything run."""

    backend: str
    seed_candidate: CandidateT | None = None
    best_candidate: CandidateT | None = None
    best_score: float | None = None
    best_scores: dict[str, float] = field(default_factory=dict)
    objective: str | None = None
    train_size: int = 0
    val_size: int = 0
    pareto_frontier: list[CandidateT] = field(default_factory=list)
    history: list[t.Any] = field(default_factory=list)
    metadata: dict[str, t.Any] = field(default_factory=dict)
    raw_result: t.Any = field(default=None, repr=False)

    def __repr__(self) -> str:
        parts = [
            f"backend='{self.backend}'",
            f"train_size={self.train_size}",
            f"val_size={self.val_size}",
        ]
        if self.best_score is not None:
            parts.append(f"best_score={self.best_score:.4f}")
        if self.best_candidate is not None:
            parts.append("best_candidate=<set>")
        return f"{self.__class__.__name__}({', '.join(parts)})"

    def to_dict(self) -> dict[str, t.Any]:
        """Return a JSON-serializable result dictionary."""
        return {
            "backend": self.backend,
            "seed_candidate": self.seed_candidate,
            "best_candidate": self.best_candidate,
            "best_score": self.best_score,
            "best_scores": self.best_scores,
            "objective": self.objective,
            "train_size": self.train_size,
            "val_size": self.val_size,
            "pareto_frontier": self.pareto_frontier,
            "history": self.history,
            "metadata": self.metadata,
        }

    @property
    def frontier_size(self) -> int:
        """Return the number of candidates currently on the Pareto frontier."""
        return len(self.pareto_frontier)


@dataclass
class StudyResult(t.Generic[CandidateT]):
    """
    The final result of an optimization study, containing all trials and summary statistics.

    Attributes:
        trials: A complete list of all trials generated during the study.
        stop_reason: The reason the study concluded.
        stop_explanation: A human-readable explanation for why the study stopped.
    """

    trials: list[Trial[CandidateT]] = field(default_factory=list)
    stop_reason: StudyStopReason = "unknown"
    stop_explanation: str | None = None

    _best_trial: Trial[CandidateT] | None = field(init=False, repr=False, default=None)

    def __post_init__(self) -> None:
        if finished_trials := [t for t in self.trials if t.status == "finished"]:
            self._best_trial = max(finished_trials, key=lambda t: (t.score, t.step))

    def __repr__(self) -> str:
        parts = [
            f"trials={len(self.trials)}",
            f"stop_reason='{self.stop_reason}'",
        ]
        if self.stop_explanation:
            parts.append(f"stop_explanation='{self.stop_explanation}'")
        if self.best_trial:
            parts.append(f"best_trial={self.best_trial.id}")
        return f"{self.__class__.__name__}({', '.join(parts)})"

    @property
    def best_trial(self) -> Trial[CandidateT] | None:
        """The trial with the highest score among all finished trials. Returns None if no trials succeeded."""
        return self._best_trial

    @property
    def best_score(self) -> float | None:
        """The highest score among all finished trials. Returns None if no trials succeeded."""
        return self._best_trial.score if self._best_trial else None

    @property
    def total_trials(self) -> int:
        """Total number of trials."""
        return len(self.trials)

    @property
    def finished_trials(self) -> int:
        """Number of successfully finished trials."""
        return len([t for t in self.trials if t.status == "finished"])

    @property
    def failed_trials(self) -> list[Trial[CandidateT]]:
        """A list of all trials that failed."""
        return [t for t in self.trials if t.status == "failed"]

    @property
    def pruned_trials(self) -> list[Trial[CandidateT]]:
        """A list of all trials that were pruned."""
        return [t for t in self.trials if t.status == "pruned"]

    @property
    def pending_trials(self) -> list[Trial[CandidateT]]:
        """A list of all trials that are still pending."""
        return [t for t in self.trials if t.status == "pending"]

    @property
    def running_trials(self) -> list[Trial[CandidateT]]:
        """A list of all trials that are currently running."""
        return [t for t in self.trials if t.status == "running"]

    def to_dicts(self) -> list[dict[str, t.Any]]:
        """Flattens the results into a list of dictionaries, one for each trial."""
        records = []
        for trial in self.trials:
            base_record = trial.model_dump(exclude={"candidate"}, mode="json")

            candidate = trial.candidate
            if isinstance(candidate, dict):
                # Flatten candidate dict into individual columns
                for key, value in candidate.items():
                    base_record[f"candidate_{key}"] = value
            else:
                base_record["candidate"] = candidate

            records.append(base_record)
        return records

    def to_dataframe(self) -> "pd.DataFrame":
        """Converts the trials into a pandas DataFrame for analysis."""
        import pandas as pd

        return pd.DataFrame(self.to_dicts())

    def to_jsonl(self, path: str | Path) -> None:
        """Saves the trials to a JSON Lines (JSONL) file."""
        records = self.to_dicts()
        with Path(path).open("w", encoding="utf-8") as f:
            f.writelines(json.dumps(record) + "\n" for record in records)
