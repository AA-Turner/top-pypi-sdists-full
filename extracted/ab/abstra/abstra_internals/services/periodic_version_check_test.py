import unittest
from datetime import timedelta
from unittest.mock import patch

from abstra_internals.services.periodic_version_check import PeriodicVersionChecker

_MOD = "abstra_internals.services.periodic_version_check"


class PeriodicVersionCheckerTest(unittest.TestCase):
    def test_check_once_refreshes_when_editor_active(self):
        checker = PeriodicVersionChecker()
        with patch(f"{_MOD}.EditorStatusEventController") as controller:
            controller.has_listeners.return_value = True
            checker._check_once()

        controller.refresh_and_broadcast.assert_called_once()

    def test_check_once_skips_when_no_listeners(self):
        checker = PeriodicVersionChecker()
        with patch(f"{_MOD}.EditorStatusEventController") as controller:
            controller.has_listeners.return_value = False
            checker._check_once()

        controller.refresh_and_broadcast.assert_not_called()

    def test_start_then_stop_lifecycle(self):
        # A long interval means the loop just waits on the stop event; stop()
        # must interrupt it near-instantly and join the thread.
        checker = PeriodicVersionChecker(interval=timedelta(hours=1))
        checker.start()
        self.assertIsNotNone(checker._thread)
        self.assertTrue(checker._thread.is_alive())  # type: ignore[union-attr]

        checker.stop(timeout=5.0)
        self.assertIsNone(checker._thread)

    def test_stop_is_safe_without_start(self):
        PeriodicVersionChecker().stop()


if __name__ == "__main__":
    unittest.main()
