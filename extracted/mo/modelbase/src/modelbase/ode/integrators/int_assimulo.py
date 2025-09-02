from __future__ import annotations

__all__ = [
    "_IntegratorAssimulo",
]

from typing import TYPE_CHECKING, Any, Callable

import numpy as np
from assimulo.problem import Explicit_Problem  # type: ignore
from assimulo.solvers import CVode  # type: ignore
from assimulo.solvers.sundials import CVodeError  # type: ignore

from .abstract_integrator import AbstractIntegrator

if TYPE_CHECKING:
    from modelbase.typing import ArrayLike


class _IntegratorAssimulo(AbstractIntegrator):
    """Wrap around assimulo CVODE."""

    _integrator_kwargs = (
        "atol",
        "backward",
        "clock_step",
        "discr",
        "display_progress",
        "dqrhomax",
        "dqtype",
        "external_event_detection",
        "inith",
        "linear_solver",
        "maxcor",
        "maxcorS",
        "maxh",
        "maxkrylov",
        "maxncf",
        "maxnef",
        "maxord",
        "maxsteps",
        "minh",
        "norm",
        "num_threads",
        "pbar",
        "precond",
        "report_continuously",
        "rtol",
        "sensmethod",
        "suppress_sens",
        "time_limit",
        "usejac",
        "usesens",
        "verbosity",
    )

    def __init__(self, rhs: Callable, y0: ArrayLike) -> None:
        default_integrator_kwargs = {
            "atol": 1e-8,
            "rtol": 1e-8,
            "maxnef": 4,  # max error failures
            "maxncf": 1,  # max convergence failures
            "verbosity": 50,
        }
        self.problem = Explicit_Problem(rhs, y0)
        self.integrator = CVode(self.problem)
        self.kwargs: dict[str, Any] = {}
        for k, v in default_integrator_kwargs.items():
            setattr(self.integrator, k, v)

    def get_integrator_kwargs(self) -> dict[str, Any]:
        return {
            k: getattr(self.integrator, k) for k in self._integrator_kwargs
        }

    def _simulate(
        self,
        *,
        t_end: float | None = None,
        steps: int | None = None,
        time_points: ArrayLike | None = None,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[ArrayLike | None, ArrayLike | None]:
        if steps is None:
            steps = 0
        for k, v in integrator_kwargs.items():
            setattr(self.integrator, k, v)
        try:
            return self.integrator.simulate(t_end, steps, time_points)  # type: ignore
        except CVodeError:
            return None, None

    def _simulate_to_steady_state(
        self,
        *,
        tolerance: float,
        integrator_kwargs: dict[str, Any],
        simulation_kwargs: dict[str, Any],
        rel_norm: bool,
    ) -> tuple[ArrayLike | None, ArrayLike | None]:
        for k, v in integrator_kwargs.items():
            setattr(self.integrator, k, v)
        max_rounds = simulation_kwargs.get("max_rounds", 3)
        self.reset()
        t_end = 1000
        for _ in range(1, max_rounds + 1):
            try:
                t, y = self.integrator.simulate(t_end)
                diff = (y[-1] - y[-2]) / y[-1] if rel_norm else y[-1] - y[-2]
                if np.linalg.norm(diff, ord=2) < tolerance:
                    return t[-1], y[-1]
                t_end *= 1000
            except CVodeError:  # noqa: PERF203
                return None, None
        return None, None

    def reset(self) -> None:
        """Reset the integrator."""
        self.integrator.reset()
