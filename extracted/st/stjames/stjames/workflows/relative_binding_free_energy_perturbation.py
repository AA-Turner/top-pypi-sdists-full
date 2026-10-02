"""Workflows covering RBFE graph construction and endpoint FEP execution."""

import math
from typing import Annotated, Any, Literal, Self

from pydantic import AfterValidator, Field, NonNegativeFloat, NonNegativeInt, PositiveFloat, PositiveInt, computed_field, model_validator

from ..base import Base, LowercaseStrEnum, round_float, round_optional_float
from ..charge import ChargeMethod
from ..forcefield import LigandParameterizationResult
from ..message import Message
from ..method import FFMethod, Method
from ..molecule import Molecule
from ..pdb import PDB
from ..types import UUID, NonPolymerResidueMapping, ProteinUUID, SimpleProteinMDTrajectory, round_list, round_list_of_lists
from .workflow import ProteinStructureWorkflow, Workflow

RBFELeg = Literal["vacuum", "solvent", "complex"]


class RBFEEdgeTopology(LowercaseStrEnum):
    """Topology strategy used to execute a free-energy graph edge."""

    SINGLE_TOPOLOGY = "single_topology"
    SEPARATED_TOPOLOGY = "separated_topology"


class TMDSeparatedTopologyAnchorEquilibrationSettings(Base):
    """Short joint equilibration used by automatic anchor selection."""

    n_eq_steps: PositiveInt = 10_000
    n_frames: PositiveInt = 100


class TMDSeparatedTopologyRestraintSettings(Base):
    """Boresch restraint force constants used by TMD separated topology.

    Force constants use TMD's native units: kJ/mol/nm² for bonds,
    kJ/mol/rad² for angles, and kJ/mol for dihedrals.
    """

    bond_force_constant: PositiveFloat = 500.0
    angle_force_constant: PositiveFloat = 200.0
    dihedral_force_constant: PositiveFloat = 10.0


class TMDSeparatedTopologySettings(Base):
    """TMD controls exposed specifically for separated-topology edges."""

    anchor_selection_method: Literal["baumann_rmsf"] = "baumann_rmsf"
    anchor_equilibration: TMDSeparatedTopologyAnchorEquilibrationSettings = TMDSeparatedTopologyAnchorEquilibrationSettings()
    restraints: TMDSeparatedTopologyRestraintSettings = TMDSeparatedTopologyRestraintSettings()


class TMDRBFESettings(Base):
    """
    TMD-specific simulation parameters shared across RBFE graph edges.

    This settings bundle targets the TMD runner; other engines should define
    their own settings model if their controls differ.

    :param forcefield: Registered St. James method corresponding to a force field.
    :param charge_method: method for computing partial charges
    :param n_eq_steps: Equilibration steps per lambda window.
    :param n_frames: Production frames saved per lambda window.
    :param steps_per_frame: MD integration steps per saved frame.
    :param n_windows: Maximum number of lambda windows considered for bisection.
    :param min_overlap: Minimum acceptable overlap during schedule bisection.
    :param target_overlap: Desired overlap after HREX optimization.
    :param water_sampling_padding: Extra nanometers added to the solvent sampling radius.
    :param rest_max_temperature_scale: Maximum effective temperature scaling for REST.
    :param rest_temperature_scale_interpolation: Functional form used for REST scaling.
    :param local_md_steps: Number of local MD steps per frame (`0` disables local MD).
    :param local_md_k: Spring constant used during local MD.
    :param local_md_radius: Sphere radius in nanometers for the local MD region.
    :param local_md_free_reference: Whether to free the reference frame during local MD.
    :param legs: Which thermodynamic cycle legs to run (default: solvent and complex).
    :param save_trajectories: Whether to save complex- and solvent-leg endpoint DCD trajectories.
    :param trajectory_save_interval: Save every Nth frame when saving trajectories.
    :param separated_topology_settings: Controls used only for separated-topology edges.
    """

    forcefield: FFMethod = Method.OFF_SAGE_2_0_0
    charge_method: ChargeMethod = ChargeMethod.AMBER_AM1BCC
    n_eq_steps: PositiveInt = 200_000
    n_frames: PositiveInt = 2_000
    steps_per_frame: PositiveInt = 400
    n_windows: PositiveInt = 48
    min_overlap: float = 0.667
    target_overlap: float = 0.667
    water_sampling_padding: float = 0.4
    rest_max_temperature_scale: float = 1.0
    rest_temperature_scale_interpolation: Literal["exponential", "linear"] = "exponential"
    local_md_steps: int = 390
    local_md_k: float = 10_000.0
    local_md_radius: float = 1.2
    local_md_free_reference: bool = False
    legs: list[RBFELeg] = ["solvent", "complex"]
    save_trajectories: bool = False
    trajectory_save_interval: PositiveInt = 100
    separated_topology_settings: TMDSeparatedTopologySettings = TMDSeparatedTopologySettings()


