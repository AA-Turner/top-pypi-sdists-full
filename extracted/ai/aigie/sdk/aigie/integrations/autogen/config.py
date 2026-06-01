"""
Configuration for AutoGen/AG2 tracing.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AutoGenConfig:
    """Configuration for AutoGen/AG2 tracing behavior.

    Attributes:
        trace_conversations: Whether to trace conversation flows
        trace_agents: Whether to trace individual agent interactions
        trace_messages: Whether to trace individual messages
        trace_llm_calls: Whether to trace LLM calls within agents
        trace_tool_calls: Whether to trace tool/function invocations
        trace_code_execution: Whether to trace code execution blocks
        trace_group_chats: Whether to trace group chat orchestration
        capture_inputs: Whether to capture message content
        capture_outputs: Whether to capture response content
        capture_code: Whether to capture code blocks
        max_content_length: Maximum content length to capture
        mask_sensitive_data: Whether to mask potentially sensitive data
        conversation_timeout: Timeout in seconds for entire conversation
        turn_timeout: Timeout in seconds for individual turns
        llm_timeout: Timeout in seconds for LLM calls
        max_retries: Maximum number of retries for failed operations
        retry_delay: Initial delay between retries in seconds (exponential backoff)
        retry_on_errors: List of error types to retry on (empty = retry all transient)
    """

    # Tracing toggles
    trace_conversations: bool = True
    trace_agents: bool = True
    trace_messages: bool = True
    trace_llm_calls: bool = True
    trace_tool_calls: bool = True
    trace_code_execution: bool = True
    trace_group_chats: bool = True

    # Data capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_code: bool = True
    max_content_length: int = 2000

    # Privacy
    mask_sensitive_data: bool = False

    # Span naming
    span_prefix: str = "autogen"

    # Timeout settings (in seconds)
    conversation_timeout: float = 1800.0  # 30 minutes for full conversation
    turn_timeout: float = 300.0  # 5 minutes per turn
    llm_timeout: float = 120.0  # 2 minutes for LLM calls

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0  # Initial delay, doubles each retry
    retry_on_errors: list[str] = field(default_factory=list)  # Empty = retry all transient

    # Metadata
    default_tags: dict[str, str] = field(default_factory=dict)
    default_metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration."""
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.conversation_timeout <= 0:
            raise ValueError("conversation_timeout must be positive")
        if self.turn_timeout <= 0:
            raise ValueError("turn_timeout must be positive")
        if self.llm_timeout <= 0:
            raise ValueError("llm_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
