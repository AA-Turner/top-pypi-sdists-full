from letschatty.models.company.assets.chat_assets import ChainOfThoughtInChatTrigger
from pydantic import BaseModel, Field, model_validator
from typing import Dict, Any, List, Optional

from letschatty.models.base_models.ai_agent_component import AiAgentComponentType
from letschatty.models.utils.types.identifier import StrObjectId
from .lambda_invokation_types import InvokationType, LambdaAiEvent
from .expected_output import ExpectedOutputIncomingMessage, ExpectedOutputSmartTag, ExpectedOutputQualityTest, ExpectedOutputSmartFollowUp, IncomingMessageAIDecision
from ...models.company.assets.ai_agents_v2.ai_agents_decision_output import IncomingMessageDecisionAction
from ...models.company.assets.ai_agents_v2.chatty_ai_agent_in_chat import HumanInterventionReason

class SmartTaggingCallbackMetadata(BaseModel):
    chat_id: StrObjectId
    company_id: StrObjectId

class ComparisonAnalysisCallbackMetadata(BaseModel):
    test_case_id: StrObjectId
    company_id : StrObjectId

class InteractionCallbackMetadata(BaseModel):
    test_case_id: StrObjectId
    chat_example_id: StrObjectId
    ai_agent_id: StrObjectId
    company_id: StrObjectId
    interaction_index: int

class IncomingMessageCallbackMetadata(BaseModel):
    chat_id: StrObjectId
    company_id: StrObjectId
    ai_agent_id: StrObjectId
    cot_id: StrObjectId
    trigger: str
    # Trigger info is in: incoming_message_ids for user_message,
    # triggered_by_user_id for manual_trigger, smart_follow_up_id for follow_up
    triggered_by_user_id: Optional[StrObjectId] = None

class IncomingMessageCallbackEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.INCOMING_MESSAGE_CALLBACK
    data: IncomingMessageAIDecision
    callback_metadata: IncomingMessageCallbackMetadata

class QualityTestCallbackEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.SINGLE_QUALITY_TEST_CALLBACK
    data: ExpectedOutputQualityTest
    callback_metadata: ComparisonAnalysisCallbackMetadata

class QualityTestInteractionCallbackEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.QUALITY_TEST_INTERACTION
    data: ExpectedOutputIncomingMessage
    callback_metadata: InteractionCallbackMetadata

    @model_validator(mode="before")
    def validate_data(cls, data):
        if isinstance(data, dict) and "data" in data and "callback_metadata" in data and "chain_of_thought" in data["data"]:
            data["data"]["chain_of_thought"]["chatty_ai_agent_id"] = data["callback_metadata"]["ai_agent_id"]
        return data

class SmartTaggingCallbackEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.SMART_TAGGING_CALLBACK
    data: ExpectedOutputSmartTag
    callback_metadata: SmartTaggingCallbackMetadata

    @model_validator(mode="before")
    def validate_data(cls, data):
        if isinstance(data, dict) and "data" in data and "chain_of_thought" in data["data"]:
                data["data"]["chain_of_thought"]["chatty_ai_agent_id"] = "000000000000000000000000"
        return data

class ChatData(BaseModel):
    chat_id: StrObjectId
    company_id: StrObjectId

class IncomingMessageEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.INCOMING_MESSAGE
    data: ChatData

class FollowUpEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.FOLLOW_UP
    data: ChatData


class SmartFollowUpDecisionOutputEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.FOLLOW_UP
    data: ExpectedOutputSmartFollowUp

class QualityTestEventData(BaseModel):
    chat_example_id: StrObjectId
    company_id: StrObjectId
    ai_agent_id: StrObjectId

class QualityTestEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.SINGLE_QUALITY_TEST
    data: QualityTestEventData

class AllQualityTestEventData(BaseModel):
    company_id: StrObjectId
    ai_agent_id: StrObjectId

class AllQualityTestEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.ALL_QUALITY_TEST
    data: AllQualityTestEventData

class SmartTaggingEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.SMART_TAGGING
    data: ChatData

class SmartTaggingPromptEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.SMART_TAGGING_PROMPT
    data: ChatData

class QualityTestsForUpdatedAIComponentEventData(BaseModel):
    company_id: StrObjectId
    ai_component_id: StrObjectId
    ai_component_type: AiAgentComponentType

class QualityTestsForUpdatedAIComponentEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.QUALITY_TESTS_FOR_UPDATED_AI_COMPONENT
    data: QualityTestsForUpdatedAIComponentEventData

class FixBuggedAiAgentsCallsInChatsEventData(BaseModel):
    company_id: Optional[StrObjectId] = None

class FixBuggedAiAgentsCallsInChatsEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.FIX_BUGGED_AI_AGENTS_CALLS_IN_CHATS
    data: FixBuggedAiAgentsCallsInChatsEventData = Field(default_factory=FixBuggedAiAgentsCallsInChatsEventData)

