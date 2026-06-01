"""
Traced LLM wrapper for browser-use.

Wraps browser-use LLM classes to add Aigie tracing for all LLM calls.
"""

import functools
import logging
import time
from typing import Any, TypeVar

from ..._legacy_stubs import (  # legacy autonomous-mode shim
    RetryExhaustedError,
    TimeoutExceededError,
    with_timeout_and_retry,
)
from .config import BrowserUseConfig
from .cost_tracking import extract_tokens_from_response, get_browser_use_cost
from .utils import safe_str


# No-op stubs (autonomous retry/timeout removed)
class RetryExhaustedError(Exception):
    def __init__(self, *a: Any, attempts: int = 0, last_error: Exception | None = None, **kw: Any) -> None:
        super().__init__(*a)
        self.attempts = attempts
        self.last_error = last_error


class TimeoutExceededError(Exception):
    def __init__(self, *a: Any, timeout: float = 0.0, **kw: Any) -> None:
        super().__init__(*a)
        self.timeout = timeout


async def with_timeout_and_retry(fn: Any, *args: Any, **kwargs: Any) -> Any:
    """No-op timeout+retry — just invokes the callable."""
    import inspect
    for k in ("timeout", "max_retries", "retry_delay", "retry_on", "operation_name", "max_attempts", "backoff_factor"):
        kwargs.pop(k, None)
    result = fn(*args, **kwargs) if callable(fn) else fn
    if inspect.isawaitable(result):
        return await result
    return result


logger = logging.getLogger(__name__)

T = TypeVar("T")


class TracedLLM:
    """Wrapper that adds Aigie tracing to any browser-use LLM.

    This wrapper implements the browser-use BaseChatModel protocol and
    intercepts all LLM calls to add tracing.

    Usage:
        from browser_use import ChatBrowserUse
        from aigie.integrations.browser_use import TracedLLM

        llm = ChatBrowserUse()
        traced_llm = TracedLLM(llm, aigie_client)

        # Use traced_llm instead of llm
        agent = Agent(task="...", llm=traced_llm)
    """

    def __init__(
        self,
        llm: Any,
        aigie: Any | None = None,
        config: BrowserUseConfig | None = None,
        span_name: str = "browser_use.llm",
        capture_input: bool = True,
        capture_output: bool = True,
        model_name: str | None = None,
    ):
        """Initialize the traced LLM wrapper.

        Args:
            llm: The browser-use LLM instance to wrap
            aigie: Optional Aigie client instance. If None, uses global client.
            config: Configuration for timeout/retry behavior
            span_name: Name for the LLM span
            capture_input: Whether to capture input messages
            capture_output: Whether to capture output
            model_name: Override model name (auto-detected if not provided)
        """
        self._llm = llm
        self._aigie = aigie
        self._config = config or BrowserUseConfig()
        self._span_name = span_name
        self._capture_input = capture_input
        self._capture_output = capture_output
        self._model_name = model_name or self._detect_model_name()
        self._call_count = 0
        self._retry_count = 0

    def _detect_model_name(self) -> str:
        """Auto-detect the model name from the wrapped LLM."""
        # Try common attribute names
        for attr in ["model", "model_name", "model_id", "_model"]:
            if hasattr(self._llm, attr):
                value = getattr(self._llm, attr)
                if value and isinstance(value, str):
                    return value

        # Check class name for hints
        class_name = type(self._llm).__name__.lower()
        if "browseruse" in class_name or "chatbrowseruse" in class_name:
            return "chat-browser-use"

        return "unknown"

    def _get_aigie(self) -> Any | None:
        """Get the Aigie client instance."""
        if self._aigie:
            return self._aigie

        # Try to get global instance
        try:
            from aigie import get_aigie

            return get_aigie()
        except (ImportError, Exception):
            return None

    def _get_current_span(self) -> Any | None:
        """Get the current span context if available."""
        try:
            from aigie.context_manager import get_current_span_context

            return get_current_span_context()
        except (ImportError, Exception):
            return None

    async def ainvoke(
        self,
        messages: Any,
        output_format: type[T] | None = None,
        **kwargs,
    ) -> str | T:
        """Invoke the LLM with tracing, timeout, and retry support.

        This is the main entry point for browser-use LLM calls.
        Matches the BaseChatModel protocol.

        Args:
            messages: Input messages
            output_format: Optional Pydantic model for structured output
            **kwargs: Additional arguments passed to the LLM

        Returns:
            String response or structured output matching output_format

        Raises:
            RetryExhaustedError: If all retry attempts are exhausted
            TimeoutExceededError: If the LLM call times out
        """
        self._call_count += 1
        call_id = self._call_count
        start_time = time.perf_counter()

        aigie = self._get_aigie()
        span = None
        result = None
        error = None
        retry_attempts = 0

        try:
            # Create span if aigie is available
            if aigie:
                try:
                    from aigie.context_manager import get_current_trace_context

                    trace_ctx = get_current_trace_context()
                    if trace_ctx:
                        span = await trace_ctx.span(
                            name=f"{self._span_name}.call_{call_id}",
                            run_type="llm",
                        ).__aenter__()

                        # Set span metadata
                        if span:
                            span.set_model(self._model_name)
                            if self._capture_input:
                                span.set_input(self._serialize_messages(messages))
                            if output_format:
                                span.set_metadata(
                                    {
                                        "output_format": output_format.__name__
                                        if hasattr(output_format, "__name__")
                                        else str(output_format)
                                    }
                                )
                except Exception:
                    pass  # Don't fail LLM call due to tracing issues

            # Make the actual LLM call with timeout and retry
            async def _do_llm_call():
                return await self._llm.ainvoke(messages, output_format, **kwargs)

            # Use timeout/retry if configured
            if self._config.max_retries > 0 or self._config.llm_timeout > 0:
                result = await with_timeout_and_retry(
                    _do_llm_call,
                    timeout=self._config.llm_timeout,
                    max_retries=self._config.max_retries,
                    retry_delay=self._config.retry_delay,
                    retry_on=self._config.retry_on_errors or None,
                    operation_name=f"llm.ainvoke[{self._model_name}]",
                )
            else:
                result = await _do_llm_call()

            return result

        except RetryExhaustedError as e:
            error = e
            retry_attempts = e.attempts
            self._retry_count += retry_attempts
            logger.error(f"LLM call failed after {retry_attempts} attempts: {e.last_error}")
            raise

        except TimeoutExceededError as e:
            error = e
            logger.error(f"LLM call timed out after {e.timeout}s")
            raise

        except Exception as e:
            error = e
            raise

        finally:
            # Calculate duration
            end_time = time.perf_counter()
            latency_seconds = end_time - start_time

            # Update span with results
            if span:
                try:
                    span.set_latency(latency_seconds)

                    # Add retry info to metadata
                    if retry_attempts > 0:
                        span.set_metadata(
                            {
                                "retry_attempts": retry_attempts,
                                "max_retries": self._config.max_retries,
                            }
                        )

                    if error:
                        span.set_error(str(error))
                        if isinstance(error, RetryExhaustedError):
                            span.set_metadata({"retry_exhausted": True})
                        elif isinstance(error, TimeoutExceededError):
                            span.set_metadata({"timed_out": True, "timeout": error.timeout})
                    elif result is not None and self._capture_output:
                        span.set_output(self._serialize_output(result))

                    # Extract and set token usage
                    tokens = extract_tokens_from_response(result) if result else None
                    if tokens:
                        span.set_tokens(
                            prompt_tokens=tokens["input_tokens"],
                            completion_tokens=tokens["output_tokens"],
                        )

                        # Calculate cost
                        cost = get_browser_use_cost(
                            model=self._model_name,
                            input_tokens=tokens["input_tokens"],
                            output_tokens=tokens["output_tokens"],
                        )
                        if cost:
                            span.set_cost(
                                input_cost=cost["input_cost"],
                                output_cost=cost["output_cost"],
                            )

                    await span.__aexit__(None, None, None)
                except Exception:
                    pass  # Don't fail due to span cleanup

    def _serialize_messages(self, messages: Any) -> Any:
        """Serialize messages for tracing."""
        if isinstance(messages, list):
            return [self._serialize_message(m) for m in messages]
        return self._serialize_message(messages)

    def _serialize_message(self, message: Any) -> Any:
        """Serialize a single message."""
        if isinstance(message, dict):
            return message
        if hasattr(message, "model_dump"):
            return message.model_dump()
        if hasattr(message, "dict"):
            return message.dict()
        if hasattr(message, "content"):
            return {
                "role": getattr(message, "role", "unknown"),
                "content": safe_str(message.content),
            }
        return safe_str(message)

    def _serialize_output(self, output: Any) -> Any:
        """Serialize output for tracing."""
        if isinstance(output, str):
            return output
        if hasattr(output, "model_dump"):
            return output.model_dump()
        if hasattr(output, "dict"):
            return output.dict()
        return safe_str(output)

    def __getattr__(self, name: str) -> Any:
        """Proxy all other attributes to the wrapped LLM."""
        return getattr(self._llm, name)

    def __repr__(self) -> str:
        return f"TracedLLM({self._llm!r}, model={self._model_name})"


