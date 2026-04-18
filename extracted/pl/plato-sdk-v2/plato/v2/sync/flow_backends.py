"""Execution backends for the synchronous FlowExecutor.

See :mod:`plato.v2.async_.flow_backends` for the async twin and an overview of
how backends work.
"""

from __future__ import annotations

import base64
import json
import shlex
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
    """Synchronous FlowBackend wrapping a Playwright ``Page``."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def click(self, selector: str, timeout_ms: int | None) -> None:
        self.page.wait_for_selector(selector, timeout=timeout_ms)
        self.page.click(selector)

    def fill(self, selector: str, value: str, timeout_ms: int | None) -> None:
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


class AgentBrowserBackend:
    """Synchronous FlowBackend driving the ``agent-browser`` CLI via ``run_cmd``.

    See the async twin in :mod:`plato.v2.async_.flow_backends` for the full
    contract. The only difference here is that ``run_cmd`` is a sync callable.
    """

    def __init__(
        self,
        *,
        run_cmd: RunCmd,
        binary: str = "agent-browser",
        session: str | None = None,
    ) -> None:
        self._run_cmd = run_cmd
        self._binary = binary
        self._session = session

    def _ab(self, *args: str) -> tuple[int, str, str]:
        argv: list[str] = [self._binary]
        if self._session is not None:
            argv += ["--session", self._session]
        argv.extend(args)
        return self._run_cmd(argv)

    def _run_checked(self, *args: str, context: str) -> str:
        rc, stdout, stderr = self._ab(*args)
        if rc != 0:
            cmd_repr = " ".join(shlex.quote(a) for a in args)
            raise _check_failure(
                f"{context} failed ({cmd_repr}): rc={rc} stdout={stdout[-400:]!r} stderr={stderr[-400:]!r}"
            )
        return stdout

    def navigate(self, url: str) -> None:
        self._run_checked("open", url, context="navigate")

    @staticmethod
    def _timeout_args(timeout_ms: int | None) -> tuple[str, ...]:
        """``None`` → use agent-browser's built-in default: omit the flag."""
        return () if timeout_ms is None else ("--timeout", str(timeout_ms))

    def click(self, selector: str, timeout_ms: int | None) -> None:
        self._run_checked("wait", selector, *self._timeout_args(timeout_ms), context="click/wait")
        self._run_checked("click", selector, context="click")

    def fill(self, selector: str, value: str, timeout_ms: int | None) -> None:
        self._run_checked("wait", selector, *self._timeout_args(timeout_ms), context="fill/wait")
        self._run_checked("fill", selector, value, context="fill")

    def wait_for_selector(self, selector: str, timeout_ms: int | None) -> None:
        self._run_checked(
            "wait",
            selector,
            *self._timeout_args(timeout_ms),
            context="wait_for_selector",
        )

    def wait_for_url(self, url_contains: str, timeout_ms: int | None) -> None:
        expr = f"window.location.href.includes({json.dumps(url_contains)})"
        self._run_checked(
            "wait",
            "--fn",
            expr,
            *self._timeout_args(timeout_ms),
            context="wait_for_url",
        )

    def wait(self, duration_ms: int) -> None:
        self._run_checked("wait", str(duration_ms), context="wait")

    def current_url(self) -> str:
        stdout = self._run_checked("eval", "--json", "window.location.href", context="current_url")
        stripped = stdout.strip()
        if not stripped:
            return ""
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError:
            return stripped
        if isinstance(payload, dict):
            for key in ("result", "value", "output"):
                if key in payload and isinstance(payload[key], str):
                    return payload[key]
        if isinstance(payload, str):
            return payload
        return stripped

    def screenshot(self, path: Path, *, full_page: bool | None = False) -> None:
        args = ["screenshot", str(path)]
        if full_page:
            args.append("--full")
        self._run_checked(*args, context="screenshot")

    def _eval_json(self, js: str, *, context: str):
        """Evaluate JS in the page and return the parsed JSON result."""
        script_b64 = base64.b64encode(js.encode("utf-8")).decode("ascii")
        stdout = self._run_checked("eval", "--json", "--base64", script_b64, context=context)
        stripped = stdout.strip()
        if not stripped:
            return None
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as e:
            raise _check_failure(f"{context} returned non-JSON output: {stripped[-200:]!r}") from e
        if isinstance(payload, dict):
            for key in ("result", "value", "output"):
                if key in payload:
                    return payload[key]
        return payload

    def check_element(self, selector: str, should_exist: bool | None) -> None:
        js = "(() => document.querySelector(" + json.dumps(selector) + ") !== null)()"
        exists = bool(self._eval_json(js, context="check_element"))
        if should_exist and not exists:
            raise _check_failure(f"Element missing: {selector}")
        if not should_exist and exists:
            raise _check_failure(f"Element present but should be absent: {selector}")

    def verify(self, step: VerifyStep) -> None:  # noqa: C901
        vt = step.verify_type
        verify_key = vt.value if hasattr(vt, "value") else vt
        key = str(verify_key)
        if key == "element_exists":
            if not step.selector:
                raise _check_failure("verify(element_exists) missing selector")
            self.check_element(step.selector, should_exist=True)
            return
        if key == "element_visible":
            if not step.selector:
                raise _check_failure("verify(element_visible) missing selector")
            js = (
                "(() => { const el = document.querySelector(" + json.dumps(step.selector) + "); if (!el) return false; "
                "const s = window.getComputedStyle(el); "
                "return s.display !== 'none' && s.visibility !== 'hidden' "
                "&& el.offsetParent !== null; })()"
            )
            visible = bool(self._eval_json(js, context="verify_element_visible"))
            if not visible:
                raise _check_failure(f"Element not visible: {step.selector}")
            return
        if key == "element_text":
            if not step.selector:
                raise _check_failure("verify(element_text) missing selector")
            js = (
                "(() => { const el = document.querySelector("
                + json.dumps(step.selector)
                + "); return el ? (el.textContent || '') : null; })()"
            )
            actual = self._eval_json(js, context="verify_element_text")
            if actual is None:
                raise _check_failure(f"Element not found: {step.selector}")
            _assert_text(step, str(actual))
            return
        if key == "element_count":
            if not step.selector:
                raise _check_failure("verify(element_count) missing selector")
            js = "document.querySelectorAll(" + json.dumps(step.selector) + ").length"
            count = int(self._eval_json(js, context="verify_element_count") or 0)
            if count != step.count:
                raise _check_failure(f"Expected {step.count} elements, found {count}")
            return
        if key == "page_title":
            title = self._eval_json("document.title", context="verify_page_title")
            _assert_title(step, str(title or ""))
            return
        raise _check_failure(f"Unknown verification type: {step.verify_type}")

    def verify_text(self, text: str, should_exist: bool | None) -> None:
        js = "(document.documentElement && document.documentElement.outerHTML) || ''"
        content = str(self._eval_json(js, context="verify_text") or "")
        found = text in content
        if should_exist and not found:
            raise _check_failure(f"Text '{text}' not found on page")
        if not should_exist and found:
            raise _check_failure(f"Text '{text}' found but should be absent")

    def verify_url(self, url: str, contains: bool | None) -> None:
        actual = self.current_url()
        if contains:
            if url not in actual:
                raise _check_failure(f"URL '{actual}' does not contain '{url}'")
        else:
            if url != actual:
                raise _check_failure(f"URL '{actual}' does not match '{url}'")

    def verify_no_errors(self, selectors: list[str]) -> None:
        if not selectors:
            return
        js = (
            "(() => { const sels = " + json.dumps(list(selectors)) + "; const out = []; for (const sel of sels) { "
            "for (const el of document.querySelectorAll(sel)) { "
            "const s = window.getComputedStyle(el); "
            "if (s.display === 'none' || s.visibility === 'hidden') continue; "
            "if (el.offsetParent === null && s.position !== 'fixed') continue; "
            "const t = (el.textContent || '').trim(); "
            "if (t) out.push(sel + ': ' + t); } } return out; })()"
        )
        errors = self._eval_json(js, context="verify_no_errors")
        if not isinstance(errors, list):
            return
        if errors:
            raise _check_failure(f"Error indicators found: {errors}")


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
    "AgentBrowserBackend",
    "FlowBackend",
    "FlowExecutionError",
    "PlaywrightBackend",
    "RunCmd",
]
