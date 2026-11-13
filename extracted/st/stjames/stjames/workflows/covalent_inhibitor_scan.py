"""Covalent inhibitor reactivity workflow, via ML/MM umbrella sampling."""

import math
from itertools import pairwise
from typing import Annotated, Self

import numpy as np
from pydantic import (
    AfterValidator,
    Field,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    model_validator,
)

from ..base import Base, UniqueList, round_float
from ..coordinate import DistanceCoordinate, LinearCombinationCoordinate
from ..engine import Engine
from ..method import FFMethod, Method, ProteinForceField, WaterForceField
from ..molecule import Molecule
from ..pdb import ResidueAtomRef, ResidueRef
from ..restraint import MDRestraints
from ..settings import Settings
from ..types import UUID, SimpleProteinMDTrajectory, round_list
from .scan import ScanSettings
from .workflow import ProteinStructureWorkflow

_RoundedPositiveFloat = Annotated[PositiveFloat, AfterValidator(round_float(3))]


class CovalentInhibitorScanSettings(Base):
    """Settings for a covalent scan using restrained molecular dynamics.

    Each window holds the reaction coordinates near a different target.
    Preparation uses 4 ps to reach temperature and 80 fs per window to seed starting structures.
    Additional MD restraints remain in the reported free-energy surface.

    Attributes:
        small_molecule_ff: force field for the ligand
        protein_ff: force field for the protein
        water_ff: force field for water and ions
        equilibration_time_ns: equilibration duration per window, excluded from analysis, in ns
        simulation_time_ns: production sampling duration per window, in ns
        temperature: target simulation temperature, in K
        langevin_timescale_ps: Langevin friction coefficient, in ps⁻¹
        timestep_fs: time advanced by each dynamics step, in fs
        hydrogen_mass: hydrogen mass after transferring mass from bonded heavy atoms, in amu
        nonbonded_cutoff: cutoff for short-range nonbonded interactions, in Å. Long-range electrostatics use PME.
        ionic_strength_M: salt concentration used when adding solvent, in mol/L
        water_buffer: water padding around the protein–ligand complex, in Å
        protein_restraint_cutoff: distance from the nearest ligand atom beyond which protein Cα atoms are restrained, in Å.
            `None` disables these restraints.
        protein_restraint_constant: strength holding those Cα atoms near their starting positions, in kcal/mol/Å²
        restraints: additional MD restraints active during preparation and sampling
        calc_settings: method and engine for the reactive region and its capping hydrogens
        frame_save_interval_ps: time between saved full-system DCD frames, in ps. Does not set the free-energy sampling interval.
        scan_coordinates: one or two distances or weighted distance combinations, with stiffness defaulting to 45 kcal/mol/Å²
        reactive_region: whole protein residues, ligand, and waters selected by residue references for `calc_settings`.
            Must contain every scan atom.
        ligand: input ligand residue reference, also included in `reactive_region`
        reactive_region_charge: charge of the region plus caps, in elementary charge units. `None` infers it from the structure.
            Explicit values must agree with known prepared charges.
        reactive_region_multiplicity: spin multiplicity of the region plus caps: 1 for singlet, 2 for doublet, etc.
            `None` uses a singlet for even electron counts without detected ligand radicals. Other cases require an explicit value.
        bootstrap_samples: resampling repeats for free-energy error bars, at least 5. `None` disables uncertainty estimation.
    """

    small_molecule_ff: FFMethod = Method.OFF_SAGE_2_3_0
    protein_ff: ProteinForceField = ProteinForceField.FF14SB
    water_ff: WaterForceField = WaterForceField.TIP3P
    equilibration_time_ns: PositiveFloat = 0.02
    simulation_time_ns: PositiveFloat = 0.05
    temperature: _RoundedPositiveFloat = 298.15
    langevin_timescale_ps: _RoundedPositiveFloat = 1.0
    timestep_fs: _RoundedPositiveFloat = 2.0
    hydrogen_mass: _RoundedPositiveFloat = 4.0
    nonbonded_cutoff: _RoundedPositiveFloat = 8.0
    ionic_strength_M: Annotated[NonNegativeFloat, AfterValidator(round_float(3))] = 0.0
    water_buffer: _RoundedPositiveFloat = 8.0
    protein_restraint_cutoff: _RoundedPositiveFloat | None = None
    protein_restraint_constant: _RoundedPositiveFloat = 100.0
    restraints: list[MDRestraints] = []
    calc_settings: Settings = Settings(method=Method.ORB_V3_CONSERVATIVE_OMOL, engine=Engine.ORB)
    frame_save_interval_ps: PositiveFloat = 10
    scan_coordinates: Annotated[list[ScanSettings], Field(min_length=1, max_length=2)]
    reactive_region: Annotated[UniqueList[ResidueRef], Field(min_length=1)]
    ligand: ResidueRef
    reactive_region_charge: int | None = None
    reactive_region_multiplicity: PositiveInt | None = None
    bootstrap_samples: Annotated[int, Field(ge=5)] | None = None

    @model_validator(mode="after")
    def validate_frame_save_interval(self) -> Self:
        """Require frame intervals to span whole integration steps."""
        steps = self.frame_save_interval_ps * 1000 / self.timestep_fs
        if steps < 1 or not math.isclose(steps, round(steps), rel_tol=0, abs_tol=1e-8):
            raise ValueError("frame_save_interval_ps must be an integer multiple of timestep_fs")
        return self

    @model_validator(mode="after")
    def validate_surface(self) -> Self:
        """Validate region membership and independent coordinates."""
        selected = set(self.reactive_region)
        if self.ligand.entity_type != "non_polymer" or self.ligand not in selected:
            raise ValueError("The ligand must be a selected non-polymer residue")
        for ref in self.reactive_region:
            if ref.entity_type == "branched" or (ref.entity_type == "polymer") != (ref.residue_key is not None):
                raise ValueError("Region supports complete polymer residues, one ligand, and waters")
            if ref.entity_type == "non_polymer" and ref != self.ligand:
                raise ValueError("Only one reactive ligand is supported")
        expressions = self.distance_expressions
        for axis, expression in zip(self.scan_coordinates, expressions, strict=True):
            if axis.num < 2 or axis.start == axis.stop:
                raise ValueError("Umbrella scans require a nonzero range and at least two windows")
            if any(atom.residue not in selected for pair in expression for atom in pair):
                raise ValueError("All coordinate atoms must belong to the selected region")
        if len(self.scan_coordinates) == 2:
            pairs = list(dict.fromkeys(pair for expression in expressions for pair in expression))
            coefficients = np.array([[expression.get(pair, 0) for pair in pairs] for expression in expressions])
            coefficients /= np.max(np.abs(coefficients), axis=1, keepdims=True)
            if np.linalg.matrix_rank(coefficients) != len(self.scan_coordinates):
                raise ValueError("Coordinates must be independent")
        self.scan_coordinates = [axis.model_copy(update={"force_constant": 45.0}) if axis.force_constant is None else axis for axis in self.scan_coordinates]
        return self

    @property
    def distance_expressions(self) -> list[dict[tuple[ResidueAtomRef, ResidueAtomRef], float]]:
        """Resolve distance coordinates into weighted pairs of PDB atom references."""
        expressions = []
        for axis in self.scan_coordinates:
            coordinate = axis.resolved_coordinate
            if isinstance(coordinate, DistanceCoordinate):
                distances, coefficients = [coordinate], [1.0]
            elif isinstance(coordinate, LinearCombinationCoordinate):
                distances, coefficients = coordinate.coordinates, coordinate.coefficients
            else:
                raise ValueError("Covalent scans require distances or linear combinations of distances")
            expression = {}
            for distance, coefficient in zip(distances, coefficients, strict=True):
                first, second = distance.atoms
                if not isinstance(first, ResidueAtomRef) or not isinstance(second, ResidueAtomRef):
                    raise ValueError("Covalent scans require PDB atom references")
                expression[first, second] = coefficient
            expressions.append(expression)
        return expressions


