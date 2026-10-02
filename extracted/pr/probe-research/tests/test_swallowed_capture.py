"""Swallowed-exception capture: evidence that fail-open used to delete.

Contracts, each pinned by a test that fails when it is removed:

  * a swallow site keeps swallowing -- a reporter that raises, or that lets an
    exception escape a fail-open body, converts observability into an outage;
  * the volume is bounded ACROSS PROCESSES, because the workload is a training
    loop shelling out to `probe log` per step, and an in-memory budget resets on
    every one of those;
  * nothing leaves a self-host install, and an unprovable backend is a no-send
    rather than a guess -- the SDK resolves its backend from `probe.init()` or a
    named context, so the CLI config file can name a different one entirely;
  * all THREE wired sites report, not just the one that had a test.
"""

from __future__ import annotations

import pytest

from probe.cli import telemetry as tm
from probe.sdk import diagnostics

HOSTED = "https://api.research.prbe.ai"
SELF_HOST = "https://research.internal.example.com"


@pytest.fixture(autouse=True)
def reset(monkeypatch, tmp_path):
    monkeypatch.setattr(diagnostics, "_swallowed_counts", {})
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "on")
    monkeypatch.delenv("PROBE_OUTBOX_DIR", raising=False)


@pytest.fixture()
def spool(tmp_path):
    d = tmp_path / "outbox"
    d.mkdir()
    return str(d)


@pytest.fixture()
def sent(monkeypatch):
    """Capture at the no-run leg (the PostHog pipe), without a network."""
    calls: list[dict] = []
    monkeypatch.setattr(tm, "report_crash", lambda exc, **kw: calls.append({"exc": exc, **kw}))
    return calls


# -- the report itself ---------------------------------------------------------


def test_a_swallow_is_reported_as_handled_and_carries_its_site(sent, spool):
    """`handled` separates "this killed a process" from "we recovered"; mixing
    them makes the crash queue useless. `site` is the grouping key and used to be
    consumed as a throttle key only, so every site arrived indistinguishable."""
    assert (
        diagnostics.capture_swallowed(
            ValueError("boom"), site="t.site", base_url=HOSTED, spool_dir=spool
        )
        is True
    )

    (call,) = sent
    assert call["handled"] is True
    assert call["site"] == "t.site"
    assert call["base_url"] == HOSTED
    assert isinstance(call["exc"], ValueError)


def test_the_handled_report_is_a_warning_and_skips_the_exit_flush(monkeypatch):
    """Drives the REAL report_crash. The whole handled= branch was previously
    unreachable from any test: all three of its expressions could be mutated at
    once and the suite stayed green."""
    captured: list[dict] = []
    flushed: list[bool] = []

    class _Ctx:
        enabled = True

        def emit(self, event, **props):
            captured.append({"event": event, **props})

    monkeypatch.setattr(tm.TelemetryContext, "start", classmethod(lambda cls, **kw: _Ctx()))
    monkeypatch.setattr(tm, "_flush_at_exit", lambda: flushed.append(True))

    try:
        raise ValueError("boom")
    except ValueError as exc:
        tm.report_crash(exc, surface="sdk", base_url=HOSTED, handled=True, site="t.site")

    (props,) = captured
    (entry,) = props["$exception_list"]
    assert entry["mechanism"] == {"handled": True, "synthetic": False}
    assert props["$exception_level"] == "warning"
    assert props["$exception_fingerprint"].startswith("t.site:")
    assert flushed == [], "a swallow must never block on the exit flush"


