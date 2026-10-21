"""The session's own name goes to the server beside its transcript (tap 0.9.20).

Claude Code names a session after its first exchange (the terminal tab) and
re-appends that name to the transcript every few turns: an `ai-title` line, plus
a `custom-title` line once the researcher has used /rename. Neither line ships
as an event, and the name is not a batch key either: the engine's receipts door
digests every batch key. After a batch lands, the journal sends the name to the
gateway's title door (`Wire.title`), again only when it changes (0339); with no
batch left to send, the tap retries a refused one now and then (`idle`).
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from probe.tap_core import sanitize
from probe.tap_core import session_journal as sj
from probe.tap_core.session_journal import Journal
from test_backfill_transcripts_upload import FakeWire


class TitledWire(FakeWire):
    def __init__(self) -> None:
        super().__init__()
        self.titles: list[tuple[str, str]] = []
        self.title_status = 200

    def title(self, session_id: str, title: str) -> tuple[int, dict]:
        self.titles.append((session_id, title))
        return self.title_status, {"status": "ok"}


def _user(sid: str, text: str) -> dict:
    return {
        "type": "user",
        "sessionId": sid,
        "cwd": "/synthetic",
        "message": {"role": "user", "content": text},
    }


def _ai_title(sid: str, title: str) -> dict:
    return {"type": "ai-title", "aiTitle": title, "sessionId": sid}


def _custom_title(sid: str, title: str) -> dict:
    return {"type": "custom-title", "customTitle": title, "sessionId": sid}


@pytest.fixture
def capture(tmp_path, monkeypatch):
    """A live journal over one growing transcript: `append` adds lines, `deliver`
    stages and sends the next batch as the tap does."""
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    wire = TitledWire()
    sid = str(uuid4())
    path = tmp_path / f"{sid}.jsonl"
    path.write_bytes(b"")
    journal = Journal(wire.base_url, "synthetic", "claude_code")

    def append(*lines: dict) -> None:
        with path.open("a") as handle:
            for line in lines:
                handle.write(json.dumps(line) + "\n")

    def deliver() -> dict:
        journal.ensure(sid, path, wire.receipts(sid), historical=False)
        encoded = journal.stage(sid, cwd="/synthetic")
        assert encoded is not None
        assert journal.deliver(sid, wire)
        return json.loads(encoded)

    deliver.journal = journal
    try:
        yield sid, wire, append, deliver
    finally:
        journal.close()


def test_the_title_goes_beside_the_batch_once_and_again_on_change(capture) -> None:
    sid, wire, append, deliver = capture
    append(_user(sid, "first prompt"))
    deliver()
    assert wire.titles == [], "no title line read yet"

    append(_ai_title(sid, "Research-os live run titles"), _user(sid, "second prompt"))
    batch = deliver()
    assert wire.titles == [(sid, "Research-os live run titles")]
    # Neither the line nor the name is in the batch the engine digests.
    assert "title" not in batch
    assert all(event["raw"].get("type") != "ai-title" for event in batch["events"])

    # Claude Code re-appends the same title every few turns: nothing new to send.
    append(_ai_title(sid, "Research-os live run titles"), _user(sid, "third prompt"))
    deliver()
    assert len(wire.titles) == 1

    append(_ai_title(sid, "Research-os session naming"), _user(sid, "fourth prompt"))
    deliver()
    assert wire.titles[-1] == (sid, "Research-os session naming")


def test_a_rename_outranks_the_generated_title_across_batches(capture) -> None:
    """Claude Code re-appends `custom-title` then `ai-title`; a batch boundary
    can fall between them, so the rename is remembered, not re-read."""
    sid, wire, append, deliver = capture
    append(_user(sid, "prompt"), _custom_title(sid, "Session naming"))
    deliver()
    append(_ai_title(sid, "Research-os daemon session naming"), _user(sid, "more"))
    deliver()
    assert wire.titles == [(sid, "Session naming")]


def test_a_refused_title_is_sent_again_and_never_holds_the_batch(capture) -> None:
    sid, wire, append, deliver = capture
    wire.title_status = 503
    append(_ai_title(sid, "Research-os live run titles"), _user(sid, "prompt"))
    deliver()
    assert wire.calls, "the batch went regardless"
    wire.title_status = 200
    append(_user(sid, "next prompt"))
    deliver()
    assert wire.titles == [(sid, "Research-os live run titles")] * 2


def test_a_title_refused_after_the_last_batch_is_retried_while_idle(capture, monkeypatch) -> None:
    """No later batch will carry it, so the tap's idle pass does -- at most every
    TITLE_RETRY_SECONDS, so a server without the door is not asked each tick."""
    sid, wire, append, deliver = capture
    wire.title_status = 404
    append(_ai_title(sid, "Research-os live run titles"), _user(sid, "last prompt"))
    deliver()
    journal = deliver.journal
    now = [1_000_000.0]
    monkeypatch.setattr(sj.time, "time", lambda: now[0])
    journal.update(sid, title_tried_at=now[0])
    journal.send_title(sid, wire, idle=True)
    assert len(wire.titles) == 1, "too soon after the refusal"
    wire.title_status = 200
    now[0] += sj.TITLE_RETRY_SECONDS
    journal.send_title(sid, wire, idle=True)
    assert len(wire.titles) == 2
    journal.send_title(sid, wire, idle=True)
    assert len(wire.titles) == 2, "taken: nothing more to send"


def test_a_credential_in_a_title_is_redacted_before_it_leaves(capture) -> None:
    sid, wire, append, deliver = capture
    key = "AKIA" + "IOSFODNN7EXAMPL3"
    append(_custom_title(sid, f"rotate {key}"), _user(sid, "prompt"))
    deliver()
    ((_, sent),) = wire.titles
    assert key not in sent and sent.startswith("rotate <redacted:")


def test_a_credential_across_the_length_cap_is_redacted_whole(capture) -> None:
    """Cut first and the redactor sees half a token it no longer recognises."""
    sid, wire, append, deliver = capture
    token = "ghp_" + "q7Lm2Xv9Rk4Tz8Np3Wd6Hs1Jc5Fb0Ga7Ye2U"  # the real shape: 36 after the prefix
    title = "x" * 170 + " rotate " + token
    append(_custom_title(sid, title), _user(sid, "prompt"))
    deliver()
    ((_, sent),) = wire.titles
    assert len(sent) <= sanitize.TITLE_MAX_LEN
    assert "q7Lm2Xv9" not in sent


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Research-os live run titles", "Research-os live run titles"),
        ("[DONE] ✳ Research-os live run titles", "Research-os live run titles"),
        ("✳ Research-os\n live\trun titles ", "Research-os live run titles"),
        ("⠂ Kimi harness", "Kimi harness"),
        ("[DONE]", None),
        ("   ", None),
        (42, None),
        ("x" * 5000, "x" * sanitize.TITLE_READ_MAX_LEN),
    ],
)
def test_a_title_is_one_clean_line(raw, expected) -> None:
    named = sanitize.session_title({"type": "ai-title", "aiTitle": raw})
    assert (named and named[0]) == expected or (named is None and expected is None)


def test_only_title_lines_name_a_session() -> None:
    assert sanitize.session_title({"type": "ai-title", "aiTitle": "A"}) == ("A", False)
    assert sanitize.session_title({"type": "custom-title", "customTitle": "B"}) == ("B", True)
    for line in (
        {"type": "user", "aiTitle": "not a title line"},
        {"type": "ai-title"},
        {"type": ["ai-title"], "aiTitle": "A"},
        ["ai-title"],
        None,
    ):
        assert sanitize.session_title(line) is None
