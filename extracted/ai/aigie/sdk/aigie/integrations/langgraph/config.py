"""
Configuration for LangGraph tracing.
"""

import os
from dataclasses import dataclass, field
from typing import Any

from aigie.tracing.config_base import FrameworkConfigBase


@dataclass
class LangGraphConfig(FrameworkConfigBase):
    """Configuration for LangGraph tracing behavior.

    Inherits ``zero_retention: bool`` from FrameworkConfigBase. When True,
    no spans or traces are emitted for invocations driven through this
    config — Aigie still runs in-process but persistence is suppressed.

    Attributes:
        trace_graphs: Whether to trace graph executions
        trace_nodes: Whether to trace individual node executions
        trace_edges: Whether to trace edge decisions
        trace_llm_calls: Whether to trace LLM calls within nodes
        trace_tool_calls: Whether to trace tool invocations
        capture_inputs: Whether to capture input data
        capture_outputs: Whether to capture output data
        capture_state: Whether to capture state transitions
        max_content_length: Maximum content length to capture
        mask_sensitive_data: Whether to mask potentially sensitive data
        graph_timeout: Timeout in seconds for entire graph execution
        node_timeout: Timeout in seconds for individual nodes
        llm_timeout: Timeout in seconds for LLM calls
        max_retries: Maximum number of retries for failed operations
        retry_delay: Initial delay between retries in seconds (exponential backoff)
        retry_on_errors: List of error types to retry on (empty = retry all transient)
    """

    # Tracing toggles
    trace_graphs: bool = True
    trace_nodes: bool = True
    trace_edges: bool = True
    trace_llm_calls: bool = True
    trace_tool_calls: bool = True

    # Data capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_state: bool = True
    max_content_length: int = 2000

    # Privacy
    mask_sensitive_data: bool = False
    redact_pii: bool = False  # Whether to redact PII from traces

    # Span naming
    span_prefix: str = "langgraph"

    # Timeout settings (in seconds)
    graph_timeout: float = 600.0  # 10 minutes for full graph
    node_timeout: float = 120.0  # 2 minutes per node
    llm_timeout: float = 120.0  # 2 minutes for LLM calls

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0  # Initial delay, doubles each retry
    retry_on_errors: list[str] = field(default_factory=list)  # Empty = retry all transient

    # Agent plan capture
    capture_agent_plan: bool = True

    # Real-time remediation settings
    enable_realtime_remediation: bool = False
    remediation_mode: str = "recommendation"  # "recommendation" or "autonomous"
    remediation_query_timeout: float = 2.0  # Max seconds to query platform for pattern

    # Metadata
    default_tags: dict[str, str] = field(default_factory=dict)
    default_metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration."""
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.graph_timeout <= 0:
            raise ValueError("graph_timeout must be positive")
        if self.node_timeout <= 0:
            raise ValueError("node_timeout must be positive")
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
    def from_env(cls) -> "LangGraphConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            AIGIE_LANGGRAPH_TRACE_GRAPHS: Trace graph executions (default: true)
            AIGIE_LANGGRAPH_TRACE_NODES: Trace individual node executions (default: true)
            AIGIE_LANGGRAPH_TRACE_EDGES: Trace edge decisions (default: true)
            AIGIE_LANGGRAPH_TRACE_LLM: Trace LLM calls within nodes (default: true)
            AIGIE_LANGGRAPH_TRACE_TOOLS: Trace tool invocations (default: true)
            AIGIE_LANGGRAPH_CAPTURE_INPUTS: Capture input data (default: true)
            AIGIE_LANGGRAPH_CAPTURE_OUTPUTS: Capture output data (default: true)
            AIGIE_LANGGRAPH_CAPTURE_STATE: Capture state transitions (default: true)
            AIGIE_LANGGRAPH_MAX_CONTENT_LENGTH: Max content length (default: 2000)
            AIGIE_LANGGRAPH_MASK_SENSITIVE: Mask sensitive data (default: false)
            AIGIE_LANGGRAPH_GRAPH_TIMEOUT: Graph timeout in seconds (default: 600)
            AIGIE_LANGGRAPH_NODE_TIMEOUT: Node timeout in seconds (default: 120)
            AIGIE_LANGGRAPH_LLM_TIMEOUT: LLM timeout in seconds (default: 120)
            AIGIE_LANGGRAPH_MAX_RETRIES: Max retry attempts (default: 3)
            AIGIE_LANGGRAPH_RETRY_DELAY: Initial retry delay in seconds (default: 1.0)
            AIGIE_LANGGRAPH_CAPTURE_PLAN: Capture agent plan from first LLM response (default: true)
            AIGIE_LANGGRAPH_REALTIME_REMEDIATION: Enable real-time remediation (default: false)
            AIGIE_LANGGRAPH_REMEDIATION_MODE: Remediation mode - recommendation or autonomous (default: recommendation)
            AIGIE_LANGGRAPH_REMEDIATION_TIMEOUT: Max seconds to query platform (default: 2.0)
        """
        return cls(
            trace_graphs=os.getenv("AIGIE_LANGGRAPH_TRACE_GRAPHS", "true").lower() == "true",
            trace_nodes=os.getenv("AIGIE_LANGGRAPH_TRACE_NODES", "true").lower() == "true",
            trace_edges=os.getenv("AIGIE_LANGGRAPH_TRACE_EDGES", "true").lower() == "true",
            trace_llm_calls=os.getenv("AIGIE_LANGGRAPH_TRACE_LLM", "true").lower() == "true",
            trace_tool_calls=os.getenv("AIGIE_LANGGRAPH_TRACE_TOOLS", "true").lower() == "true",
            capture_inputs=os.getenv("AIGIE_LANGGRAPH_CAPTURE_INPUTS", "true").lower() == "true",
            capture_outputs=os.getenv("AIGIE_LANGGRAPH_CAPTURE_OUTPUTS", "true").lower() == "true",
            capture_state=os.getenv("AIGIE_LANGGRAPH_CAPTURE_STATE", "true").lower() == "true",
            max_content_length=int(os.getenv("AIGIE_LANGGRAPH_MAX_CONTENT_LENGTH", "2000")),
            mask_sensitive_data=os.getenv("AIGIE_LANGGRAPH_MASK_SENSITIVE", "false").lower()
            == "true",
            redact_pii=os.getenv("AIGIE_LANGGRAPH_REDACT_PII", "false").lower() == "true",
            graph_timeout=float(os.getenv("AIGIE_LANGGRAPH_GRAPH_TIMEOUT", "600.0")),
            node_timeout=float(os.getenv("AIGIE_LANGGRAPH_NODE_TIMEOUT", "120.0")),
            llm_timeout=float(os.getenv("AIGIE_LANGGRAPH_LLM_TIMEOUT", "120.0")),
            max_retries=int(os.getenv("AIGIE_LANGGRAPH_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AIGIE_LANGGRAPH_RETRY_DELAY", "1.0")),
            capture_agent_plan=os.getenv("AIGIE_LANGGRAPH_CAPTURE_PLAN", "true").lower() == "true",
            enable_realtime_remediation=os.getenv(
                "AIGIE_LANGGRAPH_REALTIME_REMEDIATION", "false"
            ).lower()
            == "true",
            remediation_mode=os.getenv("AIGIE_LANGGRAPH_REMEDIATION_MODE", "recommendation"),
            remediation_query_timeout=float(
                os.getenv("AIGIE_LANGGRAPH_REMEDIATION_TIMEOUT", "2.0")
            ),
        )

    def merge(self, **overrides) -> "LangGraphConfig":
        """
        Create a new config with overridden values.

        Args:
            **overrides: Values to override

        Returns:
            New LangGraphConfig with overrides applied
        """
        return LangGraphConfig(
            zero_retention=overrides.get("zero_retention", self.zero_retention),
            trace_graphs=overrides.get("trace_graphs", self.trace_graphs),
            trace_nodes=overrides.get("trace_nodes", self.trace_nodes),
            trace_edges=overrides.get("trace_edges", self.trace_edges),
            trace_llm_calls=overrides.get("trace_llm_calls", self.trace_llm_calls),
            trace_tool_calls=overrides.get("trace_tool_calls", self.trace_tool_calls),
            capture_inputs=overrides.get("capture_inputs", self.capture_inputs),
            capture_outputs=overrides.get("capture_outputs", self.capture_outputs),
            capture_state=overrides.get("capture_state", self.capture_state),
            max_content_length=overrides.get("max_content_length", self.max_content_length),
            mask_sensitive_data=overrides.get("mask_sensitive_data", self.mask_sensitive_data),
            redact_pii=overrides.get("redact_pii", self.redact_pii),
            span_prefix=overrides.get("span_prefix", self.span_prefix),
            graph_timeout=overrides.get("graph_timeout", self.graph_timeout),
            node_timeout=overrides.get("node_timeout", self.node_timeout),
            llm_timeout=overrides.get("llm_timeout", self.llm_timeout),
            max_retries=overrides.get("max_retries", self.max_retries),
            retry_delay=overrides.get("retry_delay", self.retry_delay),
            retry_on_errors=overrides.get("retry_on_errors", self.retry_on_errors),
            default_tags=overrides.get("default_tags", self.default_tags),
            default_metadata=overrides.get("default_metadata", self.default_metadata),
            capture_agent_plan=overrides.get("capture_agent_plan", self.capture_agent_plan),
            enable_realtime_remediation=overrides.get(
                "enable_realtime_remediation", self.enable_realtime_remediation
            ),
            remediation_mode=overrides.get("remediation_mode", self.remediation_mode),
            remediation_query_timeout=overrides.get(
                "remediation_query_timeout", self.remediation_query_timeout
            ),
        )
