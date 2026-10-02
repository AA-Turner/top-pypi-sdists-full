"""Harmonic finite-displacement phonon workflow."""

from typing import Annotated, Any, Self

from pydantic import AfterValidator, PositiveInt, field_validator, model_validator

from ..base import Base, round_float
from ..mode import Mode
from ..settings import Settings
from ..types import (
    UUID,
    Vector3DPerAtom,
    round_list,
    round_list_of_lists,
    round_list_of_str_float_pairs,
    round_vector3d_per_atom,
)
from .workflow import MoleculeWorkflow


class PhononBandStructure(Base):
    """
    Phonon frequencies along a high-symmetry q-path.

    :param qpoint_distances: cumulative path coordinate, length n_qpoints, in 2π/Å
    :param frequencies: frequencies, (n_qpoints, 3N), in cm⁻¹
    :param high_symmetry_points: (label, distance) pairs, e.g. [("Γ", 0.0), ("X", 1.23)]
    """

    qpoint_distances: Annotated[list[float], AfterValidator(round_list(6))]
    frequencies: Annotated[list[list[float]], AfterValidator(round_list_of_lists(3))]
    high_symmetry_points: Annotated[list[tuple[str, float]], AfterValidator(round_list_of_str_float_pairs(6))]


class PhononDensityOfStates(Base):
    """
    Per-atom projected phonon density of states, normalized per cm⁻¹.

    :param frequency_points: frequency grid, length n_points, in cm⁻¹
    :param projected: per-primitive-atom partial DOS, (N, n_points)
    :param projection_labels: atomic number for each row of projected
    """

    frequency_points: Annotated[list[float], AfterValidator(round_list(3))]
    projected: Annotated[list[list[float]], AfterValidator(round_list_of_lists(6))]
    projection_labels: list[int]

    @property
    def total(self) -> list[float]:
        """Total DOS in states per cm⁻¹, summed over atoms; length n_points."""
        return [sum(point) for point in zip(*self.projected, strict=True)]


class PhononThermalProperties(Base):
    """
    Harmonic thermodynamic functions versus temperature, per primitive cell.

    :param temperatures: temperatures, in K
    :param free_energy: Helmholtz free energy, in Hartree
    :param entropy: entropy, in Hartree/K
    :param heat_capacity: constant-volume heat capacity, in Hartree/K
    :param zero_point_energy: zero-point vibrational energy, in Hartree
    """

    temperatures: Annotated[list[float], AfterValidator(round_list(1))]
    free_energy: Annotated[list[float], AfterValidator(round_list(6))]
    entropy: Annotated[list[float], AfterValidator(round_list(9))]
    heat_capacity: Annotated[list[float], AfterValidator(round_list(9))]
    zero_point_energy: Annotated[float, AfterValidator(round_float(6))]

    @property
    def internal_energy(self) -> list[float]:
        """Internal energy per primitive cell in Hartree, U = F + T·S."""
        return [f + t * s for f, t, s in zip(self.free_energy, self.temperatures, self.entropy, strict=True)]


class ZoneCenterMode(Base):
    """
    Single Γ-point (q=0) phonon mode.

    :param frequency: frequency, negative for imaginary, in cm⁻¹
    :param symmetry_label: Mulliken irreducible-representation label, None if unassigned
    :param electric_dipole_allowed: electric-dipole (IR) allowed by symmetry, None if unassigned
    :param electric_dipole_dipole_polarizability_allowed: electric-dipole–dipole-polarizability (Raman) allowed by symmetry, None if unassigned
    :param displacements: per-atom displacement pattern, (N, 3)
    """

    frequency: Annotated[float, AfterValidator(round_float(3))]
    symmetry_label: str | None = None
    electric_dipole_allowed: bool | None = None
    electric_dipole_dipole_polarizability_allowed: bool | None = None
    displacements: Annotated[Vector3DPerAtom, AfterValidator(round_vector3d_per_atom(6))]


class ZoneCenterModes(Base):
    """
    Γ-point modes with symmetry labels and IR/Raman selection rules.

    :param point_group: Schoenflies symbol of the crystal point group at Γ
    :param modes: 3N zone-center modes
    """

    point_group: str
    modes: list[ZoneCenterMode]


class PhononResult(Base):
    """
    Harmonic phonon properties from a finite-displacement run.

    :param band_structure: frequencies along the high-symmetry q-path
    :param density_of_states: per-atom projected phonon DOS
    :param thermal_properties: free energy, entropy, and heat capacity vs T
    :param zone_center_modes: Γ modes with symmetry labels and IR/Raman activity
    :param min_frequency: minimum stability-mesh frequency, in cm⁻¹
    :param imaginary_fraction: fraction of stability-mesh frequencies below -1 cm⁻¹
    """

    band_structure: PhononBandStructure
    density_of_states: PhononDensityOfStates
    thermal_properties: PhononThermalProperties
    zone_center_modes: ZoneCenterModes

    min_frequency: Annotated[float, AfterValidator(round_float(3))]
    imaginary_fraction: Annotated[float, AfterValidator(round_float(3))]


class PhononSettings(Base):
    """
    Configuration for a finite-displacement phonon workflow.

    :param settings: calculation settings for displaced-supercell gradients and the pre-optimization
    :param supercell: diagonal supercell expansion
    """

    settings: Settings
    supercell: tuple[PositiveInt, PositiveInt, PositiveInt] = (2, 2, 2)

    @model_validator(mode="before")
    @classmethod
    def default_mode_careful(cls, values: Any) -> Any:
        """Default an unset or Auto calculation mode to Careful."""
        if not isinstance(values, dict):
            return values

        settings = values.get("settings")
        if not isinstance(settings, dict) or Mode(settings.get("mode") or Mode.AUTO) is not Mode.AUTO:
            return values

        return values | {"settings": settings | {"mode": Mode.CAREFUL}}

    @field_validator("settings", mode="after")
    @classmethod
    def validate_settings(cls, settings: Settings) -> Settings:
        """Validate the calculation settings."""
        if settings.opt_settings.constraints:
            raise ValueError("PhononWorkflow does not support constraints")

        if settings.opt_settings.transition_state:
            raise ValueError("PhononWorkflow does not support transition state optimizations")

        if not settings.opt_settings.optimize_cell:
            raise ValueError("PhononWorkflow requires optimize_cell=True")

        return settings


class PhononWorkflow(MoleculeWorkflow):
    """
    Harmonic finite-displacement phonon workflow.

    Inherited:
    :param initial_molecule: Molecule of interest
    :param mode: Mode for workflow (currently unused)

    New:
    :param phonon_settings: calculation and supercell settings
    :param optimization_uuid: UUID of the pre-optimization calculation
    :param results: derived phonon properties, None until the phonon stage completes
    """

    phonon_settings: PhononSettings

    optimization_uuid: UUID | None = None
    results: PhononResult | None = None

    @model_validator(mode="after")
    def validate_periodic(self) -> Self:
        """Require a periodic cell."""
        if self.initial_molecule.cell is None:
            raise ValueError("PhononWorkflow requires a periodic initial_molecule (cell is None).")
        return self
