"""
Configuration for CrewAI tracing.
"""

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CrewAIConfig:
    """Configuration for CrewAI tracing behavior.

    Attributes:
        trace_crews: Whether to trace crew executions
        trace_agents: Whether to trace individual agent executions
        trace_tasks: Whether to trace task executions
        trace_llm_calls: Whether to trace LLM calls within agents
        trace_tool_calls: Whether to trace tool invocations
        trace_delegations: Whether to trace agent delegations
        capture_inputs: Whether to capture input data
        capture_outputs: Whether to capture output data
        capture_agent_thoughts: Whether to capture agent reasoning
        capture_tool_results: Whether to capture tool results
        max_content_length: Maximum content length to capture
        mask_sensitive_data: Whether to mask potentially sensitive data
        crew_timeout: Timeout in seconds for entire crew execution
        task_timeout: Timeout in seconds for individual tasks
        llm_timeout: Timeout in seconds for LLM calls
        max_retries: Maximum number of retries for failed operations
        retry_delay: Initial delay between retries in seconds (exponential backoff)
        retry_on_errors: List of error types to retry on (empty = retry all transient)
    """

    # Tracing toggles
    trace_crews: bool = True
    trace_agents: bool = True
    trace_tasks: bool = True
    trace_llm_calls: bool = True
    trace_tool_calls: bool = True
    trace_delegations: bool = True

    # Data capture settings
    capture_inputs: bool = True
    capture_outputs: bool = True
    capture_agent_thoughts: bool = True
    capture_tool_results: bool = True
    max_content_length: int = 2000

    # Privacy
    mask_sensitive_data: bool = False

    # Span naming
    span_prefix: str = "crewai"

    # Timeout settings (in seconds)
    crew_timeout: float = 1800.0  # 30 minutes for full crew
    task_timeout: float = 600.0  # 10 minutes per task
    llm_timeout: float = 120.0  # 2 minutes for LLM calls

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0  # Initial delay, doubles each retry
    retry_on_errors: list[str] = field(default_factory=list)  # Empty = retry all transient

    # Metadata
    default_tags: dict[str, str] = field(default_factory=dict)
    default_metadata: dict[str, Any] = field(default_factory=dict)

    # Real-time remediation settings
    enable_realtime_remediation: bool = False
    remediation_mode: str = "recommendation"  # "recommendation" or "autonomous"
    remediation_query_timeout: float = 2.0  # Max seconds to query platform for pattern

    def __post_init__(self):
        """Validate configuration."""
        if self.max_content_length < 100:
            raise ValueError("max_content_length must be at least 100")
        if self.crew_timeout <= 0:
            raise ValueError("crew_timeout must be positive")
        if self.task_timeout <= 0:
            raise ValueError("task_timeout must be positive")
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
    def from_env(cls) -> "CrewAIConfig":
        """Create configuration from environment variables.

        Environment variables:
            AIGIE_CREWAI_TRACE_CREWS: Trace crew executions (default: true)
            AIGIE_CREWAI_TRACE_AGENTS: Trace agent executions (default: true)
            AIGIE_CREWAI_TRACE_TASKS: Trace task executions (default: true)
            AIGIE_CREWAI_TRACE_LLM_CALLS: Trace LLM calls (default: true)
            AIGIE_CREWAI_TRACE_TOOL_CALLS: Trace tool calls (default: true)
            AIGIE_CREWAI_TRACE_DELEGATIONS: Trace delegations (default: true)
            AIGIE_CREWAI_CAPTURE_INPUTS: Capture inputs (default: true)
            AIGIE_CREWAI_CAPTURE_OUTPUTS: Capture outputs (default: true)
            AIGIE_CREWAI_CAPTURE_AGENT_THOUGHTS: Capture agent thoughts (default: true)
            AIGIE_CREWAI_CAPTURE_TOOL_RESULTS: Capture tool results (default: true)
            AIGIE_CREWAI_MAX_CONTENT_LENGTH: Max content length (default: 2000)
            AIGIE_CREWAI_MASK_SENSITIVE_DATA: Mask sensitive data (default: false)
            AIGIE_CREWAI_CREW_TIMEOUT: Crew timeout (default: 1800)
            AIGIE_CREWAI_TASK_TIMEOUT: Task timeout (default: 600)
            AIGIE_CREWAI_LLM_TIMEOUT: LLM timeout (default: 120)
            AIGIE_CREWAI_MAX_RETRIES: Max retries (default: 3)
            AIGIE_CREWAI_RETRY_DELAY: Retry delay (default: 1.0)
            AIGIE_CREWAI_REALTIME_REMEDIATION: Enable remediation (default: false)
            AIGIE_CREWAI_REMEDIATION_MODE: Mode (default: recommendation)
            AIGIE_CREWAI_REMEDIATION_TIMEOUT: Timeout (default: 2.0)
        """
        return cls(
            trace_crews=os.getenv("AIGIE_CREWAI_TRACE_CREWS", "true").lower() == "true",
            trace_agents=os.getenv("AIGIE_CREWAI_TRACE_AGENTS", "true").lower() == "true",
            trace_tasks=os.getenv("AIGIE_CREWAI_TRACE_TASKS", "true").lower() == "true",
            trace_llm_calls=os.getenv("AIGIE_CREWAI_TRACE_LLM_CALLS", "true").lower() == "true",
            trace_tool_calls=os.getenv("AIGIE_CREWAI_TRACE_TOOL_CALLS", "true").lower() == "true",
            trace_delegations=os.getenv("AIGIE_CREWAI_TRACE_DELEGATIONS", "true").lower() == "true",
            capture_inputs=os.getenv("AIGIE_CREWAI_CAPTURE_INPUTS", "true").lower() == "true",
            capture_outputs=os.getenv("AIGIE_CREWAI_CAPTURE_OUTPUTS", "true").lower() == "true",
            capture_agent_thoughts=os.getenv("AIGIE_CREWAI_CAPTURE_AGENT_THOUGHTS", "true").lower()
            == "true",
            capture_tool_results=os.getenv("AIGIE_CREWAI_CAPTURE_TOOL_RESULTS", "true").lower()
            == "true",
            max_content_length=int(os.getenv("AIGIE_CREWAI_MAX_CONTENT_LENGTH", "2000")),
            mask_sensitive_data=os.getenv("AIGIE_CREWAI_MASK_SENSITIVE_DATA", "false").lower()
            == "true",
            crew_timeout=float(os.getenv("AIGIE_CREWAI_CREW_TIMEOUT", "1800.0")),
            task_timeout=float(os.getenv("AIGIE_CREWAI_TASK_TIMEOUT", "600.0")),
            llm_timeout=float(os.getenv("AIGIE_CREWAI_LLM_TIMEOUT", "120.0")),
            max_retries=int(os.getenv("AIGIE_CREWAI_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AIGIE_CREWAI_RETRY_DELAY", "1.0")),
            enable_realtime_remediation=os.getenv(
                "AIGIE_CREWAI_REALTIME_REMEDIATION", "false"
            ).lower()
            == "true",
            remediation_mode=os.getenv("AIGIE_CREWAI_REMEDIATION_MODE", "recommendation"),
            remediation_query_timeout=float(os.getenv("AIGIE_CREWAI_REMEDIATION_TIMEOUT", "2.0")),
        )

    def merge(self, **overrides) -> "CrewAIConfig":
        """Create a new config with overridden values."""
        return CrewAIConfig(
            trace_crews=overrides.get("trace_crews", self.trace_crews),
            trace_agents=overrides.get("trace_agents", self.trace_agents),
            trace_tasks=overrides.get("trace_tasks", self.trace_tasks),
            trace_llm_calls=overrides.get("trace_llm_calls", self.trace_llm_calls),
            trace_tool_calls=overrides.get("trace_tool_calls", self.trace_tool_calls),
            trace_delegations=overrides.get("trace_delegations", self.trace_delegations),
            capture_inputs=overrides.get("capture_inputs", self.capture_inputs),
            capture_outputs=overrides.get("capture_outputs", self.capture_outputs),
            capture_agent_thoughts=overrides.get(
                "capture_agent_thoughts", self.capture_agent_thoughts
            ),
            capture_tool_results=overrides.get("capture_tool_results", self.capture_tool_results),
            max_content_length=overrides.get("max_content_length", self.max_content_length),
            mask_sensitive_data=overrides.get("mask_sensitive_data", self.mask_sensitive_data),
            span_prefix=overrides.get("span_prefix", self.span_prefix),
            crew_timeout=overrides.get("crew_timeout", self.crew_timeout),
            task_timeout=overrides.get("task_timeout", self.task_timeout),
            llm_timeout=overrides.get("llm_timeout", self.llm_timeout),
            max_retries=overrides.get("max_retries", self.max_retries),
            retry_delay=overrides.get("retry_delay", self.retry_delay),
            retry_on_errors=overrides.get("retry_on_errors", self.retry_on_errors),
            default_tags=overrides.get("default_tags", self.default_tags),
            default_metadata=overrides.get("default_metadata", self.default_metadata),
            enable_realtime_remediation=overrides.get(
                "enable_realtime_remediation", self.enable_realtime_remediation
            ),
            remediation_mode=overrides.get("remediation_mode", self.remediation_mode),
            remediation_query_timeout=overrides.get(
                "remediation_query_timeout", self.remediation_query_timeout
            ),
        )
