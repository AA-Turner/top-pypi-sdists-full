"""Docking workflow."""

from typing import Annotated, Any, Literal, Self, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    field_validator,
    model_validator,
)

from ..base import Base, LowercaseStrEnum, round_float
from ..conformers import ConformerGenSettingsUnion, OpenConfSettings
from ..pdb import PDB, ResidueAtomRef
from ..types import UUID, ProteinUUID, Vector3D
from .workflow import MoleculeWorkflow, ProteinStructureWorkflow

CalculationUUID: TypeAlias = UUID


def _validate_atom_ref(reference: int | ResidueAtomRef) -> int | ResidueAtomRef:
    """Require named-atom references to identify an atom."""
    if isinstance(reference, ResidueAtomRef):
        residue = reference.residue
        if not residue.key or (residue.entity_type == "polymer" and not residue.residue_key):
            raise ValueError("Atom reference must identify a residue")
        if not reference.atom_name.strip():
            raise ValueError("Atom name must not be empty")
    return reference


AtomRef: TypeAlias = Annotated[NonNegativeInt | ResidueAtomRef, AfterValidator(_validate_atom_ref)]


class Score(Base):
    """Pose with its score.

    Attributes:
        pose: conformation of the ligand when docked (calculation UUID)
        complex_pdb: UUID of protein–ligand complex (protein UUID)
        score: primary docking score from the selected scoring function
        affinity_score: predicted binding affinity of the pose (in log10(M))
        posebusters_valid: indicates that the ligand pose passes PoseBusters, or None when not evaluated
        strain: strain (kcal/mol)
        rmsd: RMSD from the reference, if there's a reference molecule to dock against (Å)
        mmgbsa_score: MM/GBSA binding free energy estimate (kcal/mol); None when run_local_optimization=False
        receptor_strain: induced receptor strain relative to locally relaxed unbound receptor (kcal/mol)
        geometry_penalty: penalty applied to invalid induced-fit poses (kcal/mol)
        induced_fit_score: composite score used to rank rigid and induced-fit poses (kcal/mol)
        induced_receptor_pdb: UUID of relaxed receptor used for induced-fit redocking
    """

    pose: CalculationUUID | None
    complex_pdb: ProteinUUID | None
    score: Annotated[float, AfterValidator(round_float(3))]
    affinity_score: Annotated[float, AfterValidator(round_float(3))] | None = None
    posebusters_valid: bool | None = None
    strain: float | None = None
    rmsd: Annotated[float, AfterValidator(round_float(3))] | None = None
    mmgbsa_score: Annotated[float, AfterValidator(round_float(3))] | None = None
    receptor_strain: Annotated[float, AfterValidator(round_float(3))] | None = None
    geometry_penalty: Annotated[float, AfterValidator(round_float(3))] | None = None
    induced_fit_score: Annotated[float, AfterValidator(round_float(3))] | None = None
    induced_receptor_pdb: ProteinUUID | None = None


class DockingSettings(BaseModel):
    """Base class for controlling how docked poses are generated.

    Attributes:
        max_poses: maximum number of poses generated per input molecule
    """

    max_poses: int = 4


class GninaSettings(DockingSettings):
    """Controls how gnina is run.

    When both covalent atom indices are provided, gnina runs in covalent docking mode.
    Both covalent indices must be supplied together, and covalent docking requires `scoring_function="vina"`.
    When neither is provided, gnina runs in non-covalent mode with the selected scoring function.

    Attributes:
        settings_type: docking-settings discriminator, fixed to `gnina`
        max_poses: inherited maximum number of poses generated per input molecule
        exhaustiveness: how many times gnina attempts to find a pose
        scoring_function: scoring function to use.
            - `"gnina_cnn"`: `Score.score` is CNNscore (higher is better), and
              `Score.affinity_score` is populated with CNNaffinity
            - `"vina"`: `Score.score` is minimizedAffinity (lower is better),
              `Score.affinity_score` is None, and CNN scoring is disabled

        covalent_ligand_atom_index: 0-based all-atom index of the reacting ligand atom
            (includes hydrogens)

        covalent_protein_atom_index: zero-based all-atom index of the reacting protein atom
            (in PDB file order, includes hydrogens), or named-atom reference resolved during preparation
    """

    settings_type: Literal["gnina"] = "gnina"
    exhaustiveness: int = 8
    scoring_function: Literal["gnina_cnn", "vina"] = "gnina_cnn"
    covalent_ligand_atom_index: int | None = None
    covalent_protein_atom_index: AtomRef | None = None

    @model_validator(mode="after")
    def check_covalent_fields(self) -> Self:
        """Validate covalent settings."""
        set_fields = (
            self.covalent_ligand_atom_index is not None,
            self.covalent_protein_atom_index is not None,
        )
        if any(set_fields) and not all(set_fields):
            raise ValueError("covalent_ligand_atom_index and covalent_protein_atom_index must be set together or both omitted.")
        if all(set_fields) and self.scoring_function != "vina":
            raise ValueError('Covalent gnina docking requires scoring_function="vina".')
        return self

    @property
    def is_covalent(self) -> bool:
        """Return True if covalent docking is configured."""
        return self.covalent_ligand_atom_index is not None


