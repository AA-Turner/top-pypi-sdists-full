"""Exercise the local benchmark sink without importing or rebuilding the SDK."""

import gzip
import http.client
import importlib.util
import json
import queue
import threading
from pathlib import Path

import pytest


@pytest.fixture
def benchmark_module():
    sdk_root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "native_context_benchmark", sdk_root / "benchmarks/native_context_benchmark.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def benchmark_server(monkeypatch, benchmark_module):
    module = benchmark_module
    sdk_root = Path(__file__).resolve().parents[1]
    ready = queue.Queue()
    errors = []

    class TestServer(module.HTTPServer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            ready.put(self)

        def handle_error(self, request, client_address):
            errors.append(True)

    monkeypatch.setattr(module, "HTTPServer", TestServer)
    thread = threading.Thread(
        target=module.serve,
        args=(str(sdk_root.parent / "statsig-rust/tests/data/eval_proj_dcs.json"),),
        daemon=True,
    )
    thread.start()
    server = ready.get(timeout=10)

    def request(method, path, body=None, headers=None):
        connection = http.client.HTTPConnection(
            "127.0.0.1", server.server_port, timeout=5
        )
        try:
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            assert response.status == 200
            return json.loads(response.read())
        finally:
            connection.close()

    try:
        yield request, errors
    finally:
        server.shutdown()
        thread.join(timeout=10)
        server.server_close()
        assert not thread.is_alive()


def test_empty_id_list_manifest_does_not_change_event_counts(benchmark_server):
    request, errors = benchmark_server
    event = {"eventName": "statsig::gate_exposure"}
    assert request("POST", "/events", json.dumps({"events": [event]})) == {
        "success": True
    }
    for path in ("/v1/get_id_lists", "/v1/get_id_lists?sinceTime=0"):
        assert request("POST", path, b"") == {}
    assert request("GET", "/counts") == {"statsig::gate_exposure": 1}
    assert request(
        "POST",
        "/v1/log_event",
        gzip.compress(json.dumps({"events": [event, event]}).encode()),
        {"Content-Encoding": "gzip"},
    ) == {"success": True}
    assert request("GET", "/counts") == {"statsig::gate_exposure": 3}
    assert errors == []


def test_malformed_event_batch_still_fails(benchmark_server):
    request, errors = benchmark_server
    with pytest.raises(http.client.RemoteDisconnected):
        request("POST", "/v1/log_event", b"not-json")
    assert request("GET", "/counts") == {}
    assert errors == [True]


def test_drain_flushes_partial_batch_published_after_first_manual_flush(
    benchmark_module, monkeypatch
):
    monkeypatch.setattr(benchmark_module.time, "sleep", lambda _: None)

    class SDK:
        pending = 3
        delivered = 0
        flushes = 0
        published_partial = False

        def flush_events(self):
            self.flushes += 1
            self.delivered += self.pending
            self.pending = 0
            return self

        def wait(self, timeout):
            assert 0 < timeout <= 10
            return True

        def event_counts(self):
            # The first manual flush has completed. A racing automatic task now
            # publishes its partial batch; only another flush will deliver it.
            if not self.published_partial:
                self.pending = 2
                self.published_partial = True
            return {"statsig::gate_exposure": self.delivered}

    sdk = SDK()
    counts = benchmark_module.drain_sdk_events(
        sdk, sdk.event_counts, ("statsig::gate_exposure", 5)
    )
    assert counts == {"statsig::gate_exposure": 5}
    assert sdk.flushes == 2
    assert sdk.pending == 0


def test_drain_keeps_deadline_when_expected_events_never_arrive(
    benchmark_module, monkeypatch
):
    now = [0.0]
    monkeypatch.setattr(benchmark_module.time, "monotonic", lambda: now[0])
    monkeypatch.setattr(
        benchmark_module.time, "sleep", lambda _: now.__setitem__(0, now[0] + 1)
    )

    class SDK:
        def flush_events(self):
            return self

        def wait(self, timeout):
            assert 0 < timeout <= 10
            return True

    with pytest.raises(AssertionError, match="Exposures did not finish"):
        benchmark_module.drain_sdk_events(
            SDK(), dict, ("statsig::gate_exposure", 1)
        )
    assert now[0] == 10
