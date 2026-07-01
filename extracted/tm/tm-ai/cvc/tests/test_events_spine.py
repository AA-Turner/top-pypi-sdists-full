"""
Tests for the CVC Event Spine foundation.

These tests exercise:
  - ULID generation (uniqueness + monotonicity + format)
  - capture() writes correct schema
  - atomic append survives rotation
  - query() filters (workspace, channel, kind, since, search, limit)
  - stats_by_kind / stats_by_channel / stats_by_day
  - purge_older_than
  - capture_block context manager records duration + status
  - concurrency (multiple threads writing)
  - best-effort behavior (capture never raises even with bad inputs)
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import time
from pathlib import Path
from unittest import mock

import pytest


# ---------------------------------------------------------------------------
# Fixture: isolated spine root for each test
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def isolated_spine(tmp_path, monkeypatch):
    """Point CVC_EVENTS_ROOT at a tmp dir for the duration of the test."""
    monkeypatch.setenv("CVC_EVENTS_ROOT", str(tmp_path))
    # Force re-init
    import cvc.events.spine as spine
    # Invalidate the cached lock fd
    if spine._file_lock_fd is not None:
        spine._release_file_lock()
    yield tmp_path


# ---------------------------------------------------------------------------
# ULID
# ---------------------------------------------------------------------------


def test_ulid_format():
    from cvc.events.spine import _generate_ulid
    u = _generate_ulid()
    assert len(u) == 26
    assert u.isupper()
    # No I, L, O, U in Crockford base32
    for bad in "ILOU":
        assert bad not in u, f"bad char {bad} in ULID {u}"


def test_ulid_unique_across_many_calls():
    from cvc.events.spine import _generate_ulid
    ids = {_generate_ulid() for _ in range(2000)}
    assert len(ids) == 2000, "duplicate ULID"


def test_ulid_time_ordered_within_same_ms():
    """Same-ms calls must be strictly monotonic in lexicographic order."""
    from cvc.events.spine import _generate_ulid_at
    # Pin time to a single ms — calls in sequence must yield strictly increasing ULIDs
    now_ms = int(time.time() * 1000)
    a = _generate_ulid_at(now_ms)
    b = _generate_ulid_at(now_ms)
    c = _generate_ulid_at(now_ms)
    assert a < b < c, f"not strictly monotonic: {a} {b} {c}"


def test_ulid_advances_with_time():
    from cvc.events.spine import _generate_ulid_at
    t1 = int(time.time() * 1000) - 1000
    t2 = int(time.time() * 1000)
    a = _generate_ulid_at(t1)
    b = _generate_ulid_at(t2)
    assert a < b


# ---------------------------------------------------------------------------
# Capture basic
# ---------------------------------------------------------------------------


def test_capture_minimal():
    from cvc.events.spine import capture, query
    eid = capture(kind="system.startup", summary="test")
    assert eid is not None
    assert len(eid) == 26
    events = query(kind="system.startup")
    assert len(events) == 1
    evt = events[0]
    assert evt["kind"] == "system.startup"
    assert evt["summary"] == "test"
    assert evt["id"] == eid


def test_capture_full_schema():
    from pathlib import Path as _P
    from cvc.events.spine import capture, query
    expected_ws = str(_P("/tmp/myproj").resolve())
    eid = capture(
        kind="chat.user_message",
        workspace="/tmp/myproj",
        channel="telegram",
        actor="Jai",
        summary="asked about timeline",
        data={"text_preview": "hi"},
        provider="minimax",
        model="MiniMax-M3",
        branch="main",
        session_id="sess-1",
        tokens_in=10,
        tokens_out=20,
        duration_ms=500,
        status="ok",
        tags=["soul"],
        channel_detail="chat:12345",
    )
    assert eid
    evt = query()[0]
    assert evt["kind"] == "chat.user_message"
    assert evt["workspace"] == expected_ws
    assert evt["workspace_name"] == "myproj"
    assert evt["channel"] == "telegram"
    assert evt["channel_detail"] == "chat:12345"
    assert evt["actor"] == "Jai"
    assert evt["summary"] == "asked about timeline"
    assert evt["data"] == {"text_preview": "hi"}
    assert evt["provider"] == "minimax"
    assert evt["model"] == "MiniMax-M3"
    assert evt["branch"] == "main"
    assert evt["session_id"] == "sess-1"
    assert evt["tokens_in"] == 10
    assert evt["tokens_out"] == 20
    assert evt["duration_ms"] == 500
    assert evt["status"] == "ok"
    assert evt["tags"] == ["soul"]
    assert "ts" in evt and isinstance(evt["ts"], float)
    assert "ts_iso" in evt and evt["ts_iso"].endswith("Z")
    assert "ts_mono_ms" in evt


def test_capture_unknown_kind_does_not_raise():
    """Unknown kinds are warned but stored — forward compat."""
    from cvc.events.spine import capture, query
    eid = capture(kind="future.event_type", summary="future")
    assert eid is not None
    assert query(kind="future.event_type")[0]["kind"] == "future.event_type"


def test_capture_unknown_channel_does_not_raise():
    from cvc.events.spine import capture, query
    eid = capture(kind="system.warning", channel="future-channel", summary="x")
    assert eid
    assert query(channel="future-channel")[0]["channel"] == "future-channel"


def test_capture_never_raises_even_on_broken_path():
    """capture must be best-effort — never raises to caller."""
    from cvc.events.spine import capture
    with mock.patch("cvc.events.spine._atomic_append", side_effect=OSError("disk full")):
        eid = capture(kind="system.error", summary="fail")
    assert eid is None


def test_capture_summary_truncated_to_200():
    from cvc.events.spine import capture, query
    long = "x" * 500
    capture(kind="system.warning", summary=long)
    evt = query()[0]
    assert len(evt["summary"]) == 200
    assert evt["summary"].endswith("...")


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------


def test_query_workspace_filter():
    from pathlib import Path as _P
    from cvc.events.spine import capture, query
    ws_a = str(_P("/proj/a").resolve())
    ws_b = str(_P("/proj/b").resolve())
    capture(kind="terminal.command", workspace="/proj/a")
    capture(kind="terminal.command", workspace="/proj/b")
    capture(kind="terminal.command", workspace=None)

    a = query(workspace="/proj/a")
    assert len(a) == 1
    assert a[0]["workspace"] == ws_a

    # None workspace — returns everything
    n = query(workspace=None)
    assert len(n) == 3


def test_query_channel_filter():
    from cvc.events.spine import capture, query
    capture(kind="chat.user_message", channel="web")
    capture(kind="chat.user_message", channel="telegram")
    capture(kind="chat.user_message", channel="slack")

    assert len(query(channel="web")) == 1
    assert len(query(channel=["web", "slack"])) == 2


def test_query_kind_filter():
    from cvc.events.spine import capture, query
    capture(kind="chat.user_message")
    capture(kind="chat.assistant_message")
    capture(kind="terminal.command")

    assert len(query(kind="chat.user_message")) == 1
    assert len(query(kind=["chat.user_message", "chat.assistant_message"])) == 2


def test_query_since_filter():
    from cvc.events.spine import capture, query
    capture(kind="system.startup")
    cutoff = time.time()
    time.sleep(0.05)
    capture(kind="system.warning")

    after = query(since=cutoff)
    assert len(after) == 1
    assert after[0]["kind"] == "system.warning"


def test_query_search_filter():
    from cvc.events.spine import capture, query
    capture(kind="system.warning", summary="disk space low")
    capture(kind="system.error", summary="connection refused")
    capture(kind="system.warning", summary="memory pressure")

    assert len(query(search="disk")) == 1
    assert len(query(search="CONNECTION")) == 1  # case-insensitive


def test_query_limit_enforced():
    from cvc.events.spine import capture, query, ABSOLUTE_QUERY_LIMIT
    for _ in range(50):
        capture(kind="system.warning", summary="spam")
    assert len(query(limit=10)) == 10
    assert len(query(limit=ABSOLUTE_QUERY_LIMIT)) == 50


def test_query_reverse():
    from cvc.events.spine import capture, query
    for i in range(5):
        capture(kind="system.warning", summary=f"event-{i}")
        time.sleep(0.01)

    desc = query(reverse=True)
    asc = query(reverse=False)
    assert desc[0]["summary"] == "event-4"
    assert asc[0]["summary"] == "event-0"


def test_query_tags_filter():
    from cvc.events.spine import capture, query
    capture(kind="soul.write", tags=["audit"])
    capture(kind="soul.write", tags=["compliance"])
    capture(kind="soul.write", tags=["audit", "compliance"])

    assert len(query(tags=["audit"])) == 2
    assert len(query(tags=["compliance"])) == 2
    assert len(query(tags=["nonexistent"])) == 0


def test_query_session_id():
    from cvc.events.spine import capture, query
    capture(kind="chat.user_message", session_id="sess-a")
    capture(kind="chat.user_message", session_id="sess-b")
    assert len(query(session_id="sess-a")) == 1


def test_query_actor():
    from cvc.events.spine import capture, query
    capture(kind="chat.user_message", actor="Jai")
    capture(kind="chat.user_message", actor="Anjali")
    assert len(query(actor="Jai")) == 1


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


def test_stats_by_kind():
    from cvc.events.spine import capture, stats_by_kind
    capture(kind="chat.user_message")
    capture(kind="chat.user_message")
    capture(kind="terminal.command")
    s = stats_by_kind()
    assert s["chat.user_message"] == 2
    assert s["terminal.command"] == 1


def test_stats_by_channel():
    from cvc.events.spine import capture, stats_by_channel
    capture(kind="chat.user_message", channel="web")
    capture(kind="chat.user_message", channel="telegram")
    capture(kind="system.warning", channel="system")
    s = stats_by_channel()
    assert s["web"] == 1
    assert s["telegram"] == 1
    assert s["system"] == 1


def test_stats_by_day_returns_continuous_days():
    from cvc.events.spine import capture, stats_by_day
    capture(kind="system.warning", summary="today")
    result = stats_by_day(days=7)
    assert len(result) == 7
    assert all("day" in r and "count" in r for r in result)


def test_count():
    from cvc.events.spine import capture, count
    for _ in range(10):
        capture(kind="system.warning")
    assert count() == 10
    assert count(kind="chat.user_message") == 0
    assert count(kind="system.warning") == 10


# ---------------------------------------------------------------------------
# capture_block context manager
# ---------------------------------------------------------------------------


def test_capture_block_records_duration():
    from cvc.events.spine import capture_block, query
    with capture_block(
        kind="terminal.command",
        workspace="/proj",
        channel="terminal",
        summary="git status",
    ) as ctx:
        time.sleep(0.05)
        ctx["data"] = {"exit_code": 0}

    evt = query()[0]
    assert evt["kind"] == "terminal.command"
    assert evt["summary"] == "git status"
    assert evt["duration_ms"] >= 50
    assert evt["status"] == "ok"
    assert evt["data"] == {"exit_code": 0}


def test_capture_block_records_error_status():
    from cvc.events.spine import capture_block, query
    with pytest.raises(RuntimeError):
        with capture_block(
            kind="terminal.command",
            summary="fail",
        ):
            raise RuntimeError("boom")

    evt = query()[0]
    assert evt["status"] == "err"
    assert "RuntimeError" in (evt["error"] or "")
    assert "boom" in (evt["error"] or "")


# ---------------------------------------------------------------------------
# Persistence / file layout
# ---------------------------------------------------------------------------


def test_writes_to_dated_jsonl_file(tmp_path):
    from cvc.events.spine import capture, query, _spine_root
    capture(kind="system.startup", summary="x")
    today = time.strftime("%Y-%m-%d")
    file = _spine_root() / f"{today}.jsonl"
    assert file.exists()
    # Should be valid JSONL
    lines = file.read_text().strip().split("\n")
    assert len(lines) == 1
    evt = json.loads(lines[0])
    assert evt["kind"] == "system.startup"


def test_one_event_per_line_atomically(tmp_path):
    from cvc.events.spine import capture
    for i in range(100):
        capture(kind="system.warning", summary=f"e-{i}")
    files = list(tmp_path.glob("*.jsonl"))
    assert len(files) == 1
    lines = files[0].read_text().strip().split("\n")
    assert len(lines) == 100
    # Every line is valid JSON
    for line in lines:
        json.loads(line)


# ---------------------------------------------------------------------------
# Concurrency
# ---------------------------------------------------------------------------


def test_concurrent_capture_no_corruption(tmp_path):
    from cvc.events.spine import capture, query, _spine_root
    n_threads = 8
    n_per_thread = 50

    def worker(tid: int):
        for i in range(n_per_thread):
            capture(
                kind="system.warning",
                summary=f"t{tid}-e{i}",
            )

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    total = query(limit=10000)
    assert len(total) == n_threads * n_per_thread


# ---------------------------------------------------------------------------
# Rotation + retention
# ---------------------------------------------------------------------------


def test_rotate_moves_current_to_dated_file(tmp_path):
    from cvc.events.spine import capture, rotate_if_needed, CURRENT_FILENAME
    # Write to current.jsonl
    (tmp_path / CURRENT_FILENAME).write_text('{"legacy": true}\n')
    rotated = rotate_if_needed()
    assert len(rotated) == 1
    assert not (tmp_path / CURRENT_FILENAME).exists()
    # The rotated file should exist with the legacy content
    assert any('"legacy": true' in p.read_text() for p in rotated)


def test_purge_older_than(tmp_path):
    from cvc.events.spine import capture
    import time as _time
    # Make a dated file from "long ago"
    old_file = tmp_path / "2020-01-01.jsonl"
    old_file.write_text('{"id":"01OLD","kind":"x","ts":1.0,"summary":"old"}\n')
    # Make it actually old
    old_time = _time.time() - 365 * 86400 * 2  # 2 years ago
    os.utime(old_file, (old_time, old_time))

    # And capture one fresh event
    capture(kind="system.warning", summary="fresh")

    from cvc.events.spine import purge_older_than
    deleted = purge_older_than(days=365)
    assert deleted == 1
    assert not old_file.exists()
    # Fresh event should still be there
    files = list(tmp_path.glob("2026-*.jsonl"))
    assert any(f.exists() for f in files)


# ---------------------------------------------------------------------------
# spine_info diagnostic
# ---------------------------------------------------------------------------


def test_spine_info():
    from cvc.events.spine import capture, spine_info
    capture(kind="system.startup")
    info = spine_info()
    assert "root" in info
    assert "files" in info
    assert info["total_events"] >= 1
    assert "system.startup" in info["known_kinds"]
    assert "web" in info["known_channels"]