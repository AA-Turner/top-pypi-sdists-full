"""Cross-tenant isolation tests for nx_brain_local.

Confirms that user A's $brain rows are NEVER returned to user B, even when:
- The same SQLite database file is shared (it is — ~/.nx/brain.db).
- The two users' queries happen to match the same content.
- One user searches with wildcard-like inputs.

This is a structural test of the local memory layer that backs $brain*.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path


class BrainIsolationTests(unittest.TestCase):
    def setUp(self):
        # Force the brain DB into a tempfile per test so we don't touch the
        # user's real ~/.nx/brain.db.
        self.tmp = tempfile.mkdtemp(prefix="nx-brain-isolation-")
        # Reach into nx_brain_local and redirect _DB_PATH before each test.
        import nx_brain_local
        self._orig_db = nx_brain_local._DB_PATH
        nx_brain_local._DB_PATH = Path(self.tmp) / "brain.db"
        nx_brain_local._INITIALIZED = False

    def tearDown(self):
        import nx_brain_local
        nx_brain_local._DB_PATH = self._orig_db
        nx_brain_local._INITIALIZED = False
        try:
            import shutil
            shutil.rmtree(self.tmp, ignore_errors=True)
        except Exception:
            pass

    def test_user_b_cannot_see_user_a_rows(self):
        import nx_brain_local
        nx_brain_local.save(user_id="user-A", content="secret A note", label="alpha", world="cowork")
        nx_brain_local.save(user_id="user-B", content="public B note",  label="beta",  world="cowork")

        # Same query, different user_ids
        a_hits = nx_brain_local.search("user-A", "note")
        b_hits = nx_brain_local.search("user-B", "note")

        self.assertEqual(len(a_hits), 1)
        self.assertEqual(a_hits[0]["label"], "alpha")
        self.assertEqual(a_hits[0]["content"], "secret A note")

        self.assertEqual(len(b_hits), 1)
        self.assertEqual(b_hits[0]["label"], "beta")
        self.assertEqual(b_hits[0]["content"], "public B note")

    def test_search_does_not_leak_across_users_on_exact_label_match(self):
        import nx_brain_local
        nx_brain_local.save(user_id="user-A", content="shared text token", label="shared", world="cowork")
        nx_brain_local.save(user_id="user-B", content="shared text token", label="shared", world="cowork")

        a_hits = nx_brain_local.search("user-A", "shared")
        for r in a_hits:
            self.assertEqual(r["user_id"], "user-A",
                             f"User A search returned a row owned by {r['user_id']}")
        b_hits = nx_brain_local.search("user-B", "shared")
        for r in b_hits:
            self.assertEqual(r["user_id"], "user-B",
                             f"User B search returned a row owned by {r['user_id']}")

    def test_count_per_user_is_isolated(self):
        import nx_brain_local
        for i in range(5):
            nx_brain_local.save(user_id="user-A", content=f"A row {i}", label=f"a-{i}", world="cowork")
        for i in range(3):
            nx_brain_local.save(user_id="user-B", content=f"B row {i}", label=f"b-{i}", world="cowork")

        self.assertEqual(nx_brain_local.count("user-A"), 5)
        self.assertEqual(nx_brain_local.count("user-B"), 3)
        self.assertEqual(nx_brain_local.count("user-C"), 0)

    def test_delete_only_affects_caller_rows(self):
        import nx_brain_local
        nx_brain_local.save(user_id="user-A", content="A row", label="conflict", world="cowork")
        nx_brain_local.save(user_id="user-B", content="B row", label="conflict", world="cowork")

        deleted = nx_brain_local.delete_by_label("user-A", "conflict")
        self.assertEqual(deleted, 1)

        # User B's row with the same label must still be there.
        b_hits = nx_brain_local.search("user-B", "conflict")
        self.assertEqual(len(b_hits), 1)
        self.assertEqual(b_hits[0]["content"], "B row")

    def test_empty_user_id_returns_nothing(self):
        import nx_brain_local
        nx_brain_local.save(user_id="user-A", content="secret", label="x", world="cowork")
        self.assertEqual(nx_brain_local.search("", "secret"), [])
        self.assertEqual(nx_brain_local.search(None, "secret"), [])  # type: ignore[arg-type]

    def test_wildcard_input_does_not_bypass_user_filter(self):
        """A user typing SQL/like wildcards in their search must not see
        other users' rows. The local brain uses LIKE with the input as a
        bound parameter — confirm the user_id filter still wins."""
        import nx_brain_local
        nx_brain_local.save(user_id="user-A", content="alpha", label="a", world="cowork")
        nx_brain_local.save(user_id="user-B", content="bravo", label="b", world="cowork")

        # User A searches for '%' — should match their own rows by content,
        # not user B's.
        hits = nx_brain_local.search("user-A", "%")
        for r in hits:
            self.assertEqual(r["user_id"], "user-A")


class BrainSchemaTests(unittest.TestCase):
    """Audit-Y: forward-only schema ladder must refuse a future-schema DB
    and accept the current one cleanly."""

    def setUp(self):
        import nx_brain_local
        self.tmp = tempfile.mkdtemp(prefix="nx-brain-schema-")
        self._orig_db = nx_brain_local._DB_PATH
        nx_brain_local._DB_PATH = Path(self.tmp) / "brain.db"
        nx_brain_local._INITIALIZED = False

    def tearDown(self):
        import nx_brain_local, shutil as _sh
        nx_brain_local._DB_PATH = self._orig_db
        nx_brain_local._INITIALIZED = False
        _sh.rmtree(self.tmp, ignore_errors=True)

    def test_current_schema_initialises_clean(self):
        import nx_brain_local
        nx_brain_local._ensure_schema()
        v = nx_brain_local.schema_version()
        self.assertEqual(v, nx_brain_local.BRAIN_SCHEMA_VERSION)

    def test_future_schema_db_is_refused(self):
        import sqlite3
        import nx_brain_local
        # Pre-seed a DB at user_version = 99, much higher than current.
        conn = sqlite3.connect(str(nx_brain_local._DB_PATH))
        conn.execute("PRAGMA user_version = 99")
        conn.close()
        nx_brain_local._INITIALIZED = False
        with self.assertRaises(RuntimeError) as ctx:
            nx_brain_local._ensure_schema()
        self.assertIn("schema", str(ctx.exception).lower())
        self.assertIn("99", str(ctx.exception))

    def test_save_after_normal_init_succeeds(self):
        import nx_brain_local
        r = nx_brain_local.save(
            user_id="schema-test-user",
            content="hello",
            label="x",
            world="cowork",
        )
        self.assertTrue(r.get("success"))
        self.assertEqual(nx_brain_local.count("schema-test-user"), 1)


if __name__ == "__main__":
    unittest.main()
