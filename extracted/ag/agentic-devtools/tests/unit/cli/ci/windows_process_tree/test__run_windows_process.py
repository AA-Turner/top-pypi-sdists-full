import os
import subprocess
import sys
from collections.abc import Callable
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import windows_process_cleanup, windows_process_tree
from agentic_devtools.cli.ci.windows_process_tree import run_bounded_process


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process lifecycle")
def test_timeout_uses_returncode_observed_during_cleanup(monkeypatch: pytest.MonkeyPatch) -> None:
    command = [sys.executable, "-c", "pass"]
    process = Mock(returncode=None)
    timeout_error = subprocess.TimeoutExpired(command, 5, output="partial output")

    def cleanup(
        *_args: object, **_kwargs: object
    ) -> tuple[list[windows_process_tree.ProcessCleanupDiagnostic], str | None, str | None, None]:
        process.returncode = 17
        return [], None, None, None

    monkeypatch.setattr(windows_process_tree, "_start_windows_process", Mock(return_value=(process, 123)))
    monkeypatch.setattr(
        windows_process_tree,
        "_capture_process_result",
        Mock(return_value=("partial output", None, None, timeout_error)),
    )
    monkeypatch.setattr(windows_process_tree, "_cleanup_process", cleanup)

    with pytest.raises(subprocess.TimeoutExpired) as raised:
        getattr(windows_process_tree, "_run_windows_process")(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value is timeout_error
    assert getattr(raised.value, "returncode", None) == 17


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows process lifecycle")
def test_cleanup_cancellation_after_drain_failure_preserves_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    interruption = KeyboardInterrupt("cleanup cancellation")
    process = Mock(stdout=Mock(), stderr=Mock(), stdin=Mock(), returncode=0)
    process._handle = Mock()
    close_job = Mock()
    threads: list[Mock] = []

    def make_thread(*, target: Callable[[], None], daemon: bool) -> Mock:
        thread = Mock()
        thread.is_alive.return_value = False
        thread.start.side_effect = target
        thread.join.side_effect = interruption if not threads else None
        threads.append(thread)
        assert daemon
        return thread

    monkeypatch.setattr(windows_process_tree, "_start_windows_process", Mock(return_value=(process, 123)))
    monkeypatch.setattr(
        windows_process_tree,
        "_capture_process_result",
        Mock(return_value=("output", "error", 0, None)),
    )
    monkeypatch.setattr(windows_process_tree, "_active_process_count", Mock(return_value=0))
    monkeypatch.setattr(windows_process_tree, "_drain_process", Mock(side_effect=OSError("drain failure")))
    monkeypatch.setattr(windows_process_tree, "_reap_process", Mock())
    monkeypatch.setattr(windows_process_tree, "_close_job_object", close_job)
    monkeypatch.setattr(windows_process_cleanup.threading, "Thread", make_thread)

    with pytest.raises(KeyboardInterrupt) as raised:
        getattr(windows_process_tree, "_run_windows_process")(["tool"], cwd=None, env={}, timeout=5)

    assert raised.value is interruption
    assert getattr(raised.value, "output", None) == "output"
    assert getattr(raised.value, "stderr", None) == "error"
    cleanup_errors = getattr(raised.value, "cleanup_errors", ())
    assert tuple((item.stage, item.message) for item in cleanup_errors) == (
        ("drain", "drain failure"),
        ("close", "cleanup cancellation"),
    )
    close_job.assert_called_once_with(123)
    assert len(threads) == 3
    assert all(thread.join.call_count == 1 for thread in threads)
    process._handle.Close.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_job_query_failure_and_drain_timeout_preserve_timeout_primary(monkeypatch: pytest.MonkeyPatch) -> None:
    command = [sys.executable, "-c", "import sys; print('captured output'); sys.exit(9)"]
    monkeypatch.setattr(
        windows_process_tree,
        "_active_process_count",
        Mock(side_effect=OSError("injected job query failure")),
    )
    monkeypatch.setattr(windows_process_tree, "_terminate_process_tree", Mock())
    monkeypatch.setattr(
        windows_process_tree,
        "_drain_process",
        Mock(side_effect=subprocess.TimeoutExpired(command, 10, output=b"")),
    )

    with pytest.raises(subprocess.TimeoutExpired) as raised:
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value.cmd == command
    assert raised.value.timeout == 10
    assert raised.value.output == "captured output\n"
    assert getattr(raised.value, "returncode", None) == 9
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("terminate", "drain")


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_late_cancellation_with_drain_failure_preserves_captured_output(monkeypatch: pytest.MonkeyPatch) -> None:
    command = [sys.executable, "-c", "import sys; print('captured output'); print('captured error', file=sys.stderr)"]
    interruption = KeyboardInterrupt("injected late cancellation")
    monkeypatch.setattr(windows_process_tree, "_active_process_count", Mock(side_effect=interruption))
    monkeypatch.setattr(windows_process_tree, "_terminate_process_tree", Mock())
    monkeypatch.setattr(
        windows_process_tree,
        "_drain_process",
        Mock(side_effect=OSError("injected drain failure")),
    )

    with pytest.raises(KeyboardInterrupt) as raised:
        run_bounded_process(command, cwd=None, env=os.environ.copy(), timeout=5)

    assert raised.value is interruption
    assert getattr(raised.value, "output", None) == "captured output\n"
    assert getattr(raised.value, "stderr", None) == "captured error\n"
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("drain",)


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_reap_cancellation_preserves_cleanup_evidence_without_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    process = Mock(returncode=0)
    monkeypatch.setattr(windows_process_tree, "_start_windows_process", Mock(return_value=(process, 17)))
    monkeypatch.setattr(windows_process_tree, "_capture_process_result", Mock(return_value=(None, None, 0, None)))
    monkeypatch.setattr(windows_process_tree, "_active_process_count", Mock(return_value=1))
    monkeypatch.setattr(
        windows_process_tree,
        "_terminate_process_tree",
        Mock(side_effect=OSError("injected termination failure")),
    )
    drain = Mock(side_effect=[("recovered stdout", "recovered stderr"), OSError("retry drain failed")])
    monkeypatch.setattr(windows_process_tree, "_drain_process", drain)
    monkeypatch.setattr(
        windows_process_tree,
        "_reap_process",
        Mock(side_effect=[KeyboardInterrupt("reap interrupted"), None]),
    )
    close_resources = Mock(return_value=())
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", close_resources)

    with pytest.raises(KeyboardInterrupt, match="reap interrupted") as raised:
        getattr(windows_process_tree, "_run_windows_process")(["tool"], cwd=None, env={}, timeout=5)

    assert getattr(raised.value, "output", None) == "recovered stdout"
    assert getattr(raised.value, "stderr", None) == "recovered stderr"
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("terminate", "reap")
    drain.assert_called_once()
    assert close_resources.call_count == 2


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_capture_cancellation_merges_interrupted_cleanup_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    process = Mock(returncode=0)
    capture_cancellation = KeyboardInterrupt("capture interrupted")
    reap_cancellation = KeyboardInterrupt("reap interrupted")
    monkeypatch.setattr(windows_process_tree, "_start_windows_process", Mock(return_value=(process, 17)))
    monkeypatch.setattr(
        windows_process_tree,
        "_capture_process_result",
        Mock(side_effect=capture_cancellation),
    )
    monkeypatch.setattr(windows_process_tree, "_terminate_process_tree", Mock())
    drain = Mock(return_value=("recovered stdout", "recovered stderr"))
    reap = Mock(side_effect=reap_cancellation)
    monkeypatch.setattr(windows_process_tree, "_drain_process", drain)
    monkeypatch.setattr(windows_process_tree, "_reap_process", reap)
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", Mock(return_value=()))

    with pytest.raises(KeyboardInterrupt) as raised:
        getattr(windows_process_tree, "_run_windows_process")(["tool"], cwd=None, env={}, timeout=5)

    assert raised.value is capture_cancellation
    assert getattr(raised.value, "output", None) == "recovered stdout"
    assert getattr(raised.value, "stderr", None) == "recovered stderr"
    assert tuple((item.stage, item.message) for item in getattr(raised.value, "cleanup_errors", ())) == (
        ("reap", "reap interrupted"),
    )
    drain.assert_called_once()
    reap.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Requires native Windows Job Objects")
def test_close_cancellation_preserves_output_drained_after_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    process = Mock(returncode=0)
    timeout = subprocess.TimeoutExpired(["tool"], 5)
    close_error = KeyboardInterrupt("stream close interrupted")
    monkeypatch.setattr(windows_process_tree, "_start_windows_process", Mock(return_value=(process, 17)))
    monkeypatch.setattr(
        windows_process_tree,
        "_capture_process_result",
        Mock(return_value=(None, None, 0, timeout)),
    )
    monkeypatch.setattr(windows_process_tree, "_terminate_process_tree", Mock())
    monkeypatch.setattr(
        windows_process_tree,
        "_drain_process",
        Mock(return_value=("recovered stdout", "recovered stderr")),
    )
    monkeypatch.setattr(windows_process_tree, "_reap_process", Mock())
    monkeypatch.setattr(windows_process_tree, "_close_process_resources", Mock(side_effect=close_error))

    with pytest.raises(KeyboardInterrupt, match="stream close interrupted") as raised:
        getattr(windows_process_tree, "_run_windows_process")(["tool"], cwd=None, env={}, timeout=5)

    assert getattr(raised.value, "output", None) == "recovered stdout"
    assert getattr(raised.value, "stderr", None) == "recovered stderr"
    assert tuple(item.stage for item in getattr(raised.value, "cleanup_errors", ())) == ("close",)
