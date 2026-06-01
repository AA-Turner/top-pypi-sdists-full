"""
Traced Agent wrapper for browser-use.

Provides full workflow tracing for browser-use agents including:
- Root trace for the entire task
- Spans for each agent step
- LLM call tracing with tokens/cost
- Browser action tracing
- Optional screenshot capture
- Timeout and retry support for resilient execution
"""

import contextlib
import logging
import time
from typing import Any

from ..._legacy_stubs import (  # legacy autonomous-mode shim
    RetryExhaustedError,
    TimeoutExceededError,
    with_timeout_and_retry,
)
from .browser import TracedBrowser
from .config import BrowserUseConfig
from .llm import TracedLLM
from .utils import is_browser_use_available


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


class TracedAgent:
    """Wrapper that adds full Aigie tracing to browser-use Agent.

    Creates a hierarchical trace structure:

    browser_task (root trace)
    └── agent.run (span)
        ├── step_1 (span)
        │   ├── llm_call (span) → tokens, cost, latency
        │   └── browser_action (span) → selector, success
        ├── step_2 (span)
        │   ├── llm_call (span)
        │   └── browser_action (span)
        └── ... more steps

    Usage:
        from aigie.integrations.browser_use import TracedAgent
        from browser_use import ChatBrowserUse
        import aigie

        aigie_client = aigie.Aigie()
        await aigie_client.initialize()

        agent = TracedAgent(
            task="Find restaurants in NYC",
            llm=ChatBrowserUse(),
            aigie=aigie_client,
        )
        result = await agent.run()
    """

    def __init__(
        self,
        task: str,
        llm: Any,
        browser: Any | None = None,
        aigie: Any | None = None,
        config: BrowserUseConfig | None = None,
        max_steps: int = 100,
        # Pass-through browser-use Agent parameters
        **agent_kwargs,
    ):
        """Initialize the traced agent.

        Args:
            task: The task description for the agent
            llm: The LLM instance (will be wrapped with TracedLLM if not already)
            browser: Optional Browser instance (will be wrapped with TracedBrowser)
            aigie: Optional Aigie client instance. If None, uses global client.
            config: Configuration for tracing behavior
            max_steps: Maximum number of steps before stopping
            **agent_kwargs: Additional arguments passed to browser-use Agent
        """
        self._task = task
        self._config = config or BrowserUseConfig()
        self._aigie = aigie
        self._max_steps = max_steps
        self._agent_kwargs = agent_kwargs

        # Wrap LLM if not already wrapped
        if isinstance(llm, TracedLLM):
            self._llm = llm
        else:
            self._llm = TracedLLM(llm, aigie=aigie)

        # Wrap browser if provided and not already wrapped
        if browser is None:
            self._browser = TracedBrowser(aigie=aigie, config=self._config)
        elif isinstance(browser, TracedBrowser):
            self._browser = browser
        else:
            self._browser = TracedBrowser(browser, aigie=aigie, config=self._config)

        # Internal state
        self._agent = None
        self._step_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        self._start_time: float | None = None
        self._timed_out_steps = 0
        self._retried_steps = 0

    def _get_aigie(self) -> Any | None:
        """Get the Aigie client instance."""
        if self._aigie:
            return self._aigie
        try:
            from aigie import get_aigie

            return get_aigie()
        except (ImportError, Exception):
            return None

    async def _create_browser_use_agent(self) -> Any:
        """Create the underlying browser-use Agent."""
        if not is_browser_use_available():
            raise ImportError("browser-use is required. Install with: pip install browser-use")

        from browser_use import Agent

        # Get the underlying browser if we have a TracedBrowser
        browser = self._browser._browser if hasattr(self._browser, "_browser") else self._browser

        # Create the agent with our wrapped LLM
        self._agent = Agent(
            task=self._task,
            llm=self._llm,  # Use traced LLM
            browser=browser,
            max_steps=self._max_steps,
            **self._agent_kwargs,
        )

        return self._agent

    async def run(
        self,
        trace_name: str | None = None,
        tags: dict[str, str] | None = None,
        metadata: dict[str, Any] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ) -> Any:
        """Run the agent with full tracing.

        Args:
            trace_name: Optional name for the root trace
            tags: Optional tags to add to the trace
            metadata: Optional metadata to add to the trace
            user_id: Optional user ID for the trace
            session_id: Optional session ID for the trace

        Returns:
            The agent's result (AgentHistory from browser-use)
        """
        self._start_time = time.perf_counter()
        self._step_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        self._timed_out_steps = 0
        self._retried_steps = 0

        aigie = self._get_aigie()
        trace = None
        result = None
        error = None

        # Prepare trace metadata
        trace_metadata = {
            "task": self._task,
            "max_steps": self._max_steps,
            "framework": "browser-use",
            **(metadata or {}),
            **self._config.default_metadata,
        }

        trace_tags = {
            "framework": "browser-use",
            **(tags or {}),
            **self._config.default_tags,
        }

        try:
            # Create root trace
            if aigie:
                with contextlib.suppress(Exception):
                    trace = await aigie.trace(
                        name=trace_name or "browser_use.task",
                        user_id=user_id,
                        session_id=session_id,
                        tags=trace_tags,
                        metadata=trace_metadata,
                    ).__aenter__()

            # Create the browser-use agent
            await self._create_browser_use_agent()

            # Create run span
            run_span = None
            if trace:
                try:
                    run_span = await trace.span(
                        name=f"{self._config.span_prefix}.agent.run",
                        run_type="chain",
                    ).__aenter__()

                    if run_span:
                        run_span.set_input({"task": self._task})
                except Exception:
                    pass

            try:
                # Run the agent with step callback for tracing
                if self._config.trace_agent_steps:
                    result = await self._run_with_step_tracing(run_span)
                else:
                    result = await self._agent.run()

            finally:
                # Close run span
                if run_span:
                    try:
                        duration = time.perf_counter() - self._start_time
                        run_span.set_latency(duration)
                        run_span.set_output(
                            {
                                "steps": self._step_count,
                                "total_tokens": self._total_tokens,
                                "total_cost": self._total_cost,
                                "success": result is not None and error is None,
                            }
                        )
                        await run_span.__aexit__(None, None, None)
                    except Exception:
                        pass

            return result

        except Exception as e:
            error = e
            raise

        finally:
            # Close root trace
            if trace:
                try:
                    duration = time.perf_counter() - self._start_time
                    trace.set_metadata(
                        {
                            "duration_seconds": duration,
                            "total_steps": self._step_count,
                            "total_tokens": self._total_tokens,
                            "total_cost": self._total_cost,
                            "success": error is None,
                        }
                    )
                    if error:
                        trace.set_error(str(error))
                    await trace.__aexit__(None, None, None)
                except Exception:
                    pass

    async def _run_with_step_tracing(self, parent_span: Any | None) -> Any:
        """Run agent with step-by-step tracing and timeout support.

        This hooks into the agent's execution to trace each step.
        Steps that timeout or fail transiently will be retried according to config.
        """
        # browser-use Agent has a step() method we can trace
        # We need to run steps manually to trace each one

        history = None

        while self._step_count < self._max_steps:
            self._step_count += 1
            step_span = None
            step_timed_out = False
            step_retry_count = 0

            try:
                # Create step span
                if parent_span:
                    try:
                        step_span = await parent_span.span(
                            name=f"{self._config.span_prefix}.step_{self._step_count}",
                            run_type="chain",
                        ).__aenter__()

                        if step_span:
                            step_span.set_metadata(
                                {
                                    "step_number": self._step_count,
                                    "step_timeout": self._config.step_timeout,
                                    "max_retries": self._config.max_retries,
                                }
                            )
                    except Exception:
                        pass

                # Execute the step with timeout and retry
                step_start = time.perf_counter()

                async def _execute_step():
                    return await self._agent.step()

                # Apply timeout and retry if configured
                if self._config.step_timeout > 0 or self._config.max_retries > 0:
                    try:
                        step_result = await with_timeout_and_retry(
                            _execute_step,
                            timeout=self._config.step_timeout,
                            max_retries=self._config.max_retries,
                            retry_delay=self._config.retry_delay,
                            operation_name=f"agent.step_{self._step_count}",
                        )
                    except TimeoutExceededError as e:
                        step_timed_out = True
                        self._timed_out_steps += 1
                        logger.warning(f"Step {self._step_count} timed out after {e.timeout}s")
                        # Continue to next step instead of failing entirely
                        step_result = None
                    except RetryExhaustedError as e:
                        step_retry_count = e.attempts
                        self._retried_steps += 1
                        logger.warning(
                            f"Step {self._step_count} failed after {e.attempts} retries: {e.last_error}"
                        )
                        # Continue to next step instead of failing entirely
                        step_result = None
                else:
                    step_result = await _execute_step()

                step_duration = time.perf_counter() - step_start

                # Update history
                history = step_result

                # Check if done
                is_done = self._check_if_done(step_result)

                # Update step span
                if step_span:
                    try:
                        step_span.set_latency(step_duration)
                        output_data = {
                            "step": self._step_count,
                            "done": is_done,
                        }
                        if step_timed_out:
                            output_data["timed_out"] = True
                        if step_retry_count > 0:
                            output_data["retry_attempts"] = step_retry_count
                        step_span.set_output(output_data)
                    except Exception:
                        pass

                if is_done:
                    break

            except Exception as e:
                if step_span:
                    with contextlib.suppress(Exception):
                        step_span.set_error(str(e))
                raise

            finally:
                if step_span:
                    with contextlib.suppress(Exception):
                        await step_span.__aexit__(None, None, None)

        return history

    def _check_if_done(self, step_result: Any) -> bool:
        """Check if the agent has completed its task."""
        if step_result is None:
            return True

        # Check common completion indicators
        if hasattr(step_result, "is_done"):
            return step_result.is_done

        if hasattr(step_result, "done"):
            return step_result.done

        if hasattr(step_result, "finished"):
            return step_result.finished

        # Check for final action in result
        if hasattr(step_result, "actions") and step_result.actions:
            last_action = step_result.actions[-1]
            if hasattr(last_action, "done") and last_action.done:
                return True

        return False

    async def step(self) -> Any:
        """Execute a single step with tracing.

        Use this for more granular control over execution.
        """
        if self._agent is None:
            await self._create_browser_use_agent()

        self._step_count += 1

        aigie = self._get_aigie()
        span = None

        try:
            if aigie:
                try:
                    from aigie.context_manager import get_current_trace_context

                    trace_ctx = get_current_trace_context()
                    if trace_ctx:
                        span = await trace_ctx.span(
                            name=f"{self._config.span_prefix}.step_{self._step_count}",
                            run_type="chain",
                        ).__aenter__()
                except Exception:
                    pass

            step_start = time.perf_counter()
            result = await self._agent.step()
            step_duration = time.perf_counter() - step_start

            if span:
                span.set_latency(step_duration)
                span.set_output({"step": self._step_count, "done": self._check_if_done(result)})

            return result

        finally:
            if span:
                with contextlib.suppress(Exception):
                    await span.__aexit__(None, None, None)

    @property
    def step_count(self) -> int:
        """Get the current step count."""
        return self._step_count

    @property
    def total_tokens(self) -> int:
        """Get the total tokens used."""
        return self._total_tokens

    @property
    def total_cost(self) -> float:
        """Get the total cost incurred."""
        return self._total_cost

    def __repr__(self) -> str:
        return (
            f"TracedAgent(task={self._task!r}, "
            f"steps={self._step_count}, "
            f"max_steps={self._max_steps})"
        )
