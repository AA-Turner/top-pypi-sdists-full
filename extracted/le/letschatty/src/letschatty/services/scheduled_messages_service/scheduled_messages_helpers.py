from letschatty.models.chat.continuous_conversation import ContinuousConversation, ContinuousConversationStatus
from letschatty.models.utils.types.message_types import MessageType
from letschatty.models.messages.chatty_messages.base.message_draft import SendMessagesFromAgentToChat, MessageDraft
from letschatty.models.chat.chat import Chat
from letschatty.models.messages.chatty_messages import ChattyMessage
from letschatty.models.messages.chatty_messages.button import ButtonMessage
from typing import Optional, List
from letschatty.models.messages.message_templates.filled_data_from_frontend import FilledTemplateData, FilledRecipientParameter, TemplateOrigin
from letschatty.models.messages.message_templates.raw_meta_template import WhatsappTemplate
from letschatty.services.factories.messages.central_notification_factory import CentralNotificationFactory
from letschatty.models.messages.chatty_messages.schema.chatty_content.content_central import ChattyContentCentral, CentralNotificationStatus
from letschatty.models.utils.custom_exceptions import NotFoundError
from letschatty.models.chat.scheduled_messages import ScheduledMessages, ScheduledMessageStatus, ScheduledMessageSubtype
from letschatty.services.chat.chat_service import ChatService
from letschatty.services.continuous_conversation_service.continuous_conversation_helper import ContinuousConversationHelper
from letschatty.models.execution.execution import ExecutionContext
import logging
logger = logging.getLogger(__name__)


