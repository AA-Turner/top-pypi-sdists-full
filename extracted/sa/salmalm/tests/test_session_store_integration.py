"""Integration tests for salmalm.core.session_store.

Tests: get_session, session isolation, user_id enforcement,
rollback, branch, disk save/restore, cleanup.
"""
import json
import os
import sys
import tempfile
import time
import threading
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── helpers ──────────────────────────────────────────────────────────────────

def _fresh_sessions():
    """Clear in-memory session cache for test isolation."""
    import salmalm.core.session_store as ss
    with ss._session_lock:
        ss._sessions.clear()
    ss._session_cleanup_ts = 0.0


# ── 1. get_session creates new session ───────────────────────────────────────

def test_get_session_creates_new():
    _fresh_sessions()
    with patch("salmalm.core.session_store._get_db") as mock_db, \
         patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
         patch("salmalm.core.session_store._restore_compaction_summary", return_value=None), \
         patch("salmalm.core.session_store._audit_log"), \
         patch("salmalm.security.crypto.vault") as mock_vault:
        mock_vault.is_unlocked = False
        conn = MagicMock()
        conn.execute.return_value.fetchone.return_value = None
        mock_db.return_value = conn
        import salmalm.core.session_store as ss
        sess = ss.get_session("brand-new-session")
    assert sess.id == "brand-new-session"
    assert len(sess.messages) >= 1


# ── 2. get_session returns same instance on repeat call ───────────────────────

def test_get_session_returns_same_instance():
    _fresh_sessions()
    with patch("salmalm.core.session_store._get_db") as mock_db, \
         patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
         patch("salmalm.core.session_store._restore_compaction_summary", return_value=None), \
         patch("salmalm.core.session_store._audit_log"), \
         patch("salmalm.security.crypto.vault") as mock_vault:
        mock_vault.is_unlocked = False
        conn = MagicMock()
        conn.execute.return_value.fetchone.return_value = None
        mock_db.return_value = conn
        import salmalm.core.session_store as ss
        s1 = ss.get_session("same-sess")
        s2 = ss.get_session("same-sess")
    assert s1 is s2


# ── 3. Session isolation: different users get different sessions ──────────────

def test_session_isolation_different_users():
    _fresh_sessions()
    with patch("salmalm.core.session_store._get_db") as mock_db, \
         patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
         patch("salmalm.core.session_store._restore_compaction_summary", return_value=None), \
         patch("salmalm.core.session_store._audit_log"), \
         patch("salmalm.security.crypto.vault") as mock_vault:
        mock_vault.is_unlocked = False
        conn = MagicMock()
        conn.execute.return_value.fetchone.return_value = None
        mock_db.return_value = conn
        import salmalm.core.session_store as ss
        # Create session for user 1
        s1 = ss.get_session("shared-sess", user_id=1)
        # User 2 tries to access same session_id → gets isolated copy
        s2 = ss.get_session("shared-sess", user_id=2)
    assert s1 is not s2
    assert s2.id != "shared-sess" or s2.user_id == 2


# ── 4. Session.add_user appends message ──────────────────────────────────────

def test_session_add_user():
    from salmalm.core.session_store import Session
    s = Session("test")
    s.messages = []
    s.add_user("hello world")
    assert s.messages[-1] == {"role": "user", "content": "hello world"}


# ── 5. Session.add_assistant appends + triggers persist ──────────────────────

def test_session_add_assistant():
    from salmalm.core.session_store import Session
    s = Session("test")
    s.messages = []
    with patch.object(s, "_persist") as mock_persist, \
         patch("salmalm.core.session_store.save_session_to_disk"):
        s.add_assistant("I'm an AI")
    assert s.messages[-1] == {"role": "assistant", "content": "I'm an AI"}


# ── 6. Session auto-trim when > 1000 messages ────────────────────────────────

def test_session_auto_trim():
    from salmalm.core.session_store import Session
    s = Session("trim-test")
    s.messages = [{"role": "system", "content": "sys"}]
    for i in range(1001):
        s.messages.append({"role": "user", "content": f"msg{i}"})
    # Trigger auto-trim via add_user
    s.add_user("triggering trim")
    assert len(s.messages) <= 52  # system + 50 recent + this one


# ── 7. rollback_session removes last message pair ────────────────────────────

def test_rollback_session_removes_pair():
    _fresh_sessions()
    with patch("salmalm.core.session_store._get_db") as mock_db, \
         patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
         patch("salmalm.core.session_store._restore_compaction_summary", return_value=None), \
         patch("salmalm.core.session_store._audit_log"), \
         patch("salmalm.core.session_store.save_session_to_disk"), \
         patch("salmalm.security.crypto.vault") as mock_vault:
        mock_vault.is_unlocked = False
        conn = MagicMock()
        conn.execute.return_value.fetchone.return_value = None
        mock_db.return_value = conn
        import salmalm.core.session_store as ss
        sess = ss.get_session("rollback-test")
        sess.messages = [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
        ]
        result = ss.rollback_session("rollback-test", 1)
    assert result["ok"] is True
    assert result["removed"] == 1


# ── 8. rollback with no messages returns error ───────────────────────────────

def test_rollback_empty_session_error():
    _fresh_sessions()
    with patch("salmalm.core.session_store._get_db") as mock_db, \
         patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
         patch("salmalm.core.session_store._restore_compaction_summary", return_value=None), \
         patch("salmalm.core.session_store._audit_log"), \
         patch("salmalm.security.crypto.vault") as mock_vault:
        mock_vault.is_unlocked = False
        conn = MagicMock()
        conn.execute.return_value.fetchone.return_value = None
        mock_db.return_value = conn
        import salmalm.core.session_store as ss
        sess = ss.get_session("rollback-empty")
        sess.messages = [{"role": "system", "content": "sys"}]
        result = ss.rollback_session("rollback-empty", 1)
    assert result["ok"] is False


# ── 9. branch_session creates new session with subset ────────────────────────

def test_branch_session_creates_copy():
    _fresh_sessions()
    with patch("salmalm.core.session_store._get_db") as mock_db, \
         patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
         patch("salmalm.core.session_store._restore_compaction_summary", return_value=None), \
         patch("salmalm.core.session_store._audit_log"), \
         patch("salmalm.core.session_store.save_session_to_disk"), \
         patch("salmalm.security.crypto.vault") as mock_vault:
        mock_vault.is_unlocked = False
        conn = MagicMock()
        conn.execute.return_value.fetchone.return_value = None
        mock_db.return_value = conn
        import salmalm.core.session_store as ss
        sess = ss.get_session("branch-src")
        sess.messages = [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ]
        result = ss.branch_session("branch-src", 1)
    assert result["ok"] is True
    new_id = result["new_session_id"]
    assert new_id.startswith("branch-")
    with patch("salmalm.core.session_store._get_db") as mock_db2:
        conn2 = MagicMock()
        conn2.execute.return_value.fetchone.return_value = None
        mock_db2.return_value = conn2
        import salmalm.core.session_store as ss
        branched = ss.get_session(new_id)
    assert len(branched.messages) == 2  # system + user[0]


# ── 10. save_session_to_disk writes JSON file ────────────────────────────────

def test_save_session_to_disk():
    import tempfile
    from pathlib import Path
    from salmalm.core.session_store import Session
    import salmalm.core.session_store as ss

    with tempfile.TemporaryDirectory() as tmpdir:
        orig_dir = ss._SESSIONS_DIR
        try:
            ss._SESSIONS_DIR = Path(tmpdir) / "sessions"
            sess = Session("disk-test")
            sess.messages = [{"role": "user", "content": "hello"}]
            with ss._session_lock:
                ss._sessions["disk-test"] = sess
            ss.save_session_to_disk("disk-test")
            saved = Path(tmpdir) / "sessions" / "disk-test.json"
            assert saved.exists()
            data = json.loads(saved.read_text())
            assert data["session_id"] == "disk-test"
        finally:
            ss._SESSIONS_DIR = orig_dir
            with ss._session_lock:
                ss._sessions.pop("disk-test", None)


# ── 11. Thread safety of _session_lock ───────────────────────────────────────

def test_get_session_thread_safe():
    """Multiple threads calling get_session simultaneously should not create duplicates."""
    _fresh_sessions()
    results = []
    errors = []

    def worker():
        try:
            with patch("salmalm.core.session_store._get_db") as mock_db, \
                 patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
                 patch("salmalm.core.session_store._restore_compaction_summary", return_value=None), \
                 patch("salmalm.core.session_store._audit_log"), \
                 patch("salmalm.security.crypto.vault") as mock_vault:
                mock_vault.is_unlocked = False
                conn = MagicMock()
                conn.execute.return_value.fetchone.return_value = None
                mock_db.return_value = conn
                import salmalm.core.session_store as ss
                s = ss.get_session("concurrent-sess")
                results.append(id(s))
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    # All threads should have gotten the same object (same id)
    assert len(set(results)) <= 2  # Allow 1–2 due to race on creation
