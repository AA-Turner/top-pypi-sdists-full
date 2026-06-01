"""
Configuration for LangChain tracing.
"""

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LangChainConfig:
    """Configuration for LangChain tracing behavior.

    Attributes:
        trace_chains: Whether to trace chain executions
        trace_agents: Whether to trace agent executions
        trace_llm_calls: Whether to trace LLM calls
        trace_tool_calls: Whether to trace tool invocations
        trace_retrievers: Whether to trace retriever operations
        capture_inputs: Whether to capture input data
        capture_outputs: Whether to capture output data
        capture_prompts: Whether to capture LLM prompts
        max_content_length: Maximum content length to capture
        mask_sensitive_data: Whether to mask potentially sensitive data
        chain_timeout: Timeout in seconds for chain operations
        llm_timeout: Timeout in seconds for LLM calls
        tool_timeout: Timeout in seconds for tool executions
        max_retries: Maximum number of retries for failed operations
        retry_delay: Initial delay between retries in seconds (exponential backoff)
        retry_on_errors: List of error types to retry on (empty = retry all transient)
    """

    # Tracing toggles
    trace_chains: bool = True
    trace_agents: bool = True
    trace_llm_calls: bool = True
    trace_tool_calls: bool = True
    trace_retrievers: bool = True

    # Data capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_prompts: bool = True
    max_content_length: int = 2000

    # Privacy
    mask_sensitive_data: bool = False
    redact_pii: bool = False  # Whether to redact PII from traces

    # Span naming
    span_prefix: str = "langchain"

    # Timeout settings (in seconds)
    chain_timeout: float = 300.0  # 5 minutes for chains
    llm_timeout: float = 120.0  # 2 minutes for LLM calls
    tool_timeout: float = 60.0  # 1 minute for tools

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0  # Initial delay, doubles each retry
    retry_on_errors: list[str] = field(default_factory=list)  # Empty = retry all transient

    # Remediation settings
    enable_realtime_remediation: bool = False
    remediation_mode: str = "observe"  # "observe" (read-only) or "autonomous"
    remediation_query_timeout: float = 2.0

    # Metadata
    default_tags: dict[str, str] = field(default_factory=dict)
    default_metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration."""
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.chain_timeout <= 0:
            raise ValueError("chain_timeout must be positive")
        if self.llm_timeout <= 0:
            raise ValueError("llm_timeout must be positive")
        if self.tool_timeout <= 0:
            raise ValueError("tool_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")

    @classmethod
    def from_env(cls) -> "LangChainConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_LANGCHAIN_TRACE_CHAINS: Trace chain executions (default: true)
            AIGIE_LANGCHAIN_TRACE_AGENTS: Trace agent executions (default: true)
            AIGIE_LANGCHAIN_TRACE_LLM: Trace LLM calls (default: true)
            AIGIE_LANGCHAIN_TRACE_TOOLS: Trace tool invocations (default: true)
            AIGIE_LANGCHAIN_TRACE_RETRIEVERS: Trace retriever operations (default: true)
            AIGIE_LANGCHAIN_CAPTURE_INPUTS: Capture input data (default: true)
            AIGIE_LANGCHAIN_CAPTURE_OUTPUTS: Capture output data (default: true)
            AIGIE_LANGCHAIN_CAPTURE_PROMPTS: Capture LLM prompts (default: true)
            AIGIE_LANGCHAIN_MAX_CONTENT_LENGTH: Max content length (default: 2000)
            AIGIE_LANGCHAIN_MASK_SENSITIVE: Mask sensitive data (default: false)
            AIGIE_LANGCHAIN_CHAIN_TIMEOUT: Chain timeout in seconds (default: 300)
            AIGIE_LANGCHAIN_LLM_TIMEOUT: LLM timeout in seconds (default: 120)
            AIGIE_LANGCHAIN_TOOL_TIMEOUT: Tool timeout in seconds (default: 60)
            AIGIE_LANGCHAIN_MAX_RETRIES: Max retry attempts (default: 3)
            AIGIE_LANGCHAIN_RETRY_DELAY: Initial retry delay in seconds (default: 1.0)
        """
        return cls(
            trace_chains=os.getenv("AIGIE_LANGCHAIN_TRACE_CHAINS", "true").lower() == "true",
            trace_agents=os.getenv("AIGIE_LANGCHAIN_TRACE_AGENTS", "true").lower() == "true",
            trace_llm_calls=os.getenv("AIGIE_LANGCHAIN_TRACE_LLM", "true").lower() == "true",
            trace_tool_calls=os.getenv("AIGIE_LANGCHAIN_TRACE_TOOLS", "true").lower() == "true",
            trace_retrievers=os.getenv("AIGIE_LANGCHAIN_TRACE_RETRIEVERS", "true").lower()
            == "true",
            capture_inputs=os.getenv("AIGIE_LANGCHAIN_CAPTURE_INPUTS", "true").lower() == "true",
            capture_outputs=os.getenv("AIGIE_LANGCHAIN_CAPTURE_OUTPUTS", "true").lower() == "true",
            capture_prompts=os.getenv("AIGIE_LANGCHAIN_CAPTURE_PROMPTS", "true").lower() == "true",
            max_content_length=int(os.getenv("AIGIE_LANGCHAIN_MAX_CONTENT_LENGTH", "2000")),
            mask_sensitive_data=os.getenv("AIGIE_LANGCHAIN_MASK_SENSITIVE", "false").lower()
            == "true",
            redact_pii=os.getenv("AIGIE_LANGCHAIN_REDACT_PII", "false").lower() == "true",
            chain_timeout=float(os.getenv("AIGIE_LANGCHAIN_CHAIN_TIMEOUT", "300.0")),
            llm_timeout=float(os.getenv("AIGIE_LANGCHAIN_LLM_TIMEOUT", "120.0")),
            tool_timeout=float(os.getenv("AIGIE_LANGCHAIN_TOOL_TIMEOUT", "60.0")),
            max_retries=int(os.getenv("AIGIE_LANGCHAIN_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AIGIE_LANGCHAIN_RETRY_DELAY", "1.0")),
            enable_realtime_remediation=os.getenv("AIGIE_LANGCHAIN_REMEDIATION", "false").lower()
            == "true",
            remediation_mode=os.getenv("AIGIE_LANGCHAIN_REMEDIATION_MODE", "observe"),
            remediation_query_timeout=float(
                os.getenv("AIGIE_LANGCHAIN_REMEDIATION_TIMEOUT", "2.0")
            ),
        )

    def merge(self, **overrides) -> "LangChainConfig":
        """
        Create a new config with overridden values.

        Args:
            **overrides: Values to override

        Returns:
            New LangChainConfig with overrides applied
        """
        return LangChainConfig(
            trace_chains=overrides.get("trace_chains", self.trace_chains),
            trace_agents=overrides.get("trace_agents", self.trace_agents),
            trace_llm_calls=overrides.get("trace_llm_calls", self.trace_llm_calls),
            trace_tool_calls=overrides.get("trace_tool_calls", self.trace_tool_calls),
            trace_retrievers=overrides.get("trace_retrievers", self.trace_retrievers),
            capture_inputs=overrides.get("capture_inputs", self.capture_inputs),
            capture_outputs=overrides.get("capture_outputs", self.capture_outputs),
            capture_prompts=overrides.get("capture_prompts", self.capture_prompts),
            max_content_length=overrides.get("max_content_length", self.max_content_length),
            mask_sensitive_data=overrides.get("mask_sensitive_data", self.mask_sensitive_data),
            redact_pii=overrides.get("redact_pii", self.redact_pii),
            span_prefix=overrides.get("span_prefix", self.span_prefix),
            chain_timeout=overrides.get("chain_timeout", self.chain_timeout),
            llm_timeout=overrides.get("llm_timeout", self.llm_timeout),
            tool_timeout=overrides.get("tool_timeout", self.tool_timeout),
            max_retries=overrides.get("max_retries", self.max_retries),
            retry_delay=overrides.get("retry_delay", self.retry_delay),
            retry_on_errors=overrides.get("retry_on_errors", self.retry_on_errors),
            default_tags=overrides.get("default_tags", self.default_tags),
            default_metadata=overrides.get("default_metadata", self.default_metadata),
        )
