# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = [
    "StructureAndBindingStartParams",
    "Input",
    "InputEntity",
    "InputEntityBoltz2ProteinEntity",
    "InputEntityBoltz2ProteinEntityModification",
    "InputEntityBoltz2ProteinEntityMsa",
    "InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsa",
    "InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSource",
    "InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSourceURLSource",
    "InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSourceBase64Source",
    "InputEntityBoltz2ProteinEntityMsaBoltz2EmptyMsa",
    "InputEntityRnaEntity",
    "InputEntityRnaEntityModification",
    "InputEntityDnaEntity",
    "InputEntityDnaEntityModification",
    "InputEntityLigandCcdEntity",
    "InputEntityLigandSmilesEntity",
    "InputEntityGlycanEntity",
    "InputEntityGlycanEntityBond",
    "InputEntityGlycanEntityBondAtom1",
    "InputEntityGlycanEntityBondAtom2",
    "InputEntityGlycanEntityResidue",
    "InputBinding",
    "InputBindingLigandProteinBinding",
    "InputBindingProteinProteinBinding",
    "InputBond",
    "InputBondAtom1",
    "InputBondAtom1PolymerAtom",
    "InputBondAtom1CcdAtom",
    "InputBondAtom1SmilesAtom",
    "InputBondAtom1LigandAtom",
    "InputBondAtom2",
    "InputBondAtom2PolymerAtom",
    "InputBondAtom2CcdAtom",
    "InputBondAtom2SmilesAtom",
    "InputBondAtom2LigandAtom",
    "InputConstraint",
    "InputConstraintPocketConstraint",
    "InputConstraintContactConstraint",
    "InputConstraintContactConstraintToken1",
    "InputConstraintContactConstraintToken1PolymerContactToken",
    "InputConstraintContactConstraintToken1LigandContactToken",
    "InputConstraintContactConstraintToken2",
    "InputConstraintContactConstraintToken2PolymerContactToken",
    "InputConstraintContactConstraintToken2LigandContactToken",
    "InputModelOptions",
    "InputTemplate",
    "InputTemplateTemplateChain",
    "InputTemplateTemplateStructure",
    "InputTemplateTemplateStructureURLSource",
    "InputTemplateTemplateStructureTemplateStructureBase64Source",
]


class StructureAndBindingStartParams(TypedDict, total=False):
    input: Required[Input]

    model: Required[Literal["boltz-2.1"]]
    """Model to use for prediction"""

    idempotency_key: str
    """Client-provided key to prevent duplicate submissions on retries"""

    workspace_id: str
    """Target workspace ID (admin keys only; ignored for workspace keys)"""


class InputEntityBoltz2ProteinEntityModification(TypedDict, total=False):
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


class InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSourceURLSource(TypedDict, total=False):
    type: Required[Literal["url"]]

    url: Required[str]


class InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSourceBase64Source(TypedDict, total=False):
    data: Required[str]
    """Base64-encoded file contents"""

    media_type: Required[str]
    """MIME type (e.g., text/csv)"""

    type: Required[Literal["base64"]]


InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSource: TypeAlias = Union[
    InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSourceURLSource,
    InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSourceBase64Source,
]


class InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsa(TypedDict, total=False):
    """Use a user-provided MSA for this protein entity.

    If any protein entity uses a custom MSA, every other protein entity must use either custom or empty MSA; automatic MSA generation cannot be mixed with custom MSAs in the same request.
    """

    format: Required[Literal["a3m", "csv"]]
    """Custom MSA file format.

    Base64 uploads must use media_type text/x-a3m for A3M or text/csv for CSV.
    """

    source: Required[InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsaSource]
    """How to provide a file to the API"""

    type: Required[Literal["custom"]]


class InputEntityBoltz2ProteinEntityMsaBoltz2EmptyMsa(TypedDict, total=False):
    """Run this protein entity in single-sequence mode without an MSA.

    Use this for chains that should not use automatic MSA generation, including non-homologous chains in a request that also includes custom MSAs.
    """

    type: Required[Literal["empty"]]


InputEntityBoltz2ProteinEntityMsa: TypeAlias = Union[
    InputEntityBoltz2ProteinEntityMsaBoltz2CustomMsa, InputEntityBoltz2ProteinEntityMsaBoltz2EmptyMsa
]


class InputEntityBoltz2ProteinEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["protein"]]

    value: Required[str]
    """Amino acid sequence (one-letter codes)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[InputEntityBoltz2ProteinEntityModification]
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """

    msa: InputEntityBoltz2ProteinEntityMsa
    """Optional protein MSA control.

    Omit msa on all protein entities to use automatic MSA generation. Use custom for
    user-provided A3M/CSV files, or empty for single-sequence mode. Custom MSA and
    automatic MSA cannot be mixed in one request.
    """


