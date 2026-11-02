from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import StrEnum
from ..utils.types import StrObjectId


class InsightType(StrEnum):
    """Type of insight detected"""
    SENTIMENT = "sentiment"
    BUYING_SIGNAL = "buying_signal"
    PAIN_POINT = "pain_point"
    UNRESOLVED_QUESTION = "unresolved_question"
    COMPETITOR_MENTION = "competitor_mention"
    FEATURE_REQUEST = "feature_request"
    ESCALATION_SIGNAL = "escalation_signal"
    PAYMENT_INTENT = "payment_intent"
    CHURN_RISK = "churn_risk"
    OPPORTUNITY = "opportunity"
    OBJECTION = "objection"


class InsightUrgency(StrEnum):
    """Urgency level of the insight"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InsightProcessingTier(StrEnum):
    """Processing tier that generated the insight"""
    REALTIME = "realtime"  # Detected during tagger agent run
    BATCH = "batch"  # Detected in scheduled batch processing
    ON_DEMAND = "on_demand"  # Detected in business-triggered analysis


class ChatInsight(BaseModel):
    """
    Represents a business insight discovered from a chat conversation.
    Insights are patterns, signals, or observations that provide business intelligence.
    """
    chat_id: StrObjectId = Field(description="ID of the chat where insight was detected")
    company_id: StrObjectId = Field(description="ID of the company")

    insight_type: InsightType = Field(description="Type of insight")
    category: Optional[str] = Field(
        default=None,
        description="Business-defined category or AI-discovered subcategory"
    )
    content: str = Field(description="Description of the insight")

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score for insight detection (0-1)"
    )
    urgency: InsightUrgency = Field(
        default=InsightUrgency.LOW,
        description="Urgency level of the insight"
    )

    detected_at: datetime = Field(description="When insight was detected")
    interaction_index: Optional[int] = Field(
        default=None,
        description="Index of interaction where insight was detected"
    )

    processing_tier: InsightProcessingTier = Field(
        description="Which processing tier generated this insight"
    )

    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata about the insight"
    )

    related_topics: list[str] = Field(
        default_factory=list,
        description="Conversation topics related to this insight"
    )

    action_taken: Optional[str] = Field(
        default=None,
        description="Any automated action taken based on this insight"
    )

    @classmethod
    def example_sentiment(cls) -> dict:
        """Example sentiment insight"""
        return {
            "chat_id": "chat_123",
            "company_id": "company_456",
            "insight_type": "sentiment",
            "category": "frustration",
            "content": "Customer frustrated with delayed response times",
            "confidence": 0.88,
            "urgency": "medium",
            "detected_at": "2025-10-29T10:30:00Z",
            "interaction_index": 7,
            "processing_tier": "realtime",
            "metadata": {
                "sentiment_score": -0.6,
                "keywords": ["frustrated", "delayed", "slow"]
            },
            "related_topics": ["support", "response_time"]
        }

    @classmethod
    def example_payment_intent(cls) -> dict:
        """Example payment intent insight (urgent)"""
        return {
            "chat_id": "chat_789",
            "company_id": "company_456",
            "insight_type": "payment_intent",
            "category": "immediate_purchase",
            "content": "Customer requested payment link, ready to purchase now",
            "confidence": 0.95,
            "urgency": "high",
            "detected_at": "2025-10-29T11:00:00Z",
            "interaction_index": 12,
            "processing_tier": "realtime",
            "metadata": {
                "payment_method_mentioned": "credit_card",
                "approximate_amount": "50000"
            },
            "related_topics": ["pricing", "payment"],
            "action_taken": "chat_escalated_to_sales"
        }

    @classmethod
    def example_unresolved_question(cls) -> dict:
        """Example unresolved question insight"""
        return {
            "chat_id": "chat_321",
            "company_id": "company_456",
            "insight_type": "unresolved_question",
            "category": "warranty_coverage",
            "content": "Customer asked if warranty covers water damage, AI didn't provide clear answer",
            "confidence": 0.82,
            "urgency": "medium",
            "detected_at": "2025-10-29T12:00:00Z",
            "interaction_index": 9,
            "processing_tier": "batch",
            "metadata": {
                "question": "Does the warranty cover water damage?",
                "ai_response_quality": "partial",
                "requires_human_follow_up": True
            },
            "related_topics": ["warranty", "product_coverage"]
        }


class DetectedInsight(BaseModel):
    """
    Represents an insight detected by AI in current interaction.
    Used as part of tagger agent output for real-time insights.
    """
    insight_type: InsightType = Field(description="Type of insight")
    category: str = Field(description="Business-defined or AI-discovered category")
    content: str = Field(description="Description of the insight")
    urgency: InsightUrgency = Field(description="Urgency level")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score (0-1)"
    )

    @classmethod
    def example(cls) -> dict:
        """Example detected insight"""
        return {
            "insight_type": "payment_intent",
            "category": "immediate_purchase",
            "content": "Customer requested payment link",
            "urgency": "high",
            "confidence": 0.95
        }

    @classmethod
    def get_json_schema_property(cls) -> dict:
        """Returns JSON schema for OpenAI structured output"""
        return {
            "type": "object",
            "properties": {
                "insight_type": {
                    "type": "string",
                    "enum": [t.value for t in InsightType],
                    "description": "Type of insight detected"
                },
                "category": {
                    "type": "string",
                    "description": "Business-defined or AI-discovered category"
                },
                "content": {
                    "type": "string",
                    "description": "Description of what you observed"
                },
                "urgency": {
                    "type": "string",
                    "enum": [u.value for u in InsightUrgency],
                    "description": "Urgency level (low, medium, high, critical)"
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Confidence score 0-1"
                }
            },
            "required": ["insight_type", "category", "content", "urgency", "confidence"],
            "additionalProperties": False
        }

