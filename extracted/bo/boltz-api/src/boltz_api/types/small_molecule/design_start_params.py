# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = [
    "DesignStartParams",
    "Target",
    "TargetEntity",
    "TargetEntityProteinEntity",
    "TargetEntityProteinEntityModification",
    "TargetEntityGlycanEntity",
    "TargetEntityGlycanEntityBond",
    "TargetEntityGlycanEntityBondAtom1",
    "TargetEntityGlycanEntityBondAtom2",
    "TargetEntityGlycanEntityResidue",
    "TargetBond",
    "TargetBondAtom1",
    "TargetBondAtom1PolymerAtom",
    "TargetBondAtom1CcdAtom",
    "TargetBondAtom1SmilesAtom",
    "TargetBondAtom1LigandAtom",
    "TargetBondAtom2",
    "TargetBondAtom2PolymerAtom",
    "TargetBondAtom2CcdAtom",
    "TargetBondAtom2SmilesAtom",
    "TargetBondAtom2LigandAtom",
    "TargetConstraint",
    "TargetConstraintPocketConstraint",
    "TargetConstraintContactConstraint",
    "TargetConstraintContactConstraintToken1",
    "TargetConstraintContactConstraintToken1PolymerContactToken",
    "TargetConstraintContactConstraintToken1LigandContactToken",
    "TargetConstraintContactConstraintToken2",
    "TargetConstraintContactConstraintToken2PolymerContactToken",
    "TargetConstraintContactConstraintToken2LigandContactToken",
    "MoleculeFilters",
    "MoleculeFiltersCustomFilter",
    "MoleculeFiltersCustomFilterLipinskiFilter",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilter",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterFractionCsp3",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterMolLogp",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterMolWt",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterNumAromaticRings",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHAcceptors",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHDonors",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHeteroatoms",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterNumRings",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterNumRotatableBonds",
    "MoleculeFiltersCustomFilterRdkitDescriptorFilterTpsa",
    "MoleculeFiltersCustomFilterSmartsCustomFilter",
    "MoleculeFiltersCustomFilterSmartsCatalogFilter",
    "MoleculeFiltersCustomFilterSmilesRegexFilter",
]


class DesignStartParams(TypedDict, total=False):
    num_molecules: Required[int]
    """Number of molecules to generate. Must be between 10 and 1,000,000."""

    target: Required[Target]
    """Target protein sequences for small molecule design or screening."""

    chemical_space: Literal["enamine_real", "none"]
    """Chemical space to constrain generated molecules.

    Use 'enamine_real' for the Enamine REAL chemical space, 'wuxi_galaxi' for the
    WuXi GalaXi chemical space when enabled for your organization, or 'none' to
    disable chemical-space filtering.
    """

    idempotency_key: str
    """Client-provided key to prevent duplicate submissions on retries"""

    molecule_filters: MoleculeFilters
    """Molecule filtering configuration.

    Controls both Boltz built-in SMARTS filtering and custom filters.
    """

    workspace_id: str
    """Target workspace ID (admin keys only; ignored for workspace keys)"""


class TargetEntityProteinEntityModification(TypedDict, total=False):
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


class TargetEntityProteinEntity(TypedDict, total=False):
    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for this entity"""

    type: Required[Literal["protein"]]

    value: Required[str]
    """Amino acid sequence (one-letter codes)"""

    cyclic: bool
    """Whether the sequence is cyclic"""

    modifications: Iterable[TargetEntityProteinEntityModification]
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class TargetEntityGlycanEntityBondAtom1(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class TargetEntityGlycanEntityBondAtom2(TypedDict, total=False):
    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: Required[str]
    """Request-local ID of the glycan residue containing the atom"""


class TargetEntityGlycanEntityBond(TypedDict, total=False):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: Required[TargetEntityGlycanEntityBondAtom1]

    atom2: Required[TargetEntityGlycanEntityBondAtom2]


class TargetEntityGlycanEntityResidue(TypedDict, total=False):
    id: Required[str]
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: Required[str]
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class TargetEntityGlycanEntity(TypedDict, total=False):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: Required[Iterable[TargetEntityGlycanEntityBond]]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: Required[SequenceNotStr[str]]
    """Chain IDs for identical copies of this glycan"""

    residues: Required[Iterable[TargetEntityGlycanEntityResidue]]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Required[Literal["glycan"]]


TargetEntity: TypeAlias = Union[TargetEntityProteinEntity, TargetEntityGlycanEntity]


class TargetBondAtom1PolymerAtom(TypedDict, total=False):
    atom_name: Required[str]
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: Required[str]
    """Chain ID containing the atom"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_atom"]]


class TargetBondAtom1CcdAtom(TypedDict, total=False):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: Required[str]
    """Chain ID containing the CCD residue"""

    residue_id: Required[str]
    """Request-local residue ID declared by the graph entity"""

    type: Required[Literal["ccd_atom"]]


