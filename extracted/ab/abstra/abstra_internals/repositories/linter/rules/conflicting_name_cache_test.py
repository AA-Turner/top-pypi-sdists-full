"""Item 5: reserved_names() scans the whole sys.path via iter_modules() on every
pass. Cache it (lock + project-path guard), recomputed on package install via the
full-pass refresh (the set only changes when packages change)."""

import threading
import time
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.repositories.linter.rules.conflicting_name import (
    _ReservedNamesCache,
    reserved_names,
)
from abstra_internals.settings import SettingsController
from tests.fixtures import clear_dir, init_dir

_ITER = "abstra_internals.repositories.linter.rules.conflicting_name.iter_modules"


class _FakeFinder:
    def __init__(self, path):
        self.path = path


class _FakeModule:
    def __init__(self, name, path="/elsewhere"):
        self.name = name
        self.module_finder = _FakeFinder(path)


def _fake_modules():
    return [_FakeModule("email"), _FakeModule("os")]


class ReservedNamesCacheTest(TestCase):
    def setUp(self):
        self.root = init_dir()
        _ReservedNamesCache.invalidate()

    def tearDown(self):
        _ReservedNamesCache.invalidate()
        clear_dir(self.root)

    def test_second_call_does_not_rescan_sys_path(self):
        with patch(_ITER, return_value=_fake_modules()) as mock:
            reserved_names()
            reserved_names()
        self.assertEqual(mock.call_count, 1)

    def test_invalidate_forces_recompute(self):
        with patch(_ITER, return_value=_fake_modules()) as mock:
            reserved_names()
            _ReservedNamesCache.invalidate()
            reserved_names()
        self.assertEqual(mock.call_count, 2)

    def test_cache_keyed_by_project_path(self):
        with patch(_ITER, return_value=_fake_modules()) as mock:
            reserved_names()
            other = init_dir()
            try:
                reserved_names()  # different root_path → must recompute
            finally:
                clear_dir(other)
                SettingsController.set_root_path(self.root.as_posix())
        self.assertEqual(mock.call_count, 2)

    def test_cache_returns_same_value_as_uncached(self):
        with patch(_ITER, return_value=_fake_modules()):
            cached = reserved_names()
        self.assertIn("email", cached)
        self.assertIn("os", cached)

    def test_concurrent_get_computes_once(self):
        count = [0]

        def slow():
            count[0] += 1
            time.sleep(0.05)
            return _fake_modules()

        with patch(_ITER, side_effect=slow):
            threads = [
                threading.Thread(target=_ReservedNamesCache.get) for _ in range(8)
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        self.assertEqual(count[0], 1)
