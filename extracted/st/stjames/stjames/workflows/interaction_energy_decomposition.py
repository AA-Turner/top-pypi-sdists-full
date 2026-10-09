"""Define interaction energy decomposition workflows."""

from typing import Annotated, Literal

from pydantic import AfterValidator, PositiveInt

from ..base import Base, LowercaseStrEnum, round_float
from ..basis_set import BasisSet
from .workflow import MoleculeWorkflow


class EnergyDecompositionMethod(LowercaseStrEnum):
    """Select a method for interaction energy decomposition."""

    SAPT0 = "sapt0"


class EnergyDecompositionSettings(Base):
    """How energy-decomposition calculations should be performed.

    Attributes:
        method: which energy decomposition method
        basis_set: which basis set to employ
    """

    method: EnergyDecompositionMethod = EnergyDecompositionMethod.SAPT0
    basis_set: BasisSet = BasisSet(name="jun-cc-pVDZ")

    def __str__(self) -> str:
        """Format the energy decomposition method and basis set.

        Examples:
        >>> str(EnergyDecompositionSettings())
        'SAPT0(jun-cc-pVDZ)'
        """
        return f"{self.method.value.upper()}({self.basis_set.name})"


class SAPT0Result(Base):
    """Stores the result of a SAPT0 calculation.

    Attributes:
        total_interaction_energy: total interaction energy, in kcal/mol
        electrostatic_interaction_energy: electrostatic interaction energy, in kcal/mol
        exchange_interaction_energy: exchange interaction energy, in kcal/mol
        dispersion_interaction_energy: dispersion interaction energy, in kcal/mol
        induction_interaction_energy: induction interaction energy, in kcal/mol
        result_type: to disambiguate from possible future alternate returns
    """

    total_interaction_energy: Annotated[float, AfterValidator(round_float(3))]
    electrostatic_interaction_energy: Annotated[float, AfterValidator(round_float(3))]
    exchange_interaction_energy: Annotated[float, AfterValidator(round_float(3))]
    dispersion_interaction_energy: Annotated[float, AfterValidator(round_float(3))]
    induction_interaction_energy: Annotated[float, AfterValidator(round_float(3))]

    result_type: Literal["sapt0"] = "sapt0"


class InteractionEnergyDecompositionWorkflow(MoleculeWorkflow):
    """Performs an interaction-energy-decomposition calculation.

    Attributes:
        initial_molecule: Molecule in question

        fragment1_indices: which atoms go to fragment #1, fragment #2 takes the rest (1-indexed)
        energy_decomposition_settings: settings for SAPT calculations

        energy_decomposition_result: results from the energy decomposition
    """

    fragment1_indices: list[PositiveInt]

    energy_decomposition_settings: EnergyDecompositionSettings = EnergyDecompositionSettings()

    energy_decomposition_result: SAPT0Result | None = None
