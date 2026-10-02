"""Background unit delivery overlaps later reads and keeps receipt truth."""

from pathlib import Path
from threading import Event, get_ident

import pytest

from probe.cli import backfill, backfill_import, import_jobs
from probe.cli.backfill_coverage import Coverage, CoverageError
from probe.sdk.errors import TransportError
from tests import test_backfill_background as fixtures

background_harness = fixtures.background_harness


def _two_units(harness, queued):
    (harness.folder / "b.py").write_text("value = 2\n")
    harness.placement = lambda path: Path(path).stem
    harness.run(background=True)
    payload = queued[0]
    payload["concurrency"] = 2
    assert len(payload["units"]) == 2
    return payload


def test_first_receipt_advances_progress_before_the_last_unit_finishes(
    background_harness, monkeypatch,
):
    h, queued = background_harness
    payload = _two_units(h, queued)
    last_started, first_delivered = Event(), Event()
    launch = h.launch
    last_finished = False
    delivery_thread = get_ident()
    completions = []

    def read(folder, prompt, **kwargs):
        nonlocal last_finished
        if kwargs["label"] == "b":
            last_started.set()
            assert first_delivered.wait(10), "first unit stayed queued until all reads ended"
            result = launch(folder, prompt, **kwargs)
            last_finished = True
            return result
        assert last_started.wait(10)
        return launch(folder, prompt, **kwargs)

    def progress(message, **fields):
        done = fields.get("completion_completed")
        if done is not None:
            completions.append(done)
        if message == "Uploading reviewed files" and done == 1:
            assert get_ident() == delivery_thread
            assert not last_finished
            assert len(h.remote.calls) == 1 and h.remote.calls[0][1] == "a.py"
            first_delivered.set()

    monkeypatch.setattr(backfill, "launch_agent", read)
    backfill_import.run_background_job(payload, progress=progress)
    assert first_delivered.is_set() and last_finished
    assert completions == sorted(completions) and completions[-1] == 2
    assert h.report()["delivered"] == ["a.py", "b.py"]
    assert sorted(call[1] for call in h.remote.calls) == ["a.py", "b.py"]


@pytest.mark.parametrize("change", ["receipt", "outage"])
def test_delayed_monitor_cannot_overwrite_newer_delivery_progress(
    background_harness, monkeypatch, change,
):
    h, queued = background_harness
    payload = _two_units(h, queued)
    monitor_entered, delivery_changed, change_published = Event(), Event(), Event()
    delivery_thread = get_ident()
    launch = h.launch
    accept_receipt = Coverage.accept_receipt
    observations = []
    delayed = False

    def read(folder, prompt, **kwargs):
        if kwargs["label"] == "a":
            assert monitor_entered.wait(10)
        else:
            assert change_published.wait(10)
        return launch(folder, prompt, **kwargs)

    def accepted(coverage, correlation, receipt):
        accept_receipt(coverage, correlation, receipt)
        delivery_changed.set()

    def offline_drain(**kwargs):
        delivery_changed.set()
        raise ConnectionError("synthetic drain failure")

    def progress(message, **fields):
        nonlocal delayed
        if (get_ident() != delivery_thread and message == "Reading reviewed files"
                and not delayed):
            delayed = True
            assert fields["completion_completed"] == 0
            monitor_entered.set()
            assert delivery_changed.wait(10)
            # The older snapshot must publish before the delivery thread's
            # newer count/outage. Before serialization, the newer callback
            # could run here and this paused callback overwrote it afterward.
            change_published.wait(0.5)
        observations.append(fields)
        if (change == "receipt" and fields.get("completion_completed") == 1
                or change == "outage" and fields.get("waiting_for_connection")):
            change_published.set()

    monkeypatch.setattr(backfill, "launch_agent", read)
    if change == "receipt":
        monkeypatch.setattr(Coverage, "accept_receipt", accepted)
        backfill_import.run_background_job(payload, progress=progress)
    else:
        monkeypatch.setattr(h.client, "flush", offline_drain)
        with pytest.raises(import_jobs.RetryableJobError):
            backfill_import.run_background_job(payload, progress=progress)

    assert delayed and change_published.is_set()
    completions = [fields["completion_completed"] for fields in observations
                   if "completion_completed" in fields]
    assert completions == sorted(completions)
    if change == "receipt":
        assert completions[-1] == 2
    else:
        offline_at = next(index for index, fields in enumerate(observations)
                          if fields.get("waiting_for_connection"))
        assert all(fields.get("waiting_for_connection") for fields in observations[offline_at:])


@pytest.mark.parametrize("last_unit_ok", [True, False])
@pytest.mark.parametrize("failure_source", ["upload", "drain"])
def test_offline_delivery_finishes_inflight_reads_before_retrying_saved_uploads(
    background_harness, monkeypatch, last_unit_ok, failure_source,
):
    h, queued = background_harness
    payload = _two_units(h, queued)
    last_started, connection_failed = Event(), Event()
    launch = h.launch
    upload = h.remote.upload_fingerprinted
    flush = h.client.flush
    attempts = []
    observations = []

    def read(folder, prompt, **kwargs):
        if kwargs["label"] == "b":
            last_started.set()
            assert connection_failed.wait(10)
            _ok, tail = launch(folder, prompt, **kwargs)
            return last_unit_ok, tail
        assert last_started.wait(10)
        return launch(folder, prompt, **kwargs)

    def offline(*args, **kwargs):
        attempts.append(kwargs["digest"])
        raise TransportError("synthetic outage")

    def progress(message, **fields):
        observations.append(fields)
        if "continuing approved local reads" in message:
            connection_failed.set()

    monkeypatch.setattr(backfill, "launch_agent", read)
    if failure_source == "upload":
        monkeypatch.setattr(h.remote, "upload_fingerprinted", offline)
    else:
        def offline_drain(**kwargs):
            attempts.append("drain")
            raise ConnectionError("synthetic drain failure")

        monkeypatch.setattr(h.client, "flush", offline_drain)
    expected_error = import_jobs.RetryableJobError if last_unit_ok else CoverageError
    with pytest.raises(expected_error) as failure:
        backfill_import.run_background_job(payload, progress=progress)
    assert isinstance(failure.value, import_jobs.RetryableJobError) is last_unit_ok
    assert len(attempts) == 1, "later units should save locally without repeating a known failed drain"
    assert sorted(path for path, _content in h.manifested) == ["a.py", "b.py"]
    assert h.remote.calls == []
    offline_at = next(index for index, fields in enumerate(observations)
                      if fields.get("waiting_for_connection"))
    assert all(fields.get("waiting_for_connection") for fields in observations[offline_at:])
    pending = h.client._delivery_journal().pending()
    assert len(pending) == 2

    # Recovery uses saved manifests and immutable upload bodies, including the
    # second unit that finished while the connection was unavailable.
    monkeypatch.setattr(h.remote, "upload_fingerprinted", upload)
    monkeypatch.setattr(h.client, "flush", flush)
    monkeypatch.setattr(backfill, "launch_agent", lambda *a, **k: pytest.fail("re-read a saved manifest"))
    (h.folder / "unapproved.py").write_text("outside the reviewed inventory\n")
    backfill_import.run_background_job(payload, progress=lambda *a, **k: None)
    assert sorted(call[1] for call in h.remote.calls) == ["a.py", "b.py"]
    assert h.report()["delivered"] == ["a.py", "b.py"]
    assert h.report()["new"] == ["unapproved.py"]
