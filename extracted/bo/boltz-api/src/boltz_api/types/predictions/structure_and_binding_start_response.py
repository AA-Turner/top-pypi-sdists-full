# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "StructureAndBindingStartResponse",
    "Error",
    "Input",
    "InputEntity",
    "InputEntityBoltz2ProteinEntityResponse",
    "InputEntityBoltz2ProteinEntityResponseModification",
    "InputEntityBoltz2ProteinEntityResponseMsa",
    "InputEntityBoltz2ProteinEntityResponseMsaBoltz2CustomMsaResponse",
    "InputEntityBoltz2ProteinEntityResponseMsaBoltz2CustomMsaResponseSource",
    "InputEntityBoltz2ProteinEntityResponseMsaBoltz2EmptyMsaResponse",
    "InputEntityRnaEntityResponse",
    "InputEntityRnaEntityResponseModification",
    "InputEntityDnaEntityResponse",
    "InputEntityDnaEntityResponseModification",
    "InputEntityLigandCcdEntityResponse",
    "InputEntityLigandSmilesEntityResponse",
    "InputEntityGlycanEntityResponse",
    "InputEntityGlycanEntityResponseBond",
    "InputEntityGlycanEntityResponseBondAtom1",
    "InputEntityGlycanEntityResponseBondAtom2",
    "InputEntityGlycanEntityResponseResidue",
    "InputBinding",
    "InputBindingLigandProteinBindingResponse",
    "InputBindingProteinProteinBindingResponse",
    "InputBond",
    "InputBondAtom1",
    "InputBondAtom1PolymerAtomResponse",
    "InputBondAtom1CcdAtomResponse",
    "InputBondAtom1SmilesAtomResponse",
    "InputBondAtom1LigandAtomResponse",
    "InputBondAtom2",
    "InputBondAtom2PolymerAtomResponse",
    "InputBondAtom2CcdAtomResponse",
    "InputBondAtom2SmilesAtomResponse",
    "InputBondAtom2LigandAtomResponse",
    "InputConstraint",
    "InputConstraintPocketConstraintResponse",
    "InputConstraintContactConstraintResponse",
    "InputConstraintContactConstraintResponseToken1",
    "InputConstraintContactConstraintResponseToken1PolymerContactTokenResponse",
    "InputConstraintContactConstraintResponseToken1LigandContactTokenResponse",
    "InputConstraintContactConstraintResponseToken2",
    "InputConstraintContactConstraintResponseToken2PolymerContactTokenResponse",
    "InputConstraintContactConstraintResponseToken2LigandContactTokenResponse",
    "InputModelOptions",
    "InputTemplate",
    "InputTemplateTemplateChain",
    "InputTemplateTemplateStructure",
    "Output",
    "OutputAllSampleResult",
    "OutputAllSampleResultMetrics",
    "OutputAllSampleResultStructure",
    "OutputAllSampleResultLigandStructure",
    "OutputBestSample",
    "OutputBestSampleMetrics",
    "OutputBestSampleStructure",
    "OutputBestSampleLigandStructure",
    "OutputArchive",
    "OutputBindingMetrics",
    "OutputBindingMetricsLigandProteinBindingMetrics",
    "OutputBindingMetricsProteinProteinBindingMetrics",
]


