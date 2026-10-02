# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = [
    "DesignListResultsResponse",
    "Artifacts",
    "ArtifactsArchive",
    "ArtifactsStructure",
    "ArtifactsLigandStructure",
    "Metrics",
    "Adme",
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


class ArtifactsLigandStructure(BaseModel):
    url: str
    """URL to download the file"""

    url_expires_at: datetime
    """When the presigned URL expires"""


class Artifacts(BaseModel):
    archive: ArtifactsArchive

    structure: ArtifactsStructure

    ligand_structure: Optional[ArtifactsLigandStructure] = None


class Metrics(BaseModel):
    """Scoring metrics for a designed small molecule"""

    binding_confidence: float
    """Confidence that the molecule binds the target (0-1).

    Primary metric for hit discovery.
    """

    complex_iplddt: float
    """Interface pLDDT for the complex (0-1 float).

    Confidence at the binding interface.
    """

    complex_plddt: float
    """pLDDT for the full complex (0-1 float)."""

    iptm: float
    """Interface predicted TM score (0-1).

    Confidence in relative positioning of ligand and protein.
    """

    optimization_score: float
    """Binding strength ranking score for lead optimization.

    Higher values indicate stronger predicted binding.
    """

    ptm: float
    """Predicted TM score (0-1). Global structure quality metric."""

    structure_confidence: float
    """Confidence in the predicted 3D structure (0-1)."""


class Adme(BaseModel):
    """Tier 1 ADME summary values for this molecule."""

    lipophilicity: float
    """Lipophilicity score from the internal LogD prediction."""

    permeability: float
    """Permeability score for this molecule."""

    solubility: Literal["high-confidence", "medium-confidence", "high-risk"]
    """Solubility judgement for this molecule."""


class Warning(BaseModel):
    """A warning about a potential quality issue with a result"""

    code: str
    """Machine-readable warning code (e.g. "low_confidence", "unusual_geometry")"""

    message: str
    """Human-readable description of the warning"""


class DesignListResultsResponse(BaseModel):
    """A single designed small molecule result"""

    id: str
    """Unique result ID"""

    artifacts: Artifacts

    created_at: datetime

    metrics: Metrics
    """Scoring metrics for a designed small molecule"""

    smiles: str
    """SMILES string of the designed molecule"""

    adme: Optional[Adme] = None
    """Tier 1 ADME summary values for this molecule."""

    warnings: Optional[List[Warning]] = None
    """Warnings about potential quality issues with this result."""
