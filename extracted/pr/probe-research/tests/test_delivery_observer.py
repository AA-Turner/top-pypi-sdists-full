"""Completion observers run only after durable SDK delivery and queue removal."""

from pathlib import Path

import pytest

from probe.sdk import journal as jm
from probe.sdk.client import Client
from probe.sdk.config import Settings
from tests import test_backfill_delivery as delivery_fixtures

Crash = delivery_fixtures.Crash
Store = delivery_fixtures.Store
enqueue = delivery_fixtures.enqueue
isolated = delivery_fixtures.isolated
queue = delivery_fixtures.queue


def test_client_flush_observes_receipt_namespace_after_durable_removal(tmp_path, monkeypatch):
    client = Client(
        settings=Settings(base_url="http://test", token="synthetic"),
        spool_dir=tmp_path / "outbox", async_writes=False, auto_drain=False,
    )
    source = tmp_path / "source.py"
    source.write_text("synthetic")
    client.enqueue_artifact_upload(
        correlation="approved-file", anchor="project", anchor_id="p1", name="source.py", path=source,
    )
    store = Store()
    monkeypatch.setattr(client, "_outbox_client_factory", lambda: lambda _: store)
    observed = []

    def completed(correlation):
        observed.append((correlation, client.delivery_state(correlation), client.journal.pending()))

    assert client.flush(on_delivered=completed) == 1
    assert len(observed) == 1
    correlation, receipt, pending = observed[0]
    assert correlation == "approved-file" and receipt["state"] == "delivered"
    assert receipt["readable"] is True and receipt["status"] == "complete"
    assert not pending and not client._delivery_journal().pending()


def test_callback_failure_does_not_undo_or_interrupt_delivery(queue, tmp_path):
    enqueue(queue, tmp_path)
    queue.append_upload(
        correlation="second", anchor="project", anchor_id="p1", name="second.py",
        src_path=str(tmp_path / "source.py"),
    )
    observed = []

    def broken_observer(correlation):
        observed.append(correlation)
        raise RuntimeError("progress display unavailable")

    report = jm.drain(queue, client_factory=lambda _: Store(), on_delivered=broken_observer)
    assert report.delivered == 2 and report.remaining == 0 and not report.errors
    assert observed == ["scope:file:v1", "second"]
    assert queue.receipt("scope:file:v1") and queue.receipt("second")


@pytest.mark.parametrize("failure", ["receipt", "incomplete"])
def test_no_completion_notification_before_verified_receipt(queue, tmp_path, monkeypatch, failure):
    enqueue(queue, tmp_path)
    store = Store()
    if failure == "receipt":
        def fail_receipt(conn):
            raise OSError("synthetic disk full")

        monkeypatch.setattr(jm.Journal, "_commit_receipt_index", staticmethod(fail_receipt))
    else:
        upload = store.upload_fingerprinted
        store.upload_fingerprinted = lambda *a, **kw: {**upload(*a, **kw), "status": "pending"}
    observed = []
    report = jm.drain(queue, client_factory=lambda _: store, on_delivered=observed.append)
    assert report.delivered == 0 and report.remaining == 1
    assert not observed and queue.receipt("scope:file:v1") is None


def test_receipt_before_removal_recovery_notifies_without_remote_replay(
    queue, tmp_path, monkeypatch,
):
    enqueue(queue, tmp_path)
    store, observed = Store(), []
    unlink = Path.unlink

    def crash_removal(path, *args, **kwargs):
        if path.parent == queue.ops_dir:
            raise Crash()
        return unlink(path, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(Path, "unlink", crash_removal)
        with pytest.raises(Crash):
            jm.drain(queue, client_factory=lambda _: store, on_delivered=observed.append)
    assert queue.receipt("scope:file:v1") and queue.pending() and not observed
    report = jm.drain(queue, client_factory=lambda _: store, on_delivered=observed.append)
    assert report.delivered == 1 and observed == ["scope:file:v1"]
    assert len(store.calls) == 1 and not queue.pending()
