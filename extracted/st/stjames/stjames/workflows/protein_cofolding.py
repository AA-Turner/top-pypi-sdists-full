"""Protein cofolding workflow."""

from typing import Annotated, Literal, Self, TypeAlias

from pydantic import AfterValidator, BaseModel, ConfigDict, model_validator

from ..base import Base, LowercaseStrEnum, round_float, round_optional_float
from ..pdb import PDB
from ..types import UUID, ProteinUUID, round_list
from .protein_preparation import ProtonationMethod
from .workflow import FASTAWorkflow

CalculationUUID: TypeAlias = UUID


class CofoldingModel(LowercaseStrEnum):
    """Cofolding model to be used for prediction."""

    CHAI_1R = "chai_1r"
    BOLTZ_1 = "boltz_1"
    BOLTZ_2 = "boltz_2"
    BOLTZ_2_1 = "boltz_2_1"
    OPENFOLD_3 = "openfold_3"
    DECAF_BOLTZ = "decaf_boltz"


class Token(BaseModel):
    """Either an atom in a ligand or a residue in a protein or nucleotide chain."""

    input_type: Literal["ligand", "protein", "dna", "rna"]
    input_index: int
    token_index: int
    atom_name: str | None = None


class ContactConstraint(BaseModel):
    """Contact constraint to be used for prediction."""

    token_1: Token
    token_2: Token
    max_distance: float  # Å
    force: bool = False  # Whether to use potentials to enforce the constraint


class PocketConstraint(BaseModel):
    """Pocket constraint to be used for prediction."""

    input_type: Literal["ligand", "protein", "dna", "rna"]
    input_index: int
    contacts: list[Token]
    max_distance: float  # Å
    force: bool = False  # Whether to use potentials to enforce the constraint


class BondConstraint(BaseModel):
    """Covalent bond constraint to be used for prediction (Boltz-2 only)."""

    atom_1: Token
    atom_2: Token

    @model_validator(mode="after")
    def validate_atoms_distinct(self) -> Self:
        """Validate atom_1 and atom_2 are not identical."""
        if self.atom_1 == self.atom_2:
            raise ValueError(f"Bond constraint atoms must be distinct: {self!r}")
        return self


class CofoldingTemplate(BaseModel):
    """Structural templates to guide prediction.

    :param protein: PDB structure of protein, or UUID of PDB record in Rowan
    :param max_distance: maximum allowed deviation from the template, in Å; if set,
        the constraint is enforced with a potential
    """

    protein: PDB | UUID
    max_distance: float | None = None  # Å


class CofoldingScores(BaseModel):
    """The output scores from co-folding scores."""

    confidence_score: Annotated[float, AfterValidator(round_float(3))]
    ptm: Annotated[float, AfterValidator(round_float(3))]  # predicted template modeling score
    iptm: Annotated[float, AfterValidator(round_float(3))]  # interface predicted template modeling score
    avg_lddt: Annotated[float, AfterValidator(round_float(3))]


class AffinityScore(BaseModel):
    pred_value: Annotated[float, AfterValidator(round_float(3))] | None = None
    probability_binary: Annotated[float, AfterValidator(round_float(3))] | None = None
    pred_value1: Annotated[float, AfterValidator(round_float(3))] | None = None
    probability_binary1: Annotated[float, AfterValidator(round_float(3))] | None = None
    pred_value2: Annotated[float, AfterValidator(round_float(3))] | None = None
    probability_binary2: Annotated[float, AfterValidator(round_float(3))] | None = None
    binding_confidence: Annotated[float, AfterValidator(round_float(3))] | None = None
    optimization_score: Annotated[float, AfterValidator(round_float(3))] | None = None


class CofoldingResult(Base):
    """Results for a single cofolding sample.

    :param affinity_score: affinity score
    :param lddt: local distance different test result
    :param predicted_structure_uuid: UUID of the predicted structure
    :param scores: output cofolding scores
    :param pose: UUID of the calculation pose
    :param strain: strain of the ligand, in kcal/mol
    :param mmgbsa_score: MM/GBSA binding energy of the pose, in kcal/mol
    :param predicted_refined_structure_uuid: if the structure has been refined,
        UUID of the predicted structure after refinement
    """

    lddt: Annotated[list[float] | None, AfterValidator(round_list(3))] = None
    affinity_score: AffinityScore | None = None
    predicted_structure_uuid: ProteinUUID | None = None
    scores: CofoldingScores | None = None
    pose: CalculationUUID | None = None
    posebusters_valid: bool | None = None
    strain: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    mmgbsa_score: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    predicted_refined_structure_uuid: ProteinUUID | None = None


