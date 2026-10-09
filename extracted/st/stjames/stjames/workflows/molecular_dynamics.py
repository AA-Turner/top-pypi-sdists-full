"""Molecular dynamics workflow."""

from typing import Self

from pydantic import PositiveFloat, PositiveInt, computed_field, model_validator

from ..base import Base, LowercaseStrEnum
from ..constraint import PairwiseHarmonicConstraint, SphericalHarmonicConstraint
from ..engine import Engine
from ..settings import Settings
from ..types import UUID
from .workflow import MoleculeWorkflow


class MolecularDynamicsInitialization(LowercaseStrEnum):
    """Initialization method for molecular dynamics."""

    RANDOM = "random"
    QUASICLASSICAL = "quasiclassical"
    READ = "read"


class ThermodynamicEnsemble(LowercaseStrEnum):
    """Thermodynamic ensemble for molecular dynamics."""

    NPT = "npt"
    NVT = "nvt"
    NVE = "nve"


class Frame(Base):
    """A frame in a molecular dynamics simulation.

    Attributes:
        index: frame number within the simulation
        calculation_uuid: identifier of the calculation for this frame
        pressure: frame pressure
        temperature: frame temperature
        volume: frame volume
        potential_energy: potential energy, in kcal/mol
        kinetic_energy: kinetic energy, in kcal/mol
    """

    index: int  # what number frame this is within the MD simulation

    calculation_uuid: UUID | None = None  # UUID of calculation

    pressure: float
    temperature: float
    volume: float
    potential_energy: float  # kcal/mol
    kinetic_energy: float  # kcal/mol

    @computed_field
    @property
    def energy(self) -> float:
        """Compute total frame energy from potential and kinetic energies.

        Returns:
            total energy in kcal/mol
        """
        return self.potential_energy + self.kinetic_energy


class MolecularDynamicsSettings(Base):
    """Settings for a molecular dynamics simulation.

    Attributes:
        ensemble: thermodynamic ensemble to simulate
        initialization: method used to initialize velocities
        timestep: integration time step, in fs
        num_steps: number of integration steps
        save_interval: integration steps between saved frames
        confining_constraint: spherical constraint applied to the system
        temperature: simulation temperature, in K
        pressure: simulation pressure, in atm
        langevin_thermostat_timescale: Langevin thermostat time scale, in fs
        berendsen_barostat_timescale: Berendsen barostat time scale, in fs
        constraints: additional geometric constraints
    """

    ensemble: ThermodynamicEnsemble = ThermodynamicEnsemble.NVT
    initialization: MolecularDynamicsInitialization = MolecularDynamicsInitialization.RANDOM

    timestep: PositiveFloat = 1.0  # fs
    num_steps: PositiveInt = 500
    save_interval: PositiveInt = 10

    confining_constraint: SphericalHarmonicConstraint | None = None

    temperature: PositiveFloat = 300  # K
    pressure: PositiveFloat | None = None  # atm

    langevin_thermostat_timescale: PositiveFloat = 100  # fs
    berendsen_barostat_timescale: PositiveFloat = 1000  # fs

    constraints: list[PairwiseHarmonicConstraint] = []

    @model_validator(mode="after")
    def validate_ensemble_settings(self) -> Self:
        """Check that NVT ensemble always has temperature defined, and that NPT has temp and pressure defined."""
        if self.ensemble == ThermodynamicEnsemble.NVT and self.temperature is None:
            raise ValueError("NVT ensemble must have a temperature defined")
        elif self.ensemble == ThermodynamicEnsemble.NPT and (self.temperature is None or self.pressure is None):
            raise ValueError("NPT ensemble must have both temperature and pressure defined")
        return self


class MolecularDynamicsWorkflow(MoleculeWorkflow):
    """Workflow for running a molecular dynamics simulation.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (currently unused)

        settings: settings for the molecular dynamics simulation
        calc_settings: settings for the gradient calculation
        calc_engine: engine to use for the gradient calculation [uses calc_settings.method.default_engine() if not set]

        frames: Frames from the MD
    """

    settings: MolecularDynamicsSettings
    calc_settings: Settings

    # DEPRECATED - will remove later
    calc_engine: Engine = None  # ty: ignore[invalid-assignment]

    frames: list[Frame] = []

    @model_validator(mode="after")
    def validate_calc_engine(self) -> Self:
        """Ensure that the calc_engine is set."""
        self.calc_engine = self.calc_engine or self.calc_settings.engine

        return self