def test_an_unhandled_crash_stays_an_error_and_flushes(monkeypatch):
    """The other side of the same branch, so neither can be flipped silently."""
    flushed: list[bool] = []

    class _Ctx:
        enabled = True
        captured: list[dict] = []

        def emit(self, event, **props):
            _Ctx.captured.append(props)

    monkeypatch.setattr(tm.TelemetryContext, "start", classmethod(lambda cls, **kw: _Ctx()))
    monkeypatch.setattr(tm, "_flush_at_exit", lambda: flushed.append(True))

    try:
        raise ValueError("boom")
    except ValueError as exc:
        tm.report_crash(exc, surface="cli", base_url=HOSTED)

    (props,) = _Ctx.captured
    assert props["$exception_list"][0]["mechanism"]["handled"] is False
    assert props["$exception_level"] == "error"
    assert flushed == [True]


# -- the gates -----------------------------------------------------------------


def test_the_killswitch_suppresses_it(monkeypatch, sent, spool):
    monkeypatch.setenv("PROBE_DIAGNOSTICS", "off")

    assert (
        diagnostics.capture_swallowed(
            ValueError("boom"), site="t.site", base_url=HOSTED, spool_dir=spool
        )
        is False
    )
    assert sent == []


@pytest.mark.parametrize("base_url", [SELF_HOST, None], ids=["self-host", "unknown-backend"])
def test_a_backend_we_cannot_prove_is_hosted_reports_nothing(monkeypatch, spool, base_url):
    """Drives the REAL report_crash so the gate itself is exercised. This is a
    NEWLY opened path -- before this feature no SDK code called report_crash at
    all -- and the SDK's backend comes from `probe.init()` or a named context,
    which the CLI config never reflects."""
    emitted: list[dict] = []
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: emitted.append(rec))
    monkeypatch.setenv("PROBE_TELEMETRY", "on")

    diagnostics.capture_swallowed(
        ValueError("boom"), site="t.site", base_url=base_url, spool_dir=spool
    )

    assert emitted == []


def test_a_broken_reporter_never_escapes(monkeypatch, spool):
    """The caller already recovered. A reporter that raises would replace a
    handled error with an unhandled one."""

    def explode(exc, **kw):
        raise RuntimeError("reporter is on fire")

    monkeypatch.setattr(tm, "report_crash", explode)

    assert (
        diagnostics.capture_swallowed(
            ValueError("boom"), site="t.site", base_url=HOSTED, spool_dir=spool
        )
        is False
    )


def test_a_run_scoped_swallow_stays_in_the_tenant(monkeypatch, sent, spool):
    """With a run in hand the report becomes a diagnostic span -- it never leaves
    the customer's install, which is the #734 contract."""
    emitted: list[dict] = []
    monkeypatch.setattr(diagnostics, "report_exception", lambda run, exc, **kw: emitted.append(kw))

    assert (
        diagnostics.capture_swallowed(ValueError("boom"), site="t.site", run=object()) is True
    )

    assert emitted == [{"swallowed_at": "t.site"}]
    assert sent == [], "nothing went to the vendor pipe"


# -- volume --------------------------------------------------------------------


def test_the_throttle_survives_a_fresh_process(sent, spool, monkeypatch):
    """The bug this replaced: `_swallowed_counts` is process-local, so `probe log`
    per training step got a fresh budget of 3 every invocation. Simulated by
    clearing the in-memory counter, which is exactly what a new interpreter does
    -- the file stamp on the shared journal dir is what must still hold."""
    assert diagnostics.capture_swallowed(
        ValueError("boom"), site="t.site", base_url=HOSTED, spool_dir=spool
    )
    assert len(sent) == 1

    for _ in range(20):
        diagnostics._swallowed_counts.clear()  # a fresh process
        diagnostics.capture_swallowed(
            ValueError("boom"), site="t.site", base_url=HOSTED, spool_dir=spool
        )

    assert len(sent) == 1, "a shell-out loop must not produce one report per invocation"


def test_one_chatty_site_cannot_starve_another(sent, spool):
    """Per-site windows, not one global window."""
    for _ in range(10):
        diagnostics._swallowed_counts.clear()
        diagnostics.capture_swallowed(
            ValueError("boom"), site="t.chatty", base_url=HOSTED, spool_dir=spool
        )
    sent.clear()

    assert diagnostics.capture_swallowed(
        ValueError("boom"), site="t.rare", base_url=HOSTED, spool_dir=spool
    )


