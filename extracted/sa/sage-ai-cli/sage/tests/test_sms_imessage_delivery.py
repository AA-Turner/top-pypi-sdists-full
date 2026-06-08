"""Tests for the iMessage delivery verification primitives.

Covers `_imessage_max_rowid` and `_imessage_row_matches` against a fake
chat.db at a temp path — does NOT touch the user's real Messages history,
and does NOT actually send any iMessage.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from unittest.mock import patch

import pytest

from sage.core.sms_bridge import (
    _imessage_max_rowid,
    _imessage_row_matches,
)


@pytest.fixture
def fake_chat_db(tmp_path):
    """Build a minimal chat.db with the same `message` schema iMessage uses."""
    db_path = tmp_path / "chat.db"
    with sqlite3.connect(db_path) as db:
        db.execute(
            "CREATE TABLE message ("
            "  rowid INTEGER PRIMARY KEY, "
            "  text TEXT, "
            "  is_from_me INTEGER"
            ")"
        )
        # Seed two existing rows (mixed inbound + outbound) so baseline > 0
        db.execute("INSERT INTO message (rowid, text, is_from_me) VALUES (1, 'inbound msg', 0)")
        db.execute("INSERT INTO message (rowid, text, is_from_me) VALUES (2, 'old outbound', 1)")
        db.commit()
    return str(db_path)


def _patch_path_to(fake_path: str):
    """Make os.path.expanduser('~/Library/Messages/chat.db') resolve to fake_path."""
    real_expand = os.path.expanduser

    def fake_expand(p):
        if p == "~/Library/Messages/chat.db":
            return fake_path
        return real_expand(p)

    return patch.object(os.path, "expanduser", side_effect=fake_expand)


@pytest.mark.skipif(sys.platform != "darwin", reason="iMessage helpers are macOS-only")
class TestIMessageRowIdHelpers:

    def test_max_rowid_returns_existing_max(self, fake_chat_db):
        with _patch_path_to(fake_chat_db):
            assert _imessage_max_rowid() == 2

    def test_max_rowid_handles_missing_db(self, tmp_path):
        missing = str(tmp_path / "nope.db")
        with _patch_path_to(missing):
            assert _imessage_max_rowid() == 0

    def test_row_matches_finds_new_outbound(self, fake_chat_db):
        with sqlite3.connect(fake_chat_db) as db:
            db.execute(
                "INSERT INTO message (rowid, text, is_from_me) VALUES (3, ?, 1)",
                ("hello world",),
            )
            db.commit()
        with _patch_path_to(fake_chat_db):
            assert _imessage_row_matches(prev_max_rowid=2, text="hello world") is True

    def test_row_matches_ignores_inbound(self, fake_chat_db):
        """Inbound messages (is_from_me=0) must not count as a successful send."""
        with sqlite3.connect(fake_chat_db) as db:
            db.execute(
                "INSERT INTO message (rowid, text, is_from_me) VALUES (3, ?, 0)",
                ("hello world",),
            )
            db.commit()
        with _patch_path_to(fake_chat_db):
            assert _imessage_row_matches(prev_max_rowid=2, text="hello world") is False

    def test_row_matches_ignores_pre_baseline_rows(self, fake_chat_db):
        """An outbound row that existed before send shouldn't count as success."""
        with _patch_path_to(fake_chat_db):
            # row 2 is "old outbound" - it existed before; baseline=2 excludes it
            assert _imessage_row_matches(prev_max_rowid=2, text="old outbound") is False

    def test_row_matches_handles_truncation_at_200(self, fake_chat_db):
        """Long messages are compared only on first 200 chars (the db storage)."""
        long_msg = "x" * 500
        stored = long_msg[:200]  # iMessage may truncate or chunk; our match uses 200
        with sqlite3.connect(fake_chat_db) as db:
            db.execute(
                "INSERT INTO message (rowid, text, is_from_me) VALUES (3, ?, 1)",
                (stored,),
            )
            db.commit()
        with _patch_path_to(fake_chat_db):
            assert _imessage_row_matches(prev_max_rowid=2, text=long_msg) is True


@pytest.mark.skipif(sys.platform == "darwin", reason="non-darwin guard")
class TestNonDarwinShortCircuit:
    """The helpers must short-circuit on non-darwin without touching disk."""

    def test_max_rowid_short_circuits(self):
        assert _imessage_max_rowid() == 0

    def test_row_matches_short_circuits(self):
        assert _imessage_row_matches(prev_max_rowid=0, text="x") is False
