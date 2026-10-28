"""`check_identity` reaches `validate_identity`'s verdict while reading far less.

Session discovery (the desktop app's "Finding saved history" and its review)
checks every transcript on the machine. `validate_identity` parsed the whole
last 2 MB of each Claude transcript for a proof discovery never reads: 88% of
a 6.1 s discovery on a box with 628 sessions. These pin that the cheap verdict
is the same verdict, on the shapes where reading less could differ, and that a
malformed record never crashes either one (a crash in discovery blanks the
whole picker).
"""

from __future__ import annotations

import json
import threading
import types
from pathlib import Path
from uuid import uuid4

import pytest

from probe.cli import backfill_transcripts as bt
from probe.tap_core import session_identity as si
from probe.tap_core.session_journal import ReconciliationRequired

PAD = "x" * 4000


def _claude(sid: str, **extra) -> bytes:
    record = {"type": "assistant", "sessionId": sid, "cwd": "/work", "message": {"content": "hi"}}
    return (json.dumps({**record, **extra}) + "\n").encode()


def _meta(sid: str) -> bytes:
    return (json.dumps({"type": "session_meta", "payload": {"id": sid, "cwd": "/w"}}) + "\n").encode()


def _pi(sid: str) -> bytes:
    return (json.dumps({"type": "session", "id": sid, "cwd": "/w"}) + "\n").encode()


def _filler(n: int) -> bytes:
    """Non-primary records (progress lines), about 4 KB each."""
    return b"".join(
        (json.dumps({"type": "progress", "sessionId": "ignored", "data": PAD}) + "\n").encode()
        for _ in range(n)
    )


def _write(tmp_path: Path, body: bytes) -> Path:
    path = tmp_path / f"{uuid4()}.jsonl"
    path.write_bytes(body)
    return path


def _verdict(fn, path: Path, source: str, sid: str):
    try:
        fn(path, source, sid)
    except si.IdentityMismatch as exc:
        return ("mismatch", str(exc))
    except ReconciliationRequired as exc:
        return ("unproven", str(exc))
    return ("ok", None)


def _deep(depth: int = 200_000) -> bytes:
    """One line nested past every Python's json recursion limit."""
    return b'{"type":"progress","data":' + b"[" * depth + b"]" * depth + b"}\n"


def _cases():
    sid, ancestor, other = (str(uuid4()) for _ in range(3))
    yield "claude plain", "ok", "claude_code", sid, _claude(sid) * 3
    yield "claude resumed from an ancestor", "ok", "claude_code", sid, _claude(ancestor) * 2 + _claude(sid)
    yield "claude ends on another session", "mismatch", "claude_code", sid, _claude(sid) + _claude(other)
    # The last primary record sits ~80 KB from the end: past the first 64 KB read.
    yield "claude primary past 64 KB", "ok", "claude_code", sid, _claude(sid) + _filler(20)
    # ...and ~2.4 MB from the end: outside the 2 MB window, so neither check sees it.
    yield "claude primary past the window", "unproven", "claude_code", sid, _claude(sid) + _filler(600)
    yield "claude sidechain only", "unproven", "claude_code", sid, _claude(sid, isSidechain=True) * 2
    yield "claude no records", "unproven", "claude_code", sid, b"not json\n{}\n"
    yield "claude empty", "unproven", "claude_code", sid, b""
    yield "claude no trailing newline", "ok", "claude_code", sid, _claude(sid).rstrip(b"\n")
    yield "claude earlier id not a string", "ok", "claude_code", sid, _claude(["a"]) + _claude(sid)
    yield "claude earlier ids of mixed types", "ok", "claude_code", sid, _claude(5) + _claude(ancestor) + _claude(sid)
    yield "claude deep line before the last", "ok", "claude_code", sid, _claude(sid) + _deep() + _claude(sid)
    yield "claude deep line after the last", "ok", "claude_code", sid, _claude(sid) + _deep()
    yield "codex plain", "ok", "codex", sid, _meta(sid) + b'{"type":"event_msg","payload":{}}\n'
    yield "codex conflicting headers", "mismatch", "codex", sid, _meta(sid) + _meta(other)
    # A header whose type is spelled with a \\u escape still counts as a header.
    escaped = b'{"type":"\\u0073ession_meta","payload":{"id":"' + other.encode() + b'"}}\n'
    yield "codex escaped header", "mismatch", "codex", sid, _meta(sid) + escaped
    # ...and so does one json.loads decodes from UTF-16, with no literal or escaped marker.
    utf16 = (json.dumps({"type": "session_meta", "payload": {"id": other}}) + "\n").encode("utf-16-le")
    yield "codex utf-16 header", "mismatch", "codex", sid, _meta(sid) + utf16
    yield "codex header not an object", "unproven", "codex", sid, b'{"type":"session_meta","payload":"x"}\n'
    yield "codex second header null", "mismatch", "codex", sid, _meta(sid) + b'{"type":"session_meta","payload":null}\n'
    yield "codex deep line", "ok", "codex", sid, _meta(sid) + _deep().replace(b"progress", b"session_meta")
    yield "codex header past the window", "unproven", "codex", sid, _filler(600) + _meta(sid)
    yield "codex no header", "unproven", "codex", sid, b'{"type":"event_msg","payload":{}}\n'
    yield "pi plain", "ok", "pi", sid, _pi(sid) + b'{"type":"message"}\n'
    yield "pi conflicting headers", "mismatch", "pi", sid, _pi(sid) + _pi(other)


