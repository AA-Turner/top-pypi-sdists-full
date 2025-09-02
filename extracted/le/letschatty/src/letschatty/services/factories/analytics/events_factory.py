from typing import Optional, Dict, Any
from datetime import datetime
from ....models.analytics.events import *
from ....models.base_models.chatty_asset_model import ChattyAssetModel
from ....models.company.assets.chat_assets import AssignedAssetToChat
from ....models.company.empresa import EmpresaModel
from ....models.company.assets.users.user import User
from ....models.chat.chat import Chat
from ....models.chat.chat_with_assets import ChatWithAssets
from ....models.chat.flow_link_state import FlowStateAssignedToChat
from ...chat.chat_service import ChatService
from ....models.company.assets.contact_point import ContactPoint
from ....models.analytics.events.base import Event
from ....models.company.company_chats_snapshot import CompanyChatsSnapshot
from ....models.company.assets.users.agent_chats_snapshot import AgentChatsSnapshot
from ....models.company.assets.ai_agents_v2.chatty_ai_agent import ChattyAIAgent
from zoneinfo import ZoneInfo
from typing import List
from ....models.chat.highlight import Highlight
from pathlib import Path
import toml
from ....models.utils.types.identifier import StrObjectId
from ....models.analytics.events.event_type_to_classes import event_type_to_class
import json
class EventFactory:

    @classmethod
    def package_version(cls) -> str:
        """Get the package version from pyproject.toml"""
        from importlib.metadata import version
        return version("letschatty")

        """
        pyproject_path = Path(__file__).parent.parent.parent.parent.parent.parent / "pyproject.toml"
        with open(pyproject_path) as f:
            pyproject = toml.load(f)
            return pyproject["tool"]["poetry"]["version"]"""

    @classmethod
    def from_json(cls, json_data: str) -> Event:
        json_dict = json.loads(json_data)
        event_type = EventType(json_dict["type"])
        return event_type_to_class(event_type)(**json_dict)

    @staticmethod
    def _create_base_customer_event_data(
        chat_with_assets: Optional[ChatWithAssets],
        company_info: EmpresaModel,
        executor_type: ExecutorType,
        executor_id: StrObjectId,
        company_snapshot: Optional[CompanyChatsSnapshot] = None,
        agent_snapshot: Optional[AgentChatsSnapshot] = None
    ) -> CustomerEventData:
        """Create base CustomerEventData with common fields."""

        return CustomerEventData(
            company_phone_number_id=company_info.phone_number_id, #type: ignore
            company_waba_id=company_info.waba_id_value,
            chat_id=chat_with_assets.chat.id if chat_with_assets else None,
            client_phone_number=chat_with_assets.chat.client.get_waid() if chat_with_assets else None,
            client_email=chat_with_assets.chat.client.get_email() if chat_with_assets else None,
            client_country=chat_with_assets.chat.client.country if chat_with_assets else None,
            client_name=chat_with_assets.chat.client.name if chat_with_assets else None,
            ctwa_clid=ChatService.get_last_ctwa_clid(chat_with_assets.contact_points) if chat_with_assets else None,
            fb_clid=ChatService.get_last_fbclid(chat_with_assets.contact_points) if chat_with_assets else None,
            gclid=ChatService.get_last_gclid(chat_with_assets.contact_points) if chat_with_assets else None,
            client_ip_address=ChatService.get_last_ip_address(chat_with_assets.contact_points) if chat_with_assets else None,
            client_user_agent=ChatService.get_last_user_agent(chat_with_assets.contact_points) if chat_with_assets else None,
            client_external_id=ChatService.get_external_id(chat_with_assets.chat) if chat_with_assets else None,
            chat_context=ChatService.get_chat_context(chat_with_assets.chat) if chat_with_assets else None,
            company_snapshot=company_snapshot,
            agent_snapshot=agent_snapshot,
            executor_type=executor_type,
            executor_id=executor_id
        )

    @staticmethod
    def highlight_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, highlight: Highlight, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )

        highlight_data = HighlightData(
            **base_data.model_dump(),
            highlight_id=highlight.id,
            highlight=highlight if event_type != EventType.HIGHLIGHT_DELETED else None,
            time_to_highlight_seconds=int((highlight.created_at - chat_with_assets.chat.created_at).total_seconds()) if event_type == EventType.HIGHLIGHT_CREATED else None
        )
        # Create highlight created event
        event = HighlightEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=highlight_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def ai_agent_assignment_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, assigned_asset : AssignedAssetToChat, chatty_ai_agent:ChattyAIAgent, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        ai_agent_data = ChattyAIChatData(
            **base_data.model_dump(),
            chatty_ai_agent_id=chatty_ai_agent.id,
            chatty_ai_agent=chatty_ai_agent,
            time_to_chatty_ai_agent_seconds=int((assigned_asset.assigned_at - chat_with_assets.chat.created_at).total_seconds()) if event_type == EventType.AI_AGENT_ASSIGNED_TO_CHAT else None
        )
        event = ChattyAIChatEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=ai_agent_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def tag_assignment_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, assigned_asset : AssignedAssetToChat, tag: Tag, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        tag_data = TagChatData(
            **base_data.model_dump(),
            tag_id=tag.id,
            tag=tag,
            time_to_tag_seconds=int((assigned_asset.assigned_at - chat_with_assets.chat.created_at).total_seconds()) if event_type == EventType.TAG_ASSIGNED else None
        )
        event = TagChatEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=tag_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def product_assignment_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, assigned_asset : AssignedAssetToChat, product: Product, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        product_data = ProductChatData(
            **base_data.model_dump(),
            product_id=assigned_asset.asset_id,
            product=product if event_type != EventType.PRODUCT_REMOVED else None,
            time_to_product_seconds=int((assigned_asset.assigned_at - chat_with_assets.chat.created_at).total_seconds()) if event_type == EventType.PRODUCT_ASSIGNED else None
        )
        event = ProductChatEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=product_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def quality_scoring_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, quality_score: QualityScore, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        quality_data = QualityScoringData(
            **base_data.model_dump(),
            quality_score=quality_score,
            time_to_score_seconds=int((time - chat_with_assets.chat.created_at).total_seconds())
        )
        event = QualityScoringEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=quality_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id,
        )
        events.append(event)
        return events

    @staticmethod
    def contact_point_events(chat_with_assets: Optional[ChatWithAssets], company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, contact_point: ContactPoint, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        contact_point_data = ContactPointData(
            **base_data.model_dump(),
            contact_point=contact_point if event_type != EventType.CONTACT_POINT_DELETED else None,
            contact_point_id=contact_point.id,
            source_id=contact_point.source_id,
            new_chat=contact_point.new_chat,
            matched=contact_point.matched,
            time_from_request_to_match_seconds=int((contact_point.match_timestamp - contact_point.created_at).total_seconds()) if (contact_point.matched and contact_point.match_timestamp and event_type != EventType.CONTACT_POINT_DELETED) else None,
            topic_id=contact_point.topic_id
        )
        event = ContactPointEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=contact_point_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def sales_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, sale: Sale, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        sale_data = SaleData(
            **base_data.model_dump(),
            sale=sale if event_type != EventType.SALE_DELETED else None,
            sale_id=sale.id,
            is_first_sale=len(chat_with_assets.sales) == 1,
            time_to_sale_seconds=int((time - chat_with_assets.chat.created_at).total_seconds()) if event_type != EventType.SALE_DELETED else None
                              )
        event = SaleEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=sale_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def business_area_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, business_area_id: StrObjectId, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        business_area_data = BusinessAreaData(
            **base_data.model_dump(),
            business_area_id=business_area_id,
            entered_at=time if event_type == EventType.BUSINESS_AREA_ASSIGNED else None,
            exited_at=time if event_type == EventType.BUSINESS_AREA_REMOVED else None
        )
        event = ChatBusinessAreaEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=business_area_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def funnel_stage_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, chat_funnel: ClientFunnel, funnel_transition: StageTransition, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        funnel_data = FunnelEventData(
            **base_data.model_dump(),
            funnel_id=chat_funnel.funnel_id,
            funnel_stage_transition=funnel_transition,
            time_in_funnel_seconds=chat_funnel.time_in_funnel_seconds
        )
        event = ChatFunnelEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=funnel_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def workflow_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, flow_link_state: FlowStateAssignedToChat, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        workflow_data = WorkflowEventData(
            **base_data.model_dump(),
            workflow_id=flow_link_state.id,
            execution_result=flow_link_state.execution_result,
            execution_time_seconds=flow_link_state.execution_time_seconds,
            error_message=flow_link_state.error_message
        )
        event = WorkflowEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=workflow_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def chat_updated_status_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, status_modification: ChatStatusModification, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []

        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        chat_status_data = ChatStatusEventData(
            **base_data.model_dump(),
            action_type=status_modification,
            destination_agent_id=chat_with_assets.chat.agent_id,
            area=chat_with_assets.chat.area

        )
        event = ChatStatusEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=chat_status_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def chat_created_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, event_type: EventType, time: datetime, contact_point_id: Optional[StrObjectId], created_from: ChatCreatedFrom, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []

        if created_from != ChatCreatedFrom.SYSTEM and not contact_point_id:
            raise ValueError("contact_point_id is required for CHAT_CREATED event when created_from is not SYSTEM")

        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        chat_status_data = ChatStatusEventData(
            **base_data.model_dump(),
            contact_point_id=contact_point_id,
            created_from=created_from,
            area=chat_with_assets.chat.area
        )
        event = ChatStatusEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=chat_status_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def message_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None, new_status: Optional[Status] = None, message: Optional[ChattyMessage] = None) -> List[Event]:
        events = []
        if message is None:
            raise ValueError("message is required for MESSAGE_RECEIVED and MESSAGE_SENT events")

        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        message_data = MessageData(
            **base_data.model_dump(),
            message=message if event_type != EventType.MESSAGE_STATUS_UPDATED else None,
            wamid=message.id,
            new_status = new_status,
                    )
        event = MessageEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=message_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id,
            webhook_for_agent_type=chat_with_assets.chatty_ai_agent.n8n_workspace_agent_type if chat_with_assets.chatty_ai_agent else None
        )
        events.append(event)
        return events

    @staticmethod
    def message_status_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, event_type: EventType, new_status: Status, wamid: str, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []
        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        message_data = MessageData(
            **base_data.model_dump(),
            wamid=wamid,
            new_status = new_status
        )
        event = MessageEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=message_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def continuous_conversation_events(chat_with_assets: ChatWithAssets, company_info: EmpresaModel, trace_id: str,executor_type: ExecutorType, executor_id: StrObjectId, continuous_conversation: ContinuousConversation, event_type: EventType, time: datetime, company_snapshot: Optional[CompanyChatsSnapshot] = None, agent_snapshot: Optional[AgentChatsSnapshot] = None) -> List[Event]:
        events = []

        base_data = EventFactory._create_base_customer_event_data(
                                                                    chat_with_assets=chat_with_assets,
                                                                    company_info=company_info,
                                                                    executor_type=executor_type,
                                                                    executor_id=executor_id,
                                                                    company_snapshot=company_snapshot,
                                                                    agent_snapshot=agent_snapshot
                                                                  )
        continuous_conversation_data = ContinuousConversationData(
            **base_data.model_dump(),
            cc_id=continuous_conversation.id,
            continuous_conversation=continuous_conversation if event_type != EventType.CONTINUOUS_CONVERSATION_UPDATED else None,
            template_message_waid=continuous_conversation.template_message_waid,
            status=continuous_conversation.status
        )
        event = ContinuousConversationEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=continuous_conversation_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def asset_events(company_id: StrObjectId, trace_id: str, executor_type: ExecutorType, executor_id: StrObjectId, asset: ChattyAssetModel, asset_type: CompanyAssetType, event_type: EventType, time: datetime, company_info: EmpresaModel) -> List[Event]:
        events = []

        asset_data = AssetData(
            asset_id=asset.id,
            asset=asset if "deleted" not in event_type.value else None,
            asset_type=asset_type,
            executor_type=executor_type,
            executor_id=executor_id
        )
        event = AssetEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=asset_data,
            source="chatty_api.webapp",
            company_id=company_id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def company_creation_events(empresa_model: EmpresaModel, trace_id: str, executor_type: ExecutorType, executor_id: StrObjectId, event_type: EventType, time: datetime) -> List[Event]:
        events = []
        company_data = CompanyEventData(
            company_id=empresa_model.id,
            company=empresa_model
        )
        event = CompanyEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=company_data,
            source="chatty_api.webapp",
            company_id=empresa_model.id,
            frozen_company_name=empresa_model.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events

    @staticmethod
    def user_events(company_info: EmpresaModel, trace_id: str, executor_type: ExecutorType, executor_id: StrObjectId, user: User, event_type: EventType, time: datetime, business_area_id: Optional[StrObjectId] = None, funnel_id: Optional[StrObjectId] = None) -> List[Event]:
        events = []

        user_data = UserEventData(
            user_id=user.id,
            executor_type=executor_type,
            executor_id=executor_id,
            company_id=company_info.id,
            new_status=user.status if event_type == EventType.USER_STATUS_UPDATED else None, #type: ignore
            business_area_id=business_area_id,
            funnel_id=funnel_id

        )
        event = UserEvent(
            specversion=EventFactory.package_version(),
            type=event_type,
            time=time,
            data=user_data,
            source="chatty_api.webapp",
            company_id=company_info.id,
            frozen_company_name=company_info.frozen_name,
            trace_id=trace_id
        )
        events.append(event)
        return events