class ProteinCofoldingWorkflow(FASTAWorkflow):
    """
    Workflow for predicting structures.

    Especially protein structures. At least one biological sequence is required.

    Inherited:
    :param initial_protein_sequences: protein sequences of interest
    :param initial_dna_sequences: DNA sequences of interest
    :param initial_rna_sequences: RNA sequences of interest
    :param initial_smiles_list: SMILES strings of interest
    :param ligand_binding_affinity_index: optional index selecting which ligand affinity to evaluate
    :param protein_binding_affinity_indices: optional indices selecting which protein sequences to evaluate binding affinity for

    New:
    :param use_msa_server: whether to use the MSA server
    :param use_templates_server: whether to use the templates server
    :param use_potentials: whether to use the potentials (inference-time steering) with Boltz
    :param contact_constraints: Boltz contact constraints
    :param pocket_constraints: Boltz pocket constraints
    :param bond_constraints: Boltz covalent bond constraints (Boltz-2 only)
    :param templates: structural templates to guide prediction (Boltz-2 only)
    :param protonation_method: method used to protonate polymers; `None` skips protonation
        (incompatible with `do_pose_refinement`)
    :param pH: pH value used for protonation
    :param do_pose_refinement: whether to optimize non-rotatable bonds in output poses
        (incompatible with `bond_constraints`)
    :param compute_strain: whether to compute the strain of the pose (if pose_refinement is
        enabled; incompatible with `bond_constraints`)
    :param num_samples: number of samples generated for prediction
    :param model: which cofolding model to use
    :param cofolding_results: per diffusion sample outputs, grouped together
    """

    model_config = ConfigDict(validate_assignment=True)

    use_msa_server: bool = False
    use_templates_server: bool = False
    use_potentials: bool = False
    contact_constraints: list[ContactConstraint] = []
    pocket_constraints: list[PocketConstraint] = []
    bond_constraints: list[BondConstraint] = []
    templates: list[CofoldingTemplate] = []
    protonation_method: ProtonationMethod | None = ProtonationMethod.OPENMM
    pH: Annotated[float, AfterValidator(round_float(2))] = 7.4
    do_pose_refinement: bool = False
    compute_strain: bool = False
    num_samples: int | None = None

    model: CofoldingModel = CofoldingModel.BOLTZ_2
    cofolding_results: list[CofoldingResult] | None = None

    # Deprecated: these top-level fields mirror CofoldingResult and are kept for legacy
    # reasons only. New code should use CofoldingResult instead.
    affinity_score: AffinityScore | None = None
    lddt: Annotated[list[float] | None, AfterValidator(round_list(3))] = None
    predicted_structure_uuid: ProteinUUID | None = None
    scores: CofoldingScores | None = None
    pose: CalculationUUID | None = None
    posebusters_valid: bool | None = None
    strain: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
    predicted_refined_structure_uuid: ProteinUUID | None = None

    @model_validator(mode="after")
    def validate_model_compatibility(self) -> Self:
        """Validate feature/model compatibility."""
        if any(c.force for c in self.contact_constraints) and not self.use_potentials:
            raise ValueError("use_potentials must be True when any contact_constraint has force=True")

        if any(c.force for c in self.pocket_constraints) and not self.use_potentials:
            raise ValueError("use_potentials must be True when any pocket_constraint has force=True")

        if self.model == CofoldingModel.OPENFOLD_3 and any(t.max_distance is not None for t in self.templates):
            raise ValueError("max_distance in templates is not supported by OpenFold-3")

        if any(t.max_distance is not None for t in self.templates) and not self.use_potentials:
            raise ValueError("use_potentials must be True when any template specifies max_distance")

        boltz_models = {CofoldingModel.BOLTZ_1, CofoldingModel.BOLTZ_2, CofoldingModel.BOLTZ_2_1, CofoldingModel.DECAF_BOLTZ}

        if self.use_potentials and self.model not in boltz_models:
            raise ValueError(f"use_potentials requires a Boltz model, got {self.model}")

        if self.contact_constraints and self.model not in boltz_models:
            raise ValueError(f"contact_constraints require a Boltz model, got {self.model}")

        if self.pocket_constraints and self.model not in boltz_models:
            raise ValueError(f"pocket_constraints require a Boltz model, got {self.model}")

        if self.bond_constraints and self.model != CofoldingModel.BOLTZ_2:
            raise ValueError(f"this workflow only supports bond_constraints with Boltz-2 currently, got {self.model}")

        if self.bond_constraints and (self.do_pose_refinement or self.compute_strain):
            raise ValueError("do_pose_refinement and compute_strain must be False when bond_constraints are set")

        if self.templates and self.model not in {CofoldingModel.BOLTZ_2, CofoldingModel.BOLTZ_2_1, CofoldingModel.OPENFOLD_3}:
            raise ValueError(f"templates require Boltz-2 or OpenFold-3, got {self.model}")

        if self.protein_binding_affinity_indices is not None and self.model != CofoldingModel.BOLTZ_2_1:
            raise ValueError(f"protein_binding_affinity_indices requires Boltz-2.1, got {self.model}")

        if self.model == CofoldingModel.OPENFOLD_3 and any(seq.cyclic for seq in self.initial_protein_sequences if hasattr(seq, "cyclic")):
            raise ValueError("OpenFold-3 does not support cyclic proteins")

        if self.protonation_method is None and self.do_pose_refinement:
            raise ValueError("do_pose_refinement requires a protonation_method")

        return self