class RBFEResult(Base):
    """
    Aggregate RBFE outcome for a single ligand.

    :param dg: Predicted binding free energy difference (kcal/mol).
    :param dg_err: Uncertainty estimate on `dg`.
    """

    dg: Annotated[float, AfterValidator(round_float(3))]
    dg_err: Annotated[float, AfterValidator(round_float(3))]


class RBFELigandAtomIndices(Base):
    """
    Atom indices for filtering RBFE trajectory visualization.

    Used to identify which atoms in the solvated hybrid system correspond to
    ligand A vs ligand B. Protein and solvent atoms can be identified from
    residue names in the topology PDB.

    :param ligand_a: 0-indexed atom indices for ligand A (visible at lambda=0)
    :param ligand_b: 0-indexed atom indices for ligand B (visible at lambda=1)
    """

    ligand_a: list[NonNegativeInt]
    ligand_b: list[NonNegativeInt]


RBFEDiagnosticFamily = Literal["overlap", "convergence", "mixing"]
RBFELambdaValue = Annotated[float, AfterValidator(round_float(3))]
RBFELambdaPair = tuple[RBFELambdaValue, RBFELambdaValue]
RBFEUnitFloat = Annotated[float, Field(ge=0.0, le=1.0)]


class RBFEAnalysisError(Base):
    """A nonfatal failure encountered while calculating an edge diagnostic."""

    family: RBFEDiagnosticFamily
    explanation: str
    leg: RBFELeg | None = None


class RBFEOverlapDiagnostics(Base):
    """Adjacent-state energetic-overlap diagnostics for one thermodynamic leg."""

    lambda_values: Annotated[list[float], AfterValidator(round_list(3))]
    overlap_matrix: Annotated[
        list[list[RBFEUnitFloat]],
        Field(description="Raw full-state MBAR overlap matrix."),
        AfterValidator(round_list_of_lists(3)),
    ]
    adjacent_overlaps: Annotated[
        list[RBFEUnitFloat],
        Field(description="TMD-normalized pair overlaps (2 * O[0, 1]) for adjacent states."),
        AfterValidator(round_list(3)),
    ] = []
    minimum_adjacent_overlap: Annotated[
        RBFEUnitFloat | None,
        Field(description="Minimum TMD-normalized adjacent pair overlap."),
        AfterValidator(round_optional_float(3)),
    ] = None
    minimum_adjacent_lambda_pair: RBFELambdaPair | None = None
    nonfinite_energy_count: NonNegativeInt = Field(
        default=0,
        description="Nonfinite values in evaluated adjacent-state energy blocks; unevaluated entries are excluded.",
    )


class RBFEConvergencePoint(Base):
    """A free-energy estimate at an actual production prefix or suffix."""

    fraction: Annotated[RBFEUnitFloat, AfterValidator(round_float(3))]
    frame_count: PositiveInt
    estimate: Annotated[float, AfterValidator(round_float(3))]
    uncertainty: Annotated[NonNegativeFloat, AfterValidator(round_float(3))]


class RBFEConvergenceDiagnostics(Base):
    """
    Forward/reverse estimates and simple stability summaries.

    All free-energy estimates, differences, and uncertainties are reported in
    kcal/mol. Point uncertainties are asymptotic full-state MBAR standard errors
    and treat saved production frames as effectively decorrelated.
    """

    forward_convergence: list[RBFEConvergencePoint] = []
    reverse_convergence: list[RBFEConvergencePoint] = []


class RBFEMixingDiagnostics(Base):
    """Minimal replica-mixing diagnostics for one HREX leg."""

    neighbor_exchange_acceptance_rates: Annotated[list[RBFEUnitFloat], AfterValidator(round_list(3))] = []
    replicas_visiting_both_endpoints: NonNegativeInt = 0
    complete_round_trip_count: NonNegativeInt = 0


class RBFELegDiagnostics(Base):
    """The three v1 diagnostic families for one thermodynamic leg."""

    overlap: RBFEOverlapDiagnostics | None = None
    convergence: RBFEConvergenceDiagnostics | None = None
    mixing: RBFEMixingDiagnostics | None = None


