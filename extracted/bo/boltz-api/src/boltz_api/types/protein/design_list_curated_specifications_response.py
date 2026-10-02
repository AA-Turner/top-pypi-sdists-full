# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "DesignListCuratedSpecificationsResponse",
    "Data",
    "DataBinderSpecification",
    "DataBinderSpecificationStructureTemplateBinderSpec",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelection",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpec",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotif",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotif",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotifDesignLengthRange",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotif",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotifDesignLengthRange",
    "DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplateLigandChainSpec",
    "DataBinderSpecificationStructureTemplateBinderSpecStructure",
    "DataBinderSpecificationStructureTemplateBinderSpecStructureURLSource",
    "DataBinderSpecificationStructureTemplateBinderSpecStructureCifBase64Source",
    "DataBinderSpecificationStructureTemplateBinderSpecRules",
    "DataBinderSpecificationNoTemplateBinderSpec",
    "DataBinderSpecificationNoTemplateBinderSpecEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntityModification",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntityModification",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntityModification",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntityModification",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedLigandSmilesEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityFixedLigandCcdEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntity",
    "DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBond",
    "DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom1",
    "DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom2",
    "DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityResidue",
    "DataBinderSpecificationNoTemplateBinderSpecBond",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom1",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom1PolymerAtom",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom1CcdAtom",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom1SmilesAtom",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom1LigandAtom",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom2",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom2PolymerAtom",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom2CcdAtom",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom2SmilesAtom",
    "DataBinderSpecificationNoTemplateBinderSpecBondAtom2LigandAtom",
    "DataBinderSpecificationNoTemplateBinderSpecRules",
    "DataBinderSpecificationBoltzCuratedBinderSpec",
    "DataBinderSpecificationBoltzCuratedBinderSpecRules",
    "DataBinderSpecificationUniformlySampledBinderSpec",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecification",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpec",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelection",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpec",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotif",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotif",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotifDesignLengthRange",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotif",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotifDesignLengthRange",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplateLigandChainSpec",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructure",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructureURLSource",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructureCifBase64Source",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecRules",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpec",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntityModification",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntityModification",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntityModification",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntityModification",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedLigandSmilesEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedLigandCcdEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntity",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBond",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom1",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom2",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityResidue",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBond",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1PolymerAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1CcdAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1SmilesAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1LigandAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2PolymerAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2CcdAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2SmilesAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2LigandAtom",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecRules",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationBoltzCuratedBinderSpec",
    "DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationBoltzCuratedBinderSpecRules",
]


class DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotifDesignLengthRange(
    BaseModel
):
    """Allowed sequence length range for designed regions"""

    max: int
    """Maximum sequence length in residues. Must be >= min."""

    min: int
    """Minimum sequence length in residues"""


class DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotif(
    BaseModel
):
    """Replace a contiguous region of the sequence with a designed segment.

    Residues from start_index to end_index (inclusive) are replaced with a new sequence of the specified length.
    """

    design_length_range: DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotifDesignLengthRange
    """Allowed sequence length range for designed regions"""

    end_index: int
    """0-indexed end residue (inclusive)"""

    start_index: int
    """0-indexed start residue (inclusive)"""

    type: Literal["replacement"]


class DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotifDesignLengthRange(
    BaseModel
):
    """Allowed sequence length range for designed regions"""

    max: int
    """Maximum sequence length in residues. Must be >= min."""

    min: int
    """Minimum sequence length in residues"""


class DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotif(
    BaseModel
):
    """Insert a designed segment at a specific position in the sequence."""

    after_residue_index: int
    """0-indexed position after which to insert.

    Use -1 to insert before the first residue.
    """

    design_length_range: DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotifDesignLengthRange
    """Allowed sequence length range for designed regions"""

    type: Literal["insertion"]


DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotif: TypeAlias = Union[
    DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotif,
    DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotif,
]


class DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpec(BaseModel):
    """
    Per-chain crop and design specification for a polymer chain in structure_template mode.
    """

    chain_type: Literal["polymer"]

    crop_residues: Union[List[int], Literal["all"]]
    """
    0-indexed residue indices to retain from this chain, or 'all' to keep all
    residues. Residues not listed are removed before design.
    """

    design_motifs: Optional[
        List[
            DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotif
        ]
    ] = None
    """
    Optional motifs (replacement or insertion) defining which regions to redesign on
    this chain. Omit this field to include the chain as fixed scaffold context.
    """


class DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplateLigandChainSpec(BaseModel):
    """Per-chain specification for a ligand chain in structure_template mode.

    The full ligand is always included.
    """

    chain_type: Literal["ligand"]


DataBinderSpecificationStructureTemplateBinderSpecChainSelection: TypeAlias = Union[
    DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpec,
    DataBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplateLigandChainSpec,
]


class DataBinderSpecificationStructureTemplateBinderSpecStructureURLSource(BaseModel):
    type: Literal["url"]

    url: str


class DataBinderSpecificationStructureTemplateBinderSpecStructureCifBase64Source(BaseModel):
    data: str
    """Base64-encoded CIF file contents"""

    media_type: Literal["chemical/x-cif"]
    """Must be chemical/x-cif for CIF files"""

    type: Literal["base64"]


DataBinderSpecificationStructureTemplateBinderSpecStructure: TypeAlias = Union[
    DataBinderSpecificationStructureTemplateBinderSpecStructureURLSource,
    DataBinderSpecificationStructureTemplateBinderSpecStructureCifBase64Source,
]


class DataBinderSpecificationStructureTemplateBinderSpecRules(BaseModel):
    """Constraints applied during sequence design"""

    excluded_amino_acids: Optional[List[str]] = None
    """Single-letter amino acid codes to exclude from design (e.g.

    ['C', 'P'] to exclude cysteine and proline)
    """

    excluded_sequence_motifs: Optional[List[str]] = None
    """Sequence motifs to exclude from designed regions.

    Designs containing any of these motifs are filtered out before scoring. Use X as
    a single-residue wildcard (e.g. "NGS", "NXS").
    """

    max_hydrophobic_fraction: Optional[float] = None
    """
    Maximum allowed fraction of hydrophobic residues (I, L, V, M, F, W, Y) in
    designed regions. Designs exceeding this threshold are filtered out before
    scoring. Leave empty to disable.
    """


class DataBinderSpecificationStructureTemplateBinderSpec(BaseModel):
    """Binder specification starting from an existing 3D structure.

    Upload a CIF/PDB file and select which chains to include, which residues to keep, and which regions to redesign. Only chains included in chain_selection are part of the pipeline run.
    """

    chain_selection: Dict[str, DataBinderSpecificationStructureTemplateBinderSpecChainSelection]
    """Chains selected from the uploaded binder structure, keyed by chain ID.

    Only chains listed here are included in the pipeline run — any chains omitted
    from this mapping are ignored. Each value defines which residues to keep
    (crop_residues). Omit design_motifs to include the chain as fixed scaffold
    context.
    """

    modality: Literal["peptide", "antibody", "nanobody", "custom_protein"]

    structure: DataBinderSpecificationStructureTemplateBinderSpecStructure
    """How to provide a CIF structure file.

    URLs are auto-detected; base64 uploads must use chemical/x-cif media type.
    """

    type: Literal["structure_template"]

    rules: Optional[DataBinderSpecificationStructureTemplateBinderSpecRules] = None
    """Constraints applied during sequence design"""


class DataBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntityModification(BaseModel):
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


class DataBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntity(BaseModel):
    """Protein binder entity with designed and/or fixed segments."""

    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["designed_protein"]

    value: str
    """Binder sequence specification.

    Fixed amino acids are written as literal single-letter codes. Designed regions
    are written as a length (fixed) or a length range (min..max). Example:
    "MKTAYI5..10VKSHFSRQ" means fixed MKTAYI, then 5-10 designed residues, then
    fixed VKSHFSRQ. "20" means 20 fully designed residues. "ACDE8GHI" means fixed
    ACDE, then 8 designed residues, then fixed GHI.
    """

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[
        List[DataBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntityModification]
    ] = None
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntityModification(BaseModel):
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


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntity(BaseModel):
    """A fixed protein entity whose sequence is not redesigned."""

    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[DataBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntityModification]] = (
        None
    )
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntityModification(BaseModel):
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


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["rna"]

    value: str
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[DataBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntityModification]] = None
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntityModification(BaseModel):
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


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["dna"]

    value: str
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[DataBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntityModification]] = None
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedLigandSmilesEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["ligand_smiles"]

    value: str
    """SMILES string representing the ligand"""


class DataBinderSpecificationNoTemplateBinderSpecEntityFixedLigandCcdEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["ligand_ccd"]

    value: str
    """CCD code from RCSB PDB (e.g. 'ATP', 'ADP')"""


class DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom1(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom2(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBond(BaseModel):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom1

    atom2: DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom2


class DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityResidue(BaseModel):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntity(BaseModel):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBond]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityResidue]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


