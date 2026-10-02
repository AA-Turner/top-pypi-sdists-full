# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = [
    "LibraryScreenStartParams",
    "Protein",
    "ProteinEntity",
    "ProteinEntityProteinEntity",
    "ProteinEntityProteinEntityModification",
    "ProteinEntityRnaEntity",
    "ProteinEntityRnaEntityModification",
    "ProteinEntityDnaEntity",
    "ProteinEntityDnaEntityModification",
    "ProteinEntityLigandCcdEntity",
    "ProteinEntityLigandSmilesEntity",
    "ProteinEntityGlycanEntity",
    "ProteinEntityGlycanEntityBond",
    "ProteinEntityGlycanEntityBondAtom1",
    "ProteinEntityGlycanEntityBondAtom2",
    "ProteinEntityGlycanEntityResidue",
    "Target",
    "TargetStructureTemplateTarget",
    "TargetStructureTemplateTargetChainSelection",
    "TargetStructureTemplateTargetChainSelectionStructureTemplateTargetPolymerChainSpec",
    "TargetStructureTemplateTargetChainSelectionStructureTemplateTargetLigandChainSpec",
    "TargetStructureTemplateTargetStructure",
    "TargetStructureTemplateTargetStructureURLSource",
    "TargetStructureTemplateTargetStructureCifBase64Source",
    "TargetNoTemplateTarget",
    "TargetNoTemplateTargetEntity",
    "TargetNoTemplateTargetEntityProteinEntity",
    "TargetNoTemplateTargetEntityProteinEntityModification",
    "TargetNoTemplateTargetEntityRnaEntity",
    "TargetNoTemplateTargetEntityRnaEntityModification",
    "TargetNoTemplateTargetEntityDnaEntity",
    "TargetNoTemplateTargetEntityDnaEntityModification",
    "TargetNoTemplateTargetEntityLigandCcdEntity",
    "TargetNoTemplateTargetEntityLigandSmilesEntity",
    "TargetNoTemplateTargetEntityGlycanEntity",
    "TargetNoTemplateTargetEntityGlycanEntityBond",
    "TargetNoTemplateTargetEntityGlycanEntityBondAtom1",
    "TargetNoTemplateTargetEntityGlycanEntityBondAtom2",
    "TargetNoTemplateTargetEntityGlycanEntityResidue",
    "TargetNoTemplateTargetBond",
    "TargetNoTemplateTargetBondAtom1",
    "TargetNoTemplateTargetBondAtom1PolymerAtom",
    "TargetNoTemplateTargetBondAtom1CcdAtom",
    "TargetNoTemplateTargetBondAtom1SmilesAtom",
    "TargetNoTemplateTargetBondAtom1LigandAtom",
    "TargetNoTemplateTargetBondAtom2",
    "TargetNoTemplateTargetBondAtom2PolymerAtom",
    "TargetNoTemplateTargetBondAtom2CcdAtom",
    "TargetNoTemplateTargetBondAtom2SmilesAtom",
    "TargetNoTemplateTargetBondAtom2LigandAtom",
    "TargetNoTemplateTargetConstraint",
    "TargetNoTemplateTargetConstraintPocketConstraint",
    "TargetNoTemplateTargetConstraintContactConstraint",
    "TargetNoTemplateTargetConstraintContactConstraintToken1",
    "TargetNoTemplateTargetConstraintContactConstraintToken1PolymerContactToken",
    "TargetNoTemplateTargetConstraintContactConstraintToken1LigandContactToken",
    "TargetNoTemplateTargetConstraintContactConstraintToken2",
    "TargetNoTemplateTargetConstraintContactConstraintToken2PolymerContactToken",
    "TargetNoTemplateTargetConstraintContactConstraintToken2LigandContactToken",
]


class LibraryScreenStartParams(TypedDict, total=False):
    proteins: Required[Iterable[Protein]]
    """List of protein entries to screen."""

    target: Required[Target]
    """Target specification (structure template or template-free)"""

    idempotency_key: str
    """Client-provided key to prevent duplicate submissions on retries"""

    workspace_id: str
    """Target workspace ID (admin keys only; ignored for workspace keys)"""


