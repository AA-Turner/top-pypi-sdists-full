# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["MessageUpdateResponse"]


class MessageUpdateResponse(BaseModel):
    id: str

    aggregated: bool
    """
    Boolean of whether this interaction has been uploaded to s3 bucket yet, default
    is false
    """

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: Dict[str, object]

    operation_status: Literal["SUCCESS", "ERROR", "CANCELED"]
    """The outcome of the operation"""

    output: Dict[str, object]

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT", "AGENTS_SERVICE"]] = None

    models: Optional[List[str]] = None
    """The models used for this interaction"""

    operation_metadata: Optional[Dict[str, object]] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """
