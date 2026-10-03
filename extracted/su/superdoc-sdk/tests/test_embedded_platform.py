from __future__ import annotations

import os
import stat
import tempfile
import time
import unittest
from pathlib import Path

from superdoc.embedded_platform import ensure_executable


def _metadata(path: Path) -> tuple[int, int]:
    info = path.stat()
    return stat.S_IMODE(info.st_mode), info.st_ctime_ns


@unittest.skipIf(os.name == 'nt', 'execute bits are POSIX-only')
class EnsureExecutableTests(unittest.TestCase):
    def setUp(self) -> None:
        self._directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._directory.cleanup)

    def _binary_with_mode(self, mode: int) -> Path:
        binary = Path(self._directory.name) / f'superdoc-{mode:o}'
        binary.write_bytes(b'#!/bin/sh\n')
        binary.chmod(mode)
        # ctime has coarse resolution on some filesystems; a write after this
        # pause is guaranteed to land on a later timestamp.
        time.sleep(0.02)
        return binary

    def test_leaves_an_executable_binary_untouched(self) -> None:
        for mode in (0o755, 0o700, 0o555, 0o777):
            with self.subTest(mode=oct(mode)):
                binary = self._binary_with_mode(mode)
                before = _metadata(binary)

                ensure_executable(str(binary))

                self.assertEqual(_metadata(binary), before)

    def test_adds_only_the_execute_bits(self) -> None:
        for mode, repaired in ((0o644, 0o755), (0o600, 0o711), (0o640, 0o751)):
            with self.subTest(mode=oct(mode)):
                binary = self._binary_with_mode(mode)
                _, ctime_before = _metadata(binary)

                ensure_executable(str(binary))

                repaired_mode, ctime_after = _metadata(binary)
                self.assertEqual(repaired_mode, repaired)
                self.assertNotEqual(ctime_after, ctime_before)

    def test_does_not_raise_when_the_binary_cannot_be_prepared(self) -> None:
        ensure_executable(str(Path(self._directory.name) / 'missing' / 'superdoc'))


if __name__ == '__main__':
    unittest.main()
