# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.identity import Identity
from .timestamp_question_configuration import TimestampQuestionConfiguration

__all__ = ["TimestampQuestion"]


class TimestampQuestion(BaseModel):
    id: str
    """Unique identifier of the entity"""

    created_at: datetime
    """ISO-timestamp when the entity was created"""

    created_by: Identity
    """The identity that created the entity."""

    name: str

    prompt: str
    """user-facing question prompt"""

    archived_at: Optional[datetime] = None
    """ISO-timestamp when the entity was archived"""

    conditions: Optional[List[Dict[str, object]]] = None
    """Conditions for the question to be shown"""

    configuration: Optional[TimestampQuestionConfiguration] = None

    object: Optional[Literal["question"]] = None

    question_type: Optional[Literal["timestamp"]] = None
