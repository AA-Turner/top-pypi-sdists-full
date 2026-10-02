"""The ProSeCo regressions (2026-08-19).

A live RunPod campaign disabled Probe mid-flight after two rounds of
simultaneous `TransportError` worker failures. Four defects combined to let a
transient network blip kill training processes, and each one is pinned here:

1. a metrics POST was never retried, so one blip was immediately terminal;
2. the connect phase inherited the full 30s timeout, so an unreachable endpoint
   parked the training loop long enough to trip a distributed collective;
3. `set_status` passed `strict=True` -- the one SDK write that re-raised -- and
   `Run.__exit__` calls it from inside an exception handler;
4. async writes were opt-in, and only the CLI could opt in.
"""

from __future__ import annotations

import httpx
import pytest

from probe.sdk import errors
from probe.sdk.client import Client
from probe.sdk.journal import Journal
from probe.sdk.run import Run
from probe.sdk.transport import Transport
from probe.sdk.config import Settings

from tests.conftest import make_client
from tests.test_outbox import seeded_run


@pytest.fixture(autouse=True)
def _isolated_config(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC", raising=False)


def _settings(**kw):
    return Settings(base_url="https://example.invalid", token="probe_pat_x", **kw)


# -- defect 1: a metrics POST is retried when the request never landed --------


def _counting_transport(exc, *, statuses=None):
    """A transport whose underlying httpx client raises `exc`, counting calls."""
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if statuses:
            return httpx.Response(statuses.pop(0))
        raise exc

    client = httpx.Client(
        transport=httpx.MockTransport(handler), base_url="https://example.invalid"
    )
    return Transport(_settings(), client=client), calls


def test_metrics_post_retries_a_connect_failure():
    """The defect: `retry` was `method in {GET, PUT}`, so a POST got ONE shot."""
    transport, calls = _counting_transport(httpx.ConnectError("refused"))

    with pytest.raises(errors.TransportError):
        transport.request("POST", "/v1/runs/r1/metrics", json_body={"points": []})

    # 1 initial + max_retries. Before the fix this was exactly 1.
    assert calls["n"] == 1 + transport.max_retries


def test_metrics_post_does_not_retry_a_read_timeout():
    """A response lost after the request landed must NOT be replayed: appending
    a metric batch twice is silent corruption, worse than the error it avoids."""
    transport, calls = _counting_transport(httpx.ReadTimeout("slow"))

    with pytest.raises(errors.TransportError):
        transport.request("POST", "/v1/runs/r1/metrics", json_body={"points": []})

    assert calls["n"] == 1


def test_get_still_retries_a_read_timeout():
    """Idempotent reads keep their old, broader retry envelope."""
    transport, calls = _counting_transport(httpx.ReadTimeout("slow"))

    with pytest.raises(errors.TransportError):
        transport.request("GET", "/v1/runs/r1")

    assert calls["n"] == 1 + transport.max_retries


# -- defect 2: the connect phase is bounded independently of the read ---------


def test_connect_timeout_is_bounded_below_the_read_timeout():
    """A black-holing endpoint used to park a caller for the full 30s per call."""
    transport = Transport(_settings(), timeout=30.0)
    timeout = transport._client.timeout

    assert timeout.connect == 5.0
    assert timeout.read == 30.0


def test_a_short_overall_timeout_still_caps_connect():
    """`min(timeout, 5)` -- a caller asking for 1s must not get a 5s connect."""
    transport = Transport(_settings(), timeout=1.0)

    assert transport._client.timeout.connect == 1.0


# -- defect 3: set_status fail-opens instead of killing the caller ------------


def test_set_status_journals_instead_of_raising(app, tmp_path, monkeypatch):
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=False)
    run = Run(client, {"id": run_id})

    def boom(*a, **kw):
        raise errors.TransportError("network down")

    monkeypatch.setattr(client.transport, "request", boom)

    # Before the fix this raised TransportError straight into the caller.
    assert run.set_status("failed") is None
    assert [op["method"] for _, op in client.journal.pending()] == ["PATCH"]
    client.close()


