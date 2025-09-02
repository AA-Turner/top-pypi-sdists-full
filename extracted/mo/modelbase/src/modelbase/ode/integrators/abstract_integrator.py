from __future__ import annotations

__all__ = [
    "AbstractIntegrator",
]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from modelbase.typing import Array, ArrayLike


class AbstractIntegrator(ABC):

    """Interface for integrators"""

    def __init__(self, rhs: Callable, y0: Array | ArrayLike) -> None:
        self.kwargs: dict[str, Any] = {}
        self.rhs = rhs
        self.y0 = y0

    @abstractmethod
    def reset(self) -> None:
        """Reset the integrator and simulator state"""
        ...

    @abstractmethod
    def _simulate(
        self,
        *,
        t_end: float | None = None,
        steps: int | None = None,
        time_points: ArrayLike | None = None,
        **integrator_kwargs: dict[str, Any],
    ) -> tuple[ArrayLike | None, ArrayLike | None]:
        ...

    @abstractmethod
    def _simulate_to_steady_state(
        self,
        *,
        tolerance: float,
        integrator_kwargs: dict[str, Any],
        simulation_kwargs: dict[str, Any],
        rel_norm: bool,
    ) -> tuple[ArrayLike | None, ArrayLike | None]:
        ...

    @abstractmethod
    def get_integrator_kwargs(self) -> dict[str, Any]:
        """Get possible integration settings"""
        ...
