from __future__ import annotations
from letschatty.models.chat.continuous_conversation import ContinuousConversation, ContinuousConversationStatus
from letschatty.models.utils.types.message_types import MessageType
from letschatty.models.messages.chatty_messages.base.message_draft import SendMessagesFromAgentToChat, MessageDraft
from letschatty.models.messages.chatty_messages import ChattyMessage
from letschatty.models.messages.chatty_messages.button import ButtonMessage
from typing import Optional, List, TYPE_CHECKING
from letschatty.services.messages_helpers import MessageTextOrCaptionOrPreview
from letschatty.models.messages.message_templates.filled_data_from_frontend import FilledTemplateData, FilledRecipientParameter, TemplateOrigin
from letschatty.models.messages.message_templates.raw_meta_template import WhatsappTemplate
from letschatty.services.factories.messages.central_notification_factory import CentralNotificationFactory
from letschatty.models.messages.chatty_messages.schema.chatty_content.content_central import ChattyContentCentral, CentralNotificationStatus
from letschatty.models.chat.scheduled_messages import ScheduledMessages
from letschatty.models.utils.custom_exceptions import NotFoundError
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from letschatty.models.utils.definitions import Area
from letschatty.services.chat.chat_service import ChatService
from letschatty.models.execution.execution import ExecutionContext
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from letschatty.models.chat.chat import Chat

