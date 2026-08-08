"""Health service: liveness, handshake, typed diagnostics."""

from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime
from pathlib import Path

from aiohttp import web

from plato import __version__
from plato.agents.daemon.http_util import ok_response
from plato.agents.daemon.state import DaemonContext
from plato.rpc.models.common import Limits
from plato.rpc.models.health import HandshakeResponse, HealthReport, PingResponse
from plato.rpc.protocol import (
    API_PREFIX,
    CAP_HEALTH_REPORT,
    PROTOCOL_VERSION,
)


async def _healthz(_request: web.Request) -> web.Response:
    # Unauthenticated liveness only — no state, no token. Used by the world's
    # readiness poll before the authenticated handshake.
    return web.json_response({"ok": True})


def _handshake_handler(ctx: DaemonContext):
    async def handshake(request: web.Request) -> web.Response:
        return ok_response(
            request,
            HandshakeResponse(
                protocol_version=PROTOCOL_VERSION,
                server_sdk_version=__version__,
                capabilities=list(ctx.capabilities),
                limits=Limits(),
                daemon_started_at=ctx.started_at,
                state_dir=str(ctx.state_dir),
            ),
        )

    return handshake


async def _ping(request: web.Request) -> web.Response:
    return ok_response(request, PingResponse(ts=datetime.now(UTC)))


def _report_handler(ctx: DaemonContext):
    async def report(request: web.Request) -> web.Response:
        # _collect_report reads /dev/kmsg (up to the whole ring buffer),
        # /proc, and walks the jobs dir — off-loop so a slow read can't
        # freeze the daemon (audit M4).
        return ok_response(request, await asyncio.to_thread(_collect_report, ctx))

    return report


def _collect_report(ctx: DaemonContext) -> HealthReport:
    report = HealthReport(ts=datetime.now(UTC))
    _fill_loadavg(report)
    _fill_meminfo(report)
    _fill_disk(report, ctx.state_dir)
    _fill_dmesg(report)
    _fill_processes(report)
    if ctx.jobs_dir.is_dir():
        report.running_jobs = [p.name for p in ctx.jobs_dir.iterdir() if p.is_dir()]
    return report


def _fill_loadavg(report: HealthReport) -> None:
    try:
        report.load_1m = os.getloadavg()[0]
        with open("/proc/uptime") as fh:
            report.uptime_s = float(fh.read().split()[0])
    except (OSError, ValueError, IndexError):
        pass


def _fill_meminfo(report: HealthReport) -> None:
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                key, _, rest = line.partition(":")
                if key == "MemTotal":
                    report.mem_total_kb = int(rest.split()[0])
                elif key == "MemAvailable":
                    report.mem_available_kb = int(rest.split()[0])
    except (OSError, ValueError, IndexError):
        pass


def _fill_disk(report: HealthReport, path: Path) -> None:
    try:
        stat = os.statvfs(path)
        report.disk_free_bytes = stat.f_bavail * stat.f_frsize
    except OSError:
        pass


def _fill_dmesg(report: HealthReport) -> None:
    # Best-effort; unreadable without privileges on some kernels.
    try:
        with open("/dev/kmsg") as fh:  # pragma: no cover - env dependent
            os.set_blocking(fh.fileno(), False)
            lines = [line.strip() for line in fh.readlines()[-20:]]
            report.dmesg_errors_tail = [ln for ln in lines if ln]
    except OSError:
        pass


def _fill_processes(report: HealthReport) -> None:
    try:
        for pid in os.listdir("/proc"):
            if not pid.isdigit():
                continue
            try:
                with open(f"/proc/{pid}/cmdline", "rb") as fh:
                    cmdline = fh.read().replace(b"\x00", b" ").decode(errors="replace").strip()
            except OSError:
                continue
            if any(marker in cmdline for marker in ("plato-agent-runner", "python", "node")):
                report.agent_processes.append(f"{pid} {cmdline[:120]}")
                if len(report.agent_processes) >= 20:
                    break
    except OSError:
        pass


def register(app: web.Application, ctx: DaemonContext) -> None:
    app.router.add_get("/healthz", _healthz)
    app.router.add_get(f"{API_PREFIX}/handshake", _handshake_handler(ctx))
    app.router.add_get(f"{API_PREFIX}/health/ping", _ping)
    app.router.add_get(f"{API_PREFIX}/health/report", _report_handler(ctx))
    ctx.capabilities.append(CAP_HEALTH_REPORT)
