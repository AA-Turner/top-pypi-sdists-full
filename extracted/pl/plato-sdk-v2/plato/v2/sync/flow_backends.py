"""Execution backends for the synchronous FlowExecutor.

See :mod:`plato.v2.async_.flow_backends` for the async twin and an overview of
how backends work.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from playwright.sync_api import Page

    from plato._generated.models import VerifyStep

RunCmd = Callable[[Sequence[str]], tuple[int, str, str]]
"""Sync signature: ``argv -> (exit_code, stdout, stderr)``."""


class FlowExecutionError(Exception):
    """Raised when a flow step fails."""

    pass


@runtime_checkable
class FlowBackend(Protocol):
    """Protocol every synchronous FlowExecutor backend must satisfy."""

    # Optional args mirror the wire types (``Flow*Step.timeout: int | None``,
    # ``should_exist: bool | None``, …). See the async twin for the rationale.
    def navigate(self, url: str) -> None: ...
    def click(self, selector: str, timeout_ms: int | None) -> None: ...
    def fill(self, selector: str, value: str, timeout_ms: int | None) -> None: ...
    def wait_for_selector(self, selector: str, timeout_ms: int | None) -> None: ...
    def wait_for_url(self, url_contains: str, timeout_ms: int | None) -> None: ...
    def wait(self, duration_ms: int) -> None: ...
    def current_url(self) -> str: ...
    def screenshot(self, path: Path, *, full_page: bool | None = False) -> None: ...

    def check_element(self, selector: str, should_exist: bool | None) -> None: ...
    def verify(self, step: VerifyStep) -> None: ...
    def verify_text(self, text: str, should_exist: bool | None) -> None: ...
    def verify_url(self, url: str, contains: bool | None) -> None: ...
    def verify_no_errors(self, selectors: list[str]) -> None: ...


class PlaywrightBackend:
    """Synchronous FlowBackend wrapping a Playwright ``Page``.

    See the async twin for the ``fast_mode`` rationale: ``domcontentloaded``
    navigation plus Playwright auto-wait instead of explicit pre-waits.
    """

    def __init__(self, page: Page, *, fast_mode: bool = False) -> None:
        self.page = page
        self.fast_mode = fast_mode

    def navigate(self, url: str) -> None:
        if self.fast_mode:
            self.page.goto(url, wait_until="domcontentloaded")
        else:
            self.page.goto(url)

    def click(self, selector: str, timeout_ms: int | None) -> None:
        if self.fast_mode:
            self.page.click(selector, timeout=timeout_ms)
            return
        self.page.wait_for_selector(selector, timeout=timeout_ms)
        self.page.click(selector)

    def fill(self, selector: str, value: str, timeout_ms: int | None) -> None:
        if self.fast_mode:
            self.page.fill(selector, value, timeout=timeout_ms)
            return
        self.page.wait_for_selector(selector, timeout=timeout_ms)
        self.page.fill(selector, value)

    def wait_for_selector(self, selector: str, timeout_ms: int | None) -> None:
        self.page.wait_for_selector(selector, timeout=timeout_ms)

    def wait_for_url(self, url_contains: str, timeout_ms: int | None) -> None:
        self.page.wait_for_function(
            f"window.location.href.includes('{url_contains}')",
            timeout=timeout_ms,
        )

    def wait(self, duration_ms: int) -> None:
        self.page.wait_for_timeout(duration_ms)

    def current_url(self) -> str:
        return self.page.url or ""

    def screenshot(self, path: Path, *, full_page: bool | None = False) -> None:
        self.page.screenshot(path=str(path), full_page=bool(full_page))

    def check_element(self, selector: str, should_exist: bool | None) -> None:
        element = self.page.query_selector(selector)
        exists = element is not None
        if bool(should_exist) == exists:
            return
        raise _check_failure(f"Element check failed: {selector} (expected: {should_exist}, found: {exists})")

    def verify(self, step: VerifyStep) -> None:  # noqa: C901
        vt = step.verify_type
        verify_key = vt.value if hasattr(vt, "value") else vt
        key = str(verify_key)
        if key == "element_exists":
            try:
                element = self.page.query_selector(step.selector) if step.selector else None
                if element:
                    return
                raise _check_failure(f"Element not found: {step.selector}")
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "element_visible":
            try:
                element = self.page.query_selector(step.selector) if step.selector else None
                if element and element.is_visible():
                    return
                raise _check_failure(f"Element not visible: {step.selector}")
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "element_text":
            try:
                element = self.page.query_selector(step.selector) if step.selector else None
                if not element:
                    raise _check_failure(f"Element not found: {step.selector}")
                actual_text = element.text_content() or ""
                _assert_text(step, actual_text)
                return
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "element_count":
            try:
                elements = self.page.query_selector_all(step.selector) if step.selector else []
                if len(elements) == step.count:
                    return
                raise _check_failure(f"Expected {step.count} elements, found {len(elements)}")
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "page_title":
            try:
                _assert_title(step, self.page.title())
                return
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {e}") from e
        raise _check_failure(f"Unknown verification type: {step.verify_type}")

    def verify_text(self, text: str, should_exist: bool | None) -> None:
        found = text in self.page.content()
        if should_exist and not found:
            raise _check_failure(f"Text '{text}' not found on page")
        if not should_exist and found:
            raise _check_failure(f"Text '{text}' found (should not exist)")

    def verify_url(self, url: str, contains: bool | None) -> None:
        actual = self.page.url
        if contains:
            if url not in actual:
                raise _check_failure(f"URL '{actual}' does not contain '{url}'")
        else:
            if url != actual:
                raise _check_failure(f"URL '{actual}' does not match '{url}'")

    def verify_no_errors(self, selectors: list[str]) -> None:
        errors_found: list[str] = []
        for selector in selectors or []:
            for element in self.page.query_selector_all(selector):
                if element.is_visible():
                    text = element.text_content()
                    if text and text.strip():
                        errors_found.append(f"{selector}: {text.strip()}")
        if errors_found:
            raise _check_failure(f"Error indicators found: {errors_found}")


def _check_failure(msg: str) -> Exception:
    return FlowExecutionError(msg)


def _assert_text(step: VerifyStep, actual_text: str) -> None:
    if step.contains:
        if step.text and step.text in actual_text:
            return
        raise _check_failure(f"Text '{actual_text}' does not contain '{step.text}'")
    if step.text == actual_text.strip():
        return
    raise _check_failure(f"Text '{actual_text}' does not match '{step.text}'")


def _assert_title(step: VerifyStep, actual_title: str) -> None:
    if step.contains:
        if step.title and step.title in actual_title:
            return
        raise _check_failure(f"Title '{actual_title}' does not contain '{step.title}'")
    if step.title == actual_title:
        return
    raise _check_failure(f"Title '{actual_title}' does not match '{step.title}'")


__all__ = [
    "FlowBackend",
    "FlowExecutionError",
    "PlaywrightBackend",
    "RunCmd",
]
