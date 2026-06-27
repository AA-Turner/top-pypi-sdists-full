import json
import os
import shutil
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase, skipUnless
from unittest.mock import patch

from abstra_internals.services.file_history import (
    BACKUP_DIRNAME,
    MAX_SNAPSHOTS,
    ROOT_DIRNAME,
    STATE_FILENAME,
    FileHistoryService,
    _backup_filename,
)
from abstra_internals.settings import Settings


class TestFileHistoryService(TestCase):
    def setUp(self) -> None:
        self.original_cwd = Path.cwd()
        self.tmp = Path(mkdtemp())
        Settings.set_root_path(str(self.tmp))
        FileHistoryService.reset_for_tests()
        self.svc = FileHistoryService

    def tearDown(self) -> None:
        os.chdir(self.original_cwd)
        FileHistoryService.reset_for_tests()
        if self.tmp.exists():
            shutil.rmtree(self.tmp, ignore_errors=True)

    def _write(self, rel: str, content: str) -> Path:
        path = self.tmp / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_make_snapshot_appends_one_per_message_id(self):
        self.svc.make_snapshot("m1")
        self.svc.make_snapshot("m2")
        self.assertTrue(self.svc.can_restore("m1"))
        self.assertTrue(self.svc.can_restore("m2"))

    def test_make_snapshot_is_idempotent_per_message(self):
        self.svc.make_snapshot("m1")
        self.svc.make_snapshot("m1")
        self.assertEqual(len(self.svc._get_state().snapshots), 1)

    def test_track_edit_creates_backup_with_pre_edit_content(self):
        target = self._write("abstra.json", "before")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("after", encoding="utf-8")

        backup_filename = _backup_filename("abstra.json", 1)
        backup_path = self.tmp / ROOT_DIRNAME / BACKUP_DIRNAME / backup_filename
        self.assertTrue(backup_path.exists())
        self.assertEqual(backup_path.read_text(encoding="utf-8"), "before")

    def test_track_edit_is_idempotent_for_same_path_and_message(self):
        target = self._write("abstra.json", "v1")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("v2", encoding="utf-8")
        self.svc.track_edit("m1", target)

        v1 = (
            self.tmp
            / ROOT_DIRNAME
            / BACKUP_DIRNAME
            / _backup_filename("abstra.json", 1)
        )
        v2 = (
            self.tmp
            / ROOT_DIRNAME
            / BACKUP_DIRNAME
            / _backup_filename("abstra.json", 2)
        )
        self.assertTrue(v1.exists())
        self.assertEqual(v1.read_text(encoding="utf-8"), "v1")
        self.assertFalse(v2.exists())

    def test_track_edit_creates_snapshot_implicitly(self):
        target = self._write("abstra.json", "x")
        self.svc.track_edit("m-only-track", target)
        self.assertTrue(self.svc.can_restore("m-only-track"))

    def test_track_edit_for_missing_file_records_enoent_marker(self):
        path = self.tmp / "new_form.py"
        self.assertFalse(path.exists())
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", path)

        snap_idx = self.svc._snapshot_index("m1")
        assert snap_idx is not None
        snap = self.svc._get_state().snapshots[snap_idx]
        backup = snap.tracked_file_backups["new_form.py"]
        self.assertIsNone(backup.backup_filename)

    def test_track_edit_outside_root_is_silently_ignored(self):
        outsider = Path(mkdtemp()) / "stray.txt"
        outsider.write_text("nope")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", outsider)
        snap_idx = self.svc._snapshot_index("m1")
        assert snap_idx is not None
        snap = self.svc._get_state().snapshots[snap_idx]
        self.assertEqual(snap.tracked_file_backups, {})

    def test_rewind_restores_pre_edit_content(self):
        target = self._write("abstra.json", "original")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("changed", encoding="utf-8")

        files_changed = self.svc.rewind("m1")

        self.assertEqual(target.read_text(encoding="utf-8"), "original")
        self.assertIn(target.resolve(), [p.resolve() for p in files_changed])

    def test_rewind_deletes_files_that_did_not_exist_at_snapshot(self):
        path = self.tmp / "form_new.py"
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", path)
        path.write_text("freshly created", encoding="utf-8")

        self.svc.rewind("m1")
        self.assertFalse(path.exists())

    def test_rewind_recreates_files_deleted_after_snapshot(self):
        target = self._write("dropme.py", "saved")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.unlink()

        self.svc.rewind("m1")
        self.assertTrue(target.exists())
        self.assertEqual(target.read_text(encoding="utf-8"), "saved")

    def test_rewind_same_file_to_later_message_restores_pre_later_edit(self):
        target = self._write("script.py", "v0")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("v1", encoding="utf-8")

        self.svc.make_snapshot("m2")
        self.svc.track_edit("m2", target)
        target.write_text("v2", encoding="utf-8")

        self.svc.rewind("m2")

        self.assertEqual(target.read_text(encoding="utf-8"), "v1")

    def test_rewind_many_steps_restores_all_tracked_files_to_target_state(self):
        first = self._write("first.py", "a0")
        second = self._write("second.py", "b0")
        third = self.tmp / "third.py"

        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", first)
        first.write_text("a1", encoding="utf-8")

        self.svc.make_snapshot("m2")
        self.svc.track_edit("m2", second)
        second.write_text("b1", encoding="utf-8")

        self.svc.make_snapshot("m3")
        self.svc.track_edit("m3", third)
        third.write_text("c1", encoding="utf-8")

        self.svc.rewind("m2")

        self.assertEqual(first.read_text(encoding="utf-8"), "a1")
        self.assertEqual(second.read_text(encoding="utf-8"), "b0")
        self.assertFalse(third.exists())

    def test_rewind_discards_future_snapshots(self):
        target = self._write("script.py", "v0")
        for idx in range(1, 4):
            message_id = f"m{idx}"
            self.svc.make_snapshot(message_id)
            self.svc.track_edit(message_id, target)
            target.write_text(f"v{idx}", encoding="utf-8")

        self.svc.rewind("m2")

        self.assertTrue(self.svc.can_restore("m1"))
        self.assertTrue(self.svc.can_restore("m2"))
        self.assertFalse(self.svc.can_restore("m3"))

    def test_rewind_skips_files_already_matching_backup(self):
        target = self._write("abstra.json", "stable")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        files_changed = self.svc.rewind("m1")
        self.assertEqual(files_changed, [])

    def test_rewind_unknown_message_id_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.svc.rewind("unknown")

    def test_rewind_to_earlier_snapshot_preserves_pre_existed_marker_via_v1_fallback(
        self,
    ):
        target = self._write("script.py", "kept")

        self.svc.make_snapshot("m0")

        self.svc.make_snapshot("m1")
        with patch(
            "abstra_internals.services.file_history.shutil.copy2",
            side_effect=OSError("disk full"),
        ):
            self.svc.track_edit("m1", target)

        target.write_text("modified-by-user", encoding="utf-8")

        with self.assertRaisesRegex(Exception, "File rewind partially failed"):
            self.svc.rewind("m0")

        self.assertTrue(
            target.exists(),
            "rewind to a pre-tracking snapshot must NOT unlink the user's "
            "file just because the v1 fallback's backup write failed",
        )

    def test_first_version_backup_is_called_under_lock_during_rewind(self):
        self.svc.make_snapshot("m0")

        target = self._write("a.py", "original")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("modified", encoding="utf-8")

        self.assertNotIn(
            "a.py",
            self.svc._get_state().snapshots[0].tracked_file_backups,
            "test setup invariant: m0 must not carry a.py so rewind('m0') "
            "hits the v1 fallback path under test",
        )
        self.assertIn("a.py", self.svc._get_state().tracked_files)

        if not hasattr(self.svc._lock, "_is_owned"):
            self.skipTest(
                "RLock._is_owned() unavailable on this Python runtime; "
                "cannot assert the lock invariant directly"
            )

        recorded: list[bool] = []
        original = FileHistoryService._first_version_backup

        def wrapper(cls, tracking_path):
            recorded.append(cls._lock._is_owned())
            return original(tracking_path)

        with patch.object(
            FileHistoryService, "_first_version_backup", classmethod(wrapper)
        ):
            self.svc.rewind("m0")

        self.assertGreater(
            len(recorded),
            0,
            "v1 fallback path was not exercised; the test setup did not "
            "produce a target snapshot missing an entry for a tracked file",
        )
        self.assertTrue(
            all(recorded),
            f"_first_version_backup called WITHOUT self._lock held during "
            f"rewind() (_is_owned() values: {recorded}). rewind() releases "
            f"the lock after copying target/tracked_files; the v1 fallback "
            f"then walks self._state.snapshots unlocked, racing against "
            f"make_snapshot / _evict_if_needed / _cleanup_orphans.",
        )

    def test_rewind_does_not_delete_existing_file_when_backup_write_failed(self):
        target = self._write("target.py", "original")
        self.svc.make_snapshot("m1")

        with patch(
            "abstra_internals.services.file_history.shutil.copy2",
            side_effect=OSError("disk full"),
        ):
            self.svc.track_edit("m1", target)

        snap_idx = self.svc._snapshot_index("m1")
        assert snap_idx is not None
        snap = self.svc._get_state().snapshots[snap_idx]
        backup = snap.tracked_file_backups["target.py"]
        self.assertIsNone(backup.backup_filename)

        target.write_text("modified", encoding="utf-8")

        with self.assertRaisesRegex(Exception, "File rewind partially failed"):
            self.svc.rewind("m1")

        self.assertTrue(
            target.exists(),
            "rewind destroyed an existing file because the backup write failed: "
            "backup_filename=None is overloaded as both ENOENT marker and "
            "write-failure marker",
        )

    def test_chmod_is_preserved_on_restore(self):
        target = self._write("script.py", "original")
        os.chmod(target, 0o640)
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("mut", encoding="utf-8")
        os.chmod(target, 0o600)

        self.svc.rewind("m1")
        mode = target.stat().st_mode & 0o777
        self.assertEqual(mode, 0o640)

    def test_rewind_does_not_discard_future_snapshots_when_restore_partially_fails(
        self,
    ):
        a = self._write("a.py", "a-original")
        b = self._write("b.py", "b-original")

        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", a)
        self.svc.track_edit("m1", b)

        a.write_text("a-modified", encoding="utf-8")
        b.write_text("b-modified", encoding="utf-8")

        self.svc.make_snapshot("m2")
        self.svc.track_edit("m2", a)
        self.svc.track_edit("m2", b)

        backup_a_v1 = (
            self.tmp / ROOT_DIRNAME / BACKUP_DIRNAME / _backup_filename("a.py", 1)
        )
        self.assertTrue(backup_a_v1.exists())
        backup_a_v1.unlink()

        with self.assertRaisesRegex(Exception, "File rewind partially failed"):
            self.svc.rewind("m1")

        self.assertTrue(self.svc.can_restore("m2"))

    def test_cap_evicts_oldest_snapshots_and_drops_orphan_backups(self):
        target = self._write("abstra.json", "init")
        for i in range(MAX_SNAPSHOTS + 5):
            mid = f"m{i}"
            self.svc.make_snapshot(mid)
            self.svc.track_edit(mid, target)
            target.write_text(f"v{i}", encoding="utf-8")

        self.assertEqual(len(self.svc._get_state().snapshots), MAX_SNAPSHOTS)
        self.assertFalse(self.svc.can_restore("m0"))

        survivors_versions = {
            backup.version
            for snap in self.svc._get_state().snapshots
            for backup in snap.tracked_file_backups.values()
            if backup.backup_filename
        }
        for version in survivors_versions:
            path = (
                self.tmp
                / ROOT_DIRNAME
                / BACKUP_DIRNAME
                / _backup_filename("abstra.json", version)
            )
            self.assertTrue(path.exists(), f"missing backup v{version}")

    def test_state_is_persisted_and_reloaded(self):
        target = self._write("abstra.json", "saved")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)

        FileHistoryService.reset_for_tests()
        reloaded = FileHistoryService
        self.assertTrue(reloaded.can_restore("m1"))
        snap_idx = reloaded._snapshot_index("m1")
        assert snap_idx is not None
        snap = reloaded._get_state().snapshots[snap_idx]
        self.assertIn("abstra.json", snap.tracked_file_backups)

    def test_rewind_rejects_paths_escaping_project_root(self):
        outside_dir = Path(mkdtemp())
        try:
            victim = outside_dir / "victim.txt"
            victim.write_text("untouched", encoding="utf-8")

            victim_rel = os.path.relpath(victim, self.tmp)
            self.assertTrue(
                victim_rel.startswith(".."),
                f"expected escaping relative path, got {victim_rel!r}",
            )

            backup_dir = self.tmp / ROOT_DIRNAME / BACKUP_DIRNAME
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_filename = _backup_filename(victim_rel, 1)
            (backup_dir / backup_filename).write_text("PWNED", encoding="utf-8")

            state_path = self.tmp / ROOT_DIRNAME / STATE_FILENAME
            state_payload = {
                "snapshots": [
                    {
                        "messageId": "m1",
                        "timestamp": "2024-01-01T00:00:00+00:00",
                        "trackedFileBackups": {
                            victim_rel: {
                                "backupFilename": backup_filename,
                                "version": 1,
                                "backupTime": "2024-01-01T00:00:00+00:00",
                            }
                        },
                    }
                ],
                "trackedFiles": [victim_rel],
                "snapshotSequence": 1,
            }
            state_path.write_text(json.dumps(state_payload), encoding="utf-8")

            FileHistoryService.reset_for_tests()
            svc = FileHistoryService
            svc.rewind("m1")

            self.assertTrue(
                victim.exists(),
                "rewind must not delete files outside the project root",
            )
            self.assertEqual(
                victim.read_text(encoding="utf-8"),
                "untouched",
                "rewind must not overwrite files outside the project root",
            )
        finally:
            shutil.rmtree(outside_dir, ignore_errors=True)

    @skipUnless(hasattr(os, "symlink"), "platform lacks os.symlink")
    def test_safe_absolute_path_returns_canonical_resolved_path(self):
        real_dir = self.tmp / "real_dir"
        real_dir.mkdir()
        (real_dir / "file.txt").write_text("x", encoding="utf-8")

        alias = self.tmp / "alias"
        try:
            os.symlink(real_dir, alias, target_is_directory=True)
        except (OSError, NotImplementedError) as e:
            self.skipTest(f"cannot create symlink on this platform: {e}")

        result = self.svc._safe_absolute_path("alias/file.txt")

        expected = (self.tmp / "real_dir" / "file.txt").resolve()
        self.assertEqual(result, expected)

    def test_corrupt_state_file_falls_back_to_empty(self):
        state_path = self.tmp / ROOT_DIRNAME / STATE_FILENAME
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text("not json", encoding="utf-8")

        FileHistoryService.reset_for_tests()
        state = FileHistoryService._get_state()
        self.assertEqual(state.snapshots, [])
        self.assertEqual(state.tracked_files, set())

    def test_get_diff_stats_counts_changed_lines(self):
        target = self._write("script.py", "a\nb\nc\n")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("a\nB\nc\nd\n", encoding="utf-8")

        stats = self.svc.get_diff_stats("m1")
        assert stats is not None
        self.assertIn("script.py", stats["filesChanged"])
        self.assertGreaterEqual(stats["insertions"], 1)
        self.assertGreaterEqual(stats["deletions"], 1)

    def test_has_any_changes_true_when_file_modified(self):
        target = self._write("abstra.json", "v1")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        target.write_text("v2", encoding="utf-8")
        self.assertTrue(self.svc.has_any_changes("m1"))

    def test_has_any_changes_false_when_clean(self):
        target = self._write("abstra.json", "v1")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)
        self.assertFalse(self.svc.has_any_changes("m1"))

    def test_list_checkpoints_returns_one_per_snapshot(self):
        self.svc.make_snapshot("m1")
        self.svc.make_snapshot("m2")
        out = self.svc.list_checkpoints()
        ids = [c["messageId"] for c in out]
        self.assertEqual(ids, ["m1", "m2"])

    def test_clear_wipes_snapshots_backups_and_state_file(self):
        target = self._write("abstra.json", "v1")
        self.svc.make_snapshot("m1")
        self.svc.track_edit("m1", target)

        backup_dir = self.tmp / ROOT_DIRNAME / BACKUP_DIRNAME
        state_file = self.tmp / ROOT_DIRNAME / STATE_FILENAME
        self.assertTrue(state_file.exists())
        self.assertTrue(any(backup_dir.iterdir()))

        self.svc.clear()

        self.assertEqual(self.svc._get_state().snapshots, [])
        self.assertEqual(self.svc._get_state().tracked_files, set())
        self.assertFalse(state_file.exists())
        self.assertFalse(backup_dir.exists())
        self.assertFalse(self.svc.can_restore("m1"))