class DoubleCheckerForIncomingMessagesAnswerData(BaseModel):
    incoming_message_output: ExpectedOutputIncomingMessage
    chat_id: StrObjectId
    company_id: StrObjectId
    ai_agent_id: StrObjectId
    incoming_messages_ids: List[str]

class DoubleCheckerCallbackMetadata(BaseModel):
    chat_id: StrObjectId
    company_id: StrObjectId
    ai_agent_id: StrObjectId
    incoming_messages_ids: List[str]
    # Trigger info
    trigger: str
    # Trigger info is in: incoming_messages_ids for user_message,
    # triggered_by_user_id for manual_trigger, smart_follow_up_id for follow_up
    triggered_by_user_id: Optional[StrObjectId] = None

class DoubleCheckerForIncomingMessagesAnswerEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.DOUBLE_CHECKER_FOR_INCOMING_MESSAGES_ANSWER
    data: DoubleCheckerForIncomingMessagesAnswerData

class DoubleCheckerForIncomingMessagesAnswerCallbackEvent(LambdaAiEvent):
    type: InvokationType = InvokationType.DOUBLE_CHECKER_FOR_INCOMING_MESSAGES_ANSWER_CALLBACK
    data: DoubleCheckerForIncomingMessagesAnswerData
    callback_metadata: DoubleCheckerCallbackMetadata

class DoubleCheckerForIncomingMessagesAnswerCallbackMetadata(BaseModel):
    chat_id: StrObjectId
    company_id: StrObjectId
    ai_agent_id: StrObjectId


# New AI Agent Context Building Events (for new architecture)

class GetChatWithPromptForIncomingMessageEventData(BaseModel):
    """Data for get chat with prompt for incoming message event"""
    chat_id: StrObjectId
    company_id: StrObjectId
    incoming_message_ids: List[str] = Field(
        default_factory=list,
        description="List of incoming message IDs that triggered the agent"
    )
    # Trigger information
    trigger: ChainOfThoughtInChatTrigger = Field(description="Trigger type (user_message, manual_trigger)")
    # trigger_id is derived from: incoming_message_ids[0] for user_message, triggered_by_user_id for manual_trigger
    triggered_by_user_id: Optional[StrObjectId] = Field(default=None, description="User ID if manual trigger")


class GetChatWithPromptForIncomingMessageEvent(LambdaAiEvent):
    """
    Event to build AI agent context and prompt for an incoming message.

    This event is triggered when a new user message arrives and needs
    to be processed by an AI agent. Lambda will build the complete context
    and return the prompt for the AI agent to process.
    """
    type: InvokationType = InvokationType.GET_CHAT_WITH_PROMPT_INCOMING_MESSAGE
    data: GetChatWithPromptForIncomingMessageEventData


class GetChatWithPromptForFollowUpEventData(BaseModel):
    """Data for get chat with prompt for follow-up event"""
    chat_id: StrObjectId
    company_id: StrObjectId
    smart_follow_up_id: StrObjectId
    # Trigger information
    trigger: ChainOfThoughtInChatTrigger
    # trigger_id is derived from: smart_follow_up_id


class GetChatWithPromptForFollowUpEvent(LambdaAiEvent):
    """
    Event to build AI agent context and prompt for a smart follow-up.

    This event is triggered when a smart follow-up needs to be processed.
    Lambda will build the complete context and return the prompt for the
    AI agent to process the follow-up.
    """
    type: InvokationType = InvokationType.GET_CHAT_WITH_PROMPT_FOLLOW_UP
    data: GetChatWithPromptForFollowUpEventData


# Manual Trigger and Cancel Events

class CancelExecutionEventData(BaseModel):
    """Data for cancel execution event"""
    chat_id: StrObjectId
    company_id: StrObjectId
    reason: Optional[str] = Field(default=None, description="Reason for cancellation")


class CancelExecutionEvent(LambdaAiEvent):
    """
    Event to cancel ongoing AI agent execution for a chat.

    This cancels any in-progress COT and resets the AI agent state
    to allow new executions.
    """
    type: InvokationType = InvokationType.CANCEL_EXECUTION
    data: CancelExecutionEventData


class ManualTriggerEventData(BaseModel):
    """Data for manual trigger event"""
    chat_id: StrObjectId
    company_id: StrObjectId
    triggered_by_user_id: Optional[StrObjectId] = Field(default=None, description="User who triggered manually")


class ManualTriggerEvent(LambdaAiEvent):
    """
    Event to manually trigger AI agent execution.

    This is proxied to N8N which will handle the full workflow including
    calling get_chat_with_prompt with manual trigger context.
    """
    type: InvokationType = InvokationType.MANUAL_TRIGGER
    data: ManualTriggerEventData


# AI Agent Lifecycle Events

