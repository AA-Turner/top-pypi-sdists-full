"""Molecular descriptors workflow."""

from ..solvent import Solvent
from ..types import UUID
from .workflow import MoleculeWorkflow

Descriptors = dict[str, dict[str, float] | tuple[float | None, ...] | float]


class DescriptorsWorkflow(MoleculeWorkflow):
    """A workflow for calculating molecular descriptors.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (not used)

        do_optimization: optimize with GFN2-xTB before calculating descriptors when true
        solvent: solvent to use for optimization and descriptor calculation
        optimization: UUID of optimization
        descriptors: calculated descriptors
    """

    do_optimization: bool = True
    solvent: Solvent | None = None

    optimization: UUID | None = None
    descriptors: Descriptors | None = None