class ProteinEntityProteinEntityModification(TypedDict, total=False):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: Required[int]
    """0-based index of the residue to modify"""

    type: Required[Literal["ccd"]]
    """Modification format. Only CCD polymer modifications are supported."""

    value: Required[str]
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class ProteinEntityProteinEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["protein"]]

    value: Required[str]
    """Amino acid sequence (one-letter codes)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[ProteinEntityProteinEntityModification]
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class ProteinEntityRnaEntityModification(TypedDict, total=False):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: Required[int]
    """0-based index of the residue to modify"""

    type: Required[Literal["ccd"]]
    """Modification format. Only CCD polymer modifications are supported."""

    value: Required[str]
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class ProteinEntityRnaEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["rna"]]

    value: Required[str]
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[ProteinEntityRnaEntityModification]
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class ProteinEntityDnaEntityModification(TypedDict, total=False):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: Required[int]
    """0-based index of the residue to modify"""

    type: Required[Literal["ccd"]]
    """Modification format. Only CCD polymer modifications are supported."""

    value: Required[str]
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class ProteinEntityDnaEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["dna"]]

    value: Required[str]
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[ProteinEntityDnaEntityModification]
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class ProteinEntityLigandCcdEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this ligand"""

    type: Required[Literal["ligand_ccd"]]

    value: Required[str]
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class ProteinEntityLigandSmilesEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this ligand"""

    type: Required[Literal["ligand_smiles"]]

    value: Required[str]
    """SMILES string representing the ligand"""


class ProteinEntityGlycanEntityBondAtom1(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class ProteinEntityGlycanEntityBondAtom2(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class ProteinEntityGlycanEntityBond(TypedDict, total=False):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: Required[ProteinEntityGlycanEntityBondAtom1]

    atom2: Required[ProteinEntityGlycanEntityBondAtom2]


class ProteinEntityGlycanEntityResidue(TypedDict, total=False):
    id: Required[str]
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: Required[str]
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class ProteinEntityGlycanEntity(TypedDict, total=False):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: Required[Iterable[ProteinEntityGlycanEntityBond]]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for identical copies of this glycan"""

    residues: Required[Iterable[ProteinEntityGlycanEntityResidue]]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Required[Literal["glycan"]]


ProteinEntity: TypeAlias = Union[
    ProteinEntityProteinEntity,
    ProteinEntityRnaEntity,
    ProteinEntityDnaEntity,
    ProteinEntityLigandCcdEntity,
    ProteinEntityLigandSmilesEntity,
    ProteinEntityGlycanEntity,
]


class Protein(TypedDict, total=False):
    """A protein screen entry with entities and optional ID"""

    entities: Required[Iterable[ProteinEntity]]
    """Entities that make up this protein complex"""

    id: str
    """Optional client-provided identifier for this entry"""


class TargetStructureTemplateTargetChainSelectionStructureTemplateTargetPolymerChainSpec(TypedDict, total=False):
    """
    Per-chain specification for a polymer (protein/RNA/DNA) chain in a structure template target.
    """

    chain_type: Required[Literal["polymer"]]

    crop_residues: Required[Union[Iterable[int], Literal["all"]]]
    """
    0-indexed residue indices to retain from this chain, or 'all' to keep all
    residues. Residues not listed are excluded from the pipeline run.
    """

    epitope_residues: Iterable[int]
    """0-indexed residue indices where binder contact is desired (the epitope).

    All indices must be present in crop_residues and must not overlap
    non_binding_residues.
    """

    flexible_residues: Iterable[int]
    """0-indexed residue indices allowed to move during design (e.g.

    flexible loop regions). All indices must be present in crop_residues.
    """

    non_binding_residues: Iterable[int]
    """0-indexed residue indices where binder contact should be discouraged.

    All indices must be present in crop_residues and must not overlap
    epitope_residues.
    """


class TargetStructureTemplateTargetChainSelectionStructureTemplateTargetLigandChainSpec(TypedDict, total=False):
    """Per-chain specification for a ligand chain in a structure template target.

    The full ligand is always included.
    """

    chain_type: Required[Literal["ligand"]]


TargetStructureTemplateTargetChainSelection: TypeAlias = Union[
    TargetStructureTemplateTargetChainSelectionStructureTemplateTargetPolymerChainSpec,
    TargetStructureTemplateTargetChainSelectionStructureTemplateTargetLigandChainSpec,
]


