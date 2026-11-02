from .chat import Chat
from letschatty.models.company.assets import TagPreview, FlowPreview, ContactPoint, Sale, ChattyAIAgentPreview, ProductPreview
from letschatty.models.company.CRM.funnel import ActiveFunnel

from letschatty.models.utils.types.serializer_type import SerializerType
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Optional
import json

class ChatAccountRef(BaseModel):
    """The number and WABA of the chat's WhatsApp account: what analytics events carry. No token."""
    model_config = ConfigDict(frozen=True)

    account_id: str
    phone_number_id: str
    waba_id: str


class ChatWithAssets(BaseModel):
    chat: Chat
    products: List[ProductPreview]
    tags: List[TagPreview]
    sales: List[Sale]
    contact_points: List[ContactPoint]
    flows_links_states: List[FlowPreview]
    chatty_ai_agent: Optional[ChattyAIAgentPreview]
    #: Set by the loader (it owns the account directory). Not serialized: it only feeds the events factory.
    account: Optional[ChatAccountRef] = Field(default=None, exclude=True)

    @property
    def person(self):
        """La persona completa (`clients`). El cargador la trae con `person=True`; sin eso, lanza."""
        return self.chat.person

    @property
    def active_funnel(self) -> Optional[ActiveFunnel]:
        """Convenience property to access the chat's active funnel"""
        return self.chat.active_funnel