class ResolvedScanAtom(Base):
    """Input atom matched to its location in the simulation.

    Attributes:
        reference: residue and atom name in the input PDB
        full_index: zero-based atom index in the full-system topology and DCD
        model_index: zero-based atom index in the reactive-region molecule. `None` outside that region
    """

    reference: ResidueAtomRef
    full_index: NonNegativeInt
    model_index: NonNegativeInt | None = None


class ResolvedScanSetup(Base):
    """Atom mappings and charges after system preparation.

    Attributes:
        atoms: input atoms matched to full-system and reactive-region indices
        boundary_pairs: bonds capped with hydrogen, as (inside, outside) zero-based full-system atom indices
        reactive_region_charge: charge used for the region plus caps, in elementary charge units
        reactive_region_multiplicity: spin multiplicity used for the region plus caps
    """

    atoms: list[ResolvedScanAtom]
    boundary_pairs: list[tuple[NonNegativeInt, NonNegativeInt]]
    reactive_region_charge: int
    reactive_region_multiplicity: PositiveInt


class UmbrellaWindowResult(Base):
    """Results for one target on the scan grid.

    Attributes:
        index: zero-based position along each grid axis
        centers: target reaction-coordinate values, in Å
        mean_coordinates: average reaction-coordinate values during production, in Å
        n_samples: production samples used for analysis, counted separately from saved DCD frames
        molecule: reactive region plus capping hydrogens from the snapshot whose reaction coordinates are closest to the target.
            Both coordinates count equally in 2D.
        trajectory: full-system DCD for this window, using the shared topology. Exchanges can switch which replica supplies frames.
            The first frame is saved one frame interval into production.
    """

    index: list[NonNegativeInt]
    centers: Annotated[list[float], AfterValidator(round_list(3))]
    mean_coordinates: Annotated[list[float] | None, AfterValidator(round_list(3))] = None
    n_samples: NonNegativeInt = 0
    molecule: Molecule | None = None
    trajectory: SimpleProteinMDTrajectory | None = None


