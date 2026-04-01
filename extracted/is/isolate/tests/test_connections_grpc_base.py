import asyncio
import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from isolate.backends.local import LocalPythonEnvironment
from isolate.connections import LocalPythonGRPC
from isolate.logs import LogLevel, LogSource


def make_connection(tmp_path: Path) -> LocalPythonGRPC:
    environment = LocalPythonEnvironment()
    return LocalPythonGRPC(environment, tmp_path)


def test_abort_agent_logs_return_code_for_already_exited_process(
    tmp_path: Path,
) -> None:
    connection = make_connection(tmp_path)
    process = Mock()
    process.poll.return_value = 0
    process.returncode = 0
    connection._process = process

    connection.log = Mock()
    connection.abort_agent()

    process.terminate.assert_not_called()
    process.wait.assert_not_called()
    process.kill.assert_not_called()
    connection.log.assert_called_once_with(
        "Isolate agent finished (exit code: 0)",
        level=LogLevel.INFO,
        source=LogSource.BRIDGE,
    )
    assert connection._process is None


def test_abort_agent_logs_return_code_for_graceful_termination(tmp_path: Path) -> None:
    connection = make_connection(tmp_path)
    process = Mock()
    process.poll.return_value = None
    process.wait.return_value = -15
    connection._process = process

    connection.log = Mock()
    connection.abort_agent()

    process.terminate.assert_called_once()
    process.wait.assert_called_once()
    process.kill.assert_not_called()
    connection.log.assert_called_once_with(
        "Isolate agent finished (exit code: -15)",
        level=LogLevel.INFO,
        source=LogSource.BRIDGE,
    )
    assert connection._process is None


def test_abort_agent_logs_return_code_after_kill_fallback(tmp_path: Path) -> None:
    connection = make_connection(tmp_path)
    process = Mock()
    process.poll.return_value = None
    process.terminate.side_effect = RuntimeError("terminate failed")
    process.wait.return_value = -9
    connection._process = process

    connection.log = Mock()
    connection.abort_agent()

    process.terminate.assert_called_once()
    process.kill.assert_called_once()
    process.wait.assert_called_once()
    connection.log.assert_called_once_with(
        "Isolate agent finished (exit code: -9)",
        level=LogLevel.INFO,
        source=LogSource.BRIDGE,
    )
    assert connection._process is None


def test_agent_startup_logs_to_log_fd() -> None:
    """agent_startup.main() writes startup milestones to --log-fd."""
    import sys
    import tempfile

    from isolate.connections._local import agent_startup

    read_fd, write_fd = os.pipe()

    dummy_agent = tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False)
    dummy_agent.write("pass\n")
    dummy_agent.flush()
    dummy_agent.close()

    original_argv = sys.argv
    try:
        sys.argv = [
            "agent_startup.py",
            dummy_agent.name,
            "--log-fd",
            str(write_fd),
        ]
        agent_startup.main()
    finally:
        sys.argv = original_argv
        os.unlink(dummy_agent.name)

    # main() takes ownership of write_fd via os.fdopen, so it may already be closed
    try:
        os.close(write_fd)
    except OSError:
        pass

    with os.fdopen(read_fd, "r") as f:
        output = f.read()

    assert "Loading .pth files" in output
    assert "Running agent module" in output


def test_agent_startup_falls_back_to_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    """agent_startup.main() falls back to stderr when --log-fd is absent."""
    import sys
    import tempfile

    from isolate.connections._local import agent_startup

    dummy_agent = tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False)
    dummy_agent.write("pass\n")
    dummy_agent.flush()
    dummy_agent.close()

    original_argv = sys.argv
    try:
        sys.argv = [
            "agent_startup.py",
            dummy_agent.name,
        ]
        agent_startup.main()
    finally:
        sys.argv = original_argv
        os.unlink(dummy_agent.name)

    captured = capsys.readouterr()
    assert "Loading .pth files" in captured.err
    assert "Running agent module" in captured.err


def test_run_agent_logs_startup_milestones() -> None:
    """run_agent() writes startup progress to log_file."""
    import io

    from isolate.connections.grpc.agent import run_agent

    log_buffer = io.StringIO()

    async def noop():
        pass

    mock_server = Mock()
    mock_server.start = noop
    mock_server.wait_for_termination = noop

    mock_servicer = Mock()
    mock_servicer.wait_for_idle_timeout = noop

    with patch(
        "isolate.connections.grpc.agent.create_server", return_value=mock_server
    ), patch(
        "isolate.connections.grpc.agent.AgentServicer", return_value=mock_servicer
    ), patch("isolate.connections.grpc.agent.definitions"), patch(
        "isolate.connections.grpc.agent.os.fdopen", return_value=log_buffer
    ):
        asyncio.run(run_agent("localhost:50051", log_fd=99))

    output = log_buffer.getvalue()
    assert "Binding agent to localhost:50051" in output
    assert "Starting agent" in output
    assert "Agent is ready" in output


def test_create_server_raises_on_bind_failure() -> None:
    """create_server() raises RuntimeError when add_secure_port fails."""
    from grpc import aio
    from isolate.connections.grpc.agent import create_server

    with patch.object(aio, "server") as mock_aio_server, patch(
        "isolate.connections.grpc.agent.local_server_credentials"
    ):
        mock_server = Mock()
        mock_server.add_secure_port.return_value = 0
        mock_aio_server.return_value = mock_server

        with pytest.raises(RuntimeError, match="Failed to bind"):
            create_server("localhost:50051")
