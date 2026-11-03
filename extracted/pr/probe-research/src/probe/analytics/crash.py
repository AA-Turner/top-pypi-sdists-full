"""report one crash as a PostHog $exception with free text stripped."""

from __future__ import annotations
from probe.analytics import core as core
from probe.analytics.analytics import TelemetryContext
from probe.analytics.events import EVENT_EXCEPTION
from probe.analytics.outcomes import Via
from probe.analytics import sender  # call through the module: one binding for tests to patch


# CLI and stdio-MCP crashes ride the telemetry pipe (killswitch, self-host gate), not a 2nd vendor;
# sdk.diagnostics builds the payload, so one frame filter scrubs all. Why: DESIGN.md (crash.py).


#: PostHog manual-capture frame fields: `platform`/`lang` mark a hand-rolled integration; without
#: `resolved: True` the frames count as unsymbolicated and the issue has no usable stack.
_FRAME_BASE = {"platform": "custom", "lang": "python", "resolved": True}


def _posthog_frames(report: dict) -> list[dict]:
    """Our frame records in PostHog's stack-frame shape. Caller frames stay placeholders
    (`in_app: False`, nothing of the caller's), as in `sdk/diagnostics._frames`."""
    frames: list[dict] = []
    for link in report.get("exception") or []:
        for frame in link.get("frames") or []:
            if frame.get("probe"):
                frames.append(
                    {
                        **_FRAME_BASE,
                        "filename": frame.get("file"),
                        "function": frame.get("func"),
                        "lineno": frame.get("line"),
                        "in_app": True,
                    }
                )
            else:
                frames.append({**_FRAME_BASE, "filename": "<caller>", "in_app": False})
    return frames


def _fingerprint(report: dict, exception_type: str) -> str:
    """Group by exception type plus the Probe frame that raised. PostHog's default
    fingerprint leans on the MESSAGE, which this payload omits, so every TransportError
    would collapse into one issue."""
    import hashlib

    top = ""
    for link in report.get("exception") or []:
        for frame in link.get("frames") or []:
            if frame.get("probe"):
                top = f"{frame.get('file')}:{frame.get('func')}:{frame.get('line')}"
                break
        if top:
            break
    return hashlib.sha256(f"{exception_type}|{top}".encode()).hexdigest()[:32]


def _contract_safe(report: dict) -> dict:
    """The report minus every free-text field (the METADATA ONLY contract, DESIGN.md
    (analytics.py)), scrubbed messages included: they go to a VENDOR. Kept: exception
    TYPES, our frames, HTTP statuses, durations, booleans. The message stays in the
    diagnostic span on the customer's own run."""
    safe: dict = {"schema": report.get("schema"), "environment": report.get("environment", {})}
    chain = []
    for link in report.get("exception") or []:
        entry = {"type": link.get("type"), "module": link.get("module")}
        if link.get("status") is not None:
            entry["status"] = link["status"]
        if link.get("frames_elided"):
            entry["frames_elided"] = link["frames_elided"]
        chain.append(entry)
    if chain:
        safe["exception"] = chain
    if report.get("client"):
        safe["client"] = report["client"]
    transport = []
    for hop in report.get("transport") or []:
        # `p` is one of OUR API routes, not a folder path, so it stays; `error` goes.
        transport.append(
            {k: v for k, v in hop.items() if k in ("m", "p", "ms", "status", "stalled")}
        )
    if transport:
        safe["transport"] = transport
    if report.get("degraded"):
        safe["degraded"] = report["degraded"]
    return safe


def report_crash(
    exc: BaseException,
    *,
    surface: str,
    report: dict,
    base_url: str | None = None,
    handled: bool = False,
    site: str | None = None,
) -> None:
    """Emit one `$exception` from `report`, the caller's `diagnostics.build_report(exc)`. Never raises.

    Callers go through `probe.sdk.diagnostics.report_crash`, which skips it while diagnostics
    are off and builds `report` (analytics imports nothing above foundation).

    `handled=False` (default): an unhandled crash; the caller MUST re-raise after, or the
    operator's traceback is replaced by silence. `handled=True`: a SWALLOWED exception
    (`diagnostics.capture_swallowed`), sent at `warning` level so triage never mixes it with
    crashes, and without the exit flush: it happens mid-run, maybe inside a training loop.

    `base_url` must be the RESOLVED one, not the --base-url flag (None when not passed),
    or a self-hoster configured the ordinary way falls through to hosted and emits.
    """
    try:
        if base_url is None:
            try:
                base_url = core.effective_base_url(core.read_cli_config())
            except Exception:
                return  # unknown backend: fail CLOSED, never guess hosted
        context = TelemetryContext.start(via=Via.NONE, interactive=False, base_url=base_url)
        if not context.enabled:
            return
        head = (report.get("exception") or [{}])[0]
        exception_type = head.get("type") or type(exc).__name__
        context.emit(
            # PostHog Error Tracking groups on `$exception_list` (the Sentry shape).
            EVENT_EXCEPTION,
            surface=surface,
            # The swallow LOCATION, the grouping key; once only a local throttle key, so
            # every swallow site arrived as one indistinguishable `surface="sdk"` report.
            site=site,
            probe_report=_contract_safe(report),
            **{
                "$exception_list": [
                    {
                        "type": exception_type,
                        # The TYPE, not the message: grouping keys on type + frames,
                        # and the contract forbids the message.
                        "value": exception_type,
                        "mechanism": {"handled": handled, "synthetic": False},
                        "stacktrace": {"type": "raw", "frames": _posthog_frames(report)},
                    }
                ],
                # Explicit: the generated one leans on the message we do not send.
                "$exception_fingerprint": (
                    f"{site}:{exception_type}" if site else _fingerprint(report, exception_type)
                ),
                "$exception_level": "error" if not handled else "warning",
            },
        )
        if handled:
            # A swallow continues; the sender's own atexit flush will carry it.
            return
        try:
            sender._flush_at_exit()
        except Exception:
            pass
    except Exception:
        pass  # observability must never become observable
