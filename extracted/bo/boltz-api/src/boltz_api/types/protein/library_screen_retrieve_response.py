# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "LibraryScreenRetrieveResponse",
    "Error",
    "Input",
    "InputProteins",
    "InputTarget",
    "InputTargetStructureTemplateTargetResponse",
    "InputTargetStructureTemplateTargetResponseChainSelection",
    "InputTargetStructureTemplateTargetResponseChainSelectionStructureTemplateTargetPolymerChainSpec",
    "InputTargetStructureTemplateTargetResponseChainSelectionStructureTemplateTargetLigandChainSpec",
    "InputTargetStructureTemplateTargetResponseStructure",
    "InputTargetNoTemplateTargetResponse",
    "InputTargetNoTemplateTargetResponseEntity",
    "InputTargetNoTemplateTargetResponseEntityProteinEntityResponse",
    "InputTargetNoTemplateTargetResponseEntityProteinEntityResponseModification",
    "InputTargetNoTemplateTargetResponseEntityRnaEntityResponse",
    "InputTargetNoTemplateTargetResponseEntityRnaEntityResponseModification",
    "InputTargetNoTemplateTargetResponseEntityDnaEntityResponse",
    "InputTargetNoTemplateTargetResponseEntityDnaEntityResponseModification",
    "InputTargetNoTemplateTargetResponseEntityLigandCcdEntityResponse",
    "InputTargetNoTemplateTargetResponseEntityLigandSmilesEntityResponse",
    "InputTargetNoTemplateTargetResponseEntityGlycanEntityResponse",
    "InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBond",
    "InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBondAtom1",
    "InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBondAtom2",
    "InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseResidue",
    "InputTargetNoTemplateTargetResponseBond",
    "InputTargetNoTemplateTargetResponseBondAtom1",
    "InputTargetNoTemplateTargetResponseBondAtom1PolymerAtomResponse",
    "InputTargetNoTemplateTargetResponseBondAtom1CcdAtomResponse",
    "InputTargetNoTemplateTargetResponseBondAtom1SmilesAtomResponse",
    "InputTargetNoTemplateTargetResponseBondAtom1LigandAtomResponse",
    "InputTargetNoTemplateTargetResponseBondAtom2",
    "InputTargetNoTemplateTargetResponseBondAtom2PolymerAtomResponse",
    "InputTargetNoTemplateTargetResponseBondAtom2CcdAtomResponse",
    "InputTargetNoTemplateTargetResponseBondAtom2SmilesAtomResponse",
    "InputTargetNoTemplateTargetResponseBondAtom2LigandAtomResponse",
    "InputTargetNoTemplateTargetResponseConstraint",
    "InputTargetNoTemplateTargetResponseConstraintPocketConstraintResponse",
    "InputTargetNoTemplateTargetResponseConstraintContactConstraintResponse",
    "InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1",
    "InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1PolymerContactTokenResponse",
    "InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1LigandContactTokenResponse",
    "InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2",
    "InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2PolymerContactTokenResponse",
    "InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2LigandContactTokenResponse",
    "Progress",
]


class Error(BaseModel):
    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class InputProteins(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class InputTargetStructureTemplateTargetResponseChainSelectionStructureTemplateTargetPolymerChainSpec(BaseModel):
    """
    Per-chain specification for a polymer (protein/RNA/DNA) chain in a structure template target.
    """

    chain_type: Literal["polymer"]

    crop_residues: Union[List[int], Literal["all"]]
    """
    0-indexed residue indices to retain from this chain, or 'all' to keep all
    residues. Residues not listed are excluded from the pipeline run.
    """

    epitope_residues: Optional[List[int]] = None
    """0-indexed residue indices where binder contact is desired (the epitope).

    All indices must be present in crop_residues and must not overlap
    non_binding_residues.
    """

    flexible_residues: Optional[List[int]] = None
    """0-indexed residue indices allowed to move during design (e.g.

    flexible loop regions). All indices must be present in crop_residues.
    """

    non_binding_residues: Optional[List[int]] = None
    """0-indexed residue indices where binder contact should be discouraged.

    All indices must be present in crop_residues and must not overlap
    epitope_residues.
    """


class InputTargetStructureTemplateTargetResponseChainSelectionStructureTemplateTargetLigandChainSpec(BaseModel):
    """Per-chain specification for a ligand chain in a structure template target.

    The full ligand is always included.
    """

    chain_type: Literal["ligand"]


InputTargetStructureTemplateTargetResponseChainSelection: TypeAlias = Union[
    InputTargetStructureTemplateTargetResponseChainSelectionStructureTemplateTargetPolymerChainSpec,
    InputTargetStructureTemplateTargetResponseChainSelectionStructureTemplateTargetLigandChainSpec,
]


class InputTargetStructureTemplateTargetResponseStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class InputTargetStructureTemplateTargetResponse(BaseModel):
    """Target defined by an uploaded 3D structure (CIF or PDB file).

    Only chains included in chain_selection are used.
    """

    chain_selection: Dict[str, InputTargetStructureTemplateTargetResponseChainSelection]
    """Chains selected from the uploaded structure, keyed by chain ID.

    Only chains listed here are included in the pipeline run — any chains omitted
    from this mapping are ignored. Each value defines which residues to keep, which
    are epitope residues, which are non-binding residues, and which are flexible.
    """

    structure: InputTargetStructureTemplateTargetResponseStructure

    type: Literal["structure_template"]


class InputTargetNoTemplateTargetResponseEntityProteinEntityResponseModification(BaseModel):
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


class InputTargetNoTemplateTargetResponseEntityProteinEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[InputTargetNoTemplateTargetResponseEntityProteinEntityResponseModification]] = None
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputTargetNoTemplateTargetResponseEntityRnaEntityResponseModification(BaseModel):
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


