"""The one retry loop every durable caller shares.

These pin the two decisions that make it safe to have only one: that a caller
says WHICH failures deserve another try, and that nothing sleeps after the last
attempt.
"""

import pytest

from probe.sdk.durable import RETRY_BACKOFF, backoff_delays, retry


def test_delays_double_from_the_start_and_stop_at_the_ceiling():
    assert list(backoff_delays(4, (2.0, 300.0))) == [2.0, 4.0, 8.0]
    assert list(backoff_delays(8, (2.0, 10.0))) == [2.0, 4.0, 8.0, 10.0, 10.0, 10.0, 10.0]


def test_a_single_attempt_never_waits():
    assert list(backoff_delays(1)) == []
    assert list(backoff_delays(0)) == []


def test_the_shared_backoff_is_the_one_the_outbox_worker_uses():
    from probe.sdk import outbox_worker

    assert (outbox_worker._BACKOFF_START_SECONDS, outbox_worker._BACKOFF_CAP_SECONDS) == RETRY_BACKOFF


def test_a_returned_failure_is_retried_when_the_caller_says_what_success_looks_like():
    """An agent turn answers `(None, detail)`; it never raises."""
    seen = []

    def turn():
        seen.append(len(seen))
        return (None, "no JSON") if len(seen) < 3 else ({"projects": []}, "")

    result = retry(turn, attempts=4, accept=lambda r: r[0] is not None, sleep=lambda _: None)
    assert result[0] == {"projects": []}
    assert len(seen) == 3


def test_the_last_result_is_returned_when_every_attempt_fails():
    result = retry(lambda: (None, "still nothing"), attempts=2,
                   accept=lambda r: r[0] is not None, sleep=lambda _: None)
    assert result == (None, "still nothing")


def test_only_the_named_exceptions_are_retried():
    """A programming error retried three times reads as a flaky network."""
    calls = []

    def bug():
        calls.append(1)
        raise TypeError("not a transport problem")

    with pytest.raises(TypeError):
        retry(bug, attempts=3, retry_on=OSError, sleep=lambda _: None)
    assert len(calls) == 1


def test_a_named_exception_is_retried_then_re_raised():
    calls = []

    def dropped():
        calls.append(1)
        raise OSError("connection reset")

    with pytest.raises(OSError):
        retry(dropped, attempts=3, retry_on=OSError, sleep=lambda _: None)
    assert len(calls) == 3


def test_waits_happen_between_attempts_and_not_after_the_last():
    slept = []
    retry(lambda: None, attempts=3, accept=lambda r: False,
          backoff=(1.0, 60.0), sleep=slept.append)
    assert slept == [1.0, 2.0]


def test_on_retry_sees_every_attempt_including_the_final_one():
    seen = []
    retry(lambda: (None, "x"), attempts=3, accept=lambda r: r[0] is not None,
          on_retry=lambda attempt, outcome: seen.append(attempt), sleep=lambda _: None)
    assert seen == [1, 2, 3]


def test_a_first_try_success_neither_sleeps_nor_reports():
    slept, seen = [], []
    assert retry(lambda: "ok", attempts=5, sleep=slept.append,
                 on_retry=lambda a, o: seen.append(a)) == "ok"
    assert slept == [] and seen == []


# --------------------------------------------------------------------------
# Plan 0.6: every durable retry LOOP takes its waits from `backoff_delays`,
# and waits at least as long as the server's Retry-After asked.
# --------------------------------------------------------------------------


def test_an_unbounded_sequence_never_runs_out_and_stays_at_the_ceiling():
    import itertools

    from probe.sdk.durable import backoff_delays

    assert list(itertools.islice(backoff_delays(None, (0.5, 4.0)), 7)) == [
        0.5, 1.0, 2.0, 4.0, 4.0, 4.0, 4.0,
    ]


def test_retry_after_only_ever_lengthens_a_wait_and_never_past_the_ceiling():
    from probe.sdk.durable import honor_retry_after

    assert honor_retry_after(2.0, None, ceiling=300.0) == 2.0
    assert honor_retry_after(2.0, 0.0, ceiling=300.0) == 2.0, "a 0 s ask cannot make a hot loop"
    assert honor_retry_after(2.0, 45.0, ceiling=300.0) == 45.0
    assert honor_retry_after(2.0, 86_400.0, ceiling=300.0) == 300.0


def test_the_detached_worker_waits_what_retry_after_asks(tmp_path, monkeypatch):
    """A pass stopped by a 503 carrying Retry-After: 45 waits 45 s, not the
    first backoff step (2 s); the next plain failure goes back to the ladder."""
    from probe.sdk import outbox_worker
    from probe.sdk.journal import DrainReport, Journal

    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", "/v1/runs/r-1/metrics", {"points": []})
    reports = iter(
        [
            DrainReport(remaining=1, stopped_transient=True, retry_after=45.0, errors=["503"]),
            DrainReport(remaining=1, stopped_transient=True, errors=["503"]),
            DrainReport(remaining=1, stopped_transient=True, errors=["503"]),
        ]
    )

    def fake_drain(j, **k):
        try:
            return next(reports)
        except StopIteration:
            raise KeyboardInterrupt from None

    slept: list[float] = []
    monkeypatch.setattr("probe.sdk.journal.drain", fake_drain)
    monkeypatch.setattr(outbox_worker.time, "sleep", slept.append)
    with pytest.raises(KeyboardInterrupt):
        outbox_worker.run(str(journal.dir))
    assert slept == [45.0, 4.0, 8.0], slept


