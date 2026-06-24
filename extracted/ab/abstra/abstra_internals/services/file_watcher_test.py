import unittest
from pathlib import Path, PurePosixPath, PureWindowsPath
from unittest.mock import MagicMock, patch

from watchdog.events import FileCreatedEvent, FileModifiedEvent, FileMovedEvent

from abstra_internals.services.file_watcher import FileWatcher


class TestFileWatcherShouldIgnorePath(unittest.TestCase):
    """Test suite for FileWatcher.should_ignore_path method."""

    def setUp(self):
        """Set up a FileWatcher instance for testing."""
        self.watcher = FileWatcher(handlers=[])

    def test_ignore_abstra_directory(self):
        """Test that .abstra/ directory is ignored."""
        self.assertTrue(self.watcher.should_ignore_path(Path("/project/.abstra/cache")))
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.abstra/settings.json"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/deep/path/.abstra/file.txt"))
        )

    def test_ignore_venv_directory(self):
        """Test that .venv directory is ignored."""
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.venv/lib/python"))
        )
        self.assertTrue(self.watcher.should_ignore_path(Path("/project/.venv")))
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/nested/path/.venv/bin/activate"))
        )

    def test_ignore_pycache_directory(self):
        """Test that __pycache__ directory is ignored."""
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/__pycache__/module.pyc"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/src/__pycache__"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/deep/nested/__pycache__/cache.pyc"))
        )

    def test_ignore_git_lock_files(self):
        """Test that specific .git lock files are ignored."""
        # Test index.lock
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/index.lock"))
        )

        # Test HEAD.lock
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/HEAD.lock"))
        )

        # Test config.lock (the original bug case)
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/config.lock"))
        )

    def test_ignore_git_directories(self):
        """Test that specific .git subdirectories are ignored."""
        # Test refs/
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/refs/heads/main"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/refs/tags/v1.0"))
        )

        # Test objects/
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/objects/ab/cdef123"))
        )

        # Test hooks/
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/hooks/pre-commit"))
        )

        # Test logs/
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/logs/HEAD"))
        )

    def test_ignore_git_special_files(self):
        """Test that specific .git files are ignored."""
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/COMMIT_EDITMSG"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/MERGE_HEAD"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/FETCH_HEAD"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/ORIG_HEAD"))
        )

    def test_ignore_any_git_lock_or_tmp_files(self):
        """Test that any .lock or .tmp file in .git directory is ignored."""
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/some-random.lock"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/temp-file.tmp"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(
                Path("/project/.git/refs/heads/branch.lock")
            )
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/objects/pack/temp.tmp"))
        )

    def test_do_not_ignore_regular_files(self):
        """Test that regular files are not ignored."""
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/main.py")))
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/src/utils.py")))
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/README.md")))
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/config.json")))

    def test_do_not_ignore_persistent_files(self):
        """Test that .abstra/persistent is user data and not ignored."""
        self.assertFalse(
            self.watcher.should_ignore_path(Path("/project/.abstra/persistent"))
        )
        self.assertFalse(
            self.watcher.should_ignore_path(
                Path("/project/.abstra/persistent/file.txt")
            )
        )
        self.assertFalse(
            self.watcher.should_ignore_path(
                Path("/project/.abstra/persistent/sub/dir/data.csv")
            )
        )
        win_path = PureWindowsPath(r"C:\project\.abstra\persistent\data.bin")
        self.assertFalse(self.watcher.should_ignore_path(win_path))

    def test_still_ignore_other_abstra_subdirs(self):
        """Test that non-persistent .abstra/ subdirs remain ignored."""
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.abstra/cache/foo"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.abstra/executions/log.txt"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(
                Path("/project/.abstra/persistent-other/foo")
            )
        )

    def test_ignore_all_git_internals(self):
        """The whole .git/ dir is ignored: no consumer reacts to .git/* events
        and they cause a refetch loop (get_status rewrites .git/config). Git
        state reaches the UI via GitController's explicit ".git" broadcast."""
        self.assertTrue(self.watcher.should_ignore_path(Path("/project/.git/config")))
        self.assertTrue(self.watcher.should_ignore_path(Path("/project/.git/HEAD")))
        self.assertTrue(self.watcher.should_ignore_path(Path("/project/.git/index")))
        # ".git" lookalikes outside the .git dir must NOT be ignored
        self.assertFalse(
            self.watcher.should_ignore_path(Path("/project/.github/workflows/ci.yml"))
        )

    def test_windows_paths_with_backslashes(self):
        """Test that Windows paths with backslashes are handled correctly."""
        # Create Windows-style paths using PureWindowsPath
        # These will have backslashes when converted to string
        win_path_1 = PureWindowsPath(r"C:\Users\project\.git\config.lock")
        win_path_2 = PureWindowsPath(
            r"C:\Abstra Seibel Sandbox\teste outro git\.git\config.lock"
        )
        win_path_3 = PureWindowsPath(r"D:\projects\myapp\.venv\lib\site-packages")
        win_path_4 = PureWindowsPath(r"C:\code\__pycache__\module.pyc")

        # These should all be ignored
        self.assertTrue(self.watcher.should_ignore_path(win_path_1))
        self.assertTrue(self.watcher.should_ignore_path(win_path_2))
        self.assertTrue(self.watcher.should_ignore_path(win_path_3))
        self.assertTrue(self.watcher.should_ignore_path(win_path_4))

    def test_windows_paths_with_spaces(self):
        """Test that Windows paths with spaces in directory names are handled correctly."""
        # The original bug case from the user
        win_path = PureWindowsPath(
            r"C:\Abstra Seibel Sandbox\teste outro git\.git\config.lock"
        )
        self.assertTrue(self.watcher.should_ignore_path(win_path))

        # More test cases with spaces
        self.assertTrue(
            self.watcher.should_ignore_path(
                PureWindowsPath(r"C:\Program Files\project\.git\index.lock")
            )
        )
        self.assertTrue(
            self.watcher.should_ignore_path(
                PureWindowsPath(r"D:\My Documents\code\.venv\lib")
            )
        )
        self.assertTrue(
            self.watcher.should_ignore_path(
                PureWindowsPath(r"C:\Users\John Doe\project\__pycache__")
            )
        )

    def test_unix_paths_with_forward_slashes(self):
        """Test that Unix paths with forward slashes work correctly."""
        self.assertTrue(
            self.watcher.should_ignore_path(
                PurePosixPath("/home/user/project/.git/config.lock")
            )
        )
        self.assertTrue(
            self.watcher.should_ignore_path(PurePosixPath("/var/www/app/.venv/bin"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(PurePosixPath("/opt/project/__pycache__"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(
                PurePosixPath("/Users/dev/project/.git/refs/heads/main")
            )
        )

    def test_mixed_case_sensitivity(self):
        """Test path matching with different cases."""
        # These should still match (patterns are case-sensitive)
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/__pycache__/file.pyc"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/config.lock"))
        )

        # These should not match (different case in pattern-sensitive parts)
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/__PYCACHE__")))
        self.assertFalse(
            self.watcher.should_ignore_path(Path("/project/.GIT/config.lock"))
        )

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Root level paths
        self.assertTrue(self.watcher.should_ignore_path(Path("/.git/config.lock")))
        self.assertTrue(self.watcher.should_ignore_path(Path("/.venv")))

        # Very deep nested paths
        deep_path = Path("/a/b/c/d/e/f/g/.git/config.lock")
        self.assertTrue(self.watcher.should_ignore_path(deep_path))

        # Paths that contain pattern substring but shouldn't match
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/.gitignore")))
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/venv_backup")))
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/cache_files")))

    def test_relative_paths(self):
        """Test that relative paths work correctly."""
        self.assertTrue(self.watcher.should_ignore_path(Path(".git/config.lock")))
        self.assertTrue(self.watcher.should_ignore_path(Path(".venv/lib/python")))
        self.assertTrue(
            self.watcher.should_ignore_path(Path("src/__pycache__/module.pyc"))
        )
        self.assertFalse(self.watcher.should_ignore_path(Path("src/main.py")))

    def test_git_subdirectories_ending_with_slash(self):
        """Test patterns that end with slash are matched correctly."""
        # Patterns like ".git/refs/" should match anything under refs
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/refs/heads/main"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/refs/tags/v1.0.0"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/objects/pack/file"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/hooks/pre-commit"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/logs/refs/heads/main"))
        )

    def test_abstra_directory_with_forward_slash(self):
        """Test that .abstra/ pattern (ending with /) matches correctly."""
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.abstra/settings"))
        )
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.abstra/cache/data.json"))
        )

    def test_lock_and_tmp_files_only_in_git(self):
        """Test that .lock and .tmp files are only ignored inside .git directory."""
        # Should be ignored (inside .git)
        self.assertTrue(
            self.watcher.should_ignore_path(Path("/project/.git/custom.lock"))
        )
        self.assertTrue(self.watcher.should_ignore_path(Path("/project/.git/temp.tmp")))

        # Should NOT be ignored (outside .git)
        self.assertFalse(
            self.watcher.should_ignore_path(Path("/project/database.lock"))
        )
        self.assertFalse(self.watcher.should_ignore_path(Path("/project/cache.tmp")))
        self.assertFalse(
            self.watcher.should_ignore_path(Path("/project/data/file.lock"))
        )

    def test_path_normalization_consistency(self):
        """Test that path normalization works consistently across different path representations."""
        # Unix-style path
        posix_path = PurePosixPath("/project/.git/config.lock")
        self.assertTrue(self.watcher.should_ignore_path(posix_path))

        # Windows-style path with backslashes
        win_path = PureWindowsPath(r"C:\project\.git\config.lock")
        self.assertTrue(self.watcher.should_ignore_path(win_path))

        # Windows-style path with forward slashes (also valid on Windows)
        win_path_forward = PureWindowsPath("C:/project/.git/config.lock")
        self.assertTrue(self.watcher.should_ignore_path(win_path_forward))


