"""run a sync tool body off the event loop: re-check its arguments, admit it, bound and word its errors."""

from __future__ import annotations
import functools
import inspect
import time
from collections.abc import Callable
from typing import Any, get_type_hints

import anyio
import anyio.to_thread
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import CallToolResult, TextContent
from pydantic_core import to_jsonable_python
from pydantic import BaseModel, create_model
from ...sdk import errors
from ...sdk.settings import workspace_limit
from ...foundation.request_identity.surface import tool_scope
from ..delivery import accounting, delivery as continuation
from ...foundation.token_budget.token_budget import serialize
from probe.mcp.server.limits import _QUEUE_TIMEOUT_S, _QUEUE_WARN_S, _WEB_TOOLS, _limiters, _web_limiter
from probe.mcp.server.pool import _logger, _token_fingerprint, _token_var


def _view_default(fn: Callable[..., Any]) -> Any:
    """The tool's default `view`, or None if it takes no `view` argument.

    Resolved ONCE per tool at decoration time. A caller that omits `view` still gets
    the default served, so reading only the passed kwargs would file the majority of
    get_entity traffic under no view at all -- and `card` is exactly the common
    shape worth seeing. inspect.signature is too expensive to run per call.
    """
    try:
        param = inspect.signature(fn).parameters.get("view")
    except (TypeError, ValueError):
        return None
    if param is None or param.default is inspect.Parameter.empty:
        return None
    return param.default


def _argument_validator(fn: Callable[..., Any]) -> Callable[[dict], dict]:
    """Re-check a call's arguments against the tool's own signature.

    A continuation may leave out arguments its cursor carries
    (`continuation.resume`). The carried values are JSON, so they are run
    through the same annotations FastMCP validated the caller's values with:
    the source gets `View.TRANSCRIPT`, not the string, and a hand-made cursor
    cannot carry a value the schema would have refused. Built on first use --
    most calls never fill an argument from a cursor.
    """
    model: type[BaseModel] | None = None

    def validate(arguments: dict) -> dict:
        nonlocal model
        if model is None:
            hints = get_type_hints(fn, include_extras=True)
            model = create_model(
                f"{fn.__name__}_arguments",
                **{
                    name: (
                        hints.get(name, Any),
                        ... if param.default is inspect.Parameter.empty else param.default,
                    )
                    for name, param in inspect.signature(fn).parameters.items()
                },
            )
        # Iterating a model yields its fields without reading a deprecated one
        # through its warning descriptor (entity's `filters`).
        return {name: value for name, value in model.model_validate(arguments) if name in arguments}

    return validate


def _refusal_text(exc: errors.LimitReachedError) -> str:
    """The server's refusal sentence, plus its `hint` when it sent one.

    `str(exc)` is only `detail.message`. SQL's retention refusal puts the part
    an agent can ACT on -- which tools still work -- in `detail.hint`, and
    without it the agent reads a bare refusal and retries.
    """
    text = str(exc)
    hint = exc.detail.get("hint") if isinstance(exc.detail, dict) else None
    if isinstance(hint, str) and hint and hint not in text:
        text = f"{text} {hint}"
    return text


