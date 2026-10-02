"""Covalent inhibitor reactivity workflow, via ML/MM umbrella sampling."""

from typing import Annotated, Literal

from pydantic import AfterValidator, Field, NonNegativeFloat, NonNegativeInt, PositiveFloat, computed_field

from ..base import Base, round_float, round_optional_float
from ..engine import Engine
from ..method import Method
from ..molecule import Molecule
from ..settings import Settings
from ..types import round_list
from .protein_md import ProteinMDSettingsMixin
from .workflow import ProteinStructureWorkflow

OverlapRow = Annotated[list[NonNegativeFloat], AfterValidator(round_list(4))]
"""One row of the MBAR overlap matrix, each entry a fraction of a window's samples."""

DEFAULT_WINDOW_CENTERS = [
    1.8, 1.9, 2.0, 2.1, 2.2,
    2.3, 2.35, 2.4, 2.45, 2.5, 2.55, 2.6, 2.65, 2.7, 2.75, 2.8,
    2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0,
]  # fmt: skip


class UmbrellaSamplingScanSettings(ProteinMDSettingsMixin):
    """
    Settings for a covalent inhibitor scan by umbrella sampling.

    Inherited:
    :param equilibration_time_ns: how long to equilibrate trajectories for, in ns
    :param simulation_time_ns: how long to run trajectories for, in ns
    :param timestep_fs: timestep, in femtoseconds
    :param hydrogen_mass: mass of hydrogen atoms, in amu
    :param constrain_hydrogens: whether or not to use SHAKE to freeze bonds to hydrogen

    New:
    :param settings_type: discriminator, so other sampling methods can be added later
    :param window_centers: bias centers along the reactive bond, monotonic, seeded from
        the first, in Å
    :param force_constant: umbrella harmonic force constant, in kcal/mol/Å²
    :param protein_restraint_cutoff: distance from the ligand beyond which backbone
        Cα atoms are harmonically restrained, in Å; `None` disables restraints
    :param protein_restraint_constant: Cα restraint force constant, in kcal/mol/Å²
    :param calc_settings: settings for the ML subengine on the model region
    """

    settings_type: Literal["umbrella_sampling"] = "umbrella_sampling"

    equilibration_time_ns: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 0.02
    simulation_time_ns: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 0.05

    timestep_fs: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 2.0
    hydrogen_mass: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 4.0
    constrain_hydrogens: bool = False

    window_centers: Annotated[list[PositiveFloat], Field(min_length=1)] = DEFAULT_WINDOW_CENTERS
    force_constant: PositiveFloat = 30.0

    protein_restraint_cutoff: Annotated[PositiveFloat, AfterValidator(round_float(3))] | None = 10.0
    protein_restraint_constant: Annotated[PositiveFloat, AfterValidator(round_float(3))] = 100.0

    calc_settings: Settings = Settings(method=Method.ORB_V3_CONSERVATIVE_OMOL, engine=Engine.ORB)


class UmbrellaSamplingConvergence(Base):
    """
    Diagnostics saying whether a profile can be trusted.

    :param overlap_matrix: MBAR overlap between windows; low overlap between neighbours
        means the profile should not be trusted
    :param round_trips: replicas that traversed the whole coordinate and returned
    :param worst_pair_acceptance: lowest exchange acceptance over neighbouring pairs
    """

    overlap_matrix: list[OverlapRow] = []
    round_trips: NonNegativeInt = 0
    worst_pair_acceptance: Annotated[float | None, AfterValidator(round_optional_float(4))] = None


class CovalentInhibitorScanPoint(Base):
    """
    One point on the reactivity profile.

    :param index: window index
    :param distance: bias center for this window, in Å
    :param force_constant: harmonic bias force constant, in kcal/mol/Å²
    :param free_energy: unbiased free energy at this center, in kcal/mol
    :param mean_distance: mean sampled reactive-bond distance, in Å
    :param n_samples: production samples contributing to this window
    :param molecule: final sampled geometry of the model region
    """

    index: NonNegativeInt
    distance: Annotated[float, AfterValidator(round_float(4))]
    force_constant: Annotated[float, AfterValidator(round_float(4))]
    free_energy: Annotated[float | None, AfterValidator(round_optional_float(4))] = None
    mean_distance: Annotated[float | None, AfterValidator(round_optional_float(4))] = None
    n_samples: NonNegativeInt = 0
    molecule: Molecule | None = None


class CovalentInhibitorScanWorkflow(ProteinStructureWorkflow):
    """
    Workflow for evaluating a covalent inhibitor's reactivity.

    Seeds windows along the reactive bond distance with a steered pull, samples them, and
    combines them into a free energy profile.

    Inherited:
    :param protein: PDB or UUID of the covalently docked complex (protein plus
        the ligand as a non-polymer residue)

    New:
    :param protein_reactive_atom_index: 0-based index of the reacting protein atom, in PDB record order
    :param ligand_reactive_atom_index: 0-based index of the reacting ligand atom, in PDB record order
    :param reactant_smiles: SMILES of the neutral reactant ligand, used to rebuild the
        ligand as a separate non-covalent molecule at the MM level
    :param settings: how to run the sampling

    Results:
    :param points: profile points, in `window_centers` order
    :param convergence: diagnostics for the sampling, when available
    """

    protein_reactive_atom_index: NonNegativeInt
    ligand_reactive_atom_index: NonNegativeInt
    reactant_smiles: str

    settings: UmbrellaSamplingScanSettings = UmbrellaSamplingScanSettings()

    points: list[CovalentInhibitorScanPoint] = []
    convergence: UmbrellaSamplingConvergence | None = None

    @computed_field
    @property
    def barrier(self) -> float | None:
        """Activation free energy for addition, in kcal/mol, or None without an interior maximum."""
        ordered = sorted(self.points, key=lambda point: point.distance)
        energies = [point.free_energy for point in ordered if point.free_energy is not None]
        if not energies or len(energies) != len(ordered):
            return None

        peak = max(range(len(energies)), key=energies.__getitem__)
        if peak in (0, len(energies) - 1):
            return None
        return round(energies[peak] - energies[-1], 4)