class TestFileWatcherDispatch(unittest.TestCase):
    """Test suite for FileWatcher.dispatch method, especially for move events."""

    def setUp(self):
        """Set up a FileWatcher instance with a mock handler for testing."""
        self.handler_called = False
        self.handler_filepath = None
        self.handler_event_type = None

        def mock_handler(filepath, event_type, content):
            self.handler_called = True
            self.handler_filepath = filepath
            self.handler_event_type = event_type

        self.watcher = FileWatcher(handlers=[mock_handler])

    def test_move_from_ignored_to_non_ignored_should_trigger_handler(self):
        """
        Test that moving a file from an ignored path (.abstra/temp/) to a non-ignored
        path (abstra.json) triggers the handler.

        This is the bug fix for: os.replace() from .abstra/temp/file.tmp to abstra.json
        was being ignored because only src_path was checked.
        """
        # Create a move event from .abstra/temp/ to abstra.json
        event = FileMovedEvent(
            src_path="/project/.abstra/temp/abstra.json.abc123.tmp",
            dest_path="/project/abstra.json",
        )

        # Mock Timer to execute immediately instead of with delay
        with patch("threading.Timer") as mock_timer:
            mock_timer_instance = MagicMock()
            mock_timer.return_value = mock_timer_instance

            self.watcher.dispatch(event)

            # Timer should have been started
            mock_timer.assert_called_once()
            # Get the function that was passed to Timer
            timer_func = mock_timer.call_args[1]["function"]
            # Execute the handler function
            timer_func()

        # Handler should have been called
        self.assertTrue(self.handler_called)
        # Filepath should be the destination path
        self.assertEqual(str(self.handler_filepath), "/project/abstra.json")
        self.assertEqual(self.handler_event_type, "moved")

    def test_move_within_ignored_path_should_not_trigger_handler(self):
        """
        Test that moving a file within ignored paths does NOT trigger the handler.
        """
        # Create a move event within .abstra/
        event = FileMovedEvent(
            src_path="/project/.abstra/temp/file1.tmp",
            dest_path="/project/.abstra/temp/file2.tmp",
        )

        with patch("threading.Timer") as mock_timer:
            self.watcher.dispatch(event)
            # Timer should NOT have been started
            mock_timer.assert_not_called()

    def test_move_from_non_ignored_to_ignored_should_trigger_handler(self):
        """
        Test that moving a file from a non-ignored path to an ignored path
        still triggers the handler (for the source path).
        """
        # Create a move event from a normal file to .abstra/
        event = FileMovedEvent(
            src_path="/project/some_file.py",
            dest_path="/project/.abstra/backup/some_file.py",
        )

        with patch("threading.Timer") as mock_timer:
            mock_timer_instance = MagicMock()
            mock_timer.return_value = mock_timer_instance

            self.watcher.dispatch(event)

            # Timer should have been started
            mock_timer.assert_called_once()
            # Get the function that was passed to Timer
            timer_func = mock_timer.call_args[1]["function"]
            # Execute the handler function
            timer_func()

        # Handler should have been called
        self.assertTrue(self.handler_called)
        self.assertEqual(self.handler_event_type, "moved")

    def test_modified_event_on_ignored_path_should_not_trigger_handler(self):
        """
        Test that a modified event on an ignored path does NOT trigger the handler.
        """
        event = FileModifiedEvent(src_path="/project/.abstra/settings.json")

        with patch("threading.Timer") as mock_timer:
            self.watcher.dispatch(event)
            # Timer should NOT have been started
            mock_timer.assert_not_called()

    def test_modified_event_on_non_ignored_path_should_trigger_handler(self):
        """
        Test that a modified event on a non-ignored path triggers the handler.
        """
        event = FileModifiedEvent(src_path="/project/main.py")

        with patch("threading.Timer") as mock_timer:
            mock_timer_instance = MagicMock()
            mock_timer.return_value = mock_timer_instance

            self.watcher.dispatch(event)

            # Timer should have been started
            mock_timer.assert_called_once()

    def test_create_then_modify_reports_created(self):
        """A new file's create+modify burst must coalesce to 'created' (not
        'changed'), so the frontend (which skips refetch on 'changed') still
        refreshes the tree. Plain content edits must stay 'changed'."""
        events = []
        watcher = FileWatcher(handlers=[lambda fp, ev, content: events.append(ev)])

        with patch("threading.Timer") as mock_timer:
            mock_timer.return_value = MagicMock()
            watcher.dispatch(FileCreatedEvent(src_path="/project/data/new.csv"))
            watcher.dispatch(FileModifiedEvent(src_path="/project/data/new.csv"))
            fire = mock_timer.call_args.kwargs["function"]
            fire()

        self.assertEqual(events, ["created"])

    def test_modify_only_reports_changed(self):
        """A plain content edit (no create) stays 'changed' so it doesn't trigger
        a structural refetch."""
        events = []
        watcher = FileWatcher(handlers=[lambda fp, ev, content: events.append(ev)])

        with patch("threading.Timer") as mock_timer:
            mock_timer.return_value = MagicMock()
            watcher.dispatch(FileModifiedEvent(src_path="/project/main.py"))
            fire = mock_timer.call_args.kwargs["function"]
            fire()

        self.assertEqual(events, ["changed"])

    def test_fired_debounce_timer_is_pruned(self):
        """Once a debounce timer fires it must be removed from _debounce_timers,
        so the dict doesn't grow unbounded over a long-lived watcher's lifetime."""
        event = FileModifiedEvent(src_path="/project/data/out.csv")

        with patch("threading.Timer") as mock_timer:
            mock_timer.return_value = MagicMock()
            self.watcher.dispatch(event)

            # Entry is tracked while the timer is pending.
            self.assertIn("/project/data/out.csv", self.watcher._debounce_timers)

            # Simulate the timer firing.
            fire = mock_timer.call_args.kwargs["function"]
            fire()

        self.assertNotIn("/project/data/out.csv", self.watcher._debounce_timers)


