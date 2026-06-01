"""
Kytte SDK Diagnostics — error codes, startup banner, and health checks.

Every SDK warning/error has a unique code (AIGIE-XNNN) with:
- What happened
- What the consequence is
- How to fix it

Categories:
    C = Configuration (C001-C099)
    N = Network (N001-N099)
    A = Auth / License (A001-A099)
    I = Init / Dependencies (I001-I099)
    R = Runtime (R001-R099)
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DiagnosticMessage:
    """A structured diagnostic message with error code."""

    code: str
    message: str
    consequence: str
    fix: str


def format_diagnostic(msg: DiagnosticMessage, extra: str | None = None) -> str:
    """Format a diagnostic message for logging.

    Output: [AIGIE-C001] Message: extra. Consequence. Fix: how to fix.
    """
    parts = [f"[{msg.code}] {msg.message}"]
    if extra:
        parts[0] += f": {extra}"
    parts.append(f"{msg.consequence}.")
    parts.append(f"Fix: {msg.fix}")
    return ". ".join(parts)


# ── Configuration Codes ──────────────────────────────────────────────

_C001 = DiagnosticMessage(
    code="AIGIE-C001",
    message="No platform URL configured",
    consequence="Traces will not be sent to the Kytte platform",
    fix="Set KYTTE_URL env var or pass aigie_url= to Aigie()",
)

_C002 = DiagnosticMessage(
    code="AIGIE-C002",
    message="No authentication token configured",
    consequence="Platform features inactive, data will not be sent",
    fix="Set KYTTE_TOKEN env var or pass kytte_token= to Aigie()",
)

_C003 = DiagnosticMessage(
    code="AIGIE-C003",
    message="No URL and no token configured",
    consequence="SDK running in local-only mode, no data sent to platform",
    fix="Set KYTTE_URL and KYTTE_TOKEN env vars, or pass them to Aigie()",
)

# ── Network Codes ────────────────────────────────────────────────────

_N001 = DiagnosticMessage(
    code="AIGIE-N001",
    message="Gateway WebSocket connection failed",
    consequence="SDK will operate in local-only mode (no real-time validation)",
    fix="Check that your platform URL is reachable and KYTTE_TOKEN is valid",
)

_N002 = DiagnosticMessage(
    code="AIGIE-N002",
    message="Backend API unreachable",
    consequence="Events buffered locally, will retry automatically",
    fix="Check network connectivity to your Kytte platform URL",
)

_N003 = DiagnosticMessage(
    code="AIGIE-N003",
    message="Batch ingestion failed",
    consequence="Events saved to offline storage for later retry",
    fix="Check platform URL and network connectivity. Events will be retried automatically",
)

_N004 = DiagnosticMessage(
    code="AIGIE-N004",
    message="Backend connection failed during init",
    consequence="Operating in local-only mode (interception works, no backend consultation)",
    fix="Check that your platform URL is reachable",
)

_N005 = DiagnosticMessage(
    code="AIGIE-N005",
    message="Circuit breaker opened",
    consequence="Requests will be short-circuited until backend recovers",
    fix="Backend may be overloaded or down. SDK will auto-retry after cooldown",
)

_N006 = DiagnosticMessage(
    code="AIGIE-N006",
    message="Request failed after all retries exhausted",
    consequence="This request's data was lost",
    fix="Check backend health and network connectivity",
)

_N007 = DiagnosticMessage(
    code="AIGIE-N007",
    message="Gateway reconnection attempts exhausted",
    consequence="Real-time validation disabled until next SDK restart",
    fix="Check that your platform URL is reachable and supports WebSocket connections",
)

# ── Auth / License Codes ─────────────────────────────────────────────

_A001 = DiagnosticMessage(
    code="AIGIE-A001",
    message="License expired",
    consequence="SDK operating in degraded mode (tracing continues, data not sent)",
    fix="Renew your license at https://app.aigie.io or contact support@aigie.io",
)

_A002 = DiagnosticMessage(
    code="AIGIE-A002",
    message="License revoked",
    consequence="SDK operating in degraded mode (tracing continues, data not sent)",
    fix="Contact support@aigie.io to resolve license issues",
)

_A003 = DiagnosticMessage(
    code="AIGIE-A003",
    message="License validation failed",
    consequence="SDK operating in degraded mode",
    fix="Check your KYTTE_TOKEN is valid, or contact support@aigie.io",
)

_A004 = DiagnosticMessage(
    code="AIGIE-A004",
    message="License server unreachable",
    consequence="Using cached license info (if available), will retry",
    fix="Check network connectivity to the license server",
)

# ── Init / Dependency Codes ──────────────────────────────────────────

_I001 = DiagnosticMessage(
    code="AIGIE-I001",
    message="Optional dependency not installed: zstandard",
    consequence="Compression disabled, expect higher bandwidth usage",
    fix="Install with: pip install aigie[compression]",
)

_I002 = DiagnosticMessage(
    code="AIGIE-I002",
    message="Optional dependency not installed: websockets",
    consequence="Gateway real-time validation disabled",
    fix="Install with: pip install aigie (websockets is a core dependency, reinstall the package)",
)

_I003 = DiagnosticMessage(
    code="AIGIE-I003",
    message="Autonomous features initialization failed",
    consequence="SDK works but without autonomous mode capabilities",
    fix="Check logs with AIGIE_LOG_LEVEL=DEBUG for details",
)

_I004 = DiagnosticMessage(
    code="AIGIE-I004",
    message="SDK initialization failed",
    consequence="Will retry automatically on first use",
    fix="Set KYTTE_URL and KYTTE_TOKEN correctly. Enable debug with AIGIE_LOG_LEVEL=DEBUG",
)

_I005 = DiagnosticMessage(
    code="AIGIE-I005",
    message="SDK initialized successfully",
    consequence="All subsystems operational",
    fix="No action needed",
)

_I006 = DiagnosticMessage(
    code="AIGIE-I006",
    message="SDK initialized with warnings",
    consequence="Some subsystems unavailable — tracing still active",
    fix="Check warnings above for details",
)

# ── Runtime Codes ────────────────────────────────────────────────────

_R001 = DiagnosticMessage(
    code="AIGIE-R001",
    message="Batch send failed",
    consequence="Events will be retried or saved to offline storage",
    fix="Check network connectivity and platform health",
)

_R002 = DiagnosticMessage(
    code="AIGIE-R002",
    message="Failed to serialize event payload",
    consequence="This batch of events will be dropped",
    fix="Check for non-serializable objects in trace/span data (e.g., bytes, custom classes)",
)

_R003 = DiagnosticMessage(
    code="AIGIE-R003",
    message="Buffer overflow",
    consequence="Oldest events dropped to make room for new ones",
    fix="Increase batch_size or reduce flush_interval in Config, or check if backend is slow",
)

_R004 = DiagnosticMessage(
    code="AIGIE-R004",
    message="Offline storage error",
    consequence="Buffered events may be lost if the process exits",
    fix="Check disk space and write permissions for the offline storage directory",
)

_R005 = DiagnosticMessage(
    code="AIGIE-R005",
    message="License heartbeat failed",
    consequence="License status may become stale, no immediate impact",
    fix="Check network connectivity to the license server",
)

_R006 = DiagnosticMessage(
    code="AIGIE-R006",
    message="Ingestion server error (HTTP 500)",
    consequence="Events will be retried automatically",
    fix="Platform backend may be experiencing issues. Check https://status.aigie.io",
)

# ── Code Registry ────────────────────────────────────────────────────

CODES: dict[str, DiagnosticMessage] = {
    msg.code: msg
    for msg in [
        _C001,
        _C002,
        _C003,
        _N001,
        _N002,
        _N003,
        _N004,
        _N005,
        _N006,
        _N007,
        _A001,
        _A002,
        _A003,
        _A004,
        _I001,
        _I002,
        _I003,
        _I004,
        _I005,
        _I006,
        _R001,
        _R002,
        _R003,
        _R004,
        _R005,
        _R006,
    ]
}

# Convenience aliases for import
C001, C002, C003 = _C001, _C002, _C003
N001, N002, N003, N004, N005, N006, N007 = _N001, _N002, _N003, _N004, _N005, _N006, _N007
A001, A002, A003, A004 = _A001, _A002, _A003, _A004
I001, I002, I003, I004, I005, I006 = _I001, _I002, _I003, _I004, _I005, _I006
R001, R002, R003, R004, R005, R006 = _R001, _R002, _R003, _R004, _R005, _R006


# ── Startup Banner ───────────────────────────────────────────────────


def format_startup_banner(diag: dict[str, Any]) -> str:
    """Format the startup diagnostics as a bordered banner block."""
    STATUS_ICONS = {"ok": "*", "error": "x", "skip": "-", "warn": "!"}

    title = f"Kytte SDK v{diag['version']}"
    rows = [
        ("Mode", diag["mode"]),
        ("Platform", diag.get("platform_url") or "not configured"),
        ("Auth", diag["auth"]),
        ("Gateway WS", diag["gateway"]),
        ("Interception", diag["interception"]),
        ("Judge", diag.get("judge", ("skip", "not initialized"))),
        ("Auto-instrument", diag["auto_instrument"]),
        ("Compression", diag["compression"]),
    ]

    lines = []
    for label, value in rows:
        if isinstance(value, tuple):
            status, text = value
            icon = STATUS_ICONS.get(status, " ")
            lines.append(f"  {icon} {label + ':':<18} {text}")
        else:
            lines.append(f"    {label + ':':<18} {value}")

    width = max(len(line) for line in lines) + 4
    border = "+" + "-" * (width - 2) + "+"
    title_line = f"+-- {title} " + "-" * (width - len(title) - 5) + "+"

    result = [title_line]
    for line in lines:
        result.append(f"| {line:<{width - 4}} |")
    result.append(border)

    return "\n".join(result)


# ── Doctor Health Check ──────────────────────────────────────────────


@dataclass
class DoctorResult:
    """Result of a doctor() health check."""

    healthy: bool
    checks: list[tuple[str, str, str]]  # (name, status, detail)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def format_doctor_output(result: DoctorResult) -> str:
    """Format doctor results for stdout."""
    STATUS_ICONS = {"ok": "*", "error": "x", "warn": "!"}

    lines = [
        "Kytte SDK Health Check",
        "-" * 22,
    ]

    for name, status, detail in result.checks:
        icon = STATUS_ICONS.get(status, " ")
        lines.append(f"  {icon} {name + ':':<20} {detail}")

    lines.append("")
    warning_count = len(result.warnings)
    error_count = len(result.errors)

    if result.healthy and warning_count == 0:
        lines.append("Overall: HEALTHY")
    elif result.healthy:
        lines.append(
            f"Overall: HEALTHY ({warning_count} warning{'s' if warning_count != 1 else ''})"
        )
    else:
        lines.append(
            f"Overall: UNHEALTHY ({error_count} error{'s' if error_count != 1 else ''}, "
            f"{warning_count} warning{'s' if warning_count != 1 else ''})"
        )

    return "\n".join(lines)