class RBFEEdgeDiagnostics(Base):
    """Minimal simulation diagnostics for one RBFE graph edge."""

    complex: RBFELegDiagnostics | None = None
    solvent: RBFELegDiagnostics | None = None
    ddg: RBFEConvergenceDiagnostics | None = None
    analysis_errors: list[RBFEAnalysisError] = []


class RBFEReceptorAnchorAtom(Base):
    """A resolved receptor anchor with both topology index and PDB identity."""

    index: NonNegativeInt
    chain_id: str
    residue_name: str
    residue_id: str
    atom_name: str


class RBFESeparatedTopologyAnchors(Base):
    """Automatically selected anchors for one separated-topology edge.

    Receptor indices address the receptor topology. Ligand indices are local
    to their respective input molecules, rather than TMD's combined system.
    Ligand triplets are selected independently; the shared receptor triplet is
    selected using ligand A.
    """

    selection_method: Literal["baumann_rmsf"] = "baumann_rmsf"
    receptor_atoms: tuple[RBFEReceptorAnchorAtom, RBFEReceptorAnchorAtom, RBFEReceptorAnchorAtom]
    ligand_a_atoms: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt]
    ligand_b_atoms: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt]


class RBFESeparatedTopologyTetherAtoms(Base):
    """Ligand-local atoms joined by the solvent-leg tether."""

    ligand_a: NonNegativeInt
    ligand_b: NonNegativeInt


class RBFESeparatedTopologyMetadata(Base):
    """Resolved setup and analytical results for a separated-topology edge.

    Energies are in kcal/mol. The edge's corrected complex dG is the raw value
    plus ``restraint_correction_b - restraint_correction_a``.
    """

    anchors: RBFESeparatedTopologyAnchors | None = None
    tether_atoms: RBFESeparatedTopologyTetherAtoms | None = None
    complex_raw_dg: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    restraint_correction_a: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    restraint_correction_b: Annotated[float | None, AfterValidator(round_optional_float(3))] = None

    @computed_field
    @property
    def restraint_correction(self) -> float | None:
        """Net correction added to raw complex dG, in kcal/mol."""
        if self.restraint_correction_a is None or self.restraint_correction_b is None:
            return None
        return round(self.restraint_correction_b - self.restraint_correction_a, 3)


class RBFEGraphEdge(Base):
    """
    RBFE Edge definition with optional FEP edge results.

    :param ligand_a: Source ligand identifier.
    :param ligand_b: Target ligand identifier.
    :param topology: Free-energy topology strategy selected for this edge.
    :param core: Atom-mapping pairs of indices describing the shared core, if any.
    :param score: Optional score used during graph construction.
    :param separated_topology_metadata: Resolved setup and correction metadata for a separated-topology edge.
    :param complex_dg: Predicted complex-leg free energy difference (kcal/mol).
    :param complex_dg_err: Uncertainty on `complex_dg`.
    :param solvent_dg: Predicted solvent-leg free energy difference (kcal/mol).
    :param solvent_dg_err: Uncertainty on `solvent_dg`.
    :param vacuum_dg: Predicted vacuum-leg free energy difference (kcal/mol).
    :param vacuum_dg_err: Uncertainty on `vacuum_dg`.
    :param ddg: Combined cycle result derived from complex and solvent legs.
    :param ddg_err: Uncertainty on `ddg`.
    :param failed: Whether a required leg failed, making ddG impossible to compute.
    :param diagnostics: Optional overlap, convergence, and mixing diagnostics.
    :param complex_lambda_values: Deprecated legacy TMD bisection lambda schedule used by `reconstruct_ukln()`.
    :param complex_overlap_matrix: Deprecated legacy TMD overlap matrix returned by `reconstruct_ukln()`.
    :param complex_trajectories: mapping of lambda values to SimpleProteinMDTrajectory objects
    :param complex_protein_uuid: UUID of solvated system PDB for trajectory topology
    :param complex_ligand_atom_indices: ligand atom indices for visualization filtering
    :param solvent_trajectories: mapping of lambda values to solvent-leg SimpleProteinMDTrajectory objects
    :param solvent_protein_uuid: UUID of solvated ligand system PDB for solvent trajectory topology.
        This is not actually a protein, but it's a UUID corresponding to the protein table.
    :param solvent_ligand_atom_indices: ligand atom indices in the solvent trajectory topology
    """

    ligand_a: str
    ligand_b: str
    topology: RBFEEdgeTopology = RBFEEdgeTopology.SINGLE_TOPOLOGY
    core: list[tuple[NonNegativeInt, NonNegativeInt]] | None = None
    score: float | None = None
    separated_topology_metadata: RBFESeparatedTopologyMetadata | None = None

    complex_dg: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    complex_dg_err: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    solvent_dg: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    solvent_dg_err: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    vacuum_dg: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    vacuum_dg_err: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    ddg: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    ddg_err: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    failed: bool = False

    diagnostics: RBFEEdgeDiagnostics | None = None

    complex_lambda_values: Annotated[list[float] | None, AfterValidator(round_list(3))] = Field(
        default=None,
        description="Lambda schedule from the legacy TMD bisection/reconstruct_ukln overlap analysis; not a mirror of diagnostics.complex.overlap.",
        deprecated="Legacy TMD bisection lambda schedule used by reconstruct_ukln(); not a mirror of diagnostics.complex.overlap.",
    )
    complex_overlap_matrix: Annotated[list[list[float]], AfterValidator(round_list_of_lists(3))] | None = Field(
        default=None,
        description="Overlap matrix from the legacy TMD reconstruct_ukln analysis; not a mirror of diagnostics.complex.overlap.",
        deprecated="Legacy TMD overlap matrix returned by reconstruct_ukln(); not a mirror of diagnostics.complex.overlap.",
    )
    complex_trajectories: dict[float, SimpleProteinMDTrajectory] | None = None
    complex_protein_uuid: ProteinUUID | None = None
    complex_ligand_atom_indices: RBFELigandAtomIndices | None = None
    solvent_trajectories: dict[float, SimpleProteinMDTrajectory] | None = None
    solvent_protein_uuid: ProteinUUID | None = None
    solvent_ligand_atom_indices: RBFELigandAtomIndices | None = None

    @model_validator(mode="after")
    def validate_topology_specific_fields(self) -> Self:
        """Reject fields that are incompatible with the selected topology."""
        if self.topology == RBFEEdgeTopology.SEPARATED_TOPOLOGY:
            if self.core is not None:
                raise ValueError("separated-topology edges cannot define an atom-mapping core")
        elif self.separated_topology_metadata is not None:
            raise ValueError("separated_topology_metadata requires topology='separated_topology'")
        return self


