"""Regression suite for the codebase events WebSocket route.

These tests exercise the real stack (flask_sock blueprint served by werkzeug,
simple_websocket clients) against the current handler in
`abstra_internals/server/routes/codebase.py` and must keep passing unchanged
after the handler is refactored onto the shared keepalive helper.
"""

import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from simple_websocket import Client

from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.server.routes.codebase import get_editor_bp
from abstra_internals.server.routes.ws_test_helpers import (
    KEEPALIVE_FRAME,
    isolated_listeners,
    run_ws_app,
    wait_until,
)
from abstra_internals.settings import Settings, SettingsController


class TestCodebaseEventsWebSocket(unittest.TestCase):
    def setUp(self):
        # broadcast_changes relativizes filepaths against Settings.root_path,
        # so point it at a throwaway directory (no chdir, restored in tearDown).
        self._original_root_path = SettingsController._root_path
        self._tmp_dir = tempfile.TemporaryDirectory()
        SettingsController._root_path = Path(self._tmp_dir.name)
        self.bp = get_editor_bp(MagicMock())

    def tearDown(self):
        SettingsController._root_path = self._original_root_path
        self._tmp_dir.cleanup()

    @staticmethod
    def _safe_close(ws: Client) -> None:
        if ws.connected:
            ws.close()

    def test_keepalive_does_not_close_connection(self):
        with isolated_listeners(CodebaseEventController) as listeners:
            with run_ws_app(self.bp, "/codebase") as base_url:
                ws = Client.connect(base_url + "/events")
                try:
                    self.assertTrue(
                        wait_until(lambda: len(listeners) == 1),
                        "listener was not registered",
                    )
                    ws.send(KEEPALIVE_FRAME)
                    time.sleep(1.0)
                    self.assertTrue(ws.connected)
                    self.assertEqual(len(listeners), 1)
                finally:
                    self._safe_close(ws)

    def test_broadcast_reaches_client_after_keepalive(self):
        with isolated_listeners(CodebaseEventController) as listeners:
            with run_ws_app(self.bp, "/codebase") as base_url:
                ws = Client.connect(base_url + "/events")
                try:
                    self.assertTrue(
                        wait_until(lambda: len(listeners) == 1),
                        "listener was not registered",
                    )
                    ws.send(KEEPALIVE_FRAME)
                    time.sleep(0.5)
                    CodebaseEventController.broadcast_changes(
                        Settings.root_path / "some_file.py", "changed", None
                    )
                    raw = ws.receive(timeout=5)
                    if raw is None:
                        self.fail("no broadcast received within 5s")
                    message = json.loads(raw)
                    self.assertEqual(message["filepath"], "some_file.py")
                    self.assertEqual(message["event"], "changed")
                finally:
                    self._safe_close(ws)

    def test_client_disconnect_unregisters_listener(self):
        with isolated_listeners(CodebaseEventController) as listeners:
            with run_ws_app(self.bp, "/codebase") as base_url:
                ws = Client.connect(base_url + "/events")
                try:
                    self.assertTrue(
                        wait_until(lambda: len(listeners) == 1),
                        "listener was not registered",
                    )
                    ws.close()
                    self.assertTrue(
                        wait_until(lambda: len(listeners) == 0),
                        "listener was not unregistered after disconnect",
                    )
                finally:
                    self._safe_close(ws)


if __name__ == "__main__":
    unittest.main()