class TestFileWatcherStop(unittest.TestCase):
    """Tests for the graceful-shutdown stop() method of FileWatcher."""

    def test_stop_without_start_is_noop(self):
        """stop() must be safe when start() was never called."""
        watcher = FileWatcher(handlers=[])
        watcher.stop()  # must not raise

    def test_stop_stops_observer_and_joins(self):
        """stop() must call observer.stop() and observer.join(timeout=...)."""
        watcher = FileWatcher(handlers=[])
        fake_observer = MagicMock()
        watcher._observer = fake_observer

        watcher.stop(timeout=3.0)

        fake_observer.stop.assert_called_once_with()
        fake_observer.join.assert_called_once_with(timeout=3.0)

    def test_stop_cancels_debounce_timers(self):
        """Pending per-file debounce timers must be cancelled and cleared."""
        watcher = FileWatcher(handlers=[])
        watcher._observer = MagicMock()
        timer_a = MagicMock()
        timer_b = MagicMock()
        watcher._debounce_timers = {"a": timer_a, "b": timer_b}

        watcher.stop()

        timer_a.cancel.assert_called_once_with()
        timer_b.cancel.assert_called_once_with()
        self.assertEqual(watcher._debounce_timers, {})

    def test_stop_cancels_modules_folder_timer(self):
        """Pending modules-folder debounce timer must be cancelled and cleared."""
        watcher = FileWatcher(handlers=[])
        watcher._observer = MagicMock()
        modules_timer = MagicMock()
        watcher._modules_folder_timer = modules_timer

        watcher.stop()

        modules_timer.cancel.assert_called_once_with()
        self.assertIsNone(watcher._modules_folder_timer)

    def test_stop_swallows_observer_exception(self):
        """Exceptions from observer.stop() must not propagate — shutdown cannot fail."""
        watcher = FileWatcher(handlers=[])
        fake_observer = MagicMock()
        fake_observer.stop.side_effect = RuntimeError("boom")
        watcher._observer = fake_observer

        watcher.stop()  # must not raise

        fake_observer.stop.assert_called_once()

    def test_stop_swallows_timer_cancel_exception(self):
        """Timer.cancel() failures must not prevent the rest of stop() from running."""
        watcher = FileWatcher(handlers=[])
        watcher._observer = MagicMock()
        bad_timer = MagicMock()
        bad_timer.cancel.side_effect = RuntimeError("boom")
        good_timer = MagicMock()
        watcher._debounce_timers = {"a": bad_timer, "b": good_timer}

        watcher.stop()

        good_timer.cancel.assert_called_once_with()
        self.assertEqual(watcher._debounce_timers, {})