class TargetBondAtom1SmilesAtom(TypedDict, total=False):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: Required[int]
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: Required[str]
    """Chain ID containing the SMILES ligand"""

    type: Required[Literal["smiles_atom"]]


class TargetBondAtom1LigandAtom(TypedDict, total=False):
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


TargetBondAtom1: TypeAlias = Union[
    TargetBondAtom1PolymerAtom, TargetBondAtom1CcdAtom, TargetBondAtom1SmilesAtom, TargetBondAtom1LigandAtom
]


class TargetBondAtom2PolymerAtom(TypedDict, total=False):
    atom_name: Required[str]
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: Required[str]
    """Chain ID containing the atom"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_atom"]]


class TargetBondAtom2CcdAtom(TypedDict, total=False):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: Required[str]
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: Required[str]
    """Chain ID containing the CCD residue"""

    residue_id: Required[str]
    """Request-local residue ID declared by the graph entity"""

    type: Required[Literal["ccd_atom"]]


class TargetBondAtom2SmilesAtom(TypedDict, total=False):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: Required[int]
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: Required[str]
    """Chain ID containing the SMILES ligand"""

    type: Required[Literal["smiles_atom"]]


class TargetBondAtom2LigandAtom(TypedDict, total=False):
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


TargetBondAtom2: TypeAlias = Union[
    TargetBondAtom2PolymerAtom, TargetBondAtom2CcdAtom, TargetBondAtom2SmilesAtom, TargetBondAtom2LigandAtom
]


class TargetBond(TypedDict, total=False):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: Required[TargetBondAtom1]
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: Required[TargetBondAtom2]
    """Atom reference for a specific CCD residue in a glycan graph."""


class TargetConstraintPocketConstraint(TypedDict, total=False):
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


class TargetConstraintContactConstraintToken1PolymerContactToken(TypedDict, total=False):
    chain_id: Required[str]
    """Chain ID"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_contact"]]


class TargetConstraintContactConstraintToken1LigandContactToken(TypedDict, total=False):
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


TargetConstraintContactConstraintToken1: TypeAlias = Union[
    TargetConstraintContactConstraintToken1PolymerContactToken,
    TargetConstraintContactConstraintToken1LigandContactToken,
]


class TargetConstraintContactConstraintToken2PolymerContactToken(TypedDict, total=False):
    chain_id: Required[str]
    """Chain ID"""

    residue_index: Required[int]
    """0-based residue index"""

    type: Required[Literal["polymer_contact"]]


class TargetConstraintContactConstraintToken2LigandContactToken(TypedDict, total=False):
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


TargetConstraintContactConstraintToken2: TypeAlias = Union[
    TargetConstraintContactConstraintToken2PolymerContactToken,
    TargetConstraintContactConstraintToken2LigandContactToken,
]


class TargetConstraintContactConstraint(TypedDict, total=False):
    """
    Maximum-distance contact constraint between two polymer residues or ligand atoms.
    """

    max_distance_angstrom: Required[float]
    """Maximum distance in Angstroms"""

    token1: Required[TargetConstraintContactConstraintToken1]
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    token2: Required[TargetConstraintContactConstraintToken2]
    """Ligand contact token for a CCD atom or an explicitly atom-mapped SMILES atom."""

    type: Required[Literal["contact"]]

    force: bool
    """Whether to force the constraint"""


TargetConstraint: TypeAlias = Union[TargetConstraintPocketConstraint, TargetConstraintContactConstraint]


