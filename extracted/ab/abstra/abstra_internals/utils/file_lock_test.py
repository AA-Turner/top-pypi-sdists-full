import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

from abstra_internals.utils.file_lock import create_file_lock, try_file_lock


class FileLockTest(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.lock_path = str(Path(tmp.name) / "test.lock")

    def test_try_lock_acquires_when_free_and_releases_on_exit(self):
        with try_file_lock(self.lock_path) as acquired:
            self.assertTrue(acquired)
        # Released on exit -> a fresh lock can take it again.
        lock = create_file_lock(self.lock_path)
        self.assertTrue(lock.try_acquire())
        lock.release()

    def test_try_lock_returns_false_while_another_process_holds_it(self):
        # POSIX fcntl locks are per-process, so exclusion can only be exercised
        # across processes. Spawn a child that grabs the lock and holds it while
        # writing a ready marker; the parent must then fail to acquire.
        ready = f"{self.lock_path}.ready"
        child_src = textwrap.dedent(f"""
            import time
            from abstra_internals.utils.file_lock import create_file_lock
            lock = create_file_lock({self.lock_path!r})
            lock.acquire()
            open({ready!r}, "w").close()
            time.sleep(3)
        """)
        proc = subprocess.Popen([sys.executable, "-c", child_src])
        try:
            deadline = time.monotonic() + 10
            while not Path(ready).exists():
                if time.monotonic() > deadline:
                    self.fail("child did not acquire the lock in time")
                time.sleep(0.05)

            with try_file_lock(self.lock_path) as acquired:
                self.assertFalse(acquired)
        finally:
            proc.wait(timeout=10)

        # Once the child exits, the OS drops its lock and we can acquire again.
        with try_file_lock(self.lock_path) as acquired:
            self.assertTrue(acquired)


if __name__ == "__main__":
    unittest.main()