class ContinuousConversationHelper:

    @staticmethod
    def build_filled_template_data(chat: Chat, cc: ContinuousConversation, template_name: str, param_name: str) -> FilledTemplateData:
        """
        Build the filled template data for a continuous conversation.
        """
        preview_message = ContinuousConversationHelper.get_preview_message(cc=cc)
        filled_recipient_parameters = [FilledRecipientParameter(id=param_name, text=preview_message)] #type: ignore
        filled_template_data = FilledTemplateData(
            template_name=template_name,
            area=chat.area,
            assign_to_agent=cc.creator_id if chat.area == Area.WITH_AGENT else None,
            phone_number=chat.client.waid,
            parameters=filled_recipient_parameters,
            description="Continuous conversation request",
            forced_send=True,
            origin=TemplateOrigin.FROM_CONTINUOUS_CONVERSATION
            )
        return filled_template_data
    @staticmethod

    def build_filled_template_data_for_phone_number(phone_number: str, cc: ContinuousConversation, template_name: str, param_name: str) -> FilledTemplateData:
        """
        Build the filled template data for a continuous conversation.
        """
        preview_message = ContinuousConversationHelper.get_preview_message(cc=cc)
        filled_recipient_parameters = [FilledRecipientParameter(id=param_name, text=preview_message)]  #type: ignore
        filled_template_data = FilledTemplateData(
            template_name=template_name,
            area=Area.WITH_AGENT,
            assign_to_agent=cc.creator_id,
            phone_number=phone_number,
            parameters=filled_recipient_parameters,
            description="Continuous conversation request",
            forced_send=True,
            origin=TemplateOrigin.FROM_CONTINUOUS_CONVERSATION
            )
        return filled_template_data

    @staticmethod
    def get_preview_message(cc: ContinuousConversation) -> Optional[str]:
        """
        Get the preview message for a continuous conversation.
        The preview is the first message of the continuous conversation (or a part of it if its too long, and it'll only be text for now)
        """
        preview_message = cc.messages[0]
        preview = MessageTextOrCaptionOrPreview.get_content_preview(message_content=preview_message.content)
        preview = preview.split("\n")[0]
        if len(preview) > 150:
            return preview[:150] + "..."
        else:
            return preview

    @staticmethod
    def create_continuous_conversation(chat: Chat, messages:List[MessageDraft], execution_context: ExecutionContext) -> ContinuousConversation:
        """
        Create a new continuous conversation from a list of messages.
        """
        active_cc = ContinuousConversationHelper.get_active_cc(chat)
        if active_cc:
            raise ValueError("There is already an active continuous conversation")
        cc = ContinuousConversation(messages=messages, creator_id=execution_context.executor.id, forced_send=False, created_at=datetime.now(ZoneInfo("UTC")), updated_at=datetime.now(ZoneInfo("UTC")))
        chat.continuous_conversations.append(cc)
        return cc

    @staticmethod
    def create_continuous_conversation_for_phone_number_without_chat(phone_number:str, messages:List[MessageDraft], execution_context: ExecutionContext) -> ContinuousConversation:
        """
        Create a new continuous conversation from a list of messages.
        """
        cc = ContinuousConversation(messages=messages, creator_id=execution_context.executor.id, forced_send=False, created_at=datetime.now(ZoneInfo("UTC")), updated_at=datetime.now(ZoneInfo("UTC")))
        return cc

    @staticmethod
    def update_continuous_conversation(chat: Chat, cc_id: str, messages: List[MessageDraft], execution_context: ExecutionContext) -> ContinuousConversation:
        """
        Update a continuous conversation from a list of messages.
        """
        cc = ContinuousConversationHelper.get_cc_by_id(chat=chat, cc_id=cc_id)
        if not cc.active:
            raise ValueError("Cannot update a non-active continuous conversation")
        new_cc = ContinuousConversation(_id=cc.id, messages=messages, creator_id=execution_context.executor.id, forced_send=False, created_at=datetime.now(ZoneInfo("UTC")), updated_at=datetime.now(ZoneInfo("UTC")))
        cc.messages = new_cc.messages
        cc.forced_send = new_cc.forced_send
        cc.expires_at = new_cc.expires_at
        cc.updated_at = datetime.now(ZoneInfo("UTC"))
        cc.creator_id = new_cc.creator_id
        return cc

    @staticmethod
    def get_active_cc(chat: Chat) -> Optional[ContinuousConversation]:
        """
        Check if a continuous conversation is active.
        """
        cc = next((cc for cc in chat.continuous_conversations if cc.active), None)
        if cc and cc.is_expired and not cc.forced_send:
            cc.set_status(status=ContinuousConversationStatus.EXPIRED)
            body = f"Continuous conversation expired at {cc.expires_at}"
            central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=[cta.value for cta in cc.calls_to_action])
            central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
            ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc

    @staticmethod
    def get_cc_by_message_id(chat: Chat, message_id: Optional[str]) -> Optional[ContinuousConversation]:
        """
        Get a continuous conversation by message id.
        """
        if message_id:
            return next((cc for cc in chat.continuous_conversations if cc.template_message_waid == message_id), None)
        else:
            return None

    @staticmethod
    def get_cc_by_id(chat: Chat, cc_id: str) ->ContinuousConversation:
        """
        Get a continuous conversation by id.
        """
        cc = next((cc for cc in chat.continuous_conversations if cc.id == cc_id), None)
        if not cc:
            raise NotFoundError(f"Continuous conversation with id {cc_id} not found")
        return cc

    @staticmethod
    def cancel_continuous_conversation(chat: Chat, cc_id: str, execution_context: ExecutionContext) -> ContinuousConversation:
        """
        Cancel a continuous conversation.

        Args:
            chat: The chat containing the CC
            cc_id: The ID of the CC to cancel

        Returns:
            The canceled continuous conversation, or None if not found
        """
        cc = ContinuousConversationHelper.get_cc_by_id(chat=chat, cc_id=cc_id)
        if cc:
            cc.set_status(status=ContinuousConversationStatus.CANCELLED)
            execution_context.set_event_time(datetime.now(ZoneInfo("UTC")))
            body = f"Continuous conversation cancelled by the agent {chat.agent_id}"
            logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
            central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.ERROR, calls_to_action=[cta.value for cta in cc.calls_to_action])
            central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
            ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        else:
            raise NotFoundError(f"Continuous conversation with id {cc_id} not found")
        return cc

    @staticmethod
    def get_cc_messages(chat: Chat, cc_id: str  ) -> List[MessageDraft]:
        """
        Get the messages of the active continuous conversation.
        """
        cc = next((cc for cc in chat.continuous_conversations if cc.id == cc_id), None)
        if not cc:
            raise ValueError(f"Continuous conversation with id {cc_id} not found")
        return cc.messages

    @staticmethod
    def handle_citing_inactive_cc_no_button_reply(chat: Chat, cc: ContinuousConversation, message: ChattyMessage) -> ContinuousConversation:
        """This is for the handling of a message from the user citing the CC when there's no active CC"""
        cc.set_status(status=ContinuousConversationStatus.OTHER_ANSWER)
        body = f"User sent a free message citing the CC but it wasn't active"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=[cta.value for cta in cc.calls_to_action]) #type: ignore
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc

    @staticmethod
    def handle_citing_active_cc_no_button_reply(chat: Chat, cc: ContinuousConversation, message: ChattyMessage) -> ContinuousConversation:
        """This is for the handling of a message from the user citing the CC when there's an active CC"""
        cc.set_status(status=ContinuousConversationStatus.OTHER_ANSWER)
        body="Continuous conversation ended because user sent a free message citing the CC"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=[cta.value for cta in cc.calls_to_action])
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc

    @staticmethod
    def handle_inactive_cc_rejected(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply rejecting the CC request when there's no active CC"""
        cc.set_status(status=ContinuousConversationStatus.REJECTED)
        body="Continuous conversation rejected by the user but it wasn't active"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=[cta.value for cta in cc.calls_to_action])
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc

    @staticmethod
    def handle_active_cc_rejected(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply rejecting the CC request when there's an active CC"""
        cc.set_status(status=ContinuousConversationStatus.REJECTED)
        body="Continuous conversation rejected by the user, not sending messages"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.ERROR, calls_to_action=[cta.value for cta in cc.calls_to_action])
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc


    @staticmethod
    def handle_inactive_cc_accepted(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply accepting the CC request when there's no active CC"""
        cc.set_status(status=ContinuousConversationStatus.APPROVED)
        body="Continuous conversation approved by the user but it wasn't active, not sending messages"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=[cta.value for cta in cc.calls_to_action])
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc

    @staticmethod
    def handle_active_cc_accepted(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        """This is for the handling of a button reply accepting the CC request when there's an active CC"""
        cc.set_status(status=ContinuousConversationStatus.APPROVED)
        body="Continuous conversation approved by the user, sending messages"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.SUCCESS)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc

    @staticmethod
    def handle_forced_send_cc(chat: Chat, cc: ContinuousConversation) -> ContinuousConversation:
        cc.set_status(status=ContinuousConversationStatus.FORCED_SENT)
        body="Sending Continuous Conversation messages because it was forced to be sent and user opened the free conversation back again"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.SUCCESS)
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc

    @staticmethod
    def handle_active_cc_non_related_message(chat: Chat, cc: ContinuousConversation, message: ChattyMessage) -> ContinuousConversation:
        """If we eventually want to apply NLP to detect if the message is related to a CC (if there's an active CC, here's where we'll do it)"""
        ###Here we need to add that if its a forced_send, we send the messages anyway
        cc.set_status(status=ContinuousConversationStatus.OTHER_ANSWER)
        body="Continuous conversation ended because user sent a free message (not a button reply)"
        logger.debug(f"{body} | CC status: {cc.status} | CC id: {cc.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=[cta.value for cta in cc.calls_to_action])
        central_notif = CentralNotificationFactory.continuous_conversation_status(cc=cc, content=central_notif_content)
        ChatService.add_central_notification(central_notification=central_notif, chat=chat)
        return cc