class RBFEGraph(Base):
    """
    Minimal RBFE graph container.

    :param edges: Directed edges describing the ligand pairs to simulate.
    """

    edges: list[RBFEGraphEdge]


class RBFEGraphWorkflow(Workflow):
    """
    Workflow that builds an rbfe graph for a set of ligands.

    :param ligands: Mapping from ligand identifiers to `Molecule` objects.
    :param seed_graph: Optional pre-existing graph from a prior run to extend.
    :param graph: Optional RBFE graph output populated after the build step.
    :param mode: Graph construction strategy (`"greedy"` or `"star_map"`).
    :param hub_compound_id: Ligand identifier to serve as the hub when `mode="star_map"`.
    :param refine_cutoff: Optional cutoff used to re-run atom mapping refinement.
    :param greedy_scoring: Edge scoring heuristic for greedy mode.
    :param greedy_k_min_cut: Target edge-connectivity (`k`) for greedy augmentation.
    :param separated_topology_planning_score: Optional flat planning score enabling separated-topology candidates;
        25.0 is recommended for initial mixed-network experiments.
    :param generate_intermediate_ligands: Generate virtual intermediate ligands to make difficult edges easier.
    :param intermediate_max_dummy_atoms: An edge with more dummy atoms than this is split when a generated
        intermediate brings both resulting legs back to at most this value.
    :param intermediate_min_dummy_atom_improvement: Minimum reduction in the worst leg's dummy-atom count
        required for a generated intermediate to be accepted.
    """

    ligands: dict[str, Molecule]
    seed_graph: RBFEGraph | None = None
    graph: RBFEGraph | None = None

    mode: Literal["greedy", "star_map"] = "greedy"
    hub_compound_id: str | None = None
    refine_cutoff: float | None = None
    greedy_scoring: Literal["best", "jaccard", "dummy_atoms"] = "best"
    greedy_k_min_cut: PositiveInt = 3
    separated_topology_planning_score: float | None = None

    generate_intermediate_ligands: bool = False
    intermediate_max_dummy_atoms: PositiveInt = 25
    intermediate_min_dummy_atom_improvement: PositiveInt = 5

    @model_validator(mode="after")
    def validate_builder(self) -> Self:
        """
        Validate the builder inputs.

        :raises ValueError: If star-map mode omits `hub_compound_id` or fewer than two ligands are provided.
        """
        if self.mode == "star_map" and not self.hub_compound_id:
            raise ValueError("hub_compound_id is required when mode='star_map'")
        if len(self.ligands) < 2:
            raise ValueError("Provide at least two ligands to build an RBFE graph")
        if self.separated_topology_planning_score is not None:
            if not math.isfinite(self.separated_topology_planning_score) or self.separated_topology_planning_score < 0:
                raise ValueError("separated_topology_planning_score must be finite and non-negative")
            if self.mode != "greedy":
                raise ValueError("Separated-topology graph planning supports only mode='greedy'")
            if "greedy_scoring" not in self.model_fields_set:
                self.greedy_scoring = "dummy_atoms"
            elif self.greedy_scoring != "dummy_atoms":
                raise ValueError("Separated-topology graph planning requires greedy_scoring='dummy_atoms'")
        return self


