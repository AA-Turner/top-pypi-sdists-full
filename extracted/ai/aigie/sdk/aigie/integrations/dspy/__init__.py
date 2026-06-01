"""
Aigie DSPy Integration

Full workflow tracing for DSPy programs with the Aigie SDK.
Traces module executions, predictions, retrievals, and optimizations.

Usage (Auto-Instrumentation - Recommended):
    import aigie
    from aigie.integrations.dspy import patch_dspy

    # Initialize Aigie
    aigie_client = aigie.Aigie()
    await aigie_client.initialize()

    # Enable auto-instrumentation
    patch_dspy()

    # Now all DSPy operations are automatically traced
    import dspy

    dspy.configure(lm=dspy.LM("openai/gpt-4o"))

    class GenerateAnswer(dspy.Signature):
        question: str = dspy.InputField()
        answer: str = dspy.OutputField()

    predict = dspy.Predict(GenerateAnswer)
    result = predict(question="What is AI?")  # Automatically traced!

Usage (Manual Handler):
    from aigie.integrations.dspy import DSPyHandler

    # Create handler with trace context
    async with aigie.trace("DSPy Program") as trace:
        handler = DSPyHandler(trace_name="QA Program")
        handler.set_trace_context(trace)

        module_id = await handler.handle_module_start(
            module_name="GenerateAnswer",
            module_type="predict",
            signature="question -> answer",
        )

        # ... run module ...

        await handler.handle_module_end(module_id, output=result)

Usage (Configuration):
    from aigie.integrations.dspy import DSPyConfig

    config = DSPyConfig(
        trace_modules=True,
        trace_predictions=True,
        trace_optimizations=True,
        trace_retrievers=True,
        capture_inputs=True,
        capture_outputs=True,
    )
"""

__all__ = [
    # Handler
    "DSPyHandler",
    # Configuration
    "DSPyConfig",
    # Cost tracking
    "DSPY_MODEL_PRICING",
    "get_dspy_cost",
    "extract_tokens_from_lm_response",
    "aggregate_program_costs",
    "estimate_optimization_cost",
    # Auto-instrumentation
    "patch_dspy",
    "unpatch_dspy",
    "is_dspy_patched",
    # Utilities
    "is_dspy_available",
    "get_dspy_version",
    "safe_str",
    "extract_module_info",
    "extract_prediction_info",
    "extract_signature_info",
    "format_demonstrations",
    "get_lm_info",
    "extract_optimizer_info",
    "mask_sensitive_content",
    # Retry/Timeout utilities
    "DSPyExecutionError",
    "RetryExhaustedError",
    "TimeoutExceededError",
    "with_timeout",
    "with_retry",
    "with_timeout_and_retry",
    "retry_decorator",
    "RetryContext",
    "ProgramRetryContext",
    "OptimizationRetryContext",
]

from typing import TYPE_CHECKING, Any


def __getattr__(name: str) -> Any:
    """Lazy imports for performance."""

    # Handler
    if name == "DSPyHandler":
        from .handler import DSPyHandler

        return DSPyHandler

    # Configuration
    if name == "DSPyConfig":
        from .config import DSPyConfig

        return DSPyConfig

    # Cost tracking
    if name == "DSPY_MODEL_PRICING":
        from .cost_tracking import DSPY_MODEL_PRICING

        return DSPY_MODEL_PRICING

    if name == "get_dspy_cost":
        from .cost_tracking import get_dspy_cost

        return get_dspy_cost

    if name == "extract_tokens_from_lm_response":
        from .cost_tracking import extract_tokens_from_lm_response

        return extract_tokens_from_lm_response

    if name == "aggregate_program_costs":
        from .cost_tracking import aggregate_program_costs

        return aggregate_program_costs

    if name == "estimate_optimization_cost":
        from .cost_tracking import estimate_optimization_cost

        return estimate_optimization_cost

    # Auto-instrumentation
    if name == "patch_dspy":
        from .auto_instrument import patch_dspy

        return patch_dspy

    if name == "unpatch_dspy":
        from .auto_instrument import unpatch_dspy

        return unpatch_dspy

    if name == "is_dspy_patched":
        from .auto_instrument import is_dspy_patched

        return is_dspy_patched

    # Utilities
    if name == "is_dspy_available":
        from .utils import is_dspy_available

        return is_dspy_available

    if name == "get_dspy_version":
        from .utils import get_dspy_version

        return get_dspy_version

    if name == "safe_str":
        from .utils import safe_str

        return safe_str

    if name == "extract_module_info":
        from .utils import extract_module_info

        return extract_module_info

    if name == "extract_prediction_info":
        from .utils import extract_prediction_info

        return extract_prediction_info

    if name == "extract_signature_info":
        from .utils import extract_signature_info

        return extract_signature_info

    if name == "format_demonstrations":
        from .utils import format_demonstrations

        return format_demonstrations

    if name == "get_lm_info":
        from .utils import get_lm_info

        return get_lm_info

    if name == "extract_optimizer_info":
        from .utils import extract_optimizer_info

        return extract_optimizer_info

    if name == "mask_sensitive_content":
        from .utils import mask_sensitive_content

        return mask_sensitive_content

    # Retry/Timeout utilities
    if name == "DSPyExecutionError":
        from ..._legacy_stubs import DSPyExecutionError

        return DSPyExecutionError

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

    if name == "ProgramRetryContext":
        from ..._legacy_stubs import ProgramRetryContext

        return ProgramRetryContext

    if name == "OptimizationRetryContext":
        from ..._legacy_stubs import OptimizationRetryContext

        return OptimizationRetryContext

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


if TYPE_CHECKING:
    from .auto_instrument import (
        is_dspy_patched,
        patch_dspy,
        unpatch_dspy,
    )
    from .config import DSPyConfig
    from .cost_tracking import (
        DSPY_MODEL_PRICING,
        aggregate_program_costs,
        estimate_optimization_cost,
        extract_tokens_from_lm_response,
        get_dspy_cost,
    )
    from .handler import DSPyHandler
    from ..._legacy_stubs import (
        DSPyExecutionError,
        OptimizationRetryContext,
        ProgramRetryContext,
        RetryContext,
        RetryExhaustedError,
        TimeoutExceededError,
        retry_decorator,
        with_retry,
        with_timeout,
        with_timeout_and_retry,
    )
    from .utils import (
        extract_module_info,
        extract_optimizer_info,
        extract_prediction_info,
        extract_signature_info,
        format_demonstrations,
        get_dspy_version,
        get_lm_info,
        is_dspy_available,
        mask_sensitive_content,
        safe_str,
    )
