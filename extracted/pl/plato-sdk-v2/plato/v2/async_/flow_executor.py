"""Async flow execution engine for Plato v2."""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urljoin

if TYPE_CHECKING:
    from playwright.async_api import Page

from plato._generated.models import (
    CheckElementStep,
    ClickStep,
    FillStep,
    Flow,
    NavigateStep,
    ScreenshotStep,
    Steps,
    VerifyNoErrorsStep,
    VerifyStep,
    VerifyTextStep,
    VerifyUrlStep,
    WaitForSelectorStep,
    WaitForUrlStep,
    WaitStep,
)
from plato.v2.async_.flow_backends import FlowBackend, FlowExecutionError, PlaywrightBackend
from plato.v2.fast_mode import fast_mode_skips

logger = logging.getLogger(__name__)

__all__ = ["FlowExecutionError", "FlowExecutor"]


class FlowExecutor:
    """Executes configurable flows for simulator interactions (async).

    The executor is decoupled from its execution environment via
    :class:`~plato.v2.async_.flow_backends.FlowBackend`. Passing ``page`` uses
    the default Playwright-backed path; passing ``backend`` is the extension
    point for alternate backends that drive the flow against a different
    browser surface.

    ``fast_mode`` executes the same flow minus its dead time: authored
    ``wait`` sleeps and everything after the last real action (the trailing
    confirmation tail) are skipped — see :mod:`plato.v2.fast_mode` — and the
    default Playwright backend navigates at ``domcontentloaded`` and lets
    actions auto-wait instead of pre-waiting.
    """

    def __init__(
        self,
        page: Page | None = None,
        flow: Flow | None = None,
        screenshots_dir: Path | None = None,
        log: logging.Logger | None = None,
        *,
        backend: FlowBackend | None = None,
        base_url: str | None = None,
        fast_mode: bool = False,
    ):
        if flow is None:
            raise TypeError("FlowExecutor requires a `flow` argument")
        if backend is not None and page is not None:
            raise TypeError("Pass `page` or `backend`, not both")
        if backend is None:
            if page is None:
                raise TypeError("FlowExecutor requires `page` or `backend`")
            backend = PlaywrightBackend(page, fast_mode=fast_mode)

        self.page = page
        self.backend = backend
        self.flow = flow
        self.screenshots_dir = screenshots_dir
        if self.screenshots_dir:
            self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.base_url: str | None = base_url
        self.log = log or logger
        # Executor-level fast mode (skip waits + confirmation tail) applies to
        # any backend; the backend-level speedups only when the default
        # Playwright backend was built here.
        self.fast_mode = fast_mode

    async def _resolve_url(self, url: str) -> str:
        """Resolve a URL against the base URL if it's relative."""
        if url.startswith(("http://", "https://")):
            return url

        if not self.base_url:
            current = await self.backend.current_url()
            if current:
                self.base_url = current

        if self.base_url:
            return urljoin(self.base_url, url)

        return url

    async def execute(self) -> None:
        """Execute the flow.

        Raises:
            FlowExecutionError: If any step fails.
        """
        steps = self.flow.steps or []

        self.log.info(f"🔄 Starting flow: {self.flow.name}")
        self.log.info(f"📋 Flow description: {self.flow.description or 'No description'}")
        self.log.info(f"🎯 Steps to execute: {len(steps)}")

        # Unwrap Steps RootModel to get actual steps
        unwrapped = [step_wrapper.root if isinstance(step_wrapper, Steps) else step_wrapper for step_wrapper in steps]
        skipped = fast_mode_skips([step.type for step in unwrapped]) if self.fast_mode else frozenset()
        for i, step in enumerate(unwrapped, 1):
            if i - 1 in skipped:
                self.log.info(f"⏩ Step {i}/{len(unwrapped)}: {step.type} skipped (fast mode)")
                continue
            self.log.info(f"🔸 Step {i}/{len(unwrapped)}: {step.description or step.type}")
            await self._execute_step(step)

        self.log.info(f"✅ Flow '{self.flow.name}' completed successfully")

    async def _execute_step(self, step) -> None:
        """Execute a single step in a flow."""
        handlers = {
            "wait_for_selector": self._wait_for_selector,
            "click": self._click,
            "fill": self._fill,
            "wait": self._wait,
            "navigate": self._navigate,
            "wait_for_url": self._wait_for_url,
            "check_element": self._check_element,
            "verify": self._verify,
            "screenshot": self._screenshot,
            "verify_text": self._verify_text,
            "verify_url": self._verify_url,
            "verify_no_errors": self._verify_no_errors,
        }

        handler = handlers.get(step.type)
        if handler:
            await handler(step)
            return

        raise FlowExecutionError(f"Unknown step type: {step.type}")

    async def _wait_for_selector(self, step: WaitForSelectorStep) -> None:
        try:
            await self.backend.wait_for_selector(step.selector, step.timeout)
            self.log.info(f"✅ Selector found: {step.selector}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Selector not found: {step.selector} - {e}") from e

    async def _click(self, step: ClickStep) -> None:
        try:
            await self.backend.click(step.selector, step.timeout)
            self.log.info(f"✅ Clicked: {step.selector}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Failed to click: {step.selector} - {e}") from e

    async def _fill(self, step: FillStep) -> None:
        value = step.value
        try:
            await self.backend.fill(step.selector, str(value), step.timeout)
            display_value = "*" * len(str(value)) if "password" in step.selector.lower() else str(value)
            self.log.info(f"✅ Filled {step.selector} with: {display_value}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Failed to fill: {step.selector} - {e}") from e

    async def _wait(self, step: WaitStep) -> None:
        try:
            await self.backend.wait(step.duration)
            self.log.info(f"✅ Waited {step.duration}ms")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Wait failed: {e}") from e

    async def _navigate(self, step: NavigateStep) -> None:
        try:
            resolved_url = await self._resolve_url(step.url)
            await self.backend.navigate(resolved_url)
            self.log.info(f"✅ Navigated to: {resolved_url}")
            self.base_url = await self.backend.current_url()
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Navigation failed: {step.url} - {e}") from e

    async def _wait_for_url(self, step: WaitForUrlStep) -> None:
        try:
            await self.backend.wait_for_url(step.url_contains, step.timeout)
            self.log.info(f"✅ URL contains: {step.url_contains}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"URL check failed: {step.url_contains} - {e}") from e

    async def _check_element(self, step: CheckElementStep) -> None:
        try:
            await self.backend.check_element(step.selector, step.should_exist)
            if step.should_exist:
                self.log.info(f"✅ Element exists as expected: {step.selector}")
            else:
                self.log.info(f"✅ Element absent as expected: {step.selector}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Element check error: {step.selector} - {e}") from e

    async def _verify(self, step: VerifyStep) -> None:
        try:
            await self.backend.verify(step)
            self.log.info(f"✅ Verified: {step.verify_type}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Verification error: {e}") from e

    async def _screenshot(self, step: ScreenshotStep) -> None:
        try:
            timestamp_ms = int(time.time() * 1000)
            filename = step.filename
            if "." in filename:
                name, ext = filename.rsplit(".", 1)
                timestamped_filename = f"{timestamp_ms}_{name}.{ext}"
            else:
                timestamped_filename = f"{timestamp_ms}_{filename}.png"

            if self.screenshots_dir:
                screenshot_path = self.screenshots_dir / timestamped_filename
                await self.backend.screenshot(screenshot_path, full_page=step.full_page)
                self.log.info(f"📸 Screenshot: {screenshot_path}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Screenshot failed: {e}") from e

    async def _verify_text(self, step: VerifyTextStep) -> None:
        try:
            await self.backend.verify_text(step.text, step.should_exist)
            if step.should_exist:
                self.log.info(f"✅ Text '{step.text}' found on page")
            else:
                self.log.info(f"✅ Text '{step.text}' not found (as expected)")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Text verification error: {e}") from e

    async def _verify_url(self, step: VerifyUrlStep) -> None:
        try:
            await self.backend.verify_url(step.url, step.contains)
            if step.contains:
                self.log.info(f"✅ URL contains '{step.url}'")
            else:
                self.log.info(f"✅ URL matches '{step.url}'")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"URL verification error: {e}") from e

    async def _verify_no_errors(self, step: VerifyNoErrorsStep) -> None:
        try:
            await self.backend.verify_no_errors(step.error_selectors or [])
            self.log.info("✅ No error indicators found")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Error verification failed: {e}") from e
