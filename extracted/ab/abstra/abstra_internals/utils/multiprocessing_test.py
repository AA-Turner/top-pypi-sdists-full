import tempfile
import unittest
from pathlib import Path

from abstra_internals.utils.multiprocessing import (
    cleanup_stale_multiprocessing_semaphores,
)


class TestCleanupStaleMultiprocessingSemaphores(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.shm_dir = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_removes_only_stale_semaphore_files(self):
        stale = [self.shm_dir / f"sem.mp-{i:08x}" for i in range(3)]
        for f in stale:
            f.write_bytes(b"\x00" * 32)
        unrelated = self.shm_dir / "psm_something"
        unrelated.write_bytes(b"\x00")

        removed = cleanup_stale_multiprocessing_semaphores(str(self.shm_dir))

        self.assertEqual(removed, 3)
        for f in stale:
            self.assertFalse(f.exists())
        self.assertTrue(unrelated.exists())

    def test_empty_dir_returns_zero(self):
        self.assertEqual(cleanup_stale_multiprocessing_semaphores(str(self.shm_dir)), 0)

    def test_missing_dir_is_noop(self):
        missing = self.shm_dir / "does-not-exist"
        self.assertEqual(cleanup_stale_multiprocessing_semaphores(str(missing)), 0)
