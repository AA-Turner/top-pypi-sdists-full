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
    ESMFOLD_2 = "esmfold_2"
    ESMFOLD_2_FAST = "esmfold_2_fast"


ESMFOLD_2_MODELS = frozenset({CofoldingModel.ESMFOLD_2, CofoldingModel.ESMFOLD_2_FAST})


class Token(BaseModel):
    """Either an atom in a ligand or a residue in a protein or nucleotide chain.

    Attributes:
        input_type: kind of input containing the token
        input_index: index of the input containing the token
        token_index: token position within the input
        atom_name: atom name for an atom-level token, if specified
    """

    input_type: Literal["ligand", "protein", "dna", "rna"]
    input_index: int
    token_index: int
    atom_name: str | None = None


class ContactConstraint(BaseModel):
    """Contact constraint to be used for prediction.

    Attributes:
        token_1: first token in the contact
        token_2: second token in the contact
        max_distance: maximum allowed contact distance, in Å
        force: use potentials to enforce the contact when true
    """

    token_1: Token
    token_2: Token
    max_distance: float  # Å
    force: bool = False  # Whether to use potentials to enforce the constraint


class PocketConstraint(BaseModel):
    """Pocket constraint to be used for prediction.

    Attributes:
        input_type: kind of input containing the pocket
        input_index: index of the input containing the token
        contacts: tokens constrained to contact the pocket
        max_distance: maximum allowed contact distance, in Å
        force: use potentials to enforce the pocket constraint when true
    """

    input_type: Literal["ligand", "protein", "dna", "rna"]
    input_index: int
    contacts: list[Token]
    max_distance: float  # Å
    force: bool = False  # Whether to use potentials to enforce the constraint


class BondConstraint(BaseModel):
    """Covalent bond constraint to be used for prediction (Boltz-2 and ESMFold2 only).

    Attributes:
        atom_1: first atom in the bond
        atom_2: second atom in the bond
    """

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

    Attributes:
        protein: PDB structure of protein, or UUID of PDB record in Rowan
        max_distance: maximum allowed deviation from the template, in Å; if set,
            the constraint is enforced with a potential
    """

    protein: PDB | UUID
    max_distance: float | None = None  # Å


class CofoldingScores(BaseModel):
    """Store confidence scores from a cofolding prediction.

    Attributes:
        confidence_score: overall model confidence score
        ptm: predicted template modeling score
        iptm: interface predicted template modeling score
        avg_lddt: average predicted local distance difference test score
    """

    confidence_score: Annotated[float, AfterValidator(round_float(3))]
    ptm: Annotated[float, AfterValidator(round_float(3))]  # predicted template modeling score
    iptm: Annotated[float, AfterValidator(round_float(3))]  # interface predicted template modeling score
    avg_lddt: Annotated[float, AfterValidator(round_float(3))]


class AffinityScore(BaseModel):
    """Store affinity predictions for a cofolding result.

    Attributes:
        pred_value: primary predicted affinity value
        probability_binary: primary binary binding probability
        pred_value1: first additional predicted affinity value
        probability_binary1: first additional binary binding probability
        pred_value2: second additional predicted affinity value
        probability_binary2: second additional binary binding probability
        binding_confidence: confidence in predicted binding
        optimization_score: score used to rank the prediction
    """

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

    Attributes:
        affinity_score: affinity score
        lddt: local distance different test result
        predicted_structure_uuid: UUID of the predicted structure
        scores: output cofolding scores
        pose: UUID of the calculation pose
        posebusters_valid: indicates that the predicted pose passes PoseBusters checks
        strain: strain of the ligand, in kcal/mol
        mmgbsa_score: MM/GBSA binding energy of the pose, in kcal/mol
        predicted_refined_structure_uuid: UUID of the predicted structure after refinement, when available
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
    """Workflow for predicting structures.

    Especially protein structures. At least one biological sequence is required.

    Attributes:
        initial_protein_sequences: protein sequences of interest
        initial_dna_sequences: DNA sequences of interest
        initial_rna_sequences: RNA sequences of interest
        initial_smiles_list: SMILES strings of interest
        ligand_binding_affinity_index: index selecting which ligand affinity to evaluate
        protein_binding_affinity_indices: indices selecting which protein sequences to evaluate binding affinity for

        use_msa_server: use the MSA server when true
        use_templates_server: use the templates server when true
        use_potentials: use potentials (inference-time steering) with Boltz when true
        contact_constraints: Boltz contact constraints
        pocket_constraints: Boltz pocket constraints
        bond_constraints: covalent bond constraints (Boltz-2 and ESMFold2 only)
        templates: structural templates to guide prediction (Boltz-2 only)
        protonation_method: method used to protonate polymers; `None` skips protonation
            (incompatible with `do_pose_refinement`)

        pH: pH value used for protonation
        do_pose_refinement: optimize non-rotatable bonds in output poses when true
            (incompatible with `bond_constraints`)

        compute_strain: compute the strain of the pose (if pose_refinement is
            enabled; incompatible with `bond_constraints`)

        num_samples: number of samples generated for prediction
        model: which cofolding model to use
        cofolding_results: per diffusion sample outputs, grouped together

        affinity_score: deprecated top-level affinity score
        lddt: deprecated top-level local confidence values
        predicted_structure_uuid: deprecated top-level predicted structure identifier
        scores: deprecated top-level confidence scores
        pose: deprecated top-level pose identifier
        posebusters_valid: deprecated top-level PoseBusters validity flag
        strain: deprecated top-level strain estimate, in kcal/mol
        predicted_refined_structure_uuid: deprecated top-level refined structure identifier
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

        if self.bond_constraints and self.model != CofoldingModel.BOLTZ_2 and self.model not in ESMFOLD_2_MODELS:
            raise ValueError(f"this workflow only supports bond_constraints with Boltz-2 or ESMFold2 currently, got {self.model}")

        if self.bond_constraints and (self.do_pose_refinement or self.compute_strain):
            raise ValueError("do_pose_refinement and compute_strain must be False when bond_constraints are set")

        if self.templates and self.model not in {CofoldingModel.BOLTZ_2, CofoldingModel.BOLTZ_2_1, CofoldingModel.OPENFOLD_3}:
            raise ValueError(f"templates require Boltz-2 or OpenFold-3, got {self.model}")

        if self.protein_binding_affinity_indices is not None and self.model != CofoldingModel.BOLTZ_2_1:
            raise ValueError(f"protein_binding_affinity_indices requires Boltz-2.1, got {self.model}")

        if self.model == CofoldingModel.OPENFOLD_3 and any(seq.cyclic for seq in self.initial_protein_sequences if hasattr(seq, "cyclic")):
            raise ValueError("OpenFold-3 does not support cyclic proteins")

        if self.model in ESMFOLD_2_MODELS and any(seq.cyclic for seq in self.initial_protein_sequences if hasattr(seq, "cyclic")):
            raise ValueError("ESMFold2 does not support cyclic proteins")

        if self.protonation_method is None and self.do_pose_refinement:
            raise ValueError("do_pose_refinement requires a protonation_method")

        return self
