"""AI Agent Execution Events - Track AI agent lifecycle and decision-making"""

from ..base import Event, EventData
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from typing import ClassVar, Optional, Dict, Any
from ....utils.types.identifier import StrObjectId


class AIAgentExecutionEventData(CustomerEventData):
    """Data for AI agent execution events"""
    ai_agent_id: StrObjectId
    chain_of_thought_id: StrObjectId
    trigger: str  # USER_MESSAGE, FOLLOW_UP, MANUAL_TRIGGER, RETRY
    decision_type: Optional[str] = None  # send, suggest, escalate, skip
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None
    user_rating: Optional[int] = None  # 1-5 stars
    metadata: Optional[Dict[str, Any]] = None


class AIAgentExecutionEvent(Event):
    """
    Events for AI agent execution lifecycle.

    This event type covers the entire AI agent decision-making process,
    from trigger to final decision, including all intermediate steps.
    """
    data: AIAgentExecutionEventData

    VALID_TYPES: ClassVar[set] = {
        # Trigger events
        EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_USER_MESSAGE,
        EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_FOLLOW_UP,
        EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_MANUAL,
        EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_RETRY,

        # State events
        EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_PROCESSING_STARTED,
        EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_CALL_STARTED,
        EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_ESCALATED,
        EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_UNESCALATED,

        # Call events
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_GET_CHAT_WITH_PROMPT,
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_TAGGER,
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_DOUBLE_CHECKER,
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_DEBUGGER,

        # Callback events
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_GET_CHAT_WITH_PROMPT,
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_TAGGER,
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_DOUBLE_CHECKER,
        EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_OUTPUT_RECEIVED,

        # Decision events
        EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SEND,
        EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SUGGEST,
        EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_ESCALATE,
        EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SKIP,
        EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SENT_TO_API,
        EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_COMPLETED,

        # Error events
        EventType.CHATTY_AI_AGENT_IN_CHAT_ERROR_CALL_FAILED,
        EventType.CHATTY_AI_AGENT_IN_CHAT_ERROR_CALL_CANCELLED,
        EventType.CHATTY_AI_AGENT_IN_CHAT_ERROR_VALIDATION_FAILED,

        # Rating events
        EventType.CHATTY_AI_AGENT_IN_CHAT_RATING_RECEIVED,
    }
