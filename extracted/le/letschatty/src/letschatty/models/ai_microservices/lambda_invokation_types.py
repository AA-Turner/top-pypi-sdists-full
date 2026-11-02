from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel

class InvokationType(StrEnum):
    INCOMING_MESSAGE = "incoming_message"
    FOLLOW_UP = "follow_up"
    SINGLE_QUALITY_TEST = "single_quality_test"
    ALL_QUALITY_TEST = "all_quality_test"
    SMART_TAGGING = "smart_tagging"
    SMART_TAGGING_PROMPT = "smart_tagging_prompt"
    QUALITY_TEST_INTERACTION = "quality_test_interaction"
    # Callback-specific types
    INCOMING_MESSAGE_CALLBACK = "incoming_message_callback"
    SINGLE_QUALITY_TEST_CALLBACK = "single_quality_test_callback"
    SMART_TAGGING_CALLBACK = "smart_tagging_callback"
    QUALITY_TESTS_FOR_UPDATED_AI_COMPONENT = "quality_tests_for_updated_ai_component"
    FIX_BUGGED_AI_AGENTS_CALLS_IN_CHATS = "fix_bugged_ai_agents_calls_in_chats"
    DOUBLE_CHECKER_FOR_INCOMING_MESSAGES_ANSWER = "double_checker_for_incoming_messages_answer"
    DOUBLE_CHECKER_FOR_INCOMING_MESSAGES_ANSWER_CALLBACK = "double_checker_for_incoming_messages_answer_callback"
    # AI Agent context building events (new architecture)
    GET_CHAT_WITH_PROMPT_INCOMING_MESSAGE = "get_chat_with_prompt_incoming_message"
    GET_CHAT_WITH_PROMPT_FOLLOW_UP = "get_chat_with_prompt_follow_up"
    # Manual trigger and cancel events
    CANCEL_EXECUTION = "cancel_execution"
    MANUAL_TRIGGER = "manual_trigger"
    # AI Agent lifecycle events (assign, remove, update, escalate, unescalate)
    ASSIGN_AI_AGENT_TO_CHAT = "assign_ai_agent_to_chat"
    REMOVE_AI_AGENT_FROM_CHAT = "remove_ai_agent_from_chat"
    UPDATE_AI_AGENT_MODE_IN_CHAT = "update_ai_agent_mode_in_chat"
    ESCALATE_AI_AGENT_IN_CHAT = "escalate_ai_agent_in_chat"
    UNESCALATE_AI_AGENT_IN_CHAT = "unescalate_ai_agent_in_chat"
    # Launch events
    LAUNCH_COMMUNICATION = "launch_communication"
    LAUNCH_WELCOME_KIT = "launch_welcome_kit"

class LambdaAiEvent(BaseModel):
    type: InvokationType
    data: dict
