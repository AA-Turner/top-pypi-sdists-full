# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "LibraryScreenListResultsResponse",
    "Artifacts",
    "ArtifactsArchive",
    "ArtifactsStructure",
    "Entity",
    "EntityProteinEntity",
    "EntityProteinEntityModification",
    "EntityRnaEntity",
    "EntityRnaEntityModification",
    "EntityDnaEntity",
    "EntityDnaEntityModification",
    "EntityLigandCcdEntity",
    "EntityLigandSmilesEntity",
    "EntityGlycanEntity",
    "EntityGlycanEntityBond",
    "EntityGlycanEntityBondAtom1",
    "EntityGlycanEntityBondAtom2",
    "EntityGlycanEntityResidue",
    "Metrics",
    "Warning",
]


class ArtifactsArchive(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class ArtifactsStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class Artifacts(BaseModel):
    archive: ArtifactsArchive

    structure: ArtifactsStructure


class EntityProteinEntityModification(BaseModel):
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


class EntityProteinEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["protein"]

    value: str
    """Amino acid sequence (one-letter codes)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[EntityProteinEntityModification]] = None
    """CCD post-translational modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class EntityRnaEntityModification(BaseModel):
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


class EntityRnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["rna"]

    value: str
    """RNA nucleotide sequence (A, C, G, U, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[EntityRnaEntityModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class EntityDnaEntityModification(BaseModel):
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


class EntityDnaEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this entity"""

    type: Literal["dna"]

    value: str
    """DNA nucleotide sequence (A, C, G, T, N)"""

    cyclic: Optional[bool] = None
    """Whether the sequence is cyclic"""

    modifications: Optional[List[EntityDnaEntityModification]] = None
    """CCD chemical modifications.

    Optional; defaults to an empty list when omitted. SMILES modifications are not
    supported.
    """


class EntityLigandCcdEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_ccd"]

    value: str
    """One CCD code (for example ATP or ADP).

    This field remains a string; use a glycan entity for multiple connected CCD
    residues.
    """


class EntityLigandSmilesEntity(BaseModel):
    chain_ids: List[str]
    """Chain IDs for this ligand"""

    type: Literal["ligand_smiles"]

    value: str
    """SMILES string representing the ligand"""


class EntityGlycanEntityBondAtom1(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class EntityGlycanEntityBondAtom2(BaseModel):
    atom_id: str
    """Exact atom identifier from the residue CCD entry (\\__chem_comp_atom.atom_id)"""

    residue_id: str
    """Request-local ID of the glycan residue containing the atom"""


class EntityGlycanEntityBond(BaseModel):
    """Internal covalent bond between atoms in two residues of the glycan graph."""

    atom1: EntityGlycanEntityBondAtom1

    atom2: EntityGlycanEntityBondAtom2


class EntityGlycanEntityResidue(BaseModel):
    id: str
    """Request-local residue ID used by glycan bonds and external atom references"""

    ccd: str
    """CCD code for this monosaccharide residue (for example NAG, BMA, or FUC)"""


class EntityGlycanEntity(BaseModel):
    """Branched glycan represented as an explicit graph of CCD monosaccharide residues.

    Declare internal connectivity in this entity and cross-entity attachments in the request-level bonds array.
    """

    bonds: List[EntityGlycanEntityBond]
    """Internal covalent bonds connecting the glycan residues.

    A single-residue glycan uses an empty array.
    """

    chain_ids: List[str]
    """Chain IDs for identical copies of this glycan"""

    residues: List[EntityGlycanEntityResidue]
    """CCD residues in the glycan.

    Array order is not part of the public residue identity; bonds reference residue
    IDs.
    """

    type: Literal["glycan"]


Entity: TypeAlias = Union[
    EntityProteinEntity,
    EntityRnaEntity,
    EntityDnaEntity,
    EntityLigandCcdEntity,
    EntityLigandSmilesEntity,
    EntityGlycanEntity,
]


class Metrics(BaseModel):
    """Structural and binding quality metrics for a screened protein"""

    binding_confidence: float
    """Confidence that the protein binds the target (0-1).

    Primary metric for hit discovery.
    """

    helix_fraction: float
    """Fraction of the sequence forming alpha helices (0-1)."""

    iptm: float
    """Interface predicted TM score (0-1).

    Confidence in the protein-protein interface.
    """

    loop_fraction: float
    """Fraction of the sequence in coil/loop regions (0-1)."""

    min_interaction_pae: float
    """Minimum predicted aligned error at the interface (Angstroms).

    Lower values indicate higher confidence.
    """

    sheet_fraction: float
    """Fraction of the sequence forming beta sheets (0-1)."""

    structure_confidence: float
    """Confidence in the predicted 3D structure (0-1)."""

    ipsae_min: Optional[float] = None
    """
    Lower of the target-to-protein and protein-to-target ipSAE scores using a 10
    Angstrom PAE cutoff. Higher values indicate a more confidently predicted
    interface.
    """


class Warning(BaseModel):
    """A warning about a potential quality issue with a result"""

    code: str
    """Machine-readable warning code (e.g. "low_confidence", "unusual_geometry")"""

    message: str
    """Human-readable description of the warning"""


class LibraryScreenListResultsResponse(BaseModel):
    """Result for a single screened protein"""

    id: str
    """Unique result ID"""

    artifacts: Artifacts

    created_at: datetime

    entities: List[Entity]
    """Entities of the screened complex.

    Includes both screened and fixed entities from the input.
    """

    metrics: Metrics
    """Structural and binding quality metrics for a screened protein"""

    external_id: Optional[str] = None
    """Client-provided identifier for this protein, if provided"""

    warnings: Optional[List[Warning]] = None
    """Warnings about potential quality issues with this result."""