def test_the_in_process_budget_still_bounds_one_interpreter(sent, spool):
    """The SDK case: `import probe` in a training script can hit a swallow site
    thousands of times in ONE process, and the file stamp is a stat per call."""
    for _ in range(50):
        diagnostics.capture_swallowed(
            ValueError("boom"), site="t.site", base_url=HOSTED, spool_dir=spool
        )

    assert len(sent) <= diagnostics.MAX_SWALLOWED_PER_SITE


# -- the wired sites -----------------------------------------------------------


def _broken_journal(tmp_path):
    class Broken:
        dir = tmp_path

        def append_http(self, *a, **k):
            raise OSError(28, "No space left on device")

        def append_upload(self, *a, **k):
            raise OSError(28, "No space left on device")

        def note_capture_gap(self, *a, **k):
            pass

    return Broken()


@pytest.mark.parametrize(
    "method,kwargs,expected",
    [
        ("_enqueue", {"method": "POST", "path": "/v1/runs/x/metrics", "body": {}}, "client.enqueue_dropped"),
        (
            "_enqueue_upload",
            {"anchor": "run", "anchor_id": "r", "name": "n", "src_path": "x"},
            "client.enqueue_upload_dropped",
        ),
    ],
    ids=["write", "upload"],
)
def test_both_data_loss_branches_are_reported(monkeypatch, tmp_path, method, kwargs, expected):
    """BOTH branches, not just the one that had a test. Each is data loss -- the
    write reached neither the server nor the journal -- and deleting either call
    previously left the whole suite green."""
    from probe.sdk import client as client_module

    captured: list[str] = []
    monkeypatch.setattr(
        client_module,
        "_capture_swallowed",
        lambda exc, *, site, **kw: captured.append(site),
    )

    obj = client_module.Client.__new__(client_module.Client)
    obj.journal = _broken_journal(tmp_path)
    obj.dropped_writes = 0
    obj._redact = None
    obj.settings = type("S", (), {"base_url": HOSTED})()

    if method == "_enqueue_upload":
        # Reach the simulated ENOSPC journal failure after credential admission;
        # a missing source is now correctly refused before enqueue is attempted.
        source = tmp_path / "benign-report.txt"
        source.write_text("training loss: 0.25\n")
        kwargs = {**kwargs, "src_path": str(source)}
    getattr(obj, method)(**kwargs)

    assert captured == [expected]
    assert obj.dropped_writes == 1, "the existing accounting must still run"


def test_a_failed_lease_renewal_is_reported(monkeypatch):
    """Its own comment states the stakes: a lease that stops renewing is how a
    live run silently becomes `untracked`. There was no test for the failure leg
    at all -- nothing made renew_lease_if_stale raise."""
    from probe.cli import run_lock
    from probe.sdk import client as client_module

    captured: list[str] = []

    def boom(*a, **k):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(run_lock, "renew_lease_if_stale", boom)
    monkeypatch.setattr(
        client_module, "_capture_swallowed", lambda exc, *, site, **kw: captured.append(site)
    )

    # Must not raise: this rides on a real write.
    client_module._touch_run_lease("/v1/runs/3c5f3695-1a4a-49ef-a255-cf845ea3373a/metrics")

    assert captured == ["client.lease_renew"]


def test_importing_the_sdk_does_not_drag_in_the_cli():
    """`_capture_swallowed` exists ONLY to keep `probe.cli` out of a training
    script's import graph. Nothing verified the constraint that motivates it."""
    import subprocess
    import sys

    out = subprocess.run(
        [sys.executable, "-c", "import sys, probe; print(any(m.startswith('probe.cli') for m in sys.modules))"],
        capture_output=True,
        text=True,
    )
    assert out.stdout.strip() == "False", out.stderr[-500:]