class InducedFitSettings(BaseModel):
    """Control soft docking, local receptor relaxation, and induced-receptor redocking.

    Attributes:
        max_receptors: maximum number of representative poses relaxed into induced receptors
        flexible_sidechain_radius: ligand distance cutoff for selecting flexible receptor residues, in Å
    """

    max_receptors: PositiveInt = 6
    flexible_sidechain_radius: PositiveFloat = 5.0


class VinaSettings(DockingSettings):
    """Controls how AutoDock Vina is run.

    `executable="heron"` uses Heron's fixed private-state search, as does
    `HeronSettings`.

    Attributes:
        settings_type: docking-settings discriminator, fixed to `vina`
        max_poses: inherited maximum number of poses generated per input molecule
        executable: which Vina implementation is run.
        scoring_function: which scoring function is employed.
        exhaustiveness: how many times Vina attempts to find a pose.
            8 is typical, 32 is considered relatively careful.
    """

    settings_type: Literal["vina"] = "vina"
    executable: Literal["qvina2", "qvina-w", "vina", "heron"] = "vina"
    scoring_function: Literal["vinardo", "vina"] = "vinardo"
    exhaustiveness: int = 8

    @model_validator(mode="after")
    def check_executable_scoring_function(self) -> Self:
        """Check if the combination of exectuable and scoring function is supported."""
        if (self.executable in {"qvina2", "qvina-w"}) and (self.scoring_function == "vinardo"):
            raise ValueError("QVina does not implement the Vinardo scoring function!")
        if self.executable == "heron" and self.scoring_function != "vinardo":
            raise ValueError("Heron implements Vinardo scoring only.")
        return self


class DockingDistanceRestraint(BaseModel):
    """Harmonic distance restraint between a ligand atom and a protein atom.

    Preparation resolves named protein atoms before calling the docking engine.

    Attributes:
        type: restraint discriminator
        ligand_atom_index: zero-based all-atom index in the separately supplied ligand, including hydrogens
        protein_atom_index: zero-based all-atom index in the separately supplied protein, including hydrogens,
            or named-atom reference in that protein
        target: target distance in Å
        force_constant: spring constant in kcal/mol/Å² for `0.5*k*(r-target)^2`
    """

    type: Literal["distance"] = "distance"
    ligand_atom_index: NonNegativeInt
    protein_atom_index: AtomRef
    target: Annotated[FiniteFloat, Field(ge=0)]
    force_constant: Annotated[FiniteFloat, Field(ge=0)] = 10


class DockingPositionRestraint(BaseModel):
    """Harmonic tether of one ligand atom to an absolute position.

    Attributes:
        type: restraint discriminator
        ligand_atom_index: zero-based all-atom ligand index, including hydrogens
        position: target Cartesian position in Å in the receptor coordinate frame
        force_constant: spring constant in kcal/mol/Å² for `0.5*k*|r-position|²`
    """

    type: Literal["position"] = "position"
    ligand_atom_index: NonNegativeInt
    position: tuple[FiniteFloat, FiniteFloat, FiniteFloat]
    force_constant: Annotated[FiniteFloat, Field(ge=0)] = 10


DockingRestraint: TypeAlias = Annotated[DockingDistanceRestraint | DockingPositionRestraint, Field(discriminator="type")]


