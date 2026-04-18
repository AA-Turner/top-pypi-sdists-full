"""Execution backends for the async FlowExecutor.

A ``FlowBackend`` is the side-effect surface the executor drives: it knows how
to perform one action (click, fill, navigate, …) against *some* browser. The
executor itself stays environment-agnostic.

Two backends are shipped:

* :class:`PlaywrightBackend` — wraps a Playwright :class:`~playwright.async_api.Page`
  and preserves the executor's historical behaviour byte-for-byte.
* :class:`AgentBrowserBackend` — shells out to the ``agent-browser`` CLI via a
  caller-supplied ``run_cmd`` callable. The callable is the only
  execution-environment abstraction; callers plug in local subprocess, SSH into
  an agent VM, or anything else that can run a shell command.
"""

from __future__ import annotations

import base64
import json
import shlex
from collections.abc import Awaitable, Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from playwright.async_api import Page

    from plato._generated.models import VerifyStep

RunCmd = Callable[[Sequence[str]], Awaitable[tuple[int, str, str]]]
"""Signature for executing a shell command wherever ``agent-browser`` lives.

Takes ``argv`` and returns ``(exit_code, stdout, stderr)``.
"""


class FlowExecutionError(Exception):
    """Raised when a flow step fails."""

    pass


@runtime_checkable
class FlowBackend(Protocol):
    """Protocol every FlowExecutor backend must satisfy."""

    # Nullable args mirror the wire types (`Flow*Step.timeout: int | None`,
    # `should_exist: bool | None`, …). Each backend is responsible for mapping
    # ``None`` to its own notion of "unspecified": Playwright uses its built-in
    # 30s default, agent-browser inherits its CLI default. Widening the
    # Protocol keeps the types honest end-to-end rather than hiding ``None``
    # behind silent fallbacks in the executor.
    async def navigate(self, url: str) -> None: ...
    async def click(self, selector: str, timeout_ms: int | None) -> None: ...
    async def fill(self, selector: str, value: str, timeout_ms: int | None) -> None: ...
    async def wait_for_selector(self, selector: str, timeout_ms: int | None) -> None: ...
    async def wait_for_url(self, url_contains: str, timeout_ms: int | None) -> None: ...
    async def wait(self, duration_ms: int) -> None: ...
    async def current_url(self) -> str: ...
    async def screenshot(self, path: Path, *, full_page: bool | None = False) -> None: ...

    async def check_element(self, selector: str, should_exist: bool | None) -> None: ...
    async def verify(self, step: VerifyStep) -> None: ...
    async def verify_text(self, text: str, should_exist: bool | None) -> None: ...
    async def verify_url(self, url: str, contains: bool | None) -> None: ...
    async def verify_no_errors(self, selectors: list[str]) -> None: ...


