# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "DesignStartResponse",
    "Error",
    "Input",
    "InputTarget",
    "InputTargetEntity",
    "InputTargetEntityProteinEntityResponse",
    "InputTargetEntityProteinEntityResponseModification",
    "InputTargetEntityGlycanEntityResponse",
    "InputTargetEntityGlycanEntityResponseBond",
    "InputTargetEntityGlycanEntityResponseBondAtom1",
    "InputTargetEntityGlycanEntityResponseBondAtom2",
    "InputTargetEntityGlycanEntityResponseResidue",
    "InputTargetBond",
    "InputTargetBondAtom1",
    "InputTargetBondAtom1PolymerAtomResponse",
    "InputTargetBondAtom1CcdAtomResponse",
    "InputTargetBondAtom1SmilesAtomResponse",
    "InputTargetBondAtom1LigandAtomResponse",
    "InputTargetBondAtom2",
    "InputTargetBondAtom2PolymerAtomResponse",
    "InputTargetBondAtom2CcdAtomResponse",
    "InputTargetBondAtom2SmilesAtomResponse",
    "InputTargetBondAtom2LigandAtomResponse",
    "InputTargetConstraint",
    "InputTargetConstraintPocketConstraintResponse",
    "InputTargetConstraintContactConstraintResponse",
    "InputTargetConstraintContactConstraintResponseToken1",
    "InputTargetConstraintContactConstraintResponseToken1PolymerContactTokenResponse",
    "InputTargetConstraintContactConstraintResponseToken1LigandContactTokenResponse",
    "InputTargetConstraintContactConstraintResponseToken2",
    "InputTargetConstraintContactConstraintResponseToken2PolymerContactTokenResponse",
    "InputTargetConstraintContactConstraintResponseToken2LigandContactTokenResponse",
    "InputMoleculeFilters",
    "InputMoleculeFiltersCustomFilter",
    "InputMoleculeFiltersCustomFilterLipinskiFilterResponse",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponse",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseFractionCsp3",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseMolLogp",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseMolWt",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumAromaticRings",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHAcceptors",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHDonors",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHeteroatoms",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumRings",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumRotatableBonds",
    "InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseTpsa",
    "InputMoleculeFiltersCustomFilterSmartsCustomFilterResponse",
    "InputMoleculeFiltersCustomFilterSmartsCatalogFilterResponse",
    "InputMoleculeFiltersCustomFilterSmilesRegexFilterResponse",
    "Progress",
]


class Error(BaseModel):
    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class InputTargetEntityProteinEntityResponseModification(BaseModel):
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


