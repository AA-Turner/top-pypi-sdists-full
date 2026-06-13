"""Regression suite for the linter events WebSocket handler.

Exercises the real route (`get_editor_bp` sock route "/events") over a real
werkzeug server + simple_websocket client. The handler must: register the ws
in LinterEventController, immediately send the cached checks payload, survive
the front's 30s keepalive frames, deliver broadcasts, and unregister on
disconnect. These tests must keep passing after the handler is refactored
onto the shared keepalive helper.
"""

import json
import time
import unittest
from unittest.mock import MagicMock

from simple_websocket import Client

from abstra_internals.controllers.linter_events import LinterEventController
from abstra_internals.server.routes.linters import get_editor_bp
from abstra_internals.server.routes.ws_test_helpers import (
    KEEPALIVE_FRAME,
    isolated_listeners,
    run_ws_app,
    wait_until,
)


class TestLinterEventsWebSocket(unittest.TestCase):
    def setUp(self):
        listeners_cm = isolated_listeners(LinterEventController)
        self.listeners = listeners_cm.__enter__()
        self.addCleanup(listeners_cm.__exit__, None, None, None)

        controller = MagicMock()
        controller.linter_repository.checks = []
        server_cm = run_ws_app(get_editor_bp(controller), "/linters")
        self.base_url = server_cm.__enter__()
        self.addCleanup(server_cm.__exit__, None, None, None)

    def _connect(self) -> Client:
        ws = Client.connect(self.base_url + "/events")
        self.addCleanup(self._close, ws)
        return ws

    @staticmethod
    def _close(ws: Client) -> None:
        try:
            ws.close()
        except Exception:
            pass

    def _consume_initial_payload(self, ws: Client) -> None:
        msg = ws.receive(timeout=5)
        if msg is None:
            self.fail("no initial payload received within 5s")
        self.assertEqual(json.loads(msg), {"checks": []})

    def test_initial_checks_payload_sent_on_connect(self):
        ws = self._connect()
        self._consume_initial_payload(ws)

    def test_keepalive_does_not_close_connection(self):
        ws = self._connect()
        self._consume_initial_payload(ws)
        self.assertTrue(wait_until(lambda: len(self.listeners) == 1))

        ws.send(KEEPALIVE_FRAME)
        time.sleep(1.0)

        self.assertTrue(ws.connected)
        self.assertEqual(len(self.listeners), 1)

    def test_broadcast_reaches_client_after_keepalive(self):
        ws = self._connect()
        self._consume_initial_payload(ws)
        self.assertTrue(wait_until(lambda: len(self.listeners) == 1))

        ws.send(KEEPALIVE_FRAME)
        time.sleep(0.5)
        LinterEventController.broadcast([])

        msg = ws.receive(timeout=5)
        if msg is None:
            self.fail("no broadcast received within 5s")
        self.assertEqual(json.loads(msg), {"checks": []})

    def test_client_disconnect_unregisters_listener(self):
        ws = self._connect()
        self._consume_initial_payload(ws)
        self.assertTrue(wait_until(lambda: len(self.listeners) == 1))

        ws.close()

        self.assertTrue(wait_until(lambda: len(self.listeners) == 0))


if __name__ == "__main__":
    unittest.main()