class InputEntityRnaEntityModification(TypedDict, total=False):
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


class InputEntityRnaEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["rna"]]

    value: Required[str]
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[InputEntityRnaEntityModification]
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputEntityDnaEntityModification(TypedDict, total=False):
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


class InputEntityDnaEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["dna"]]

    value: Required[str]
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[InputEntityDnaEntityModification]
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class InputEntityLigandCcdEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this ligand"""

    type: Required[Literal["ligand_ccd"]]

    value: Required[str]
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class InputEntityLigandSmilesEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this ligand"""

    type: Required[Literal["ligand_smiles"]]

    value: Required[str]
    """SMILES string representing the ligand"""


class InputEntityGlycanEntityBondAtom1(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class InputEntityGlycanEntityBondAtom2(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class InputEntityGlycanEntityBond(TypedDict, total=False):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: Required[InputEntityGlycanEntityBondAtom1]

    atom2: Required[InputEntityGlycanEntityBondAtom2]


class InputEntityGlycanEntityResidue(TypedDict, total=False):
    id: Required[str]
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: Required[str]
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class InputEntityGlycanEntity(TypedDict, total=False):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: Required[Iterable[InputEntityGlycanEntityBond]]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for identical copies of this glycan"""

    residues: Required[Iterable[InputEntityGlycanEntityResidue]]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Required[Literal["glycan"]]


InputEntity: TypeAlias = Union[
    InputEntityBoltz2ProteinEntity,
    InputEntityRnaEntity,
    InputEntityDnaEntity,
    InputEntityLigandCcdEntity,
    InputEntityLigandSmilesEntity,
    InputEntityGlycanEntity,
]


class InputBindingLigandProteinBinding(TypedDict, total=False):
    binder_chain_id: Required[str]
    """
    Chain ID of the ligand binder (must have exactly 1 copy, at most 2048 heavy
    atoms, and only ligands+proteins in entities)
    """

    type: Required[Literal["ligand_protein_binding"]]


class InputBindingProteinProteinBinding(TypedDict, total=False):
    binder_chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs of the protein binders"""

    type: Required[Literal["protein_protein_binding"]]


InputBinding: TypeAlias = Union[InputBindingLigandProteinBinding, InputBindingProteinProteinBinding]


class InputBondAtom1PolymerAtom(TypedDict, total=False):
    atom_name: Required[str]
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: Required[str]
    """Chain ID containing the atom"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_atom"]]


class InputBondAtom1CcdAtom(TypedDict, total=False):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: Required[str]
    """Chain ID containing the CCD residue"""

    residue_id: Required[str]
    """Request-local residue ID declared by the graph entity"""

    type: Required[Literal["ccd_atom"]]


class InputBondAtom1SmilesAtom(TypedDict, total=False):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: Required[int]
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: Required[str]
    """Chain ID containing the SMILES ligand"""

    type: Required[Literal["smiles_atom"]]


class InputBondAtom1LigandAtom(TypedDict, total=False):
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


InputBondAtom1: TypeAlias = Union[
    InputBondAtom1PolymerAtom, InputBondAtom1CcdAtom, InputBondAtom1SmilesAtom, InputBondAtom1LigandAtom
]


class InputBondAtom2PolymerAtom(TypedDict, total=False):
    atom_name: Required[str]
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: Required[str]
    """Chain ID containing the atom"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_atom"]]


class InputBondAtom2CcdAtom(TypedDict, total=False):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: Required[str]
    """Chain ID containing the CCD residue"""

    residue_id: Required[str]
    """Request-local residue ID declared by the graph entity"""

    type: Required[Literal["ccd_atom"]]


class InputBondAtom2SmilesAtom(TypedDict, total=False):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: Required[int]
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: Required[str]
    """Chain ID containing the SMILES ligand"""

    type: Required[Literal["smiles_atom"]]


class InputBondAtom2LigandAtom(TypedDict, total=False):
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


InputBondAtom2: TypeAlias = Union[
    InputBondAtom2PolymerAtom, InputBondAtom2CcdAtom, InputBondAtom2SmilesAtom, InputBondAtom2LigandAtom
]


class InputBond(TypedDict, total=False):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: Required[InputBondAtom1]
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: Required[InputBondAtom2]
    """Atom reference for a specific CCD residue in a glycan graph."""


class InputConstraintPocketConstraint(TypedDict, total=False):
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