class InputTargetEntityProteinEntityResponse(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[InputTargetEntityProteinEntityResponseModification]] = None
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputTargetEntityGlycanEntityResponseBondAtom1(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class InputTargetEntityGlycanEntityResponseBondAtom2(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class InputTargetEntityGlycanEntityResponseBond(BaseModel):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: InputTargetEntityGlycanEntityResponseBondAtom1

    atom2: InputTargetEntityGlycanEntityResponseBondAtom2


class InputTargetEntityGlycanEntityResponseResidue(BaseModel):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class InputTargetEntityGlycanEntityResponse(BaseModel):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[InputTargetEntityGlycanEntityResponseBond]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[InputTargetEntityGlycanEntityResponseResidue]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


InputTargetEntity: TypeAlias = Union[InputTargetEntityProteinEntityResponse, InputTargetEntityGlycanEntityResponse]


class InputTargetBondAtom1PolymerAtomResponse(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class InputTargetBondAtom1CcdAtomResponse(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class InputTargetBondAtom1SmilesAtomResponse(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class InputTargetBondAtom1LigandAtomResponse(BaseModel):
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


InputTargetBondAtom1: TypeAlias = Union[
    InputTargetBondAtom1PolymerAtomResponse,
    InputTargetBondAtom1CcdAtomResponse,
    InputTargetBondAtom1SmilesAtomResponse,
    InputTargetBondAtom1LigandAtomResponse,
]


class InputTargetBondAtom2PolymerAtomResponse(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class InputTargetBondAtom2CcdAtomResponse(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class InputTargetBondAtom2SmilesAtomResponse(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class InputTargetBondAtom2LigandAtomResponse(BaseModel):
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


InputTargetBondAtom2: TypeAlias = Union[
    InputTargetBondAtom2PolymerAtomResponse,
    InputTargetBondAtom2CcdAtomResponse,
    InputTargetBondAtom2SmilesAtomResponse,
    InputTargetBondAtom2LigandAtomResponse,
]


class InputTargetBond(BaseModel):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: InputTargetBondAtom1
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: InputTargetBondAtom2
    """Atom reference for a specific CCD residue in a glycan graph."""


class InputTargetConstraintPocketConstraintResponse(BaseModel):
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


class InputTargetConstraintContactConstraintResponseToken1PolymerContactTokenResponse(BaseModel):
    chain_id: str
    """Chain ID"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_contact"]


class InputTargetConstraintContactConstraintResponseToken1LigandContactTokenResponse(BaseModel):
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


InputTargetConstraintContactConstraintResponseToken1: TypeAlias = Union[
    InputTargetConstraintContactConstraintResponseToken1PolymerContactTokenResponse,
    InputTargetConstraintContactConstraintResponseToken1LigandContactTokenResponse,
]


class InputTargetConstraintContactConstraintResponseToken2PolymerContactTokenResponse(BaseModel):
    chain_id: str
    """Chain ID"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_contact"]


class InputTargetConstraintContactConstraintResponseToken2LigandContactTokenResponse(BaseModel):
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


InputTargetConstraintContactConstraintResponseToken2: TypeAlias = Union[
    InputTargetConstraintContactConstraintResponseToken2PolymerContactTokenResponse,
    InputTargetConstraintContactConstraintResponseToken2LigandContactTokenResponse,
]


class InputTargetConstraintContactConstraintResponse(BaseModel):
    """
    Maximum-distance contact constraint between two polymer residues or ligand atoms.
    """

    max_distance_angstrom: float
    """Maximum distance in Angstroms"""

    token1: InputTargetConstraintContactConstraintResponseToken1
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    token2: InputTargetConstraintContactConstraintResponseToken2
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    type: Literal["contact"]

    force: Optional[bool] = None
    """Whether to force the constraint"""


InputTargetConstraint: TypeAlias = Union[
    InputTargetConstraintPocketConstraintResponse, InputTargetConstraintContactConstraintResponse
]


class InputTarget(BaseModel):
    """Target protein sequences for small molecule design or screening."""

    entities: List[InputTargetEntity]
    """Protein and glycan entities defining the target structure.

    At least one protein entity is required.
    """

    bonds: Optional[List[InputTargetBond]] = None
    """Covalent bond constraints between atoms in the target complex.

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    constraints: Optional[List[InputTargetConstraint]] = None
    """Structural constraints (pocket and contact).

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    pocket_residues: Optional[Dict[str, List[int]]] = None
    """Binding pocket residues, keyed by chain ID.

    Each key is a chain ID (e.g. "A") and the value is an array of 0-indexed residue
    indices that define the binding pocket on that chain. When provided, these
    residues guide pocket extraction and add a derived pocket constraint during
    affinity predictions. That derived constraint remains separate from any explicit
    pocket constraints in target.constraints. When omitted, the model auto-detects
    the pocket.
    """

    reference_ligands: Optional[List[str]] = None
    """
    Reference ligands as SMILES strings that help the model identify the binding
    pocket. When omitted, a set of drug-like default ligands is used for pocket
    detection.
    """

    type: Optional[Literal["no_template"]] = None
    """
    Target is defined directly by protein sequences rather than a structure
    template.
    """


class InputMoleculeFiltersCustomFilterLipinskiFilterResponse(BaseModel):
    """Lipinski's Rule of Five filter.

    Rejects molecules that violate drug-likeness criteria based on molecular weight, LogP, hydrogen bond donors, and hydrogen bond acceptors.
    """

    max_hba: float
    """Maximum number of hydrogen bond acceptors. Lipinski threshold: 10"""

    max_hbd: float
    """Maximum number of hydrogen bond donors. Lipinski threshold: 5"""

    max_logp: float
    """Maximum LogP. Lipinski threshold: 5"""

    max_mw: float
    """Maximum molecular weight (Da). Lipinski threshold: 500"""

    type: Literal["lipinski_filter"]

    allow_single_violation: Optional[bool] = None
    """If true, one rule violation is allowed (classic Rule of Five).

    Defaults to false (all rules must pass).
    """


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseFractionCsp3(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseMolLogp(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseMolWt(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumAromaticRings(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHAcceptors(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHDonors(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHeteroatoms(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumRings(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumRotatableBonds(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseTpsa(BaseModel):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: Optional[float] = None
    """Maximum allowed value (inclusive)"""

    min: Optional[float] = None
    """Minimum allowed value (inclusive)"""


class InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponse(BaseModel):
    """Filter molecules by RDKit molecular descriptors.

    Each descriptor is constrained to a min/max range. Only descriptors you provide are checked — omitted descriptors are unconstrained.
    """

    type: Literal["rdkit_descriptor_filter"]

    fraction_csp3: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseFractionCsp3] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    mol_logp: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseMolLogp] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    mol_wt: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseMolWt] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_aromatic_rings: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumAromaticRings] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_h_acceptors: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHAcceptors] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_h_donors: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHDonors] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_heteroatoms: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumHeteroatoms] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_rings: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumRings] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_rotatable_bonds: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseNumRotatableBonds] = None
    """Min/max range constraint for an RDKit molecular descriptor"""

    tpsa: Optional[InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponseTpsa] = None
    """Min/max range constraint for an RDKit molecular descriptor"""


class InputMoleculeFiltersCustomFilterSmartsCustomFilterResponse(BaseModel):
    """Filter molecules by custom SMARTS patterns.

    Molecules matching any pattern are rejected.
    """

    patterns: List[str]
    """SMARTS patterns. Molecules matching any pattern are rejected."""

    type: Literal["smarts_custom_filter"]


class InputMoleculeFiltersCustomFilterSmartsCatalogFilterResponse(BaseModel):
    """Filter molecules using a predefined SMARTS catalog of structural alerts."""

    catalog: Literal[
        "PAINS",
        "PAINS_A",
        "PAINS_B",
        "PAINS_C",
        "BRENK",
        "CHEMBL",
        "CHEMBL_BMS",
        "CHEMBL_Dundee",
        "CHEMBL_Glaxo",
        "CHEMBL_Inpharmatica",
        "CHEMBL_LINT",
        "CHEMBL_MLSMR",
        "CHEMBL_SureChEMBL",
        "NIH",
    ]
    """Predefined SMARTS catalog to apply.

    PAINS, BRENK, ChEMBL, and NIH catalogs reject known problematic substructures.
    """

    type: Literal["smarts_catalog_filter"]


class InputMoleculeFiltersCustomFilterSmilesRegexFilterResponse(BaseModel):
    """Filter molecules by regex patterns on their SMILES representation."""

    patterns: List[str]
    """Regex patterns applied to SMILES strings.

    Molecules matching any pattern are rejected.
    """

    type: Literal["smiles_regex_filter"]


InputMoleculeFiltersCustomFilter: TypeAlias = Union[
    InputMoleculeFiltersCustomFilterLipinskiFilterResponse,
    InputMoleculeFiltersCustomFilterRdkitDescriptorFilterResponse,
    InputMoleculeFiltersCustomFilterSmartsCustomFilterResponse,
    InputMoleculeFiltersCustomFilterSmartsCatalogFilterResponse,
    InputMoleculeFiltersCustomFilterSmilesRegexFilterResponse,
]


class InputMoleculeFilters(BaseModel):
    """Molecule filtering configuration.

    Controls both Boltz built-in SMARTS filtering and custom filters.
    """

    boltz_smarts_catalog_filter_level: Optional[Literal["recommended", "extra", "aggressive", "disabled"]] = None
    """
    Controls the stringency of Boltz's built-in SMARTS structural alert filtering,
    which removes molecules matching known problematic substructures. When omitted,
    small-molecule design and library screen use 'recommended', while Explore uses
    'disabled'. 'recommended': applies a curated set of alerts balancing safety and
    hit rate. 'extra': adds additional alerts beyond the recommended set for
    stricter filtering. 'aggressive': applies the most comprehensive alert set — may
    reject viable molecules. 'disabled': turns off Boltz SMARTS filtering entirely;
    only custom_filters will be applied.
    """

    custom_filters: Optional[List[InputMoleculeFiltersCustomFilter]] = None
    """Custom filters to apply. Molecules must pass all filters (AND logic)."""


class Input(BaseModel):
    """Pipeline input (null if data deleted)"""

    num_molecules: int
    """Number of molecules to generate. Must be between 10 and 1,000,000."""

    target: InputTarget
    """Target protein sequences for small molecule design or screening."""

    chemical_space: Optional[Literal["enamine_real", "none"]] = None
    """Chemical space to constrain generated molecules.

    Use 'enamine_real' for the Enamine REAL chemical space, 'wuxi_galaxi' for the
    WuXi GalaXi chemical space when enabled for your organization, or 'none' to
    disable chemical-space filtering.
    """

    idempotency_key: Optional[str] = None
    """Client-provided key to prevent duplicate submissions on retries"""

    molecule_filters: Optional[InputMoleculeFilters] = None
    """Molecule filtering configuration.

    Controls both Boltz built-in SMARTS filtering and custom filters.
    """

    workspace_id: Optional[str] = None
    """Target workspace ID (admin keys only; ignored for workspace keys)"""


class Progress(BaseModel):
    num_molecules_generated: int
    """Number of molecules generated so far"""

    total_molecules_to_generate: int
    """Total number of molecules requested"""

    latest_result_id: Optional[str] = None
    """ID of the most recently generated result"""


class DesignStartResponse(BaseModel):
    """A small molecule design pipeline run that generates novel molecules"""

    id: str
    """Unique SmDesignRun identifier"""

    completed_at: Optional[datetime] = None

    created_at: datetime

    data_deleted_at: Optional[datetime] = None
    """When the input, output, and result data was permanently deleted.

    Null if data has not been deleted.
    """

    engine: Literal["boltzmol"]
    """Deprecated. Use pipeline instead."""

    engine_version: Literal["1.0"]
    """Deprecated. Use pipeline_version instead."""

    error: Optional[Error] = None

    input: Optional[Input] = None
    """Pipeline input (null if data deleted)"""

    livemode: bool
    """Whether this resource was created with a live API key."""

    pipeline: Literal["boltzmol"]
    """Pipeline used for small molecule design"""

    pipeline_version: Literal["1.0"]
    """Pipeline version used for small molecule design"""

    progress: Optional[Progress] = None

    started_at: Optional[datetime] = None

    status: Literal["pending", "running", "succeeded", "failed", "stopped"]

    stopped_at: Optional[datetime] = None

    workspace_id: str
    """Workspace ID"""

    idempotency_key: Optional[str] = None
    """Client-provided idempotency key"""