DataBinderSpecificationNoTemplateBinderSpecEntity: TypeAlias = Union[
    DataBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntity,
    DataBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntity,
    DataBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntity,
    DataBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntity,
    DataBinderSpecificationNoTemplateBinderSpecEntityFixedLigandSmilesEntity,
    DataBinderSpecificationNoTemplateBinderSpecEntityFixedLigandCcdEntity,
    DataBinderSpecificationNoTemplateBinderSpecEntityGlycanEntity,
]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom1PolymerAtom(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom1CcdAtom(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom1SmilesAtom(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom1LigandAtom(BaseModel):
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


DataBinderSpecificationNoTemplateBinderSpecBondAtom1: TypeAlias = Union[
    DataBinderSpecificationNoTemplateBinderSpecBondAtom1PolymerAtom,
    DataBinderSpecificationNoTemplateBinderSpecBondAtom1CcdAtom,
    DataBinderSpecificationNoTemplateBinderSpecBondAtom1SmilesAtom,
    DataBinderSpecificationNoTemplateBinderSpecBondAtom1LigandAtom,
]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom2PolymerAtom(BaseModel):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom2CcdAtom(BaseModel):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom2SmilesAtom(BaseModel):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class DataBinderSpecificationNoTemplateBinderSpecBondAtom2LigandAtom(BaseModel):
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


DataBinderSpecificationNoTemplateBinderSpecBondAtom2: TypeAlias = Union[
    DataBinderSpecificationNoTemplateBinderSpecBondAtom2PolymerAtom,
    DataBinderSpecificationNoTemplateBinderSpecBondAtom2CcdAtom,
    DataBinderSpecificationNoTemplateBinderSpecBondAtom2SmilesAtom,
    DataBinderSpecificationNoTemplateBinderSpecBondAtom2LigandAtom,
]


class DataBinderSpecificationNoTemplateBinderSpecBond(BaseModel):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: DataBinderSpecificationNoTemplateBinderSpecBondAtom1
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: DataBinderSpecificationNoTemplateBinderSpecBondAtom2
    """Atom reference for a specific CCD residue in a glycan graph."""


class DataBinderSpecificationNoTemplateBinderSpecRules(BaseModel):
    """Constraints applied during sequence design"""

    excluded_amino_acids: Optional[List[str]] = None
    """Single-letter amino acid codes to exclude from design (e.g.

    ['C', 'P'] to exclude cysteine and proline)
    """

    excluded_sequence_motifs: Optional[List[str]] = None
    """Sequence motifs to exclude from designed regions.

    Designs containing any of these motifs are filtered out before scoring. Use X as
    a single-residue wildcard (e.g. "NGS", "NXS").
    """

    max_hydrophobic_fraction: Optional[float] = None
    """
    Maximum allowed fraction of hydrophobic residues (I, L, V, M, F, W, Y) in
    designed regions. Designs exceeding this threshold are filtered out before
    scoring. Leave empty to disable.
    """


class DataBinderSpecificationNoTemplateBinderSpec(BaseModel):
    """Binder specification without a structural template.

    Define the binder from sequence components (fixed and designed segments) without providing a starting 3D structure.
    """

    entities: List[DataBinderSpecificationNoTemplateBinderSpecEntity]
    """Binder entities composing the design.

    At least one must be a designed_protein entity. Additional fixed entities (RNA,
    DNA, ligands) can be included as part of the complex.
    """

    modality: Literal["peptide", "antibody", "nanobody", "custom_protein"]

    type: Literal["no_template"]

    bonds: Optional[List[DataBinderSpecificationNoTemplateBinderSpecBond]] = None
    """Covalent bond constraints between atoms in the binder complex.

    If defining bonds where an atom is part of a designed protein chain, assume
    residue indices count designed regions as the minimum length. Example: designed
    protein "1..3C1..2", "C" is residue 1 (0-indexed) of the designed protein.
    """

    rules: Optional[DataBinderSpecificationNoTemplateBinderSpecRules] = None
    """Constraints applied during sequence design"""


class DataBinderSpecificationBoltzCuratedBinderSpecRules(BaseModel):
    """Constraints applied during sequence design"""

    excluded_amino_acids: Optional[List[str]] = None
    """Single-letter amino acid codes to exclude from design (e.g.

    ['C', 'P'] to exclude cysteine and proline)
    """

    excluded_sequence_motifs: Optional[List[str]] = None
    """Sequence motifs to exclude from designed regions.

    Designs containing any of these motifs are filtered out before scoring. Use X as
    a single-residue wildcard (e.g. "NGS", "NXS").
    """

    max_hydrophobic_fraction: Optional[float] = None
    """
    Maximum allowed fraction of hydrophobic residues (I, L, V, M, F, W, Y) in
    designed regions. Designs exceeding this threshold are filtered out before
    scoring. Leave empty to disable.
    """


class DataBinderSpecificationBoltzCuratedBinderSpec(BaseModel):
    """Boltz-managed curated binder specification.

    Choose a curated nanobody or antibody family and Boltz will select from maintained template lists during design. The curated lists are managed by Boltz and may be updated over time to improve quality and coverage.
    """

    binder: Literal["boltz_nanobody", "boltz_antibody"]
    """Boltz-managed curated binder family.

    Boltz maintains and may update the underlying template lists on behalf of
    customers.
    """

    type: Literal["boltz_curated"]

    rules: Optional[DataBinderSpecificationBoltzCuratedBinderSpecRules] = None
    """Constraints applied during sequence design"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotifDesignLengthRange(
    BaseModel
):
    """Allowed sequence length range for designed regions"""

    max: int
    """Maximum sequence length in residues. Must be >= min."""

    min: int
    """Minimum sequence length in residues"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotif(
    BaseModel
):
    """Replace a contiguous region of the sequence with a designed segment.

    Residues from start_index to end_index (inclusive) are replaced with a new sequence of the specified length.
    """

    design_length_range: DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotifDesignLengthRange
    """Allowed sequence length range for designed regions"""

    end_index: int
    """0-indexed end residue (inclusive)"""

    start_index: int
    """0-indexed start residue (inclusive)"""

    type: Literal["replacement"]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotifDesignLengthRange(
    BaseModel
):
    """Allowed sequence length range for designed regions"""

    max: int
    """Maximum sequence length in residues. Must be >= min."""

    min: int
    """Minimum sequence length in residues"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotif(
    BaseModel
):
    """Insert a designed segment at a specific position in the sequence."""

    after_residue_index: int
    """0-indexed position after which to insert.

    Use -1 to insert before the first residue.
    """

    design_length_range: DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotifDesignLengthRange
    """Allowed sequence length range for designed regions"""

    type: Literal["insertion"]


DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotif: TypeAlias = Union[
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifReplacementMotif,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotifInsertionMotif,
]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpec(
    BaseModel
):
    """
    Per-chain crop and design specification for a polymer chain in structure_template mode.
    """

    chain_type: Literal["polymer"]

    crop_residues: Union[List[int], Literal["all"]]
    """
    0-indexed residue indices to retain from this chain, or 'all' to keep all
    residues. Residues not listed are removed before design.
    """

    design_motifs: Optional[
        List[
            DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpecDesignMotif
        ]
    ] = None
    """
    Optional motifs (replacement or insertion) defining which regions to redesign on
    this chain. Omit this field to include the chain as fixed scaffold context.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplateLigandChainSpec(
    BaseModel
):
    """Per-chain specification for a ligand chain in structure_template mode.

    The full ligand is always included.
    """

    chain_type: Literal["ligand"]


DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelection: TypeAlias = Union[
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplatePolymerChainSpec,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelectionStructureTemplateLigandChainSpec,
]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructureURLSource(
    BaseModel
):
    type: Literal["url"]

    url: str


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructureCifBase64Source(
    BaseModel
):
    data: str
    """Base64-encoded CIF file contents"""

    media_type: Literal["chemical/x-cif"]
    """Must be chemical/x-cif for CIF files"""

    type: Literal["base64"]


DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructure: TypeAlias = Union[
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructureURLSource,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructureCifBase64Source,
]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecRules(BaseModel):
    """Constraints applied during sequence design"""

    excluded_amino_acids: Optional[List[str]] = None
    """Single-letter amino acid codes to exclude from design (e.g.

    ['C', 'P'] to exclude cysteine and proline)
    """

    excluded_sequence_motifs: Optional[List[str]] = None
    """Sequence motifs to exclude from designed regions.

    Designs containing any of these motifs are filtered out before scoring. Use X as
    a single-residue wildcard (e.g. "NGS", "NXS").
    """

    max_hydrophobic_fraction: Optional[float] = None
    """
    Maximum allowed fraction of hydrophobic residues (I, L, V, M, F, W, Y) in
    designed regions. Designs exceeding this threshold are filtered out before
    scoring. Leave empty to disable.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpec(BaseModel):
    """Binder specification starting from an existing 3D structure.

    Upload a CIF/PDB file and select which chains to include, which residues to keep, and which regions to redesign. Only chains included in chain_selection are part of the pipeline run.
    """

    chain_selection: Dict[
        str,
        DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecChainSelection,
    ]
    """Chains selected from the uploaded binder structure, keyed by chain ID.

    Only chains listed here are included in the pipeline run — any chains omitted
    from this mapping are ignored. Each value defines which residues to keep
    (crop_residues). Omit design_motifs to include the chain as fixed scaffold
    context.
    """

    modality: Literal["peptide", "antibody", "nanobody", "custom_protein"]

    structure: DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecStructure
    """How to provide a CIF structure file.

    URLs are auto-detected; base64 uploads must use chemical/x-cif media type.
    """

    type: Literal["structure_template"]

    rules: Optional[
        DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpecRules
    ] = None
    """Constraints applied during sequence design"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntityModification(
    BaseModel
):
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


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntity(
    BaseModel
):
    """Protein binder entity with designed and/or fixed segments."""

    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["designed_protein"]

    value: str
    """Binder sequence specification.

    Fixed amino acids are written as literal single-letter codes. Designed regions
    are written as a length (fixed) or a length range (min..max). Example:
    "MKTAYI5..10VKSHFSRQ" means fixed MKTAYI, then 5-10 designed residues, then
    fixed VKSHFSRQ. "20" means 20 fully designed residues. "ACDE8GHI" means fixed
    ACDE, then 8 designed residues, then fixed GHI.
    """

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[
        List[
            DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntityModification
        ]
    ] = None
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntityModification(
    BaseModel
):
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


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntity(
    BaseModel
):
    """A fixed protein entity whose sequence is not redesigned."""

    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[
        List[
            DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntityModification
        ]
    ] = None
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntityModification(
    BaseModel
):
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


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntity(
    BaseModel
):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["rna"]

    value: str
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[
        List[
            DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntityModification
        ]
    ] = None
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntityModification(
    BaseModel
):
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


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntity(
    BaseModel
):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["dna"]

    value: str
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[
        List[
            DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntityModification
        ]
    ] = None
    """Optional CCD polymer modifications.

    Defaults to [] when omitted. SMILES modifications are not supported.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedLigandSmilesEntity(
    BaseModel
):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["ligand_smiles"]

    value: str
    """SMILES string representing the ligand"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedLigandCcdEntity(
    BaseModel
):
    chain_ids: List[str]
    """Chain IDs to assign to this entity"""

    type: Literal["ligand_ccd"]

    value: str
    """CCD code from RCSB PDB (e.g. 'ATP', 'ADP')"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom1(
    BaseModel
):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom2(
    BaseModel
):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBond(
    BaseModel
):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom1

    atom2: DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBondAtom2


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityResidue(
    BaseModel
):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntity(
    BaseModel
):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[
        DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityBond
    ]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[
        DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntityResidue
    ]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntity: TypeAlias = Union[
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityDesignedProteinEntity,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedProteinEntity,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedRnaEntity,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedDnaEntity,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedLigandSmilesEntity,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityFixedLigandCcdEntity,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntityGlycanEntity,
]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1PolymerAtom(
    BaseModel
):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1CcdAtom(
    BaseModel
):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1SmilesAtom(
    BaseModel
):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1LigandAtom(
    BaseModel
):
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


DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1: TypeAlias = Union[
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1PolymerAtom,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1CcdAtom,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1SmilesAtom,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1LigandAtom,
]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2PolymerAtom(
    BaseModel
):
    atom_name: str
    """Standardized atom name (verifiable in CIF file on RCSB)"""

    chain_id: str
    """Chain ID containing the atom"""

    residue_index: int
    """0-based residue index"""

    type: Literal["polymer_atom"]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2CcdAtom(
    BaseModel
):
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    chain_id: str
    """Chain ID containing the CCD residue"""

    residue_id: str
    """Request-local residue ID declared by the graph entity"""

    type: Literal["ccd_atom"]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2SmilesAtom(
    BaseModel
):
    """Atom reference using an explicit numeric atom-map in the input SMILES."""

    atom_map: int
    """Numeric atom-map identifier from the input SMILES (for example 7 for [C:7])"""

    chain_id: str
    """Chain ID containing the SMILES ligand"""

    type: Literal["smiles_atom"]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2LigandAtom(
    BaseModel
):
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


DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2: TypeAlias = Union[
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2PolymerAtom,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2CcdAtom,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2SmilesAtom,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2LigandAtom,
]


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBond(BaseModel):
    """Request-level covalent bond between atoms, including protein-glycan attachments.

    Internal glycan connectivity belongs in the glycan entity bonds field.
    """

    atom1: DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom1
    """Atom reference for a specific CCD residue in a glycan graph."""

    atom2: DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBondAtom2
    """Atom reference for a specific CCD residue in a glycan graph."""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecRules(BaseModel):
    """Constraints applied during sequence design"""

    excluded_amino_acids: Optional[List[str]] = None
    """Single-letter amino acid codes to exclude from design (e.g.

    ['C', 'P'] to exclude cysteine and proline)
    """

    excluded_sequence_motifs: Optional[List[str]] = None
    """Sequence motifs to exclude from designed regions.

    Designs containing any of these motifs are filtered out before scoring. Use X as
    a single-residue wildcard (e.g. "NGS", "NXS").
    """

    max_hydrophobic_fraction: Optional[float] = None
    """
    Maximum allowed fraction of hydrophobic residues (I, L, V, M, F, W, Y) in
    designed regions. Designs exceeding this threshold are filtered out before
    scoring. Leave empty to disable.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpec(BaseModel):
    """Binder specification without a structural template.

    Define the binder from sequence components (fixed and designed segments) without providing a starting 3D structure.
    """

    entities: List[DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecEntity]
    """Binder entities composing the design.

    At least one must be a designed_protein entity. Additional fixed entities (RNA,
    DNA, ligands) can be included as part of the complex.
    """

    modality: Literal["peptide", "antibody", "nanobody", "custom_protein"]

    type: Literal["no_template"]

    bonds: Optional[
        List[DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecBond]
    ] = None
    """Covalent bond constraints between atoms in the binder complex.

    If defining bonds where an atom is part of a designed protein chain, assume
    residue indices count designed regions as the minimum length. Example: designed
    protein "1..3C1..2", "C" is residue 1 (0-indexed) of the designed protein.
    """

    rules: Optional[DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpecRules] = (
        None
    )
    """Constraints applied during sequence design"""


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationBoltzCuratedBinderSpecRules(BaseModel):
    """Constraints applied during sequence design"""

    excluded_amino_acids: Optional[List[str]] = None
    """Single-letter amino acid codes to exclude from design (e.g.

    ['C', 'P'] to exclude cysteine and proline)
    """

    excluded_sequence_motifs: Optional[List[str]] = None
    """Sequence motifs to exclude from designed regions.

    Designs containing any of these motifs are filtered out before scoring. Use X as
    a single-residue wildcard (e.g. "NGS", "NXS").
    """

    max_hydrophobic_fraction: Optional[float] = None
    """
    Maximum allowed fraction of hydrophobic residues (I, L, V, M, F, W, Y) in
    designed regions. Designs exceeding this threshold are filtered out before
    scoring. Leave empty to disable.
    """


class DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationBoltzCuratedBinderSpec(BaseModel):
    """Boltz-managed curated binder specification.

    Choose a curated nanobody or antibody family and Boltz will select from maintained template lists during design. The curated lists are managed by Boltz and may be updated over time to improve quality and coverage.
    """

    binder: Literal["boltz_nanobody", "boltz_antibody"]
    """Boltz-managed curated binder family.

    Boltz maintains and may update the underlying template lists on behalf of
    customers.
    """

    type: Literal["boltz_curated"]

    rules: Optional[DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationBoltzCuratedBinderSpecRules] = (
        None
    )
    """Constraints applied during sequence design"""


DataBinderSpecificationUniformlySampledBinderSpecBinderSpecification: TypeAlias = Union[
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationStructureTemplateBinderSpec,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationNoTemplateBinderSpec,
    DataBinderSpecificationUniformlySampledBinderSpecBinderSpecificationBoltzCuratedBinderSpec,
]


class DataBinderSpecificationUniformlySampledBinderSpec(BaseModel):
    """A collection of binder specifications sampled uniformly during protein design.

    This lets one run explore multiple binder definitions while keeping each generation request shape unchanged.
    """

    binder_specifications: List[DataBinderSpecificationUniformlySampledBinderSpecBinderSpecification]
    """Binder specifications to sample uniformly when generating designs.

    Each generation samples one specification from this list; over larger runs this
    gives roughly equal representation.
    """

    type: Literal["uniformly_sampled_specifications"]


DataBinderSpecification: TypeAlias = Union[
    DataBinderSpecificationStructureTemplateBinderSpec,
    DataBinderSpecificationNoTemplateBinderSpec,
    DataBinderSpecificationBoltzCuratedBinderSpec,
    DataBinderSpecificationUniformlySampledBinderSpec,
]


class Data(BaseModel):
    binder_specification: DataBinderSpecification
    """Binder specification for protein design.

    Use no_template for sequence-defined binders, structure_template for uploaded
    binder structures, boltz_curated for Boltz-managed nanobody and antibody
    defaults, or uniformly_sampled_specifications to sample uniformly across
    multiple binder specifications.
    """

    name: str
    """Human-readable name for this curated binder specification."""


class DesignListCuratedSpecificationsResponse(BaseModel):
    data: List[Data]
