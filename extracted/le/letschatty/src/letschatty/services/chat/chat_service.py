from __future__ import annotations
from letschatty.models.chat.client import ClientData
from letschatty.models.chat.preview import ChatPreview, ClientPreview
from letschatty.models.company.assets.users.user import User
from letschatty.models.chat.time_left import TimeLeft, TimeLeftStatus
from letschatty.models.company.assets.tag import Tag
from letschatty.models.company.assets.sale import Sale
from letschatty.models.company.assets.flow import FlowPreview
from letschatty.models.messages.chatty_messages import ChattyMessage, CentralNotification
from letschatty.models.utils import Status, MessageSubtype
from letschatty.models.utils.definitions import Area
from letschatty.models.company.assets.contact_point import ContactPoint
from letschatty.models.chat.highlight import Highlight, HighlightRequestData
from letschatty.models.chat.quality_scoring import QualityScore
from letschatty.models.copilot.links import LinkItem
from letschatty.models.chat.flow_link_state import FlowStateAssignedToChat, SmartFollowUpState
from datetime import datetime
from typing import Dict, Any, Optional, List, TYPE_CHECKING
from letschatty.models.execution.execution import ExecutionContext
from letschatty.models.messages.meta_message_model.meta_status_json import ErrorDetail
from ...models.company.assets.product import Product
from ...models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from ...models.company.assets.ai_agents_v2.chatty_ai_mode import ChattyAIMode
from ...models.company.assets.chat_assets import SaleAssignedToChat, AssignedAssetToChat, ChatAssetType, ContactPointAssignedToChat, ChattyAIAgentAssignedToChat
from ...models.chat.scheduled_messages import ScheduledMessageStatus
from ...models.utils.types.identifier import StrObjectId
from ...models.utils.custom_exceptions.custom_exceptions import AssetAlreadyAssigned, MessageNotFoundError, NotFoundError, MessageAlreadyInChat, MetaErrorNotification, ChatAlreadyAssigned, AlreadyCompleted, ErrorToMantainSafety
from ..factories.messages.central_notification_factory import CentralNotificationFactory
from ...models.messages.chatty_messages.base.message_draft import MessageDraft
from ...models.messages.chatty_messages.schema.chatty_content.content_central import CentralNotificationStatus
from ...models.messages.chatty_messages.schema import ChattyContext
from ...models.utils.types.message_types import MessageType
import logging
import bisect
from ...models.analytics.events.chat_based_events.chat_context import ChatContext
from zoneinfo import ZoneInfo

if TYPE_CHECKING:
    from letschatty.models.chat.chat import Chat
    from letschatty.models.analytics.sources import Source
logger = logging.getLogger("ChatService")

