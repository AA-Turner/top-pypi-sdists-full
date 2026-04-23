import multiprocessing
import os
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock

import pytest
import tokens

import zign.api


def test_is_valid():
    now = time.time()
    assert not zign.api.is_valid({})
    assert not zign.api.is_valid({"creation_time": now - 3610, "expires_in": 3600})
    assert zign.api.is_valid({"creation_time": now - 100, "expires_in": 600})
    # still valid for 2 minutes, but we only return tokens valid for at least 5 more minutes
    assert not zign.api.is_valid({"creation_time": now - 3480, "expires_in": 3600})


def test_get_named_token_deprecated(monkeypatch):
    logger = MagicMock()
    monkeypatch.setattr("zign.api.get_token", lambda x, y: "mytok701")
    monkeypatch.setattr("zign.api.logger", logger)
    token = zign.api.get_named_token(
        "myrealm", ["myscope"], "myuser", "mypass", "http://example.org"
    )
    assert "mytok701" == token["access_token"]
    logger.warning.assert_called_with(
        '"get_named_token" is deprecated, please use "zign.api.get_token" instead'
    )


def test_get_new_token_server_error(monkeypatch):
    response = MagicMock(status_code=500)
    monkeypatch.setattr("requests.get", MagicMock(return_value=response))
    with pytest.raises(zign.api.ServerError) as excinfo:
        zign.api.get_new_token(
            "myrealm", ["myscope"], "myuser", "mypass", "http://example.org"
        )

    assert "Server error: Token Service returned HTTP status 500" in str(excinfo.value)


def test_get_new_token_invalid_json(monkeypatch):
    response = MagicMock(status_code=200)
    response.json.side_effect = ValueError("invalid JSON!")
    monkeypatch.setattr("requests.get", MagicMock(return_value=response))
    with pytest.raises(zign.api.ServerError):
        zign.api.get_new_token(
            "myrealm", ["myscope"], "myuser", "mypass", "http://example.org"
        )


def test_get_new_token_missing_access_token(monkeypatch):
    response = MagicMock(status_code=200)
    response.json.return_value = {}
    monkeypatch.setattr("requests.get", MagicMock(return_value=response))
    with pytest.raises(zign.api.ServerError):
        zign.api.get_new_token(
            "myrealm", ["myscope"], "myuser", "mypass", "http://example.org"
        )


def test_get_token_existing(monkeypatch):
    monkeypatch.setattr(
        "zign.api.get_existing_token", lambda x: {"access_token": "tt77"}
    )
    assert zign.api.get_token("mytok", ["myscope"]) == "tt77"


def test_get_token_service_success(monkeypatch):
    monkeypatch.setattr("tokens.get", lambda x: "svc123")

    assert zign.api.get_token("mytok", ["myscope"]) == "svc123"


def test_get_token_fallback_success(monkeypatch):
    def get_token(name):
        raise tokens.ConfigurationError("TEST")

    monkeypatch.setattr("tokens.get", get_token)
    monkeypatch.setattr(
        "zign.api.get_token_implicit_flow",
        lambda *args, **kwargs: {"access_token": "tt77"},
    )

    assert zign.api.get_token("mytok", ["myscope"]) == "tt77"


def test_get_named_token_existing(monkeypatch):
    existing = {
        "mytok": {
            "access_token": "tt77",
            "creation_time": time.time() - 10,
            "expires_in": 3600,
        }
    }
    monkeypatch.setattr("zign.api.get_tokens", lambda: existing)
    tok = zign.api.get_named_token(
        scope=["myscope"], realm=None, name="mytok", user="myusr", password="mypw"
    )
    assert tok["access_token"] == "tt77"


def test_get_named_token_services(monkeypatch):
    response = MagicMock(status_code=401)
    monkeypatch.setattr("requests.get", MagicMock(return_value=response))
    monkeypatch.setattr("tokens.get", lambda x: "svcmytok123")
    tok = zign.api.get_named_token(
        scope=["myscope"], realm=None, name="mytok", user="myusr", password="mypw"
    )
    assert tok["access_token"] == "svcmytok123"


def test_backwards_compatible_get_config(monkeypatch):
    load_config = MagicMock()
    load_config.return_value = {"url": "http://localhost"}
    monkeypatch.setattr("stups_cli.config.load_config", load_config)
    assert {"url": "http://localhost"} == zign.api.get_config()
    load_config.assert_called_with("zign")


def test_get_config(monkeypatch):
    load_config = MagicMock()
    load_config.return_value = {}
    store_config = MagicMock()

    def prompt(message, **kwargs):
        # just return the prompt text for easy assertion
        return message

    monkeypatch.setattr("stups_cli.config.load_config", load_config)
    monkeypatch.setattr("stups_cli.config.store_config", store_config)
    monkeypatch.setattr("click.prompt", prompt)
    monkeypatch.setattr("requests.get", lambda x, timeout: None)
    config = zign.api.get_config(zign.config.CONFIG_NAME)
    expected_config = {
        "authorize_url": "Please enter the OAuth 2 Authorization Endpoint URL",
        "business_partner_id": "Please enter the Business Partner ID",
        "client_id": "Please enter the OAuth 2 Client ID",
        "token_url": "Please enter the OAuth 2 Token Endpoint URL",
    }
    assert config == expected_config


