"""logP prediction workflow."""

from typing import Annotated, Self

from pydantic import AfterValidator, model_validator

from ..base import LowercaseStrEnum, round_float
from ..molecule import Molecule
from .workflow import SMILESWorkflow


class LogPMethod(LowercaseStrEnum):
    """Method used for logP prediction.

    CHEMPROP_SANGSTER2026: chemprop v2 D-MPNN trained on experimental logP (octanol/water
        partition coefficient) from the Sangster dataset
    CRIPPEN: RDKit implementation of the Wildman-Crippen atom-contribution model
    COSMORS: COSMO-RS activity coefficients
    """

    CHEMPROP_SANGSTER2026 = "chemprop_sangster2026"
    CRIPPEN = "crippen"
    COSMORS = "cosmors"


class LogPWorkflow(SMILESWorkflow):
    """logP prediction workflow.

    Attributes:
        initial_smiles: SMILES string of the molecule
        initial_molecule: nonperiodic 3D structure of the molecule, supported by COSMO-RS
        logp_method: model used for logP prediction
        logp: predicted logP value
    """

    initial_smiles: str = ""
    initial_molecule: Molecule | None = None
    logp_method: LogPMethod = LogPMethod.CHEMPROP_SANGSTER2026

    logp: Annotated[float, AfterValidator(round_float(3))] | None = None

    @model_validator(mode="after")
    def validate_mol_input(self) -> Self:
        """Require one molecular input compatible with the selected method."""
        if bool(self.initial_smiles) == (self.initial_molecule is not None):
            raise ValueError("Provide exactly one of initial_smiles and initial_molecule")

        if self.initial_molecule is not None:
            if self.logp_method != LogPMethod.COSMORS:
                raise ValueError("initial_molecule is only supported by the COSMO-RS logP method")
            if self.initial_molecule.cell is not None:
                raise ValueError("initial_molecule must be a nonperiodic structure")

        return self