def test_run_exit_does_not_mask_the_bodys_exception(app, tmp_path, monkeypatch):
    """The mechanism that killed the campaign's workers: `Run.__exit__` closes
    the run from inside an exception handler, so a raising `set_status` replaced
    the body's real traceback with a transport one and took the process down."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=False)

    def boom(*a, **kw):
        raise errors.TransportError("network down")

    with pytest.raises(ZeroDivisionError):
        with Run(client, {"id": run_id}) as run:
            monkeypatch.setattr(client.transport, "request", boom)
            1 / 0  # noqa: B018 -- the body's own failure must survive the close

    client.close()


# -- defect 4: async is the default, and remains a choice ---------------------


def test_default_client_is_async(tmp_path):
    client = Client(settings=_settings(), journal=Journal(tmp_path / "outbox"))
    assert client.async_writes is True
    client.close()


def test_explicit_false_still_wins(tmp_path):
    client = Client(
        settings=_settings(),
        journal=Journal(tmp_path / "outbox"),
        async_writes=False,
    )
    assert client.async_writes is False
    client.close()


def test_env_var_can_pin_sync_without_touching_code(monkeypatch, tmp_path):
    """The campaign had no way to change write mode without editing the training
    script: PROBE_ASYNC was read only by the CLI."""
    monkeypatch.setenv("PROBE_ASYNC", "0")
    client = Client(settings=_settings(), journal=Journal(tmp_path / "outbox"))
    assert client.async_writes is False
    client.close()


def test_an_explicit_argument_beats_the_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_ASYNC", "0")
    client = Client(
        settings=_settings(),
        journal=Journal(tmp_path / "outbox"),
        async_writes=True,
    )
    assert client.async_writes is True
    client.close()


def test_a_typod_env_value_warns_and_defers_to_the_default(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_ASYNC", "asynchronous")
    with pytest.warns(UserWarning, match="PROBE_ASYNC"):
        client = Client(settings=_settings(), journal=Journal(tmp_path / "outbox"))
    assert client.async_writes is True
    client.close()


def test_an_injected_transport_stays_sync_by_default(tmp_path):
    """Delivery needs the default transport -- the detached worker cannot replay
    an injected one. Defaulting those clients to async would journal writes that
    nothing drains, and would silently change the hosted MCP's semantics."""
    settings = _settings()
    client = Client(
        settings=settings,
        transport=Transport(settings),
        journal=Journal(tmp_path / "outbox"),
    )
    assert client.async_writes is False
    client.close()


def test_missing_credentials_degrade_to_sync_rather_than_raising(tmp_path):
    """An explicit async_writes=True still raises (F7). The DEFAULT must not:
    nothing could drain the journal, so the honest fallback is the path that
    still works."""
    client = Client(
        settings=Settings(base_url="https://example.invalid"),
        journal=Journal(tmp_path / "outbox"),
    )
    assert client.async_writes is False
    client.close()


def test_explicit_async_without_credentials_still_refuses(tmp_path):
    with pytest.raises(errors.ValidationError, match="deliverable credentials"):
        Client(
            settings=Settings(base_url="https://example.invalid"),
            journal=Journal(tmp_path / "outbox"),
            async_writes=True,
        )


def test_a_metric_log_never_touches_the_network_by_default(app, tmp_path, monkeypatch):
    """The headline: `run.log()` in a training loop cannot block or fail on the
    network, because it does not use it."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    def boom(*a, **kw):
        raise AssertionError("a default-mode log must not reach the transport")

    monkeypatch.setattr(client.transport, "request", boom)
    run.log({"loss": 0.5}, step=1)

    assert [op["path"] for _, op in client.journal.pending()] == [
        f"/v1/runs/{run_id}/metrics"
    ]
    client.close()


# -- follow-up: caller semantics under the new default ------------------------
#
# The flip above was merged before these were caught. Each one is a way the
# default could silently change what a caller MEANS, which is worse than the
# blocking it was meant to cure.


def test_strict_forces_the_network_even_under_async(app, tmp_path, monkeypatch):
    """strict means "fail loudly, never journal" -- a demand for the network.

    It used to be resolved AFTER the async branch, so async silently downgraded
    it to a queued replay. Miles passes strict=True and then deletes its own
    durable queue record on the strength of not seeing an exception, so a
    queued write erased the only copy of the data.
    """
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    def boom(*a, **kw):
        raise errors.TransportError("network down")

    monkeypatch.setattr(client.transport, "request", boom)

    with pytest.raises(errors.TransportError):
        run.log({"loss": 0.5}, step=1, strict=True)

    assert client.journal.pending() == [], "strict must never journal"
    client.close()


def test_a_non_strict_log_still_journals_under_async(app, tmp_path, monkeypatch):
    """The headline behaviour must survive the strict fix."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})

    monkeypatch.setattr(
        client.transport, "request", lambda *a, **kw: pytest.fail("must not be called")
    )
    run.log({"loss": 0.5}, step=1)

    assert len(client.journal.pending()) == 1
    client.close()


def test_set_status_strict_raises_for_the_cli_barrier(app, tmp_path, monkeypatch):
    """`probe run end` is documented as the barrier: it delivers or fails loudly."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=False)
    run = Run(client, {"id": run_id})

    def boom(*a, **kw):
        raise errors.TransportError("network down")

    monkeypatch.setattr(client.transport, "request", boom)

    with pytest.raises(errors.TransportError):
        run.set_status("completed", strict=True)
    client.close()


def test_env_async_does_not_defeat_the_injected_transport_gate(monkeypatch, tmp_path):
    """PROBE_ASYNC is a documented CLI knob, so it may be exported in a profile
    or a SLURM script. It must not turn an injected-transport client async: that
    client has no auto-drain, no exporter and no credential guard, so its writes
    would be journaled to disk with nothing to deliver them."""
    monkeypatch.setenv("PROBE_ASYNC", "1")
    settings = _settings()
    client = Client(
        settings=settings,
        transport=Transport(settings),
        journal=Journal(tmp_path / "outbox"),
    )
    assert client.async_writes is False
    client.close()


def test_an_explicit_true_still_opts_an_injected_transport_in(tmp_path):
    """The gate is about defaults, not a prohibition: F2's in-process exporter
    delivers through THIS client, so an explicit request still works."""
    settings = _settings()
    client = Client(
        settings=settings,
        transport=Transport(settings),
        journal=Journal(tmp_path / "outbox"),
        async_writes=True,
        drain_interval=5.0,
    )
    assert client.async_writes is True
    client.close()


def test_a_dead_lettered_close_is_not_reported_as_delivered(app, tmp_path, monkeypatch):
    """Counting pending() alone read a permanently-rejected close as success:
    the drain moves the op to failed/, so it vanishes from pending."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=False)
    run = Run(client, {"id": run_id})

    def reject(method, path, *a, **kw):
        if method == "PATCH":
            raise errors.ValidationError("bad", status=422)
        return None

    monkeypatch.setattr(client.transport, "request", reject)

    # Plan 0.2: a default close never raises over delivery -- but it must not
    # CLAIM delivery either. It warns and reports the rejected close.
    with pytest.warns(UserWarning, match="dead-lettered"):
        result = run.finish("completed")
    assert result["delivered"] == 0 and result["close_rejected"] is True
    assert result.get("finish_queued") is False
    client.close()


# -- 0.99.1: two ways the fixes themselves reopened the original wound --------


def test_run_exit_does_not_mask_the_body_when_the_close_dead_letters(
    app, tmp_path, monkeypatch
):
    """The earlier version of this test used a TransportError, which fail-opens
    into PENDING and never raised. A 422 DEAD-LETTERS, and the raise added for
    that case propagated out of `Run.__exit__` -- turning `1/0` into "the
    terminal status was dead-lettered" and reopening defect #3 from a new
    direction. The body's exception wins, always.
    """
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=False)

    def reject(method, path, *a, **kw):
        if method == "PATCH":
            raise errors.ValidationError("bad", status=422)
        return None

    with pytest.raises(ZeroDivisionError):
        with Run(client, {"id": run_id}):
            monkeypatch.setattr(client.transport, "request", reject)
            1 / 0  # noqa: B018

    client.close()


def test_a_strict_finish_still_raises_on_a_dead_letter(app, tmp_path, monkeypatch):
    """A caller who asked for the barrier (`strict=True`) must hear that the
    close did not happen as an exception; everyone else hears it as a warning
    (plan 0.2), and `Run.__exit__` never masks the body either way."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=False)
    run = Run(client, {"id": run_id})

    def reject(method, path, *a, **kw):
        if method == "PATCH":
            raise errors.ValidationError("bad", status=422)
        return None

    monkeypatch.setattr(client.transport, "request", reject)
    # Strict sends the close synchronously and surfaces the server's refusal.
    with pytest.raises(errors.RosError, match="bad"):
        run.finish("completed", strict=True)
    assert app.runs[run_id]["status"] != "completed"
    client.close()


def test_flush_for_span_leaves_other_runs_queued(app, tmp_path, monkeypatch):
    """`client.flush()` is a MACHINE-WIDE drain. On a hot path -- harbor calls
    log_artifact(path=, span_id=) once per file per trial -- that dragged every
    neighbouring run's backlog through an artifact upload. The barrier is
    scoped to this run's ops with run_ref."""
    other_id = seeded_run(app, tmp_path)
    mine_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)

    other = Run(client, {"id": other_id})
    mine = Run(client, {"id": mine_id})
    other.log({"loss": 1.0}, step=1)
    span = mine.span("rollout", external_key="k1")

    artifact = tmp_path / "weights.bin"
    artifact.write_bytes(b"x" * 32)
    mine.log_artifact("weights", path=str(artifact), span_id=str(span))

    refs = [op.get("run_ref") for _, op in client.journal.pending()]
    assert other_id in refs, (
        "the neighbour's queued op must survive an artifact upload on my run"
    )
    # My upload is now QUEUED rather than posted directly (staged-or-synchronous),
    # so it joins the queue too — the point of the change. What must NOT happen
    # is my run's work dragging the neighbour's backlog through a drain.
    # Queued in the waiting room until its credential scan has run.
    assert client.journal.waiting(run_ref=mine_id), "the artifact should be queued, not uploaded inline"
    client.close()


def test_flush_for_span_is_a_noop_without_a_queued_span(app, tmp_path, monkeypatch):
    """A pending metric point says nothing about whether the cited span landed,
    so it must not make every artifact upload wait on unrelated telemetry."""
    run_id = seeded_run(app, tmp_path)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
    run = Run(client, {"id": run_id})
    run.log({"loss": 1.0}, step=1)

    called = {"n": 0}
    import probe.sdk.journal as journal_mod

    real_drain = journal_mod.drain
    monkeypatch.setattr(
        journal_mod, "drain", lambda *a, **kw: (called.__setitem__("n", called["n"] + 1), real_drain(*a, **kw))[1]
    )
    run._flush_for_span("some-span-id")

    assert called["n"] == 0, "no queued span op — nothing to order against"
    client.close()
