import os
import shutil
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase

from flask import Flask

from abstra_internals.services.file_history import FileHistoryService
from abstra_internals.services.mcp_context import (
    USER_MESSAGE_ID_HEADER,
    current_message_id,
    set_current_message_id,
)
from abstra_internals.settings import Settings
from abstra_internals.utils.mcp import requires_approval
from abstra_internals.utils.mcp_bp import mcp_bp


def _captured_message_id_tool():
    return {"message_id": current_message_id()}


@requires_approval
def _mutating_noop_tool():
    """A mutating tool that does nothing — used to verify snapshot interception."""
    return {"ok": True}


class TestMCPContextHelpers(TestCase):
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.mcp_blueprint = mcp_bp([_captured_message_id_tool])
        self.app.register_blueprint(self.mcp_blueprint, url_prefix="/mcp")
        self.client = self.app.test_client()

    def test_current_message_id_outside_request_returns_none(self):
        self.assertIsNone(current_message_id())

    def test_set_current_message_id_outside_request_is_noop(self):
        set_current_message_id("does-not-stick")
        self.assertIsNone(current_message_id())

    def test_header_is_propagated_into_tool_call(self):
        request_body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "_captured_message_id_tool", "arguments": {}},
        }
        response = self.client.post(
            "/mcp/",
            json=request_body,
            headers={
                "Content-Type": "application/json",
                USER_MESSAGE_ID_HEADER: "msg-abc-123",
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        text = body["result"]["content"][0]["text"]
        self.assertIn("msg-abc-123", text)

    def test_missing_header_yields_null_message_id(self):
        request_body = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "_captured_message_id_tool", "arguments": {}},
        }
        response = self.client.post(
            "/mcp/",
            json=request_body,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        text = body["result"]["content"][0]["text"]
        self.assertIn("null", text)


class TestMCPContextSnapshotIntegration(TestCase):
    """End-to-end: mcp_bp must snapshot before mutating tools run, using the header's message_id."""

    def setUp(self) -> None:
        self.original_cwd = Path.cwd()
        self.tmp = Path(mkdtemp())
        Settings.set_root_path(str(self.tmp))  # also chdir's into self.tmp
        FileHistoryService.reset_for_tests()
        self.app = Flask(__name__)
        self.app.register_blueprint(mcp_bp([_mutating_noop_tool]), url_prefix="/mcp")
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        os.chdir(self.original_cwd)
        FileHistoryService.reset_for_tests()
        if self.tmp.exists():
            shutil.rmtree(self.tmp, ignore_errors=True)

    def _call_mutating_tool(self, headers):
        return self.client.post(
            "/mcp/",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "_mutating_noop_tool__req_approval__",
                    "arguments": {},
                },
            },
            headers=headers,
        )

    def test_mutating_tool_with_valid_header_creates_snapshot_with_that_id(self):
        resp = self._call_mutating_tool(
            {
                "Content-Type": "application/json",
                USER_MESSAGE_ID_HEADER: "msg-snapshot-1",
            }
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            FileHistoryService.can_restore("msg-snapshot-1"),
            "expected a file-history snapshot to be created for msg-snapshot-1",
        )

    def test_mutating_tool_without_header_does_not_create_snapshot(self):
        resp = self._call_mutating_tool({"Content-Type": "application/json"})
        self.assertEqual(resp.status_code, 200)
        # No header → no message_id → no snapshot, but the tool still runs.
        self.assertEqual(
            FileHistoryService.list_checkpoints(),
            [],
            "no snapshots expected when header is absent",
        )

    def test_mutating_tool_with_unsafe_header_does_not_create_snapshot(self):
        resp = self._call_mutating_tool(
            {
                "Content-Type": "application/json",
                USER_MESSAGE_ID_HEADER: "../../etc/passwd",
            }
        )
        self.assertEqual(resp.status_code, 200)
        # Invalid format → set_current_message_id stored None → no snapshot.
        self.assertEqual(
            FileHistoryService.list_checkpoints(),
            [],
            "no snapshots expected for an invalid message_id format",
        )
