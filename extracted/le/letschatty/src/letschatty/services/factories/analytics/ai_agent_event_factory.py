"""
AI Agent Event Factory - Helper for creating AI agent execution events

This factory simplifies event creation by providing a consistent interface
for generating both full analytics events and simplified UI events.
"""

from letschatty.models.analytics.events.chat_based_events.ai_agent_execution_event import (
    AIAgentExecutionEvent,
    AIAgentExecutionEventData
)
from letschatty.models.analytics.events.event_types import EventType
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional, Dict, Any
from letschatty.models.utils.types.identifier import StrObjectId
import logging

logger = logging.getLogger(__name__)


class AIAgentEventFactory:
    """
    Factory for creating AI agent execution events with proper context.

    Provides a simplified API for event creation while ensuring all required
    fields are properly populated for analytics and monitoring.
    """

    @staticmethod
    def create_event(
        event_type: EventType,
        chat_id: StrObjectId,
        company_id: StrObjectId,
        frozen_company_name: str,
        ai_agent_id: StrObjectId,
        chain_of_thought_id: StrObjectId,
        trigger: str,
        source: str = "chatty.api",
        decision_type: Optional[str] = None,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None,
        user_rating: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> AIAgentExecutionEvent:
        """
        Create a full AI agent execution event for EventBridge.

        Args:
            event_type: The type of event (from EventType enum)
            chat_id: ID of the chat where the event occurred
            company_id: ID of the company
            frozen_company_name: Company name snapshot for analytics
            ai_agent_id: ID of the AI agent asset
            chain_of_thought_id: ID of the chain of thought execution
            trigger: What triggered the execution (USER_MESSAGE, FOLLOW_UP, etc.)
            source: Event source (e.g., 'chatty.api', 'chatty.lambda')
            decision_type: Type of decision if applicable (send, suggest, escalate, skip)
            error_message: Error message if this is an error event
            duration_ms: Duration of the operation in milliseconds
            user_rating: User rating (1-5 stars) if applicable
            metadata: Additional event-specific data
            trace_id: Trace ID for tracking event flows across systems

        Returns:
            AIAgentExecutionEvent ready to be queued to EventBridge
        """
        return AIAgentExecutionEvent(
            type=event_type,
            time=datetime.now(ZoneInfo("UTC")),
            source=source,
            company_id=company_id,
            frozen_company_name=frozen_company_name,
            specversion="1.0",
            trace_id=trace_id,
            data=AIAgentExecutionEventData(
                chat_id=chat_id,
                ai_agent_id=ai_agent_id,
                chain_of_thought_id=chain_of_thought_id,
                trigger=trigger,
                decision_type=decision_type,
                error_message=error_message,
                duration_ms=duration_ms,
                user_rating=user_rating,
                metadata=metadata
            )
        )

    @staticmethod
    def get_simplified_event_type(event_type: EventType) -> str:
        """
        Convert full EventType to simplified event type string for UI.

        Transforms 'chatty_ai_agent_in_chat.trigger.user_message' -> 'trigger.user_message'
        This provides a cleaner format for embedded events in COT documents.

        Args:
            event_type: Full EventType enum value

        Returns:
            Simplified event type string (e.g., 'trigger.user_message')
        """
        # Extract the last two parts after 'chatty_ai_agent_in_chat.'
        parts = event_type.value.split('.')
        if len(parts) >= 3 and parts[0] == 'chatty_ai_agent_in_chat':
            return '.'.join(parts[1:])  # e.g., 'trigger.user_message'
        return event_type.value  # Fallback to full type if format doesn't match

    @staticmethod
    def get_user_friendly_message(event_type: EventType, **context) -> str:
        """
        Generate a user-friendly message for an event type.

        This provides human-readable descriptions for events that will be
        displayed in the UI as part of the chain of thought timeline.

        Args:
            event_type: The type of event
            **context: Additional context for message formatting (e.g., decision_type, error_message)

        Returns:
            User-friendly message string
        """
        messages = {
            EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_USER_MESSAGE: "Triggered by user message",
            EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_FOLLOW_UP: "Triggered by smart follow-up",
            EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_MANUAL: "Manually triggered",
            EventType.CHATTY_AI_AGENT_IN_CHAT_TRIGGER_RETRY: "Retry triggered",

            EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_PROCESSING_STARTED: "Processing started",
            EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_CALL_STARTED: "AI agent call started",
            EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_ESCALATED: "Escalated to human agent",
            EventType.CHATTY_AI_AGENT_IN_CHAT_STATE_UNESCALATED: "Returned to AI agent",

            EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_GET_CHAT_WITH_PROMPT: "Requesting chat context",
            EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_TAGGER: "Calling tagger service",
            EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_DOUBLE_CHECKER: "Calling double checker",
            EventType.CHATTY_AI_AGENT_IN_CHAT_CALL_DEBUGGER: "Running debugger",

            EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_GET_CHAT_WITH_PROMPT: "Chat context received",
            EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_TAGGER: "Tagger response received",
            EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_DOUBLE_CHECKER: "Double checker validation complete",
            EventType.CHATTY_AI_AGENT_IN_CHAT_CALLBACK_OUTPUT_RECEIVED: "AI agent output received",

            EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SEND: "Decision: Send message",
            EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SUGGEST: "Decision: Suggest message",
            EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_ESCALATE: "Decision: Escalate to human",
            EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SKIP: "Decision: Skip message",
            EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_SENT_TO_API: "Decision sent to API",
            EventType.CHATTY_AI_AGENT_IN_CHAT_DECISION_COMPLETED: "Decision completed successfully",

            EventType.CHATTY_AI_AGENT_IN_CHAT_ERROR_CALL_FAILED: f"Call failed: {context.get('error_message', 'Unknown error')}",
            EventType.CHATTY_AI_AGENT_IN_CHAT_ERROR_CALL_CANCELLED: "Call cancelled",
            EventType.CHATTY_AI_AGENT_IN_CHAT_ERROR_VALIDATION_FAILED: f"Validation failed: {context.get('error_message', 'Invalid data')}",

            EventType.CHATTY_AI_AGENT_IN_CHAT_RATING_RECEIVED: f"User rated: {context.get('user_rating', '?')}/5 stars",
        }

        return messages.get(event_type, str(event_type))

