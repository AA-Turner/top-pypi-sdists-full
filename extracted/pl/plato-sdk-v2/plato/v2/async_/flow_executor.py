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

logger = logging.getLogger(__name__)


class FlowExecutionError(Exception):
    """Raised when a flow step fails."""

    pass


class FlowExecutor:
    """Executes configurable flows for simulator interactions (async)."""

    def __init__(
        self,
        page: Page,
        flow: Flow,
        screenshots_dir: Path | None = None,
        log: logging.Logger | None = None,
    ):
        self.page = page
        self.flow = flow
        self.screenshots_dir = screenshots_dir
        if self.screenshots_dir:
            self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.base_url: str | None = None
        self.log = log or logger

    def _resolve_url(self, url: str) -> str:
        """Resolve a URL against the base URL if it's relative."""
        if url.startswith(("http://", "https://")):
            return url

        if not self.base_url and self.page.url:
            self.base_url = self.page.url

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

        for i, step_wrapper in enumerate(steps, 1):
            # Unwrap Steps RootModel to get actual step
            step = step_wrapper.root if isinstance(step_wrapper, Steps) else step_wrapper
            self.log.info(f"🔸 Step {i}/{len(steps)}: {step.description or step.type}")
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
            await self.page.wait_for_selector(step.selector, timeout=step.timeout)
            self.log.info(f"✅ Selector found: {step.selector}")
        except Exception as e:
            raise FlowExecutionError(f"Selector not found: {step.selector} - {e}") from e

    async def _click(self, step: ClickStep) -> None:
        try:
            await self.page.wait_for_selector(step.selector, timeout=step.timeout)
            await self.page.click(step.selector)
            self.log.info(f"✅ Clicked: {step.selector}")
        except Exception as e:
            raise FlowExecutionError(f"Failed to click: {step.selector} - {e}") from e

    async def _fill(self, step: FillStep) -> None:
        value = step.value
        try:
            await self.page.wait_for_selector(step.selector, timeout=step.timeout)
            await self.page.fill(step.selector, str(value))
            display_value = "*" * len(str(value)) if "password" in step.selector.lower() else str(value)
            self.log.info(f"✅ Filled {step.selector} with: {display_value}")
        except Exception as e:
            raise FlowExecutionError(f"Failed to fill: {step.selector} - {e}") from e

    async def _wait(self, step: WaitStep) -> None:
        try:
            await self.page.wait_for_timeout(step.duration)
            self.log.info(f"✅ Waited {step.duration}ms")
        except Exception as e:
            raise FlowExecutionError(f"Wait failed: {e}") from e

    async def _navigate(self, step: NavigateStep) -> None:
        try:
            resolved_url = self._resolve_url(step.url)
            await self.page.goto(resolved_url)
            self.log.info(f"✅ Navigated to: {resolved_url}")
            self.base_url = self.page.url
        except Exception as e:
            raise FlowExecutionError(f"Navigation failed: {step.url} - {e}") from e

    async def _wait_for_url(self, step: WaitForUrlStep) -> None:
        try:
            await self.page.wait_for_function(
                f"window.location.href.includes('{step.url_contains}')",
                timeout=step.timeout,
            )
            self.log.info(f"✅ URL contains: {step.url_contains}")
        except Exception as e:
            raise FlowExecutionError(f"URL check failed: {step.url_contains} - {e}") from e

    async def _check_element(self, step: CheckElementStep) -> None:
        try:
            element = await self.page.query_selector(step.selector)
            exists = element is not None

            if step.should_exist and exists:
                self.log.info(f"✅ Element exists as expected: {step.selector}")
                return
            elif not step.should_exist and not exists:
                self.log.info(f"✅ Element absent as expected: {step.selector}")
                return
            else:
                raise FlowExecutionError(
                    f"Element check failed: {step.selector} (expected: {step.should_exist}, found: {exists})"
                )
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Element check error: {step.selector} - {e}") from e

    async def _verify(self, step: VerifyStep) -> None:
        handlers = {
            "element_exists": self._verify_element_exists,
            "element_visible": self._verify_element_visible,
            "element_text": self._verify_element_text,
            "element_count": self._verify_element_count,
            "page_title": self._verify_page_title,
        }
        vt = step.verify_type
        verify_key = vt.value if hasattr(vt, "value") else vt
        handler = handlers.get(str(verify_key))
        if handler:
            await handler(step)
            return
        raise FlowExecutionError(f"Unknown verification type: {step.verify_type}")

    async def _verify_element_exists(self, step: VerifyStep) -> None:
        try:
            element = await self.page.query_selector(step.selector) if step.selector else None
            if element:
                self.log.info(f"✅ Element exists: {step.selector}")
                return
            raise FlowExecutionError(f"Element not found: {step.selector}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Verification error: {step.selector} - {e}") from e

    async def _verify_element_visible(self, step: VerifyStep) -> None:
        try:
            element = await self.page.query_selector(step.selector) if step.selector else None
            if element and await element.is_visible():
                self.log.info(f"✅ Element is visible: {step.selector}")
                return
            raise FlowExecutionError(f"Element not visible: {step.selector}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Verification error: {step.selector} - {e}") from e

    async def _verify_element_text(self, step: VerifyStep) -> None:
        try:
            element = await self.page.query_selector(step.selector) if step.selector else None
            if not element:
                raise FlowExecutionError(f"Element not found: {step.selector}")

            actual_text = await element.text_content() or ""
            if step.contains:
                if step.text and step.text in actual_text:
                    self.log.info(f"✅ Text contains '{step.text}'")
                    return
                raise FlowExecutionError(f"Text '{actual_text}' does not contain '{step.text}'")
            else:
                if step.text == actual_text.strip():
                    self.log.info(f"✅ Text matches '{step.text}'")
                    return
                raise FlowExecutionError(f"Text '{actual_text}' does not match '{step.text}'")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Verification error: {step.selector} - {e}") from e

    async def _verify_element_count(self, step: VerifyStep) -> None:
        try:
            elements = await self.page.query_selector_all(step.selector) if step.selector else []
            actual_count = len(elements)
            if actual_count == step.count:
                self.log.info(f"✅ Found {actual_count} elements")
                return
            raise FlowExecutionError(f"Expected {step.count} elements, found {actual_count}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Verification error: {step.selector} - {e}") from e

    async def _verify_page_title(self, step: VerifyStep) -> None:
        try:
            actual_title = await self.page.title()
            if step.contains:
                if step.title and step.title in actual_title:
                    self.log.info(f"✅ Title contains '{step.title}'")
                    return
                raise FlowExecutionError(f"Title '{actual_title}' does not contain '{step.title}'")
            else:
                if step.title == actual_title:
                    self.log.info(f"✅ Title matches '{step.title}'")
                    return
                raise FlowExecutionError(f"Title '{actual_title}' does not match '{step.title}'")
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
                await self.page.screenshot(path=str(screenshot_path), full_page=step.full_page)
                self.log.info(f"📸 Screenshot: {screenshot_path}")
        except Exception as e:
            raise FlowExecutionError(f"Screenshot failed: {e}") from e

    async def _verify_text(self, step: VerifyTextStep) -> None:
        try:
            page_content = await self.page.content()
            text_found = step.text in page_content

            if step.should_exist and text_found:
                self.log.info(f"✅ Text '{step.text}' found on page")
                return
            elif not step.should_exist and not text_found:
                self.log.info(f"✅ Text '{step.text}' not found (as expected)")
                return
            else:
                if step.should_exist:
                    raise FlowExecutionError(f"Text '{step.text}' not found on page")
                else:
                    raise FlowExecutionError(f"Text '{step.text}' found (should not exist)")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Text verification error: {e}") from e

    async def _verify_url(self, step: VerifyUrlStep) -> None:
        try:
            current_url = self.page.url
            if step.contains:
                if step.url in current_url:
                    self.log.info(f"✅ URL contains '{step.url}'")
                    return
                raise FlowExecutionError(f"URL '{current_url}' does not contain '{step.url}'")
            else:
                if step.url == current_url:
                    self.log.info(f"✅ URL matches '{step.url}'")
                    return
                raise FlowExecutionError(f"URL '{current_url}' does not match '{step.url}'")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"URL verification error: {e}") from e

    async def _verify_no_errors(self, step: VerifyNoErrorsStep) -> None:
        try:
            errors_found = []
            for selector in step.error_selectors or []:
                elements = await self.page.query_selector_all(selector)
                for element in elements:
                    if await element.is_visible():
                        text = await element.text_content()
                        if text and text.strip():
                            errors_found.append(f"{selector}: {text.strip()}")

            if not errors_found:
                self.log.info("✅ No error indicators found")
                return
            raise FlowExecutionError(f"Error indicators found: {errors_found}")
        except FlowExecutionError:
            raise
        except Exception as e:
            raise FlowExecutionError(f"Error verification failed: {e}") from e