class InputTargetNoTemplateTargetResponseEntityRnaEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["rna"]

    value: str
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[InputTargetNoTemplateTargetResponseEntityRnaEntityResponseModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputTargetNoTemplateTargetResponseEntityDnaEntityResponseModification(BaseModel):
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


class InputTargetNoTemplateTargetResponseEntityDnaEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["dna"]

    value: str
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[InputTargetNoTemplateTargetResponseEntityDnaEntityResponseModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputTargetNoTemplateTargetResponseEntityLigandCcdEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_ccd"]

    value: str
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class InputTargetNoTemplateTargetResponseEntityLigandSmilesEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_smiles"]

    value: str
    """SMILES string representing the ligand"""


class InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBondAtom1(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBondAtom2(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBond(BaseModel):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBondAtom1

    atom2: InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBondAtom2


class InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseResidue(BaseModel):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class InputTargetNoTemplateTargetResponseEntityGlycanEntityResponse(BaseModel):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseBond]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[InputTargetNoTemplateTargetResponseEntityGlycanEntityResponseResidue]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


InputTargetNoTemplateTargetResponseEntity: TypeAlias = Union[
    InputTargetNoTemplateTargetResponseEntityProteinEntityResponse,
    InputTargetNoTemplateTargetResponseEntityRnaEntityResponse,
    InputTargetNoTemplateTargetResponseEntityDnaEntityResponse,
    InputTargetNoTemplateTargetResponseEntityLigandCcdEntityResponse,
    InputTargetNoTemplateTargetResponseEntityLigandSmilesEntityResponse,
    InputTargetNoTemplateTargetResponseEntityGlycanEntityResponse,
]


class InputTargetNoTemplateTargetResponseBondAtom1PolymerAtomResponse(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class InputTargetNoTemplateTargetResponseBondAtom1CcdAtomResponse(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class InputTargetNoTemplateTargetResponseBondAtom1SmilesAtomResponse(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class InputTargetNoTemplateTargetResponseBondAtom1LigandAtomResponse(BaseModel):
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


InputTargetNoTemplateTargetResponseBondAtom1: TypeAlias = Union[
    InputTargetNoTemplateTargetResponseBondAtom1PolymerAtomResponse,
    InputTargetNoTemplateTargetResponseBondAtom1CcdAtomResponse,
    InputTargetNoTemplateTargetResponseBondAtom1SmilesAtomResponse,
    InputTargetNoTemplateTargetResponseBondAtom1LigandAtomResponse,
]


class InputTargetNoTemplateTargetResponseBondAtom2PolymerAtomResponse(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class InputTargetNoTemplateTargetResponseBondAtom2CcdAtomResponse(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class InputTargetNoTemplateTargetResponseBondAtom2SmilesAtomResponse(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class InputTargetNoTemplateTargetResponseBondAtom2LigandAtomResponse(BaseModel):
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


InputTargetNoTemplateTargetResponseBondAtom2: TypeAlias = Union[
    InputTargetNoTemplateTargetResponseBondAtom2PolymerAtomResponse,
    InputTargetNoTemplateTargetResponseBondAtom2CcdAtomResponse,
    InputTargetNoTemplateTargetResponseBondAtom2SmilesAtomResponse,
    InputTargetNoTemplateTargetResponseBondAtom2LigandAtomResponse,
]


class InputTargetNoTemplateTargetResponseBond(BaseModel):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: InputTargetNoTemplateTargetResponseBondAtom1
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: InputTargetNoTemplateTargetResponseBondAtom2
    """Atom reference for a specific CCD residue in a glycan graph."""


class InputTargetNoTemplateTargetResponseConstraintPocketConstraintResponse(BaseModel):
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


class InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1PolymerContactTokenResponse(
    BaseModel
):
    chain_id: str
    """Chain ID"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_contact"]


class InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1LigandContactTokenResponse(BaseModel):
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


InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1: TypeAlias = Union[
    InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1PolymerContactTokenResponse,
    InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1LigandContactTokenResponse,
]


class InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2PolymerContactTokenResponse(
    BaseModel
):
    chain_id: str
    """Chain ID"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_contact"]


class InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2LigandContactTokenResponse(BaseModel):
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


InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2: TypeAlias = Union[
    InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2PolymerContactTokenResponse,
    InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2LigandContactTokenResponse,
]


class InputTargetNoTemplateTargetResponseConstraintContactConstraintResponse(BaseModel):
    """
    Maximum-distance contact constraint between two polymer residues or ligand atoms.
    """

    max_distance_angstrom: float
    """Maximum distance in Angstroms"""

    token1: InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken1
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    token2: InputTargetNoTemplateTargetResponseConstraintContactConstraintResponseToken2
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    type: Literal["contact"]

    force: Optional[bool] = None
    """Whether to force the constraint"""


InputTargetNoTemplateTargetResponseConstraint: TypeAlias = Union[
    InputTargetNoTemplateTargetResponseConstraintPocketConstraintResponse,
    InputTargetNoTemplateTargetResponseConstraintContactConstraintResponse,
]


class InputTargetNoTemplateTargetResponse(BaseModel):
    """Target defined by sequences only, without a 3D structure template"""

    entities: List[InputTargetNoTemplateTargetResponseEntity]
    """Entities (proteins, RNA, DNA, ligands) defining the target complex."""

    type: Literal["no_template"]

    bonds: Optional[List[InputTargetNoTemplateTargetResponseBond]] = None
    """Covalent bond constraints between atoms in the target complex.

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    constraints: Optional[List[InputTargetNoTemplateTargetResponseConstraint]] = None
    """Structural constraints (pocket and contact).

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    epitope_ligand_chains: Optional[List[str]] = None
    """Chain IDs of ligand entities that are part of the binding epitope.

    Ligands are marked as epitope in full (no residue-level selection).
    """

    epitope_residues: Optional[Dict[str, List[int]]] = None
    """Polymer chain residues where binder contact is desired (the epitope).

    Each key is a chain ID of a polymer entity, each value is an array of 0-indexed
    residue indices. Residues must not overlap non_binding_residues on the same
    chain.
    """

    non_binding_residues: Optional[Dict[str, List[int]]] = None
    """Polymer chain residues where binder contact should be discouraged.

    Each key is a chain ID of a polymer entity, each value is an array of 0-indexed
    residue indices. Residues must not overlap epitope_residues on the same chain.
    """


InputTarget: TypeAlias = Union[InputTargetStructureTemplateTargetResponse, InputTargetNoTemplateTargetResponse]


class Input(BaseModel):
    """Pipeline input (null if data deleted)"""

    proteins: InputProteins

    target: InputTarget
    """Target specification (structure template or template-free)"""


class Progress(BaseModel):
    num_proteins_failed: int
    """Number of accepted proteins that reached terminal failure during screening."""

    num_proteins_screened: int
    """Number of accepted proteins that produced usable screening results."""

    total_proteins_to_screen: int
    """Total number of proteins accepted into the screening run."""

    latest_result_id: Optional[str] = None
    """ID of the latest result"""


class LibraryScreenRetrieveResponse(BaseModel):
    """A protein library screening pipeline run"""

    id: str
    """Unique ProteinLibraryScreen identifier"""

    completed_at: Optional[datetime] = None

    created_at: datetime

    data_deleted_at: Optional[datetime] = None
    """When the input, output, and result data was permanently deleted.

    Null if data has not been deleted.
    """

    engine: Literal["boltzprot"]
    """Deprecated. Use pipeline instead."""

    engine_version: Literal["1.0"]
    """Deprecated. Use pipeline_version instead."""

    error: Optional[Error] = None

    input: Optional[Input] = None
    """Pipeline input (null if data deleted)"""

    livemode: bool
    """Whether this resource was created with a live API key."""

    pipeline: Literal["boltzprot"]
    """Pipeline used for protein library screen"""

    pipeline_version: Literal["1.0"]
    """Pipeline version used for protein library screen"""

    progress: Optional[Progress] = None

    started_at: Optional[datetime] = None

    status: Literal["pending", "running", "succeeded", "failed", "stopped"]

    stopped_at: Optional[datetime] = None

    workspace_id: str
    """Workspace ID"""

    idempotency_key: Optional[str] = None
    """Client-provided idempotency key"""
