import unittest
from unittest.mock import MagicMock

from abstra_internals.tasks_watcher import TasksWatcher


class TestTasksWatcherStop(unittest.TestCase):
    """Tests for the graceful-shutdown stop() method of TasksWatcher."""

    def test_stop_without_start_is_noop(self):
        """stop() must be safe when start() was never called."""
        watcher = TasksWatcher()
        watcher.stop()  # must not raise

    def test_stop_stops_observer_and_joins(self):
        """stop() must call observer.stop() and observer.join(timeout=...)."""
        watcher = TasksWatcher()
        fake_observer = MagicMock()
        watcher._observer = fake_observer

        watcher.stop(timeout=4.0)

        fake_observer.stop.assert_called_once_with()
        fake_observer.join.assert_called_once_with(timeout=4.0)

    def test_stop_swallows_observer_exception(self):
        """Exceptions from observer.stop() must not propagate."""
        watcher = TasksWatcher()
        fake_observer = MagicMock()
        fake_observer.stop.side_effect = RuntimeError("boom")
        watcher._observer = fake_observer

        watcher.stop()  # must not raise

        fake_observer.stop.assert_called_once()


if __name__ == "__main__":
    unittest.main()