class ScheduledMessagesHelper:

    @staticmethod
    def get_active_sms(chat: Chat) -> List[ScheduledMessages]:
        """
        Get the active scheduled messages from the chat and update their status if they are expired.
        """
        return [sm.update_if_expired() for sm in chat.scheduled_messages if sm.active]

    @staticmethod
    def get_sm_by_id(chat: Chat, sm_id: str) -> ScheduledMessages:
        """
        Get the scheduled message by id.
        """
        sm = next((sm.update_if_expired() for sm in chat.scheduled_messages if sm.id == sm_id), None)
        if sm is None:
            raise NotFoundError(f"Scheduled message {sm_id} not found")
        return sm

    @staticmethod
    def handle_new_incoming_message(chat: Chat) -> None:
        """
        Handle a new incoming message from the user.
        If the SM is not forced_send, set the status to ON_HOLD.
        """
        sms = ScheduledMessagesHelper.get_active_sms(chat)
        for sm in sms:
            if not sm.forced_send:
                sm.set_status(status=ScheduledMessageStatus.ON_HOLD)
                body = f"Scheduled message at {sm.scheduled_at} #{sm.id} set to ON_HOLD because of the new incoming message from the user"
                logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
                central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING)
                central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
                ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return None

    @staticmethod
    def release_hold_on_sm(chat: Chat, sm_id: str) -> ScheduledMessages:
        """
        Release the hold on the scheduled message.
        """
        sm = ScheduledMessagesHelper.get_sm_by_id(chat, sm_id)
        if sm.status != ScheduledMessageStatus.ON_HOLD:
            raise ValueError(f"Scheduled message {sm_id} is not on hold")
        sm.set_status(status=ScheduledMessageStatus.SCHEDULED)

        body = f"Scheduled message at {sm.scheduled_at} #{sm.id} released from hold by the agent {sm.creator_id}"
        logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.INFO)
        central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
        ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return sm

    @staticmethod
    def update_sm_free_message(chat: Chat, sm_id: str, messages_from_agent: SendMessagesFromAgentToChat, execution_context:ExecutionContext) -> ScheduledMessages:
        """
        Update the scheduled message with the new messages from the agent.
        """
        sm = ScheduledMessagesHelper.get_sm_by_id(chat, sm_id)
        if not sm.active:
            raise ValueError(f"Can't update inactive scheduled message {sm_id}")
        new_sm = ScheduledMessagesHelper.instantiate_sm_free_message(messages_from_agent, execution_context)
        sm.messages = new_sm.messages
        sm.scheduled_at = new_sm.scheduled_at
        sm.forced_send = new_sm.forced_send
        sm.creator_id = new_sm.creator_id
        sm.set_status(status=ScheduledMessageStatus.SCHEDULED)
        body = f"Scheduled message at {sm.scheduled_at} #{sm.id} updated by the agent {sm.creator_id}"
        logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.INFO)
        central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
        ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return sm

    @staticmethod
    def update_sm_template(chat: Chat, sm_id: str, filled_template_data: FilledTemplateData, execution_context:ExecutionContext) -> ScheduledMessages:
        """
        Update the scheduled message with the new filled template data.
        """
        sm = ScheduledMessagesHelper.get_sm_by_id(chat, sm_id)
        if not sm.active:
            raise ValueError(f"Can't update inactive scheduled message {sm_id}")
        new_sm = ScheduledMessagesHelper.instantiate_sm_template(filled_template_data)
        sm.filled_template_data = new_sm.filled_template_data
        sm.scheduled_at = new_sm.scheduled_at
        sm.forced_send = new_sm.forced_send
        sm.creator_id = new_sm.creator_id
        sm.update_now()
        execution_context.set_event_time(sm.updated_at)
        sm.set_status(status=ScheduledMessageStatus.SCHEDULED)
        body = f"Scheduled message at {sm.scheduled_at} #{sm.id} updated by the agent {sm.creator_id}"
        logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.INFO)
        central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
        ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return sm


    @staticmethod
    def instantiate_sm_free_message(messages_from_agent: SendMessagesFromAgentToChat, execution_context:ExecutionContext) -> ScheduledMessages:
        """
        Instantiate a new scheduled message from the messages from the agent.
        """
        logger.debug(f"Instantiating scheduled message from messages from the agent {execution_context.executor.id  }")
        return ScheduledMessages(messages=messages_from_agent.messages, scheduled_at=messages_from_agent.scheduled_at, forced_send=messages_from_agent.forced_send, creator_id=execution_context.executor.id, subtype=ScheduledMessageSubtype.FREE_MESSAGE) #type: ignore

    @staticmethod
    def create_sm(chat: Chat, messages_from_agent: SendMessagesFromAgentToChat) -> ScheduledMessages:
        """
        Create a new scheduled message from the messages from the agent.
        """
        sm = ScheduledMessages(messages=messages_from_agent.messages, scheduled_at=messages_from_agent.scheduled_at, forced_send=messages_from_agent.forced_send, agent_email=messages_from_agent.agent_email, subtype=ScheduledMessageSubtype.FREE_MESSAGE) #type: ignore
        chat.scheduled_messages.append(sm)
        body = f"Scheduled message at {sm.scheduled_at} #{sm.id} created by the agent {chat.agent_id}"

        logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.INFO)
        central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
        ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return sm

    @staticmethod
    def instantiate_sm_template(filled_template_data: FilledTemplateData) -> ScheduledMessages:
        """
        Instantiate a new scheduled message from the filled template data.
        """
        logger.debug(f"Instantiating scheduled message from filled template data {filled_template_data.template_name}")
        return ScheduledMessages(filled_template_data=filled_template_data, scheduled_at=filled_template_data.scheduled_at, forced_send=filled_template_data.forced_send, agent_email=filled_template_data.agent_email, subtype=ScheduledMessageSubtype.TEMPLATE) #type: ignore

    @staticmethod
    def create_sm_template(chat: Chat, filled_template_data: FilledTemplateData, execution_context:ExecutionContext) -> ScheduledMessages:
        """
        Create a new scheduled message from the filled template data.
        """
        sm = ScheduledMessages(filled_template_data=filled_template_data, scheduled_at=filled_template_data.scheduled_at, forced_send=filled_template_data.forced_send, agent_email=filled_template_data.creator_id, subtype=ScheduledMessageSubtype.TEMPLATE) #type: ignore
        chat.scheduled_messages.append(sm)
        body = f"Scheduled message at {sm.scheduled_at} #{sm.id} created by the agent {chat.agent_id}"
        logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.INFO)
        central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
        ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return sm

    @staticmethod
    def cancel_sm(chat: Chat, sm_id: str) -> ScheduledMessages:
        """
        Cancel a scheduled message.
        """
        sm = ScheduledMessagesHelper.get_sm_by_id(chat, sm_id)
        sm.set_status(status=ScheduledMessageStatus.CANCELLED)

        body = f"Scheduled message at {sm.scheduled_at} #{sm.id} cancelled by the agent {chat.agent_id}"
        logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.WARNING, calls_to_action=["get_scheduled_messages"])
        central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
        ChatService.add_central_notification(chat=chat, central_notification=central_notif)

        return sm

    @staticmethod
    def to_be_sent_sm(chat: Chat, sm_id: str) -> Optional[ScheduledMessages]:
        """
        Returns the scheduled message to be sent, or None if it there's nothing to do (maybe it's already sent or cancelled)
        """
        sm = ScheduledMessagesHelper.get_sm_by_id(chat, sm_id)
        if sm.status != ScheduledMessageStatus.SCHEDULED:
            return None
        if sm.subtype == ScheduledMessageSubtype.FREE_MESSAGE and not chat.is_free_conversation_active:
            sm.subtype = ScheduledMessageSubtype.CONTINUOUS_CONVERSATION
            body = f"Scheduled message at {sm.scheduled_at} #{sm.id} will be sent as a CONTINUOUS CONVERSATION because the free conversation is CLOSED"
            logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
            central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.INFO)
            central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
            ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return sm

    @staticmethod
    def sent_sm(chat: Chat, sm: ScheduledMessages) -> ScheduledMessages:
        """
        Scheduled message already sent.
        """
        sm.set_status(status=ScheduledMessageStatus.SENT)
        body = f"Scheduled message at {sm.scheduled_at} #{sm.id} sent"
        logger.debug(f"{body} | SM status: {sm.status} | SM id: {sm.id} | chat id: {chat.identifier}")
        central_notif_content = ChattyContentCentral(body=body, status=CentralNotificationStatus.SUCCESS)
        central_notif = CentralNotificationFactory.scheduled_message_status(sm=sm, content=central_notif_content)
        ChatService.add_central_notification(chat=chat, central_notification=central_notif)
        return sm