class Error(BaseModel):
    """Error details when failed"""

    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class InputEntityBoltz2ProteinEntityResponseModification(BaseModel):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: int
    """0-based index of the residue to modify"""

    type: Literal["ccd"]
    """Modification format. Only CCD polymer modifications are supported."""

    value: str
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class InputEntityBoltz2ProteinEntityResponseMsaBoltz2CustomMsaResponseSource(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class InputEntityBoltz2ProteinEntityResponseMsaBoltz2CustomMsaResponse(BaseModel):
    """Use a user-provided MSA for this protein entity.

    If any protein entity uses a custom MSA, every other protein entity must use either custom or empty MSA; automatic MSA generation cannot be mixed with custom MSAs in the same request.
    """

    format: Literal["a3m", "csv"]
    """Custom MSA file format.

    Base64 uploads must use media_type text/x-a3m for A3M or text/csv for CSV.
    """

    source: InputEntityBoltz2ProteinEntityResponseMsaBoltz2CustomMsaResponseSource

    type: Literal["custom"]


class InputEntityBoltz2ProteinEntityResponseMsaBoltz2EmptyMsaResponse(BaseModel):
    """Run this protein entity in single-sequence mode without an MSA.

    Use this for chains that should not use automatic MSA generation, including non-homologous chains in a request that also includes custom MSAs.
    """

    type: Literal["empty"]


InputEntityBoltz2ProteinEntityResponseMsa: TypeAlias = Union[
    InputEntityBoltz2ProteinEntityResponseMsaBoltz2CustomMsaResponse,
    InputEntityBoltz2ProteinEntityResponseMsaBoltz2EmptyMsaResponse,
]


class InputEntityBoltz2ProteinEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[InputEntityBoltz2ProteinEntityResponseModification]] = None
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """

    msa: Optional[InputEntityBoltz2ProteinEntityResponseMsa] = None
    """Optional protein MSA control.

    Omit msa on all protein entities to use automatic MSA generation. Use custom for
    user-provided A3M/CSV files, or empty for single-sequence mode. Custom MSA and
    automatic MSA cannot be mixed in one request.
    """


class InputEntityRnaEntityResponseModification(BaseModel):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: int
    """0-based index of the residue to modify"""

    type: Literal["ccd"]
    """Modification format. Only CCD polymer modifications are supported."""

    value: str
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class InputEntityRnaEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["rna"]

    value: str
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[InputEntityRnaEntityResponseModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputEntityDnaEntityResponseModification(BaseModel):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: int
    """0-based index of the residue to modify"""

    type: Literal["ccd"]
    """Modification format. Only CCD polymer modifications are supported."""

    value: str
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class InputEntityDnaEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["dna"]

    value: str
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[InputEntityDnaEntityResponseModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputEntityLigandCcdEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_ccd"]

    value: str
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class InputEntityLigandSmilesEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_smiles"]

    value: str
    """SMILES string representing the ligand"""


class InputEntityGlycanEntityResponseBondAtom1(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class InputEntityGlycanEntityResponseBondAtom2(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class InputEntityGlycanEntityResponseBond(BaseModel):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: InputEntityGlycanEntityResponseBondAtom1

    atom2: InputEntityGlycanEntityResponseBondAtom2


class InputEntityGlycanEntityResponseResidue(BaseModel):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class InputEntityGlycanEntityResponse(BaseModel):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[InputEntityGlycanEntityResponseBond]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[InputEntityGlycanEntityResponseResidue]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


InputEntity: TypeAlias = Union[
    InputEntityBoltz2ProteinEntityResponse,
    InputEntityRnaEntityResponse,
    InputEntityDnaEntityResponse,
    InputEntityLigandCcdEntityResponse,
    InputEntityLigandSmilesEntityResponse,
    InputEntityGlycanEntityResponse,
]


class InputBindingLigandProteinBindingResponse(BaseModel):
    binder_chain_id: str
    """
    Chain ID of the ligand binder (must have exactly 1 copy, at most 2048 heavy
    atoms, and only ligands+proteins in entities)
    """

    type: Literal["ligand_protein_binding"]


class InputBindingProteinProteinBindingResponse(BaseModel):
    binder_chain_ids: List[str]
    """Chain IDs of the protein binders"""

    type: Literal["protein_protein_binding"]


InputBinding: TypeAlias = Union[InputBindingLigandProteinBindingResponse, InputBindingProteinProteinBindingResponse]


class InputBondAtom1PolymerAtomResponse(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class InputBondAtom1CcdAtomResponse(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class InputBondAtom1SmilesAtomResponse(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class InputBondAtom1LigandAtomResponse(BaseModel):
    """
    Atom reference for a single-residue ligand_ccd or an explicitly atom-mapped SMILES ligand. Glycan bonds use ccd_atom; new SMILES bonds should use smiles_atom.
    """

    atom_name: str
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: str
    """Chain ID containing the atom"""

    type: Literal["ligand_atom"]


InputBondAtom1: TypeAlias = Union[
    InputBondAtom1PolymerAtomResponse,
    InputBondAtom1CcdAtomResponse,
    InputBondAtom1SmilesAtomResponse,
    InputBondAtom1LigandAtomResponse,
]


class InputBondAtom2PolymerAtomResponse(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class InputBondAtom2CcdAtomResponse(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class InputBondAtom2SmilesAtomResponse(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class InputBondAtom2LigandAtomResponse(BaseModel):
    """
    Atom reference for a single-residue ligand_ccd or an explicitly atom-mapped SMILES ligand. Glycan bonds use ccd_atom; new SMILES bonds should use smiles_atom.
    """

    atom_name: str
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: str
    """Chain ID containing the atom"""

    type: Literal["ligand_atom"]


InputBondAtom2: TypeAlias = Union[
    InputBondAtom2PolymerAtomResponse,
    InputBondAtom2CcdAtomResponse,
    InputBondAtom2SmilesAtomResponse,
    InputBondAtom2LigandAtomResponse,
]


class InputBond(BaseModel):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: InputBondAtom1
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: InputBondAtom2
    """Atom reference for a specific CCD residue in a glycan graph."""


class InputConstraintPocketConstraintResponse(BaseModel):
    """Constrains the binder to interact with specific pocket residues on the target."""

    binder_chain_id: str
    """Chain ID of the binder molecule"""

    contact_residues: Dict[str, List[int]]
    """Binding pocket residues keyed by chain ID.

    Each key is a chain ID (e.g. "A") and the value is an array of 0-indexed residue
    indices that define the pocket on that chain.
    """

    max_distance_angstrom: float
    """Maximum allowed distance in Angstroms between binder and pocket residues.

    Typical range: 4-8 A.
    """

    type: Literal["pocket"]

    force: Optional[bool] = None
    """Whether to force the constraint"""


class InputConstraintContactConstraintResponseToken1PolymerContactTokenResponse(BaseModel):
    chain_id: str
    """Chain ID"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_contact"]