class TestFileWatcherRoots(unittest.TestCase):
    """Tests for the configurable watch roots (worker watches /project + /files)."""

    @patch("abstra_internals.services.file_watcher.Observer")
    def test_default_watches_settings_root(self, mock_observer_cls):
        from abstra_internals.settings import Settings, SettingsController

        with patch.object(SettingsController, "_root_path", Path("/project")):
            watcher = FileWatcher(handlers=[])
            watcher.start()

            observer = mock_observer_cls.return_value
            observer.schedule.assert_called_once()
            self.assertEqual(
                observer.schedule.call_args.kwargs["path"], str(Settings.root_path)
            )

    @patch("abstra_internals.services.file_watcher.Observer")
    def test_multiple_roots_each_scheduled(self, mock_observer_cls):
        roots = [Path("/project"), Path("/files")]
        watcher = FileWatcher(handlers=[], roots=roots)
        watcher.start()

        observer = mock_observer_cls.return_value
        scheduled = {call.kwargs["path"] for call in observer.schedule.call_args_list}
        self.assertEqual(scheduled, {"/project", "/files"})
        for call in observer.schedule.call_args_list:
            self.assertTrue(call.kwargs["recursive"])
        observer.start.assert_called_once()


if __name__ == "__main__":
    unittest.main()