def _tool(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Run a sync tool body on a worker thread so the event loop — and the
    /healthz endpoint the kubelet probes — stays responsive.

    FastMCP dispatches sync tools INLINE on the event loop (mcp
    func_metadata.call_fn_with_arg_validation is a bare ``fn(...)``), and every
    tool here does a blocking backend round-trip bounded only by the SDK's
    30s-per-attempt retry budget. One slow call therefore froze the whole
    process — the 2026-07-30 liveness-kill incident.

    ``functools.wraps`` preserves the signature and annotations FastMCP reads
    to build the tool schema; tests pin the schemas byte-for-byte so that
    contract is verified, not assumed. Contextvars (the caller's token,
    tool_scope) propagate into the worker thread — anyio runs the function in
    the calling task's context copy.

    Admission: waiting past _QUEUE_WARN_S logs a saturation breadcrumb;
    waiting past _QUEUE_TIMEOUT_S sheds the call with a retryable
    "overloaded" error instead of queueing toward the ingress timeout."""

    view_default = _view_default(fn)
    accepted = inspect.signature(fn).parameters
    defaults = {
        name: param.default
        for name, param in accepted.items()
        if param.default is not inspect.Parameter.empty
    }
    validate = _argument_validator(fn)

    # A tool `description` is a BUDGET and a schema is not: Claude Code slices
    # MCP descriptions at 2,048 chars and passes `input_schema` verbatim. Python
    # 3.13 dedents docstrings at compile time but 3.11/3.12 do not, and the
    # deployed image is 3.12 -- so on the interpreter that actually serves
    # agents, ~11% of every description was leading whitespace, spending budget
    # to deliver indentation. cleandoc here makes the wire text identical on
    # every interpreter and hands that 11% back as room for words.
    if fn.__doc__:
        fn.__doc__ = inspect.cleandoc(fn.__doc__)

    @functools.wraps(fn)
    async def _threaded(*args: Any, **kwargs: Any) -> Any:
        admission, thread_permit = _limiters()
        # The open-web sub-quota (see `_WEB_CAPACITY_FRACTION`). Acquired FIRST
        # and released last, so a web burst queues on its own share instead of
        # holding general admission slots while it waits for one -- taking
        # admission first would let 16 web calls own the pool merely by waiting.
        web_slot = _web_limiter() if fn.__name__ in _WEB_TOOLS else None
        start = time.monotonic()
        if web_slot is not None:
            try:
                with anyio.fail_after(_QUEUE_TIMEOUT_S):
                    await web_slot.acquire()
            except TimeoutError:
                _logger.warning(
                    "tool %s SHED after %.0fs waiting on the open-web sub-quota "
                    "(%d slots; token %s)",
                    fn.__name__,
                    _QUEUE_TIMEOUT_S,
                    int(web_slot.total_tokens),
                    _token_fingerprint(),
                )
                # Named distinctly from the general shed so the two are
                # separable in logs: this one means "too much browsing at once",
                # which is a different operational fact from "the pod is busy".
                raise ToolError(
                    f"too many open-web reads in flight: waited "
                    f"{_QUEUE_TIMEOUT_S:.0f}s for one of "
                    f"{int(web_slot.total_tokens)} web slots. Other Probe tools "
                    "are unaffected; retry this one shortly."
                ) from None
        try:
            with anyio.fail_after(_QUEUE_TIMEOUT_S):
                await admission.acquire()
        except TimeoutError:
            # The shed is the strongest overload signal this process has —
            # every probe stays green while it happens — so it MUST log.
            _logger.warning(
                "tool %s SHED after %.0fs queue wait (pool saturated; token %s)",
                fn.__name__,
                _QUEUE_TIMEOUT_S,
                _token_fingerprint(),
            )
            if web_slot is not None:
                web_slot.release()
            raise ToolError(
                f"server overloaded: waited {_QUEUE_TIMEOUT_S:.0f}s for a free "
                "worker thread; retry shortly"
            ) from None
        try:
            waited = time.monotonic() - start
            if waited >= _QUEUE_WARN_S:
                _logger.warning(
                    "tool %s waited %.1fs for a worker thread (pool saturated; token %s)",
                    fn.__name__,
                    waited,
                    _token_fingerprint(),
                )

            def _invoke() -> Any:
                # tool_scope rides inside the worker thread's context copy, so
                # the tool bodies no longer repeat their own name.
                #
                # note_tool goes the OTHER way, out of that copy: the hosted ASGI
                # wrapper needs the tool name to label its byte count, and this
                # thread's context is a copy, so rebinding a ContextVar here would
                # be invisible to it. It mutates a dict the wrapper still holds a
                # reference to. No-op under stdio, where no holder is bound.
                accounting.note_tool(fn.__name__)
                # A continuation may leave out the arguments its cursor carries:
                # FastMCP has already put the defaults in, so this is where the
                # cursor's values replace them -- before the view is counted and
                # before the cursor's binding is checked against them.
                arguments = continuation.resume(kwargs, defaults, validate)
                # get_entity is two cost shapes under one name -- bounded row views
                # and complete document reads. Without this they are one
                # indistinguishable row. None for every tool that takes no `view`.
                accounting.note_view(arguments.get("view", view_default))
                # The read's ids (refs given by slug or name are only counted),
                # so a search joins to what was opened from it. None for every
                # tool that takes no `refs`.
                accounting.note_refs(arguments.get("refs"))
                with tool_scope(fn.__name__):

                    def read(passed: dict) -> dict:
                        value = fn(*args, **{k: v for k, v in passed.items() if k in accepted})
                        return to_jsonable_python(value)

                    result = continuation.invoke(
                        fn.__name__,
                        arguments,
                        read,
                        _token_var.get() or "stdio",
                        defaults=defaults,
                    )
                    # Explicit content bypasses FastMCP's pretty JSON conversion.
                    return CallToolResult(
                        content=[TextContent(type="text", text=serialize(result))]
                    )

            try:
                return await anyio.to_thread.run_sync(_invoke, limiter=thread_permit)
            except errors.LimitReachedError as exc:
                # A plan refusal is NOT a failure, and the difference matters
                # more here than anywhere else. The agent reading this is inside
                # the researcher's editor, and a raw 402 reads to it as a broken
                # tool -- so it retries, burns the rest of an allowance that is
                # already spent, and finally reports that Probe is down.
                #
                # One sentence, the server's own, which already ends with the
                # CTA. Nothing is appended: the server writes the copy once so
                # every client says the same thing, and a second locally-worded
                # line would be the same drift the CLI printer already had.
                raise ToolError(_refusal_text(exc)) from None
        finally:
            admission.release()
            if web_slot is not None:
                web_slot.release()

    return _threaded


def _limit_hint(exc: BaseException) -> str:
    """`(hidden by this computer's workspace limit: ...)` when a 404 somewhere in
    `exc`'s chain was answered under the caller's workspace limit (the API's
    `X-Probe-Workspace-Limit-Applied` echo, `RosError.workspace_limit_applied`)."""
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        applied = getattr(current, "workspace_limit_applied", None)
        if isinstance(applied, str) and applied:
            return workspace_limit.hidden_hint(applied)
        current = current.__cause__ or current.__context__
    return ""


def _bounded_error_text(exc: BaseException, limit: int = 600) -> str:
    """A tool error's text, at most `limit` characters -- and, when the caller's
    workspace limit hid what was asked for, saying so (kept whole, never the part
    the bound cuts): an agent reads a silent miss as data loss."""
    message = str(exc)
    hint = _limit_hint(exc)
    if hint:
        body = message.replace(hint, "").strip()
        message = f"{body[: max(0, limit - len(hint) - 1)].rstrip()} {hint}".strip()
    return message[:limit].encode("utf-8", errors="replace").decode("utf-8") or "Probe MCP read failed."
