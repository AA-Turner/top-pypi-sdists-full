"""Unhandled-crash reporting for the CLI and the stdio MCP.

These two surfaces are not the SDK: they own their process, so a crash costs one
command rather than a training run, and there is no run to hang a diagnostic span
on. They ride the existing PostHog pipe instead -- which already has the
killswitch, the self-host egress gate and identity -- while reusing
`sdk.diagnostics` to build the payload, so scrubbing and bounding have one
implementation rather than two.
"""

from __future__ import annotations

import importlib
import json

import pytest

from probe.cli import telemetry as telemetry_mod
from probe.sdk import diagnostics
from probe.sdk import errors as errors_mod

# `probe.cli.__init__` defines a `main` FUNCTION, which shadows the submodule of
# the same name on the package -- `from probe.cli import main` hands back the
# function. Import the module by path so `app` is reachable for patching.
cli_main = importlib.import_module("probe.cli.main")


@pytest.fixture(autouse=True)
def _diagnostics_on(monkeypatch):
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "on")


def test_cli_reports_then_reraises(monkeypatch):
    """Re-raising is the contract. Swallowing the traceback to file a report
    would trade the operator's diagnosis for ours."""
    seen = []

    def boom(*_a, **_kw):
        raise RuntimeError("unexpected")

    monkeypatch.setattr(cli_main, "app", boom)
    monkeypatch.setattr(telemetry_mod, "report_crash", lambda exc, **kw: seen.append((exc, kw)))

    with pytest.raises(RuntimeError, match="unexpected"):
        cli_main.main([])

    assert len(seen) == 1
    assert seen[0][1]["surface"] == "cli"


def test_known_errors_are_still_handled_not_reported(monkeypatch):
    """Every user mistake has a branch above the catch-all. A usage error that
    started filing crash reports would bury the real ones."""
    seen = []
    monkeypatch.setattr(telemetry_mod, "report_crash", lambda exc, **kw: seen.append(exc))

    def bad(*_a, **_kw):
        from probe.sdk import errors

        raise errors.RosError("nope")

    monkeypatch.setattr(cli_main, "app", bad)
    assert cli_main.main([]) == 1
    assert seen == []


def test_report_crash_never_raises(monkeypatch):
    """A broken reporter must not become the crash."""

    def explode(*_a, **_kw):
        raise RuntimeError("sender is down")

    monkeypatch.setattr(telemetry_mod.TelemetryContext, "start", explode)
    telemetry_mod.report_crash(ValueError("x"), surface="cli")


def test_report_crash_is_suppressed_by_the_killswitch(monkeypatch):
    started = []
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "off")
    monkeypatch.setattr(
        telemetry_mod.TelemetryContext,
        "start",
        classmethod(lambda cls, **kw: started.append(kw)),
    )
    telemetry_mod.report_crash(ValueError("x"), surface="cli")
    assert started == []


def test_posthog_frames_separate_our_code_from_the_callers():
    """`in_app` is what makes PostHog group on OUR frames. A caller frame that
    leaked in as in_app would group unrelated customers' crashes together."""
    report = {
        "exception": [
            {
                "frames": [
                    {"probe": False},
                    {"probe": True, "file": "sdk/transport.py", "func": "request", "line": 221},
                ]
            }
        ]
    }
    frames = telemetry_mod._posthog_frames(report)
    assert frames[0]["filename"] == "<caller>"
    assert frames[0]["in_app"] is False
    assert set(frames[0]) == {"platform", "lang", "resolved", "filename", "in_app"}
    assert frames[1]["in_app"] is True
    assert frames[1]["filename"] == "sdk/transport.py"
    # PostHog's manual-capture schema: without these, ingestion treats the
    # frames as needing symbolication and the issue renders without a stack.
    assert frames[1]["platform"] == "custom"
    assert frames[1]["lang"] == "python"
    assert frames[1]["resolved"] is True


def test_payload_is_built_by_the_shared_scrubber(monkeypatch):
    """One implementation of the frame filter, not two."""
    calls = []
    real = diagnostics.build_report
    monkeypatch.setattr(
        diagnostics, "build_report", lambda *a, **kw: calls.append(a) or real(*a, **kw)
    )
    monkeypatch.setattr(
        telemetry_mod.TelemetryContext,
        "start",
        classmethod(lambda cls, **kw: telemetry_mod.null_context()),
    )
    telemetry_mod.report_crash(ValueError("x"), surface="cli")
    assert len(calls) == 1


