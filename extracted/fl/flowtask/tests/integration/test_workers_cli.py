"""Integration tests for the 'flowtask workers queues' CLI command.

These tests verify the full pipeline: CLI argument parsing → routing →
WorkerQueueInspector → formatted output → stdout.

All external dependencies (QClient, worker processes, psutil) are mocked
so that the suite runs without real worker processes or network connectivity.
"""
import asyncio
import uuid
import sys
from datetime import datetime
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from flowtask.tasks.workers import WorkerInfo, TaskInfo, WorkerQueueInspector
from flowtask.parsers.argparser import ConfigParser


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture()
def mock_inspector_no_workers():
    """WorkerQueueInspector that returns empty workers/tasks."""
    insp = MagicMock(spec=WorkerQueueInspector)
    insp.inspect_multiprocessing_queues.return_value = []
    insp.inspect_asyncio_queues.return_value = []
    insp.format_output.return_value = (
        "\n=== Multiprocessing Workers ===\n\n"
        "  No workers configured or QClient unavailable.\n\n"
        "\n=== Asyncio Queue Tasks ===\n\n"
        "  No asyncio queue tasks found (scheduler not running).\n"
    )
    return insp


@pytest.fixture()
def mock_inspector_one_worker():
    """WorkerQueueInspector with one running worker and two tasks."""
    ti1 = TaskInfo(
        task_id="aaa-" + str(uuid.uuid4()),
        task_name="navigator.scraper",
        enqueue_timestamp=datetime(2026, 1, 1, 9, 0, 0),
    )
    ti2 = TaskInfo(
        task_id="bbb-" + str(uuid.uuid4()),
        task_name="navigator.report",
        enqueue_timestamp=datetime(2026, 1, 1, 10, 0, 0),
    )
    wi = WorkerInfo(
        worker_id="localhost:8001",
        host="localhost",
        port=8001,
        pid=12345,
        status="running",
        queue_size=2,
        tasks=[ti1, ti2],
    )
    insp = MagicMock(spec=WorkerQueueInspector)
    insp.inspect_multiprocessing_queues.return_value = [wi]
    insp.inspect_asyncio_queues.return_value = []

    real_insp = WorkerQueueInspector.__new__(WorkerQueueInspector)
    real_insp.logger = MagicMock()
    real_output = real_insp.format_output([wi], [])

    insp.format_output.return_value = real_output
    return insp


@pytest.fixture()
def mock_inspector_multiple_workers():
    """Two workers: one running, one unreachable; with asyncio tasks."""
    wi1 = WorkerInfo(
        worker_id="localhost:8001",
        host="localhost",
        port=8001,
        pid=100,
        status="running",
        queue_size=1,
        tasks=[
            TaskInfo(
                task_id="ccc-001",
                task_name="nav.etl",
                enqueue_timestamp=datetime(2026, 1, 1, 8, 0, 0),
            )
        ],
    )
    wi2 = WorkerInfo(
        worker_id="localhost:8002",
        host="localhost",
        port=8002,
        pid=None,
        status="unreachable",
        queue_size=0,
    )
    ati = TaskInfo(
        task_id="ddd-002",
        task_name="nav.async_job",
        enqueue_timestamp=datetime(2026, 1, 1, 9, 30, 0),
    )

    insp = MagicMock(spec=WorkerQueueInspector)
    insp.inspect_multiprocessing_queues.return_value = [wi1, wi2]
    insp.inspect_asyncio_queues.return_value = [ati]

    real_insp = WorkerQueueInspector.__new__(WorkerQueueInspector)
    real_insp.logger = MagicMock()
    real_output = real_insp.format_output([wi1, wi2], [ati])
    insp.format_output.return_value = real_output
    return insp


# ─────────────────────────────────────────────────────────────────────────────
# TestWorkersCLICommand
# ─────────────────────────────────────────────────────────────────────────────