class AssignAIAgentToChatEventData(BaseModel):
    """Data for assigning an AI agent to a chat"""
    chat_id: StrObjectId
    company_id: StrObjectId
    ai_agent_id: StrObjectId
    mode: str = Field(description="AI agent mode (autonomous, copilot, suggestions, off)")
    assigned_by: Optional[StrObjectId] = Field(default=None, description="User who assigned the AI agent")


class AssignAIAgentToChatEvent(LambdaAiEvent):
    """
    Event to assign an AI agent to a chat.

    Creates a new ChattyAIAgentInChat document and optionally starts processing
    if there are pending messages.
    """
    type: InvokationType = InvokationType.ASSIGN_AI_AGENT_TO_CHAT
    data: AssignAIAgentToChatEventData


class RemoveAIAgentFromChatEventData(BaseModel):
    """Data for removing an AI agent from a chat"""
    chat_id: StrObjectId
    company_id: StrObjectId
    removed_by: Optional[StrObjectId] = Field(default=None, description="User who removed the AI agent")
    reason: Optional[str] = Field(default=None, description="Reason for removal")


class RemoveAIAgentFromChatEvent(LambdaAiEvent):
    """
    Event to remove an AI agent from a chat.

    Cancels any active execution, deletes the ChattyAIAgentInChat document,
    and cleans up related resources.
    """
    type: InvokationType = InvokationType.REMOVE_AI_AGENT_FROM_CHAT
    data: RemoveAIAgentFromChatEventData


class UpdateAIAgentModeInChatEventData(BaseModel):
    """Data for updating AI agent mode in a chat"""
    chat_id: StrObjectId
    company_id: StrObjectId
    new_mode: str = Field(description="New AI agent mode (autonomous, copilot, suggestions, off)")
    updated_by: Optional[StrObjectId] = Field(default=None, description="User who updated the mode")


class UpdateAIAgentModeInChatEvent(LambdaAiEvent):
    """
    Event to update the AI agent mode for a chat.

    Updates the mode in the ChattyAIAgentInChat document. If switching to OFF,
    may cancel active executions.
    """
    type: InvokationType = InvokationType.UPDATE_AI_AGENT_MODE_IN_CHAT
    data: UpdateAIAgentModeInChatEventData


class EscalateAIAgentInChatEventData(BaseModel):
    """Data for escalating an AI agent (requiring human intervention)"""
    chat_id: StrObjectId
    company_id: StrObjectId
    reason: str = Field(description="Reason for escalation (e.g., 'Complex technical issue', 'Customer request')")


class EscalateAIAgentInChatEvent(LambdaAiEvent):
    """
    Event to escalate an AI agent in a chat.

    Sets the requires_human_intervention flag and records the escalation reason
    for analytics and tracking purposes.
    """
    type: InvokationType = InvokationType.ESCALATE_AI_AGENT_IN_CHAT
    data: EscalateAIAgentInChatEventData


class UnescalateAIAgentInChatEventData(BaseModel):
    """Data for unescalating an AI agent (removing human intervention requirement)"""
    chat_id: StrObjectId
    company_id: StrObjectId
    unescalated_by: Optional[StrObjectId] = Field(default=None, description="User who unescalated")


class UnescalateAIAgentInChatEvent(LambdaAiEvent):
    """
    Event to unescalate an AI agent in a chat.

    Removes the requires_human_intervention flag, allowing the AI agent
    to resume autonomous operation.
    """
    type: InvokationType = InvokationType.UNESCALATE_AI_AGENT_IN_CHAT
    data: UnescalateAIAgentInChatEventData


# Launch Events

class LaunchCommunicationEventData(BaseModel):
    """Data for sending a scheduled launch communication"""
    chat_ids: List[StrObjectId] = Field(description="Batch of chat IDs to send communication to")
    company_id: StrObjectId
    launch_id: StrObjectId
    communication_id: str = Field(description="ID of the communication within the launch")
    communication_type: str = Field(description="Type: pre_launch, post_attended, post_missed, welcome_kit")
    lambda_callback_url: str = Field(description="URL for Lambda to call back after N8N processing")


class LaunchCommunicationEvent(LambdaAiEvent):
    """
    Event to send a scheduled launch communication.

    Triggered by Copilot when delta_minutes is reached. Lambda processes
    the batch of chats, building context for each and sending to N8N
    for AI adaptation (or sending literal messages directly).
    """
    type: InvokationType = InvokationType.LAUNCH_COMMUNICATION
    data: LaunchCommunicationEventData


class LaunchWelcomeKitEventData(BaseModel):
    """Data for sending a welcome kit with AI adaptation"""
    chat_id: StrObjectId
    company_id: StrObjectId
    launch_id: StrObjectId


class LaunchWelcomeKitEvent(LambdaAiEvent):
    """
    Event to send a welcome kit with AI adaptation.

    Triggered when a user subscribes to a launch and the welcome kit
    requires AI adaptation. Lambda builds context and sends to N8N.
    """
    type: InvokationType = InvokationType.LAUNCH_WELCOME_KIT
    data: LaunchWelcomeKitEventData
