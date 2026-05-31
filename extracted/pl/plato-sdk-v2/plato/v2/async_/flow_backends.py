"""Execution backends for the async FlowExecutor.

A ``FlowBackend`` is the side-effect surface the executor drives: it knows
how to perform one action (click, fill, navigate, …) against *some* browser.
The executor itself stays environment-agnostic.

For cases where the browser lives on a remote VM (e.g. an agent runtime), pair
:func:`make_ssh_run_cmd` with
:func:`plato.v2.async_.cdp_bridge.shared_cdp_chromium` to expose the remote
chromium over CDP, then drive it with :class:`PlaywrightBackend` as usual.
"""

from __future__ import annotations

import shlex
from collections.abc import Awaitable, Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from plato.utils.subprocess import run_ssh

if TYPE_CHECKING:
    from playwright.async_api import Page

    from plato._generated.models import VerifyStep

RunCmd = Callable[[Sequence[str]], Awaitable[tuple[int, str, str]]]
"""Signature for executing a shell command on the target host.

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


CLAUDE_CODE_SSH_SHELL_PREFIX = (
    'export PATH="$HOME/.nvm/versions/node/$(ls $HOME/.nvm/versions/node/ | '
    'head -1)/bin:$HOME/.bun/bin:/usr/local/bin:$PATH"'
)
"""``shell_prefix`` for reaching ``agent-browser`` over non-interactive SSH on
the claude-code / gemini-cli / codex base images.

Inside an interactive agent subshell, ``plato.agents.browser_tooling``'s
``AGENT_BROWSER_PATH_EXPORT`` is enough because nvm.sh is already sourced.
Over SSH the non-interactive shell doesn't source nvm, so we hand-roll the
absolute node bin dir via ``ls | head -1`` in addition to adding
``$HOME/.bun/bin``. Callers on other images should pass their own
``shell_prefix``.
"""


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
    pairing this with :func:`plato.v2.async_.cdp_bridge.shared_cdp_chromium`
    to bring up a CDP-reachable chromium on a remote agent VM.

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
    "CLAUDE_CODE_SSH_SHELL_PREFIX",
    "FlowBackend",
    "FlowExecutionError",
    "PlaywrightBackend",
    "RunCmd",
    "make_ssh_run_cmd",
]