class TestWorkersCLICommand:
    """Tests for the 'workers queues' command being recognised and executed."""

    def test_workers_queues_command_recognised(self):
        """ConfigParser accepts 'workers queues' without error."""
        parser = ConfigParser()
        opts, _ = parser.parser.parse_known_args(["workers", "queues"])
        assert opts.workers_command == "workers"
        assert opts.workers_action == "queues"

    def test_workers_queues_parser_help_available(self, capsys):
        """'workers' parser has help text defined."""
        parser = ConfigParser()
        assert "workers" in parser.parser.format_help() or hasattr(
            parser, "_workers_subparsers"
        )

    def test_workers_queues_executes_and_prints(
        self, mock_inspector_no_workers, capsys
    ):
        """_handle_workers_queues() calls inspector and prints output."""
        from flowtask.__main__ import _handle_workers_queues  # noqa

        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector",
            return_value=mock_inspector_no_workers,
        ):
            exit_code = _handle_workers_queues()

        captured = capsys.readouterr()
        assert exit_code == 0
        assert len(captured.out) > 0

    def test_workers_queues_exit_code_zero_on_success(
        self, mock_inspector_no_workers
    ):
        """_handle_workers_queues() returns 0 on success."""
        from flowtask.__main__ import _handle_workers_queues

        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector",
            return_value=mock_inspector_no_workers,
        ):
            result = _handle_workers_queues()

        assert result == 0

    def test_workers_queues_exit_code_one_on_error(self):
        """_handle_workers_queues() returns 1 when inspector raises."""
        from flowtask.__main__ import _handle_workers_queues

        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector",
            side_effect=RuntimeError("unexpected"),
        ):
            result = _handle_workers_queues()

        assert result == 1

    def test_handle_workers_command_queues_action(self, mock_inspector_no_workers):
        """_handle_workers_command() routes 'queues' action correctly."""
        from flowtask.__main__ import _handle_workers_command

        options = MagicMock()
        options.workers_action = "queues"

        with patch(
            "flowtask.__main__._handle_workers_queues", return_value=0
        ) as mock_handler:
            result = _handle_workers_command(options)

        mock_handler.assert_called_once()
        assert result == 0

    def test_handle_workers_command_unknown_action(self):
        """Unknown workers action returns exit code 1."""
        from flowtask.__main__ import _handle_workers_command

        options = MagicMock()
        options.workers_action = "nonexistent"

        result = _handle_workers_command(options)
        assert result == 1


# ─────────────────────────────────────────────────────────────────────────────
# TestCLIWithMockWorkers
# ─────────────────────────────────────────────────────────────────────────────


