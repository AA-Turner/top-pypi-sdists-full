# from letschatty.models.base_models.chatty_asset_model import ChattyAssetModel
# from letschatty.models.utils.definitions import Area
# from letschatty.models.messages.chatty_messages import ChattyMessage
# from letschatty.models.chat.highlight import Highlight
# from letschatty.models.chat.tag import Tag
# from letschatty.models.chat.client import Client
# from letschatty.models.chat.metadata import Metadata
# from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.chat.continuous_conversation import ContinuousConversation
from letschatty.models.chat.scheduled_messages import ScheduledMessages
from typing import List, Optional
from pydantic import BaseModel, Field
from letschatty.models.utils.definitions import Area
from letschatty.models.messages.chatty_messages import ChattyMessage
from letschatty.models.utils.types.identifier import StrObjectId
from letschatty.models.chat.client import Client
from datetime import datetime
# class Chat(ChattyAssetModel):
#     agent_id: Optional[str] = Field(default=None) #email of the agent that created the chat
#     client: Client
#     metadata_business: Metadata
#     area: Area
#     messages: List[ChattyMessage]
#     highlights: List[Highlight]
#     tags: List[Tag]
#     is_read_status: bool
#     starred: bool = False
#     free_conversation_expire_date: datetime
#     free_template_window_expire_date: datetime
#     time_left: dict
#     sent_fast_answers: set

class Chat(BaseModel):
    agent_id: Optional[str] = Field(default=None) #email of the agent that created the chat
    identifier: str
    id: StrObjectId
    continuous_conversations: Optional[List[ContinuousConversation]] = Field(default=[])
    scheduled_messages: Optional[List[ScheduledMessages]] = Field(default=[])
    is_free_conversation_active: bool
    area: Area
    client: Client
    messages: List[ChattyMessage]
    created_at: datetime

    @classmethod
    def mock_chat(cls):
        return cls(
            identifier="1234567890",
            continuous_conversations=[],
            is_free_conversation_active=False,
            area=Area.ARCHIVED,
            client=Client(waid="1234567890", name="John Doe"),
            messages=[]
        )

    def add_central_notification(self, message: str):
        return