def test_the_in_process_exporter_backs_off_after_a_transient_stop(app, tmp_path, monkeypatch):
    """It used to re-drain on every wake -- a training loop wakes it per
    `log()` -- hammering a sick server. After a transient stop, wakes wait out
    the backoff; only `close()` cuts it short, and still gets its last pass."""
    import time

    from probe.sdk import exporter as exporter_module
    from probe.sdk.journal import DrainReport

    from tests.conftest import make_client

    passes: list[float] = []
    waits: list[float] = []

    def fake_drain(journal, **k):
        passes.append(time.monotonic())
        return DrainReport(remaining=1, stopped_transient=True, retry_after=30.0, errors=["503"])

    real_honor = exporter_module.durable.honor_retry_after

    def recording_honor(*a, **k):
        waits.append(real_honor(*a, **k))
        return waits[-1]

    monkeypatch.setattr(exporter_module, "drain", fake_drain)
    monkeypatch.setattr(exporter_module.durable, "honor_retry_after", recording_honor)
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True, drain_interval=0.05)
    client._after_enqueue()  # starts the exporter and wakes it
    deadline = time.monotonic() + 5
    while not passes and time.monotonic() < deadline:
        time.sleep(0.01)
    assert len(passes) == 1
    for _ in range(20):  # a training loop logging
        client._after_enqueue()
        time.sleep(0.01)
    assert len(passes) == 1, "wakes during the backoff must not re-drain"
    assert waits == [30.0], "the wait is the server's Retry-After (30 s), not the 2 s first step"
    client.close()
    assert len(passes) == 2, "close() still makes its final pass"


# -- the transport's own in-request retries (plan 0.4: "the client honours
# Retry-After"; the server sends a jittered one on a lock timeout, #2008, and
# 5 s on entitlement_unavailable, #1998) -------------------------------------


def _transport_answering(responses, recorded):
    """A real `Transport` over httpx.MockTransport answering `responses` in turn."""
    import httpx

    from probe.sdk.config import Settings
    from probe.sdk.transport import Transport

    queue = list(responses)

    def handler(request):
        recorded.append(request)
        status, headers = queue.pop(0)
        body = {"detail": "concurrent telemetry write; retry this ingest batch"} if status >= 400 else {}
        return httpx.Response(status, json=body, headers=headers)

    settings = Settings(base_url="http://test", token="ros_pat_deadbeef")
    return Transport(settings, client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler)))


@pytest.fixture
def slept(monkeypatch):
    from probe.sdk import transport as transport_module

    waits: list[float] = []
    monkeypatch.setattr(transport_module.time, "sleep", waits.append)
    return waits


def test_an_inline_retry_waits_at_least_the_servers_retry_after(slept):
    requests = []
    transport = _transport_answering([(503, {"Retry-After": "1.5"}), (200, {})], requests)
    transport.request("GET", "/v1/runs/r-1")
    assert len(requests) == 2 and slept == [1.5], "0.2 s would retry before the server asked"


def test_an_inline_retry_without_retry_after_keeps_the_ladder(slept):
    requests = []
    transport = _transport_answering([(503, {}), (503, {}), (200, {})], requests)
    transport.request("GET", "/v1/runs/r-1")
    assert slept == [0.2, 0.4], "durable.backoff_delays with the transport's (0.2, 2.0)"


def test_a_long_retry_after_goes_back_to_the_callers_loop(slept):
    """A minute is not waited out inside one call: the error returns at once
    carrying `retry_after`, for the outbox worker / exporter / finish() loop."""
    requests = []
    transport = _transport_answering([(503, {"Retry-After": "60"}), (200, {})], requests)
    with pytest.raises(errors_module().ServerError) as err:
        transport.request("GET", "/v1/runs/r-1")
    assert len(requests) == 1 and slept == []
    assert err.value.retry_after == 60.0


def test_inside_a_deadline_a_retry_after_that_does_not_fit_is_not_retried_early(slept):
    import time

    from probe.sdk.transport import deadline_scope

    requests = []
    transport = _transport_answering([(503, {"Retry-After": "5"}), (200, {})], requests)
    with deadline_scope(time.monotonic() + 1.0):
        with pytest.raises(errors_module().ServerError) as err:
            transport.request("GET", "/v1/runs/r-1")
    assert len(requests) == 1 and slept == [], "never sooner than asked, never past the deadline"
    assert err.value.retry_after == 5.0


def test_a_presigned_put_honours_retry_after_too(slept):
    requests = []
    transport = _transport_answering([(503, {"Retry-After": "2.5"}), (200, {})], requests)
    transport.put_url("http://test/blob/x", b"bytes")
    assert len(requests) == 2 and slept == [2.5]


def errors_module():
    from probe.sdk import errors

    return errors
