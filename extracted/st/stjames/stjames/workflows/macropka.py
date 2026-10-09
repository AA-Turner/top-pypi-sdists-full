"""pKa workflow."""

from typing import Annotated, Self

from pydantic import AfterValidator, model_validator

from ..base import Base, LowercaseStrEnum, round_float, round_optional_float
from ..types import round_list
from .workflow import SMILESWorkflow


class MacropKaMicrostate(Base):
    """A microstate for pKa calculations.

    Attributes:
        smiles: SMILES string for this conformer
        energy: free energy of this conformer
        charge: total charge
    """

    smiles: str
    energy: Annotated[float, AfterValidator(round_float(3))]  # free energy
    charge: int


class MacropKaValue(Base):
    """Represents a change in pKa.

    Attributes:
        initial_charge: charge of initial state
        final_charge: charge of final state
        pKa: pKa for the transition
    """

    initial_charge: int
    final_charge: int
    pKa: Annotated[float, AfterValidator(round_float(3))]


class MacroscopicpKaMethod(LowercaseStrEnum):
    """Select a method for macroscopic pKa prediction."""

    STARLING = "starling"
    STARLING_II = "starling_ii"


class MacropKaWorkflow(SMILESWorkflow):
    """Workflow for calculating pKa.

    Attributes:
        initial_smiles:

        method: how macroscopic pKa values should be computed
        min_pH: for precomputed microstate weights, logD, etc
        max_pH: for precomputed microstate weights, logD, etc
        max_charge: max charge to consider for microstates
        min_charge: min charge to consider for microstates
        compute_aqueous_solubility: compute aqueous solubility when true
        compute_solvation_energy: run a csearch and compute solvation energy (for Kpuu) when true

        microstates: microstates
        pKa_values: macroscopic pKa values
        isoelectric_point: isoelectric point (in pH units)
        solvation_energy: solvation energy, in kcal/mol
        microstate_weights_by_pH: % of different microstates by pH
        logD_by_pH: distribution constant (water/octanol) by pH
        aqueous_solubility_by_pH: solubility of compound in water, by pH, in log(S)/L
        kpuu_probability: probability that Kpuu >= 0.3 (Schrödinger-determined threshold)
    """

    method: MacroscopicpKaMethod = MacroscopicpKaMethod.STARLING

    min_pH: Annotated[float, AfterValidator(round_float(3))] = 0.0
    max_pH: Annotated[float, AfterValidator(round_float(3))] = 14.0
    max_charge: int = 2
    min_charge: int = -2
    compute_aqueous_solubility: bool = False
    compute_solvation_energy: bool = True

    microstates: list[MacropKaMicrostate] = []
    pKa_values: list[MacropKaValue] = []
    isoelectric_point: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    solvation_energy: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    kpuu_probability: Annotated[float | None, AfterValidator(round_optional_float(3))] = None

    microstate_weights_by_pH: list[
        tuple[
            Annotated[float, AfterValidator(round_float(3))],
            Annotated[list[float], AfterValidator(round_list(6))],
        ]
    ] = []

    logD_by_pH: list[
        tuple[
            Annotated[float, AfterValidator(round_float(3))],
            Annotated[float, AfterValidator(round_float(3))],
        ]
    ] = []

    aqueous_solubility_by_pH: list[
        tuple[
            Annotated[float, AfterValidator(round_float(3))],
            Annotated[float, AfterValidator(round_float(3))],
        ]
    ] = []

    @model_validator(mode="after")
    def check_weights(self) -> Self:
        """Match each microstate weight list to the microstates.

        Returns:
            validated workflow

        Raises:
            ValueError: weight count differs from microstate count
        """
        for _, weights in self.microstate_weights_by_pH:
            if len(weights) != len(self.microstates):
                raise ValueError("Length of microstate weights doesn't match!")

        return self

    @model_validator(mode="after")
    def check_minmax_charges(self) -> Self:
        """Require the minimum charge to be below the maximum.

        Returns:
            validated workflow

        Raises:
            ValueError: charge bounds are reversed or equal
        """
        if self.min_charge >= self.max_charge:
            raise ValueError("Incoherent min/max charge specification")

        return self
