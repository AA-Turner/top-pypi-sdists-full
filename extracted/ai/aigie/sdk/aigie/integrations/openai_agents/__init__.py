"""
Aigie OpenAI Agents SDK Integration

Full workflow tracing for OpenAI Agents SDK applications with the Aigie SDK.
Traces agent runs, LLM generations, tool calls, handoffs, and guardrails.

Usage (Tracing Processor - Recommended):
    import aigie
    from aigie.integrations.openai_agents import AigieTracingProcessor

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Add Aigie tracing processor (additive to existing tracing)
    from agents import add_trace_processor
    processor = AigieTracingProcessor()
    add_trace_processor(processor)

    # Now all agent operations are automatically traced
    from agents import Agent, Runner

    agent = Agent(name="assistant", model="gpt-4o")
    result = await Runner.run(agent, "Hello!")  # Automatically traced!

Usage (Auto-Instrumentation):
    from aigie.integrations.openai_agents import patch_openai_agents

    # Enable auto-instrumentation
    patch_openai_agents()

    # All agent operations are now traced

Usage (Manual Handler):
    from aigie.integrations.openai_agents import OpenAIAgentsHandler

    # Create handler with trace context
    async with aigie.trace("Agent Workflow") as trace:
        handler = OpenAIAgentsHandler(trace_name="Agent Run")
        handler.set_trace_context(trace)

        workflow_id = await handler.handle_workflow_start("main")
        agent_id = await handler.handle_agent_start("assistant", model="gpt-4o")

        # ... run agent operations ...

        await handler.handle_agent_end(agent_id, output="Response")
        await handler.handle_workflow_end(workflow_id)

Usage (Configuration):
    from aigie.integrations.openai_agents import OpenAIAgentsConfig

    config = OpenAIAgentsConfig(
        trace_agents=True,
        trace_generations=True,
        trace_tool_calls=True,
        trace_handoffs=True,
        trace_guardrails=True,
        capture_inputs=True,
        capture_outputs=True,
    )
"""

__all__ = [
    # Tracing Processor (primary integration)
    "AigieTracingProcessor",
    # Handler
    "OpenAIAgentsHandler",
    # Configuration
    "OpenAIAgentsConfig",
    # Cost tracking
    "OPENAI_AGENTS_MODEL_PRICING",
    "get_openai_agents_cost",
    "extract_tokens_from_response",
    "aggregate_workflow_costs",
    "estimate_tool_cost",
    # Auto-instrumentation
    "patch_openai_agents",
    "unpatch_openai_agents",
    "is_openai_agents_patched",
    # Utilities
    "is_openai_agents_available",
    "get_openai_agents_version",
    "safe_str",
    "extract_agent_info",
    "extract_tool_info",
    "extract_handoff_info",
    "extract_guardrail_info",
    "format_messages",
    "extract_workflow_summary",
    "mask_sensitive_content",
    # Retry/Timeout utilities
    "AgentExecutionError",
    "RetryExhaustedError",
    "TimeoutExceededError",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_decorator",
    "RetryContext",
    "WorkflowRetryContext",
]

from typing import TYPE_CHECKING, Any


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Tracing Processor
    if name == "AigieTracingProcessor":
        from .processor import AigieTracingProcessor

        return AigieTracingProcessor

    # Handler
    if name == "OpenAIAgentsHandler":
        from .handler import OpenAIAgentsHandler

        return OpenAIAgentsHandler

    # Configuration
    if name == "OpenAIAgentsConfig":
        from .config import OpenAIAgentsConfig

        return OpenAIAgentsConfig

    # Cost tracking
    if name == "OPENAI_AGENTS_MODEL_PRICING":
        from .cost_tracking import OPENAI_AGENTS_MODEL_PRICING

        return OPENAI_AGENTS_MODEL_PRICING

    if name == "get_openai_agents_cost":
        from .cost_tracking import get_openai_agents_cost

        return get_openai_agents_cost

    if name == "extract_tokens_from_response":
        from .cost_tracking import extract_tokens_from_response

        return extract_tokens_from_response

    if name == "aggregate_workflow_costs":
        from .cost_tracking import aggregate_workflow_costs

        return aggregate_workflow_costs

    if name == "estimate_tool_cost":
        from .cost_tracking import estimate_tool_cost

        return estimate_tool_cost

    # Auto-instrumentation
    if name == "patch_openai_agents":
        from .auto_instrument import patch_openai_agents

        return patch_openai_agents

    if name == "unpatch_openai_agents":
        from .auto_instrument import unpatch_openai_agents

        return unpatch_openai_agents

    if name == "is_openai_agents_patched":
        from .auto_instrument import is_openai_agents_patched

        return is_openai_agents_patched

    # Utilities
    if name == "is_openai_agents_available":
        from .utils import is_openai_agents_available

        return is_openai_agents_available

    if name == "get_openai_agents_version":
        from .utils import get_openai_agents_version

        return get_openai_agents_version

    if name == "safe_str":
        from .utils import safe_str

        return safe_str

    if name == "extract_agent_info":
        from .utils import extract_agent_info

        return extract_agent_info

    if name == "extract_tool_info":
        from .utils import extract_tool_info

        return extract_tool_info

    if name == "extract_handoff_info":
        from .utils import extract_handoff_info

        return extract_handoff_info

    if name == "extract_guardrail_info":
        from .utils import extract_guardrail_info

        return extract_guardrail_info

    if name == "format_messages":
        from .utils import format_messages

        return format_messages

    if name == "extract_workflow_summary":
        from .utils import extract_workflow_summary

        return extract_workflow_summary

    if name == "mask_sensitive_content":
        from .utils import mask_sensitive_content

        return mask_sensitive_content

    # Retry/Timeout utilities
    if name == "AgentExecutionError":
        from ..._legacy_stubs import AgentExecutionError

        return AgentExecutionError

    if name == "RetryExhaustedError":
        from ..._legacy_stubs import RetryExhaustedError

        return RetryExhaustedError

    if name == "TimeoutExceededError":
        from ..._legacy_stubs import TimeoutExceededError

        return TimeoutExceededError

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

    if name == "WorkflowRetryContext":
        from ..._legacy_stubs import WorkflowRetryContext

        return WorkflowRetryContext

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_openai_agents_patched,
        patch_openai_agents,
        unpatch_openai_agents,
    )
    from .config import OpenAIAgentsConfig
    from .cost_tracking import (
        OPENAI_AGENTS_MODEL_PRICING,
        aggregate_workflow_costs,
        estimate_tool_cost,
        extract_tokens_from_response,
        get_openai_agents_cost,
    )
    from .handler import OpenAIAgentsHandler
    from .processor import AigieTracingProcessor
    from ..._legacy_stubs import (
        AgentExecutionError,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        WorkflowRetryContext,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from .utils import (
        extract_agent_info,
        extract_guardrail_info,
        extract_handoff_info,
        extract_tool_info,
        extract_workflow_summary,
        format_messages,
        get_openai_agents_version,
        is_openai_agents_available,
        mask_sensitive_content,
        safe_str,
    )
