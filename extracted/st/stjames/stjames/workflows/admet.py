"""ADME-Tox property prediction workflow."""

import warnings
from typing import Self

from pydantic import model_validator

from ..molecule import Molecule
from .workflow import MoleculeWorkflow, SMILESWorkflow


class ADMETWorkflow(SMILESWorkflow, MoleculeWorkflow):
    """A workflow for predicting ADME-Tox properties.

    Attributes:
        initial_smiles: SMILES string of molecule (mutually exclusive with initial_molecule)
        initial_molecule: Molecule of interest (deprecated)
        mode: Mode for workflow (currently unused)

        properties: predicted properties
    """

    initial_smiles: str = ""
    initial_molecule: Molecule | None = None  # Deprecated
    properties: dict[str, float | int] | None = None

    @model_validator(mode="after")
    def validate_mol_input(self) -> Self:
        """Ensure that only one of initial_molecule or initial_smiles is set."""
        if not (bool(self.initial_smiles) ^ bool(self.initial_molecule)):
            raise ValueError("Can only set one of initial_molecule and initial_smiles")

        if self.initial_molecule is not None:
            warnings.warn(DeprecationWarning("initial_molecule is deprecated. Use initial_smiles instead."))  # noqa: B028

        return self
