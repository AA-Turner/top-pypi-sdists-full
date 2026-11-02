# from ..base import Event, EventType
# from pydantic import BaseModel, Field
# from datetime import datetime
# from typing import Optional, List
# from ....utils.types.identifier import StrObjectId

# class MessagesIntentContextData(BaseModel):
#     company_id: StrObjectId
#     chat_id: StrObjectId
#     last_incoming_messages_embeddings: Optional[List[float]] = Field(default=None)
#     all_incoming_messages_embeddings: Optional[List[float]] = Field(default=None)
#     embedding_model_version: Optional[str] = Field(default=None, description="Version of embedding model used")
#     embedding_timestamp: Optional[datetime] = Field(default=None)

# class MessagesIntentContextEvent(Event):
#     type: EventType = EventType.MESSAGE_INTENT_CONTEXT
#     data: MessagesIntentContextData