def wrap_browser_use_llm(
    llm: Any,
    aigie: Any | None = None,
    span_name: str = "browser_use.llm",
    capture_input: bool = True,
    capture_output: bool = True,
) -> TracedLLM:
    """Convenience function to wrap a browser-use LLM with tracing.

    Args:
        llm: The browser-use LLM instance to wrap
        aigie: Optional Aigie client instance
        span_name: Name for the LLM span
        capture_input: Whether to capture input messages
        capture_output: Whether to capture output

    Returns:
        TracedLLM wrapper instance

    Example:
        from browser_use import ChatBrowserUse
        from aigie.integrations.browser_use import wrap_browser_use_llm

        llm = ChatBrowserUse()
        traced_llm = wrap_browser_use_llm(llm)
    """
    return TracedLLM(
        llm=llm,
        aigie=aigie,
        span_name=span_name,
        capture_input=capture_input,
        capture_output=capture_output,
    )


def patch_browser_use_llm_module() -> bool:
    """Patch browser-use LLM module for automatic instrumentation.

    This patches the BaseChatModel class to automatically add tracing
    to all LLM instances.

    Returns:
        True if patching was successful, False otherwise
    """
    try:
        from browser_use.llm import base

        original_ainvoke = base.BaseChatModel.ainvoke

        @functools.wraps(original_ainvoke)
        async def patched_ainvoke(self, messages, output_format=None, **kwargs):
            # Check if already wrapped
            if hasattr(self, "_aigie_traced"):
                return await original_ainvoke(self, messages, output_format, **kwargs)

            # Create temporary wrapper for this call
            wrapper = TracedLLM(self)
            wrapper._aigie_traced = True  # Mark to avoid double-wrapping
            return await wrapper.ainvoke(messages, output_format, **kwargs)

        base.BaseChatModel.ainvoke = patched_ainvoke
        return True

    except ImportError:
        return False
    except Exception:
        return False
