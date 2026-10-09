"""Ion mobility workflow."""

from typing import Annotated, Self

from pydantic import AfterValidator, computed_field, model_validator

from ..base import Base, round_optional_float
from ..data import ELEMENT_SYMBOL
from ..types import UUID, round_list
from .workflow import MoleculeWorkflow


class IonMobilityForcefieldElement(Base):
    """A single atom specification for the ion-mobility forcefield.

    Attributes:
        name: name of element (e.g. "Hydrogen")
        atomic_number: element's atomic number
        mass: mass of element, in Daltons (e.g. 1.00794)
        sigma: sigma Lennard-Jones parameter, in Å
        epsilon: epsilon Lennard-Jones parameter, in kcal/mol
    """

    name: str
    atomic_number: int
    mass: float
    sigma: float
    epsilon: float

    @computed_field
    @property
    def symbol(self) -> str:
        """Return the element symbol corresponding to atomic_number."""
        return ELEMENT_SYMBOL[self.atomic_number]


class IonMobilityWorkflow(MoleculeWorkflow):
    """Workflow for calculating ion-mobility collision cross sections (CCS).

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (currently unused)

        protonate: automatically protonate molecule
        temperature: bath-gas temperature for the CCS calculation, in Kelvin (default 300); does not set conformer weights
        do_csearch: perform conformational search when true
        do_optimization: perform optimization when true
        forcefield: forcefield for atom–gas interactions; if None, default forcefield used

        conformers: UUIDs of conformers
        conformer_ccs: collision cross section per conformer, in Å**2
        conformer_ccs_stdev: uncertainty in same
        boltzmann_weights: conformer Boltzmann weights at 298.15 K, normalized over successful CCS results when the workflow completes
        average_ccs: Boltzmann-weighted CCS for the ensemble, in Å**2
        average_ccs_stdev: uncertainty in same
    """

    protonate: bool = False
    temperature: float = 300
    do_csearch: bool = True
    do_optimization: bool = True

    forcefield: list[IonMobilityForcefieldElement] | None = None

    conformers: list[UUID] = []

    conformer_ccs: Annotated[list[float], AfterValidator(round_list(3))] = []
    conformer_ccs_stdev: Annotated[list[float], AfterValidator(round_list(3))] = []
    boltzmann_weights: Annotated[list[float], AfterValidator(round_list(3))] = []

    average_ccs: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    average_ccs_stdev: Annotated[float | None, AfterValidator(round_optional_float(3))] = None

    @model_validator(mode="after")
    def check_supported_atoms(self) -> Self:
        """Validate that user-supplied forcefields have correct atoms."""
        if self.forcefield is not None:
            supported_atoms = {e.atomic_number for e in self.forcefield}
            if not all(z in supported_atoms for z in self.initial_molecule.atomic_numbers):
                raise ValueError("Provided forcefield does not support all elements in input structure!")

        return self