class InputConstraintContactConstraintResponseToken1LigandContactTokenResponse(BaseModel):
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    atom_name: str
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: str
    """Chain ID"""

    type: Literal["ligand_contact"]


InputConstraintContactConstraintResponseToken1: TypeAlias = Union[
    InputConstraintContactConstraintResponseToken1PolymerContactTokenResponse,
    InputConstraintContactConstraintResponseToken1LigandContactTokenResponse,
]


class InputConstraintContactConstraintResponseToken2PolymerContactTokenResponse(BaseModel):
    chain_id: str
    """Chain ID"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_contact"]


class InputConstraintContactConstraintResponseToken2LigandContactTokenResponse(BaseModel):
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    atom_name: str
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: str
    """Chain ID"""

    type: Literal["ligand_contact"]


InputConstraintContactConstraintResponseToken2: TypeAlias = Union[
    InputConstraintContactConstraintResponseToken2PolymerContactTokenResponse,
    InputConstraintContactConstraintResponseToken2LigandContactTokenResponse,
]


class InputConstraintContactConstraintResponse(BaseModel):
    """
    Maximum-distance contact constraint between two polymer residues or ligand atoms.
    """

    max_distance_angstrom: float
    """Maximum distance in Angstroms"""

    token1: InputConstraintContactConstraintResponseToken1
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    token2: InputConstraintContactConstraintResponseToken2
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    type: Literal["contact"]

    force: Optional[bool] = None
    """Whether to force the constraint"""


InputConstraint: TypeAlias = Union[InputConstraintPocketConstraintResponse, InputConstraintContactConstraintResponse]


class InputModelOptions(BaseModel):
    recycling_steps: Optional[int] = None
    """The number of recycling steps to use for prediction. Default is 3."""

    sampling_steps: Optional[int] = None
    """The number of sampling steps to use for prediction. Default is 200."""

    step_scale: Optional[float] = None
    """Diffusion step scale (temperature).

    Controls sampling diversity — higher values produce more varied structures.
    Default is 1.638.
    """


class InputTemplateTemplateChain(BaseModel):
    """
    Mapping from one request chain to the corresponding chain in the template structure file.
    """

    input_chain_id: str
    """Chain ID in this prediction request"""

    template_chain_id: str
    """Corresponding chain ID in the template structure file"""


class InputTemplateTemplateStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class InputTemplate(BaseModel):
    """
    Template structure used as an inference-time guide for Boltz-2.1 protein-chain geometry. Provide a CIF or PDB file from an HTTPS URL or base64 upload.
    """

    template_chains: List[InputTemplateTemplateChain]
    """Request-to-template chain mappings.

    Each input_chain_id and template_chain_id must be unique within this template.
    """

    template_structure: InputTemplateTemplateStructure

    force_threshold_angstroms: Optional[float] = None
    """Force the template reference potential with this distance threshold in
    angstroms.

    Omit to use the template without force.
    """


class Input(BaseModel):
    """Prediction input (null if data deleted)"""

    entities: List[InputEntity]
    """
    Entities (proteins, RNA, DNA, ligands, and glycans) forming the complex to
    predict. Order determines chain assignment.
    """

    binding: Optional[InputBinding] = None

    bonds: Optional[List[InputBond]] = None
    """Request-level covalent bonds between atoms.

    Use ccd_atom with a glycan residue ID, smiles_atom with a numeric SMILES
    atom-map, or ligand_atom for a single-residue ligand. Internal glycan bonds
    belong in the glycan entity bonds field.
    """

    constraints: Optional[List[InputConstraint]] = None
    """Structural constraints (pocket and contact).

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    api_model_options: Optional[InputModelOptions] = FieldInfo(alias="model_options", default=None)

    num_samples: Optional[int] = None
    """Number of structure samples to generate (1-10)"""

    templates: Optional[List[InputTemplate]] = None
    """Template structure files to guide protein-chain prediction.

    Supports up to 4 CIF or PDB templates from HTTPS URLs or base64 uploads. Use
    template_chains to map request chains to template-file chains.
    """


