from __future__ import annotations
from typing import Optional, Dict, Any, List, TYPE_CHECKING
from datetime import datetime, timedelta
from pydantic import Field, BaseModel, Field, model_validator, ConfigDict
from zoneinfo import ZoneInfo
from .client import Client
from ..utils.types.serializer_type import SerializerType
from ..messages.chatty_messages import ChattyMessage
from ..utils.types.message_types import MessageSubtype, MessageType
from ..base_models.chatty_asset_model import CompanyAssetModel
from ..utils.types.identifier import StrObjectId
from ..utils.definitions import Area
from .continuous_conversation import ContinuousConversation
from .scheduled_messages import ScheduledMessages
from .flow_link_state import FlowStateAssignedToChat
from ..company.assets.chat_assets import ChattyAIAgentAssignedToChat
from ..messages.chatty_messages.base.message_draft import MessageDraft
from ..utils.custom_exceptions.custom_exceptions import MissingAIAgentForSmartFollowUp
from .time_left import TimeLeft
import json
import logging
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..company.assets.chat_assets import AssignedAssetToChat, SaleAssignedToChat, ContactPointAssignedToChat
    from .highlight import Highlight
    from ..company.assets.sale import Sale
    from ..company.assets.contact_point import ContactPoint

class Chat(CompanyAssetModel):
    """
    Chat data model representing a conversation between a client and an agent.
    This model is stateless and only contains data.
    """
    client: Client
    channel_id: str = Field(description="The channel id where the Chat is happening")
    agent_id: Optional[StrObjectId] = Field(default=None, description="The id of the agents that's handling the chat if assigned")
    area: Area = Field(default=Area.WAITING_AGENT, description="Each Area represents a stage of the chat, it's an old naming that should eventually be renamed to status or StatusArea")
    messages: List[ChattyMessage] = Field(default_factory=list)
    is_read_status: bool = Field(default=False)
    starred: bool = Field(default=False)
    continuous_conversations: List[ContinuousConversation] = Field(default_factory=list)
    scheduled_messages: List[ScheduledMessages] = Field(default_factory=list)
    flow_states: List[FlowStateAssignedToChat] = Field(default_factory=list)
    chatty_ai_agent: Optional[ChattyAIAgentAssignedToChat] = Field(default=None, description="The id of the chatty ai agent that might or might not be assigned to the chat")
    suggested_messages: List[MessageDraft] = Field(default_factory=list)
    model_config = ConfigDict(extra="ignore")

    @property
    def has_active_cc(self) -> bool:
        """
        Check if a chat has an active continuous conversation.
        """
        return any(cc.active for cc in self.continuous_conversations)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Chat):
            return False
        return self.id == other.id

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Chat):
            return False
        return self.id != other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __gt__(self, other: Any) -> bool:
        """Compare two chats by the last message timestamp if any last message timestamp is None, compare by created_at"""
        if not isinstance(other, Chat):
            return False
        self_last_message_timestamp = self.last_message_timestamp if self.last_message_timestamp else self.created_at
        other_last_message_timestamp = other.last_message_timestamp if other.last_message_timestamp else other.created_at
        return self_last_message_timestamp > other_last_message_timestamp

    def __lt__(self, other: Any) -> bool:
        """Compare two chats by the last message timestamp if any last message timestamp is None, compare by created_at"""
        if not isinstance(other, Chat):
            return False
        self_last_message_timestamp = self.last_message_timestamp if self.last_message_timestamp else self.created_at
        other_last_message_timestamp = other.last_message_timestamp if other.last_message_timestamp else other.created_at
        return self_last_message_timestamp < other_last_message_timestamp

    @property
    def identifier(self) -> StrObjectId:
        return self.id

    @property
    def free_conversation_expire_date(self) -> datetime:
        """Get the expire date of the free conversation"""
        return self.last_incoming_message_timestamp + timedelta(hours=24) if self.last_incoming_message_timestamp else datetime.now(tz=ZoneInfo("UTC")) - timedelta(hours=1)

    @property
    def is_free_conversation_active(self) -> bool:
        """Check if the free conversation is active"""
        return self.free_conversation_expire_date > datetime.now(tz=ZoneInfo("UTC"))

    @property
    def time_left_for_free_conversation(self) -> float:
        """Get the time left for the free conversation in seconds"""
        return (self.free_conversation_expire_date - datetime.now(tz=ZoneInfo("UTC"))).total_seconds()

    @property
    def free_template_window_expire_date(self) -> datetime:
        """Get the expire date of the free template window"""
        expire_date_from_free_access_point = self.get_last_referal_incoming_message.created_at + timedelta(hours=72) if self.get_last_referal_incoming_message else datetime.now(tz=ZoneInfo("UTC")) - timedelta(hours=1)
        return expire_date_from_free_access_point

    @property
    def is_free_template_window_active(self) -> bool:
        """Check if the free template window is active"""
        return self.free_template_window_expire_date > datetime.now(tz=ZoneInfo("UTC"))

    @property
    def time_left_for_free_template_window(self) -> float:
        """Get the time left for the free template window in seconds"""
        return (self.free_template_window_expire_date - datetime.now(tz=ZoneInfo("UTC"))).total_seconds()

    @property
    def time_left(self) -> TimeLeft:
        """Get the time left for the free conversation and the free template window"""
        return TimeLeft.get_time_left(
            time_left_for_free_conversation_seconds=self.time_left_for_free_conversation,
            time_left_for_free_template_window_seconds=self.time_left_for_free_template_window
        )

    def is_chat_assigned_to_agent(self, agent_id: StrObjectId) -> bool:
        """Check if the chat is assigned to the AI agent"""
        return self.area == Area.WITH_AGENT and self.agent_id == agent_id

    def is_chat_assigned_to_another_agent(self, agent_id: StrObjectId) -> bool:
        """Check if the chat is assigned to the AI agent"""
        return self.is_chat_assigned_to_agent(agent_id=agent_id)

    @property
    def assigned_chatty_ai_agent(self) -> ChattyAIAgentAssignedToChat:
        """Get the assigned chatty ai agent"""
        if self.chatty_ai_agent is None:
            raise MissingAIAgentForSmartFollowUp(f"Chat {self.id} has no chatty ai agent assigned to it")
        return self.chatty_ai_agent


    @property
    def chat_has_ai_agent_assigned(self) -> bool:
        """Check if the chat is assigned to the AI agent"""
        return self.chatty_ai_agent is not None

    @property
    def sent_fast_answers_ids(self) -> List[StrObjectId]:
        """Load fast answers that have been sent in this chat"""
        sent_fast_answers_ids = []
        for message in self.messages:
            if message.subtype == MessageSubtype.CHATTY_FAST_ANSWER:
                sent_fast_answers_ids.append(message.context.response_id)
        return sent_fast_answers_ids

    @property
    def sent_templates(self) -> List[ChattyMessage]:
        """Load templates names that have been sent in this chat"""
        sent_templates: List[ChattyMessage] = []
        for message in self.messages:
            if message.is_template_message:
                sent_templates.append(message)
        return sent_templates

    @property
    def get_sent_templates_names(self) -> List[str]:
        """Load templates names that have been sent in this chat"""
        sent_templates: List[ChattyMessage] = self.sent_templates
        return [template.context.template_name for template in sent_templates] # type: ignore

    @property
    def last_message(self) -> Optional[ChattyMessage]:
        """Get the last non-central message in the chat"""
        for mensaje in reversed(self.messages):
            if mensaje.type != MessageType.CENTRAL:
                return mensaje
        return None

    @property
    def is_first_message(self) -> bool:
        """This is actually checking if it's the first time the user is writting to us based on the fact that all messages are incoming (still no answer from us)"""
        return (all(message.is_incoming_message for message in self.real_messages))

    @property
    def real_messages(self) -> List[ChattyMessage]:
        """Get the real messages in the chat"""
        return [message for message in self.messages if message.type != MessageType.CENTRAL]

    @property
    def last_message_timestamp(self) -> Optional[datetime]:
        """Get the timestamp of the last message in the chat"""
        last_message = self.last_message
        return last_message.created_at if last_message else None

    @property
    def last_incoming_message(self) -> Optional[ChattyMessage]:
        """Get the last incoming message in the chat"""
        for message in reversed(self.messages):
            if message.is_incoming_message:
                return message
        return None

    @property
    def last_incoming_message_timestamp(self) -> Optional[datetime]:
        """Get the timestamp of the last incoming message in the chat"""
        last_incoming_message = self.last_incoming_message
        return last_incoming_message.created_at if last_incoming_message else None

    @property
    def last_outgoing_message(self) -> Optional[ChattyMessage]:
        """Get the last outgoing message in the chat"""
        for message in reversed(self.messages):
            if not message.is_incoming_message and not message.type == MessageType.CENTRAL:
                return message
        return None

    @property
    def last_outgoing_message_timestamp(self) -> Optional[datetime]:
        """Get the timestamp of the last outgoing message in the chat"""
        last_outgoing_message = self.last_outgoing_message
        return last_outgoing_message.created_at if last_outgoing_message else None

    @property
    def get_last_referal_incoming_message(self) -> Optional[ChattyMessage]:
        """Get the last referal incoming message in the chat"""
        for message in reversed(self.messages):
            if message.is_incoming_message and not message.referral.is_default:
                return message
        return None

    @property
    def get_last_template_message_sent(self) -> Optional[ChattyMessage]:
        """Get the last template message sent in the chat"""
        for message in reversed(self.messages):
            if not message.is_incoming_message and message.context.template_name:
                return message
        return None

    @property
    def is_starred(self) -> bool:
        """Check if the chat is starred"""
        return self.starred

    @property
    def sales(self) -> List[SaleAssignedToChat]:
        """Get all sales in the chat"""
        return self.client.sales

    @property
    def bought_product_ids(self) -> List[StrObjectId]:
        """Get all sale ids in the chat"""
        return [sale.product_id for sale in self.sales]

    @property
    def products(self) -> List[AssignedAssetToChat]:
        """Get all products in the chat"""
        return self.client.products

    @property
    def assigned_product_ids(self) -> List[StrObjectId]:
        """Get all product ids in the chat"""
        return [product.asset_id for product in self.products]

    @property
    def tags(self) -> List[AssignedAssetToChat]:
        """Get all tags in the chat"""
        return self.client.tags

    @property
    def assigned_tag_ids(self) -> List[StrObjectId]:
        """Get all tag ids in the chat"""
        return [tag.asset_id for tag in self.tags]

    @property
    def highlights(self) -> List[Highlight]:
        """Get all highlights in the chat"""
        return self.client.highlights

    @property
    def contact_points(self) -> List[ContactPointAssignedToChat]:
        """Get all contact points in the chat"""
        return self.client.contact_points

    @property
    def assigned_source_ids(self) -> List[StrObjectId]:
        """Get all source ids in the chat"""
        return [contact_point.source_id for contact_point in self.contact_points]

    def get_all_tags(self) -> List[AssignedAssetToChat]:
        """Get all tags in the chat"""
        return self.client.tags

    def get_all_highlights(self) -> List[Highlight]:
        """Get all highlights in the chat"""
        return self.client.highlights

    def get_all_contact_points(self) -> List[ContactPointAssignedToChat]:
        """Get all contact points in the chat"""
        return self.contact_points

    def get_area(self) -> Area:
        """Get the area of the chat"""
        return self.area

    def is_read(self) -> bool:
        """Check if the chat is read"""
        return self.is_read_status

    def get_agent_id(self) -> Optional[StrObjectId]:
        """Get the agent id of the chat"""
        return self.agent_id


    def was_template_sent_to_chat(self, template_name: str) -> bool:
        """Check if a template was sent to the chat"""
        return template_name in self.get_sent_templates_names

    def get_templates_sent_to_chat(self) -> List[ChattyMessage]:
        """Get all templates sent to the chat"""
        #just because we had the method in previous version of Chat.
        return self.sent_templates

    def get_message_by_id(self, message_id: str) -> Optional[ChattyMessage]:
        """Get a message by its id"""
        for message in self.messages:
            if message.id == message_id:
                return message
        return None

    def get_time_delta_between_an_incoming_message_and_its_previous(self, message: ChattyMessage) -> Optional[timedelta]:
        """Get the time delta between an incoming message and its previous message"""
        for m in reversed(self.messages):
            if m.is_incoming_message and m.id != message.id:
                return message.created_at - m.created_at
        return None


    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        """Since we currently don't support all messages types in the frontend, we need to convert the message to a text message."""
        dump = super().model_dump_json(*args, **kwargs)
        serializer = kwargs.get('serializer', SerializerType.API)
        if serializer == SerializerType.DATABASE:
            dump["last_message_timestamp"]= self.last_message_timestamp
            dump["free_conversation_expire_date"] = self.free_conversation_expire_date
            dump["free_template_window_expire_date"] = self.free_template_window_expire_date
            dump["last_message"] = self.last_message.model_dump_json(serializer=SerializerType.DATABASE) if self.last_message else None
            dump["flow_states"] = [flow_state.model_dump_json(serializer=SerializerType.DATABASE) for flow_state in self.flow_states]
        return dump

