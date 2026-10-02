"""Several upload bodies move at once; everything that DECIDES stays serial.

presign -> PUT -> confirm is three round trips per file, and the drain did them
one file after another. These pin the narrow thing that became parallel and,
more importantly, the things that did not.
"""

from __future__ import annotations

import hashlib
import threading
import time
from types import SimpleNamespace

import pytest

from probe.sdk import journal as jm
from probe.sdk.journal import Journal, drain


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_ATTRIBUTION", raising=False)
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)


@pytest.fixture
def queue(tmp_path):
    return Journal.for_receipts(
        tmp_path / "outbox", context={"name": None, "base_url": "http://test"}
    )


class SlowStore:
    """Counts how many uploads are in the air at the same moment."""

    def __init__(self, delay=0.05):
        self.delay = delay
        self.lock = threading.Lock()
        self.in_flight = 0
        self.peak = 0
        self.concurrent = 0
        self.uploaded = []
        self.http = []
        self.records = {}
        self.transport = SimpleNamespace(request=self.reference)

    def upload_fingerprinted(self, anchor, anchor_id, name, path, *, digest, size, **kwargs):
        with self.lock:
            self.in_flight += 1
            self.peak = max(self.peak, self.in_flight)
            if self.in_flight > 1:
                self.concurrent += 1
        try:
            time.sleep(self.delay)
            with self.lock:
                self.uploaded.append(name)
            return self.records.setdefault(
                (anchor, anchor_id, name, digest),
                {"id": f"artifact-{name}", "name": name, "status": "complete",
                 "uri": f"r2://artifacts/{digest}", "content_hash": digest,
                 "size_bytes": size, "is_reference": False},
            )
        finally:
            with self.lock:
                self.in_flight -= 1

    def reference(self, method, path, *, json_body):
        with self.lock:
            self.http.append((method, path))
        return {**json_body, "id": f"ref-{len(self.http)}", "status": "complete"}


def stage(queue, tmp_path, count):
    expected = []
    for index in range(count):
        source = tmp_path / f"file{index}.bin"
        source.write_bytes(f"contents {index}".encode())
        queue.append_upload(
            correlation=f"scope:file{index}:v1",
            anchor="project", anchor_id="p1", name=f"src/file{index}.bin",
            src_path=str(source),
            expected_content_hash=hashlib.sha256(source.read_bytes()).hexdigest(),
        )
        expected.append(f"src/file{index}.bin")
    return expected


def test_several_uploads_are_in_the_air_at_once(queue, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "4")
    names = stage(queue, tmp_path, 8)
    store = SlowStore()
    report = drain(queue, client_factory=lambda _: store)
    assert report.delivered == 8
    assert sorted(store.uploaded) == sorted(names)
    assert store.peak > 1, "uploads were still strictly one at a time"
    assert queue.pending() == []


def test_one_worker_restores_the_strictly_serial_drain(queue, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "1")
    stage(queue, tmp_path, 5)
    store = SlowStore()
    assert drain(queue, client_factory=lambda _: store).delivered == 5
    assert store.peak == 1


def test_every_file_keeps_exactly_one_receipt_and_one_upload(queue, tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "4")
    names = stage(queue, tmp_path, 6)
    store = SlowStore(delay=0)
    drain(queue, client_factory=lambda _: store)
    for index in range(6):
        receipt = queue.receipt(f"scope:file{index}:v1")
        assert receipt and receipt["status"] == "complete"
    assert len(store.uploaded) == len(names)
    # A second drain has nothing to do, and must not PUT anything again.
    assert drain(queue, client_factory=lambda _: store).delivered == 0
    assert len(store.uploaded) == len(names)


def test_a_failing_upload_is_left_for_the_serial_pass_to_classify(queue, tmp_path, monkeypatch):
    """Workers decide nothing. A raise in the fast path changes no state."""
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "4")
    stage(queue, tmp_path, 4)

    class Breaks(SlowStore):
        def upload_fingerprinted(self, anchor, anchor_id, name, path, **kwargs):
            if name.endswith("file1.bin"):
                raise OSError("connection reset")
            return super().upload_fingerprinted(anchor, anchor_id, name, path, **kwargs)

    store = Breaks(delay=0)
    report = drain(queue, client_factory=lambda _: store)
    # The queue parks rather than dead-lettering, and the failure is reported
    # exactly once by the serial pass -- not four times by four threads.
    assert report.stopped_transient or report.dead_lettered
    assert queue.pending(), "a failed upload must stay queued"
    healthy = SlowStore(delay=0)
    assert drain(queue, client_factory=lambda _: healthy).delivered >= 1


def test_plain_http_operations_are_never_reordered(queue, tmp_path, monkeypatch):
    """Only correlated uploads fan out. An http op's order IS its meaning."""
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "4")
    for index in range(4):
        queue.append_http("POST", "/v1/projects/p1/artifacts",
                          {"name": f"ref{index}", "uri": f"file:///r{index}", "is_reference": True},
                          correlation=f"scope:ref{index}:v1")
    store = SlowStore(delay=0)
    assert drain(queue, client_factory=lambda _: store).delivered == 4
    assert store.peak <= 1
    assert [body for _, body in store.http] == ["/v1/projects/p1/artifacts"] * 4


def test_the_worker_count_is_bounded_and_survives_nonsense(monkeypatch):
    from probe.sdk.journal import _upload_workers

    monkeypatch.delenv("PROBE_UPLOAD_WORKERS", raising=False)
    assert _upload_workers() == 4
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "0")
    assert _upload_workers() == 1
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "9999")
    assert _upload_workers() == 32
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "not-a-number")
    assert _upload_workers() == 4


def test_the_window_refills_so_late_files_are_parallel_too(queue, tmp_path, monkeypatch):
    """The first version fetched ONE window and serialised everything after it.

    Caught by review, not by a test: every test here staged fewer operations
    than the window held, so the cliff was invisible. On a real import the
    window is a rounding error against the queue.
    """
    monkeypatch.setenv("PROBE_UPLOAD_WORKERS", "4")
    names = stage(queue, tmp_path, 40)
    store = SlowStore(delay=0.01)
    assert drain(queue, client_factory=lambda _: store).delivered == 40
    assert sorted(store.uploaded) == sorted(names)
    assert store.peak > 1
    assert store.concurrent >= 30, (
        f"only {store.concurrent} of 40 uploads had a peer in flight; the parallel "
        "window is not refilling as the drain advances"
    )
