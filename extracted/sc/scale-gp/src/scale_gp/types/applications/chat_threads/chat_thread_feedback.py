# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["ChatThreadFeedback"]


class ChatThreadFeedback(BaseModel):
    id: str

    application_interaction_id: str

    chat_thread_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    description: str

    sentiment: Literal["positive", "negative"]
