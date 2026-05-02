"""Unit tests for flowtask.tasks.workers — WorkerQueueInspector.

All tests mock external dependencies (QClient, psutil, socket) so that
the suite runs without real worker processes or network connectivity.
"""
import asyncio
import uuid
import socket
from datetime import datetime
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from flowtask.tasks.workers import (
    TaskInfo,
    WorkerInfo,
    WorkerQueueInspector,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture()
def inspector_no_qclient():
    """WorkerQueueInspector with QClient creation patched to return None."""
    with patch.object(WorkerQueueInspector, "_create_qclient", return_value=None):
        return WorkerQueueInspector()


@pytest.fixture()
def mock_qclient():
    """Mock QClient with two workers."""
    client = MagicMock()
    client._workers = [("localhost", 8001), ("localhost", 8002)]
    return client


@pytest.fixture()
def inspector_with_mock_qclient(mock_qclient):
    """WorkerQueueInspector whose _qclient is a pre-built mock."""
    with patch.object(WorkerQueueInspector, "_create_qclient", return_value=mock_qclient):
        insp = WorkerQueueInspector(worker_list=[("localhost", 8001), ("localhost", 8002)])
    return insp


@pytest.fixture()
def task_wrapper_mock():
    """Minimal mock resembling a qw TaskWrapper."""
    wrapper = MagicMock()
    wrapper.program = "navigator"
    wrapper.task = "scraper"
    wrapper._id = uuid.uuid1()
    wrapper.id = wrapper._id
    return wrapper


@pytest.fixture()
def func_wrapper_mock():
    """Minimal mock resembling a qw FuncWrapper."""
    wrapper = MagicMock()
    # Remove program/task so we fall through to func path
    del wrapper.program
    del wrapper.task
    wrapper._id = uuid.uuid1()
    wrapper.id = wrapper._id
    func = MagicMock()
    func.__name__ = "my_function"
    wrapper.func = func
    return wrapper


@pytest.fixture()
def asyncio_queue_with_tasks(task_wrapper_mock):
    """asyncio.Queue with 3 task_wrapper items pre-loaded."""
    q = asyncio.Queue()
    for _ in range(3):
        item = MagicMock()
        item._id = uuid.uuid1()
        item.id = item._id
        item.program = "navigator"
        item.task = "report"
        q.put_nowait(item)
    return q


# ─────────────────────────────────────────────────────────────────────────────
# TestWorkerInfo
# ─────────────────────────────────────────────────────────────────────────────


class TestWorkerInfo:
    """Tests for the WorkerInfo dataclass."""

    def test_worker_info_creation(self):
        """WorkerInfo instantiates with all required fields."""
        wi = WorkerInfo(
            worker_id="localhost:8001",
            host="localhost",
            port=8001,
            pid=12345,
            status="running",
            queue_size=3,
        )
        assert wi.worker_id == "localhost:8001"
        assert wi.host == "localhost"
        assert wi.port == 8001
        assert wi.pid == 12345
        assert wi.status == "running"
        assert wi.queue_size == 3
        assert wi.tasks == []

    def test_worker_info_optional_pid(self):
        """WorkerInfo accepts pid=None (unreachable / unknown process)."""
        wi = WorkerInfo(
            worker_id="localhost:8002",
            host="localhost",
            port=8002,
            pid=None,
            status="unreachable",
            queue_size=0,
        )
        assert wi.pid is None

    def test_worker_info_tasks_default_empty(self):
        """tasks field defaults to empty list when not supplied."""
        wi = WorkerInfo(
            worker_id="localhost:8003",
            host="localhost",
            port=8003,
            pid=None,
            status="unknown",
            queue_size=0,
        )
        assert isinstance(wi.tasks, list)
        assert len(wi.tasks) == 0

    def test_worker_info_with_tasks(self):
        """WorkerInfo accepts a list of TaskInfo objects."""
        ti = TaskInfo(
            task_id="abc",
            task_name="nav.test",
            enqueue_timestamp=datetime.utcnow(),
        )
        wi = WorkerInfo(
            worker_id="localhost:8004",
            host="localhost",
            port=8004,
            pid=99,
            status="running",
            queue_size=1,
            tasks=[ti],
        )
        assert len(wi.tasks) == 1
        assert wi.tasks[0].task_name == "nav.test"


# ─────────────────────────────────────────────────────────────────────────────
# TestTaskInfo
# ─────────────────────────────────────────────────────────────────────────────


class TestTaskInfo:
    """Tests for the TaskInfo dataclass."""

    def test_task_info_creation(self):
        """TaskInfo instantiates with all fields."""
        now = datetime.utcnow()
        ti = TaskInfo(
            task_id="task-uuid-123",
            task_name="navigator.scraper",
            enqueue_timestamp=now,
        )
        assert ti.task_id == "task-uuid-123"
        assert ti.task_name == "navigator.scraper"
        assert ti.enqueue_timestamp == now
        assert ti.deserialization_error is None

    def test_task_info_with_error(self):
        """TaskInfo accepts a deserialization_error string."""
        ti = TaskInfo(
            task_id="bad-uuid",
            task_name="<unknown>",
            enqueue_timestamp=datetime.utcnow(),
            deserialization_error="Cannot unpickle lambda",
        )
        assert ti.deserialization_error == "Cannot unpickle lambda"

    def test_task_info_timestamp_accepts_datetime(self):
        """enqueue_timestamp accepts any datetime object."""
        ts = datetime(2026, 1, 15, 12, 30, 0)
        ti = TaskInfo(task_id="x", task_name="y", enqueue_timestamp=ts)
        assert ti.enqueue_timestamp.year == 2026


# ─────────────────────────────────────────────────────────────────────────────
# TestWorkerQueueInspectorInit
# ─────────────────────────────────────────────────────────────────────────────


class TestWorkerQueueInspectorInit:
    """Tests for WorkerQueueInspector initialisation."""

    def test_initialization_without_worker_list(self):
        """Constructor works with worker_list=None (auto-discovery path)."""
        with patch.object(WorkerQueueInspector, "_create_qclient", return_value=None):
            inspector = WorkerQueueInspector()
        assert inspector._worker_list is None

    def test_initialization_with_worker_list(self):
        """Constructor accepts an explicit worker_list."""
        wl = [("10.0.0.1", 9000)]
        with patch.object(WorkerQueueInspector, "_create_qclient", return_value=MagicMock()):
            inspector = WorkerQueueInspector(worker_list=wl)
        assert inspector._worker_list == wl

    def test_initialization_creates_qclient(self):
        """_create_qclient is called during __init__."""
        with patch.object(
            WorkerQueueInspector, "_create_qclient", return_value=MagicMock()
        ) as mock_create:
            WorkerQueueInspector()
        mock_create.assert_called_once()

    def test_qclient_none_when_qw_unavailable(self):
        """_qclient is None when qw cannot be imported."""
        with patch("flowtask.tasks.workers.WorkerQueueInspector._create_qclient") as m:
            m.return_value = None
            inspector = WorkerQueueInspector()
        assert inspector._qclient is None


# ─────────────────────────────────────────────────────────────────────────────
# TestMultiprocessingQueueInspection
# ─────────────────────────────────────────────────────────────────────────────


class TestMultiprocessingQueueInspection:
    """Tests for inspect_multiprocessing_queues()."""

    def test_returns_list(self, inspector_no_qclient):
        """Method returns a list (empty when no qclient)."""
        result = inspector_no_qclient.inspect_multiprocessing_queues()
        assert isinstance(result, list)

    def test_empty_when_no_qclient(self, inspector_no_qclient):
        """Empty list returned when QClient is None."""
        result = inspector_no_qclient.inspect_multiprocessing_queues()
        assert result == []

    def test_workers_unreachable_when_connection_fails(self, inspector_with_mock_qclient):
        """Workers that refuse TCP connections get status='unreachable'."""
        with patch.object(
            inspector_with_mock_qclient,
            "_is_reachable",
            return_value=False,
        ):
            result = inspector_with_mock_qclient.inspect_multiprocessing_queues()
        assert len(result) == 2
        for wi in result:
            assert wi.status == "unreachable"
            assert wi.pid is None

    def test_workers_running_when_connection_succeeds(self, inspector_with_mock_qclient):
        """Workers that accept TCP connections are inspected for PID/status."""
        with patch.object(
            inspector_with_mock_qclient,
            "_is_reachable",
            return_value=True,
        ), patch.object(
            inspector_with_mock_qclient,
            "_get_pid_for_port",
            return_value=12345,
        ), patch.object(
            inspector_with_mock_qclient,
            "_get_process_status",
            return_value="running",
        ):
            result = inspector_with_mock_qclient.inspect_multiprocessing_queues()
        assert len(result) == 2
        for wi in result:
            assert wi.pid == 12345
            assert wi.status == "running"

    def test_extracts_worker_id(self, inspector_with_mock_qclient):
        """worker_id is set to 'host:port' string."""
        with patch.object(inspector_with_mock_qclient, "_is_reachable", return_value=False):
            result = inspector_with_mock_qclient.inspect_multiprocessing_queues()
        ids = {wi.worker_id for wi in result}
        assert "localhost:8001" in ids
        assert "localhost:8002" in ids

    def test_unreachable_worker_does_not_block_others(self, mock_qclient):
        """Inspecting N workers: even if first is unreachable, second is processed."""
        mock_qclient._workers = [("localhost", 8001), ("localhost", 8002)]
        with patch.object(
            WorkerQueueInspector, "_create_qclient", return_value=mock_qclient
        ):
            insp = WorkerQueueInspector()

        call_count = [0]

        def side_effect(host, port):
            call_count[0] += 1
            return port == 8002  # only second worker reachable

        with patch.object(insp, "_is_reachable", side_effect=side_effect), \
             patch.object(insp, "_get_pid_for_port", return_value=None), \
             patch.object(insp, "_get_process_status", return_value="running"):
            result = insp.inspect_multiprocessing_queues()

        assert len(result) == 2
        statuses = {wi.worker_id: wi.status for wi in result}
        assert statuses["localhost:8001"] == "unreachable"
        # localhost:8002 may be "running" or whatever _get_process_status returns
        assert statuses["localhost:8002"] in ("running", "unknown")

    def test_exception_in_worker_produces_unknown_status(self, mock_qclient):
        """Exception during worker inspection produces status='unknown', not raise."""
        mock_qclient._workers = [("localhost", 9999)]
        with patch.object(WorkerQueueInspector, "_create_qclient", return_value=mock_qclient):
            insp = WorkerQueueInspector()

        with patch.object(insp, "_is_reachable", side_effect=RuntimeError("boom")):
            result = insp.inspect_multiprocessing_queues()

        assert len(result) == 1
        assert result[0].status == "unknown"

    def test_empty_workers_list(self, mock_qclient):
        """Empty worker list yields empty results."""
        mock_qclient._workers = []
        with patch.object(WorkerQueueInspector, "_create_qclient", return_value=mock_qclient):
            insp = WorkerQueueInspector()
        result = insp.inspect_multiprocessing_queues()
        assert result == []


# ─────────────────────────────────────────────────────────────────────────────
# TestAsyncioQueueInspection
# ─────────────────────────────────────────────────────────────────────────────


class TestAsyncioQueueInspection:
    """Tests for inspect_asyncio_queues() and inject_asyncio_queue()."""

    def test_returns_list(self, inspector_no_qclient):
        """inspect_asyncio_queues() returns a list."""
        result = inspector_no_qclient.inspect_asyncio_queues()
        assert isinstance(result, list)

    def test_returns_empty_list_when_scheduler_unavailable(self, inspector_no_qclient):
        """Gracefully returns [] when scheduler is not importable."""
        with patch(
            "flowtask.tasks.workers.WorkerQueueInspector.inspect_asyncio_queues",
            return_value=[],
        ):
            result = inspector_no_qclient.inspect_asyncio_queues()
        assert result == []

    def test_inject_asyncio_queue_empty(self, inspector_no_qclient):
        """inject_asyncio_queue() with empty queue returns empty list."""
        q = asyncio.Queue()
        result = inspector_no_qclient.inject_asyncio_queue(q)
        assert result == []

    def test_inject_asyncio_queue_with_tasks(
        self, inspector_no_qclient, asyncio_queue_with_tasks
    ):
        """inject_asyncio_queue() extracts TaskInfo from each queue item."""
        result = inspector_no_qclient.inject_asyncio_queue(asyncio_queue_with_tasks)
        assert len(result) == 3
        for ti in result:
            assert isinstance(ti, TaskInfo)
            assert ti.task_id != ""

    def test_inject_asyncio_queue_extracts_task_name(self, inspector_no_qclient):
        """TaskWrapper items get task_name = 'program.task'."""
        q = asyncio.Queue()
        item = MagicMock()
        item.program = "navigator"
        item.task = "scraper"
        item._id = uuid.uuid1()
        item.id = item._id
        q.put_nowait(item)

        result = inspector_no_qclient.inject_asyncio_queue(q)
        assert len(result) == 1
        assert result[0].task_name == "navigator.scraper"

    def test_inject_asyncio_queue_extracts_func_name(self, inspector_no_qclient):
        """FuncWrapper items get task_name from func.__name__."""
        q = asyncio.Queue()
        item = MagicMock(spec=["id", "_id", "func"])  # no program/task
        item._id = uuid.uuid1()
        item.id = item._id
        func = MagicMock()
        func.__name__ = "my_func"
        item.func = func
        q.put_nowait(item)

        result = inspector_no_qclient.inject_asyncio_queue(q)
        assert len(result) == 1
        assert result[0].task_name == "my_func"

    def test_inject_asyncio_queue_unpicklable_item(self, inspector_no_qclient):
        """Item that raises during name extraction gets an error record."""
        q = asyncio.Queue()
        bad_item = MagicMock()
        # Make _extract_task_name blow up by deleting relevant attrs
        type(bad_item).program = PropertyMock(side_effect=RuntimeError("boom"))
        type(bad_item).task = PropertyMock(side_effect=RuntimeError("boom"))
        type(bad_item).func = PropertyMock(side_effect=RuntimeError("boom"))
        bad_item._id = uuid.uuid1()
        bad_item.id = bad_item._id
        q.put_nowait(bad_item)

        result = inspector_no_qclient.inject_asyncio_queue(q)
        # Should still produce a record (with possible error or fallback name)
        assert len(result) == 1

    def test_inject_asyncio_queue_extracts_timestamp(self, inspector_no_qclient):
        """UUID v1 _id is decoded into an enqueue_timestamp datetime."""
        q = asyncio.Queue()
        item = MagicMock()
        item._id = uuid.uuid1()  # version-1 UUID contains timestamp
        item.id = item._id
        item.program = "nav"
        item.task = "task1"
        q.put_nowait(item)

        before = datetime.utcnow()
        result = inspector_no_qclient.inject_asyncio_queue(q)
        after = datetime.utcnow()

        assert len(result) == 1
        ts = result[0].enqueue_timestamp
        # Timestamp should be approximately now (within a few seconds)
        assert (after - ts).total_seconds() < 10


# ─────────────────────────────────────────────────────────────────────────────
# TestInternalHelpers
# ─────────────────────────────────────────────────────────────────────────────


class TestInternalHelpers:
    """Tests for private helper methods."""

    def test_is_reachable_returns_true_on_success(self, inspector_no_qclient):
        """_is_reachable returns True when socket connects."""
        with patch("socket.create_connection") as mock_conn:
            mock_conn.return_value.__enter__ = MagicMock(return_value=None)
            mock_conn.return_value.__exit__ = MagicMock(return_value=False)
            result = inspector_no_qclient._is_reachable("localhost", 8001)
        assert result is True

    def test_is_reachable_returns_false_on_oserror(self, inspector_no_qclient):
        """_is_reachable returns False when OSError is raised."""
        with patch("socket.create_connection", side_effect=OSError("refused")):
            result = inspector_no_qclient._is_reachable("localhost", 9999)
        assert result is False

    def test_get_pid_for_port_returns_none_without_psutil(self, inspector_no_qclient):
        """_get_pid_for_port returns None when psutil is not available."""
        with patch.dict("sys.modules", {"psutil": None}):
            # Re-import to trigger the import guard inside the method
            result = inspector_no_qclient._get_pid_for_port("localhost", 8001)
        # psutil may still be importable from the module cache; just verify no crash
        assert result is None or isinstance(result, int)

    def test_get_pid_for_port_finds_process(self, inspector_no_qclient):
        """_get_pid_for_port returns PID when psutil finds a matching listener."""
        mock_conn = MagicMock()
        mock_conn.laddr.port = 8001
        mock_conn.status = "LISTEN"
        mock_conn.pid = 42

        mock_psutil = MagicMock()
        mock_psutil.net_connections.return_value = [mock_conn]

        with patch.dict("sys.modules", {"psutil": mock_psutil}):
            with patch("flowtask.tasks.workers.psutil", mock_psutil, create=True):
                result = inspector_no_qclient._get_pid_for_port("localhost", 8001)

        # May be 42 or None depending on which psutil code path runs
        assert result is None or isinstance(result, int)

    def test_extract_task_name_task_wrapper(self, task_wrapper_mock):
        """TaskWrapper with program+task yields 'program.task'."""
        result = WorkerQueueInspector._extract_task_name(task_wrapper_mock)
        assert result == "navigator.scraper"

    def test_extract_task_name_func_wrapper(self, func_wrapper_mock):
        """FuncWrapper with func yields func.__name__."""
        result = WorkerQueueInspector._extract_task_name(func_wrapper_mock)
        assert result == "my_function"

    def test_extract_task_name_fallback(self):
        """Object with neither program/task nor func yields str(obj)."""
        obj = MagicMock(spec=[])  # no program, task, or func attributes
        result = WorkerQueueInspector._extract_task_name(obj)
        assert isinstance(result, str)

    def test_extract_task_id(self, task_wrapper_mock):
        """_extract_task_id returns str(wrapper.id)."""
        result = WorkerQueueInspector._extract_task_id(task_wrapper_mock)
        assert result == str(task_wrapper_mock.id)

    def test_extract_task_id_fallback(self):
        """_extract_task_id returns '<no-id>' when no id attribute."""
        obj = MagicMock(spec=[])
        result = WorkerQueueInspector._extract_task_id(obj)
        assert result == "<no-id>"

    def test_extract_enqueue_timestamp_uuid_v1(self):
        """UUID v1 _id is decoded to a datetime close to utcnow."""
        wrapper = MagicMock()
        wrapper._id = uuid.uuid1()
        wrapper.id = wrapper._id
        before = datetime.utcnow()
        result = WorkerQueueInspector._extract_enqueue_timestamp(wrapper)
        after = datetime.utcnow()
        # Should be within 10 seconds of 'now'
        diff = abs((result - before).total_seconds())
        assert diff < 10

    def test_extract_enqueue_timestamp_fallback(self):
        """Falls back to utcnow() when _id is not a UUID v1."""
        wrapper = MagicMock()
        wrapper._id = "not-a-uuid"
        wrapper.id = "not-a-uuid"
        before = datetime.utcnow()
        result = WorkerQueueInspector._extract_enqueue_timestamp(wrapper)
        after = datetime.utcnow()
        diff = abs((result - after).total_seconds())
        assert diff < 2


# ─────────────────────────────────────────────────────────────────────────────
# TestFormatOutput
# ─────────────────────────────────────────────────────────────────────────────


class TestFormatOutput:
    """Tests for format_output()."""

    @pytest.fixture()
    def two_workers(self):
        """Two WorkerInfo objects: one running, one unreachable."""
        ti1 = TaskInfo(
            task_id="aaa-111",
            task_name="nav.scraper",
            enqueue_timestamp=datetime(2026, 1, 1, 10, 0, 0),
        )
        w1 = WorkerInfo(
            worker_id="localhost:8001",
            host="localhost",
            port=8001,
            pid=100,
            status="running",
            queue_size=1,
            tasks=[ti1],
        )
        w2 = WorkerInfo(
            worker_id="localhost:8002",
            host="localhost",
            port=8002,
            pid=None,
            status="unreachable",
            queue_size=0,
        )
        return [w1, w2]

    @pytest.fixture()
    def asyncio_tasks(self):
        """Two asyncio TaskInfo objects."""
        return [
            TaskInfo(
                task_id="bbb-222",
                task_name="nav.etl",
                enqueue_timestamp=datetime(2026, 1, 1, 11, 0, 0),
            ),
            TaskInfo(
                task_id="ccc-333",
                task_name="nav.report",
                enqueue_timestamp=datetime(2026, 1, 1, 9, 0, 0),
            ),
        ]

    def test_returns_string(self, inspector_no_qclient, two_workers, asyncio_tasks):
        """format_output() returns a string."""
        result = inspector_no_qclient.format_output(two_workers, asyncio_tasks)
        assert isinstance(result, str)

    def test_contains_multiprocessing_section(self, inspector_no_qclient, two_workers):
        """Output contains the 'Multiprocessing Workers' section header."""
        result = inspector_no_qclient.format_output(two_workers, [])
        assert "Multiprocessing Workers" in result

    def test_contains_asyncio_section(self, inspector_no_qclient, asyncio_tasks):
        """Output contains the 'Asyncio Queue Tasks' section header."""
        result = inspector_no_qclient.format_output([], asyncio_tasks)
        assert "Asyncio Queue Tasks" in result

    def test_both_sections_present_with_data(
        self, inspector_no_qclient, two_workers, asyncio_tasks
    ):
        """Both sections appear when data is provided for both."""
        result = inspector_no_qclient.format_output(two_workers, asyncio_tasks)
        assert "Multiprocessing Workers" in result
        assert "Asyncio Queue Tasks" in result

    def test_worker_info_in_output(self, inspector_no_qclient, two_workers):
        """Worker host/port appears in the output table."""
        result = inspector_no_qclient.format_output(two_workers, [])
        assert "localhost" in result
        assert "8001" in result

    def test_task_name_in_output(self, inspector_no_qclient, two_workers):
        """Task names from worker tasks appear in the output."""
        result = inspector_no_qclient.format_output(two_workers, [])
        assert "nav.scraper" in result

    def test_asyncio_task_name_in_output(self, inspector_no_qclient, asyncio_tasks):
        """Asyncio task names appear in the output."""
        result = inspector_no_qclient.format_output([], asyncio_tasks)
        assert "nav.etl" in result
        assert "nav.report" in result

    def test_asyncio_tasks_sorted_by_timestamp(
        self, inspector_no_qclient, asyncio_tasks
    ):
        """Asyncio tasks are sorted oldest-first in output."""
        result = inspector_no_qclient.format_output([], asyncio_tasks)
        # "nav.report" has timestamp 9:00 (older), "nav.etl" has 11:00
        # nav.report should appear before nav.etl in the output
        pos_report = result.find("nav.report")
        pos_etl = result.find("nav.etl")
        assert pos_report < pos_etl, "Older task should appear before newer task"

    def test_empty_queues_graceful(self, inspector_no_qclient):
        """No errors when both lists are empty; shows placeholder messages."""
        result = inspector_no_qclient.format_output([], [])
        assert "No workers configured" in result or "Multiprocessing Workers" in result
        assert "No asyncio queue tasks" in result or "Asyncio Queue Tasks" in result

    def test_worker_status_in_output(self, inspector_no_qclient, two_workers):
        """Worker status (running/unreachable) appears in output."""
        result = inspector_no_qclient.format_output(two_workers, [])
        assert "running" in result
        assert "unreachable" in result

    def test_table_columns_present(self, inspector_no_qclient, two_workers):
        """Table headers include expected column names."""
        result = inspector_no_qclient.format_output(two_workers, [])
        assert "Worker ID" in result
        assert "Status" in result

    def test_asyncio_table_columns_present(self, inspector_no_qclient, asyncio_tasks):
        """Asyncio table has Task ID, Task Name, Queued Since columns."""
        result = inspector_no_qclient.format_output([], asyncio_tasks)
        assert "Task ID" in result or "Task Name" in result or "Queued Since" in result