class HeronSettings(DockingSettings):
    """Configure Heron docking with Vinardo scoring and optional harmonic restraints.

    Ordinary search uses four serial 250,000-call chunks and retains at most five poses.
    Both covalent atom indices together select prepared-product covalent docking;
    they identify the attachment and do not define missing product chemistry.
    `max_poses` limits delivered poses without changing the search budget.
    Exhaustiveness, scoring overrides and custom weights are unsupported.
    Local optimization and score-only operations use the same Vinardo objective.

    Attributes:
        settings_type: docking-settings discriminator, fixed to `heron`
        max_poses: maximum number of delivered poses per input molecule
        seed: deterministic search seed in Heron's public seed domain
        restraints: harmonic protein–ligand distance restraints and ligand position
            tethers, phased in during local search
        covalent_ligand_atom_index: zero-based reacting ligand atom index, including hydrogens
        covalent_protein_atom_index: zero-based reacting protein atom index in PDB file order, including hydrogens,
            or named-atom reference resolved during preparation
    """

    settings_type: Literal["heron"] = "heron"
    seed: Annotated[int, Field(ge=1, le=2147483647)] = 1

    restraints: list[DockingRestraint] = []
    covalent_ligand_atom_index: NonNegativeInt | None = None
    covalent_protein_atom_index: AtomRef | None = None

    @model_validator(mode="after")
    def check_covalent_fields(self) -> Self:
        """Require both reacting atom indices together."""
        if (self.covalent_ligand_atom_index is None) != (self.covalent_protein_atom_index is None):
            raise ValueError("Both covalent atom indices must be supplied together")
        return self

    @property
    def is_covalent(self) -> bool:
        """Return whether covalent docking is selected."""
        return self.covalent_ligand_atom_index is not None

    @property
    def executable(self) -> Literal["heron"]:
        """Return the fixed executable identifier."""
        return "heron"

    @property
    def scoring_function(self) -> Literal["vinardo"]:
        """Return the fixed scoring function."""
        return "vinardo"


class TurboDockPreset(LowercaseStrEnum):
    """Named search-effort presets for TurboDock."""

    FAST = "fast"
    BALANCED = "balanced"
    RIGOROUS = "rigorous"


class TurboDockSettings(DockingSettings):
    """Configure explicit scientific parameters for high-throughput GPU batch docking.

    Presets resolve to numeric search parameters. Execution backends control
    hardware allocation and scheduling.

    Attributes:
        max_poses: maximum number of alternative poses returned per ligand
        scoring_function: scoring function used during docking
        exhaustiveness: number of independent search attempts per ligand
        max_search_steps: maximum global search steps per attempt
    """

    max_poses: PositiveInt = 1
    settings_type: Literal["turbodock"] = "turbodock"
    scoring_function: Literal["vina", "vinardo"] = "vina"
    exhaustiveness: PositiveInt = 128
    max_search_steps: PositiveInt = 20

    @classmethod
    def from_preset(
        cls,
        preset: TurboDockPreset | str,
        *,
        scoring_function: Literal["vina", "vinardo"] = "vina",
        max_poses: int = 1,
    ) -> Self:
        """Construct explicit search parameters from a preset.

        Args:
            preset: named search-effort preset or its string value
            scoring_function: scoring function independent of the search preset
            max_poses: maximum number of alternative poses returned per ligand

        Returns:
            Settings containing the resolved search parameters

        Raises:
            ValueError: preset is unsupported

        Examples:
            >>> settings = TurboDockSettings.from_preset(TurboDockPreset.BALANCED)
            >>> settings.exhaustiveness, settings.max_search_steps
            (384, 40)
        """
        settings = _TURBODOCK_PRESETS[TurboDockPreset(preset)]
        return cls.model_validate(settings.model_dump() | {"scoring_function": scoring_function, "max_poses": max_poses})


_TURBODOCK_PRESETS = {
    TurboDockPreset.FAST: TurboDockSettings(exhaustiveness=128, max_search_steps=20),
    TurboDockPreset.BALANCED: TurboDockSettings(exhaustiveness=384, max_search_steps=40),
    TurboDockPreset.RIGOROUS: TurboDockSettings(exhaustiveness=512, max_search_steps=40),
}


DockingSettingsUnion = Annotated[VinaSettings | HeronSettings | GninaSettings, Field(discriminator="settings_type")]


