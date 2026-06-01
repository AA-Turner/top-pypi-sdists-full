"""
Configuration for OpenAI Agents SDK integration.
"""

import os
from dataclasses import dataclass, field


@dataclass
class OpenAIAgentsConfig:
    """Configuration for OpenAI Agents SDK tracing.

    Attributes:
        trace_agents: Enable agent execution tracing
        trace_generations: Enable LLM generation tracing
        trace_tool_calls: Enable tool/function call tracing
        trace_handoffs: Enable agent handoff tracing
        trace_guardrails: Enable guardrail validation tracing
        capture_inputs: Capture input messages
        capture_outputs: Capture output responses
        capture_tool_args: Capture tool call arguments
        capture_tool_results: Capture tool call results
        max_content_length: Maximum content length to capture
        agent_timeout: Timeout for agent execution in seconds
        generation_timeout: Timeout for LLM generation in seconds
        max_retries: Maximum retry attempts for failed operations
        retry_delay: Initial delay between retries in seconds
        sensitive_patterns: Patterns to mask in captured content
    """

    # Tracing toggles
    trace_agents: bool = True
    trace_generations: bool = True
    trace_tool_calls: bool = True
    trace_handoffs: bool = True
    trace_guardrails: bool = True

    # Capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_tool_args: bool = True
    capture_tool_results: bool = True
    max_content_length: int = 2000

    # Timeouts
    agent_timeout: float = 300.0  # 5 minutes per agent
    generation_timeout: float = 120.0  # 2 minutes per generation
    workflow_timeout: float = 1800.0  # 30 minutes total

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0

    # Privacy
    sensitive_patterns: list[str] = field(default_factory=list)

    # Real-time remediation settings
    enable_realtime_remediation: bool = False
    remediation_mode: str = "recommendation"  # "recommendation" or "autonomous"
    remediation_query_timeout: float = 2.0  # Max seconds to query platform for pattern

    def __post_init__(self):
        """Validate configuration."""
        if self.max_content_length < 0:
            raise ValueError("max_content_length must be non-negative")
        if self.agent_timeout <= 0:
            raise ValueError("agent_timeout must be positive")
        if self.generation_timeout <= 0:
            raise ValueError("generation_timeout must be positive")
        if self.workflow_timeout <= 0:
            raise ValueError("workflow_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
        if self.remediation_mode not in ("recommendation", "autonomous"):
            raise ValueError("remediation_mode must be 'recommendation' or 'autonomous'")
        if self.remediation_query_timeout <= 0:
            raise ValueError("remediation_query_timeout must be positive")

    @classmethod
    def from_env(cls) -> "OpenAIAgentsConfig":
        """Create configuration from environment variables.

        Environment variables:
            AIGIE_OPENAI_AGENTS_TRACE_AGENTS: Trace agent executions (default: true)
            AIGIE_OPENAI_AGENTS_TRACE_GENERATIONS: Trace LLM generations (default: true)
            AIGIE_OPENAI_AGENTS_TRACE_TOOL_CALLS: Trace tool calls (default: true)
            AIGIE_OPENAI_AGENTS_TRACE_HANDOFFS: Trace handoffs (default: true)
            AIGIE_OPENAI_AGENTS_TRACE_GUARDRAILS: Trace guardrails (default: true)
            AIGIE_OPENAI_AGENTS_CAPTURE_INPUTS: Capture inputs (default: true)
            AIGIE_OPENAI_AGENTS_CAPTURE_OUTPUTS: Capture outputs (default: true)
            AIGIE_OPENAI_AGENTS_CAPTURE_TOOL_ARGS: Capture tool args (default: true)
            AIGIE_OPENAI_AGENTS_CAPTURE_TOOL_RESULTS: Capture tool results (default: true)
            AIGIE_OPENAI_AGENTS_MAX_CONTENT_LENGTH: Max content length (default: 2000)
            AIGIE_OPENAI_AGENTS_AGENT_TIMEOUT: Agent timeout (default: 300)
            AIGIE_OPENAI_AGENTS_GENERATION_TIMEOUT: Generation timeout (default: 120)
            AIGIE_OPENAI_AGENTS_WORKFLOW_TIMEOUT: Workflow timeout (default: 1800)
            AIGIE_OPENAI_AGENTS_MAX_RETRIES: Max retries (default: 3)
            AIGIE_OPENAI_AGENTS_RETRY_DELAY: Retry delay (default: 1.0)
            AIGIE_OPENAI_AGENTS_REALTIME_REMEDIATION: Enable remediation (default: false)
            AIGIE_OPENAI_AGENTS_REMEDIATION_MODE: Mode (default: recommendation)
            AIGIE_OPENAI_AGENTS_REMEDIATION_TIMEOUT: Timeout (default: 2.0)
        """
        return cls(
            trace_agents=os.getenv("AIGIE_OPENAI_AGENTS_TRACE_AGENTS", "true").lower() == "true",
            trace_generations=os.getenv("AIGIE_OPENAI_AGENTS_TRACE_GENERATIONS", "true").lower()
            == "true",
            trace_tool_calls=os.getenv("AIGIE_OPENAI_AGENTS_TRACE_TOOL_CALLS", "true").lower()
            == "true",
            trace_handoffs=os.getenv("AIGIE_OPENAI_AGENTS_TRACE_HANDOFFS", "true").lower()
            == "true",
            trace_guardrails=os.getenv("AIGIE_OPENAI_AGENTS_TRACE_GUARDRAILS", "true").lower()
            == "true",
            capture_inputs=os.getenv("AIGIE_OPENAI_AGENTS_CAPTURE_INPUTS", "true").lower()
            == "true",
            capture_outputs=os.getenv("AIGIE_OPENAI_AGENTS_CAPTURE_OUTPUTS", "true").lower()
            == "true",
            capture_tool_args=os.getenv("AIGIE_OPENAI_AGENTS_CAPTURE_TOOL_ARGS", "true").lower()
            == "true",
            capture_tool_results=os.getenv(
                "AIGIE_OPENAI_AGENTS_CAPTURE_TOOL_RESULTS", "true"
            ).lower()
            == "true",
            max_content_length=int(os.getenv("AIGIE_OPENAI_AGENTS_MAX_CONTENT_LENGTH", "2000")),
            agent_timeout=float(os.getenv("AIGIE_OPENAI_AGENTS_AGENT_TIMEOUT", "300.0")),
            generation_timeout=float(os.getenv("AIGIE_OPENAI_AGENTS_GENERATION_TIMEOUT", "120.0")),
            workflow_timeout=float(os.getenv("AIGIE_OPENAI_AGENTS_WORKFLOW_TIMEOUT", "1800.0")),
            max_retries=int(os.getenv("AIGIE_OPENAI_AGENTS_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AIGIE_OPENAI_AGENTS_RETRY_DELAY", "1.0")),
            enable_realtime_remediation=os.getenv(
                "AIGIE_OPENAI_AGENTS_REALTIME_REMEDIATION", "false"
            ).lower()
            == "true",
            remediation_mode=os.getenv("AIGIE_OPENAI_AGENTS_REMEDIATION_MODE", "recommendation"),
            remediation_query_timeout=float(
                os.getenv("AIGIE_OPENAI_AGENTS_REMEDIATION_TIMEOUT", "2.0")
            ),
        )

    def merge(self, **overrides) -> "OpenAIAgentsConfig":
        """Create a new config with overridden values."""
        return OpenAIAgentsConfig(
            trace_agents=overrides.get("trace_agents", self.trace_agents),
            trace_generations=overrides.get("trace_generations", self.trace_generations),
            trace_tool_calls=overrides.get("trace_tool_calls", self.trace_tool_calls),
            trace_handoffs=overrides.get("trace_handoffs", self.trace_handoffs),
            trace_guardrails=overrides.get("trace_guardrails", self.trace_guardrails),
            capture_inputs=overrides.get("capture_inputs", self.capture_inputs),
            capture_outputs=overrides.get("capture_outputs", self.capture_outputs),
            capture_tool_args=overrides.get("capture_tool_args", self.capture_tool_args),
            capture_tool_results=overrides.get("capture_tool_results", self.capture_tool_results),
            max_content_length=overrides.get("max_content_length", self.max_content_length),
            agent_timeout=overrides.get("agent_timeout", self.agent_timeout),
            generation_timeout=overrides.get("generation_timeout", self.generation_timeout),
            workflow_timeout=overrides.get("workflow_timeout", self.workflow_timeout),
            max_retries=overrides.get("max_retries", self.max_retries),
            retry_delay=overrides.get("retry_delay", self.retry_delay),
            sensitive_patterns=overrides.get("sensitive_patterns", self.sensitive_patterns),
            enable_realtime_remediation=overrides.get(
                "enable_realtime_remediation", self.enable_realtime_remediation
            ),
            remediation_mode=overrides.get("remediation_mode", self.remediation_mode),
            remediation_query_timeout=overrides.get(
                "remediation_query_timeout", self.remediation_query_timeout
            ),
        )


# Default configuration
DEFAULT_CONFIG = OpenAIAgentsConfig()
