import errno
import socket
import threading
import time
import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.execution_stdio import BroadcastController
from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import ScriptContext


def _make_broadcast_controller():
    main_controller = MagicMock()
    main_controller.execution_logs_repository = MagicMock()
    main_controller.execution_repository = MagicMock()
    return BroadcastController(
        main_controller=main_controller,
    )


def _make_execution():
    return Execution.create(
        id="exec-123",
        context=ScriptContext(task_id="task-1"),
        stage_id="stage-456",
        worker_id="worker-1",
    )


class TestSendStdioQueueBroadcast(unittest.TestCase):
    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        False,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_without_flag_does_not_add_to_buffer(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        bc.send_stdio(execution, "stdout", "hello world")

        mock_buffer.add.assert_not_called()

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_with_flag_adds_to_buffer(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        bc.send_stdio(execution, "stdout", "hello world")

        mock_buffer.add.assert_called_once()
        msg = mock_buffer.add.call_args[0][0]
        self.assertEqual(msg["type"], "stdout")
        self.assertEqual(msg["log"], "hello world")
        self.assertEqual(msg["execution_id"], "exec-123")
        self.assertEqual(msg["stage_id"], "stage-456")

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
        return_value=None,
    )
    def test_send_stdio_with_flag_but_no_buffer_does_not_crash(self, _):
        bc = _make_broadcast_controller()
        execution = _make_execution()

        # Should not raise
        bc.send_stdio(execution, "stdout", "hello world")

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_buffer_error_does_not_break_execution(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_buffer.add.side_effect = Exception("Buffer full")
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        # Should not raise despite buffer.add() failing
        # (the exception is caught by _handle_stdio's try/except)
        bc.send_stdio(execution, "stderr", "error msg")

    @patch(
        "abstra_internals.controllers.execution.execution_stdio.WORKER_LOG_TO_QUEUE",
        True,
    )
    @patch(
        "abstra_internals.controllers.execution.execution_conn.get_stdio_buffer",
    )
    def test_send_stdio_still_writes_to_repository(self, mock_get_buffer):
        mock_buffer = MagicMock()
        mock_get_buffer.return_value = mock_buffer

        bc = _make_broadcast_controller()
        execution = _make_execution()

        bc.send_stdio(execution, "stdout", "hello")

        bc.execution_logs_repository.insert_stdio.assert_called_once_with(  # type: ignore[union-attr]
            "exec-123", "stage-456", "stdout", "hello"
        )


class TestBroadcastControllerThreadSafety(unittest.TestCase):
    """Item 2: broadcast() must snapshot listeners under lock and must not
    mutate cls.listeners during iteration."""

    def setUp(self):
        # listeners is class-level state shared with the rest of the process.
        # Start and end each test from empty so order-independence holds.
        with BroadcastController._lock:
            BroadcastController.listeners.clear()

    def tearDown(self):
        with BroadcastController._lock:
            BroadcastController.listeners.clear()

    def test_broadcast_does_not_skip_listeners_when_one_fails(self):
        good_a = MagicMock()
        good_a.send = MagicMock()
        bad = MagicMock()
        bad.send = MagicMock(side_effect=Exception("send failed"))
        good_b = MagicMock()
        good_b.send = MagicMock()

        BroadcastController.register(good_a)
        BroadcastController.register(bad)
        BroadcastController.register(good_b)

        BroadcastController.broadcast(msg="hello")

        good_a.send.assert_called_once_with("hello")
        bad.send.assert_called_once_with("hello")
        good_b.send.assert_called_once_with("hello")

        with BroadcastController._lock:
            self.assertIn(good_a, BroadcastController.listeners)
            self.assertNotIn(bad, BroadcastController.listeners)
            self.assertIn(good_b, BroadcastController.listeners)

    def test_broadcast_is_safe_under_concurrent_register_unregister(self):
        errors = []
        stop = threading.Event()

        for _ in range(20):
            listener = MagicMock()
            listener.send = MagicMock()
            BroadcastController.register(listener)

        def broadcaster():
            try:
                while not stop.is_set():
                    BroadcastController.broadcast(msg="x")
            except Exception as e:
                errors.append(e)

        def churn():
            try:
                while not stop.is_set():
                    new_listener = MagicMock()
                    new_listener.send = MagicMock()
                    BroadcastController.register(new_listener)
                    BroadcastController.unregister(new_listener)
            except Exception as e:
                errors.append(e)

        threads = []
        for _ in range(5):
            t = threading.Thread(target=broadcaster, daemon=True)
            t.start()
            threads.append(t)
        for _ in range(5):
            t = threading.Thread(target=churn, daemon=True)
            t.start()
            threads.append(t)

        # Bounded window: enough to exercise the race, short enough to keep the
        # suite fast.
        time.sleep(0.3)
        stop.set()
        for t in threads:
            t.join(timeout=2.0)

        self.assertEqual(errors, [])

    def test_broadcast_uses_snapshot_so_unregister_during_iteration_is_safe(self):
        # An "evil" listener whose .send() unregisters every other listener while
        # broadcast is iterating. With the snapshot, the bystanders MUST still
        # receive the message — the snapshot was taken before the unregisters.
        def evil_send(msg):
            for listener in list(BroadcastController.listeners):
                if listener is not evil:
                    BroadcastController.unregister(listener)

        evil = MagicMock()
        evil.send = MagicMock(side_effect=evil_send)
        bystander_a = MagicMock()
        bystander_a.send = MagicMock()
        bystander_b = MagicMock()
        bystander_b.send = MagicMock()

        BroadcastController.register(evil)
        BroadcastController.register(bystander_a)
        BroadcastController.register(bystander_b)

        BroadcastController.broadcast(msg="probe")

        bystander_a.send.assert_called_once_with("probe")
        bystander_b.send.assert_called_once_with("probe")

    def test_broadcast_with_no_listeners_is_noop(self):
        # The empty-list fast path must be a clean no-op (this is also the
        # abstra-server/abstra-worker path, where nothing ever registers).
        BroadcastController.broadcast(msg="nobody-home")
        with BroadcastController._lock:
            self.assertEqual(BroadcastController.listeners, [])

    def test_failed_listener_already_unregistered_is_clean_noop(self):
        # A listener whose send fails AND was already unregistered (e.g. by its
        # own route's finally) before broadcast's removal phase: the guarded
        # removal (`if listener in cls.listeners`) must be a clean no-op, never a
        # ValueError from list.remove on an absent element.
        def fail_and_self_unregister(msg):
            BroadcastController.unregister(bad)
            raise OSError("send failed after self-unregister")

        bad = MagicMock()
        bad.send = MagicMock(side_effect=fail_and_self_unregister)
        healthy = MagicMock()
        healthy.send = MagicMock()

        BroadcastController.register(bad)
        BroadcastController.register(healthy)

        # Must not raise despite bad being gone before the removal phase.
        BroadcastController.broadcast(msg="x")

        healthy.send.assert_called_once_with("x")
        with BroadcastController._lock:
            self.assertNotIn(bad, BroadcastController.listeners)
            self.assertIn(healthy, BroadcastController.listeners)


class TestBroadcastControllerSendTimeout(unittest.TestCase):
    """Item 3: a listener whose send blocks/times out must not stop the
    broadcast loop; it must be reclaimed (socket half-closed) and dropped."""

    def setUp(self):
        with BroadcastController._lock:
            BroadcastController.listeners.clear()

    def tearDown(self):
        with BroadcastController._lock:
            BroadcastController.listeners.clear()

    def test_register_tolerates_socket_without_setsockopt(self):
        listener = MagicMock()
        # Simulate a socket whose setsockopt is unsupported.
        listener.sock.setsockopt.side_effect = AttributeError("no setsockopt")
        BroadcastController.register(listener)
        with BroadcastController._lock:
            self.assertIn(listener, BroadcastController.listeners)

    def test_register_tolerates_listener_without_sock_attribute(self):
        listener = MagicMock(spec=[])  # no attributes at all
        BroadcastController.register(listener)
        with BroadcastController._lock:
            self.assertIn(listener, BroadcastController.listeners)

    def test_listener_whose_send_raises_oserror_eagain_is_dropped(self):
        # On a blocking socket, SO_SNDTIMEO expiry surfaces as
        # OSError(EWOULDBLOCK) — NOT socket.timeout. broadcast() must drop the
        # listener and continue to the next.
        slow = MagicMock()
        slow.send.side_effect = OSError(errno.EWOULDBLOCK, "send timed out")
        healthy = MagicMock()

        BroadcastController.register(slow)
        BroadcastController.register(healthy)

        BroadcastController.broadcast(msg="ping")

        healthy.send.assert_called_once_with("ping")
        with BroadcastController._lock:
            self.assertNotIn(slow, BroadcastController.listeners)
            self.assertIn(healthy, BroadcastController.listeners)

    def test_listener_whose_send_raises_socket_timeout_is_dropped(self):
        # Defensive: some stacks may surface a timeout as socket.timeout. It
        # must be handled the same way.
        slow = MagicMock()
        slow.send.side_effect = socket.timeout("send timed out")
        healthy = MagicMock()

        BroadcastController.register(slow)
        BroadcastController.register(healthy)

        BroadcastController.broadcast(msg="ping")

        healthy.send.assert_called_once_with("ping")
        with BroadcastController._lock:
            self.assertNotIn(slow, BroadcastController.listeners)
            self.assertIn(healthy, BroadcastController.listeners)

    def test_dropped_listener_is_reclaimed_via_shutdown(self):
        # Dropping a failed listener must half-close its socket so
        # simple_websocket's reader thread wakes on EOF, exits and frees the fd.
        slow = MagicMock()
        slow.send.side_effect = OSError(errno.EWOULDBLOCK, "send timed out")

        BroadcastController.register(slow)
        BroadcastController.broadcast(msg="ping")

        slow.sock.shutdown.assert_called_once_with(socket.SHUT_RDWR)
        with BroadcastController._lock:
            self.assertNotIn(slow, BroadcastController.listeners)

    def test_reclaim_failure_does_not_break_broadcast(self):
        # If shutdown() raises (already-dead socket / test double), broadcast
        # must still deliver to the healthy listeners and finish cleanly.
        slow = MagicMock()
        slow.send.side_effect = OSError(errno.EWOULDBLOCK, "send timed out")
        slow.sock.shutdown.side_effect = OSError("not connected")
        healthy = MagicMock()

        BroadcastController.register(slow)
        BroadcastController.register(healthy)

        BroadcastController.broadcast(msg="ping")

        healthy.send.assert_called_once_with("ping")
        with BroadcastController._lock:
            self.assertNotIn(slow, BroadcastController.listeners)
            self.assertIn(healthy, BroadcastController.listeners)


class TestBroadcastControllerSendOnlySockoptPin(unittest.TestCase):
    """Pin against regression: register() must bound only the send via
    setsockopt(SO_SNDTIMEO), never socket.settimeout (which also bounds recv()
    and would tear the WS down ~timeout after the first inbound frame)."""

    def setUp(self):
        with BroadcastController._lock:
            BroadcastController.listeners.clear()

    def tearDown(self):
        with BroadcastController._lock:
            BroadcastController.listeners.clear()

    def test_register_uses_setsockopt_so_sndtimeo_not_settimeout(self):
        from abstra_internals.controllers.execution.execution_stdio import (
            _SO_SNDTIMEO_VALUE,
        )

        listener = MagicMock()
        BroadcastController.register(listener)

        listener.sock.setsockopt.assert_called_once_with(
            socket.SOL_SOCKET, socket.SO_SNDTIMEO, _SO_SNDTIMEO_VALUE
        )
        # The whole point of the item: settimeout must NEVER be called.
        listener.sock.settimeout.assert_not_called()


class TestEchoLineAtomicity(unittest.TestCase):
    """Regression for cross-execution stdout tearing.

    print() reaches the patched write as the content and its "\\n" in SEPARATE
    calls. _echo must coalesce a logical line and emit it in ONE os.write, so the
    whole line hits the shared pod fd as a single (PIPE_BUF-atomic) syscall and
    concurrent executions/threads cannot interleave mid-line
    ("[RUN a] ...[RUN b] ...").
    """

    MOD = "abstra_internals.controllers.execution.execution_stdio.os.write"

    def test_content_then_newline_is_one_write_of_the_whole_line(self):
        bc = _make_broadcast_controller()
        with patch(self.MOD) as w:
            bc._echo("stdout", "[RUN abc] hello")  # print()'s content write
            w.assert_not_called()  # partial line held, NOT echoed yet
            bc._echo("stdout", "\n")  # print()'s separate newline write
            # The whole line in a single syscall -- this is what defeats the tear.
            w.assert_called_once_with(1, b"[RUN abc] hello\n")

    def test_stderr_goes_to_fd_2(self):
        bc = _make_broadcast_controller()
        with patch(self.MOD) as w:
            bc._echo("stderr", "boom\n")
            w.assert_called_once_with(2, b"boom\n")

    def test_multiple_lines_each_emitted_whole_and_partial_held(self):
        bc = _make_broadcast_controller()
        with patch(self.MOD) as w:
            bc._echo("stdout", "a\nb\nc")
            self.assertEqual(
                [c.args for c in w.call_args_list], [(1, b"a\n"), (1, b"b\n")]
            )
        self.assertEqual(getattr(bc._echo_local, "stdout", ""), "c")

    def test_handle_stdio_tags_then_coalesces_into_one_write(self):
        bc = _make_broadcast_controller()
        execution = _make_execution()  # id "exec-123" -> tag prefix "[RUN exec] "
        with (
            patch.object(bc, "get_current_execution", return_value=execution),
            patch.object(bc, "send_stdio"),
            patch(self.MOD) as w,
        ):
            bc.patched_stdout_write("hi")  # tagged content
            bc.patched_stdout_write("\n")  # separate newline
            w.assert_called_once_with(1, b"[RUN exec] hi\n")

    def test_concurrent_threads_never_emit_a_torn_line(self):
        bc = _make_broadcast_controller()
        captured = []
        clock = threading.Lock()

        def cap(_fd, b):
            with clock:
                captured.append(b)
            return len(b)

        def worker(rid):
            for i in range(400):
                bc._echo("stdout", f"[RUN {rid}] line {i}")  # content
                bc._echo("stdout", "\n")  # separate newline

        with patch(self.MOD, side_effect=cap):
            threads = [
                threading.Thread(target=worker, args=(r,))
                for r in ("aaaa", "bbbb", "cccc", "dddd")
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

        torn = [b for b in captured if b.count(b"[RUN ") != 1 or not b.endswith(b"\n")]
        self.assertEqual(torn, [], f"{len(torn)} torn writes, e.g. {torn[:3]}")
        self.assertEqual(len(captured), 4 * 400)


if __name__ == "__main__":
    unittest.main()
