import unittest
from collections import OrderedDict

from abstra_internals.controllers.codebase_events import (
    CodebaseEventController,
    _lru_set,
)
from tests.fixtures import BaseTest


class TestLruSet(unittest.TestCase):
    def test_evicts_lru_when_exceeding_cap(self):
        od: "OrderedDict[str, int]" = OrderedDict()
        for i in range(5):
            _lru_set(od, f"k{i}", i, max_size=3)
        self.assertEqual(list(od.keys()), ["k2", "k3", "k4"])

    def test_reinsert_refreshes_mru(self):
        od: "OrderedDict[str, int]" = OrderedDict()
        for i in range(3):
            _lru_set(od, f"k{i}", i, max_size=3)
        # Touch k0 again -> it becomes most-recent, so the next insert evicts k1.
        _lru_set(od, "k0", 99, max_size=3)
        _lru_set(od, "k3", 3, max_size=3)
        self.assertEqual(list(od.keys()), ["k2", "k0", "k3"])

    def test_max_size_1_keeps_only_last(self):
        od: "OrderedDict[str, int]" = OrderedDict()
        for i in range(10):
            _lru_set(od, f"k{i}", i, max_size=1)
        self.assertEqual(list(od.items()), [("k9", 9)])


class TestContentHashGate(BaseTest):
    """_content_changed must skip lint when a path's content hash is unchanged,
    and re-lint on real changes / deletions. Class-level state is snapshotted."""

    def setUp(self) -> None:
        super().setUp()
        self._saved_hashes = OrderedDict(CodebaseEventController._content_hashes)
        self._saved_cap = CodebaseEventController._MAX_TRACKED_FILES
        CodebaseEventController._content_hashes = OrderedDict()

    def tearDown(self) -> None:
        CodebaseEventController._content_hashes = self._saved_hashes
        CodebaseEventController._MAX_TRACKED_FILES = self._saved_cap
        super().tearDown()

    def test_first_call_returns_true(self):
        f = self.root / "a.py"
        f.write_text("v1\n")
        self.assertTrue(CodebaseEventController._content_changed(f))

    def test_second_call_same_content_returns_false(self):
        f = self.root / "a.py"
        f.write_text("v1\n")
        CodebaseEventController._content_changed(f)
        self.assertFalse(CodebaseEventController._content_changed(f))

    def test_content_change_returns_true(self):
        f = self.root / "a.py"
        f.write_text("v1\n")
        CodebaseEventController._content_changed(f)
        f.write_text("v2\n")
        self.assertTrue(CodebaseEventController._content_changed(f))

    def test_missing_file_returns_true_and_drops_entry(self):
        f = self.root / "a.py"
        f.write_text("v1\n")
        CodebaseEventController._content_changed(f)
        f.unlink()
        self.assertTrue(CodebaseEventController._content_changed(f))
        self.assertNotIn(f, CodebaseEventController._content_hashes)

    def test_lru_bound_enforced(self):
        CodebaseEventController._MAX_TRACKED_FILES = 5
        for i in range(20):
            p = self.root / f"a{i}.py"
            p.write_text(f"v{i}\n")
            CodebaseEventController._content_changed(p)
        self.assertEqual(len(CodebaseEventController._content_hashes), 5)

    def test_rehash_same_content_refreshes_mru(self):
        CodebaseEventController._MAX_TRACKED_FILES = 3
        files = [self.root / f"a{i}.py" for i in range(3)]
        for i, p in enumerate(files):
            p.write_text(f"v{i}\n")
            CodebaseEventController._content_changed(p)
        # Re-hash a0 (same content) -> refreshes MRU, so adding a3 evicts a1.
        CodebaseEventController._content_changed(files[0])
        new = self.root / "a3.py"
        new.write_text("v3\n")
        CodebaseEventController._content_changed(new)
        keys = list(CodebaseEventController._content_hashes.keys())
        self.assertIn(files[0], keys)
        self.assertNotIn(files[1], keys)


class TestRequirementsGateInteraction(BaseTest):
    """In local mode (_controller_driven=False), schedule_lint_for_path must NOT
    record the content hash — otherwise the FileWatcher's lint_files for the same
    path would later be gated out and the requirements lint silently dropped."""

    def setUp(self) -> None:
        super().setUp()
        self._saved_hashes = OrderedDict(CodebaseEventController._content_hashes)
        self._saved_driven = CodebaseEventController._controller_driven
        CodebaseEventController._content_hashes = OrderedDict()

    def tearDown(self) -> None:
        CodebaseEventController._content_hashes = self._saved_hashes
        CodebaseEventController._controller_driven = self._saved_driven
        super().tearDown()

    def test_schedule_lint_does_not_record_hash_in_local_mode(self):
        CodebaseEventController._controller_driven = False
        f = self.root / "requirements.txt"
        f.write_text("abstra\n")
        CodebaseEventController.schedule_lint_for_path(f)
        self.assertNotIn(f, CodebaseEventController._content_hashes)


if __name__ == "__main__":
    unittest.main()