class OutputAllSampleResultMetrics(BaseModel):
    complex_ipde: float
    """Complex interface predicted distance error. Lower is better."""

    complex_iplddt: float
    """Complex interface pLDDT (0-1 float). Confidence at inter-chain interfaces."""

    complex_pde: float
    """Complex predicted distance error. Lower is better."""

    complex_plddt: float
    """Complex pLDDT (0-1 float). Per-residue confidence averaged over the complex."""

    iptm: float
    """Interface predicted TM score (0-1). Confidence in domain interfaces."""

    ligand_iptm: float
    """Ligand interface pTM (0-1). Only present when ligands are included."""

    protein_iptm: float
    """Protein-protein interface pTM (0-1). Only present for multi-protein complexes."""

    ptm: float
    """Predicted TM score (0-1). Global structure quality."""

    structure_confidence: float
    """Overall structure confidence (0-1)."""


class OutputAllSampleResultStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class OutputAllSampleResultLigandStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class OutputAllSampleResult(BaseModel):
    metrics: OutputAllSampleResultMetrics

    structure: OutputAllSampleResultStructure

    ligand_structure: Optional[OutputAllSampleResultLigandStructure] = None


class OutputBestSampleMetrics(BaseModel):
    complex_ipde: float
    """Complex interface predicted distance error. Lower is better."""

    complex_iplddt: float
    """Complex interface pLDDT (0-1 float). Confidence at inter-chain interfaces."""

    complex_pde: float
    """Complex predicted distance error. Lower is better."""

    complex_plddt: float
    """Complex pLDDT (0-1 float). Per-residue confidence averaged over the complex."""

    iptm: float
    """Interface predicted TM score (0-1). Confidence in domain interfaces."""

    ligand_iptm: float
    """Ligand interface pTM (0-1). Only present when ligands are included."""

    protein_iptm: float
    """Protein-protein interface pTM (0-1). Only present for multi-protein complexes."""

    ptm: float
    """Predicted TM score (0-1). Global structure quality."""

    structure_confidence: float
    """Overall structure confidence (0-1)."""


class OutputBestSampleStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class OutputBestSampleLigandStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class OutputBestSample(BaseModel):
    metrics: OutputBestSampleMetrics

    structure: OutputBestSampleStructure

    ligand_structure: Optional[OutputBestSampleLigandStructure] = None


class OutputArchive(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class OutputBindingMetricsLigandProteinBindingMetrics(BaseModel):
    binding_confidence: float
    """Confidence that binding occurs (0-1). Primary metric for hit discovery."""

    optimization_score: float
    """Binding strength ranking score for lead optimization.

    Higher values indicate stronger predicted binding.
    """

    type: Literal["ligand_protein_binding_metrics"]


class OutputBindingMetricsProteinProteinBindingMetrics(BaseModel):
    binding_confidence: float
    """Confidence that binding occurs (0-1). Primary metric for hit discovery."""

    type: Literal["protein_protein_binding_metrics"]


OutputBindingMetrics: TypeAlias = Union[
    OutputBindingMetricsLigandProteinBindingMetrics, OutputBindingMetricsProteinProteinBindingMetrics
]


class Output(BaseModel):
    """Prediction output when succeeded"""

    all_sample_results: List[OutputAllSampleResult]
    """Per-sample structure results"""

    best_sample: OutputBestSample

    archive: Optional[OutputArchive] = None

    binding_metrics: Optional[OutputBindingMetrics] = None


class StructureAndBindingStartResponse(BaseModel):
    id: str
    """Unique prediction identifier"""

    completed_at: Optional[datetime] = None

    created_at: datetime

    data_deleted_at: Optional[datetime] = None
    """When the input/output data was deleted, or null if still available"""

    error: Optional[Error] = None
    """Error details when failed"""

    expires_at: Optional[datetime] = None
    """When this resource and its associated data will be permanently deleted.

    Null while still in progress.
    """

    input: Optional[Input] = None
    """Prediction input (null if data deleted)"""

    livemode: bool
    """Whether this resource was created with a live API key."""

    model: Literal["boltz-2.1"]
    """Model used for prediction"""

    output: Optional[Output] = None
    """Prediction output when succeeded"""

    started_at: Optional[datetime] = None

    status: Literal["pending", "running", "succeeded", "failed"]

    version: str
    """Model version used for prediction"""

    workspace_id: str
    """Workspace ID"""

    idempotency_key: Optional[str] = None
    """Client-provided idempotency key"""