class PlaywrightBackend:
    """FlowBackend wrapping a Playwright ``Page`` — historical executor behaviour."""

    def __init__(self, page: Page) -> None:
        self.page = page

    async def navigate(self, url: str) -> None:
        await self.page.goto(url)

    async def click(self, selector: str, timeout_ms: int | None) -> None:
        await self.page.wait_for_selector(selector, timeout=timeout_ms)
        await self.page.click(selector)

    async def fill(self, selector: str, value: str, timeout_ms: int | None) -> None:
        await self.page.wait_for_selector(selector, timeout=timeout_ms)
        await self.page.fill(selector, value)

    async def wait_for_selector(self, selector: str, timeout_ms: int | None) -> None:
        await self.page.wait_for_selector(selector, timeout=timeout_ms)

    async def wait_for_url(self, url_contains: str, timeout_ms: int | None) -> None:
        await self.page.wait_for_function(
            f"window.location.href.includes('{url_contains}')",
            timeout=timeout_ms,
        )

    async def wait(self, duration_ms: int) -> None:
        await self.page.wait_for_timeout(duration_ms)

    async def current_url(self) -> str:
        return self.page.url or ""

    async def screenshot(self, path: Path, *, full_page: bool | None = False) -> None:
        await self.page.screenshot(path=str(path), full_page=bool(full_page))

    async def check_element(self, selector: str, should_exist: bool | None) -> None:
        element = await self.page.query_selector(selector)
        exists = element is not None
        if bool(should_exist) == exists:
            return
        raise _check_failure(f"Element check failed: {selector} (expected: {should_exist}, found: {exists})")

    async def verify(self, step: VerifyStep) -> None:  # noqa: C901 — dispatch table
        vt = step.verify_type
        verify_key = vt.value if hasattr(vt, "value") else vt
        key = str(verify_key)
        if key == "element_exists":
            try:
                element = await self.page.query_selector(step.selector) if step.selector else None
                if element:
                    return
                raise _check_failure(f"Element not found: {step.selector}")
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "element_visible":
            try:
                element = await self.page.query_selector(step.selector) if step.selector else None
                if element and await element.is_visible():
                    return
                raise _check_failure(f"Element not visible: {step.selector}")
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "element_text":
            try:
                element = await self.page.query_selector(step.selector) if step.selector else None
                if not element:
                    raise _check_failure(f"Element not found: {step.selector}")
                actual_text = await element.text_content() or ""
                _assert_text(step, actual_text)
                return
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "element_count":
            try:
                elements = await self.page.query_selector_all(step.selector) if step.selector else []
                if len(elements) == step.count:
                    return
                raise _check_failure(f"Expected {step.count} elements, found {len(elements)}")
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {step.selector} - {e}") from e
        if key == "page_title":
            try:
                actual_title = await self.page.title()
                _assert_title(step, actual_title)
                return
            except FlowExecutionError:
                raise
            except Exception as e:
                raise _check_failure(f"Verification error: {e}") from e
        raise _check_failure(f"Unknown verification type: {step.verify_type}")

    async def verify_text(self, text: str, should_exist: bool | None) -> None:
        content = await self.page.content()
        found = text in content
        if should_exist and not found:
            raise _check_failure(f"Text '{text}' not found on page")
        if not should_exist and found:
            raise _check_failure(f"Text '{text}' found (should not exist)")

    async def verify_url(self, url: str, contains: bool | None) -> None:
        actual = self.page.url
        if contains:
            if url not in actual:
                raise _check_failure(f"URL '{actual}' does not contain '{url}'")
        else:
            if url != actual:
                raise _check_failure(f"URL '{actual}' does not match '{url}'")

    async def verify_no_errors(self, selectors: list[str]) -> None:
        errors_found: list[str] = []
        for selector in selectors or []:
            for element in await self.page.query_selector_all(selector):
                if await element.is_visible():
                    text = await element.text_content()
                    if text and text.strip():
                        errors_found.append(f"{selector}: {text.strip()}")
        if errors_found:
            raise _check_failure(f"Error indicators found: {errors_found}")


class AgentBrowserBackend:
    """FlowBackend that drives the ``agent-browser`` CLI via a ``run_cmd`` callable.

    The backend emits one CLI invocation per step and relies on ``agent-browser``
    keeping browser state alive across calls through its daemon (one daemon per
    ``AGENT_BROWSER_SESSION``). Callers are responsible for setting
    ``AGENT_BROWSER_SESSION`` in the environment where ``run_cmd`` executes, so
    the correct session is used.

    Parameters
    ----------
    run_cmd:
        Async callable ``argv -> (exit_code, stdout, stderr)`` — the only
        abstraction over where ``agent-browser`` runs.
    binary:
        Name or absolute path of the ``agent-browser`` executable on the target
        host. Defaults to ``"agent-browser"`` (resolved via PATH).
    session:
        Optional session name. When set, the backend prepends
        ``--session <session>`` to every call. Leave ``None`` to defer to the
        ``AGENT_BROWSER_SESSION`` env var in the caller's shell.
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

    async def _ab(self, *args: str) -> tuple[int, str, str]:
        argv: list[str] = [self._binary]
        if self._session is not None:
            argv += ["--session", self._session]
        argv.extend(args)
        return await self._run_cmd(argv)

    async def _run_checked(self, *args: str, context: str) -> str:
        rc, stdout, stderr = await self._ab(*args)
        if rc != 0:
            cmd_repr = " ".join(shlex.quote(a) for a in args)
            raise _check_failure(
                f"{context} failed ({cmd_repr}): rc={rc} stdout={stdout[-400:]!r} stderr={stderr[-400:]!r}"
            )
        return stdout

    async def navigate(self, url: str) -> None:
        await self._run_checked("open", url, context="navigate")

    @staticmethod
    def _timeout_args(timeout_ms: int | None) -> tuple[str, ...]:
        """``None`` → use agent-browser's built-in default: omit the flag."""
        return () if timeout_ms is None else ("--timeout", str(timeout_ms))

    async def click(self, selector: str, timeout_ms: int | None) -> None:
        # Resolve the selector first so transient DOM mounts don't race the click.
        await self._run_checked("wait", selector, *self._timeout_args(timeout_ms), context="click/wait")
        await self._run_checked("click", selector, context="click")

    async def fill(self, selector: str, value: str, timeout_ms: int | None) -> None:
        await self._run_checked("wait", selector, *self._timeout_args(timeout_ms), context="fill/wait")
        await self._run_checked("fill", selector, value, context="fill")

    async def wait_for_selector(self, selector: str, timeout_ms: int | None) -> None:
        await self._run_checked(
            "wait",
            selector,
            *self._timeout_args(timeout_ms),
            context="wait_for_selector",
        )

    async def wait_for_url(self, url_contains: str, timeout_ms: int | None) -> None:
        # agent-browser's `wait --url` wants a glob, not a substring. Use --fn
        # with location.href.includes(...) to match the Playwright backend.
        expr = f"window.location.href.includes({json.dumps(url_contains)})"
        await self._run_checked(
            "wait",
            "--fn",
            expr,
            *self._timeout_args(timeout_ms),
            context="wait_for_url",
        )

    async def wait(self, duration_ms: int) -> None:
        await self._run_checked("wait", str(duration_ms), context="wait")

    async def current_url(self) -> str:
        stdout = await self._run_checked("eval", "--json", "window.location.href", context="current_url")
        stripped = stdout.strip()
        if not stripped:
            return ""
        # agent-browser --json wraps eval output; fall back to raw text.
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

    async def screenshot(self, path: Path, *, full_page: bool | None = False) -> None:
        args = ["screenshot", str(path)]
        if full_page:
            args.append("--full")
        await self._run_checked(*args, context="screenshot")

    async def _eval_json(self, js: str, *, context: str):
        """Evaluate JS in the page and return the parsed JSON result."""
        script_b64 = base64.b64encode(js.encode("utf-8")).decode("ascii")
        stdout = await self._run_checked("eval", "--json", "--base64", script_b64, context=context)
        stripped = stdout.strip()
        if not stripped:
            return None
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as e:
            raise _check_failure(f"{context} returned non-JSON output: {stripped[-200:]!r}") from e
        # agent-browser wraps results as {"result": ...} (and sometimes more).
        if isinstance(payload, dict):
            for key in ("result", "value", "output"):
                if key in payload:
                    return payload[key]
        return payload

    async def check_element(self, selector: str, should_exist: bool | None) -> None:
        js = "(() => document.querySelector(" + json.dumps(selector) + ") !== null)()"
        exists = bool(await self._eval_json(js, context="check_element"))
        if should_exist and not exists:
            raise _check_failure(f"Element missing: {selector}")
        if not should_exist and exists:
            raise _check_failure(f"Element present but should be absent: {selector}")

    async def verify(self, step: VerifyStep) -> None:
        vt = step.verify_type
        verify_key = vt.value if hasattr(vt, "value") else vt
        key = str(verify_key)
        if key == "element_exists":
            if not step.selector:
                raise _check_failure("verify(element_exists) missing selector")
            await self.check_element(step.selector, should_exist=True)
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
            visible = bool(await self._eval_json(js, context="verify_element_visible"))
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
            actual = await self._eval_json(js, context="verify_element_text")
            if actual is None:
                raise _check_failure(f"Element not found: {step.selector}")
            _assert_text(step, str(actual))
            return
        if key == "element_count":
            if not step.selector:
                raise _check_failure("verify(element_count) missing selector")
            js = "document.querySelectorAll(" + json.dumps(step.selector) + ").length"
            count = int(await self._eval_json(js, context="verify_element_count") or 0)
            if count != step.count:
                raise _check_failure(f"Expected {step.count} elements, found {count}")
            return
        if key == "page_title":
            title = await self._eval_json("document.title", context="verify_page_title")
            _assert_title(step, str(title or ""))
            return
        raise _check_failure(f"Unknown verification type: {step.verify_type}")

    async def verify_text(self, text: str, should_exist: bool | None) -> None:
        js = "(document.documentElement && document.documentElement.outerHTML) || ''"
        content = str(await self._eval_json(js, context="verify_text") or "")
        found = text in content
        if should_exist and not found:
            raise _check_failure(f"Text '{text}' not found on page")
        if not should_exist and found:
            raise _check_failure(f"Text '{text}' found but should be absent")

    async def verify_url(self, url: str, contains: bool | None) -> None:
        actual = await self.current_url()
        if contains:
            if url not in actual:
                raise _check_failure(f"URL '{actual}' does not contain '{url}'")
        else:
            if url != actual:
                raise _check_failure(f"URL '{actual}' does not match '{url}'")

    async def verify_no_errors(self, selectors: list[str]) -> None:
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
        errors = await self._eval_json(js, context="verify_no_errors")
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


