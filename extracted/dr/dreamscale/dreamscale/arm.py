"""Connection helpers shared by the sim runners and bench: the pinned QUIC connect,
the UDP preflight adapter, and the background event-loop runner."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

from dreamscale import errors
from dreamscale.control import Session
from dreamscale.policy.lifecycle import _LoopRunner

__all__ = ["_LoopRunner", "_compatible_diagnose_udp", "_default_transport_connect", "_pin_connect"]


def _default_transport_connect(addr: str, port: int, *, cert_fingerprint: str,
                               session_id: str, session_token: str):
    from dreamscale_transport import QuicClient

    return QuicClient.connect(addr, port, cert_fingerprint=cert_fingerprint,
                              session_id=session_id, session_token=session_token)


def _compatible_diagnose_udp(preflight_fn: Callable[..., Any]) -> Callable[..., Any]:
    async def diagnose(addr: str, port: int, **kwargs):
        call_kwargs = _accepted_preflight_kwargs(preflight_fn, kwargs)
        result = preflight_fn(addr, port, **call_kwargs)
        if inspect.isawaitable(result):
            result = await result
        return _as_udp_reachability_report(result)

    return diagnose


def _accepted_preflight_kwargs(preflight_fn: Callable[..., Any],
                               kwargs: dict[str, Any]) -> dict[str, Any]:
    try:
        params = inspect.signature(preflight_fn).parameters
    except (TypeError, ValueError):
        return kwargs
    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in params.values()):
        return kwargs
    return {key: value for key, value in kwargs.items() if key in params}


def _as_udp_reachability_report(result: Any) -> Any:
    if hasattr(result, "ok") and hasattr(result, "worker"):
        return result
    if not hasattr(result, "status"):
        return result
    from dreamscale_transport import PreflightResult, UdpReachabilityReport

    status = result.status
    remediation = getattr(result, "remediation", "")
    reason = "ok"
    if status == "udp_blocked":
        reason = "udp_refused"
    elif status != "ok":
        reason = "data_plane_unreachable"
    return UdpReachabilityReport(
        worker=PreflightResult(status=status, remediation=remediation),
        diagnostic=None,
        reason=reason,
        remediation="" if status == "ok" else remediation,
    )


async def _pin_connect(transport_connect, session: Session):
    try:
        return await transport_connect(
            session.worker_addr, session.port,
            cert_fingerprint=session.cert_fingerprint,
            session_id=session.session_id,
            session_token=session.session_token,
        )
    except errors.DreamscaleError:
        raise
    except Exception as exc:
        text = str(exc).lower()
        if "fingerprint" in text or "pin" in text:
            raise errors.catalog("cert_fingerprint_mismatch") from exc
        raise