def test_the_verdict_matches_validate_identity_on_every_shape(tmp_path):
    for name, expected, source, sid, body in _cases():
        path = _write(tmp_path, body)
        full = _verdict(si.validate_identity, path, source, sid)
        assert full[0] == expected, name
        assert _verdict(si.check_identity, path, source, sid) == full, name


def test_window_edges_agree(tmp_path):
    """Files whose size straddles VERDICT_FIRST_BYTES and SAMPLE_BYTES."""
    sid = str(uuid4())
    for size in (si.VERDICT_FIRST_BYTES - 1, si.VERDICT_FIRST_BYTES, si.VERDICT_FIRST_BYTES + 1,
                 si.SAMPLE_BYTES - 1, si.SAMPLE_BYTES, si.SAMPLE_BYTES + 1):
        for primary_first in (True, False):
            record = _claude(sid)
            opening = b'{"type":"progress","data":"'
            line = opening + b"x" * (size - len(record) - len(opening) - 3) + b'"}\n'
            body = (record + line) if primary_first else (line + record)
            assert len(body) == size
            path = _write(tmp_path, body)
            full = _verdict(si.validate_identity, path, "claude_code", sid)
            assert _verdict(si.check_identity, path, "claude_code", sid) == full, (size, primary_first)


def test_the_verdict_parses_a_handful_of_lines_not_the_window(tmp_path, monkeypatch):
    """The speed is the point: a 3 MB transcript ending on a primary record."""
    sid = str(uuid4())
    path = _write(tmp_path, _claude(sid) + _filler(750) + _claude(sid))
    calls = []
    real = json.loads
    monkeypatch.setattr(si, "json", types.SimpleNamespace(loads=lambda raw: calls.append(1) or real(raw)))
    si.check_identity(path, "claude_code", sid)
    assert len(calls) <= 2


def test_the_proof_still_reads_its_whole_window(tmp_path):
    """An ancestor ~400 KB back: past the verdict's first read, inside the proof's window."""
    sid, ancestor = str(uuid4()), str(uuid4())
    path = _write(tmp_path, _claude(ancestor) + _filler(100) + _claude(sid))
    assert si.validate_identity(path, "claude_code", sid)["observed_lineage"] == [ancestor]


def test_validate_identity_still_returns_the_full_proof(tmp_path):
    sid, ancestor = str(uuid4()), str(uuid4())
    path = _write(tmp_path, _claude(ancestor) + _claude(sid) + _filler(3))
    proof = si.validate_identity(path, "claude_code", sid)
    assert proof["native_session_id"] == sid
    assert proof["observed_lineage"] == [ancestor]
    assert proof["source_cwd"] == "/work"
    assert si.check_identity(path, "claude_code", sid) is None


def test_unknown_source_and_missing_file_raise_as_before(tmp_path):
    sid = str(uuid4())
    with pytest.raises(OSError):
        si.check_identity(tmp_path / "gone.jsonl", "claude_code", sid)
    path = _write(tmp_path, _claude(sid))
    with pytest.raises(ReconciliationRequired):
        si.check_identity(path, "no-such-source", sid)
    with pytest.raises(ReconciliationRequired):
        si.check_identity(path, "claude_code", "not-a-uuid")


def test_a_failed_hash_surfaces_without_waiting_for_the_others(tmp_path, monkeypatch):
    """A review whose first file vanished reports it while another read is stuck
    (a network volume), instead of after every queued file is hashed."""
    release = threading.Event()

    def prefix_hash(path, size):
        if path.name == "gone.jsonl":
            raise FileNotFoundError(path)
        release.wait()
        return "digest"

    monkeypatch.setattr(bt, "prefix_hash", prefix_hash)
    monkeypatch.setattr(bt, "_background_identity", lambda client: {})
    rows = [bt.Transcript(path=tmp_path / name, session_id=str(uuid4()), agent="claude_code",
                          cwd=None, size=1, mtime=0.0) for name in ("gone.jsonl", "stuck.jsonl", "queued.jsonl")]
    raised = []

    def review():
        try:
            bt._background_payload(bt.Census(candidates=rows), client=None, posters={}, devices={},
                                   budget_bytes=None, unpaired=[])
        except FileNotFoundError as exc:
            raised.append(exc)

    worker = threading.Thread(target=review, daemon=True)
    worker.start()
    worker.join(timeout=30)  # gstack-timing-ok: the failure is a hang until release, not a slow pass
    stuck = worker.is_alive()
    release.set()
    worker.join(timeout=30)
    assert not stuck and raised