class TargetStructureTemplateTargetStructureURLSource(TypedDict, total=False):
    type: Required[Literal["url"]]

    url: Required[str]


class TargetStructureTemplateTargetStructureCifBase64Source(TypedDict, total=False):
    data: Required[str]
    """Base64-encoded CIF file contents"""

    media_type: Required[Literal["chemical/x-cif"]]
    """Must be chemical/x-cif for CIF files"""

    type: Required[Literal["base64"]]


TargetStructureTemplateTargetStructure: TypeAlias = Union[
    TargetStructureTemplateTargetStructureURLSource, TargetStructureTemplateTargetStructureCifBase64Source
]


class TargetStructureTemplateTarget(TypedDict, total=False):
    """Target defined by an uploaded 3D structure (CIF or PDB file).

    Only chains included in chain_selection are used.
    """

    chain_selection: Required[Dict[str, TargetStructureTemplateTargetChainSelection]]
    """Chains selected from the uploaded structure, keyed by chain ID.

    Only chains listed here are included in the pipeline run — any chains omitted
    from this mapping are ignored. Each value defines which residues to keep, which
    are epitope residues, which are non-binding residues, and which are flexible.
    """

    structure: Required[TargetStructureTemplateTargetStructure]
    """How to provide a CIF structure file.

    URLs are auto-detected; base64 uploads must use chemical/x-cif media type.
    """

    type: Required[Literal["structure_template"]]


class TargetNoTemplateTargetEntityProteinEntityModification(TypedDict, total=False):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: Required[int]
    """0-based index of the residue to modify"""

    type: Required[Literal["ccd"]]
    """Modification format. Only CCD polymer modifications are supported."""

    value: Required[str]
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class TargetNoTemplateTargetEntityProteinEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["protein"]]

    value: Required[str]
    """Amino acid sequence (one-letter codes)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[TargetNoTemplateTargetEntityProteinEntityModification]
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class TargetNoTemplateTargetEntityRnaEntityModification(TypedDict, total=False):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: Required[int]
    """0-based index of the residue to modify"""

    type: Required[Literal["ccd"]]
    """Modification format. Only CCD polymer modifications are supported."""

    value: Required[str]
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class TargetNoTemplateTargetEntityRnaEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["rna"]]

    value: Required[str]
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[TargetNoTemplateTargetEntityRnaEntityModification]
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class TargetNoTemplateTargetEntityDnaEntityModification(TypedDict, total=False):
    """Polymer residue modification.

    Only CCD codes are supported; SMILES modifications are not accepted.
    """

    residue_index: Required[int]
    """0-based index of the residue to modify"""

    type: Required[Literal["ccd"]]
    """Modification format. Only CCD polymer modifications are supported."""

    value: Required[str]
    """CCD code from RCSB PDB (e.g.

    'MSE' for selenomethionine, 'SEP' for phosphoserine)
    """


class TargetNoTemplateTargetEntityDnaEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["dna"]]

    value: Required[str]
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[TargetNoTemplateTargetEntityDnaEntityModification]
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class TargetNoTemplateTargetEntityLigandCcdEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this ligand"""

    type: Required[Literal["ligand_ccd"]]

    value: Required[str]
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class TargetNoTemplateTargetEntityLigandSmilesEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this ligand"""

    type: Required[Literal["ligand_smiles"]]

    value: Required[str]
    """SMILES string representing the ligand"""


class TargetNoTemplateTargetEntityGlycanEntityBondAtom1(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class TargetNoTemplateTargetEntityGlycanEntityBondAtom2(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class TargetNoTemplateTargetEntityGlycanEntityBond(TypedDict, total=False):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: Required[TargetNoTemplateTargetEntityGlycanEntityBondAtom1]

    atom2: Required[TargetNoTemplateTargetEntityGlycanEntityBondAtom2]


class TargetNoTemplateTargetEntityGlycanEntityResidue(TypedDict, total=False):
    id: Required[str]
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: Required[str]
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class TargetNoTemplateTargetEntityGlycanEntity(TypedDict, total=False):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: Required[Iterable[TargetNoTemplateTargetEntityGlycanEntityBond]]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for identical copies of this glycan"""

    residues: Required[Iterable[TargetNoTemplateTargetEntityGlycanEntityResidue]]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Required[Literal["glycan"]]


