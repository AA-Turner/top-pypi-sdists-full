import sys
import warnings
from collections.abc import Awaitable, Callable
from typing import Any, NamedTuple

import httpx

from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

_OBO_WARNING = (
    "get_mistral_client() without run_as calls as the deployment in this on_behalf_of workflow; "
    "in v4 the default becomes run_as=RunAs.AUTO, which calls as the executing user. "
    "Pass run_as=RunAs.DEPLOYMENT to keep the current identity, or run_as=RunAs.AUTO to adopt the v4 behavior "
    "(from mistralai.workflows.core.auth import RunAs)."
)
_NO_CONTEXT_WARNING = (
    "get_mistral_client() without run_as was used outside a workflow execution; "
    "in v4 the default becomes run_as=RunAs.AUTO, which raises there. "
    "Pass run_as=RunAs.DEPLOYMENT (from mistralai.workflows.core.auth import RunAs)."
)


class CallSite(NamedTuple):
    filename: str
    lineno: int
    module: str
    registry: dict[Any, Any]


def caller_call_site(depth: int) -> CallSite:
    frame = sys._getframe(depth + 1)
    return CallSite(
        filename=frame.f_code.co_filename,
        lineno=frame.f_lineno,
        module=frame.f_globals.get("__name__", "<unknown>"),
        # Same registry warnings.warn uses, so the default filter shows each call site once.
        registry=frame.f_globals.setdefault("__warningregistry__", {}),
    )


def _warn_if_v4_identity_differs(call_site: CallSite) -> None:
    context = retrieve_context()
    if context is not None and not context.on_behalf_of:
        return
    warnings.warn_explicit(
        _NO_CONTEXT_WARNING if context is None else _OBO_WARNING,
        FutureWarning,
        call_site.filename,
        call_site.lineno,
        module=call_site.module,
        registry=call_site.registry,
    )


def warn_default_identity(call_site: CallSite) -> Callable[[httpx.Request], None]:
    def hook(request: httpx.Request) -> None:
        _warn_if_v4_identity_differs(call_site)

    return hook


def warn_default_identity_async(call_site: CallSite) -> Callable[[httpx.Request], Awaitable[None]]:
    async def hook(request: httpx.Request) -> None:
        _warn_if_v4_identity_differs(call_site)

    return hook