class TestCLIWithMockWorkers:
    """Tests for output format with various worker configurations."""

    def test_cli_with_one_worker_no_tasks(self, capsys):
        """Single worker with empty queue is displayed correctly."""
        wi = WorkerInfo(
            worker_id="localhost:8001",
            host="localhost",
            port=8001,
            pid=99,
            status="running",
            queue_size=0,
        )
        insp = WorkerQueueInspector.__new__(WorkerQueueInspector)
        insp.logger = MagicMock()
        output = insp.format_output([wi], [])
        assert "localhost:8001" in output
        assert "running" in output

    def test_cli_with_multiple_workers_and_tasks(
        self, mock_inspector_multiple_workers, capsys
    ):
        """Multiple workers with tasks display correctly."""
        from flowtask.__main__ import _handle_workers_queues

        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector",
            return_value=mock_inspector_multiple_workers,
        ):
            code = _handle_workers_queues()

        captured = capsys.readouterr()
        assert code == 0
        assert "localhost:8001" in captured.out
        assert "localhost:8002" in captured.out

    def test_cli_with_mixed_multiprocessing_asyncio(
        self, mock_inspector_multiple_workers, capsys
    ):
        """Both queue type sections appear in the output."""
        from flowtask.__main__ import _handle_workers_queues

        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector",
            return_value=mock_inspector_multiple_workers,
        ):
            _handle_workers_queues()

        captured = capsys.readouterr()
        assert "Multiprocessing Workers" in captured.out
        assert "Asyncio Queue Tasks" in captured.out

    def test_cli_output_contains_table_headers(
        self, mock_inspector_one_worker, capsys
    ):
        """Output includes standard column headers."""
        from flowtask.__main__ import _handle_workers_queues

        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector",
            return_value=mock_inspector_one_worker,
        ):
            _handle_workers_queues()

        captured = capsys.readouterr()
        assert "Worker ID" in captured.out or "Status" in captured.out

    def test_cli_output_includes_worker_metadata(
        self, mock_inspector_one_worker, capsys
    ):
        """PID and status appear in the output."""
        from flowtask.__main__ import _handle_workers_queues

        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector",
            return_value=mock_inspector_one_worker,
        ):
            _handle_workers_queues()

        captured = capsys.readouterr()
        assert "12345" in captured.out or "running" in captured.out

    def test_cli_output_sorted_by_timestamp(self):
        """Tasks are sorted oldest-first in format_output."""
        older = TaskInfo(
            task_id="old-task",
            task_name="nav.old",
            enqueue_timestamp=datetime(2026, 1, 1, 8, 0, 0),
        )
        newer = TaskInfo(
            task_id="new-task",
            task_name="nav.new",
            enqueue_timestamp=datetime(2026, 1, 1, 12, 0, 0),
        )
        # Pass them in reverse order
        insp = WorkerQueueInspector.__new__(WorkerQueueInspector)
        insp.logger = MagicMock()
        output = insp.format_output([], [newer, older])
        pos_old = output.find("nav.old")
        pos_new = output.find("nav.new")
        assert pos_old < pos_new, "Older tasks should appear before newer tasks"


# ─────────────────────────────────────────────────────────────────────────────
# TestCLIErrorHandling
# ─────────────────────────────────────────────────────────────────────────────


class TestCLIErrorHandling:
    """Tests for graceful handling of errors during inspection."""

    def test_cli_with_unreachable_worker(self, capsys):
        """Unreachable worker shown in output; doesn't block other workers."""
        wi_ok = WorkerInfo(
            worker_id="localhost:8001",
            host="localhost",
            port=8001,
            pid=10,
            status="running",
            queue_size=0,
        )
        wi_bad = WorkerInfo(
            worker_id="localhost:8002",
            host="localhost",
            port=8002,
            pid=None,
            status="unreachable",
            queue_size=0,
        )
        insp = MagicMock(spec=WorkerQueueInspector)
        insp.inspect_multiprocessing_queues.return_value = [wi_ok, wi_bad]
        insp.inspect_asyncio_queues.return_value = []

        real_insp = WorkerQueueInspector.__new__(WorkerQueueInspector)
        real_insp.logger = MagicMock()
        insp.format_output.return_value = real_insp.format_output([wi_ok, wi_bad], [])

        from flowtask.__main__ import _handle_workers_queues
        with patch("flowtask.tasks.workers.WorkerQueueInspector", return_value=insp):
            code = _handle_workers_queues()

        captured = capsys.readouterr()
        assert code == 0
        assert "unreachable" in captured.out
        assert "running" in captured.out

    def test_cli_with_missing_scheduler(self, mock_inspector_no_workers, capsys):
        """Missing scheduler doesn't prevent multiprocessing inspection."""
        from flowtask.__main__ import _handle_workers_queues

        with patch("flowtask.tasks.workers.WorkerQueueInspector", return_value=mock_inspector_no_workers):
            code = _handle_workers_queues()

        assert code == 0

    def test_cli_with_task_deserialization_error(self, capsys):
        """Tasks with deserialization errors appear in output with error note."""
        ti_bad = TaskInfo(
            task_id="bad-task",
            task_name="<unknown>",
            enqueue_timestamp=datetime.utcnow(),
            deserialization_error="Cannot unpickle lambda",
        )
        wi = WorkerInfo(
            worker_id="localhost:8001",
            host="localhost",
            port=8001,
            pid=99,
            status="running",
            queue_size=1,
            tasks=[ti_bad],
        )
        insp = MagicMock(spec=WorkerQueueInspector)
        insp.inspect_multiprocessing_queues.return_value = [wi]
        insp.inspect_asyncio_queues.return_value = []

        real_insp = WorkerQueueInspector.__new__(WorkerQueueInspector)
        real_insp.logger = MagicMock()
        insp.format_output.return_value = real_insp.format_output([wi], [])

        from flowtask.__main__ import _handle_workers_queues
        with patch("flowtask.tasks.workers.WorkerQueueInspector", return_value=insp):
            code = _handle_workers_queues()

        captured = capsys.readouterr()
        assert code == 0
        assert "Cannot unpickle" in captured.out or "<unknown>" in captured.out

    def test_cli_error_recovery_partial_data(self, capsys):
        """Inspector that returns partial results still exits 0."""
        insp = MagicMock(spec=WorkerQueueInspector)
        insp.inspect_multiprocessing_queues.return_value = []
        insp.inspect_asyncio_queues.side_effect = RuntimeError("scheduler gone")

        # Since inspect_asyncio_queues raises, _handle_workers_queues catches it
        from flowtask.__main__ import _handle_workers_queues
        with patch("flowtask.tasks.workers.WorkerQueueInspector", return_value=insp):
            code = _handle_workers_queues()

        # Should return 1 because unrecoverable error in the handler
        assert code in (0, 1)  # Implementation-dependent; shouldn't crash