class DockingWorkflow(MoleculeWorkflow, ProteinStructureWorkflow):
    """Docking workflow.

    Note that the protein can be supplied either by UUID or raw PDB object.
    We anticipate that the former will dominate deployed usage, but the latter is handy for isolated testing.
    If, for whatever reason, the workflow is initialized with both a `target_uuid` and a `target`, the UUID will be ignored.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (currently unused)
        protein: Protein target, as PDB or UUID

        target: PDB of the protein; DEPRECATED.
        target_uuid: UUID of the protein; DEPRECATED.
        pocket: center (x, y, z) and size (x, y, z) of the pocket
        do_csearch: search starting structures for conformers when true
        conformer_gen_settings: settings for initial conformer search.
        do_optimization: optimize starting structures when true
        do_pose_refinement: optimize non-rotatable bonds in output poses when true
        induced_fit_settings: induced-fit configuration; None disables induced fit
        docking_settings: settings for the docking engine

        conformers: UUIDs of optimized conformers
        scores: docked poses sorted by score
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    target: PDB | None = None
    target_uuid: UUID | None = None
    pocket: tuple[Vector3D, Vector3D]

    docking_settings: DockingSettingsUnion = VinaSettings()

    do_csearch: bool = True
    conformer_gen_settings: ConformerGenSettingsUnion = OpenConfSettings(max_confs=5, n_steps=30)
    do_optimization: bool = True
    do_pose_refinement: bool = True
    induced_fit_settings: InducedFitSettings | None = None

    conformers: list[CalculationUUID] = []
    scores: list[Score] = []

    def __str__(self) -> str:
        """Return the workflow representation as text."""
        return repr(self)

    def __repr__(self) -> str:
        """Return a string representation of the Docking workflow."""
        if self.target is not None:
            desc = self.target.description
            target = desc.code or desc.title
        else:
            target = ""

        ligand = "".join(atom.atomic_symbol for atom in self.initial_molecule.atoms)
        return f"<{type(self).__name__} {target} {ligand}>"

    @model_validator(mode="before")
    def harmonize_target_and_protein(cls, data: Any) -> Any:  # noqa: N805
        """Syncs data between "target"/"target_uuid" and "protein" field.

        Args:
            data: input model data to normalize
        """
        protein = data.get("protein", False)
        target = data.get("target", False)
        target_uuid = data.get("target_uuid", False)

        if not protein:
            if target:
                data["protein"] = target
            elif target_uuid:
                data["protein"] = target_uuid
        elif not target and not target_uuid:
            if isinstance(data["protein"], PDB):
                data["target"] = protein
            elif isinstance(data["protein"], UUID):
                data["target_uuid"] = protein

        return data

    @model_validator(mode="after")
    def check_protein(self) -> Self:
        """Check if protein is provided."""
        if not self.target and not self.target_uuid:
            raise ValueError("Must provide either target or target_uuid")
        return self

    @model_validator(mode="after")
    def check_induced_fit_engine(self) -> Self:
        """Require an engine supported by the induced-fit protocol."""
        if self.induced_fit_settings is None:
            return self
        if not isinstance(self.docking_settings, VinaSettings) or self.docking_settings.executable not in {
            "vina",
            "qvina2",
        }:
            raise ValueError("Induced-fit docking requires the Vina or QVina2 executable.")
        return self

    @field_validator("pocket", mode="after")
    def validate_pocket(cls, pocket: tuple[Vector3D, Vector3D]) -> tuple[Vector3D, Vector3D]:
        """Require positive pocket dimensions.

        Args:
            pocket: pocket center and dimensions

        Returns:
            validated pocket

        Raises:
            ValueError: any pocket dimension is nonpositive
        """
        _center, size = pocket
        if any(q <= 0 for q in size):
            raise ValueError(f"Pocket size must be positive, got: {size}")
        return pocket


class AnalogueDockingWorkflow(MoleculeWorkflow, ProteinStructureWorkflow):
    """Dock analogues of an initial molecule.

    (1) Conformers are generated in analogous poses to the initial molecule.
    (2) They're then optimized locally using the docking scoring function.
    (3) PoseBusters is used to check the validity of the output poses.

    Attributes:
        initial_molecule: molecule of interest, to which subsequent molecules will be aligned
        mode: Mode for workflow (currently unused)
        protein: PDB or UUID

        analogues: SMILES for analogues of `initial_molecule`
        analogue_names: molecule names parallel to `analogues` (empty string = no name); either empty or same length as `analogues`
        num_conformers_per_analogue: number of top poses to retain per analogue; 5× this many conformers are generated internally and the best are kept
        require_posebusters: filter conformers based on PoseBusters validity before docking
        run_local_optimization: optimize in the docking pocket when true, or just score otherwise
        docking_settings: how docking should be run; Vina and Heron executables are supported

        analogue_scores: docked poses for each analogue of form {smiles: list[poses]}
    """

    analogues: list[str]
    analogue_names: list[str] = []
    num_conformers_per_analogue: PositiveInt = 20
    require_posebusters: bool = False
    run_local_optimization: bool = False
    docking_settings: Annotated[VinaSettings | HeronSettings, Field(discriminator="settings_type")] = VinaSettings()

    analogue_scores: dict[str, list[Score]] = {}

    @model_validator(mode="after")
    def check_analogue_names_length(self) -> Self:
        """Check that analogue_names is either empty or the same length as analogues."""
        if self.analogue_names and len(self.analogue_names) != len(self.analogues):
            raise ValueError(
                f"analogue_names must be empty or the same length as analogues (got {len(self.analogue_names)} names for {len(self.analogues)} analogues)"
            )
        return self

    @model_validator(mode="after")
    def check_analogue_docking_executable(self) -> Self:
        """Check that Vina or Heron is used for analogue docking."""
        if self.docking_settings.executable not in {"vina", "heron"}:
            raise ValueError(
                f"AnalogueDockingWorkflow only supports the vina and heron executables, not {self.docking_settings.executable!r} "
                "(qvina2 and qvina-w are not supported)"
            )
        return self
