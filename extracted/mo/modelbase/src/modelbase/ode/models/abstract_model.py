from __future__ import annotations

__all__ = [
    "_AbstractRateModel",
    "_AbstractStoichiometricModel",
]

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from modelbase.core import (
    AlgebraicMixin,
    BaseModel,
    CompoundMixin,
    RateMixin,
    StoichiometricMixin,
)

if TYPE_CHECKING:
    from modelbase.typing import Array, ArrayLike


class _AbstractStoichiometricModel(StoichiometricMixin, CompoundMixin, BaseModel, ABC):
    @abstractmethod
    def _get_rhs(self, t: float | ArrayLike, y: list[Array]) -> Array:
        pass


class _AbstractRateModel(RateMixin, AlgebraicMixin, _AbstractStoichiometricModel):
    def _collect_used_parameters(self) -> set[str]:
        used_parameters = set()
        for par in self.derived_parameters.values():
            used_parameters.update(par["parameters"])
        for module in self.algebraic_modules.values():
            used_parameters.update(module.parameters)
        for rate in self.rates.values():
            used_parameters.update(rate.parameters)
        return used_parameters

    def check_unused_parameters(self) -> set[str]:
        used_parameters = self._collect_used_parameters()
        return self.get_all_parameter_names().difference(used_parameters)

    def check_missing_parameters(self) -> set[str]:
        used_parameters = self._collect_used_parameters()
        return used_parameters.difference(self.get_all_parameter_names())

    def remove_unused_parameters(self) -> None:
        self.remove_parameters(self.check_unused_parameters())

    def _collect_used_compounds(self) -> set[str]:
        return {
            i for i in self.compounds if len(self.stoichiometries_by_compounds[i]) > 0
        }

    def check_unused_compounds(self) -> set[str]:
        used_compounds = self._collect_used_compounds()
        return used_compounds.difference(self.compounds)

    def remove_unused_compounds(self) -> None:
        self.remove_compounds(self.check_unused_compounds())

    def get_readout_names(
        self,
    ) -> list[str]:
        return list(self.readouts.keys())

    @abstractmethod
    def get_full_concentration_dict(
        self,
        y: dict[str, float] | dict[str, Array] | ArrayLike | Array,
        t: float | ArrayLike | Array = 0.0,
        include_readouts: bool = False,
    ) -> dict[str, Array]:
        ...

    @abstractmethod
    def get_fluxes_dict(
        self,
        y: dict[str, float] | dict[str, ArrayLike] | dict[str, Array] | Array | ArrayLike,
        t: float | ArrayLike | Array = 0.0,
    ) -> dict[str, Array]:
        ...

    def get_fluxes_array(
        self,
        y: dict[str, float] | dict[str, ArrayLike] | dict[str, Array] | Array | ArrayLike,
        t: float | ArrayLike | Array = 0.0,
    ) -> Array:
        """Calculate the fluxes at time point(s) t."""
        return np.array(list(self.get_fluxes_dict(y=y, t=t).values())).T

    def get_fluxes_df(
        self,
        y: dict[str, float] | dict[str, ArrayLike] | dict[str, Array] | Array | ArrayLike,
        t: float | ArrayLike | Array = 0.0,
    ) -> pd.DataFrame:
        """Calculate the fluxes at time point(s) t."""
        if isinstance(t, (int, float)):
            t = [t]  # type: ignore
        return pd.DataFrame(
            data=self.get_fluxes_dict(y=y, t=t), index=t, columns=self.get_rate_names()
        )

    def get_right_hand_side(
        self,
        y: dict[str, float] | dict[str, ArrayLike] | dict[str, Array] | Array | ArrayLike,
        t: float | ArrayLike | Array = 0.0,
        annotate_names: bool = True,
    ) -> dict[str, float]:
        """Calculate the right hand side of the ODE system."""
        fcd = self.get_full_concentration_dict(y=y, t=t)  # type: ignore
        fcd_array = [fcd[i] for i in self.get_compounds()]
        rhs = self._get_rhs(t=t, y=fcd_array)
        if annotate_names:
            eqs = [f"d{cpd}dt" for cpd in self.get_compounds()]
        else:
            eqs = self.get_compounds()
        return dict(zip(eqs, rhs))
