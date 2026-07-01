"""Optuna-based sampler - uses Optuna's advanced samplers (TPE, etc.)."""

import typing as t

import optuna
from loguru import logger

from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.search import (
    Categorical,
    Float,
    Int,
    SearchSpace,
)
from dreadnode.optimization.trial import Trial


def _convert_search_space(
    search_space: SearchSpace,
) -> dict[str, optuna.distributions.BaseDistribution]:
    """Convert our SearchSpace to Optuna's distribution format."""
    optuna_space: dict[str, optuna.distributions.BaseDistribution] = {}

    for name, dist in search_space.items():
        if isinstance(dist, Float):
            optuna_space[name] = optuna.distributions.FloatDistribution(
                low=dist.low, high=dist.high, log=dist.log, step=dist.step
            )
        elif isinstance(dist, Int):
            optuna_space[name] = optuna.distributions.IntDistribution(
                low=dist.low, high=dist.high, log=dist.log, step=dist.step
            )
        elif isinstance(dist, Categorical):
            optuna_space[name] = optuna.distributions.CategoricalDistribution(choices=dist.choices)
        elif isinstance(dist, list):
            # Shorthand: list of values treated as categorical
            optuna_space[name] = optuna.distributions.CategoricalDistribution(choices=dist)
        else:
            raise TypeError(f"Unsupported distribution type: {type(dist)}")

    return optuna_space


class OptunaSampler(Sampler[dict[str, t.Any]]):
    """
    Sampler using Optuna's advanced optimization algorithms.

    Wraps Optuna's samplers (TPE, CMA-ES, etc.) for Bayesian optimization.
    Learns from previous trials to suggest better candidates.

    Example:
        sampler = OptunaSampler(
            search_space={
                "temperature": Float(0.0, 2.0),
                "max_tokens": Int(100, 1000),
            },
            sampler=optuna.samplers.TPESampler(),
        )

    Args:
        search_space: Dictionary mapping parameter names to distributions.
        sampler: Optuna sampler to use. Defaults to TPESampler.
        directions: Optimization directions for multi-objective.
            Defaults to ["maximize"].
    """

    def __init__(
        self,
        search_space: SearchSpace,
        *,
        sampler: optuna.samplers.BaseSampler | None = None,
        directions: list[t.Literal["maximize", "minimize"]] | None = None,
    ):
        if not search_space:
            raise ValueError("Search space cannot be empty")

        self.search_space = _convert_search_space(search_space)
        self.directions = directions or ["maximize"]

        # Create Optuna study
        self._study = optuna.create_study(
            directions=self.directions,
            sampler=sampler,
        )

        # Track pending trial for tell()
        self._pending_trial: optuna.trial.Trial | None = None
        self._objective_names: list[str] = []

        logger.info(
            f"OptunaSampler initialized: "
            f"sampler={self._study.sampler.__class__.__name__}, "
            f"directions={self.directions}"
        )

    def sample(self, history: list[Trial[dict]]) -> list[Sample[dict]]:  # noqa: ARG002
        """Ask Optuna for the next candidate."""
        self._pending_trial = self._study.ask(self.search_space)
        return [Sample(self._pending_trial.params)]

    def tell(self, trials: list[Trial[dict]]) -> None:
        """Inform Optuna of trial results."""
        if self._pending_trial is None:
            return

        for trial in trials:
            if trial.status == "finished":
                # Update objective names from first successful trial
                if not self._objective_names and trial.scores:
                    self._objective_names = list(trial.scores.keys())

                # Provide scores in correct order for multi-objective
                if self._objective_names:
                    scores = [trial.scores.get(name, 0.0) for name in self._objective_names]
                else:
                    scores = [trial.score]

                self._study.tell(self._pending_trial, scores)

            elif trial.status == "pruned":
                self._study.tell(self._pending_trial, state=optuna.trial.TrialState.PRUNED)

            else:  # failed
                self._study.tell(self._pending_trial, state=optuna.trial.TrialState.FAIL)

        self._pending_trial = None

    @property
    def exhausted(self) -> bool:
        """Optuna sampler never exhausts - always returns False."""
        return False

    def reset(self) -> None:
        """Reset the Optuna study."""
        self._study = optuna.create_study(
            directions=self.directions,
            sampler=self._study.sampler,
        )
        self._pending_trial = None

    @property
    def best_params(self) -> dict[str, t.Any] | None:
        """Get the best parameters found so far."""
        try:
            return self._study.best_params
        except ValueError:
            return None

    @property
    def best_value(self) -> float | None:
        """Get the best objective value found so far."""
        try:
            return self._study.best_value
        except ValueError:
            return None
