"""Docking workflow."""

from typing import Annotated, Any, Literal, Self, TypeAlias

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    PositiveFloat,
    PositiveInt,
    field_validator,
    model_validator,
)

from ..base import Base, round_float
from ..conformers import ConformerGenSettingsUnion, OpenConfSettings
from ..pdb import PDB
from ..types import UUID, ProteinUUID, Vector3D
from .workflow import MoleculeWorkflow, ProteinStructureWorkflow

CalculationUUID: TypeAlias = UUID


class Score(Base):
    """
    Pose with its score.

    :param pose: conformation of the ligand when docked (calculation UUID)
    :param complex_pdb: UUID of protein–ligand complex (protein UUID)
    :param score: primary docking score from the selected scoring function
    :param affinity_score: predicted binding affinity of the pose (in log10(M))
    :param posebusters_valid: whether ligand pose passes PoseBusters, or None when not evaluated
    :param strain: strain (kcal/mol)
    :param rmsd: RMSD from the reference, if there's a reference molecule to dock against (Å)
    :param mmgbsa_score: MM/GBSA binding free energy estimate (kcal/mol); None when run_local_optimization=False
    :param receptor_strain: induced receptor strain relative to locally relaxed unbound receptor (kcal/mol)
    :param geometry_penalty: penalty applied to invalid induced-fit poses (kcal/mol)
    :param induced_fit_score: composite score used to rank rigid and induced-fit poses (kcal/mol)
    :param induced_receptor_pdb: UUID of relaxed receptor used for induced-fit redocking
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
    """
    Base class for controlling how docked poses are generated.

    :param max_poses: maximum number of poses generated per input molecule
    """

    max_poses: int = 4


class GninaSettings(DockingSettings):
    """
    Controls how gnina is run.

    When both covalent atom indices are provided, gnina runs in covalent docking mode.
    When neither is provided (the default), gnina runs in standard non-covalent mode
    with CNN scoring.

    :param exhaustiveness: how many times gnina attempts to find a pose
    :param scoring_function: scoring function to use.
        - `"gnina_cnn"`: `Score.score` is CNNscore (higher is better), and
          `Score.affinity_score` is populated with CNNaffinity
        - `"vina"`: `Score.score` is minimizedAffinity (lower is better),
          `Score.affinity_score` is None, and CNN scoring is disabled
    :param covalent_ligand_atom_index: 0-based all-atom index of the reacting ligand atom
        (includes hydrogens)
    :param covalent_protein_atom_index: 0-based all-atom index of the reacting protein atom
        (in PDB file order, includes hydrogens)
    """

    settings_type: Literal["gnina"] = "gnina"
    exhaustiveness: int = 8
    scoring_function: Literal["gnina_cnn", "vina"] = "gnina_cnn"
    covalent_ligand_atom_index: int | None = None
    covalent_protein_atom_index: int | None = None

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
    """
    Control soft docking, local receptor relaxation, and induced-receptor redocking.

    :param max_receptors: maximum number of representative poses relaxed into induced receptors
    :param flexible_sidechain_radius: ligand distance cutoff for selecting flexible receptor residues, in Å
    """

    max_receptors: PositiveInt = 6
    flexible_sidechain_radius: PositiveFloat = 5.0


class VinaSettings(DockingSettings):
    """
    Controls how AutoDock Vina is run.

    :param executable: which Vina implementation is run.
    :param scoring_function: which scoring function is employed.
    :param exhaustiveness: how many times Vina attempts to find a pose.
        8 is typical, 32 is considered relatively careful.
    """

    settings_type: Literal["vina"] = "vina"
    executable: Literal["qvina2", "qvina-w", "vina"] = "vina"
    scoring_function: Literal["vinardo", "vina"] = "vinardo"
    exhaustiveness: int = 8

    @model_validator(mode="after")
    def check_executable_scoring_function(self) -> Self:
        """Check if the combination of exectuable and scoring function is supported."""
        if (self.executable in {"qvina2", "qvina-w"}) and (self.scoring_function == "vinardo"):
            raise ValueError("QVina does not implement the Vinardo scoring function!")
        return self


DockingSettingsUnion = Annotated[VinaSettings | GninaSettings, Field(discriminator="settings_type")]


class DockingWorkflow(MoleculeWorkflow, ProteinStructureWorkflow):
    """
    Docking workflow.

    Note that the protein can be supplied either by UUID or raw PDB object.
    We anticipate that the former will dominate deployed usage, but the latter is handy for isolated testing.
    If, for whatever reason, the workflow is initialized with both a `target_uuid` and a `target`, the UUID will be ignored.

    Inherited:
    :param initial_molecule: Molecule of interest
    :param mode: Mode for workflow (currently unused)
    :param protein: Protein target, as PDB or UUID

    New:
    :param target: PDB of the protein; DEPRECATED.
    :param target_uuid: UUID of the protein; DEPRECATED.
    :param pocket: center (x, y, z) and size (x, y, z) of the pocket
    :param do_csearch: whether to csearch starting structures
    :param conformer_gen_settings: settings for initial conformer search.
    :param do_optimization: whether to optimize starting structures
    :param do_pose_refinement: whether to optimize non-rotatable bonds in output poses
    :param induced_fit_settings: induced-fit configuration; None disables induced fit

    Results:
    :param conformers: UUIDs of optimized conformers
    :param scores: docked poses sorted by score
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
        """
        Syncs data between "target"/"target_uuid" and "protein" field.
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
        _center, size = pocket
        if any(q <= 0 for q in size):
            raise ValueError(f"Pocket size must be positive, got: {size}")
        return pocket


class AnalogueDockingWorkflow(MoleculeWorkflow, ProteinStructureWorkflow):
    """
    Workflow for docking analogues:
    (1) Conformers are generated in analogous poses to the initial molecule.
    (2) They're then optimized locally using the docking scoring function.
    (3) PoseBusters is used to check the validity of the output poses.

    Inherited:
    :param initial_molecule: molecule of interest, to which subsequent molecules will be aligned
    :param mode: Mode for workflow (currently unused)
    :param protein: PDB or UUID

    New:
    :param analogues: SMILES for analogues of `initial_molecule`
    :param analogue_names: molecule names parallel to `analogues` (empty string = no name); either empty or same length as `analogues`
    :param num_conformers_per_analogue: the number of top poses to retain per analogue; 5× this many conformers are generated internally and the best are kept
    :param require_posebusters: filter conformers based on PoseBusters validity before docking
    :param run_local_optimization: whether to run a local optimization in the docking pocket or just to score
    :param docking_settings: how docking should be run; only the vina executable is supported

    Results:
    :param analogue_scores: docked poses for each analogue of form {smiles: list[poses]}
    """

    analogues: list[str]
    analogue_names: list[str] = []
    num_conformers_per_analogue: PositiveInt = 20
    require_posebusters: bool = False
    run_local_optimization: bool = False
    docking_settings: VinaSettings = VinaSettings()

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
    def check_vina_only(self) -> Self:
        """Check that only the vina executable is used."""
        if self.docking_settings.executable != "vina":
            raise ValueError(
                f"AnalogueDockingWorkflow only supports the vina executable, not {self.docking_settings.executable!r} (qvina2 and qvina-w are not supported)"
            )
        return self
