"""
Aigie CrewAI Integration

Full workflow tracing for CrewAI multi-agent crews with the Aigie SDK.
Traces crew executions, agent steps, task completion, and delegations.

Usage (Auto-Instrumentation - Recommended):
    import aigie
    from aigie.integrations.crewai import patch_crewai

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Enable auto-instrumentation
    patch_crewai()

    # Now all CrewAI operations are automatically traced
    from crewai import Crew, Agent, Task

    researcher = Agent(role="Researcher", ...)
    writer = Agent(role="Writer", ...)
    task = Task(description="...", agent=researcher)
    crew = Crew(agents=[researcher, writer], tasks=[task])
    result = crew.kickoff()  # Automatically traced!

Usage (Manual Callback Handler):
    from aigie.integrations.crewai import CrewAIHandler

    # Create handler with trace context
    async with aigie.trace("Research Crew") as trace:
        handler = CrewAIHandler(trace_name="Research Project")
        handler.set_trace_context(trace)

        await handler.handle_crew_start(
            crew_name="Research Crew",
            agents=[...],
            tasks=[...]
        )

        # ... run crew operations ...

        await handler.handle_crew_end(success=True, result=result)

Usage (Configuration):
    from aigie.integrations.crewai import CrewAIConfig, patch_crewai

    # Custom configuration
    config = CrewAIConfig(
        trace_crews=True,
        trace_agents=True,
        trace_tasks=True,
        crew_timeout=3600.0,  # 1 hour timeout
        max_retries=5,
    )

    # Apply configuration (config is used by handlers)
    patch_crewai()
"""

__all__ = [
    # Handler
    "CrewAIHandler",
    # Configuration
    "CrewAIConfig",
    # Cost tracking
    "CREWAI_MODEL_PRICING",
    "get_crewai_cost",
    "extract_tokens_from_response",
    "extract_model_from_agent",
    "aggregate_crew_costs",
    # Auto-instrumentation
    "patch_crewai",
    "unpatch_crewai",
    "is_crewai_patched",
    # Utilities
    "is_crewai_available",
    "get_crewai_version",
    "safe_str",
    "extract_agent_info",
    "extract_task_info",
    "extract_crew_info",
    "format_step_output",
    "get_execution_path",
    "mask_sensitive_content",
    # Retry/Timeout utilities
    "RetryExhaustedError",
    "TimeoutExceededError",
    "CrewExecutionError",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_decorator",
    "RetryContext",
    "CrewRetryContext",
]

from typing import TYPE_CHECKING, Any


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "CrewAIHandler":
        from .handler import CrewAIHandler

        return CrewAIHandler

    # Configuration
    if name == "CrewAIConfig":
        from .config import CrewAIConfig

        return CrewAIConfig

    # Cost tracking
    if name == "CREWAI_MODEL_PRICING":
        from .cost_tracking import CREWAI_MODEL_PRICING

        return CREWAI_MODEL_PRICING

    if name == "get_crewai_cost":
        from .cost_tracking import get_crewai_cost

        return get_crewai_cost

    if name == "extract_tokens_from_response":
        from .cost_tracking import extract_tokens_from_response

        return extract_tokens_from_response

    if name == "extract_model_from_agent":
        from .cost_tracking import extract_model_from_agent

        return extract_model_from_agent

    if name == "aggregate_crew_costs":
        from .cost_tracking import aggregate_crew_costs

        return aggregate_crew_costs

    # Auto-instrumentation
    if name == "patch_crewai":
        from .auto_instrument import patch_crewai

        return patch_crewai

    if name == "unpatch_crewai":
        from .auto_instrument import unpatch_crewai

        return unpatch_crewai

    if name == "is_crewai_patched":
        from .auto_instrument import is_crewai_patched

        return is_crewai_patched

    # Utilities
    if name == "is_crewai_available":
        from .utils import is_crewai_available

        return is_crewai_available

    if name == "get_crewai_version":
        from .utils import get_crewai_version

        return get_crewai_version

    if name == "safe_str":
        from .utils import safe_str

        return safe_str

    if name == "extract_agent_info":
        from .utils import extract_agent_info

        return extract_agent_info

    if name == "extract_task_info":
        from .utils import extract_task_info

        return extract_task_info

    if name == "extract_crew_info":
        from .utils import extract_crew_info

        return extract_crew_info

    if name == "format_step_output":
        from .utils import format_step_output

        return format_step_output

    if name == "get_execution_path":
        from .utils import get_execution_path

        return get_execution_path

    if name == "mask_sensitive_content":
        from .utils import mask_sensitive_content

        return mask_sensitive_content

    # Retry/Timeout utilities
    if name == "RetryExhaustedError":
        from ..._legacy_stubs import RetryExhaustedError

        return RetryExhaustedError

    if name == "TimeoutExceededError":
        from ..._legacy_stubs import TimeoutExceededError

        return TimeoutExceededError

    if name == "CrewExecutionError":
        from ..._legacy_stubs import CrewExecutionError

        return CrewExecutionError

    if name == "with_timeout":
        from ..._legacy_stubs import with_timeout

        return with_timeout

    if name == "with_retry":
        from ..._legacy_stubs import with_retry

        return with_retry

    if name == "with_timeout_and_retry":
        from ..._legacy_stubs import with_timeout_and_retry

        return with_timeout_and_retry

    if name == "retry_decorator":
        from ..._legacy_stubs import retry_decorator

        return retry_decorator

    if name == "RetryContext":
        from ..._legacy_stubs import RetryContext

        return RetryContext

    if name == "CrewRetryContext":
        from ..._legacy_stubs import CrewRetryContext

        return CrewRetryContext

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_crewai_patched,
        patch_crewai,
        unpatch_crewai,
    )
    from .config import CrewAIConfig
    from .cost_tracking import (
        CREWAI_MODEL_PRICING,
        aggregate_crew_costs,
        extract_model_from_agent,
        extract_tokens_from_response,
        get_crewai_cost,
    )
    from .handler import CrewAIHandler
    from ..._legacy_stubs import (
        CrewExecutionError,
        CrewRetryContext,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from .utils import (
        extract_agent_info,
        extract_crew_info,
        extract_task_info,
        format_step_output,
        get_crewai_version,
        get_execution_path,
        is_crewai_available,
        mask_sensitive_content,
        safe_str,
    )
