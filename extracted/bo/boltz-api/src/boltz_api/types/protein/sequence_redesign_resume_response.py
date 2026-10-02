# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "SequenceRedesignResumeResponse",
    "Error",
    "Input",
    "InputBinderProteinSequenceRedesignRunInputResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseEntity",
    "InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignTargetEntityResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotif",
    "InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilter",
    "InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterExcludedAminoAcidsDesignFilterResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterMaxHydrophobicFractionDesignFilterResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterExcludedSequenceMotifsDesignFilterResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseStructure",
    "InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilter",
    "InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedAminoAcidsDesignFilterResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterMaxHydrophobicFractionDesignFilterResponse",
    "InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedSequenceMotifsDesignFilterResponse",
    "InputGenericProteinSequenceRedesignRunInputResponse",
    "InputGenericProteinSequenceRedesignRunInputResponseEntity",
    "InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotif",
    "InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilter",
    "InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterExcludedAminoAcidsDesignFilterResponse",
    "InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterMaxHydrophobicFractionDesignFilterResponse",
    "InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterExcludedSequenceMotifsDesignFilterResponse",
    "InputGenericProteinSequenceRedesignRunInputResponseStructure",
    "InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilter",
    "InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedAminoAcidsDesignFilterResponse",
    "InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterMaxHydrophobicFractionDesignFilterResponse",
    "InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedSequenceMotifsDesignFilterResponse",
    "Progress",
]


class Error(BaseModel):
    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignTargetEntityResponse(BaseModel):
    """A fixed target chain from the input CIF."""

    chain_id: str

    role: Literal["target"]

    type: Literal["from_template"]


class InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterExcludedAminoAcidsDesignFilterResponse(
    BaseModel
):
    amino_acids: List[str]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Literal["excluded_amino_acids"]


class InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterMaxHydrophobicFractionDesignFilterResponse(
    BaseModel
):
    max_fraction: float

    type: Literal["max_hydrophobic_fraction"]


class InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterExcludedSequenceMotifsDesignFilterResponse(
    BaseModel
):
    motifs: List[str]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Literal["excluded_sequence_motifs"]


InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilter: TypeAlias = Union[
    InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterExcludedAminoAcidsDesignFilterResponse,
    InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterMaxHydrophobicFractionDesignFilterResponse,
    InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilterExcludedSequenceMotifsDesignFilterResponse,
]


class InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotif(
    BaseModel
):
    filters: List[
        InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotifFilter
    ]
    """Filters applied to this motif in addition to global_design_filters."""

    residues: List[int]
    """0-indexed residues to redesign on this chain."""

    type: Literal["residues"]


class InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponse(BaseModel):
    chain_id: str

    role: Literal["binder"]

    type: Literal["from_template"]

    design_motifs: Optional[
        List[
            InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponseDesignMotif
        ]
    ] = None
    """Residues to redesign. Omit this field to keep the binder chain fixed."""


InputBinderProteinSequenceRedesignRunInputResponseEntity: TypeAlias = Union[
    InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignTargetEntityResponse,
    InputBinderProteinSequenceRedesignRunInputResponseEntityBinderSequenceRedesignBinderEntityResponse,
]


class InputBinderProteinSequenceRedesignRunInputResponseStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedAminoAcidsDesignFilterResponse(
    BaseModel
):
    amino_acids: List[str]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Literal["excluded_amino_acids"]


class InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterMaxHydrophobicFractionDesignFilterResponse(
    BaseModel
):
    max_fraction: float

    type: Literal["max_hydrophobic_fraction"]


class InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedSequenceMotifsDesignFilterResponse(
    BaseModel
):
    motifs: List[str]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Literal["excluded_sequence_motifs"]


InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilter: TypeAlias = Union[
    InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedAminoAcidsDesignFilterResponse,
    InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterMaxHydrophobicFractionDesignFilterResponse,
    InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedSequenceMotifsDesignFilterResponse,
]


class InputBinderProteinSequenceRedesignRunInputResponse(BaseModel):
    entities: List[InputBinderProteinSequenceRedesignRunInputResponseEntity]
    """Every chain in the input CIF, assigned exactly once as target or binder."""

    num_proteins: int
    """Number of unique filter-passing redesigned proteins to generate."""

    structure: InputBinderProteinSequenceRedesignRunInputResponseStructure

    type: Literal["binder"]

    global_design_filters: Optional[List[InputBinderProteinSequenceRedesignRunInputResponseGlobalDesignFilter]] = None
    """Filters applied to every redesigned region.

    When omitted, cysteine is excluded. Pass [] to disable global filters.
    """

    idempotency_key: Optional[str] = None

    workspace_id: Optional[str] = None
    """Workspace to run this redesign in."""


class InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterExcludedAminoAcidsDesignFilterResponse(
    BaseModel
):
    amino_acids: List[str]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Literal["excluded_amino_acids"]


class InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterMaxHydrophobicFractionDesignFilterResponse(
    BaseModel
):
    max_fraction: float

    type: Literal["max_hydrophobic_fraction"]


class InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterExcludedSequenceMotifsDesignFilterResponse(
    BaseModel
):
    motifs: List[str]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Literal["excluded_sequence_motifs"]


InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilter: TypeAlias = Union[
    InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterExcludedAminoAcidsDesignFilterResponse,
    InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterMaxHydrophobicFractionDesignFilterResponse,
    InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilterExcludedSequenceMotifsDesignFilterResponse,
]


class InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotif(BaseModel):
    filters: List[InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotifFilter]
    """Filters applied to this motif in addition to global_design_filters."""

    residues: List[int]
    """0-indexed residues to redesign on this chain."""

    type: Literal["residues"]


class InputGenericProteinSequenceRedesignRunInputResponseEntity(BaseModel):
    chain_id: str

    type: Literal["from_template"]

    design_motifs: Optional[List[InputGenericProteinSequenceRedesignRunInputResponseEntityDesignMotif]] = None
    """Residues to redesign. Omit this field to keep the chain fixed."""


class InputGenericProteinSequenceRedesignRunInputResponseStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedAminoAcidsDesignFilterResponse(
    BaseModel
):
    amino_acids: List[str]
    """
    Single-letter amino-acid codes that must not occur in the filtered designed
    region.
    """

    type: Literal["excluded_amino_acids"]


class InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterMaxHydrophobicFractionDesignFilterResponse(
    BaseModel
):
    max_fraction: float

    type: Literal["max_hydrophobic_fraction"]


class InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedSequenceMotifsDesignFilterResponse(
    BaseModel
):
    motifs: List[str]
    """Sequence motifs that must not occur. X matches any single residue."""

    type: Literal["excluded_sequence_motifs"]


InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilter: TypeAlias = Union[
    InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedAminoAcidsDesignFilterResponse,
    InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterMaxHydrophobicFractionDesignFilterResponse,
    InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilterExcludedSequenceMotifsDesignFilterResponse,
]


class InputGenericProteinSequenceRedesignRunInputResponse(BaseModel):
    entities: List[InputGenericProteinSequenceRedesignRunInputResponseEntity]
    """Every chain in the input CIF, assigned exactly once."""

    num_proteins: int
    """Number of unique filter-passing redesigned proteins to generate."""

    structure: InputGenericProteinSequenceRedesignRunInputResponseStructure

    type: Literal["generic"]

    global_design_filters: Optional[List[InputGenericProteinSequenceRedesignRunInputResponseGlobalDesignFilter]] = None
    """Filters applied to every redesigned region.

    When omitted, cysteine is excluded. Pass [] to disable global filters.
    """

    idempotency_key: Optional[str] = None

    workspace_id: Optional[str] = None
    """Workspace to run this redesign in."""


Input: TypeAlias = Union[
    InputBinderProteinSequenceRedesignRunInputResponse, InputGenericProteinSequenceRedesignRunInputResponse, None
]


class Progress(BaseModel):
    num_proteins_generated: int
    """Number of protein designs generated so far"""

    total_proteins_to_generate: int
    """Total number of protein designs requested"""

    latest_result_id: Optional[str] = None
    """ID of the most recently generated result"""


class SequenceRedesignResumeResponse(BaseModel):
    """A fixed-structure protein sequence redesign run."""

    id: str
    """Unique ProteinSequenceRedesignRun identifier"""

    completed_at: Optional[datetime] = None

    created_at: datetime

    data_deleted_at: Optional[datetime] = None
    """When the input, output, and result data was permanently deleted.

    Null if data has not been deleted.
    """

    engine: Literal["boltz-protein-redesign"]
    """Deprecated. Use pipeline instead."""

    engine_version: Literal["v2026-07-14"]
    """Deprecated. Use pipeline_version instead."""

    error: Optional[Error] = None

    input: Optional[Input] = None
    """Pipeline input (null if data deleted)"""

    livemode: bool
    """Whether this resource was created with a live API key."""

    pipeline: Literal["boltz-protein-redesign"]

    pipeline_version: Literal["v2026-07-14"]

    progress: Optional[Progress] = None

    started_at: Optional[datetime] = None

    status: Literal["pending", "running", "succeeded", "failed", "stopped"]

    stopped_at: Optional[datetime] = None

    workspace_id: str
    """Workspace ID"""

    idempotency_key: Optional[str] = None
    """Client-provided idempotency key"""
