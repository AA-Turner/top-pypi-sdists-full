# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "SequenceRedesignListResultsResponse",
    "BinderProteinDesignResult",
    "BinderProteinDesignResultArtifacts",
    "BinderProteinDesignResultArtifactsArchive",
    "BinderProteinDesignResultArtifactsStructure",
    "BinderProteinDesignResultEntity",
    "BinderProteinDesignResultEntityProteinEntity",
    "BinderProteinDesignResultEntityProteinEntityModification",
    "BinderProteinDesignResultEntityRnaEntity",
    "BinderProteinDesignResultEntityRnaEntityModification",
    "BinderProteinDesignResultEntityDnaEntity",
    "BinderProteinDesignResultEntityDnaEntityModification",
    "BinderProteinDesignResultEntityLigandCcdEntity",
    "BinderProteinDesignResultEntityLigandSmilesEntity",
    "BinderProteinDesignResultEntityGlycanEntity",
    "BinderProteinDesignResultEntityGlycanEntityBond",
    "BinderProteinDesignResultEntityGlycanEntityBondAtom1",
    "BinderProteinDesignResultEntityGlycanEntityBondAtom2",
    "BinderProteinDesignResultEntityGlycanEntityResidue",
    "BinderProteinDesignResultMetrics",
    "BinderProteinDesignResultWarning",
    "GenericProteinDesignResult",
    "GenericProteinDesignResultArtifacts",
    "GenericProteinDesignResultArtifactsArchive",
    "GenericProteinDesignResultArtifactsStructure",
    "GenericProteinDesignResultEntity",
    "GenericProteinDesignResultEntityProteinEntity",
    "GenericProteinDesignResultEntityProteinEntityModification",
    "GenericProteinDesignResultEntityRnaEntity",
    "GenericProteinDesignResultEntityRnaEntityModification",
    "GenericProteinDesignResultEntityDnaEntity",
    "GenericProteinDesignResultEntityDnaEntityModification",
    "GenericProteinDesignResultEntityLigandCcdEntity",
    "GenericProteinDesignResultEntityLigandSmilesEntity",
    "GenericProteinDesignResultEntityGlycanEntity",
    "GenericProteinDesignResultEntityGlycanEntityBond",
    "GenericProteinDesignResultEntityGlycanEntityBondAtom1",
    "GenericProteinDesignResultEntityGlycanEntityBondAtom2",
    "GenericProteinDesignResultEntityGlycanEntityResidue",
    "GenericProteinDesignResultMetrics",
    "GenericProteinDesignResultWarning",
]


class BinderProteinDesignResultArtifactsArchive(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class BinderProteinDesignResultArtifactsStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class BinderProteinDesignResultArtifacts(BaseModel):
    archive: BinderProteinDesignResultArtifactsArchive

    structure: Optional[BinderProteinDesignResultArtifactsStructure] = None


class BinderProteinDesignResultEntityProteinEntityModification(BaseModel):
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


class BinderProteinDesignResultEntityProteinEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[BinderProteinDesignResultEntityProteinEntityModification]] = None
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class BinderProteinDesignResultEntityRnaEntityModification(BaseModel):
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


class BinderProteinDesignResultEntityRnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["rna"]

    value: str
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[BinderProteinDesignResultEntityRnaEntityModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class BinderProteinDesignResultEntityDnaEntityModification(BaseModel):
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


class BinderProteinDesignResultEntityDnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["dna"]

    value: str
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[BinderProteinDesignResultEntityDnaEntityModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class BinderProteinDesignResultEntityLigandCcdEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_ccd"]

    value: str
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class BinderProteinDesignResultEntityLigandSmilesEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_smiles"]

    value: str
    """SMILES string representing the ligand"""


class BinderProteinDesignResultEntityGlycanEntityBondAtom1(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class BinderProteinDesignResultEntityGlycanEntityBondAtom2(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class BinderProteinDesignResultEntityGlycanEntityBond(BaseModel):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: BinderProteinDesignResultEntityGlycanEntityBondAtom1

    atom2: BinderProteinDesignResultEntityGlycanEntityBondAtom2


class BinderProteinDesignResultEntityGlycanEntityResidue(BaseModel):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class BinderProteinDesignResultEntityGlycanEntity(BaseModel):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[BinderProteinDesignResultEntityGlycanEntityBond]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[BinderProteinDesignResultEntityGlycanEntityResidue]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


BinderProteinDesignResultEntity: TypeAlias = Union[
    BinderProteinDesignResultEntityProteinEntity,
    BinderProteinDesignResultEntityRnaEntity,
    BinderProteinDesignResultEntityDnaEntity,
    BinderProteinDesignResultEntityLigandCcdEntity,
    BinderProteinDesignResultEntityLigandSmilesEntity,
    BinderProteinDesignResultEntityGlycanEntity,
]


class BinderProteinDesignResultMetrics(BaseModel):
    """Structural and binding quality metrics for a designed protein binder"""

    binding_confidence: float
    """Confidence that the designed binder binds the target (0-1).

    Primary metric for hit discovery.
    """

    helix_fraction: float
    """Fraction of the designed sequence forming alpha helices (0-1)."""

    iptm: float
    """Interface predicted TM score (0-1).

    Confidence in the protein-protein interface.
    """

    loop_fraction: float
    """Fraction of the designed sequence in coil/loop regions (0-1)."""

    min_interaction_pae: float
    """Minimum predicted aligned error at the interface (Angstroms).

    Lower values indicate higher confidence.
    """

    sheet_fraction: float
    """Fraction of the designed sequence forming beta sheets (0-1)."""

    structure_confidence: float
    """Confidence in the predicted 3D structure (0-1)."""

    ipsae_min: Optional[float] = None
    """
    Lower of the target-to-binder and binder-to-target ipSAE scores using a 10
    Angstrom PAE cutoff. Higher values indicate a more confidently predicted
    interface.
    """


class BinderProteinDesignResultWarning(BaseModel):
    """A warning about a potential quality issue with a result"""

    code: str
    """Machine-readable warning code (e.g. "low_confidence", "unusual_geometry")"""

    message: str
    """Human-readable description of the warning"""


class BinderProteinDesignResult(BaseModel):
    id: str
    """Unique result ID."""

    artifacts: BinderProteinDesignResultArtifacts

    created_at: datetime

    entities: List[BinderProteinDesignResultEntity]
    """Designed and fixed entities returned for this result."""

    metrics: BinderProteinDesignResultMetrics
    """Structural and binding quality metrics for a designed protein binder"""

    type: Literal["binder"]

    warnings: Optional[List[BinderProteinDesignResultWarning]] = None
    """Warnings about potential quality issues with this result."""


class GenericProteinDesignResultArtifactsArchive(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class GenericProteinDesignResultArtifactsStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class GenericProteinDesignResultArtifacts(BaseModel):
    archive: GenericProteinDesignResultArtifactsArchive

    structure: Optional[GenericProteinDesignResultArtifactsStructure] = None


class GenericProteinDesignResultEntityProteinEntityModification(BaseModel):
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


class GenericProteinDesignResultEntityProteinEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[GenericProteinDesignResultEntityProteinEntityModification]] = None
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class GenericProteinDesignResultEntityRnaEntityModification(BaseModel):
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


class GenericProteinDesignResultEntityRnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["rna"]

    value: str
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[GenericProteinDesignResultEntityRnaEntityModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class GenericProteinDesignResultEntityDnaEntityModification(BaseModel):
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


class GenericProteinDesignResultEntityDnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["dna"]

    value: str
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[GenericProteinDesignResultEntityDnaEntityModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class GenericProteinDesignResultEntityLigandCcdEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_ccd"]

    value: str
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class GenericProteinDesignResultEntityLigandSmilesEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_smiles"]

    value: str
    """SMILES string representing the ligand"""


class GenericProteinDesignResultEntityGlycanEntityBondAtom1(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class GenericProteinDesignResultEntityGlycanEntityBondAtom2(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class GenericProteinDesignResultEntityGlycanEntityBond(BaseModel):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: GenericProteinDesignResultEntityGlycanEntityBondAtom1

    atom2: GenericProteinDesignResultEntityGlycanEntityBondAtom2


class GenericProteinDesignResultEntityGlycanEntityResidue(BaseModel):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class GenericProteinDesignResultEntityGlycanEntity(BaseModel):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[GenericProteinDesignResultEntityGlycanEntityBond]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[GenericProteinDesignResultEntityGlycanEntityResidue]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


GenericProteinDesignResultEntity: TypeAlias = Union[
    GenericProteinDesignResultEntityProteinEntity,
    GenericProteinDesignResultEntityRnaEntity,
    GenericProteinDesignResultEntityDnaEntity,
    GenericProteinDesignResultEntityLigandCcdEntity,
    GenericProteinDesignResultEntityLigandSmilesEntity,
    GenericProteinDesignResultEntityGlycanEntity,
]


class GenericProteinDesignResultMetrics(BaseModel):
    """Structure and design-quality metrics for a generic protein design."""

    helix_fraction: float
    """Fraction of the designed sequence forming alpha helices (0-1)."""

    loop_fraction: float
    """Fraction of the designed sequence in coil/loop regions (0-1)."""

    sheet_fraction: float
    """Fraction of the designed sequence forming beta sheets (0-1)."""

    structure_confidence: float
    """Confidence in the predicted 3D structure (0-1)."""


class GenericProteinDesignResultWarning(BaseModel):
    """A warning about a potential quality issue with a result"""

    code: str
    """Machine-readable warning code (e.g. "low_confidence", "unusual_geometry")"""

    message: str
    """Human-readable description of the warning"""


class GenericProteinDesignResult(BaseModel):
    id: str
    """Unique result ID."""

    artifacts: GenericProteinDesignResultArtifacts

    created_at: datetime

    entities: List[GenericProteinDesignResultEntity]
    """Designed and fixed entities returned for this result."""

    metrics: GenericProteinDesignResultMetrics
    """Structure and design-quality metrics for a generic protein design."""

    type: Literal["generic"]

    warnings: Optional[List[GenericProteinDesignResultWarning]] = None
    """Warnings about potential quality issues with this result."""


SequenceRedesignListResultsResponse: TypeAlias = Union[BinderProteinDesignResult, GenericProteinDesignResult]
