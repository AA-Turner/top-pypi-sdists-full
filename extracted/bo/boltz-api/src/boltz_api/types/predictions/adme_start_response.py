# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "AdmeStartResponse",
    "Error",
    "Input",
    "InputMolecule",
    "Output",
    "OutputMolecule",
    "OutputMoleculeAdmeMoleculeSucceeded",
    "OutputMoleculeAdmeMoleculeSucceededAdme",
    "OutputMoleculeAdmeMoleculeFailed",
    "OutputMoleculeAdmeMoleculeFailedError",
]


class Error(BaseModel):
    """Error details when failed"""

    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class InputMolecule(BaseModel):
    smiles: str
    """SMILES string of the molecule to predict ADME properties for."""

    id: Optional[str] = None
    """Optional client-provided identifier.

    Returned as `external_id` in the matching output item.
    """


class Input(BaseModel):
    """Prediction input (null if data deleted)"""

    molecules: List[InputMolecule]
    """Molecules to score (1-128 per request).

    Results are returned in the same order as this list.
    """


class OutputMoleculeAdmeMoleculeSucceededAdme(BaseModel):
    """Tier 1 ADME summary values for this molecule."""

    lipophilicity: float
    """Lipophilicity score from the internal LogD prediction."""

    permeability: float
    """Permeability score for this molecule."""

    solubility: Literal["high-confidence", "medium-confidence", "high-risk"]
    """Solubility judgement for this molecule."""


class OutputMoleculeAdmeMoleculeSucceeded(BaseModel):
    id: str
    """Internally generated molecule identifier."""

    adme: OutputMoleculeAdmeMoleculeSucceededAdme
    """Tier 1 ADME summary values for this molecule."""

    error: None = None

    smiles: str
    """Echoed SMILES from the request."""

    status: Literal["succeeded"]

    external_id: Optional[str] = None
    """Client-provided molecule identifier, if one was supplied."""


class OutputMoleculeAdmeMoleculeFailedError(BaseModel):
    code: str
    """Machine-readable error code"""

    message: str
    """Human-readable error message"""

    details: Optional[object] = None
    """Additional field-level error details keyed by input path, when available."""


class OutputMoleculeAdmeMoleculeFailed(BaseModel):
    id: str
    """Internally generated molecule identifier."""

    adme: None = None

    error: OutputMoleculeAdmeMoleculeFailedError

    smiles: str
    """Echoed SMILES from the request."""

    status: Literal["failed"]

    external_id: Optional[str] = None
    """Client-provided molecule identifier, if one was supplied."""


OutputMolecule: TypeAlias = Union[OutputMoleculeAdmeMoleculeSucceeded, OutputMoleculeAdmeMoleculeFailed]


class Output(BaseModel):
    """Prediction output when succeeded"""

    molecules: List[OutputMolecule]
    """Per-molecule results in the same order as the request.

    Successful molecules carry an `adme` summary. Failed molecules carry
    `status: "failed"` and a non-null `error`.
    """


class AdmeStartResponse(BaseModel):
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

    model: Literal["adme-v1"]
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