class RBFECycle(Base):
    """
    One independent cycle in the RBFE graph, with its closure statistics.

    :param ligands: Ligand identifiers, in path order, comprising the cycle.
    :param closure_error: Signed sum of ddG values around the cycle (kcal/mol).
    :param closure_error_uncertainty: Propagated uncertainty on `closure_error`.
    :param normalized_closure_error: Closure error divided by its propagated uncertainty.
    """

    ligands: list[str]
    closure_error: Annotated[float, AfterValidator(round_float(3))]
    closure_error_uncertainty: Annotated[float, AfterValidator(round_float(3))]

    @computed_field
    @property
    def normalized_closure_error(self) -> float | None:
        """Return the signed cycle-closure error in standard-error units."""
        if self.closure_error_uncertainty == 0:
            return None
        return round(self.closure_error / self.closure_error_uncertainty, 3)


class RBFEDiagnostics(Base):
    """
    Quality-control metrics gathered during endpoint RBFE.

    :param cycle_closure_rms: RMS error across the independent cycle basis.
    :param cycles: Independent cycle basis of the RBFE graph, with per-cycle closure statistics.
    :param windows_completed: Count of successfully converged lambda windows.
    :param windows_failed: Count of failed lambda windows.
    :param notes: Structured messages describing noteworthy events.
    """

    cycle_closure_rms: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    cycles: list[RBFECycle] = []
    windows_completed: PositiveInt | None = None
    windows_failed: PositiveInt | None = None
    notes: list[Message] = []


class RelativeBindingFreeEnergyPerturbationWorkflow(ProteinStructureWorkflow):
    """
    Workflow for running relative binding free energy perturbation simulations.

    Inherited:
    :param protein: PDB of the protein, or the UUID of the protein.

    New:
    :param ligands: Mapping from ligand identifiers to `Molecule` objects.
    :param graph: RBFE graph topology.
    :param target: PDB object or the UUID of the PDB object used for simulation. DEPRECATED.
    :param small_molecules: fixed non-candidate molecules included in complex simulations

    Results:
    :param ligand_dg_results: Optional per-ligand FEP summaries produced downstream.
    :param diagnostics: Optional aggregate QC metrics.
    :param settings: Simulation controls shared across all RBFE edges.
    """

    ligands: dict[str, Molecule]
    graph: RBFEGraph
    target: PDB | UUID | None = None
    small_molecules: NonPolymerResidueMapping | None = None

    settings: TMDRBFESettings

    ligand_dg_results: dict[str, RBFEResult] | None = None
    diagnostics: RBFEDiagnostics | None = None
    ligand_parameterizations: dict[str, LigandParameterizationResult] = Field(default_factory=dict)
    small_molecule_parameterizations: dict[str, LigandParameterizationResult] = Field(default_factory=dict)

    @model_validator(mode="before")
    def harmonize_target_and_protein(cls, data: Any) -> Any:  # noqa: N805
        """
        Syncs data between "target" and "protein" field.
        """
        protein = data.get("protein")
        target = data.get("target")

        if target and not protein:
            data["protein"] = target
        elif not target and protein:
            data["target"] = protein

        return data

    @model_validator(mode="after")
    def validate_separated_topology_execution(self) -> Self:
        """Validate execution constraints specific to separated topology."""
        separated_edges = [edge for edge in self.graph.edges if edge.topology == RBFEEdgeTopology.SEPARATED_TOPOLOGY]
        if not separated_edges:
            return self
        if "vacuum" in self.settings.legs:
            raise ValueError("separated-topology edges support only solvent and complex legs")
        for edge in separated_edges:
            ligand_a = self.ligands.get(edge.ligand_a)
            ligand_b = self.ligands.get(edge.ligand_b)
            if ligand_a is not None and ligand_b is not None and ligand_a.charge != ligand_b.charge:
                raise ValueError("separated-topology edges require ligands with equal formal charge")
        return self
