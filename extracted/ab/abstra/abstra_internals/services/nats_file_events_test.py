import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from abstra_internals.services.nats_file_events import (
    FILE_CHANGE_SUBJECT,
    EditorFileChangeSubscriber,
    WorkerFileChangeNotifier,
    to_editor_relative,
)
from abstra_internals.settings import SettingsController

MODULE = "abstra_internals.services.nats_file_events"


class TestToEditorRelative(unittest.TestCase):
    """The crux: translate a worker-side absolute path into the editor-relative
    path the frontend file tree uses."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.files_root = base / "files"
        self.project_root = base / "project"
        self.outside = base / "temp"
        for d in (self.files_root, self.project_root, self.outside):
            d.mkdir(parents=True, exist_ok=True)
        self._patches = [
            patch(f"{MODULE}.get_persistent_dir", return_value=self.files_root),
            patch.object(SettingsController, "_root_path", self.project_root),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        self._tmp.cleanup()

    def test_persistent_file_maps_to_dot_abstra_persistent(self):
        # abstra.files writes land in the persistent mount (/files), which the
        # editor exposes as .abstra/persistent/...
        result = to_editor_relative(self.files_root / "out.csv")
        self.assertEqual(result, ".abstra/persistent/out.csv")

    def test_persistent_nested_file(self):
        result = to_editor_relative(self.files_root / "sub" / "dir" / "data.csv")
        self.assertEqual(result, ".abstra/persistent/sub/dir/data.csv")

    def test_project_tree_file_maps_one_to_one(self):
        result = to_editor_relative(self.project_root / "data" / "x.csv")
        self.assertEqual(result, "data/x.csv")

    def test_project_root_file(self):
        result = to_editor_relative(self.project_root / "output.csv")
        self.assertEqual(result, "output.csv")

    def test_path_outside_both_roots_is_ignored(self):
        # e.g. /packages, /temp — not part of the editor file tree
        self.assertIsNone(to_editor_relative(self.outside / "junk.bin"))

    def test_persistent_takes_precedence_when_nested_under_root(self):
        # Local/dev layout: persistent dir lives *inside* the project root. The
        # persistent branch must win so the path still maps to .abstra/persistent.
        nested_files = self.project_root / ".abstra" / "persistent"
        nested_files.mkdir(parents=True, exist_ok=True)
        with patch(f"{MODULE}.get_persistent_dir", return_value=nested_files):
            result = to_editor_relative(nested_files / "out.csv")
        self.assertEqual(result, ".abstra/persistent/out.csv")


class TestWorkerFileChangeNotifier(unittest.TestCase):
    def _make(self):
        with (
            patch(f"{MODULE}.NATSPersistentConnection") as MockNATS,
            patch(f"{MODULE}.FileWatcher"),
            patch(f"{MODULE}.get_persistent_dir", return_value=Path("/files")),
            patch.object(SettingsController, "_root_path", Path("/project")),
        ):
            notifier = WorkerFileChangeNotifier("nats://x", "creds")
        notifier._nats = MockNATS.return_value
        return notifier

    @patch(f"{MODULE}.asyncio.run_coroutine_threadsafe")
    @patch(f"{MODULE}.to_editor_relative", return_value=".abstra/persistent/out.csv")
    def test_on_change_publishes_mapped_payload(self, _map, mock_run):
        notifier = self._make()
        notifier._on_change(Path("/files/out.csv"), "created", None)

        notifier._nats.nc.publish.assert_called_once()
        subject, payload = notifier._nats.nc.publish.call_args.args
        self.assertEqual(subject, FILE_CHANGE_SUBJECT)
        self.assertEqual(
            payload, b'{"filepath": ".abstra/persistent/out.csv", "event": "created"}'
        )
        mock_run.assert_called_once()

    @patch(f"{MODULE}.asyncio.run_coroutine_threadsafe")
    @patch(f"{MODULE}.to_editor_relative", return_value=None)
    def test_on_change_skips_out_of_tree_paths(self, _map, mock_run):
        notifier = self._make()
        notifier._on_change(Path("/temp/junk.bin"), "created", None)
        notifier._nats.nc.publish.assert_not_called()
        mock_run.assert_not_called()

    @patch(f"{MODULE}.asyncio.run_coroutine_threadsafe")
    @patch(f"{MODULE}.to_editor_relative", return_value="data/x.csv")
    def test_moved_event_normalized_to_created(self, _map, _run):
        notifier = self._make()
        notifier._on_change(Path("/project/data/x.csv"), "moved", None)
        _, payload = notifier._nats.nc.publish.call_args.args
        self.assertIn(b'"event": "created"', payload)

    @patch(f"{MODULE}.asyncio.run_coroutine_threadsafe", side_effect=RuntimeError("x"))
    @patch(f"{MODULE}.to_editor_relative", return_value="x.csv")
    def test_publish_failure_is_swallowed(self, _map, _run):
        notifier = self._make()
        notifier._on_change(Path("/project/x.csv"), "changed", None)  # must not raise


class TestEditorFileChangeSubscriber(unittest.TestCase):
    def _make(self):
        with patch(f"{MODULE}.NATSPersistentConnection"):
            return EditorFileChangeSubscriber("nats://x", "creds")

    def test_handle_enqueues_without_blocking_loop(self):
        import asyncio

        sub = self._make()
        msg = MagicMock()
        msg.data = b'{"filepath": "data/out.csv", "event": "created"}'
        asyncio.run(sub._handle(msg))
        self.assertEqual(sub._queue.get_nowait(), ("data/out.csv", "created"))

    def test_handle_bad_message_is_swallowed(self):
        import asyncio

        sub = self._make()
        msg = MagicMock()
        msg.data = b"not json"
        asyncio.run(sub._handle(msg))  # must not raise
        self.assertTrue(sub._queue.empty())

    def test_process_batch_broadcasts_and_schedules_lint(self):
        sub = self._make()
        with (
            patch(
                "abstra_internals.controllers.codebase_events.CodebaseEventController"
            ) as MockCtrl,
            patch.object(SettingsController, "_root_path", Path("/project")),
        ):
            sub._process_batch(MockCtrl, [("data/out.csv", "created")])

        MockCtrl.broadcast_changes.assert_called_once()
        path_arg, event_arg, content_arg = MockCtrl.broadcast_changes.call_args.args
        self.assertEqual(path_arg, Path("/project/data/out.csv"))
        self.assertEqual(event_arg, "created")
        self.assertIsNone(content_arg)
        MockCtrl.schedule_lint_for_path.assert_called_once_with(
            Path("/project/data/out.csv")
        )

    def test_process_batch_coalesces_broadcasts_per_directory(self):
        # A burst of many files in one directory must collapse to one broadcast
        # per directory (frontend refetches the dir), but lint stays per file.
        sub = self._make()
        batch = [
            (".abstra/persistent/uploads/a.csv", "changed"),
            (".abstra/persistent/uploads/b.csv", "changed"),
            (".abstra/persistent/uploads/c.csv", "changed"),
            ("data/x.csv", "created"),
        ]
        with (
            patch(
                "abstra_internals.controllers.codebase_events.CodebaseEventController"
            ) as MockCtrl,
            patch.object(SettingsController, "_root_path", Path("/project")),
        ):
            sub._process_batch(MockCtrl, batch)

        self.assertEqual(MockCtrl.broadcast_changes.call_count, 2)  # 2 unique dirs
        self.assertEqual(MockCtrl.schedule_lint_for_path.call_count, 4)  # 4 files

    def test_process_batch_prefers_structural_event_over_changed(self):
        # A 'changed' ordered first must NOT mask a 'created' in the same dir:
        # the single per-directory broadcast must carry the structural event so
        # a consumer that only refetches on non-'changed' still sees the new file.
        sub = self._make()
        batch = [
            ("data/existing.csv", "changed"),  # ordered first
            ("data/brand_new.csv", "created"),
        ]
        with (
            patch(
                "abstra_internals.controllers.codebase_events.CodebaseEventController"
            ) as MockCtrl,
            patch.object(SettingsController, "_root_path", Path("/project")),
        ):
            sub._process_batch(MockCtrl, batch)

        MockCtrl.broadcast_changes.assert_called_once()
        _, event_arg, _ = MockCtrl.broadcast_changes.call_args.args
        self.assertEqual(event_arg, "created")

    def test_process_batch_failure_is_swallowed(self):
        sub = self._make()
        with (
            patch(
                "abstra_internals.controllers.codebase_events.CodebaseEventController"
            ) as MockCtrl,
            patch.object(SettingsController, "_root_path", Path("/project")),
        ):
            MockCtrl.broadcast_changes.side_effect = RuntimeError("boom")
            sub._process_batch(MockCtrl, [("x.csv", "changed")])  # must not raise


if __name__ == "__main__":
    unittest.main()
