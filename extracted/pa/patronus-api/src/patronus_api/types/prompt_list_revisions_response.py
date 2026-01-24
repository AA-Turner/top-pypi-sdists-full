# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PromptListRevisionsResponse", "PromptRevision"]


class PromptRevision(BaseModel):
    id: str
    """Unique identifier for this specific prompt revision"""

    body: str
    """The actual content/text of the prompt - immutable for a specific revision"""

    created_at: datetime
    """Timestamp when this revision was created"""

    labels: List[str]
    """List of tags/labels associated with this specific revision"""

    normalized_body_sha256: str
    """SHA-256 hash of the prompt body with whitespace stripped from start and end"""

    project_id: str
    """ID of the project this prompt belongs to"""

    project_name: str
    """Name of the project this prompt belongs to"""

    prompt_definition_id: str
    """Identifier of the prompt definition this revision belongs to"""

    prompt_definition_name: str
    """Name of the prompt definition this revision belongs to"""

    revision: int
    """Sequential revision number, starting from 1 for the first version"""

    metadata: Optional[object] = None
    """Optional JSON metadata associated with this revision"""


class PromptListRevisionsResponse(BaseModel):
    prompt_revisions: List[PromptRevision]
