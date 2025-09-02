from __future__ import annotations

__all__ = [
    "StoichiometricMixin",
]

import warnings
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from typing_extensions import Self

from .basemodel import BaseModel
from .compoundmixin import CompoundMixin
from .utils import convert_id_to_sbml, warning_on_one_line

if TYPE_CHECKING:
    import libsbml

    from modelbase.typing import Array

warnings.formatwarning = warning_on_one_line  # type: ignore


class StoichiometricMixin(CompoundMixin, BaseModel):

    """Mixin for stoichiometries."""

    def __init__(
        self, rate_stoichiometries: dict[str, dict[str, float]] | None = None
    ) -> None:
        self.stoichiometries: dict[str, dict[str, float]] = {}
        self.stoichiometries_by_compounds: dict[str, dict[str, float]] = {}
        if rate_stoichiometries is not None:
            self.add_stoichiometries(rate_stoichiometries=rate_stoichiometries)

    ##########################################################################
    # Stoichiometries
    ##########################################################################

    def add_stoichiometry(self, rate_name: str, stoichiometry: dict[str, float]) -> Self:
        """Add the stoichiometry of a rate to the model.

        Examples
        --------
        add_stoichiometry(rate_name="v1", stoichiometry={"x": 1})

        """
        if rate_name in self.stoichiometries:
            warnings.warn(f"Overwriting stoichiometry for rate {rate_name}")
            self.remove_rate_stoichiometry(rate_name=rate_name)

        # Stoichiometries
        self.stoichiometries[rate_name] = stoichiometry

        # Stoichiometries by compounds
        for compound, factor in stoichiometry.items():
            self.stoichiometries_by_compounds.setdefault(compound, {})[rate_name] = factor
        return self

    def add_stoichiometry_by_compound(
        self, compound: str, stoichiometry: dict[str, float]
    ) -> Self:
        """Add the stoichiometry of compound to the model.

        Examples
        --------
        add_stoichiometry_by_compoundcompound="x", stoichiometry={"v1": 1})

        """
        if compound in self.stoichiometries_by_compounds:
            warnings.warn(f"Overwriting stoichiometry for compound {compound}")
            self.remove_compound_stoichiometry(compound=compound)

        self.stoichiometries_by_compounds[compound] = stoichiometry

        for rate, factor in stoichiometry.items():
            self.stoichiometries.setdefault(rate, {})[compound] = factor
        return self

    def add_stoichiometries(
        self, rate_stoichiometries: dict[str, dict[str, float]]
    ) -> Self:
        """Add the stoichiometry of multiple rates.

        Examples
        --------
        add_stoichiometries(
            rate_stoichiometries={
                "v1": {"x": -1, "y": 1},
                "v2": {"x": 1, "y": -1}
            }
        )

        """
        for rate_name, stoichiometry in rate_stoichiometries.items():
            self.add_stoichiometry(rate_name=rate_name, stoichiometry=stoichiometry)
        return self

    def update_stoichiometry(
        self, rate_name: str, stoichiometry: dict[str, float]
    ) -> Self:
        """Update stoichiometry of a rate"""
        if rate_name not in self.stoichiometries:
            warnings.warn("Rate not in stoichiometries!")
        else:
            self.remove_rate_stoichiometry(rate_name)
        self.add_stoichiometry(rate_name, stoichiometry)
        return self

    def update_stoichiometries(
        self, stoichiometries: dict[str, dict[str, float]]
    ) -> Self:
        """Update stoichiometries of multiple rates"""
        for rate_name, stoichiometry in stoichiometries.items():
            self.update_stoichiometry(rate_name, stoichiometry)
        return self

    def add_stoichiometries_by_compounds(
        self, compound_stoichiometries: dict[str, dict[str, float]]
    ) -> Self:
        """Add the stoichiometry of multiple compounds to the model.

        Examples
        --------
        add_stoichiometries_by_compounds(
            compound_stoichiometries={
                "x": {"v1": -1, "v2": 1},
                "y": {"v1": 1, "v2": -1}
            }
        )

        """
        for compound, stoichiometry in compound_stoichiometries.items():
            self.add_stoichiometry_by_compound(
                compound=compound, stoichiometry=stoichiometry
            )
        return self

    def remove_rate_stoichiometry(self, rate_name: str) -> Self:
        """Remove a rate stoichiometry from the model."""
        compounds = self.stoichiometries.pop(rate_name)
        for compound in compounds:
            del self.stoichiometries_by_compounds[compound][rate_name]
            if not bool(self.stoichiometries_by_compounds[compound]):
                del self.stoichiometries_by_compounds[compound]
        return self

    def remove_rate_stoichiometries(self, rate_names: list[str]) -> Self:
        """Remove multiple rate stoichiometries from the model."""
        for rate_name in rate_names:
            self.remove_rate_stoichiometry(rate_name=rate_name)
        return self

    def remove_compound_stoichiometry(self, compound: str) -> Self:
        """Remove stoichiometry of a compound."""
        rates = self.stoichiometries_by_compounds.pop(compound)
        for rate in rates:
            del self.stoichiometries[rate][compound]
            if not bool(self.stoichiometries[rate]):
                del self.stoichiometries[rate]
        return self

    def remove_compound_stoichiometries(self, compounds: list[str]) -> Self:
        """Remove stoichiometry of multiple compounds."""
        for compound in compounds:
            self.remove_compound_stoichiometry(compound=compound)
        return self

    def get_rate_stoichiometry(self, rate_name: str) -> dict[str, float]:
        """Get stoichiometry of a rate."""
        return dict(self.stoichiometries[rate_name])

    def get_compound_stoichiometry(self, compound: str) -> dict[str, float]:
        """Get stoichiometry of a compound."""
        return dict(self.stoichiometries_by_compounds[compound])

    def get_stoichiometries(self) -> dict[str, dict[str, float]]:
        """Return stoichiometries ordered by reactions."""
        return dict(self.stoichiometries)

    def get_stoichiometries_by_compounds(self) -> dict[str, dict[str, float]]:
        """Return stoichiometries ordered by compounds."""
        return dict(self.stoichiometries_by_compounds)

    def get_stoichiometric_matrix(self) -> Array:
        """Return the stoichiometric matrix."""
        compound_indexes = {v: k for k, v in enumerate(sorted(self.get_compounds()))}
        M = np.zeros(shape=[len(self.get_compounds()), len(self.stoichiometries)])
        for stoich_idx, rate_name in enumerate(sorted(self.stoichiometries)):
            cpd_stoich = self.stoichiometries[rate_name]
            for cpd, stoich in cpd_stoich.items():
                M[compound_indexes[cpd], stoich_idx] = stoich
        return M

    def get_stoichiometric_df(self) -> pd.DataFrame:
        """Return the stoichiometric matrix as a pandas DataFrame."""
        return pd.DataFrame(
            data=self.get_stoichiometric_matrix(),
            index=sorted(self.get_compounds()),
            columns=sorted(self.stoichiometries),
        )

    ##########################################################################
    # Source code functions
    ##########################################################################

    def _generate_stoichiometries_source_code(self) -> str:
        """Generate modelbase source code for stoichiometries.

        See Also
        --------
        generate_model_source_code

        """
        if len(self.stoichiometries) == 0:
            return ""
        return f"m.add_stoichiometries(rate_stoichiometries={self.stoichiometries!r})"

    ##########################################################################
    # SBML functions
    ##########################################################################

    def _create_sbml_stoichiometries(self, *, sbml_model: libsbml.Model) -> None:
        """Create the reactions for the sbml model.

        Parameters
        ----------
        sbml_model : libsbml.Model

        """
        for rate_id, stoichiometry in self.stoichiometries.items():
            rxn = sbml_model.createReaction()
            rxn.setId(convert_id_to_sbml(id_=rate_id, prefix="RXN"))

            for compound_id, factor in stoichiometry.items():
                if factor < 0:
                    sref = rxn.createReactant()
                else:
                    sref = rxn.createProduct()
                sref.setSpecies(convert_id_to_sbml(id_=compound_id, prefix="CPD"))
                sref.setStoichiometry(abs(factor))
                sref.setConstant(True)