def test_token_implicit_flow(monkeypatch):
    access_token = "myacctok"

    def webbrowser_open(url, **kwargs):
        assert (
            url
            == "https://localhost/authorize?business_partner_id=123&client_id=foobar&redirect_uri=http://localhost:8081&response_type=token"
        )

    server = MagicMock()
    server.return_value.query_params = {
        "access_token": access_token,
        "refresh_token": "foo",
        "expires_in": 3600,
        "token_type": "Bearer",
    }

    load_config = MagicMock()
    load_config.return_value = {
        "authorize_url": "https://localhost/authorize",
        "token_url": "https://localhost/token",
        "client_id": "foobar",
        "business_partner_id": "123",
    }
    monkeypatch.setattr("stups_cli.config.load_config", load_config)
    monkeypatch.setattr("zign.api.load_config_ztoken", lambda x: {})
    monkeypatch.setattr("webbrowser.open", webbrowser_open)
    monkeypatch.setattr("zign.api.ClientRedirectServer", server)
    token = zign.api.get_token_implicit_flow("test_token_implicit_flow")
    assert access_token == token["access_token"]


def test_file_lock_serializes_threads():
    """Test that file_lock provides mutual exclusion between threads.

    Uses a threading.Barrier(2) inside the critical section: if both threads
    were inside the lock simultaneously, both would reach the barrier and pass.
    Instead, the first thread times out alone at the barrier, proving only one
    thread was inside the lock at a time.

    We track each thread's entry time into the critical section. If the lock
    serializes correctly, the second thread enters only after the first has
    left (i.e., after the barrier timeout), so the entries don't overlap.

    Two possible outcomes per thread, three in total:
    - "alone":       timed out at the barrier — the other thread didn’t arrive in time
    - "both_inside": both threads were inside the lock at the same time (failure)
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_path = os.path.join(tmpdir, "test.lock")
        barrier = threading.Barrier(2, timeout=0.2)
        results = []
        entry_times = []

        def worker():
            with zign.api.file_lock(lock_path):
                entry_times.append(time.monotonic())
                try:
                    barrier.wait()
                    results.append("both_inside")
                except threading.BrokenBarrierError:
                    results.append("alone")

        with ThreadPoolExecutor(max_workers=2) as pool:
            pool.submit(worker)
            pool.submit(worker)

        assert results == ["alone", "alone"], (
            f"Expected both threads to time out alone at the barrier, proving "
            f"serialization. Got: {results}"
        )
        # The second thread must have entered after the first's barrier timeout
        # (~0.2s), proving it was blocked by the lock, not just slow to start.
        gap = abs(entry_times[1] - entry_times[0])
        assert gap >= 0.15, (
            f"Threads entered the critical section only {gap:.3f}s apart; "
            f"expected ≥0.15s (the barrier timeout), proving the lock held"
        )


def test_file_lock_serializes_processes():
    with tempfile.TemporaryDirectory() as tmpdir:
        lock_path = os.path.join(tmpdir, "test.lock")

        # Passed to the child processes for them to synchronize.
        barrier = multiprocessing.Barrier(2)

        # Queues to collect data from processes (we can't share lists directly).
        results_queue = multiprocessing.Queue()
        times_queue = multiprocessing.Queue()

        # Start two identical workers:
        p1 = multiprocessing.Process(
            target=_barrier_worker,
            args=(lock_path, barrier, results_queue, times_queue),
        )
        p2 = multiprocessing.Process(
            target=_barrier_worker,
            args=(lock_path, barrier, results_queue, times_queue),
        )
        p1.start()
        p2.start()

        # Wait for them to finish (should be much faster than 2s):
        p1.join(timeout=2)
        p2.join(timeout=2)

        # Ensure they are dead
        if p1.is_alive():
            p1.terminate()
        if p2.is_alive():
            p2.terminate()

        results = []
        while not results_queue.empty():
            results.append(results_queue.get())
        entry_times = []
        while not times_queue.empty():
            entry_times.append(times_queue.get())
        entry_times.sort()

        # Both processes should have reported "alone" (i.e. broken barrier):
        assert len(results) == 2, f"Expected 2 results, got {results}"
        assert results == ["alone", "alone"], (
            f"Processes met at the barrier! This means both were in the lock "
            f"at the same time. Got: {results}"
        )
        # Check timing gap. If P1 enters at T=0 and waits 0.2s, P2 cannot enter until T=0.2s.
        # Therefore, the gap between entry times must be >= 0.2s.
        assert len(entry_times) == 2
        gap = entry_times[1] - entry_times[0]
        assert gap > 0.19, f"Processes entered too close together ({gap:.3f}s)."


# Worker task for test_file_lock_serializes_processes_barrier
# (must be at module level for pickling)
def _barrier_worker(lock_path, barrier, results_queue, times_queue):
    """
    Tries to enter lock and meet at the barrier.
    If lock works, we should time out (BrokenBarrierError) because the other process is blocked outside.
    """
    try:
        with zign.api.file_lock(lock_path):
            # Record entry time
            times_queue.put(time.monotonic())
            try:
                # Wait for the other process to join us inside the lock.
                # If serialization works, the other process CANNOT join us,
                # so this MUST time out.
                barrier.wait(timeout=0.2)
                results_queue.put("both_inside")  # Failure case
            except threading.BrokenBarrierError:
                # (Weirdly multiprocessing reuses the same exception as threading.Barrier.)
                results_queue.put("alone")  # Success case
    except Exception as e:
        # Catch unexpected errors (like lock acquisition failure)
        results_queue.put(f"ERROR: {e}")
