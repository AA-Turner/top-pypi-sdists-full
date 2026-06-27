import os
import shutil
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase
from unittest.mock import MagicMock, patch

import flask

from abstra_internals.server.routes.file_history import get_editor_bp
from abstra_internals.services.file_history import (
    BACKUP_DIRNAME,
    ROOT_DIRNAME,
    FileHistoryService,
    _backup_filename,
)
from abstra_internals.settings import Settings


class TestFileHistoryRoutes(TestCase):
    def setUp(self) -> None:
        self.original_cwd = Path.cwd()
        self.tmp = Path(mkdtemp())
        Settings.set_root_path(str(self.tmp))
        FileHistoryService.reset_for_tests()

        self.app = flask.Flask(__name__)
        self.app.register_blueprint(
            get_editor_bp(MagicMock()), url_prefix="/file-history"
        )
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        os.chdir(self.original_cwd)
        FileHistoryService.reset_for_tests()
        if self.tmp.exists():
            shutil.rmtree(self.tmp, ignore_errors=True)

    def _seed(self, message_id: str, rel_path: str, content: str) -> Path:
        target = self.tmp / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        svc = FileHistoryService
        svc.make_snapshot(message_id)
        svc.track_edit(message_id, target)
        return target

    def test_list_checkpoints_returns_empty_when_no_snapshots(self):
        response = self.client.get("/file-history/checkpoints")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"checkpoints": []})

    def test_list_checkpoints_returns_recorded_messages(self):
        self._seed("m1", "abstra.json", "before")
        response = self.client.get("/file-history/checkpoints")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        ids = [c["messageId"] for c in body["checkpoints"]]
        self.assertEqual(ids, ["m1"])

    def test_diff_endpoint_returns_404_for_unknown_checkpoint(self):
        response = self.client.get("/file-history/checkpoints/missing/diff")
        self.assertEqual(response.status_code, 404)

    def test_diff_endpoint_reports_changed_files(self):
        target = self._seed("m1", "abstra.json", "v1")
        target.write_text("v2", encoding="utf-8")
        response = self.client.get("/file-history/checkpoints/m1/diff")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertIn("abstra.json", body["filesChanged"])

    def test_rewind_endpoint_restores_files_and_returns_list(self):
        target = self._seed("m1", "abstra.json", "original")
        target.write_text("changed", encoding="utf-8")
        response = self.client.post("/file-history/checkpoints/m1/rewind")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(target.read_text(encoding="utf-8"), "original")
        self.assertEqual(len(body["filesRestored"]), 1)

    def test_rewind_endpoint_returns_404_for_unknown_checkpoint(self):
        response = self.client.post("/file-history/checkpoints/missing/rewind")
        self.assertEqual(response.status_code, 404)

    def test_rewind_endpoint_returns_409_when_restore_partially_fails(self):
        target = self._seed("m1", "abstra.json", "original")
        target.write_text("changed", encoding="utf-8")
        backup = (
            self.tmp
            / ROOT_DIRNAME
            / BACKUP_DIRNAME
            / _backup_filename("abstra.json", 1)
        )
        backup.unlink()

        response = self.client.post("/file-history/checkpoints/m1/rewind")

        self.assertEqual(response.status_code, 409)
        body = response.get_json()
        self.assertEqual(body["error"], "File rewind partially failed")
        self.assertEqual(body["filesRestored"], [])
        self.assertEqual(body["errors"][0]["path"], "abstra.json")

    def test_rewind_endpoint_emits_changed_event_for_restored_file(self):
        target = self._seed("m1", "abstra.json", "original")
        target.write_text("changed", encoding="utf-8")
        with patch(
            "abstra_internals.controllers.codebase_events.CodebaseEventController.notify_change"
        ) as notify:
            response = self.client.post("/file-history/checkpoints/m1/rewind")
        self.assertEqual(response.status_code, 200)
        events = [(str(c.args[0]), c.args[1]) for c in notify.call_args_list]
        self.assertTrue(
            any(p.endswith("abstra.json") and ev == "changed" for p, ev in events)
        )

    def test_rewind_endpoint_emits_deleted_event_for_file_created_after_snapshot(self):
        svc = FileHistoryService
        new_file = self.tmp / "new_stage.py"
        svc.make_snapshot("m1")
        svc.track_edit("m1", new_file)
        new_file.write_text("created after rollback point", encoding="utf-8")
        with patch(
            "abstra_internals.controllers.codebase_events.CodebaseEventController.notify_change"
        ) as notify:
            response = self.client.post("/file-history/checkpoints/m1/rewind")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(new_file.exists())
        events = [(str(c.args[0]), c.args[1]) for c in notify.call_args_list]
        self.assertTrue(
            any(p.endswith("new_stage.py") and ev == "deleted" for p, ev in events)
        )
