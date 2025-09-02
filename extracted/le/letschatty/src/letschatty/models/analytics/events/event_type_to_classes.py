from .event_types import EventType
from .base import Event
from .import *
from typing import Type, List
EVENT_TO_TYPE_CLASSES = {

    ##CHAT EVENTS
    EventType.CHAT_CREATED : ChatStatusEvent,
    EventType.CHAT_STATUS_UPDATED : ChatStatusEvent,
    EventType.CHAT_DELETED : ChatStatusEvent,
    #TAGS
    EventType.TAG_ASSIGNED : TagChatEvent,
    EventType.TAG_REMOVED : TagChatEvent,
    #PRODUCTS
    EventType.PRODUCT_ASSIGNED : ProductChatEvent,
    EventType.PRODUCT_REMOVED : ProductChatEvent,
    #SALES
    EventType.SALE_CREATED : SaleEvent,
    EventType.SALE_UPDATED : SaleEvent,
    EventType.SALE_DELETED : SaleEvent,
    #HIGHLIGHTS
    EventType.HIGHLIGHT_CREATED : HighlightEvent,
    EventType.HIGHLIGHT_UPDATED : HighlightEvent,
    EventType.HIGHLIGHT_DELETED : HighlightEvent,
    #MESSAGES
    EventType.MESSAGE_RECEIVED : MessageEvent,
    EventType.MESSAGE_SENT : MessageEvent,
    EventType.MESSAGE_STATUS_UPDATED : MessageEvent,
    #CONTACT POINTS
    EventType.CONTACT_POINT_CREATED : ContactPointEvent,
    EventType.CONTACT_POINT_UPDATED : ContactPointEvent,
    EventType.CONTACT_POINT_DELETED : ContactPointEvent,
    #WORKFLOWS
    EventType.WORKFLOW_ASSIGNED : WorkflowEvent,
    EventType.WORKFLOW_REMOVED : WorkflowEvent,
    EventType.WORKFLOW_STATUS_UPDATED : WorkflowEvent,
    #QUALITY SCORING
    EventType.GOOD_QUALITY_SCORE_ASSIGNED : QualityScoringEvent,
    EventType.BAD_QUALITY_SCORE_ASSIGNED : QualityScoringEvent,
    EventType.NEUTRAL_QUALITY_SCORE_ASSIGNED : QualityScoringEvent,
    #CONTINUOUS CONVERSATION
    EventType.CONTINUOUS_CONVERSATION_CREATED : ContinuousConversationEvent,
    EventType.CONTINUOUS_CONVERSATION_UPDATED : ContinuousConversationEvent,
    #FUNNEL STAGES
    # Funnel-level events
    EventType.CHAT_FUNNEL_STARTED : ChatFunnelEvent,
    EventType.CHAT_FUNNEL_UPDATED : ChatFunnelEvent,
    EventType.CHAT_FUNNEL_COMPLETED : ChatFunnelEvent,
    EventType.CHAT_FUNNEL_ABANDONED : ChatFunnelEvent,

    #BUSINESS AREAS
    EventType.BUSINESS_AREA_ASSIGNED : ChatBusinessAreaEvent,
    EventType.BUSINESS_AREA_REMOVED : ChatBusinessAreaEvent,
    ##COMPANY EVENTS
    EventType.COMPANY_CREATED : CompanyEvent,
    EventType.COMPANY_UPDATED : CompanyEvent,
    EventType.COMPANY_DELETED : CompanyEvent,
    #PRODUCTS
    EventType.PRODUCT_CREATED : AssetEvent,
    EventType.PRODUCT_UPDATED : AssetEvent,
    EventType.PRODUCT_DELETED : AssetEvent,
    #SOURCES
    EventType.SOURCE_CREATED : AssetEvent,
    EventType.SOURCE_UPDATED : AssetEvent,
    EventType.SOURCE_DELETED : AssetEvent,
    #TAGS
    EventType.TAG_CREATED : AssetEvent,
    EventType.TAG_UPDATED : AssetEvent,
    EventType.TAG_DELETED : AssetEvent,
    #FAST ANSWERS
    EventType.FAST_ANSWER_CREATED : AssetEvent,
    EventType.FAST_ANSWER_UPDATED : AssetEvent,
    EventType.FAST_ANSWER_DELETED : AssetEvent,
    #FUNNEL STAGES
    EventType.FUNNEL_CREATED : AssetEvent,
    EventType.FUNNEL_UPDATED : AssetEvent,
    EventType.FUNNEL_DELETED : AssetEvent,
    EventType.FUNNEL_STAGE_CREATED : AssetEvent,
    EventType.FUNNEL_STAGE_UPDATED : AssetEvent,
    EventType.FUNNEL_STAGE_DELETED : AssetEvent,
    #BUSINESS AREA
    EventType.BUSINESS_AREA_CREATED : AssetEvent,
    EventType.BUSINESS_AREA_UPDATED : AssetEvent,
    EventType.BUSINESS_AREA_DELETED : AssetEvent,
    #WORKFLOWS
    EventType.WORKFLOW_CREATED : AssetEvent,
    EventType.WORKFLOW_UPDATED : AssetEvent,
    EventType.WORKFLOW_DELETED : AssetEvent,
    #AGENTS
    EventType.USER_CREATED : UserEvent,
    EventType.USER_UPDATED : UserEvent,
    EventType.USER_DELETED : UserEvent,
    EventType.USER_LOGGED_IN : UserEvent,
    EventType.USER_LOGGED_OUT : UserEvent,
    EventType.USER_STATUS_UPDATED : UserEvent,
    EventType.USER_ASSIGNED_AREA : UserEvent,
    EventType.USER_UNASSIGNED_AREA : UserEvent,
    EventType.USER_ASSIGNED_FUNNEL : UserEvent,
    EventType.USER_UNASSIGNED_FUNNEL : UserEvent
}

def event_type_to_class(event_type: EventType) -> Type[Event]:
    return EVENT_TO_TYPE_CLASSES[event_type]

def class_to_event_type(event_class: Type[Event]) -> List[EventType]:
    return [k for k, v in EVENT_TO_TYPE_CLASSES.items() if v == event_class]