TargetNoTemplateTargetEntity: TypeAlias = Union[
    TargetNoTemplateTargetEntityProteinEntity,
    TargetNoTemplateTargetEntityRnaEntity,
    TargetNoTemplateTargetEntityDnaEntity,
    TargetNoTemplateTargetEntityLigandCcdEntity,
    TargetNoTemplateTargetEntityLigandSmilesEntity,
    TargetNoTemplateTargetEntityGlycanEntity,
]


class TargetNoTemplateTargetBondAtom1PolymerAtom(TypedDict, total=False):
    atom_name: Required[str]
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: Required[str]
    """Chain ID containing the atom"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_atom"]]


class TargetNoTemplateTargetBondAtom1CcdAtom(TypedDict, total=False):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: Required[str]
    """Chain ID containing the CCD residue"""

    residue_id: Required[str]
    """Request-local residue ID declared by the graph entity"""

    type: Required[Literal["ccd_atom"]]


class TargetNoTemplateTargetBondAtom1SmilesAtom(TypedDict, total=False):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: Required[int]
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: Required[str]
    """Chain ID containing the SMILES ligand"""

    type: Required[Literal["smiles_atom"]]


class TargetNoTemplateTargetBondAtom1LigandAtom(TypedDict, total=False):
    """
    Atom reference for a single-residue ligand_ccd or an explicitly atom-mapped SMILES ligand. Glycan bonds use ccd_atom; new SMILES bonds should use smiles_atom.
    """

    atom_name: Required[str]
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: Required[str]
    """Chain ID containing the atom"""

    type: Required[Literal["ligand_atom"]]


TargetNoTemplateTargetBondAtom1: TypeAlias = Union[
    TargetNoTemplateTargetBondAtom1PolymerAtom,
    TargetNoTemplateTargetBondAtom1CcdAtom,
    TargetNoTemplateTargetBondAtom1SmilesAtom,
    TargetNoTemplateTargetBondAtom1LigandAtom,
]


class TargetNoTemplateTargetBondAtom2PolymerAtom(TypedDict, total=False):
    atom_name: Required[str]
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: Required[str]
    """Chain ID containing the atom"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_atom"]]


class TargetNoTemplateTargetBondAtom2CcdAtom(TypedDict, total=False):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: Required[str]
    """Chain ID containing the CCD residue"""

    residue_id: Required[str]
    """Request-local residue ID declared by the graph entity"""

    type: Required[Literal["ccd_atom"]]


class TargetNoTemplateTargetBondAtom2SmilesAtom(TypedDict, total=False):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: Required[int]
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: Required[str]
    """Chain ID containing the SMILES ligand"""

    type: Required[Literal["smiles_atom"]]


class TargetNoTemplateTargetBondAtom2LigandAtom(TypedDict, total=False):
    """
    Atom reference for a single-residue ligand_ccd or an explicitly atom-mapped SMILES ligand. Glycan bonds use ccd_atom; new SMILES bonds should use smiles_atom.
    """

    atom_name: Required[str]
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: Required[str]
    """Chain ID containing the atom"""

    type: Required[Literal["ligand_atom"]]


TargetNoTemplateTargetBondAtom2: TypeAlias = Union[
    TargetNoTemplateTargetBondAtom2PolymerAtom,
    TargetNoTemplateTargetBondAtom2CcdAtom,
    TargetNoTemplateTargetBondAtom2SmilesAtom,
    TargetNoTemplateTargetBondAtom2LigandAtom,
]


class TargetNoTemplateTargetBond(TypedDict, total=False):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: Required[TargetNoTemplateTargetBondAtom1]
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: Required[TargetNoTemplateTargetBondAtom2]
    """Atom reference for a specific CCD residue in a glycan graph."""


