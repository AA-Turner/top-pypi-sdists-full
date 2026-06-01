"""
Configuration for Agno integration.
"""

import os
from dataclasses import dataclass


@dataclass
class AgnoConfig:
    """
    Configuration for Agno integration.

    Attributes:
        enabled: Whether tracing is enabled
        trace_agents: Whether to trace agent invocations
        trace_tools: Whether to trace tool calls
        trace_teams: Whether to trace Team invocations
        capture_inputs: Whether to capture input data
        capture_outputs: Whether to capture output data
        capture_messages: Whether to capture message content
        redact_pii: Whether to redact PII from traces
        max_content_length: Maximum length of captured content
        max_message_length: Maximum length of captured messages
        max_tool_result_length: Maximum length of captured tool results
        agent_timeout: Timeout in seconds for agent operations
        llm_timeout: Timeout in seconds for LLM calls
        tool_timeout: Timeout in seconds for tool executions
        max_retries: Maximum number of retries for failed operations
        retry_delay: Initial delay between retries in seconds (exponential backoff)
        retry_on_errors: List of error types to retry on (empty = retry all transient)
        enable_realtime_remediation: Enable real-time remediation
        remediation_mode: Remediation mode - recommendation or autonomous
        remediation_query_timeout: Max seconds to query platform
    """

    enabled: bool = True
    trace_agents: bool = True
    trace_tools: bool = True
    trace_teams: bool = True
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_messages: bool = True
    redact_pii: bool = False
    max_content_length: int = 2000
    max_message_length: int = 2000
    max_tool_result_length: int = 1000

    # Timeout settings (in seconds)
    agent_timeout: float = 300.0  # 5 minutes for agent operations
    llm_timeout: float = 120.0  # 2 minutes for LLM calls
    tool_timeout: float = 60.0  # 1 minute for tools

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0  # Initial delay, doubles each retry
    retry_on_errors: list = None  # Empty = retry all transient errors

    # Real-time remediation settings
    enable_realtime_remediation: bool = False
    remediation_mode: str = "recommendation"  # "recommendation" or "autonomous"
    remediation_query_timeout: float = 2.0  # Max seconds to query platform for pattern

    def __post_init__(self):
        """Validate configuration."""
        if self.retry_on_errors is None:
            self.retry_on_errors = []
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.max_message_length < 100:
            raise ValueError("max_message_length must be at least 100")
        if self.max_tool_result_length < 100:
            raise ValueError("max_tool_result_length must be at least 100")
        if self.agent_timeout <= 0:
            raise ValueError("agent_timeout must be positive")
        if self.llm_timeout <= 0:
            raise ValueError("llm_timeout must be positive")
        if self.tool_timeout <= 0:
            raise ValueError("tool_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
        if self.remediation_mode not in ("recommendation", "autonomous"):
            raise ValueError("remediation_mode must be 'recommendation' or 'autonomous'")
        if self.remediation_query_timeout <= 0:
            raise ValueError("remediation_query_timeout must be positive")

    @classmethod
    def from_env(cls) -> "AgnoConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_AGNO_ENABLED: Enable/disable tracing (default: true)
            AIGIE_AGNO_TRACE_AGENTS: Trace agent invocations (default: true)
            AIGIE_AGNO_TRACE_TOOLS: Trace tool calls (default: true)
            AIGIE_AGNO_TRACE_TEAMS: Trace Team invocations (default: true)
            AIGIE_AGNO_CAPTURE_INPUTS: Capture input data (default: true)
            AIGIE_AGNO_CAPTURE_OUTPUTS: Capture output data (default: true)
            AIGIE_AGNO_CAPTURE_MESSAGES: Capture messages (default: true)
            AIGIE_AGNO_REDACT_PII: Redact PII (default: false)
            AIGIE_AGNO_MAX_CONTENT_LENGTH: Max content length (default: 2000)
            AIGIE_AGNO_MAX_MESSAGE_LENGTH: Max message length (default: 2000)
            AIGIE_AGNO_MAX_TOOL_RESULT_LENGTH: Max tool result length (default: 1000)
            AIGIE_AGNO_AGENT_TIMEOUT: Agent timeout in seconds (default: 300)
            AIGIE_AGNO_LLM_TIMEOUT: LLM timeout in seconds (default: 120)
            AIGIE_AGNO_TOOL_TIMEOUT: Tool timeout in seconds (default: 60)
            AIGIE_AGNO_MAX_RETRIES: Max retry attempts (default: 3)
            AIGIE_AGNO_RETRY_DELAY: Initial retry delay in seconds (default: 1.0)
            AIGIE_AGNO_REALTIME_REMEDIATION: Enable real-time remediation (default: false)
            AIGIE_AGNO_REMEDIATION_MODE: Remediation mode (default: recommendation)
            AIGIE_AGNO_REMEDIATION_TIMEOUT: Max seconds to query platform (default: 2.0)
        """
        return cls(
            enabled=os.getenv("AIGIE_AGNO_ENABLED", "true").lower() == "true",
            trace_agents=os.getenv("AIGIE_AGNO_TRACE_AGENTS", "true").lower() == "true",
            trace_tools=os.getenv("AIGIE_AGNO_TRACE_TOOLS", "true").lower() == "true",
            trace_teams=os.getenv("AIGIE_AGNO_TRACE_TEAMS", "true").lower() == "true",
            capture_inputs=os.getenv("AIGIE_AGNO_CAPTURE_INPUTS", "true").lower() == "true",
            capture_outputs=os.getenv("AIGIE_AGNO_CAPTURE_OUTPUTS", "true").lower() == "true",
            capture_messages=os.getenv("AIGIE_AGNO_CAPTURE_MESSAGES", "true").lower() == "true",
            redact_pii=os.getenv("AIGIE_AGNO_REDACT_PII", "false").lower() == "true",
            max_content_length=int(os.getenv("AIGIE_AGNO_MAX_CONTENT_LENGTH", "2000")),
            max_message_length=int(os.getenv("AIGIE_AGNO_MAX_MESSAGE_LENGTH", "2000")),
            max_tool_result_length=int(os.getenv("AIGIE_AGNO_MAX_TOOL_RESULT_LENGTH", "1000")),
            agent_timeout=float(os.getenv("AIGIE_AGNO_AGENT_TIMEOUT", "300.0")),
            llm_timeout=float(os.getenv("AIGIE_AGNO_LLM_TIMEOUT", "120.0")),
            tool_timeout=float(os.getenv("AIGIE_AGNO_TOOL_TIMEOUT", "60.0")),
            max_retries=int(os.getenv("AIGIE_AGNO_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AIGIE_AGNO_RETRY_DELAY", "1.0")),
            enable_realtime_remediation=os.getenv(
                "AIGIE_AGNO_REALTIME_REMEDIATION", "false"
            ).lower()
            == "true",
            remediation_mode=os.getenv("AIGIE_AGNO_REMEDIATION_MODE", "recommendation"),
            remediation_query_timeout=float(os.getenv("AIGIE_AGNO_REMEDIATION_TIMEOUT", "2.0")),
        )

    def merge(self, **overrides) -> "AgnoConfig":
        """
        Create a new config with overridden values.

        Args:
            **overrides: Values to override

        Returns:
            New AgnoConfig with overrides applied
        """
        return AgnoConfig(
            enabled=overrides.get("enabled", self.enabled),
            trace_agents=overrides.get("trace_agents", self.trace_agents),
            trace_tools=overrides.get("trace_tools", self.trace_tools),
            trace_teams=overrides.get("trace_teams", self.trace_teams),
            capture_inputs=overrides.get("capture_inputs", self.capture_inputs),
            capture_outputs=overrides.get("capture_outputs", self.capture_outputs),
            capture_messages=overrides.get("capture_messages", self.capture_messages),
            redact_pii=overrides.get("redact_pii", self.redact_pii),
            max_content_length=overrides.get("max_content_length", self.max_content_length),
            max_message_length=overrides.get("max_message_length", self.max_message_length),
            max_tool_result_length=overrides.get(
                "max_tool_result_length", self.max_tool_result_length
            ),
            agent_timeout=overrides.get("agent_timeout", self.agent_timeout),
            llm_timeout=overrides.get("llm_timeout", self.llm_timeout),
            tool_timeout=overrides.get("tool_timeout", self.tool_timeout),
            max_retries=overrides.get("max_retries", self.max_retries),
            retry_delay=overrides.get("retry_delay", self.retry_delay),
            retry_on_errors=overrides.get("retry_on_errors", self.retry_on_errors),
            enable_realtime_remediation=overrides.get(
                "enable_realtime_remediation", self.enable_realtime_remediation
            ),
            remediation_mode=overrides.get("remediation_mode", self.remediation_mode),
            remediation_query_timeout=overrides.get(
                "remediation_query_timeout", self.remediation_query_timeout
            ),
        )
