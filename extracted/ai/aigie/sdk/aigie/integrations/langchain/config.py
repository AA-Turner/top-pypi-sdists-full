"""Configuration for LangChain tracing.

Mirrors :class:`~aigie.integrations.langgraph.config.LangGraphConfig` in shape
so the two integrations stay documentation-consistent. Reads
``AIGIE_LANGCHAIN_*`` environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from aigie.tracing.config_base import FrameworkConfigBase


@dataclass
class LangChainConfig(FrameworkConfigBase):
    """Configuration for LangChain tracing behavior.

    Inherits ``zero_retention: bool`` from :class:`FrameworkConfigBase`. When
    True, no spans or traces are emitted for invocations driven through this
    config — Aigie still runs in-process but persistence is suppressed.
    """

    # Tracing toggles
    trace_chains: bool = True
    trace_llm_calls: bool = True
    trace_tool_calls: bool = True
    trace_retrievers: bool = True

    # Data capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    max_content_length: int = 2000

    # Privacy
    mask_sensitive_data: bool = False
    redact_pii: bool = False

    # Span naming
    span_prefix: str = "langchain"

    # Timeout settings (in seconds)
    chain_timeout: float = 600.0
    llm_timeout: float = 120.0

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_on_errors: list[str] = field(default_factory=list)

    # Remediation settings
    enable_realtime_remediation: bool = False
    remediation_mode: str = "recommendation"  # "recommendation" or "autonomous"
    remediation_query_timeout: float = 2.0

    # Metadata
    default_tags: dict[str, str] = field(default_factory=dict)
    default_metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration."""
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.chain_timeout <= 0:
            raise ValueError("chain_timeout must be positive")
        if self.llm_timeout <= 0:
            raise ValueError("llm_timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
        if self.remediation_mode not in ("recommendation", "autonomous"):
            raise ValueError("remediation_mode must be 'recommendation' or 'autonomous'")
        if self.remediation_query_timeout <= 0:
            raise ValueError("remediation_query_timeout must be positive")

    @classmethod
    def from_env(cls) -> LangChainConfig:
        """Create configuration from ``AIGIE_LANGCHAIN_*`` environment variables."""
        return cls(
            zero_retention=os.getenv("AIGIE_LANGCHAIN_ZERO_RETENTION", "false").lower() == "true",
            trace_chains=os.getenv("AIGIE_LANGCHAIN_TRACE_CHAINS", "true").lower() == "true",
            trace_llm_calls=os.getenv("AIGIE_LANGCHAIN_TRACE_LLM", "true").lower() == "true",
            trace_tool_calls=os.getenv("AIGIE_LANGCHAIN_TRACE_TOOLS", "true").lower() == "true",
            trace_retrievers=os.getenv("AIGIE_LANGCHAIN_TRACE_RETRIEVERS", "true").lower()
            == "true",
            capture_inputs=os.getenv("AIGIE_LANGCHAIN_CAPTURE_INPUTS", "true").lower() == "true",
            capture_outputs=os.getenv("AIGIE_LANGCHAIN_CAPTURE_OUTPUTS", "true").lower() == "true",
            max_content_length=int(os.getenv("AIGIE_LANGCHAIN_MAX_CONTENT_LENGTH", "2000")),
            mask_sensitive_data=os.getenv("AIGIE_LANGCHAIN_MASK_SENSITIVE", "false").lower()
            == "true",
            redact_pii=os.getenv("AIGIE_LANGCHAIN_REDACT_PII", "false").lower() == "true",
            chain_timeout=float(os.getenv("AIGIE_LANGCHAIN_CHAIN_TIMEOUT", "600.0")),
            llm_timeout=float(os.getenv("AIGIE_LANGCHAIN_LLM_TIMEOUT", "120.0")),
            max_retries=int(os.getenv("AIGIE_LANGCHAIN_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AIGIE_LANGCHAIN_RETRY_DELAY", "1.0")),
            enable_realtime_remediation=os.getenv(
                "AIGIE_LANGCHAIN_REALTIME_REMEDIATION", "false"
            ).lower()
            == "true",
            remediation_mode=os.getenv("AIGIE_LANGCHAIN_REMEDIATION_MODE", "recommendation"),
            remediation_query_timeout=float(
                os.getenv("AIGIE_LANGCHAIN_REMEDIATION_TIMEOUT", "2.0")
            ),
        )

    def merge(self, **overrides: Any) -> LangChainConfig:
        """Create a new config with overridden values."""
        return LangChainConfig(
            zero_retention=overrides.get("zero_retention", self.zero_retention),
            trace_chains=overrides.get("trace_chains", self.trace_chains),
            trace_llm_calls=overrides.get("trace_llm_calls", self.trace_llm_calls),
            trace_tool_calls=overrides.get("trace_tool_calls", self.trace_tool_calls),
            trace_retrievers=overrides.get("trace_retrievers", self.trace_retrievers),
            capture_inputs=overrides.get("capture_inputs", self.capture_inputs),
            capture_outputs=overrides.get("capture_outputs", self.capture_outputs),
            max_content_length=overrides.get("max_content_length", self.max_content_length),
            mask_sensitive_data=overrides.get("mask_sensitive_data", self.mask_sensitive_data),
            redact_pii=overrides.get("redact_pii", self.redact_pii),
            span_prefix=overrides.get("span_prefix", self.span_prefix),
            chain_timeout=overrides.get("chain_timeout", self.chain_timeout),
            llm_timeout=overrides.get("llm_timeout", self.llm_timeout),
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
            default_tags=overrides.get("default_tags", self.default_tags),
            default_metadata=overrides.get("default_metadata", self.default_metadata),
        )
