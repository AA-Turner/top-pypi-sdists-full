"""A foreground import waits out a dropped connection instead of ending.

Two ways to get this wrong, and this file exists because both were shipped.

Retrying on an EXCEPTION never fires: `Client.flush` returns a delivered count
and the drain classifies transport errors itself, parks the operation and
returns normally. Retrying on "anything still queued" fires far too often: an
import with no drainer attached leaves work queued as a matter of course, so
every ordinary partial run would sit through the whole backoff.

What is waited out is the drain's own `stopped_transient` -- it parked
something for a reason worth waiting on, and nothing else.
"""

from __future__ import annotations

import pytest

from probe.cli import backfill_import as imp
from probe.sdk.journal import DrainReport


class Report:
    def __init__(self):
        self.lines = []

    def add(self, *lines):
        self.lines.extend(line for line in lines if line)


class Client:
    """Stands in for a client whose drain never raises -- the real contract."""

    def __init__(self, reports):
        self._reports = list(reports)
        self.drains = 0
        self.journal = object()

    def _outbox_client_factory(self):
        return lambda _context: None


@pytest.fixture(autouse=True)
def no_sleeping(monkeypatch):
    """Opt back into the full attempt count, without the waiting."""
    from probe.sdk import durable

    monkeypatch.delenv(imp.FLUSH_ATTEMPTS_ENV, raising=False)
    monkeypatch.setattr(durable.time, "sleep", lambda _seconds: None)


@pytest.fixture
def drains(monkeypatch):
    """Replace the drain itself; these tests are about what its report means."""
    calls = []

    def install(reports):
        queue = list(reports)

        def fake_drain(journal, **kwargs):
            calls.append(kwargs)
            return queue.pop(0) if len(queue) > 1 else queue[0]

        monkeypatch.setattr("probe.sdk.journal.drain", fake_drain)
        return calls

    return install


def test_a_transient_stop_is_waited_out_until_it_clears(drains):
    calls = drains([
        DrainReport(stopped_transient=True, remaining=2),
        DrainReport(stopped_transient=True, remaining=2),
        DrainReport(delivered=2, remaining=0),
    ])
    report, said = Report(), []
    imp._flush_uploads(Client([]), retry_network=False, report=report,
                       progress=lambda message, **kw: said.append(message))
    assert len(calls) == 3, "the drain must be retried while it keeps parking work"
    assert any("connection is unavailable" in message for message in said)
    assert report.lines == [], "nothing to report once the queue drained"


def test_work_merely_left_queued_is_not_a_connection_problem(drains):
    """An import with no drainer attached queues as a matter of course."""
    calls = drains([DrainReport(delivered=0, remaining=7, stopped_transient=False)])
    report = Report()
    imp._flush_uploads(Client([]), retry_network=False, report=report)
    assert len(calls) == 1, "a queued outbox must not cost the whole backoff"
    assert report.lines == []


def test_a_stop_that_never_clears_is_reported_not_silent(drains):
    calls = drains([DrainReport(stopped_transient=True, remaining=3)])
    report = Report()
    imp._flush_uploads(Client([]), retry_network=False, report=report)
    assert len(calls) == imp.flush_attempts()
    assert "3 upload(s) are still queued" in report.lines[-1]
    assert "Re-running resumes them" in report.lines[-1]


def test_a_clean_drain_runs_once_and_says_nothing(drains):
    calls = drains([DrainReport(delivered=4, remaining=0)])
    report = Report()
    imp._flush_uploads(Client([]), retry_network=False, report=report)
    assert len(calls) == 1
    assert report.lines == []


def test_a_background_job_still_defers_to_its_own_supervisor(monkeypatch):
    """It can wait far longer than a foreground process should, so it owns this."""
    seen = {}

    class Supervised:
        def __init__(self):
            self.flushes = 0

        def flush(self, *, on_error=None, on_delivered=None):
            self.flushes += 1
            seen["on_error"] = on_error
            return 0

    client = Supervised()
    imp._flush_uploads(client, retry_network=True, report=Report())
    assert client.flushes == 1, "a supervised job must not also retry in-process"
    assert callable(seen["on_error"])


def test_the_wait_is_bounded_and_the_comment_matches_the_constants():
    from probe.sdk.durable import RETRY_BACKOFF, backoff_delays

    total = sum(backoff_delays(imp.FLUSH_ATTEMPTS, RETRY_BACKOFF))
    assert 60 <= total <= 300, (
        f"the documented wait is {total}s; a foreground process that sits much "
        "longer is one nobody can tell from a hang"
    )


def test_a_real_error_is_not_swallowed_as_a_connection_problem(monkeypatch):
    def explode(journal, **kwargs):
        raise TypeError("a bug, not a network")

    monkeypatch.setattr("probe.sdk.journal.drain", explode)
    with pytest.raises(TypeError):
        imp._flush_uploads(Client([]), retry_network=False, report=Report())


def test_the_census_adapter_reports_into_the_scanning_phase():
    """`observe` counts files; the TUI wants a phase and a message."""
    said = []
    report = imp._census_progress(lambda message, **fields: said.append((message, fields)),
                                  "Verifying file contents")
    report(completed=120, total=1154, reused=0)
    report(completed=1154, total=1154, reused=1154)
    assert said[0][1] == {"phase": "scanning", "completed": 120, "total": 1154,
                           "stage": None, "stage_completed": None, "stage_total": None}
    assert "120 of 1,154" in said[0][0]
    assert "1,154 already verified" in said[1][0]


def test_no_progress_channel_means_no_adapter():
    assert imp._census_progress(None, "anything") is None