# -- the stdio MCP -------------------------------------------------------------
def test_mcp_stdio_reports_then_reraises(monkeypatch):
    """A crash here is invisible in a way a CLI crash is not: the traceback goes
    down a pipe the coding agent owns, and the user just sees a tool that
    stopped working. Re-raise for the same reason as the CLI -- the parent still
    needs the exit."""
    from probe.mcp import server as mcp_server

    seen = []

    def boom():
        raise RuntimeError("stdio server died")

    monkeypatch.setattr(mcp_server, "create_server", boom)
    monkeypatch.setattr(telemetry_mod, "report_crash", lambda exc, **kw: seen.append((exc, kw)))

    with pytest.raises(RuntimeError, match="stdio server died"):
        mcp_server.main()

    assert len(seen) == 1
    assert seen[0][1]["surface"] == "mcp_stdio"


# -- the CLI egress gate -------------------------------------------------------
def test_a_self_hosted_backend_emits_nothing(monkeypatch):
    """The self-host promise, extended to crash reports."""
    started = []
    monkeypatch.setattr(
        telemetry_mod.TelemetryContext,
        "start",
        classmethod(lambda cls, **kw: started.append(kw) or telemetry_mod.null_context()),
    )
    telemetry_mod.report_crash(
        ValueError("x"), surface="cli", base_url="https://probe.internal.corp"
    )
    assert started and started[0]["base_url"] == "https://probe.internal.corp"
    # start() applies core.hosted_base_url, which refuses a non-prbe.ai host
    assert not telemetry_mod.TelemetryContext.start(
        via=telemetry_mod.Via.NONE, interactive=False, base_url="https://probe.internal.corp"
    ).enabled


def test_the_vendor_payload_carries_no_free_text():
    """cli/telemetry.py's contract: "No folder paths, no error strings
    (exception text can embed a path)". Nothing asserted that before."""
    try:
        raise errors_mod.TransportError("GET /v1/x from /Users/alice/secret/train.py failed")
    except Exception as exc:
        report = diagnostics.build_report(exc)
    report.setdefault("transport", [{"m": "POST", "p": "/v1/x", "ms": 5, "error": "boom"}])

    safe = telemetry_mod._contract_safe(report)

    # Structural, not substring: "error" legitimately appears inside the module
    # name `probe.sdk.errors`, which is a type identifier and stays.
    assert all("message" not in link for link in safe["exception"])
    assert all("error" not in hop for hop in safe["transport"])
    assert "alice" not in json.dumps(safe), "a path survived into the vendor payload"
    # the parts grouping actually needs survive
    assert safe["exception"][0]["type"] == "TransportError"
    assert safe["transport"][0]["ms"] == 5


def test_the_fingerprint_separates_call_sites():
    """PostHog's generated fingerprint leans on the exception MESSAGE, and this
    payload deliberately has none -- so without an explicit one every
    TransportError in the SDK would collapse into a single issue."""
    def report_at(func, line):
        return {
            "exception": [
                {
                    "type": "TransportError",
                    "frames": [
                        {"probe": False},
                        {"probe": True, "file": "sdk/transport.py", "func": func, "line": line},
                    ],
                }
            ]
        }

    a = telemetry_mod._fingerprint(report_at("request", 221), "TransportError")
    b = telemetry_mod._fingerprint(report_at("get_url", 440), "TransportError")
    assert a != b, "two different call sites must be two issues"
    assert a == telemetry_mod._fingerprint(report_at("request", 221), "TransportError")
    assert len(a) == 32


def test_the_emitted_event_matches_posthogs_schema(monkeypatch):
    """End to end through report_crash: the properties PostHog's Error Tracking
    actually reads. Nothing asserted these before, so a wrong shape would have
    ingested fine and rendered an empty dashboard."""
    captured = []

    class _Ctx:
        enabled = True

        def emit(self, event, **props):
            captured.append((event, props))

    monkeypatch.setattr(
        telemetry_mod.TelemetryContext, "start", classmethod(lambda cls, **kw: _Ctx())
    )
    monkeypatch.setattr(telemetry_mod, "_flush_at_exit", lambda: None)

    try:
        raise errors_mod.TransportError("POST /v1/runs/x/metrics: connect timeout")
    except Exception as exc:
        telemetry_mod.report_crash(exc, surface="cli", base_url="https://api.research.prbe.ai")

    (event, props) = captured[0]
    assert event == "$exception"
    (entry,) = props["$exception_list"]
    assert entry["type"] == "TransportError"
    assert entry["mechanism"] == {"handled": False, "synthetic": False}
    assert entry["stacktrace"]["type"] == "raw"
    assert entry["stacktrace"]["frames"], "an empty stack renders an empty issue"
    assert props["$exception_fingerprint"]
    assert props["$exception_level"] == "error"
    assert props["surface"] == "cli"
    # and still no free text anywhere in the payload
    assert "connect timeout" not in json.dumps(props)