def make_ssh_run_cmd(
    *,
    ssh_key_path: Path,
    hostname: str,
    shell_prefix: str = "",
    timeout: int = 120,
    extra_opts: list[tuple[str, str]] | None = None,
) -> RunCmd:
    """Build a :data:`RunCmd` that SSHes into ``hostname`` for each invocation.

    Each call shells into the target and runs one command — typical usage is
    pairing this with :class:`AgentBrowserBackend` when ``agent-browser`` lives
    on a remote VM (e.g. a claude-code agent runtime).

    Parameters
    ----------
    ssh_key_path:
        Private key used for the SSH connection.
    hostname:
        SSH target. Format depends on the caller's SSH config (direct
        mesh DNS, gateway + ProxyCommand, etc.).
    shell_prefix:
        Optional shell fragment prepended via ``&&`` before the quoted command
        — use this to export PATH or activate a venv on the remote host when
        the non-interactive login shell doesn't pick it up automatically. The
        SDK doesn't know or care what the prefix contains; callers provide
        image-specific fixes.
    timeout:
        Per-call SSH timeout in seconds.
    extra_opts:
        ``(name, value)`` tuples forwarded to ``ssh -o``. Needed when reaching
        the target through the Plato gateway from a dev machine (the
        ProxyCommand is not in the default SSH config).
    """
    from plato.utils.subprocess import run_ssh

    async def _run(argv: Sequence[str]) -> tuple[int, str, str]:
        quoted = " ".join(shlex.quote(a) for a in argv)
        command = f"{shell_prefix} && {quoted}" if shell_prefix else quoted
        return await run_ssh(
            ssh_key_path,
            hostname,
            command,
            timeout=timeout,
            extra_opts=extra_opts,
        )

    return _run


__all__ = [
    "AgentBrowserBackend",
    "FlowBackend",
    "FlowExecutionError",
    "PlaywrightBackend",
    "RunCmd",
    "make_ssh_run_cmd",
]