class FreeEnergySurface(Base):
    """Free energies on a 1D or 2D grid at fixed temperature and volume.

    Cell lists use ascending coordinates, with the second axis varying fastest in 2D.

    Attributes:
        bin_edges: ascending cell boundaries along each coordinate, in Å
        free_energies: free energies from probability density, relative to the lowest populated cell, in kcal/mol.
            Empty cells are `None`.
        effective_samples: effective sample counts after reweighting, without correction for correlation between samples
        uncertainty: bootstrap standard deviations, in kcal/mol. `None` entries when disabled or unavailable
        outside_probability: fraction of reweighted probability outside the output grid, from 0 to 1
    """

    bin_edges: list[list[float]]
    free_energies: list[float | None]
    effective_samples: list[NonNegativeFloat]
    uncertainty: list[NonNegativeFloat | None]
    outside_probability: Annotated[float, Field(ge=0, le=1)] = 0

    @property
    def shape(self) -> list[int]:
        """Return bin counts along each axis."""
        return [len(edges) - 1 for edges in self.bin_edges]

    @model_validator(mode="after")
    def validate_shape(self) -> Self:
        """Require aligned axes and flattened cell arrays."""
        if len(self.bin_edges) not in (1, 2):
            raise ValueError("A surface must have one or two axes")
        for edges in self.bin_edges:
            if len(edges) < 2 or any(b <= a for a, b in pairwise(edges)):
                raise ValueError("Each axis requires at least two strictly increasing bin edges")
        size = math.prod(self.shape)
        if any(len(values) != size for values in (self.free_energies, self.effective_samples, self.uncertainty)):
            raise ValueError("Surface arrays must match the flattened shape")
        return self


class SurfaceDiagnostics(Base):
    """Window exchange counts and sampling overlap.

    Attributes:
        exchange_pairs: neighboring pairs of zero-based indices into `windows`
        exchange_attempts: exchanges attempted for each pair during equilibration and production
        exchange_accepts: exchanges accepted for each pair, in the same order as `exchange_pairs`
        overlap_matrix: MBAR sampling overlap, with rows and columns ordered like `windows`. Empty when unavailable
    """

    exchange_pairs: list[tuple[int, int]] = []
    exchange_attempts: list[NonNegativeInt] = []
    exchange_accepts: list[NonNegativeInt] = []
    overlap_matrix: list[list[NonNegativeFloat]] = []


class CovalentInhibitorScanWorkflow(ProteinStructureWorkflow):
    """Free-energy scan of a reaction in a prepared protein–ligand complex.

    Input coordinates and ligand SMILES must describe the intended starting protonation
    and connectivity. Scan coordinates identify atoms by residue and input atom name.

    Attributes:
        protein: prepared protein–ligand PDB structure or its saved UUID
        reactant_smiles: ligand reactant SMILES used to assign classical force-field parameters
        settings: reaction coordinates, reactive region, and simulation settings
        topology_uuid: shared full-system PDB with atoms in DCD order
        resolved_setup: atom mappings and charges from system preparation
        windows: per-window results, representative reactive-region snapshots, and DCD references
        surface: free-energy grid and sampling uncertainties. `None` when unavailable
        surface_diagnostics: window overlap and exchange counts
    """

    reactant_smiles: str
    settings: CovalentInhibitorScanSettings
    topology_uuid: UUID | None = None

    resolved_setup: ResolvedScanSetup | None = None
    windows: list[UmbrellaWindowResult] = []
    surface: FreeEnergySurface | None = None
    surface_diagnostics: SurfaceDiagnostics | None = None
