from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any, Literal

from dreamscale import errors

log = logging.getLogger(__name__)
REPORT_TRANSPORT_TIMEOUT_S = 2.0

NoticeStyle = Literal["cli", "cli_transport", "sdk"]

CLI_FALLBACK_NOTICE = (
    "QUIC/UDP is unavailable on this network; using HTTPS fallback.",
    "Motion may feel less responsive while using fallback.",
    "To require QUIC only, re-run with --no-fallback.",
)

SDK_FALLBACK_NOTICE = (
    "QUIC/UDP is unavailable on this network; using HTTPS fallback.",
    "Motion may feel less responsive while using fallback.",
    'To require QUIC only, pass transport="quic".',
)

CLI_TRANSPORT_FALLBACK_NOTICE = (
    "QUIC/UDP is unavailable on this network; using HTTPS fallback.",
    "Motion may feel less responsive while using fallback.",
    "To require QUIC only, re-run with --transport quic.",
)

WORKER_PATH_NOTICE = (
    "The assigned compute did not respond over QUIC/UDP.",
    "Using HTTPS fallback while Dreamscale routes around the issue.",
    "To require QUIC only, re-run with --no-fallback.",
)


def _validate_notice_style(notice_style: str) -> NoticeStyle:
    if notice_style not in ("cli", "cli_transport", "sdk"):
        raise ValueError('notice_style must be "cli", "cli_transport", or "sdk"')
    return notice_style


def _diagnostic_preflight_status(report: Any) -> str | None:
    return report.diagnostic.status if report.diagnostic is not None else None


def _notice_lines(reason: str, *, notice_style: NoticeStyle) -> tuple[str, str, str]:
    if reason == "worker_udp_unreachable" and notice_style == "cli":
        return WORKER_PATH_NOTICE
    if notice_style == "sdk":
        return SDK_FALLBACK_NOTICE
    if notice_style == "cli_transport":
        return CLI_TRANSPORT_FALLBACK_NOTICE
    return CLI_FALLBACK_NOTICE


async def _report_transport_best_effort(
    report_transport_fn: Callable[..., Awaitable[None]] | None,
    session_id: str,
    **metadata: Any,
) -> None:
    if report_transport_fn is None:
        return
    try:
        await asyncio.wait_for(
            report_transport_fn(session_id, **metadata),
            timeout=REPORT_TRANSPORT_TIMEOUT_S,
        )
    except Exception:
        log.debug("failed to report selected transport", exc_info=True)


async def connect_selected_transport(
    session: Any,
    *,
    diagnose_udp_fn: Callable[..., Awaitable[Any]],
    quic_connect: Callable[[Any], Awaitable[Any]],
    relay_connect: Callable[[Any], Awaitable[Any]],
    allow_fallback: bool,
    on_line: Callable[[str], None],
    notice_style: NoticeStyle = "cli",
    diagnostic_addr: str | None = None,
    diagnostic_port: int | None = None,
    report_transport_fn: Callable[..., Awaitable[None]] | None = None,
) -> Any:
    notice_style = _validate_notice_style(notice_style)
    report = await diagnose_udp_fn(
        session.worker_addr,
        session.port,
        diagnostic_addr=diagnostic_addr,
        diagnostic_port=diagnostic_port,
    )
    if report.ok:
        try:
            transport = await quic_connect(session)
        except errors.DreamscaleError:
            raise
        except Exception:
            if not allow_fallback:
                raise
            fallback_reason = "quic_connect_failed"
        else:
            transport.mode = getattr(transport, "mode", "quic")
            transport.fallback_reason = None
            transport.primary_preflight_status = report.worker.status
            transport.diagnostic_preflight_status = _diagnostic_preflight_status(report)
            await _report_transport_best_effort(
                report_transport_fn,
                session.session_id,
                transport_protocol="quic",
                fallback_used=False,
                primary_preflight_status=report.worker.status,
                diagnostic_preflight_status=_diagnostic_preflight_status(report),
            )
            return transport
    else:
        fallback_reason = report.reason

    if not allow_fallback:
        raise errors.catalog("data_plane_unreachable", remediation=report.remediation)

    transport = await relay_connect(session)
    transport.mode = getattr(transport, "mode", "relay")
    transport.fallback_reason = fallback_reason
    transport.primary_preflight_status = report.worker.status
    transport.diagnostic_preflight_status = _diagnostic_preflight_status(report)
    await _report_transport_best_effort(
        report_transport_fn,
        session.session_id,
        transport_protocol="relay",
        fallback_used=True,
        fallback_reason=fallback_reason,
        primary_preflight_status=report.worker.status,
        diagnostic_preflight_status=_diagnostic_preflight_status(report),
    )
    for line in _notice_lines(fallback_reason, notice_style=notice_style):
        on_line(line)
    return transport