class TargetNoTemplateTargetConstraintPocketConstraint(TypedDict, total=False):
    """Constrains the binder to interact with specific pocket residues on the target."""

    binder_chain_id: Required[str]
    """Chain ID of the binder molecule"""

    contact_residues: Required[Dict[str, Iterable[int]]]
    """Binding pocket residues keyed by chain ID.

    Each key is a chain ID (e.g. "A") and the value is an array of 0-indexed residue
    indices that define the pocket on that chain.
    """

    max_distance_angstrom: Required[float]
    """Maximum allowed distance in Angstroms between binder and pocket residues.

    Typical range: 4-8 A.
    """

    type: Required[Literal["pocket"]]

    force: bool
    """Whether to force the constraint"""


class TargetNoTemplateTargetConstraintContactConstraintToken1PolymerContactToken(TypedDict, total=False):
    chain_id: Required[str]
    """Chain ID"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_contact"]]


class TargetNoTemplateTargetConstraintContactConstraintToken1LigandContactToken(TypedDict, total=False):
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    atom_name: Required[str]
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: Required[str]
    """Chain ID"""

    type: Required[Literal["ligand_contact"]]


TargetNoTemplateTargetConstraintContactConstraintToken1: TypeAlias = Union[
    TargetNoTemplateTargetConstraintContactConstraintToken1PolymerContactToken,
    TargetNoTemplateTargetConstraintContactConstraintToken1LigandContactToken,
]


class TargetNoTemplateTargetConstraintContactConstraintToken2PolymerContactToken(TypedDict, total=False):
    chain_id: Required[str]
    """Chain ID"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_contact"]]


class TargetNoTemplateTargetConstraintContactConstraintToken2LigandContactToken(TypedDict, total=False):
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    atom_name: Required[str]
    """Atom name.

    For ligand_ccd, use the standardized CIF atom name. For ligand_smiles,
    explicitly label the atom with numeric atom-map notation: [C:1] is referenced as
    C1 and [O:2] as O2. The resulting name must be unique within the molecule and at
    most four characters.
    """

    chain_id: Required[str]
    """Chain ID"""

    type: Required[Literal["ligand_contact"]]


TargetNoTemplateTargetConstraintContactConstraintToken2: TypeAlias = Union[
    TargetNoTemplateTargetConstraintContactConstraintToken2PolymerContactToken,
    TargetNoTemplateTargetConstraintContactConstraintToken2LigandContactToken,
]


class TargetNoTemplateTargetConstraintContactConstraint(TypedDict, total=False):
    """
    Maximum-distance contact constraint between two polymer residues or ligand atoms.
    """

    max_distance_angstrom: Required[float]
    """Maximum distance in Angstroms"""

    token1: Required[TargetNoTemplateTargetConstraintContactConstraintToken1]
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    token2: Required[TargetNoTemplateTargetConstraintContactConstraintToken2]
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    type: Required[Literal["contact"]]

    force: bool
    """Whether to force the constraint"""


TargetNoTemplateTargetConstraint: TypeAlias = Union[
    TargetNoTemplateTargetConstraintPocketConstraint, TargetNoTemplateTargetConstraintContactConstraint
]


class TargetNoTemplateTarget(TypedDict, total=False):
    """Target defined by sequences only, without a 3D structure template"""

    entities: Required[Iterable[TargetNoTemplateTargetEntity]]
    """Entities (proteins, RNA, DNA, ligands) defining the target complex."""

    type: Required[Literal["no_template"]]

    bonds: Iterable[TargetNoTemplateTargetBond]
    """Covalent bond constraints between atoms in the target complex.

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    constraints: Iterable[TargetNoTemplateTargetConstraint]
    """Structural constraints (pocket and contact).

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    epitope_ligand_chains: SequenceNotStr[str]
    """Chain IDs of ligand entities that are part of the binding epitope.

    Ligands are marked as epitope in full (no residue-level selection).
    """

    epitope_residues: Dict[str, Iterable[int]]
    """Polymer chain residues where binder contact is desired (the epitope).

    Each key is a chain ID of a polymer entity, each value is an array of 0-indexed
    residue indices. Residues must not overlap non_binding_residues on the same
    chain.
    """

    non_binding_residues: Dict[str, Iterable[int]]
    """Polymer chain residues where binder contact should be discouraged.

    Each key is a chain ID of a polymer entity, each value is an array of 0-indexed
    residue indices. Residues must not overlap epitope_residues on the same chain.
    """


Target: TypeAlias = Union[TargetStructureTemplateTarget, TargetNoTemplateTarget]