class Target(TypedDict, total=False):
    """Target protein sequences for small molecule design or screening."""

    entities: Required[Iterable[TargetEntity]]
    """Protein and glycan entities defining the target structure.

    At least one protein entity is required.
    """

    bonds: Iterable[TargetBond]
    """Covalent bond constraints between atoms in the target complex.

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    constraints: Iterable[TargetConstraint]
    """Structural constraints (pocket and contact).

    Ligand atom references support CCD atom names and explicitly atom-mapped SMILES
    atoms.
    """

    pocket_residues: Dict[str, Iterable[int]]
    """Binding pocket residues, keyed by chain ID.

    Each key is a chain ID (e.g. "A") and the value is an array of 0-indexed residue
    indices that define the binding pocket on that chain. When provided, these
    residues guide pocket extraction and add a derived pocket constraint during
    affinity predictions. That derived constraint remains separate from any explicit
    pocket constraints in target.constraints. When omitted, the model auto-detects
    the pocket.
    """

    reference_ligands: SequenceNotStr[str]
    """
    Reference ligands as SMILES strings that help the model identify the binding
    pocket. When omitted, a set of drug-like default ligands is used for pocket
    detection.
    """

    type: Literal["no_template"]
    """
    Target is defined directly by protein sequences rather than a structure
    template.
    """


class MoleculeFiltersCustomFilterLipinskiFilter(TypedDict, total=False):
    """Lipinski's Rule of Five filter.

    Rejects molecules that violate drug-likeness criteria based on molecular weight, LogP, hydrogen bond donors, and hydrogen bond acceptors.
    """

    max_hba: Required[float]
    """Maximum number of hydrogen bond acceptors. Lipinski threshold: 10"""

    max_hbd: Required[float]
    """Maximum number of hydrogen bond donors. Lipinski threshold: 5"""

    max_logp: Required[float]
    """Maximum LogP. Lipinski threshold: 5"""

    max_mw: Required[float]
    """Maximum molecular weight (Da). Lipinski threshold: 500"""

    type: Required[Literal["lipinski_filter"]]

    allow_single_violation: bool
    """If true, one rule violation is allowed (classic Rule of Five).

    Defaults to false (all rules must pass).
    """


class MoleculeFiltersCustomFilterRdkitDescriptorFilterFractionCsp3(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterMolLogp(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterMolWt(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterNumAromaticRings(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHAcceptors(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHDonors(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHeteroatoms(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterNumRings(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterNumRotatableBonds(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilterTpsa(TypedDict, total=False):
    """Min/max range constraint for an RDKit molecular descriptor"""

    max: float
    """Maximum allowed value (inclusive)"""

    min: float
    """Minimum allowed value (inclusive)"""


class MoleculeFiltersCustomFilterRdkitDescriptorFilter(TypedDict, total=False):
    """Filter molecules by RDKit molecular descriptors.

    Each descriptor is constrained to a min/max range. Only descriptors you provide are checked — omitted descriptors are unconstrained.
    """

    type: Required[Literal["rdkit_descriptor_filter"]]

    fraction_csp3: MoleculeFiltersCustomFilterRdkitDescriptorFilterFractionCsp3
    """Min/max range constraint for an RDKit molecular descriptor"""

    mol_logp: MoleculeFiltersCustomFilterRdkitDescriptorFilterMolLogp
    """Min/max range constraint for an RDKit molecular descriptor"""

    mol_wt: MoleculeFiltersCustomFilterRdkitDescriptorFilterMolWt
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_aromatic_rings: MoleculeFiltersCustomFilterRdkitDescriptorFilterNumAromaticRings
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_h_acceptors: MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHAcceptors
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_h_donors: MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHDonors
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_heteroatoms: MoleculeFiltersCustomFilterRdkitDescriptorFilterNumHeteroatoms
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_rings: MoleculeFiltersCustomFilterRdkitDescriptorFilterNumRings
    """Min/max range constraint for an RDKit molecular descriptor"""

    num_rotatable_bonds: MoleculeFiltersCustomFilterRdkitDescriptorFilterNumRotatableBonds
    """Min/max range constraint for an RDKit molecular descriptor"""

    tpsa: MoleculeFiltersCustomFilterRdkitDescriptorFilterTpsa
    """Min/max range constraint for an RDKit molecular descriptor"""


class MoleculeFiltersCustomFilterSmartsCustomFilter(TypedDict, total=False):
    """Filter molecules by custom SMARTS patterns.

    Molecules matching any pattern are rejected.
    """

    patterns: Required[SequenceNotStr[str]]
    """SMARTS patterns. Molecules matching any pattern are rejected."""

    type: Required[Literal["smarts_custom_filter"]]


class MoleculeFiltersCustomFilterSmartsCatalogFilter(TypedDict, total=False):
    """Filter molecules using a predefined SMARTS catalog of structural alerts."""

    catalog: Required[
        Literal[
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
    ]
    """Predefined SMARTS catalog to apply.

    PAINS, BRENK, ChEMBL, and NIH catalogs reject known problematic substructures.
    """

    type: Required[Literal["smarts_catalog_filter"]]


class MoleculeFiltersCustomFilterSmilesRegexFilter(TypedDict, total=False):
    """Filter molecules by regex patterns on their SMILES representation."""

    patterns: Required[SequenceNotStr[str]]
    """Regex patterns applied to SMILES strings.

    Molecules matching any pattern are rejected.
    """

    type: Required[Literal["smiles_regex_filter"]]


MoleculeFiltersCustomFilter: TypeAlias = Union[
    MoleculeFiltersCustomFilterLipinskiFilter,
    MoleculeFiltersCustomFilterRdkitDescriptorFilter,
    MoleculeFiltersCustomFilterSmartsCustomFilter,
    MoleculeFiltersCustomFilterSmartsCatalogFilter,
    MoleculeFiltersCustomFilterSmilesRegexFilter,
]


class MoleculeFilters(TypedDict, total=False):
    """Molecule filtering configuration.

    Controls both Boltz built-in SMARTS filtering and custom filters.
    """

    boltz_smarts_catalog_filter_level: Literal["recommended", "extra", "aggressive", "disabled"]
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

    custom_filters: Iterable[MoleculeFiltersCustomFilter]
    """Custom filters to apply. Molecules must pass all filters (AND logic)."""
