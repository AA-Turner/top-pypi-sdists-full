import time
import unittest
from contextlib import ExitStack

from simple_websocket import Client, ConnectionClosed

from abstra_internals.controllers.execution.execution_stdio import BroadcastController
from abstra_internals.server.routes.stdio import get_editor_bp
from abstra_internals.server.routes.ws_test_helpers import (
    KEEPALIVE_FRAME,
    isolated_listeners,
    run_ws_app,
    wait_until,
)


class TestStdioListenWebSocket(unittest.TestCase):
    """Behavior of the editor /stdio/listen WebSocket route.

    Encodes the DESIRED behavior: the handler must stay alive across the
    frontend's application-level keepalive frames (sent every 30s) and only
    tear down on a real disconnect. With the current `ws.event.wait()`
    implementation, any inbound frame wakes the handler and flask_sock closes
    the connection — so the keepalive tests fail until the handler drains
    inbound frames instead of parking on the event.
    """

    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        self.listeners = stack.enter_context(isolated_listeners(BroadcastController))
        base_url = stack.enter_context(run_ws_app(get_editor_bp(None), "/stdio"))
        self.listen_url = base_url + "/listen"

    def _connect(self) -> Client:
        ws = Client.connect(self.listen_url)
        self.addCleanup(self._close_quietly, ws)
        return ws

    @staticmethod
    def _close_quietly(ws: Client) -> None:
        try:
            ws.close()
        except Exception:
            # Already closed (possibly by the server) — nothing to clean up.
            pass

    def _wait_registered(self, count: int = 1) -> None:
        self.assertTrue(
            wait_until(lambda: len(self.listeners) == count),
            f"expected {count} registered listener(s), got {len(self.listeners)}",
        )

    def _receive_or_fail(self, ws: Client, context: str) -> str:
        try:
            received = ws.receive(timeout=5)
        except ConnectionClosed:
            self.fail(f"connection was closed by the server {context}")
        if received is None:
            self.fail(f"no message received within timeout {context}")
        return received

    def test_broadcast_reaches_connected_client(self):
        ws = self._connect()
        self._wait_registered()

        msg = '{"type": "stdout", "log": "hello", "execution_id": "ex1"}'
        BroadcastController.broadcast(msg=msg)

        received = self._receive_or_fail(ws, "before the broadcast was delivered")
        self.assertEqual(received, msg)

    def test_keepalive_does_not_close_connection(self):
        ws = self._connect()
        self._wait_registered()

        ws.send(KEEPALIVE_FRAME)
        time.sleep(1.0)

        self.assertTrue(
            ws.connected,
            "connection was closed by the server after keepalive",
        )
        self.assertEqual(
            len(self.listeners),
            1,
            "listener was unregistered by the server after keepalive",
        )

    def test_broadcast_still_delivered_after_keepalive(self):
        ws = self._connect()
        self._wait_registered()

        ws.send(KEEPALIVE_FRAME)
        time.sleep(0.5)

        first = '{"type": "stdout", "log": "after first keepalive"}'
        BroadcastController.broadcast(msg=first)
        received = self._receive_or_fail(ws, "after the first keepalive")
        self.assertEqual(received, first)

        # The front sends a keepalive every 30s forever — the connection must
        # survive repeated cycles, not just the first frame.
        try:
            ws.send(KEEPALIVE_FRAME)
        except ConnectionClosed:
            self.fail("connection was closed by the server before the second keepalive")
        time.sleep(0.5)

        second = '{"type": "stdout", "log": "after second keepalive"}'
        BroadcastController.broadcast(msg=second)
        received = self._receive_or_fail(ws, "after the second keepalive")
        self.assertEqual(received, second)

    def test_client_disconnect_unregisters_listener(self):
        ws = self._connect()
        self._wait_registered()

        ws.close()

        self.assertTrue(
            wait_until(lambda: len(self.listeners) == 0),
            "listener was not unregistered after the client disconnected",
        )


if __name__ == "__main__":
    unittest.main()
