"""Surface energies of a crystal's symmetry-distinct low-index faces."""

from typing import Annotated, Self, TypeAlias

from pydantic import AfterValidator, PositiveInt, field_validator, model_validator

from ..base import Base, round_float, round_optional_float
from ..settings import Settings
from ..types import UUID
from .workflow import MoleculeWorkflow

MillerIndices: TypeAlias = tuple[int, int, int]


class FacetSurfaceEnergy(Base):
    """
    Surface energy of one symmetry-distinct crystal face.

    :param miller_indices: exposed face
    :param surface_energy: surface energy, in J/m²
    :param termination: fractional cut offset used
    :param equivalents: every symmetry-equivalent face sharing this energy, including this one
    :param area_fraction: share of the equilibrium crystal's surface, 0 when cut away entirely, None until the scan completes or when no shape exists
    :param eps_bulk: bulk reference energy per atom, in Hartree
    :param slab_calculation_uuid: UUID of the slab calculation
    :param bulk_reference_calculation_uuid: UUID of the oriented bulk reference calculation
    """

    miller_indices: MillerIndices
    surface_energy: Annotated[float, AfterValidator(round_float(4))]
    termination: Annotated[float, AfterValidator(round_float(4))]
    equivalents: list[MillerIndices]
    eps_bulk: Annotated[float, AfterValidator(round_float(4))]
    area_fraction: Annotated[float | None, AfterValidator(round_optional_float(4))] = None

    slab_calculation_uuid: UUID | None = None
    bulk_reference_calculation_uuid: UUID | None = None

    @property
    def face_multiplicity(self) -> int:
        """Number of symmetry-equivalent faces sharing this surface energy."""
        return len(self.equivalents)


class SurfaceEnergyResult(Base):
    """
    Ranked surface energies and equilibrium shape of one crystal.

    :param facets: computed faces, most stable first, filled in as the scan runs
    :param skipped_facets: (face, why no surface energy is available) pairs
    :param bulk_relaxation_uuid: UUID of the one bulk relaxation every face is cut from
    :param space_group: space group of the relaxed bulk structure
    :param mean_surface_energy: γ̄ = Σ area_fraction_i · surface_energy_i, None if any area_fraction is missing
    :param surface_energy_anisotropy: α_γ = sqrt(Σ area_fraction_i · (surface_energy_i − γ̄)²) / γ̄, None if any area_fraction is missing
    :param shape_factor: η = volume / (surface area · effective radius) of the Wulff shape, None until constructed
    """

    facets: list[FacetSurfaceEnergy] = []
    skipped_facets: list[tuple[MillerIndices, str]] = []
    bulk_relaxation_uuid: UUID | None = None
    space_group: str | int | None = None
    mean_surface_energy: Annotated[float | None, AfterValidator(round_optional_float(4))] = None
    surface_energy_anisotropy: Annotated[float | None, AfterValidator(round_optional_float(4))] = None
    shape_factor: Annotated[float | None, AfterValidator(round_optional_float(4))] = None

    @property
    def most_stable_facet(self) -> FacetSurfaceEnergy | None:
        """Face with the lowest surface energy, None before any face is computed."""
        return self.facets[0] if self.facets else None


class SurfaceEnergyWorkflow(MoleculeWorkflow):
    """
    Surface-energy scan over a crystal's symmetry-distinct low-index faces.

    Inherited:
    :param initial_molecule: crystal of interest
    :param mode: Mode for workflow

    New:
    :param settings: calculation settings for the bulk, slab, and reference calculations
    :param max_miller_index: largest absolute value of any single Miller index
    :param results: ranked surface energies, filled in as the scan runs
    """

    settings: Settings
    max_miller_index: PositiveInt = 1

    results: SurfaceEnergyResult | None = None

    @model_validator(mode="after")
    def validate_fully_periodic(self) -> Self:
        """Require a crystal periodic in all three dimensions."""
        if (cell := self.initial_molecule.cell) is None:
            raise ValueError("SurfaceEnergyWorkflow requires a periodic initial_molecule (cell is None).")
        if not all(cell.is_periodic):
            raise ValueError(f"SurfaceEnergyWorkflow requires a fully periodic crystal, got is_periodic={cell.is_periodic}.")
        return self

    @field_validator("settings", mode="after")
    @classmethod
    def validate_settings(cls, settings: Settings) -> Settings:
        """Reject settings resolved per structure or incompatible with relaxed minima."""
        if (pbc := settings.pbc_dft_settings) is not None and pbc.kpoints is not None:
            raise ValueError(f"SurfaceEnergyWorkflow resolves k-points per structure, got pbc_dft_settings.kpoints={pbc.kpoints}.")

        if settings.opt_settings.constraints:
            raise ValueError("SurfaceEnergyWorkflow does not support constraints, slabs are re-cut from the relaxed bulk.")

        if settings.opt_settings.transition_state:
            raise ValueError("SurfaceEnergyWorkflow requires relaxed minima, got opt_settings.transition_state=True.")

        if not settings.opt_settings.optimize_cell:
            raise ValueError("SurfaceEnergyWorkflow requires optimize_cell=True, the bulk is relaxed before any face is cut.")

        return settings
