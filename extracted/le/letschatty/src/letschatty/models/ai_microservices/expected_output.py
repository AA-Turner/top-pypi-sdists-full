from letschatty.models.messages.chatty_messages.base.message_draft import MessageDraft
from letschatty.models.messages.chatty_messages.schema.chatty_content.content_text import ChattyContentText
from letschatty.models.utils.types import StrObjectId
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime

from letschatty.models.utils.types.message_types import MessageType
from ...models.company.assets.ai_agents_v2.ai_agents_decision_output import ChainOfThoughtInChatRequest, IncomingMessageAIDecision, IncomingMessageDecisionAction
from ...models.company.assets.automation import Automation
from ...models.company.form_field import CollectedData

class ExpectedOutputQualityTest(BaseModel):
    accuracy: float = Field(description="The accuracy of the comparison analysis")
    comments: Optional[str] = Field(description="The comments of the comparison analysis")

class ExpectedOutputSmartTag(BaseModel):
    automation: Automation
    conversation_topics: List[str] = Field(
        default_factory=list,
        description="List of conversation topic names detected in this interaction"
    )
    data_collection: CollectedData = Field(
        default_factory=CollectedData,
        description="Structured customer data extracted from conversation"
    )
    chain_of_thought: ChainOfThoughtInChatRequest = Field(
        description="REQUIRED: Your reasoning process and response decision explanation"
    )
    # Unsubscribe intent detection (for launch agents)
    unsubscribe_intent: bool = Field(
        default=False,
        description="True if user expressed intent to unsubscribe from communications (e.g., 'no more messages', 'unsubscribe', 'stop', 'rechazar mensajes')"
    )
    # Acceptance criteria evaluation (for agents with data collection + acceptance_criteria)
    acceptance_criteria_met: Optional[bool] = Field(
        default=None,
        description="True if user meets acceptance criteria, False if not, None if cannot be determined yet or no criteria configured"
    )
    acceptance_criteria_reason: Optional[str] = Field(
        default=None,
        description="Reason explaining why acceptance criteria is met or not met"
    )

    @staticmethod
    def get_json_schema() -> dict:
        """
        Returns the complete JSON schema for OpenAI structured output.
        This ensures schema and model are always in sync.
        """
        return {
            "type": "object",
            "properties": {
                "automation": {
                    "type": "object",
                    "properties": {
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of tag IDs to apply to the chat"
                        },
                        "products": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of product IDs to associate with the chat"
                        },
                        "flow": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of flow IDs to apply"
                        },
                        "highlight_description": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "description": "Optional description to highlight"
                        },
                        "agent_id": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "description": "Optional agent ID if area is with_agent"
                        }
                    },
                    "required": ["tags", "products", "flow", "highlight_description", "agent_id"],
                    "additionalProperties": False
                },
                "conversation_topics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of conversation topic names detected in this interaction (e.g., ['delivery_time', 'prices'])"
                },
                "data_collection": CollectedData.get_json_schema_property(),
                "chain_of_thought": {
                    "type": "object",
                    "properties": {
                        "trigger": {
                            "type": "string",
                            "enum": ["user_message", "follow_up", "manual_trigger", "automatic_tagging"],
                            "description": "Type of event triggering this decision"
                        },
                        "trigger_id": {
                            "type": "string",
                            "description": "ID of the trigger event"
                        },
                        "chatty_ai_agent_id": {
                            "type": "string",
                            "description": "Your AI agent identifier (will be provided in context)"
                        },
                        "chain_of_thought": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "description": "Your detailed reasoning for the automation decision"
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Confidence score for the automation decision, normalized between 0 and 100"
                        },
                        "title": {
                            "type": "string",
                            "description": "Short summary of your decision (e.g., 'Tagging as urgent billing issue')"
                        }
                    },
                    "required": ["trigger", "trigger_id", "chatty_ai_agent_id", "chain_of_thought", "confidence", "title"],
                    "additionalProperties": False
                },
                "unsubscribe_intent": {
                    "type": "boolean",
                    "description": "True if user expressed intent to unsubscribe from communications (e.g., 'no more messages', 'unsubscribe', 'stop', 'rechazar mensajes')"
                },
                "acceptance_criteria_met": {
                    "anyOf": [{"type": "boolean"}, {"type": "null"}],
                    "description": "True if user meets acceptance criteria, False if not, null if cannot be determined yet"
                },
                "acceptance_criteria_reason": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "description": "Reason explaining why acceptance criteria is met or not met"
                }
            },
            "required": ["automation", "conversation_topics", "data_collection", "chain_of_thought", "unsubscribe_intent", "acceptance_criteria_met", "acceptance_criteria_reason"],
            "additionalProperties": False
        }

    @staticmethod
    def get_example() -> dict:
        """
        Returns a complete example of the expected output.
        Useful for testing and documentation.
        """
        return {
            "automation": {
                "tags": ["tag_id_123", "tag_id_456"],
                "products": ["product_id_789"],
                "flow": [],
                "highlight_description": "Customer interested in bulk purchase",
                "agent_id": None
            },
            "conversation_topics": ["delivery_time", "prices"],
            "data_collection": {
                "email": "customer@example.com",
                "phone": "+5491123456789",
                "dni": None,
                "additional_fields": {
                    "budget": "50000-100000",
                    "timeline": "this_month"
                }
            },
            "chain_of_thought": {
                "trigger": "automatic_tagging",
                "trigger_id": "chat_id_123",
                "chatty_ai_agent_id": "agent_456",
                "chain_of_thought": "Customer is interested in bulk purchase with specific delivery requirements. Tagged as high-value lead with delivery concerns. Collected contact info and budget details.",
                "confidence": 88,
                "title": "High-value bulk purchase lead - delivery concerns"
            }
        }

class ExpectedOutputIncomingMessage(BaseModel):
    action: IncomingMessageDecisionAction
    messages: List[str] = Field(description="Array of message strings to send to the customer. Required for send/suggest actions, optional for escalate action, empty array for skip/remove actions.")
    chain_of_thought: ChainOfThoughtInChatRequest = Field(description="REQUIRED: Your reasoning process and response decision explanation")
    confidence: Optional[int] = Field(
        default=None,
        ge=0,
        le=100,
        description="Confidence level 0-100"
    )

    def to_incoming_message_decision_output(self) -> IncomingMessageAIDecision:
        messages_drafts = [
            MessageDraft(
                type=MessageType.TEXT,
                content=ChattyContentText(body=message),
                is_incoming_message=False
            )
            for message in self.messages
        ]
        incoming_decision = IncomingMessageAIDecision(
            action=self.action,
            messages=messages_drafts,
            chain_of_thought=self.chain_of_thought
        )
        return incoming_decision


class ExpectedOutputSmartFollowUp(BaseModel):
    action: Optional[str] = None
