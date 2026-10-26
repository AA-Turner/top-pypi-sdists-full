"""The Probe service stamps the tap's 401 latch where every surface reads it.

A refused key used to read as "not recording" at best: the stamp
(`last_401_at` in the tap's state db) is written only by the tap's old outbox
drain, never by the journal path every tap since 0.4.5 delivers through
(release gate, 2026-10-25).
"""

from __future__ import annotations

import sqlite3
import types

from probe.service import keylatch

GATEWAY_401 = {"detail": "capture credentials were rejected"}


def _db(tmp_path):
    db = tmp_path / "state.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE meta (k TEXT PRIMARY KEY, v TEXT NOT NULL)")
    return db


def _meta(db):
    with sqlite3.connect(db) as conn:
        return dict(conn.execute("SELECT k, v FROM meta").fetchall())


def _fresh(monkeypatch):
    monkeypatch.setattr(keylatch, "_SEEN", {})


def test_a_gateway_401_stamps_the_latch_and_a_later_success_clears_it(tmp_path, monkeypatch):
    _fresh(monkeypatch)
    db = _db(tmp_path)
    keylatch.note("claude_code", "probe_ing_old", 401, GATEWAY_401, db=db)
    meta = _meta(db)
    assert meta[keylatch.STAMP]
    assert meta[keylatch.FINGERPRINT] == keylatch.fingerprint("probe_ing_old")
    keylatch.note("claude_code", "probe_ing_old", 200, {"ok": True}, db=db)
    assert keylatch.STAMP not in _meta(db)


def test_offline_a_5xx_and_a_proxy_page_say_nothing_about_the_key(tmp_path, monkeypatch):
    _fresh(monkeypatch)
    db = _db(tmp_path)
    for code, body in ((0, {}), (503, {"detail": "down"}), (401, {"detail": "invalid error response"}),
                       (401, {}), (407, {"detail": "proxy"})):
        keylatch.note("claude_code", "probe_ing_x", code, body, db=db)
    assert _meta(db) == {}


def test_a_success_with_a_new_key_never_clears_another_keys_stamp(tmp_path, monkeypatch):
    _fresh(monkeypatch)
    db = _db(tmp_path)
    keylatch.note("claude_code", "probe_ing_old", 401, GATEWAY_401, db=db)
    keylatch.note("claude_code", "probe_ing_new", 200, {}, db=db)
    assert _meta(db)[keylatch.FINGERPRINT] == keylatch.fingerprint("probe_ing_old")


def test_it_writes_only_when_the_state_changes_and_never_creates_the_db(tmp_path, monkeypatch):
    _fresh(monkeypatch)
    writes = []
    real = keylatch._write
    monkeypatch.setattr(keylatch, "_write", lambda *a, **k: writes.append(k) or real(*a, **k))
    db = _db(tmp_path)
    for _ in range(5):
        keylatch.note("claude_code", "probe_ing_a", 401, GATEWAY_401, db=db)
    assert len(writes) == 1
    missing = tmp_path / "none" / "state.db"
    keylatch.note("codex", "probe_ing_b", 401, GATEWAY_401, db=missing)
    assert not missing.exists()


def test_install_wraps_the_tap_wire_once_and_capture_still_gets_its_answer(tmp_path, monkeypatch):
    _fresh(monkeypatch)
    db = _db(tmp_path)
    monkeypatch.setattr(keylatch, "state_db", lambda source: db)

    class Wire:
        def __init__(self):
            self.token, self.source = "probe_ing_t", "claude_code"

        def _request(self, path, body=None):
            return 401, GATEWAY_401

    tap = types.SimpleNamespace(session_journal=types.SimpleNamespace(Wire=Wire))
    assert keylatch.install(tap) and keylatch.install(tap)  # the second is a no-op
    assert Wire()._request("/ingest") == (401, GATEWAY_401)
    assert _meta(db)[keylatch.FINGERPRINT] == keylatch.fingerprint("probe_ing_t")


def test_the_cli_reads_the_stamp_as_halted(tmp_path, monkeypatch):
    """What `probe session status` / doctor read (`capture_state._halted`)."""
    from probe.cli import capture_state

    _fresh(monkeypatch)
    db = _db(tmp_path)
    monkeypatch.setattr(capture_state, "tap_plugin_dir", lambda source: tmp_path)
    monkeypatch.setattr(capture_state, "resolved_capture_credential", lambda source: ("probe_ing_k", "test"))
    assert capture_state._halted("claude_code") is False
    keylatch.note("claude_code", "probe_ing_k", 401, GATEWAY_401, db=db)
    assert capture_state._halted("claude_code") is True