class ChatService:

    @staticmethod
    def get_chat_context(chat: Chat) -> ChatContext:
        """
        Get the chat context for the chat.
        """
        return None #type: ignore

    @staticmethod
    def get_last_ctwa_clid(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last ctwa_clid from the chat.
        """
        contact_point_with_ctwa_clid = next((contact_point for contact_point in reversed(contact_points) if contact_point.ctwa_clid is not None), None)
        return contact_point_with_ctwa_clid.ctwa_clid if contact_point_with_ctwa_clid is not None else None

    @staticmethod
    def get_last_fbclid(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last fbclid from the chat.
        """
        contact_point_with_fbclid = next((contact_point for contact_point in reversed(contact_points) if contact_point.fb_clid is not None), None)
        return contact_point_with_fbclid.fb_clid if contact_point_with_fbclid is not None else None

    @staticmethod
    def get_last_gclid(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last gclid from the chat.
        """
        contact_point_with_gclid = next((contact_point for contact_point in reversed(contact_points) if contact_point.gclid is not None), None)
        return contact_point_with_gclid.gclid if contact_point_with_gclid is not None else None

    @staticmethod
    def get_last_ip_address(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last ip address from the chat.
        """
        contact_point_with_ip_address = next((contact_point for contact_point in reversed(contact_points) if contact_point.client_ip_address is not None), None)
        return contact_point_with_ip_address.client_ip_address if contact_point_with_ip_address is not None else None

    @staticmethod
    def get_last_user_agent(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last user agent from the chat.
        """
        contact_point_with_user_agent = next((contact_point for contact_point in reversed(contact_points) if contact_point.client_user_agent is not None), None)
        return contact_point_with_user_agent.client_user_agent if contact_point_with_user_agent is not None else None

    @staticmethod
    def get_external_id(chat: Chat) -> Optional[str]:
        """
        Get the external id from the chat.
        """
        return chat.client.external_id


    @staticmethod
    def add_product(chat : Chat, execution_context: ExecutionContext, product : Product) -> AssignedAssetToChat:
        """
        Add a product to the chat.
        """
        if next((product for product in chat.client.products if product.asset_id == product.id), None) is not None:
            raise AssetAlreadyAssigned(f"Product with id {product.id} already assigned to chat {chat.id}")
        assigned_asset = AssignedAssetToChat(
            asset_type=ChatAssetType.PRODUCT,
            asset_id=product.id,
            assigned_at=datetime.now(),
            assigned_by=execution_context.executor.id
        )
        execution_context.set_event_time(assigned_asset.assigned_at)
        bisect.insort(chat.client.products, assigned_asset)
        ChatService.add_central_notification_from_text(chat=chat, body=f"Producto {product.name} agregado al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.PRODUCT_ADDED)
        return assigned_asset

    @staticmethod
    def remove_product(chat : Chat, execution_context: ExecutionContext, product_id : StrObjectId) -> AssignedAssetToChat:
        """
        Remove a product from the chat.
        """
        try:
            assigned_asset_to_remove = next(product for product in chat.client.products if product.asset_id == product_id)
            chat.client.products.remove(assigned_asset_to_remove)
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            ChatService.add_central_notification_from_text(chat=chat, body=f"Producto {assigned_asset_to_remove.asset_id} eliminado del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.PRODUCT_DELETED)
            return assigned_asset_to_remove
        except StopIteration:
            raise NotFoundError(message=f"Product with id {product_id} not found in chat {chat.id}")

    @staticmethod
    def add_tag(chat : Chat, tag : Tag, execution_context: ExecutionContext) -> AssignedAssetToChat:
        """
        Add a tag to the chat.
        """
        if next((assigned_tag for assigned_tag in chat.client.tags if assigned_tag.asset_id == tag.id), None) is not None:
            raise AssetAlreadyAssigned(f"Tag with id {tag.id} already assigned to chat {chat.id}")
        assigned_asset = AssignedAssetToChat(
            asset_type=ChatAssetType.TAG,
            asset_id=tag.id,
            assigned_at=datetime.now(),
            assigned_by=execution_context.executor.id
        )
        execution_context.set_event_time(assigned_asset.assigned_at)
        bisect.insort(chat.client.tags, assigned_asset)
        ChatService.add_central_notification_from_text(chat=chat, body=f"Etiqueta {tag.name} agregada al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.TAG_ADDED)
        logger.debug(f"added tag {tag} to chat {chat.id}")
        return assigned_asset

    @staticmethod
    def remove_tag(chat : Chat, tag_id : StrObjectId, tag : Tag, execution_context: ExecutionContext) -> AssignedAssetToChat:
        """
        Remove a tag from the chat.
        """
        try:
            assigned_asset_to_remove = next(tag for tag in chat.client.tags if tag.asset_id == tag_id)
            chat.client.tags.remove(assigned_asset_to_remove)
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            ChatService.add_central_notification_from_text(chat=chat, body=f"Etiqueta {tag.name} eliminada del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.TAG_DELETED)
            return assigned_asset_to_remove
        except StopIteration:
            logger.info(f"Tag with id {tag_id} not found in chat {chat.id}")
            raise AlreadyCompleted(message=f"Tag with id {tag_id} not found in chat {chat.id}. Returning success")


    @staticmethod
    def add_chatty_ai_agent(chat : Chat, execution_context: ExecutionContext, chatty_ai_agent: ChattyAIAgent, mode_for_chat: Optional[ChattyAIMode] = None) -> AssignedAssetToChat:
        """
        Add a chatty ai agent config to the chat.
        """
        assigned_ai_agent = ChattyAIAgentAssignedToChat(
            asset_type=ChatAssetType.CHATTY_AI_AGENT,
            asset_id=chatty_ai_agent.id,
            assigned_at=datetime.now(tz=ZoneInfo("UTC")),
            assigned_by=execution_context.executor.id,
            mode=mode_for_chat if mode_for_chat else chatty_ai_agent.mode
        )
        execution_context.set_event_time(assigned_ai_agent.assigned_at)
        chat.chatty_ai_agent = assigned_ai_agent
        ChatService.add_central_notification_from_text(chat=chat, body=f"Agente de IA {chatty_ai_agent.name} agregado al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CHATTY_AI_AGENT_ADDED)
        return assigned_ai_agent

    @staticmethod
    def remove_chatty_ai_agent(chat : Chat, execution_context: ExecutionContext, chatty_ai_agent: ChattyAIAgent) -> ChattyAIAgentAssignedToChat:
        """
        Remove a chatty ai agent from the chat.
        """
        if chat.chatty_ai_agent is None:
            raise NotFoundError(message=f"Chatty AI agent not found in chat {chat.id}")
        current_chatty_ai_agent = chat.chatty_ai_agent
        chat.chatty_ai_agent = None
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"Agente de IA {chatty_ai_agent.name} eliminado del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CHATTY_AI_AGENT_DELETED)
        return current_chatty_ai_agent

    @staticmethod
    def update_chatty_ai_agent(chat : Chat, execution_context: ExecutionContext, chatty_ai_agent_id: StrObjectId,chatty_ai_agent: ChattyAIAgent, mode_for_chat: ChattyAIMode) -> ChattyAIAgentAssignedToChat:
        """
        Update a chatty ai agent for the chat.
        """
        if chat.chatty_ai_agent is None:
            raise NotFoundError(message=f"Chatty AI agent not found in chat {chat.id}")
        if chatty_ai_agent_id != chat.chatty_ai_agent.asset_id:
            raise NotFoundError(message=f"Chatty AI agent with id {chatty_ai_agent_id} not found in chat {chat.id}")
        chat.chatty_ai_agent.mode = mode_for_chat
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"Agente de IA {chatty_ai_agent.name} actualizado en el chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CHATTY_AI_AGENT_UPDATED)
        return chat.chatty_ai_agent

    @staticmethod
    def add_workflow_link(chat : Chat, link : LinkItem, flow:FlowPreview, execution_context: ExecutionContext, description: str, last_incoming_message_id: Optional[str] = None, next_call: Optional[datetime] = None) -> FlowStateAssignedToChat:
        """
        Add a tag to the chat.
        """
        if flow.is_smart_follow_up:
            current_smart_follow_up_state = next((state for state in chat.flow_states if state.is_smart_follow_up), None)
            if current_smart_follow_up_state is not None:
                raise AssetAlreadyAssigned(f"Smart follow up with id {link.flow_id} already assigned to chat {chat.id}")
        state = FlowStateAssignedToChat.from_link(link=link, execution_context=execution_context, description=description, last_incoming_message_id=last_incoming_message_id, next_call=next_call, is_smart_follow_up=flow.is_smart_follow_up)
        if state in chat.flow_states:
            raise AssetAlreadyAssigned(f"Flow with id {link.flow_id} already assigned to chat {chat.id}")
        execution_context.set_event_time(state.assigned_at)
        bisect.insort(chat.flow_states, state)
        ChatService.add_central_notification_from_text(chat=chat, body=f"Workflow {flow.title} agregada al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.WORKFLOW_ADDED)
        return state

    @staticmethod
    def remove_workflow_link(chat : Chat, workflow_id : StrObjectId, flow:FlowPreview, execution_context: ExecutionContext) -> FlowStateAssignedToChat:
        """
        Remove a tag from the chat.
        """
        try:
            assigned_asset_to_remove = next(state for state in chat.flow_states if state.flow_id == workflow_id)
            chat.flow_states.remove(assigned_asset_to_remove)
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            ChatService.add_central_notification_from_text(chat=chat, body=f"Workflow {flow.title} eliminada del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.WORKFLOW_DELETED)
            return assigned_asset_to_remove
        except StopIteration:
            raise NotFoundError(message=f"Workflow with id {workflow_id} not found in chat {chat.id}")

    @staticmethod
    def update_workflow_link(chat : Chat, workflow_id : StrObjectId, workflow_link: FlowStateAssignedToChat, execution_context: ExecutionContext) -> FlowStateAssignedToChat:
        """
        Update a workflow link for the chat.
        """
        logger.debug(f"Updating workflow link for chat {chat.id} with workflow {workflow_id} and workflow link {workflow_link}")
        assigned_asset_to_remove = next(state for state in chat.flow_states if state.flow_id == workflow_id)
        logger.debug(f"Assigned asset to remove: {assigned_asset_to_remove}")
        chat.flow_states.remove(assigned_asset_to_remove)
        logger.debug(f"Chat flow states: {chat.flow_states}")
        bisect.insort(chat.flow_states, workflow_link)
        logger.debug(f"Chat flow states after inserting the updated workflow link: {chat.flow_states}")
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return workflow_link

    @staticmethod
    def get_smart_follow_up_state(chat : Chat) -> Optional[SmartFollowUpState]:
        """
        Get the smart follow up state for the chat.
        """
        return next((state for state in chat.flow_states if isinstance(state, SmartFollowUpState)), None)

    @staticmethod
    def create_sale(chat : Chat, execution_context: ExecutionContext, sale : Sale, product : Product) -> SaleAssignedToChat:
        """
        Add a sale to the chat.
        """
        if next((sale for sale in chat.client.sales if sale.asset_id == sale.id), None) is not None:
            raise AssetAlreadyAssigned(f"Sale with id {sale.id} already assigned to chat {chat.id}")
        assigned_asset = SaleAssignedToChat(
            asset_type=ChatAssetType.SALE,
            asset_id=sale.id,
            assigned_at=sale.created_at,
            assigned_by=execution_context.executor.id,
            product_id=product.id
        )
        execution_context.set_event_time(assigned_asset.assigned_at)
        bisect.insort(chat.client.sales, assigned_asset)
        ChatService.create_highlight(chat=chat, execution_context=execution_context, highlight_data=HighlightRequestData(title=f"🛍️ Venta de {product.name}", description=f"Venta de {product.name} creada por {execution_context.executor.name}", starred=False, subtype=MessageSubtype.SALE_ADDED))
        ChatService.add_central_notification_from_text(chat=chat, body=f"Venta de {product.name} agregada al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.SALE_ADDED)
        return assigned_asset

    @staticmethod
    def update_sale(chat : Chat, execution_context: ExecutionContext, sale : Sale, product : Product) -> Sale:
        """
        Update a sale for the chat.
        """
        ChatService.create_highlight(chat=chat, execution_context=execution_context, highlight_data=HighlightRequestData(title=f"🛍️ Venta actualizada de {product.name}", description=f"Venta de {product.name} actualizada por {execution_context.executor.name}", starred=False, subtype=MessageSubtype.SALE_UPDATED))
        ChatService.add_central_notification_from_text(chat=chat, body=f"Venta de {product.name} actualizada en el chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.SALE_UPDATED)
        return sale

    @staticmethod
    def delete_sale(chat : Chat, execution_context: ExecutionContext, sale_id : StrObjectId, product : Product) -> SaleAssignedToChat:
        """
        Logically remove a sale from the chat.
        """
        try:
            assigned_asset_to_remove = next(sale for sale in chat.client.sales if sale.asset_id == sale_id)
            chat.client.sales.remove(assigned_asset_to_remove)
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            ChatService.create_highlight(chat=chat, execution_context=execution_context, highlight_data=HighlightRequestData(title=f"🛍️ Venta eliminada de {product.name}", description=f"Venta de {product.name} eliminada por {execution_context.executor.name}", starred=False, subtype=MessageSubtype.SALE_DELETED))
            ChatService.add_central_notification_from_text(chat=chat, body=f"Venta de {product.name} eliminada del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.SALE_DELETED)
            return assigned_asset_to_remove
        except StopIteration:
            raise NotFoundError(message=f"Sale with id {sale_id} not found in chat {chat.id}")

    @staticmethod
    def create_highlight(chat : Chat, execution_context: ExecutionContext, highlight_data: HighlightRequestData) -> Highlight:
        """
        Create a highlight for the chat.
        """
        highlight = Highlight(
            title=highlight_data.title,
            description=highlight_data.description,
            creator_id=execution_context.executor.id,
            starred=highlight_data.starred,
            subtype=highlight_data.subtype
        ) #type: ignore
        execution_context.set_event_time(highlight.created_at)
        bisect.insort(chat.client.highlights, highlight)
        # Sort highlights in descending order by created_at timestamp
        chat.client.highlights.sort(reverse=True)
        ChatService.add_central_notification_from_text(chat=chat, body=f"Highlight {highlight.title} agregado al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.HIGHLIGHT_ADDED)
        return highlight

    @staticmethod
    def update_highlight(chat : Chat, execution_context: ExecutionContext, highlight_id : StrObjectId, highlight_data: HighlightRequestData) -> Highlight:
        """
        Update a highlight for the chat.
        """
        try:
            highlight_to_update = next(highlight for highlight in chat.client.highlights if highlight.id == highlight_id)
            highlight = Highlight(
                title=highlight_data.title,
                description=highlight_data.description,
                creator_id=execution_context.executor.id,
                starred=highlight_data.starred,
                subtype=highlight_data.subtype
            ) #type: ignore
            updated_highlight = highlight_to_update.update(highlight)
            chat.client.highlights.remove(highlight_to_update)
            bisect.insort(chat.client.highlights, updated_highlight)
            # Sort highlights in descending order by created_at timestamp
            chat.client.highlights.sort(reverse=True)
            execution_context.set_event_time(updated_highlight.updated_at)
            CentralNotificationFactory.from_notification_body(f"Highlight {highlight_to_update.title} actualizado en el chat {chat.id} por {execution_context.executor.name}", MessageSubtype.HIGHLIGHT_UPDATED)
            return updated_highlight
        except StopIteration:
            raise NotFoundError(message=f"Highlight with id {highlight_id} not found in chat {chat.id}")

    @staticmethod
    def delete_highlight(chat : Chat, execution_context: ExecutionContext, highlight_id : StrObjectId) -> Highlight:
        """
        Logically remove a highlight from the chat.
        """
        try:
            highlight = next(highlight for highlight in chat.client.highlights if highlight.id == highlight_id)
            chat.client.highlights.remove(highlight)
            # Sort highlights in descending order by created_at timestamp
            chat.client.highlights.sort(reverse=True)
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            ChatService.add_central_notification_from_text(chat=chat, body=f"Highlight #{highlight.title} eliminado del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.HIGHLIGHT_DELETED)
            return highlight
        except StopIteration:
            raise NotFoundError(message=f"Highlight with id {highlight_id} not found in chat {chat.id}")

    @staticmethod
    def add_contact_point(chat : Chat, execution_context: ExecutionContext, contact_point : ContactPoint, source : Source) -> ContactPointAssignedToChat:
        """
        Add a contact point to the chat.
        """
        if next((contact_point for contact_point in chat.client.contact_points if contact_point.asset_id == contact_point.id), None) is not None:
            raise AssetAlreadyAssigned(f"Contact point with id {contact_point.id} already assigned to chat {chat.id}")
        assigned_asset = ContactPointAssignedToChat(
            asset_type=ChatAssetType.CONTACT_POINT,
            asset_id=contact_point.id,
            assigned_at=contact_point.created_at,
            assigned_by=execution_context.executor.id,
            source_id=contact_point.matched_source_id
        )
        bisect.insort(chat.client.contact_points, assigned_asset)
        ChatService.add_central_notification_from_text(chat=chat, body=f"TouchPoint de la fuente {source.name} agregado al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CONTACT_POINT_ADDED)
        return assigned_asset

    @staticmethod
    def update_contact_point(chat : Chat, execution_context: ExecutionContext, contact_point : ContactPoint, source : Source) -> ContactPoint:
        """
        Update a contact point for the chat.
        """
        ChatService.add_central_notification_from_text(chat=chat, body=f"TouchPoint de la fuente {source.name} actualizado en el chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CONTACT_POINT_UPDATED)
        return contact_point

    @staticmethod
    def delete_contact_point(chat : Chat, execution_context: ExecutionContext, contact_point_id : StrObjectId, contact_point : ContactPoint, source : Source) -> ContactPointAssignedToChat:
        """
        Logically remove a contact point from the chat.
        """
        try:
            assigned_asset_to_remove = next(contact_point for contact_point in chat.client.contact_points if contact_point.asset_id == contact_point_id)
            chat.client.contact_points.remove(assigned_asset_to_remove)
            ChatService.add_central_notification_from_text(chat=chat, body=f"TouchPoint de la fuente {source.name} eliminado del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CONTACT_POINT_DELETED)
            return assigned_asset_to_remove
        except StopIteration:
            raise NotFoundError(message=f"TouchPoint de la fuente {source.name} not found in chat {chat.id}")

    @staticmethod
    def add_message(chat : Chat, message : ChattyMessage) -> ChattyMessage:
        """
        Add a message to the chat.
        """
        if message in chat.messages:
            raise MessageAlreadyInChat(f"Message with id {message.id} already in chat {chat.id}")
        bisect.insort(chat.messages, message)
        logger.debug(f"Added message to chat {chat.id}: {message}")
        return message

    @staticmethod
    def update_message_status(chat : Chat, message_id : str, status : Status, error_details : Optional[ErrorDetail] = None ) -> ChattyMessage:
        """
        Update the status of a message in the chat.
        """
        message = chat.get_message_by_id(message_id)
        if message is None:
            # logger.warning(f"Message with id {message_id} not found in chat {chat.id}")
            raise MessageNotFoundError(message=f"Message with id {message_id} not found in chat {chat.id}")

        message.update_status(new_status=status, status_datetime=datetime.now())
        if message.subtype == MessageSubtype.TEMPLATE and status == Status.FAILED and error_details is not None:
            ChatService.add_central_notification_from_text(chat=chat, body=f"La plantilla de mensaje {message.context.template_name} falló: {error_details.get_error_details()}", subtype=MessageSubtype.META_ERROR, content_status=CentralNotificationStatus.ERROR)

            logger.warning(f"Template {message.context.template_name} failed: {error_details.get_error_details()}")
            raise MetaErrorNotification(message=f"Template {message.context.template_name} failed", status_code=400, chat_id=chat.identifier, details=error_details.get_more_info())
        return message

    @staticmethod
    def add_central_notification_from_text(chat : Chat, body:str, subtype:MessageSubtype = MessageSubtype.SYSTEM, content_status:CentralNotificationStatus = CentralNotificationStatus.INFO, context:ChattyContext | None = None) -> CentralNotification:
        """
        Add a central notification to the chat.
        """
        central_notification = CentralNotificationFactory.from_notification_body(notification_body=body, subtype=subtype, content_status=content_status, context=context)
        ChatService.add_message(chat=chat, message=central_notification)
        return central_notification

    @staticmethod
    def add_central_notification(chat : Chat, central_notification : CentralNotification) -> CentralNotification:
        """
        Add a central notification to the chat.
        """
        ChatService.add_message(chat=chat, message=central_notification)
        return central_notification

    @staticmethod
    def star_chat(chat : Chat, execution_context: ExecutionContext) -> Chat:
        """
        Star a chat.
        """
        if chat.starred:
            raise ValueError(f"Chat {chat.id} is already starred")
        chat.starred = True
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue marcado como destacado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_STARRED)
        return chat

    @staticmethod
    def unstar_chat(chat : Chat, execution_context: ExecutionContext) -> Chat:
        """
        Unstar a chat.
        """
        if not chat.starred:
            raise ValueError(f"Chat {chat.id} is not starred")
        chat.starred = False
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue desmarcado como destacado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_UNSTARRED)
        return chat

    @staticmethod
    def archive_chat(chat : Chat, execution_context: ExecutionContext, current_agent:Optional[User]) -> Chat:
        """
        Archive a chat.
        """
        if chat.area == Area.ARCHIVED:
            raise AlreadyCompleted(f"Chat {chat.id} is already archived")
        if current_agent and current_agent.id != execution_context.executor.id: #notify the previous agent
            ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue archivado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_ARCHIVED)
        else:
            ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue archivado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_ARCHIVED)
        chat.area = Area.ARCHIVED
        chat.agent_id = None
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat

    @staticmethod
    def unarchive_chat(chat : Chat, execution_context: ExecutionContext) -> Chat:
        """
        Unarchive a chat.
        """
        if chat.area != Area.ARCHIVED:
            raise ValueError(f"Chat {chat.id} is not archived")
        chat.area = Area.WAITING_AGENT
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue desarchivado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_UNARCHIVED)
        return chat

    @staticmethod
    def assign_chat(chat : Chat, agent_destination:User, execution_context: ExecutionContext, current_agent:Optional[User]) -> Chat:
        """
        Assign a chat to an agent.
        """
        logger.debug(f"Assigning chat to {agent_destination.name} - Current agent: {current_agent.name if current_agent else 'None'}")
        if current_agent is None: #No current agent - So its an assignment
            logger.debug(f"Assigning chat to {agent_destination.name} - No current agent - So its an assignment")
            if agent_destination.id != execution_context.executor.id:
                logger.debug(f"Destination is not the executor - So its a transfer")
                ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue asignado a {agent_destination.name} por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_ASSIGNED)
            else:
                #assigned by itself
                logger.debug(f"Assigned to itself")
                ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue asignado a {agent_destination.name} por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_ASSIGNED)
        elif current_agent.id == agent_destination.id:
            logger.debug(f"Chat {chat.id} already assigned to {agent_destination.name}")
        elif current_agent.id != execution_context.executor.id: #Chat is already assigned, so its a transfer
            if execution_context.is_integration:
                raise ErrorToMantainSafety(f"An integration user is trying to STEAL a chat from {current_agent.name} to {agent_destination.name} | Chat {chat.id} | is {chat.area} | is assigned to {agent_destination.name} by {execution_context.executor.name} | This is a safety warning")
            logger.debug(f"Chat is already assigned, so its a transfer")
            if agent_destination.id != execution_context.executor.id:                 #notify the previous agent and the new one
                logger.debug(f"Destination is not the executor - So its a transfer")
                ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue transferido de {current_agent.name} a {agent_destination.name} por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_TRANSFERRED)
            else:                 #notify the previous agent
                logger.debug(f"Assigned to itself")
                ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue transferido de {current_agent.name} a {agent_destination.name} por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_TRANSFERRED)
        chat.agent_id = agent_destination.id
        chat.area = Area.WITH_AGENT
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        logger.debug(f"Chat assigned to {agent_destination.name}")
        return chat

    @staticmethod
    def desassign_chat(chat : Chat, execution_context:ExecutionContext, current_agent:User) -> Chat:
        """
        Desassign a chat from an agent.
        """
        if chat.area != Area.WITH_AGENT:
            raise AlreadyCompleted(f"Chat {chat.id} is already not assigned to any agent")
        if current_agent.id == execution_context.executor.id:
            ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue desasignado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_DESASSIGNED)
        else: #notify the previous agent
            ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue transferido de {current_agent.name} a {execution_context.executor.name} por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_TRANSFERRED)
        chat.agent_id = None
        chat.area = Area.WAITING_AGENT
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat

    @staticmethod
    def read_chat(chat : Chat, execution_context:ExecutionContext) -> Chat:
        """
        Read a chat.
        """
        if chat.is_read_status:
            raise AlreadyCompleted(f"Chat {chat.id} was already read")
        chat.is_read_status = True
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat

    @staticmethod
    def unread_chat(chat : Chat, execution_context:ExecutionContext) -> Chat:
        """
        Unread a chat.
        """
        if not chat.is_read_status:
            raise AlreadyCompleted(f"Chat {chat.id} was already unread")
        chat.is_read_status = False
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat


    @staticmethod
    def get_scheduled_message_status_for_preview(chat: Chat) -> Optional[ScheduledMessageStatus]:
        """
        Get the scheduled message status for the preview of the chat.
        """
        if any(scheduled_message.status == ScheduledMessageStatus.EXPIRED_ON_HOLD for scheduled_message in chat.scheduled_messages):
            return ScheduledMessageStatus.EXPIRED_ON_HOLD
        if any(scheduled_message.status == ScheduledMessageStatus.ON_HOLD for scheduled_message in chat.scheduled_messages):
            return ScheduledMessageStatus.ON_HOLD
        if any(scheduled_message.status == ScheduledMessageStatus.SCHEDULED for scheduled_message in chat.scheduled_messages):
            return ScheduledMessageStatus.SCHEDULED
        return None

    @staticmethod
    def get_previous_message(chat: Chat, message: ChattyMessage) -> Optional[ChattyMessage]:
        """
        Get the previous message in the chat to the given message.
        """
        next = False
        for msg in reversed(chat.messages):
            if msg.id == message.id:
                next = True
            if next and msg.type != MessageType.CENTRAL:
                return msg
        return None

    @staticmethod
    def is_first_response(chat: Chat, message: ChattyMessage) -> bool:
        """
        Check if the message is the first response in the chat.
        """
        previous_message = ChatService.get_previous_message(chat, message)
        if previous_message is None:
            return False
        if not previous_message.is_incoming_message:
            return False
        return True

    @staticmethod
    def get_response_time(chat: Chat, message: ChattyMessage) -> Optional[int]:
        """
        Get the response time of the message.
        """
        if message.is_incoming_message:
            last_incoming_message = chat.last_incoming_message
            if last_incoming_message is None:
                return None
            return int((message.created_at - last_incoming_message.created_at).total_seconds())
        else:
            last_outgoing_message = chat.last_outgoing_message
            if last_outgoing_message is None:
                return None
            return int((message.created_at - last_outgoing_message.created_at).total_seconds())

    @staticmethod
    def qualify_lead(chat : Chat, quality_score: QualityScore, execution_context: ExecutionContext) -> Chat:
        """
        Qualify a lead.
        """
        chat.client.lead_quality = quality_score
        logger.debug(f"Chat {chat.id} qualified as {quality_score.value}")
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat

    @staticmethod
    def update_client_data(chat: Chat, client_data: ClientData, execution_context: ExecutionContext) -> Chat:
        if client_data.name is not None:
            chat.client.name = client_data.name
        if client_data.country is not None:
            chat.client.country = client_data.country
        if client_data.email is not None:
            chat.client.email = client_data.email
        if client_data.DNI is not None:
            chat.client.DNI = client_data.DNI
        if client_data.external_id is not None:
            chat.client.external_id = client_data.external_id
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"La info del cliente fue actualizada por {execution_context.executor.name}", subtype=MessageSubtype.CLIENT_INFO_UPDATED)
        return chat

    @staticmethod
    def update_waid(chat: Chat, waid: str, execution_context: ExecutionContext) -> Chat:
        chat.client.waid = waid
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El waid del cliente fue actualizado por {execution_context.executor.name}", subtype=MessageSubtype.CLIENT_INFO_UPDATED)
        return chat

    @staticmethod
    def block_chat(chat: Chat, execution_context: ExecutionContext) -> Chat:
        """
        Block a chat.
        """
        if chat.area == Area.BLOCKED:
            raise AlreadyCompleted(f"Chat {chat.id} is already blocked")
        chat.area = Area.BLOCKED
        chat.agent_id = None
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue bloqueado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_BLOCKED)
        return chat

    @staticmethod
    def unblock_chat(chat: Chat, execution_context: ExecutionContext) -> Chat:
        """
        Unblock a chat.
        """
        if chat.area != Area.BLOCKED:
            raise ValueError(f"Chat {chat.id} is not blocked")
        chat.area = Area.WAITING_AGENT
        chat.agent_id = None
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue desbloqueado por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_UNBLOCKED)
        return chat

    @staticmethod
    def add_suggested_messages(chat: Chat, suggested_messages: List[MessageDraft], execution_context: ExecutionContext) -> Chat:
        """
        Add suggested messages to the chat.
        """
        chat.suggested_messages=suggested_messages
        logger.debug(f"Added {len(suggested_messages)} suggested messages to chat {chat.id} #{chat.client.get_waid()}")
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat

    @staticmethod
    def remove_suggested_messages(chat: Chat, execution_context: ExecutionContext) -> Chat:
        """
        Remove suggested messages from the chat.
        """
        chat.suggested_messages = []
        logger.debug(f"Removed all suggested messages from chat {chat.id} #{chat.client.get_waid()}")
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat