# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PromptListDefinitionsResponse", "PromptDefinition"]


class PromptDefinition(BaseModel):
    id: str
    """Unique identifier for the prompt definition"""

    created_at: datetime
    """Timestamp when the prompt definition was created"""

    name: str
    """Name of the prompt definition"""

    project_id: str
    """ID of the project this prompt belongs to"""

    project_name: str
    """Name of the project this prompt belongs to"""

    updated_at: datetime
    """Timestamp when the prompt definition was last updated"""

    description: Optional[str] = None
    """Optional description of the prompt's purpose or contents"""

    latest_revision: Optional[int] = None
    """Latest revision number, if available"""


class PromptListDefinitionsResponse(BaseModel):
    prompt_definitions: List[PromptDefinition]