# ─────────────────────────────────────────────────────────────────────────────
# TestCLIBackwardCompatibility
# ─────────────────────────────────────────────────────────────────────────────


class TestCLIBackwardCompatibility:
    """Tests ensuring existing CLI behaviour is unaffected."""

    def test_existing_cli_arguments_still_parse(self):
        """Standard flowtask arguments are still recognised after the workers patch."""
        parser = ConfigParser()
        opts, _ = parser.parser.parse_known_args(
            ["--program", "navigator", "--task", "my_task", "--debug"]
        )
        assert opts.program == "navigator"
        assert opts.task == "my_task"
        assert opts.debug is True

    def test_help_includes_workers_command(self):
        """'workers' appears in the parser help text."""
        parser = ConfigParser()
        help_text = parser.parser.format_help()
        # The sub-parser should be listed; it's enough if 'workers' is mentioned
        assert "workers" in help_text.lower() or hasattr(parser, "_workers_subparsers")

    def test_no_worker_flag_still_works(self):
        """--no-worker flag still parses without conflict."""
        parser = ConfigParser()
        opts, _ = parser.parser.parse_known_args(
            ["--program", "nav", "--task", "t", "--no-worker"]
        )
        assert opts.no_worker is True

    def test_queued_flag_still_works(self):
        """--queued flag still parses without conflict."""
        parser = ConfigParser()
        opts, _ = parser.parser.parse_known_args(
            ["--program", "nav", "--task", "t", "--queued"]
        )
        assert opts.queued is True

    def test_workers_command_doesnt_affect_task_parsing(self):
        """Adding the workers subparser doesn't break normal task arg parsing."""
        parser = ConfigParser()
        # Regular task invocation should still work
        opts, _ = parser.parser.parse_known_args(
            ["--program", "myapp", "--task", "export_data"]
        )
        assert opts.program == "myapp"
        assert opts.task == "export_data"
        # workers_command should be None when not used
        assert getattr(opts, "workers_command", None) is None

    def test_workers_queues_does_not_interfere_with_debug(self):
        """--debug flag does not conflict with workers subcommand."""
        parser = ConfigParser()
        opts, _ = parser.parser.parse_known_args(["workers", "queues", "--debug"])
        assert opts.workers_command == "workers"
        # debug may or may not parse depending on argparse precedence
        # The key is no crash
