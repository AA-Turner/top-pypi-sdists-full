"""Batched small-molecule force-field parameterization workflow."""

from typing import Literal, Self

from pydantic import Field, model_validator

from ..charge import ChargeMethod
from ..forcefield import LigandParameterizationResult
from ..method import Method
from ..molecule import Molecule
from .workflow import Workflow


class LigandParameterizationWorkflow(Workflow):
    """Parameterize ligands independently in one batched request.

    :param ligands: non-empty ordered list of molecules
    :param forcefield: force field used for parameterization
    :param charge_method: method for computing partial charges
    :param results: parameterization outcomes in input order
    """

    ligands: list[Molecule]
    forcefield: Literal[Method.MANGO_1_0_0] = Method.MANGO_1_0_0
    charge_method: ChargeMethod = ChargeMethod.NAGL
    results: list[LigandParameterizationResult] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_ligands_and_results(self) -> Self:
        """Validate a non-empty input and parallel result list."""
        if not self.ligands:
            raise ValueError("ligands must contain at least one molecule")
        if len(self.results) > len(self.ligands):
            raise ValueError("results cannot contain more entries than ligands")
        return self
