from __future__ import annotations
from letschatty.models.chat.client import ClientData
from letschatty.models.chat.preview import ChatPreview, ClientPreview
from letschatty.models.company.assets.users.user import User
from letschatty.models.chat.time_left import TimeLeft, TimeLeftStatus
from letschatty.models.company.assets.tag import Tag
from letschatty.models.company.assets.sale import Sale
from letschatty.models.company.assets.flow import FlowPreview
from letschatty.models.messages.chatty_messages import ChattyMessage, CentralNotification
from letschatty.models.utils import Status, MessageSubtype, MessageType
from letschatty.models.utils.definitions import Area
from letschatty.models.company.assets.contact_point import ContactPoint
from letschatty.models.chat.highlight import Highlight, HighlightRequestData, HighlightUpdateData
from letschatty.models.chat.quality_scoring import QualityScore
from letschatty.models.copilot.links import LinkItem
from letschatty.models.chat.flow_link_state import FlowStateAssignedToChat, StateTrigger
from letschatty.models.company.conversation_topic import TopicTimelineEntry
from letschatty.models.company.form_field import CollectedData
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
from ...models.messages.chatty_messages.base.message_draft import ChattyContentAudio, MessageDraft
from ...models.messages.chatty_messages.schema.chatty_content.content_central import CentralNotificationStatus
from ...models.messages.chatty_messages.schema import ChattyContext
from ...models.utils.types.message_types import MessageType
from .conversation_topics_service import ConversationTopicsService
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
    def _get_escalation_reason_text(reason: Optional[str], message: Optional[str]) -> str:
        default_reason = "El chat necesita intervención humana"
        reason_map = {
            "control_trigger": default_reason,
            "something_went_wrong": default_reason,
            "suggested_messages": "El chat requiere revisión humana de mensajes sugeridos",
        }

        if reason and reason.strip():
            return reason_map.get(reason.strip().lower(), reason.strip())

        # Backward-compatible fallback: only use message if it looks like a short reason,
        # never a long COT/multi-line text.
        if message and message.strip():
            candidate = message.strip()
            if len(candidate) <= 120 and "\n" not in candidate:
                return candidate

        return default_reason

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
        contact_point_with_ctwa_clid = next((contact_point for contact_point in reversed(contact_points) if contact_point.ctwa_clid), None)
        return contact_point_with_ctwa_clid.ctwa_clid if contact_point_with_ctwa_clid is not None else None

    @staticmethod
    def get_last_fbclid(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last fbclid from the chat.
        """
        contact_point_with_fbclid = next((contact_point for contact_point in reversed(contact_points) if contact_point.fb_clid), None)
        return contact_point_with_fbclid.fb_clid if contact_point_with_fbclid is not None else None

    @staticmethod
    def get_last_fbc(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last Meta _fbc cookie from the chat.

        Preferred over synthesizing one from the fbclid: the cookie carries the
        real click time, where a synthesized value can only use the event time.
        """
        contact_point_with_fbc = next((contact_point for contact_point in reversed(contact_points) if contact_point.fbc), None)
        return contact_point_with_fbc.fbc if contact_point_with_fbc is not None else None

    @staticmethod
    def get_last_fbp(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last Meta _fbp browser id cookie from the chat.
        """
        contact_point_with_fbp = next((contact_point for contact_point in reversed(contact_points) if contact_point.fbp), None)
        return contact_point_with_fbp.fbp if contact_point_with_fbp is not None else None

    @staticmethod
    def get_last_gclid(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last gclid from the chat.
        """
        contact_point_with_gclid = next((contact_point for contact_point in reversed(contact_points) if contact_point.gclid), None)
        return contact_point_with_gclid.gclid if contact_point_with_gclid is not None else None

    @staticmethod
    def get_last_ip_address(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last ip address from the chat.
        """
        contact_point_with_ip_address = next((contact_point for contact_point in reversed(contact_points) if contact_point.client_ip_address), None)
        return contact_point_with_ip_address.client_ip_address if contact_point_with_ip_address is not None else None

    @staticmethod
    def get_last_user_agent(contact_points: List[ContactPoint]) -> Optional[str]:
        """
        Get the last user agent from the chat.
        """
        contact_point_with_user_agent = next((contact_point for contact_point in reversed(contact_points) if contact_point.client_user_agent), None)
        return contact_point_with_user_agent.client_user_agent if contact_point_with_user_agent is not None else None

    @staticmethod
    def get_external_id(chat: Chat) -> Optional[str]:
        """
        Get the external id from the chat.
        """
        return chat.person.external_id


    @staticmethod
    def add_product(chat : Chat, execution_context: ExecutionContext, product : Product) -> AssignedAssetToChat:
        """
        Add a product to the chat.
        """
        if next((product for product in chat.products if product.asset_id == product.id), None) is not None:
            raise AssetAlreadyAssigned(f"Product with id {product.id} already assigned to chat {chat.id}")
        assigned_asset = AssignedAssetToChat(
            asset_type=ChatAssetType.PRODUCT,
            asset_id=product.id,
            assigned_at=datetime.now(),
            assigned_by=execution_context.executor.id
        )
        execution_context.set_event_time(assigned_asset.assigned_at)
        bisect.insort(chat.products, assigned_asset)
        ChatService.add_central_notification_from_text(chat=chat, body=f"Producto {product.name} agregado al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.PRODUCT_ADDED, context=ChattyContext(chain_of_thought_id=execution_context.chain_of_thought_id))
        return assigned_asset

    @staticmethod
    def remove_product(chat : Chat, execution_context: ExecutionContext, product_id : StrObjectId) -> AssignedAssetToChat:
        """
        Remove a product from the chat.
        """
        try:
            assigned_asset_to_remove = next(product for product in chat.products if product.asset_id == product_id)
            chat.products.remove(assigned_asset_to_remove)
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            ChatService.add_central_notification_from_text(chat=chat, body=f"Producto {assigned_asset_to_remove.asset_id} eliminado del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.PRODUCT_DELETED)
            return assigned_asset_to_remove
        except StopIteration:
            # Mismo contrato que `remove_tag`: que el chat no lo tenga es un
            # no-op, no un error. Los editores de api-chatty tratan
            # `AlreadyCompleted` como éxito, así que una acción masiva que pide
            # quitar un producto que no está deja de reportar «falló».
            # `NotFoundError` sigue siendo lo correcto para «el producto no
            # existe en la empresa», que se levanta antes, en el editor.
            logger.info(f"Product with id {product_id} not found in chat {chat.id}")
            raise AlreadyCompleted(message=f"Product with id {product_id} not found in chat {chat.id}. Returning success")

    @staticmethod
    def add_tag(chat : Chat, tag : Tag, execution_context: ExecutionContext) -> AssignedAssetToChat:
        """
        Add a tag to the chat.
        """
        if next((assigned_tag for assigned_tag in chat.tags if assigned_tag.asset_id == tag.id), None) is not None:
            raise AssetAlreadyAssigned(f"Tag with id {tag.id} already assigned to chat {chat.id}")
        assigned_asset = AssignedAssetToChat(
            asset_type=ChatAssetType.TAG,
            asset_id=tag.id,
            assigned_at=datetime.now(),
            assigned_by=execution_context.executor.id
        )
        execution_context.set_event_time(assigned_asset.assigned_at)
        bisect.insort(chat.tags, assigned_asset)
        ChatService.add_central_notification_from_text(chat=chat, body=f"Etiqueta {tag.name} agregada al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.TAG_ADDED, context=ChattyContext(chain_of_thought_id=execution_context.chain_of_thought_id))
        logger.debug(f"added tag {tag} to chat {chat.id}")
        return assigned_asset

    @staticmethod
    def remove_tag(chat : Chat, tag_id : StrObjectId, tag : Tag, execution_context: ExecutionContext) -> AssignedAssetToChat:
        """
        Remove a tag from the chat.
        """
        try:
            assigned_asset_to_remove = next(tag for tag in chat.tags if tag.asset_id == tag_id)
            chat.tags.remove(assigned_asset_to_remove)
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
    def escalate_chatty_ai_agent(
        chat: Chat,
        execution_context: ExecutionContext,
        message: Optional[str] = None,
        reason: Optional[str] = None
    ) -> None:
        """
        Add a central notification indicating AI-agent escalation.
        AI-agent escalation state is managed by Lambda (chatty_ai_agent_in_chat),
        so this method must not mutate embedded chat.chatty_ai_agent fields.
        """
        reason_text = ChatService._get_escalation_reason_text(reason=reason, message=message)
        body = f"El chat fue escalado a un agente humano. Motivo: {reason_text}"
        ChatService.add_central_notification_from_text(
            chat=chat,
            body=body,
            subtype=MessageSubtype.CHATTY_AI_AGENT_NOTIFICATION,
            content_status=CentralNotificationStatus.WARNING,
            context=ChattyContext(chain_of_thought_id=execution_context.chain_of_thought_id)
        )

    @staticmethod
    def add_workflow_link(chat : Chat, link : LinkItem, flow:FlowPreview, execution_context: ExecutionContext, description: str, last_incoming_message_id: Optional[str] = None, next_call: Optional[datetime] = None, trigger: Optional[StateTrigger] = None) -> FlowStateAssignedToChat:
        """
        Add a tag to the chat.
        """
        if flow.is_smart_follow_up:
            current_smart_follow_up_state = ChatService.get_smart_follow_up_state(chat=chat)
            if current_smart_follow_up_state is not None:
                raise AssetAlreadyAssigned(f"Smart follow up with id {link.flow_id} already assigned to chat {chat.id}")
        state = FlowStateAssignedToChat.from_link(link=link, execution_context=execution_context, description=description, last_incoming_message_id=last_incoming_message_id, next_call=next_call, is_smart_follow_up=flow.is_smart_follow_up, trigger=trigger)
        if state in chat.flow_states:
            raise AssetAlreadyAssigned(f"Flow with id {link.flow_id} already assigned to chat {chat.id}")
        execution_context.set_event_time(state.assigned_at)
        chat.flow_states.append(state)
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
        chat.flow_states.append(workflow_link)
        logger.debug(f"Chat flow states after inserting the updated workflow link: {chat.flow_states}")
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return workflow_link

    @staticmethod
    def get_smart_follow_up_state(chat : Chat) -> Optional[FlowStateAssignedToChat]:
        """
        Get the smart follow up state for the chat.
        """
        logger.debug(f"Chat flow states: {chat.flow_states}")
        return next((state for state in chat.flow_states if state.is_smart_follow_up), None)

    @staticmethod
    def create_sale(chat : Chat, execution_context: ExecutionContext, sale : Sale) -> SaleAssignedToChat:
        """
        Add a sale to the chat.

        El texto del chat sale de la venta (`Sale.titulo`): con un producto es el de siempre
        ("Venta de Plan anual"); con varios los nombra ("Venta de A, B y 3 más"); sin
        productos usa el concepto. Los nombres son la foto que guarda cada línea, así que
        quien llama tiene que haberlos completado (`Sale.con_nombres_de_productos`).
        """
        if any(assigned.asset_id == sale.id for assigned in chat.sales):
            raise AssetAlreadyAssigned(f"Sale with id {sale.id} already assigned to chat {chat.id}")
        assigned_asset = SaleAssignedToChat.from_sale(sale=sale, assigned_by=execution_context.executor.id)
        # La hora del evento sigue siendo la de siempre: cuándo se REGISTRÓ la venta. Antes se
        # tomaba de `assigned_at`, que ahora es la fecha de venta; sin fijarla acá el evento
        # pasaría a fecharse hacia atrás (y el refresco incremental de analytics_v2 sólo
        # levanta eventos de los últimos 7 días). La fecha de venta viaja adentro del evento,
        # en `data.sale.sold_at`, para que analytics la use cuando corresponda.
        execution_context.set_event_time(sale.created_at)
        bisect.insort(chat.sales, assigned_asset)
        ChatService.create_highlight(chat=chat, execution_context=execution_context, highlight_data=HighlightRequestData(title=f"🛍️ {sale.titulo()}", description=f"{sale.titulo()} creada por {execution_context.executor.name}", starred=False, subtype=MessageSubtype.SALE_ADDED))
        ChatService.add_central_notification_from_text(chat=chat, body=f"{sale.titulo()} agregada al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.SALE_ADDED)
        return assigned_asset

    @staticmethod
    def update_sale(chat : Chat, execution_context: ExecutionContext, sale : Sale, previous_sale : Sale) -> SaleAssignedToChat:
        """
        Update a sale for the chat.

        Pone al día la referencia de `client.sales` con la venta ya editada (`sale`; la de
        antes de editar es `previous_sale`) y la devuelve. Si la edición no cambió ni la fecha
        de venta ni los productos, la referencia vuelve igual y no hay nada que persistir.
        """
        try:
            index = next(i for i, a in enumerate(chat.sales) if a.asset_id == sale.id)
        except StopIteration:
            raise NotFoundError(message=f"Sale with id {sale.id} not found in chat {chat.id}")
        # En el mismo lugar, como en Mongo (`array_update_element`): reordenar acá sólo
        # cambiaría la copia en memoria.
        synced = chat.sales[index].synced_with(sale, previous=previous_sale)
        chat.sales[index] = synced
        ChatService.create_highlight(chat=chat, execution_context=execution_context, highlight_data=HighlightRequestData(title=f"🛍️ {sale.titulo('actualizada')}", description=f"{sale.titulo()} actualizada por {execution_context.executor.name}", starred=False, subtype=MessageSubtype.SALE_UPDATED))
        ChatService.add_central_notification_from_text(chat=chat, body=f"{sale.titulo()} actualizada en el chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.SALE_UPDATED)
        return synced

    @staticmethod
    def delete_sale(chat : Chat, execution_context: ExecutionContext, sale : Sale) -> SaleAssignedToChat:
        """
        Logically remove a sale from the chat.
        """
        try:
            assigned_asset_to_remove = next(assigned for assigned in chat.sales if assigned.asset_id == sale.id)
        except StopIteration:
            raise NotFoundError(message=f"Sale with id {sale.id} not found in chat {chat.id}")
        chat.sales.remove(assigned_asset_to_remove)
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.create_highlight(chat=chat, execution_context=execution_context, highlight_data=HighlightRequestData(title=f"🛍️ {sale.titulo('eliminada')}", description=f"{sale.titulo()} eliminada por {execution_context.executor.name}", starred=False, subtype=MessageSubtype.SALE_DELETED))
        ChatService.add_central_notification_from_text(chat=chat, body=f"{sale.titulo()} eliminada del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.SALE_DELETED)
        return assigned_asset_to_remove

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
            subtype=highlight_data.subtype,
            in_chat=highlight_data.in_chat,
        ) #type: ignore
        execution_context.set_event_time(highlight.created_at)
        bisect.insort(chat.highlights, highlight)
        # Sort highlights in descending order by created_at timestamp
        chat.highlights.sort(reverse=True)
        if highlight.in_chat:
            # La nota misma se ve en el hilo: el aviso «Highlight X agregado…» sería ruido al lado.
            return highlight
        ChatService.add_central_notification_from_text(chat=chat, body=f"Highlight {highlight.title} agregado al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.HIGHLIGHT_ADDED)
        return highlight

    @staticmethod
    def update_highlight(chat : Chat, execution_context: ExecutionContext, highlight_id : StrObjectId, highlight_data: HighlightRequestData | HighlightUpdateData) -> Highlight:
        """
        Update a highlight for the chat.

        Sólo cambia lo que el pedido informó (lo ausente o null se conserva) y nunca el autor:
        antes se rearmaba la nota entera con `creator_id` = quien edita, así que el autor cambiaba
        en cada edición y un PUT sin `starred` la desmarcaba. `edited_at` se mueve sólo si cambió
        el título o el texto. Quién puede editar lo decide quien llama (api-chatty).
        """
        try:
            highlight_to_update = next(highlight for highlight in chat.highlights if highlight.id == highlight_id)
        except StopIteration:
            raise NotFoundError(message=f"Highlight with id {highlight_id} not found in chat {chat.id}")
        cambios = {
            campo: valor for campo, valor in highlight_data.model_dump(exclude_unset=True).items()
            if campo in ("title", "description", "starred", "in_chat") and valor is not None
        }
        if any(campo in cambios and cambios[campo] != getattr(highlight_to_update, campo) for campo in ("title", "description")):
            cambios["edited_at"] = datetime.now(tz=ZoneInfo("UTC"))
        updated_highlight = highlight_to_update.update_from_dict(**cambios)
        chat.highlights.remove(highlight_to_update)
        bisect.insort(chat.highlights, updated_highlight)
        # Sort highlights in descending order by created_at timestamp
        chat.highlights.sort(reverse=True)
        execution_context.set_event_time(updated_highlight.updated_at)
        return updated_highlight

    @staticmethod
    def delete_highlight(chat : Chat, execution_context: ExecutionContext, highlight_id : StrObjectId) -> Highlight:
        """
        Logically remove a highlight from the chat.
        """
        try:
            highlight = next(highlight for highlight in chat.highlights if highlight.id == highlight_id)
            chat.highlights.remove(highlight)
            # Sort highlights in descending order by created_at timestamp
            chat.highlights.sort(reverse=True)
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            ChatService.add_central_notification_from_text(chat=chat, body=f"Highlight #{highlight.title} eliminado del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.HIGHLIGHT_DELETED)
            return highlight
        except StopIteration:
            raise NotFoundError(message=f"Highlight with id {highlight_id} not found in chat {chat.id}")

    @staticmethod
    def attach_contact_point(chat : Chat, execution_context: ExecutionContext, contact_point : ContactPoint) -> ContactPointAssignedToChat:
        """Cuelga el touchpoint del chat, sin anunciarlo en el hilo.

        Es la mitad "estructura" de `add_contact_point`, separada porque hay caminos que
        necesitan que el touchpoint exista en `client.contact_points` —que es de donde sale
        el panel del chat— pero NO que se escriba una notificación central. El caso concreto
        es el envío de plantillas: ya escribe su propia notificación ("Template X pending to
        be sent…") y la fuente de una plantilla se llama `Template 'X'`, así que la del
        touchpoint quedaría pegada abajo diciendo lo mismo. A volumen de campaña eso es un
        renglón por destinatario.

        Idempotente: si el touchpoint ya está colgado devuelve la asignación existente en
        vez de duplicarla. (El guard original comparaba `contact_point.asset_id` contra
        `contact_point.id` sobre la variable del generador, que shadoweaba al parámetro —
        dos campos distintos del MISMO objeto, así que nunca daba verdadero y el chequeo
        estaba muerto. Al arreglarlo se prefirió devolver a levantar: los llamadores lo usan
        para colgar un touchpoint recién creado, y un 500 en el camino de envío por algo que
        ya está hecho es peor que no hacer nada.)
        """
        ya_asignado = next((asignado for asignado in chat.contact_points if asignado.asset_id == contact_point.id), None)
        if ya_asignado is not None:
            return ya_asignado
        assigned_asset = ContactPointAssignedToChat(
            asset_type=ChatAssetType.CONTACT_POINT,
            asset_id=contact_point.id,
            assigned_at=contact_point.created_at,
            assigned_by=execution_context.executor.id,
            source_id=contact_point.matched_source_id
        )
        bisect.insort(chat.contact_points, assigned_asset)
        return assigned_asset

    @staticmethod
    def add_contact_point(chat : Chat, execution_context: ExecutionContext, contact_point : ContactPoint, source : Source) -> ContactPointAssignedToChat:
        """
        Add a contact point to the chat, and announce it in the thread.
        """
        assigned_asset = ChatService.attach_contact_point(chat=chat, execution_context=execution_context, contact_point=contact_point)
        # El puntero al touchpoint, además del texto: el body nombra la fuente y ese
        # nombre queda congelado, así que en cuanto alguien reatribuye el touchpoint la
        # notificación miente. Con el id el cliente resuelve la fuente actual.
        ChatService.add_central_notification_from_text(chat=chat, body=f"TouchPoint de la fuente {source.name} agregado al chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CONTACT_POINT_ADDED, context=ChattyContext(contact_point_id=str(contact_point.id)))
        return assigned_asset

    @staticmethod
    def update_contact_point(chat : Chat, execution_context: ExecutionContext, contact_point : ContactPoint, source : Source) -> ContactPoint:
        """
        Update a contact point for the chat.
        """
        ChatService.add_central_notification_from_text(chat=chat, body=f"TouchPoint de la fuente {source.name} actualizado en el chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CONTACT_POINT_UPDATED, context=ChattyContext(contact_point_id=str(contact_point.id)))
        return contact_point

    @staticmethod
    def delete_contact_point(chat : Chat, execution_context: ExecutionContext, contact_point_id : StrObjectId, contact_point : ContactPoint, source : Source) -> ContactPointAssignedToChat:
        """
        Logically remove a contact point from the chat.
        """
        try:
            assigned_asset_to_remove = next(contact_point for contact_point in chat.contact_points if contact_point.asset_id == contact_point_id)
            chat.contact_points.remove(assigned_asset_to_remove)
            # Se estampa igual aunque el touchpoint deje de existir: el cliente lo
            # resuelve a "touchpoint eliminado" en vez de mostrar un nombre de fuente que
            # ya no aplica. La notificación queda — es el registro de que hubo atribución.
            ChatService.add_central_notification_from_text(chat=chat, body=f"TouchPoint de la fuente {source.name} eliminado del chat {chat.id} por {execution_context.executor.name}", subtype=MessageSubtype.CONTACT_POINT_DELETED, context=ChattyContext(contact_point_id=str(contact_point_id)))
            return assigned_asset_to_remove
        except StopIteration:
            raise NotFoundError(message=f"TouchPoint de la fuente {source.name} not found in chat {chat.id}")

    @staticmethod
    def add_message(chat : Chat, message : ChattyMessage) -> ChattyMessage:
        """
        Add a message to the chat.
        """
        if message in chat.pending_messages or (chat.messages_loaded and message in chat.messages):
            raise MessageAlreadyInChat(f"Message with id {message.id} already in chat {chat.id}")
        # Queda pendiente: el guardado del chat (`ChatAssetService.save_pending`) lo escribe en
        # `chat_messages`. Si el chat tiene mensajes cargados, también se suma a esa lista.
        chat.add_pending_message(message)
        logger.debug(f"Added message to chat {chat.id}: {message}")
        return message

    @staticmethod
    def update_message_status(chat : Chat, message_id : str, status : Status, error_details : Optional[ErrorDetail] = None ) -> ChattyMessage:
        """
        Update the status of a message in the chat.
        """
        from letschatty.services.continuous_conversation_service.continuous_conversation_helper import ContinuousConversationHelper

        message = chat.get_message_by_id(message_id)
        if message is None:
            # logger.warning(f"Message with id {message_id} not found in chat {chat.id}")
            raise MessageNotFoundError(message=f"Message with id {message_id} not found in chat {chat.id}")

        # Si llegó tarde (un `sent` después del `delivered`), update_status no lo aplica. Lo
        # de abajo —la conversación continua y la señal de plantilla fallida— sigue igual
        # que siempre: lo único que cambia es que el estado guardado no retrocede.
        message.update_status(new_status=status, status_datetime=datetime.now())
        # The agent-facing failure NOTICE (the central "… falló: {motivo}" message) is built and
        # persisted by the ORCHESTRATION layer (api: ChatMessagesEditor._persist_failure_notice),
        # NOT here. This is a pure in-memory domain service with no persistence, so a notice added
        # here would never be saved. Our job is only: update the status, drive the continuous
        # conversation, and SIGNAL template failures via MetaErrorNotification (which the api turns
        # into the in-chat notice + the Slack alert). See docs/outbound-send-failure-handling.md (ADR).
        if message.subtype == MessageSubtype.TEMPLATE and status == Status.FAILED and error_details is not None:
            if message.is_cc_related:
                active_cc = ContinuousConversationHelper.get_active_cc(chat=chat)
                if active_cc:
                    active_cc = ContinuousConversationHelper.handle_failed_template_cc(chat=chat, cc=active_cc, error_details=error_details.get_error_details())
                else:
                    logger.warning(f"No active CC found for chat {chat.id}")
            logger.warning(f"Template {message.context.template_name} failed: {error_details.get_error_details()}")
            raise MetaErrorNotification(message=f"Template {message.context.template_name} failed", status_code=400, chat_id=chat.identifier, details=error_details.get_more_info())
        elif status == Status.FAILED and error_details is not None:
            logger.warning(f"Message {message_id} failed (meta_code={error_details.code}): {error_details.get_error_details()}")
        return message

    @staticmethod
    def mark_message_played(chat: Chat, message_id: str, played_datetime: datetime) -> ChattyMessage:
        """Record that a VOICE NOTE was played (Meta `played` status) — in-memory only.
        Finds the message by wamid, sets `played_at` (set-once), and NEVER touches `status`
        (played is a separate audio-only signal, not a delivery status). Raises
        MessageNotFoundError if the message isn't in the chat (the receiver swallows it → 200,
        same as any status for a message we don't have)."""
        message = chat.get_message_by_id(message_id)
        if message is None:
            raise MessageNotFoundError(message=f"Message with id {message_id} not found in chat {chat.id}")
        message.mark_played(played_datetime)
        return message

    @staticmethod
    def mark_message_revoked(chat : Chat, message_id : str) -> Optional[ChattyMessage]:
        """Tombstone the message identified by `message_id` (a wamid) as DELETED.

        Returns the message, or None if it isn't in the chat — a revoke can reference a
        message we never stored (e.g. the owner deleted something sent before onboarding,
        or a media message we skipped), so a miss is NORMAL and must NOT raise. Pure
        in-memory: the api layer persists (ChatCollection.update_message_revoked)."""
        message = chat.get_message_by_id(message_id)
        if message is None:
            logger.info(f"Revoke references message {message_id} not found in chat {chat.id} — nothing to tombstone")
            return None
        message.mark_as_revoked()
        return message

    @staticmethod
    def apply_message_edit(chat : Chat, message_id : str, new_body : str, edited_at : datetime) -> Optional[ChattyMessage]:
        """Apply a sender-side EDIT (Meta `type: edit`): replace the text body of the
        message identified by `message_id` (a wamid) and stamp context.edited_at.

        Returns the message, or None when there is nothing to apply — the edit can
        reference a message we never stored (sent before onboarding, or a type we
        skipped), so a miss is NORMAL and must NOT raise. Only TEXT messages are
        applied today: an edit targeting any other type (e.g. a media caption edit)
        is logged and skipped. Pure in-memory: the api layer persists
        (ChatCollection.update_message_edited)."""
        message = chat.get_message_by_id(message_id)
        if message is None:
            logger.info(f"Edit references message {message_id} not found in chat {chat.id} — nothing to apply")
            return None
        if message.type != MessageType.TEXT:
            logger.warning(f"Edit references non-text message {message_id} (type {message.type}) in chat {chat.id} — caption/other edits not applied yet, skipping")
            return None
        message.mark_as_edited(new_body=new_body, edited_at=edited_at)
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

        Todo cambio de dueño deja notificación central. El único caso que no
        escribe nada es el no-op (el chat YA era del agente destino), porque no
        hubo cambio que registrar.

        Ojo con la forma de este if/elif: hasta 0.4.531 la cadena terminaba en
        `elif current_agent.id != executor.id` SIN `else`, así que el traspaso
        más común de todos —el dueño del chat se lo pasa a un compañero— caía al
        vacío y no dejaba rastro. Medido en prod: 13.851 traspasos silenciosos
        en 11.327 chats de 62 empresas entre el 1-jun y el 9-sep de 2026.
        """
        logger.debug(f"Assigning chat to {agent_destination.name} - Current agent: {current_agent.name if current_agent else 'None'}")
        if current_agent is None:
            #Nadie lo tenía: es una asignación (se lo quede el ejecutor o se lo dé a un tercero).
            logger.debug(f"Assigning chat to {agent_destination.name} - No current agent - So its an assignment")
            if not execution_context.wpp_apb_mode:
                ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue asignado a {agent_destination.name} por {execution_context.executor.name}", subtype=MessageSubtype.CHAT_ASSIGNED)
        elif current_agent.id == agent_destination.id:
            #Ya era del agente destino: no hay cambio de dueño que registrar.
            logger.debug(f"Chat {chat.id} already assigned to {agent_destination.name}")
        else:
            #Lo tenía otro agente: es una transferencia. Dos sabores, misma leyenda:
            #  - current_agent != executor -> un tercero (admin) mueve el chat de otro.
            #  - current_agent == executor -> el dueño se lo pasa a un compañero.
            #La guarda de integración sigue cubriendo SOLO el primer sabor: que una
            #integración suelte un chat propio es legítimo, robárselo a otro no.
            if execution_context.is_integration and current_agent.id != execution_context.executor.id:
                raise ErrorToMantainSafety(f"An integration user is trying to STEAL a chat from {current_agent.name} to {agent_destination.name} | Chat {chat.id} | is {chat.area} | is assigned to {agent_destination.name} by {execution_context.executor.name} | This is a safety warning")
            logger.debug(f"Chat is already assigned, so its a transfer")
            if not execution_context.wpp_apb_mode:
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

        Desasignar devuelve el chat al pool: `agent_id = None`, `WAITING_AGENT`.
        NADIE se lo queda. Transferir es otra operación (`assign_chat`).

        Hasta 0.4.532, cuando lo desasignaba un tercero la leyenda decía "El chat
        fue transferido de A a {ejecutor} por {ejecutor}" con subtipo
        CHAT_TRANSFERRED: nombraba como nuevo dueño a alguien que nunca lo recibió
        y anunciaba una transferencia que no pasó. Ahora las dos ramas escriben
        CHAT_DESASSIGNED y se diferencian sólo en si nombran al que lo perdió.
        """
        if chat.area != Area.WITH_AGENT:
            raise AlreadyCompleted(f"Chat {chat.id} is already not assigned to any agent")
        if not execution_context.wpp_apb_mode:
            if current_agent.id == execution_context.executor.id:
                body = f"El chat fue desasignado por {execution_context.executor.name}"
            else:
                #Lo saca un tercero: hay que nombrar al agente que lo tenía, que es
                #el que se entera acá de que dejó de tenerlo.
                body = f"El chat fue desasignado de {current_agent.name} por {execution_context.executor.name}"
            ChatService.add_central_notification_from_text(chat=chat, body=body, subtype=MessageSubtype.CHAT_DESASSIGNED)
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
        chat.lead_quality = quality_score
        logger.debug(f"Chat {chat.id} qualified as {quality_score.value}")
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El chat fue calificado como {quality_score.value} por {execution_context.executor.name}", subtype=MessageSubtype.CLIENT_INFO_UPDATED, context=ChattyContext(chain_of_thought_id=execution_context.chain_of_thought_id))
        return chat

    @staticmethod
    def update_client_data(chat: Chat, client_data: ClientData, execution_context: ExecutionContext) -> Chat:
        """Edita la persona (necesita `chat.person` cargada). Los cambios quedan pendientes para
        `clients`, y los de la preview llegan a todos los chats de la persona al guardar."""
        for name, value in (("name", client_data.name), ("country", client_data.country), ("email", client_data.email),
                            ("document_id", client_data.DNI), ("external_id", client_data.external_id)):
            if value is not None:
                chat.set_person_field(name, value)
        if client_data.lead_form_data is not None:
            # Se mezcla con lo que había, clave por clave, en vez de reemplazarlo.
            for key, value in client_data.lead_form_data.items():
                chat.set_person_form_value(key, value)
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"La info del cliente fue actualizada por {execution_context.executor.name}", subtype=MessageSubtype.CLIENT_INFO_UPDATED)
        return chat

    @staticmethod
    def update_waid(chat: Chat, waid: str, execution_context: ExecutionContext) -> Chat:
        chat.set_person_field("waid", waid)
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(chat=chat, body=f"El waid del cliente fue actualizado por {execution_context.executor.name}", subtype=MessageSubtype.CLIENT_INFO_UPDATED)
        return chat

    @staticmethod
    def apply_contact_number_change(chat: Chat, user_id: str, waid: Optional[str], user_id_parent: Optional[str], execution_context: ExecutionContext) -> Chat:
        """El contacto cambió de número y Meta le regeneró el BSUID (`user_changed_user_id`).

        El BSUID pasa al nuevo, y el teléfono guardado —que es el del número VIEJO— se
        reemplaza por el nuevo si Meta lo compartió o se borra si no. Conservarlo tenía
        dos efectos: Meta prioriza el teléfono sobre el BSUID al enviar, así que las
        respuestas seguían yendo al número viejo; y el entrante sólo completa un teléfono
        vacío, así que el viejo no se corregía nunca. El número anterior queda escrito en
        la notificación central, que es lo que ve el agente.
        """
        previous_waid = chat.client.waid
        chat.set_person_field("user_id", user_id)
        chat.set_person_field("waid", waid)
        chat.set_person_field("user_id_parent", user_id_parent)
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(
            chat=chat,
            body=ChatService._contact_number_change_notice(previous_waid=previous_waid, new_waid=waid),
            subtype=MessageSubtype.CLIENT_INFO_UPDATED,
        )
        return chat

    @staticmethod
    def _contact_number_change_notice(previous_waid: Optional[str], new_waid: Optional[str]) -> str:
        if new_waid:
            notice = f"El contacto cambió su número de WhatsApp a +{new_waid}."
        else:
            notice = "El contacto cambió su número de WhatsApp. Meta no compartió el número nuevo: se completa cuando vuelva a escribir."
        if previous_waid:
            notice += f" Número anterior: +{previous_waid}."
        return notice

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

    @staticmethod
    def add_audio_transcription(chat: Chat, transcript:Optional[str], message_id:StrObjectId, execution_context:ExecutionContext, transcription_status: Optional[str] = None) -> Chat:
        """
        Add an audio transcription (or the reason there isn't one) to an audio message.

        - A non-empty transcript is stored and CLEARS any previous status: a later
          successful transcription wins over an earlier "sin_creditos".
        - With no transcript (None or blank) and a status, only the status is set; an
          existing transcription is never erased.
        - With neither, the transcription is set as given (previous behavior).
        """
        message = chat.get_message_by_id(message_id)
        if message is None:
            raise MessageNotFoundError(message=f"Message with id {message_id} not found in chat {chat.id}")
        if not isinstance(message.content, ChattyContentAudio):
            raise ValueError(f"Message with id {message_id} is not an audio message")
        has_transcript = bool(transcript and transcript.strip())
        if has_transcript:
            message.content.transcription = transcript
            message.content.transcription_status = None
        elif transcription_status:
            message.content.transcription_status = transcription_status
        else:
            message.content.transcription = transcript
        logger.debug(f"Added audio transcription to chat {chat.id} #{chat.client.get_waid()} (status={message.content.transcription_status})")
        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        return chat

    # ============================================================================
    # Conversation Topics Methods
    # ============================================================================

    @staticmethod
    def update_conversation_topics(
        chat: Chat,
        detected_topics: List[str],
        execution_context: ExecutionContext
    ) -> TopicTimelineEntry:
        """
        Update conversation topics based on tagger agent output.

        Simply adds new timeline entry with detected topics.
        Topics replace previous active topics.

        Args:
            chat: Chat instance
            detected_topics: List of topic names detected by tagger
            execution_context: Execution context for event tracking

        Returns:
            The new timeline entry that was added
        """
        entry = ConversationTopicsService.update_topics(
            chat=chat,
            detected_topics=detected_topics
        )

        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))

        # Log update
        logger.info(f"Updated topics for chat {chat.id}: {detected_topics}")

        return entry

    @staticmethod
    def get_active_conversation_topics(chat: Chat) -> List[str]:
        """
        Get currently active conversation topics.

        Args:
            chat: Chat instance

        Returns:
            List of active topic names
        """
        return chat.active_topics

    @staticmethod
    def cancel_all_conversation_topics(
        chat: Chat,
        execution_context: ExecutionContext
    ) -> TopicTimelineEntry:
        """
        Manually cancel all active conversation topics.

        Adds empty timeline entry to mark cancellation.

        Args:
            chat: Chat instance
            execution_context: Execution context for event tracking

        Returns:
            The empty timeline entry that was added
        """
        entry = ConversationTopicsService.cancel_all_topics(chat)

        execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
        ChatService.add_central_notification_from_text(
            chat=chat,
            body=f"All conversation topics cleared by {execution_context.executor.name}",
            subtype=MessageSubtype.SYSTEM
        )

        return entry

    # ============================================================================
    # Data Collection Methods
    # ============================================================================

    @staticmethod
    def update_collected_data(
        chat: Chat,
        collected_data: CollectedData,
        execution_context: ExecutionContext
    ) -> CollectedData:
        """
        Update collected customer data in the chat.

        Args:
            chat: Chat instance
            collected_data: New collected data from tagger
            execution_context: Execution context for event tracking

        Returns:
            Updated CollectedData object
        """

        # Update fields that have new values
        updated_fields = []
        person = chat.person

        for name in ("name", "email", "document_id", "external_id"):
            value = getattr(collected_data, name)
            if value and getattr(person, name) != value:
                chat.set_person_field(name, value)
                updated_fields.append(name)

        if collected_data.phone:
            # El teléfono es la identidad de la persona: un dato que recolectó la IA no la
            # cambia. Antes esto escribía `client.phone`, un atributo que no existe, y fallaba.
            logger.warning(f"Collected phone for chat {chat.id} not stored: the phone is the identity, not collected data")

        # Merge additional_fields
        if collected_data.additional_fields:
            for key, value in collected_data.additional_fields.items():
                if value is not None and person.lead_form_data.get(key) != value:
                    chat.set_person_form_value(key, value)
                    updated_fields.append(key)

        if updated_fields:
            execution_context.set_event_time(datetime.now(tz=ZoneInfo("UTC")))
            logger.info(f"Updated collected data for chat {chat.id}: {', '.join(updated_fields)}")

            ChatService.add_central_notification_from_text(
                chat=chat,
                body=f"Collected customer data: {', '.join(updated_fields)}",
                subtype=MessageSubtype.CLIENT_INFO_UPDATED,
                context=ChattyContext(chain_of_thought_id=execution_context.chain_of_thought_id)
            )

        return chat.person.lead_form_data