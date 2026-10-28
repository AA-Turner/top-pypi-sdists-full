"""Define membrane permeability workflows."""

from typing import Annotated, Self

from pydantic import AfterValidator, model_validator

from ..base import LowercaseStrEnum, round_float
from ..molecule import Molecule
from .workflow import MoleculeWorkflow, SMILESWorkflow


class MembranePermeabilityMethod(LowercaseStrEnum):
    """Select a membrane permeability prediction method."""

    CHEMPROP_OHLSSON2025 = "chemprop_ohlsson2025"
    PYPERMM = "pypermm"


class MembranePermeabilityWorkflow(SMILESWorkflow, MoleculeWorkflow):
    """Membrane permeability prediction workflow.

    Attributes:
        initial_smiles: SMILES string of the molecule
        initial_molecule: molecule of interest

    Inputs:

        membrane_permeability_method: model used to predict membrane permeability

        caco_2_P_app: base-10 logarithm of Caco-2 apparent permeability, in cm/s
        blm_P_app: base-10 logarithm of bilayer-lipid-membrane apparent permeability, in cm/s
        pampa_P_app: base-10 logarithm of PAMPA apparent permeability, in cm/s
        plasma_P_app: base-10 logarithm of plasma-membrane apparent permeability, in cm/s
        bbb_P_app: base-10 logarithm of blood-brain-barrier apparent permeability, in cm/s
        caco_2_logP: base-10 logarithm of Caco-2 intrinsic permeability, in cm/s
        blm_logP: base-10 logarithm of bilayer-lipid-membrane intrinsic permeability, in cm/s
        pampa_logP: base-10 logarithm of PAMPA intrinsic permeability, in cm/s
        plasma_logP: base-10 logarithm of plasma-membrane intrinsic permeability, in cm/s
        bbb_logP: base-10 logarithm of blood-brain-barrier intrinsic permeability, in cm/s
        energy_profile: how the energy of the compound is predicted to change as it passes through a membrane.
            the first value is the membrane profile, in Å, the second is the energy, in kcal/mol
    """

    initial_smiles: str = ""
    initial_molecule: Molecule | None = None

    membrane_permeability_method: MembranePermeabilityMethod = MembranePermeabilityMethod.CHEMPROP_OHLSSON2025

    caco_2_P_app: Annotated[float, AfterValidator(round_float(3))] | None = None
    blm_P_app: Annotated[float, AfterValidator(round_float(3))] | None = None
    pampa_P_app: Annotated[float, AfterValidator(round_float(3))] | None = None
    plasma_P_app: Annotated[float, AfterValidator(round_float(3))] | None = None
    bbb_P_app: Annotated[float, AfterValidator(round_float(3))] | None = None

    caco_2_logP: Annotated[float, AfterValidator(round_float(3))] | None = None
    blm_logP: Annotated[float, AfterValidator(round_float(3))] | None = None
    pampa_logP: Annotated[float, AfterValidator(round_float(3))] | None = None
    plasma_logP: Annotated[float, AfterValidator(round_float(3))] | None = None
    bbb_logP: Annotated[float, AfterValidator(round_float(3))] | None = None

    energy_profile: list[
        tuple[
            Annotated[float, AfterValidator(round_float(3))],
            Annotated[float, AfterValidator(round_float(3))],
        ]
    ] = []

    @model_validator(mode="after")
    def validate_mol_input(self) -> Self:
        """Ensure that only one of initial_molecule or initial_smiles is set."""
        if not (bool(self.initial_smiles) ^ bool(self.initial_molecule)):
            raise ValueError("Can only set one of initial_molecule and initial_smiles")

        if self.initial_molecule:
            assert self.membrane_permeability_method == MembranePermeabilityMethod.PYPERMM
        elif self.initial_smiles:
            assert self.membrane_permeability_method == MembranePermeabilityMethod.CHEMPROP_OHLSSON2025

        return self
