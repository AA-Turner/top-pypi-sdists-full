"""
Traced Browser wrapper for browser-use.

Wraps browser-use Browser class to trace browser actions.
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
from .config import BrowserUseConfig
from .utils import (
    compress_screenshot,
    extract_action_info,
    mask_sensitive_text,
    safe_str,
    screenshot_to_base64,
)


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


class TracedBrowser:
    """Wrapper that adds Aigie tracing to browser-use Browser.

    Traces browser actions like click, type, scroll, navigate, etc.
    Optionally captures screenshots and DOM state.

    Usage:
        from browser_use import Browser
        from aigie.integrations.browser_use import TracedBrowser

        # Option 1: Wrap existing browser
        browser = Browser()
        traced_browser = TracedBrowser(browser, aigie_client)

        # Option 2: Create new traced browser
        traced_browser = TracedBrowser(aigie=aigie_client)
    """

    def __init__(
        self,
        browser: Any | None = None,
        aigie: Any | None = None,
        config: BrowserUseConfig | None = None,
    ):
        """Initialize the traced browser wrapper.

        Args:
            browser: Optional existing Browser instance to wrap.
                    If None, creates a new Browser when needed.
            aigie: Optional Aigie client instance. If None, uses global client.
            config: Configuration for tracing behavior.
        """
        self._browser = browser
        self._aigie = aigie
        self._config = config or BrowserUseConfig()
        self._action_count = 0
        self._initialized = False

    async def _ensure_browser(self) -> Any:
        """Ensure browser instance exists."""
        if self._browser is None:
            try:
                from browser_use import Browser

                self._browser = Browser()
            except ImportError:
                raise ImportError("browser-use is required. Install with: pip install browser-use")
        return self._browser

    def _get_aigie(self) -> Any | None:
        """Get the Aigie client instance."""
        if self._aigie:
            return self._aigie
        try:
            from aigie import get_aigie

            return get_aigie()
        except (ImportError, Exception):
            return None

    async def _get_current_span(self) -> Any | None:
        """Get the current span context if available."""
        try:
            from aigie.context_manager import get_current_span_context

            return get_current_span_context()
        except (ImportError, Exception):
            return None

    async def _trace_action(
        self,
        action_name: str,
        action_func: Any,
        *args,
        capture_screenshot: bool = True,
        metadata: dict[str, Any] | None = None,
        use_timeout: bool = True,
        use_retry: bool = True,
        **kwargs,
    ) -> Any:
        """Execute and trace a browser action with timeout/retry support.

        Args:
            action_name: Name of the action (e.g., "click", "type")
            action_func: The actual function to call
            *args: Arguments for the action
            capture_screenshot: Whether to capture screenshot after action
            metadata: Additional metadata to include
            use_timeout: Whether to apply action timeout
            use_retry: Whether to retry on transient failures
            **kwargs: Keyword arguments for the action

        Returns:
            Result of the action

        Raises:
            RetryExhaustedError: If all retry attempts are exhausted
            TimeoutExceededError: If the action times out
        """
        if not self._config.trace_browser_actions:
            # Still apply timeout/retry even without tracing
            if use_timeout or use_retry:
                return await with_timeout_and_retry(
                    action_func,
                    *args,
                    timeout=self._config.action_timeout if use_timeout else 0,
                    max_retries=self._config.max_retries if use_retry else 0,
                    retry_delay=self._config.retry_delay,
                    operation_name=f"browser.{action_name}",
                    **kwargs,
                )
            return await action_func(*args, **kwargs)

        self._action_count += 1
        action_id = self._action_count
        start_time = time.perf_counter()

        span = None
        result = None
        error = None
        retry_attempts = 0

        try:
            # Create span
            parent_span = await self._get_current_span()
            if parent_span:
                try:
                    span = await parent_span.span(
                        name=f"{self._config.span_prefix}.action.{action_name}",
                        run_type="tool",
                    ).__aenter__()

                    if span:
                        # Set action metadata
                        action_metadata = {
                            "action_type": action_name,
                            "action_id": action_id,
                            "timeout": self._config.action_timeout if use_timeout else None,
                            "max_retries": self._config.max_retries if use_retry else 0,
                        }
                        if metadata:
                            action_metadata.update(metadata)

                        # Add selector info if available
                        if self._config.include_action_selectors and args:
                            action_metadata["target"] = safe_str(args[0], max_length=200)

                        span.set_metadata(action_metadata)
                        span.set_input({"action": action_name, "args": [safe_str(a) for a in args]})
                except Exception:
                    pass

            # Execute the action with timeout/retry if configured
            if use_timeout or use_retry:
                result = await with_timeout_and_retry(
                    action_func,
                    *args,
                    timeout=self._config.action_timeout if use_timeout else 0,
                    max_retries=self._config.max_retries if use_retry else 0,
                    retry_delay=self._config.retry_delay,
                    operation_name=f"browser.{action_name}",
                    **kwargs,
                )
            else:
                result = await action_func(*args, **kwargs)

            # Capture screenshot if enabled
            if capture_screenshot and self._config.trace_screenshots and span and self._browser:
                try:
                    await self._capture_and_attach_screenshot(span)
                except Exception:
                    pass  # Don't fail action due to screenshot issues

            # Capture DOM state if enabled
            if self._config.trace_dom and span and self._browser:
                try:
                    await self._capture_and_attach_dom(span)
                except Exception:
                    pass  # Don't fail action due to DOM capture issues

            return result

        except RetryExhaustedError as e:
            error = e
            retry_attempts = e.attempts
            logger.error(
                f"Browser action '{action_name}' failed after {retry_attempts} attempts: {e.last_error}"
            )
            raise

        except TimeoutExceededError as e:
            error = e
            logger.error(f"Browser action '{action_name}' timed out after {e.timeout}s")
            raise

        except Exception as e:
            error = e
            raise

        finally:
            # Update span
            if span:
                try:
                    latency = time.perf_counter() - start_time
                    span.set_latency(latency)

                    # Add retry info to metadata
                    if retry_attempts > 0:
                        span.set_metadata(
                            {
                                "retry_attempts": retry_attempts,
                            }
                        )

                    if error:
                        span.set_error(str(error))
                        error_info = {"success": False, "error": str(error)}
                        if isinstance(error, RetryExhaustedError):
                            error_info["retry_exhausted"] = True
                            error_info["attempts"] = retry_attempts
                        elif isinstance(error, TimeoutExceededError):
                            error_info["timed_out"] = True
                            error_info["timeout"] = error.timeout
                        span.set_output(error_info)
                    else:
                        span.set_output(
                            {
                                "success": True,
                                "result": safe_str(result) if result else None,
                            }
                        )

                    await span.__aexit__(None, None, None)
                except Exception:
                    pass

    async def _capture_and_attach_screenshot(self, span: Any) -> None:
        """Capture screenshot and attach to span."""
        if not self._browser:
            return

        try:
            # Try to get screenshot from browser
            screenshot_bytes = None

            if hasattr(self._browser, "screenshot"):
                screenshot_bytes = await self._browser.screenshot()
            elif hasattr(self._browser, "page") and self._browser.page:
                screenshot_bytes = await self._browser.page.screenshot()

            if screenshot_bytes:
                # Compress if needed
                if self._config.compress_screenshots:
                    screenshot_bytes = compress_screenshot(
                        screenshot_bytes,
                        quality=self._config.screenshot_quality,
                        max_size=self._config.max_screenshot_size,
                    )

                # Attach as base64
                screenshot_b64 = screenshot_to_base64(screenshot_bytes)
                span.set_metadata(
                    {
                        "screenshot": screenshot_b64,
                        "screenshot_size": len(screenshot_bytes),
                    }
                )
        except Exception:
            pass  # Screenshot capture is optional

    async def _capture_and_attach_dom(self, span: Any) -> None:
        """Capture DOM state and attach to span.

        Captures key DOM information including:
        - Current URL
        - Page title
        - Visible text content (truncated)
        - Interactive elements count
        """
        if not self._browser or not self._config.trace_dom:
            return

        try:
            dom_state: dict[str, Any] = {}

            # Get current URL
            if hasattr(self._browser, "current_url"):
                dom_state["url"] = self._browser.current_url
            elif hasattr(self._browser, "page") and self._browser.page:
                dom_state["url"] = self._browser.page.url

            # Get page title
            if hasattr(self._browser, "title"):
                dom_state["title"] = self._browser.title
            elif hasattr(self._browser, "page") and self._browser.page:
                with contextlib.suppress(Exception):
                    dom_state["title"] = await self._browser.page.title()

            # Get visible text (truncated for size)
            if hasattr(self._browser, "get_page_content"):
                try:
                    content = await self._browser.get_page_content()
                    # Extract text only, remove HTML tags
                    import re

                    text_only = re.sub(r"<[^>]+>", " ", content)
                    text_only = re.sub(r"\s+", " ", text_only).strip()
                    dom_state["visible_text"] = text_only[:2000]  # Limit to 2KB
                    dom_state["content_length"] = len(content)
                except Exception:
                    pass

            # Get interactive elements count
            if hasattr(self._browser, "page") and self._browser.page:
                try:
                    # Count interactive elements
                    buttons = await self._browser.page.query_selector_all("button")
                    links = await self._browser.page.query_selector_all("a")
                    inputs = await self._browser.page.query_selector_all("input")
                    dom_state["interactive_elements"] = {
                        "buttons": len(buttons) if buttons else 0,
                        "links": len(links) if links else 0,
                        "inputs": len(inputs) if inputs else 0,
                    }
                except Exception:
                    pass

            if dom_state:
                span.set_metadata({"dom_state": dom_state})

        except Exception:
            pass  # DOM capture is optional

    # Browser interface methods - these proxy to the underlying browser
    # with tracing added

    async def click(self, selector: str, **kwargs) -> Any:
        """Click an element with tracing."""
        browser = await self._ensure_browser()
        return await self._trace_action(
            "click",
            browser.click,
            selector,
            metadata={"selector": selector},
            **kwargs,
        )

    async def type(self, selector: str, text: str, **kwargs) -> Any:
        """Type text into an element with tracing."""
        browser = await self._ensure_browser()

        # Mask text if configured
        if self._config.mask_sensitive_data:
            mask_sensitive_text(text)

        return await self._trace_action(
            "type",
            browser.type,
            selector,
            text,
            metadata={"selector": selector, "text_length": len(text)},
            **kwargs,
        )

    async def navigate(self, url: str, **kwargs) -> Any:
        """Navigate to a URL with tracing."""
        browser = await self._ensure_browser()
        return await self._trace_action(
            "navigate",
            browser.navigate,
            url,
            metadata={"url": url},
            **kwargs,
        )

    async def scroll(self, direction: str = "down", amount: int = 300, **kwargs) -> Any:
        """Scroll the page with tracing."""
        browser = await self._ensure_browser()
        return await self._trace_action(
            "scroll",
            browser.scroll,
            direction,
            amount,
            metadata={"direction": direction, "amount": amount},
            **kwargs,
        )

    async def wait(self, selector: str, **kwargs) -> Any:
        """Wait for an element with tracing."""
        browser = await self._ensure_browser()
        return await self._trace_action(
            "wait",
            browser.wait,
            selector,
            capture_screenshot=False,  # Don't screenshot for waits
            metadata={"selector": selector},
            **kwargs,
        )

    async def screenshot(self, **kwargs) -> bytes:
        """Take a screenshot with tracing."""
        browser = await self._ensure_browser()
        return await self._trace_action(
            "screenshot",
            browser.screenshot,
            capture_screenshot=False,  # The action itself is a screenshot
            **kwargs,
        )

    async def get_page_content(self, **kwargs) -> str:
        """Get page HTML content with tracing."""
        browser = await self._ensure_browser()
        return await self._trace_action(
            "get_page_content",
            browser.get_page_content,
            capture_screenshot=False,
            **kwargs,
        )

    async def execute_action(self, action: Any, **kwargs) -> Any:
        """Execute a browser-use action object with tracing.

        This handles the ActionModel objects that browser-use uses.
        """
        browser = await self._ensure_browser()
        action_info = extract_action_info(action)

        return await self._trace_action(
            action_info.get("type", "unknown_action"),
            browser.execute_action,
            action,
            metadata=action_info,
            **kwargs,
        )

    async def close(self) -> None:
        """Close the browser."""
        if self._browser:
            await self._browser.close()

    def __getattr__(self, name: str) -> Any:
        """Proxy all other attributes to the wrapped browser."""
        if self._browser:
            return getattr(self._browser, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __repr__(self) -> str:
        return f"TracedBrowser(actions={self._action_count}, config={self._config})"