class InputConstraintContactConstraintToken1PolymerContactToken(TypedDict, total=False):
    chain_id: Required[str]
    """Chain ID"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_contact"]]


class InputConstraintContactConstraintToken1LigandContactToken(TypedDict, total=False):
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


InputConstraintContactConstraintToken1: TypeAlias = Union[
    InputConstraintContactConstraintToken1PolymerContactToken, InputConstraintContactConstraintToken1LigandContactToken
]


class InputConstraintContactConstraintToken2PolymerContactToken(TypedDict, total=False):
    chain_id: Required[str]
    """Chain ID"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_contact"]]


class InputConstraintContactConstraintToken2LigandContactToken(TypedDict, total=False):
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


InputConstraintContactConstraintToken2: TypeAlias = Union[
    InputConstraintContactConstraintToken2PolymerContactToken, InputConstraintContactConstraintToken2LigandContactToken
]


class InputConstraintContactConstraint(TypedDict, total=False):
    """
    Maximum-distance contact constraint between two polymer residues or ligand atoms.
    """

    max_distance_angstrom: Required[float]
    """Maximum distance in Angstroms"""

    token1: Required[InputConstraintContactConstraintToken1]
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    token2: Required[InputConstraintContactConstraintToken2]
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    type: Required[Literal["contact"]]

    force: bool
    """Whether to force the constraint"""


InputConstraint: TypeAlias = Union[InputConstraintPocketConstraint, InputConstraintContactConstraint]


class InputModelOptions(TypedDict, total=False):
    recycling_steps: int
    """The number of recycling steps to use for prediction. Default is 3."""

    sampling_steps: int
    """The number of sampling steps to use for prediction. Default is 200."""

    step_scale: float
    """Diffusion step scale (temperature).

    Controls sampling diversity — higher values produce more varied structures.
    Default is 1.638.
    """


class InputTemplateTemplateChain(TypedDict, total=False):
    """
    Mapping from one request chain to the corresponding chain in the template structure file.
    """

    input_chain_id: Required[str]
    """Chain ID in this prediction request"""

    template_chain_id: Required[str]
    """Corresponding chain ID in the template structure file"""


class InputTemplateTemplateStructureURLSource(TypedDict, total=False):
    type: Required[Literal["url"]]

    url: Required[str]


class InputTemplateTemplateStructureTemplateStructureBase64Source(TypedDict, total=False):
    data: Required[str]
    """Base64-encoded template structure file contents"""

    media_type: Required[Literal["chemical/x-cif", "chemical/x-pdb"]]
    """Template structure MIME type

    - `chemical/x-cif` - CIF template structure
    - `chemical/x-pdb` - PDB template structure
    """

    type: Required[Literal["base64"]]


InputTemplateTemplateStructure: TypeAlias = Union[
    InputTemplateTemplateStructureURLSource, InputTemplateTemplateStructureTemplateStructureBase64Source
]


class InputTemplate(TypedDict, total=False):
    """
    Template structure used as an inference-time guide for Boltz-2.1 protein-chain geometry. Provide a CIF or PDB file from an HTTPS URL or base64 upload.
    """

    template_chains: Required[Iterable[InputTemplateTemplateChain]]
    """Request-to-template chain mappings.

    Each input_chain_id and template_chain_id must be unique within this template.
    """

    template_structure: Required[InputTemplateTemplateStructure]
    """How to provide a template structure file.

    URLs must point to a CIF or PDB file; base64 uploads must use chemical/x-cif or
    chemical/x-pdb.
    """

    force_threshold_angstroms: float
    """Force the template reference potential with this distance threshold in
    angstroms.

    Omit to use the template without force.
    """


class Input(TypedDict, total=False):
    entities: Required[Iterable[InputEntity]]
    """
    Entities (proteins, RNA, DNA, ligands, and glycans) forming the complex to
    predict. Order determines chain assignment.
    """

    binding: InputBinding

    bonds: Iterable[InputBond]
    """Request-level covalent bonds between atoms.

    Use ccd_atom with a glycan residue ID, smiles_atom with a numeric SMILES
    atom-map, or ligand_atom for a single-residue ligand. Internal glycan bonds
    belong in the glycan entity bonds field.
    """

    constraints: Iterable[InputConstraint]
    """Structural constraints (pocket and contact).

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    model_options: InputModelOptions

    num_samples: int
    """Number of structure samples to generate (1-10)"""

    templates: Iterable[InputTemplate]
    """Template structure files to guide protein-chain prediction.

    Supports up to 4 CIF or PDB templates from HTTPS URLs or base64 uploads. Use
    template_chains to map request chains to template-file chains.
    """
