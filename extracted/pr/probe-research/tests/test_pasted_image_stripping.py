"""A pasted screenshot must not leave the machine, and must not kill an import.

Codex inlines a paste as `data:image/png;base64,...` on ONE line, so one
screenshot is one event of its full encoded size. Shipping that verbatim was
wrong twice over:

  * the import review screen promises "tool output, file contents and API
    metadata never leave", and an image is file content, so every paste small
    enough to fit a batch was quietly breaking that promise;
  * every paste too big for a batch was FATAL. `Journal.stage` could put it in
    no batch at all, refused, and the session never imported -- on every retry,
    forever. Eight sessions failed that way in one real import.

Measured on one machine's history when this was written: 1,790 codex events
carried an inlined image, 1.47GB of 4.03GB (36.5%), and 354 were individually
over the 1 MiB packing target. After this change, 0 of 526,255 events exceed it.

`pi_sanitize` already answered this exactly this way ("Size, mime and nothing
else"), so these tests pin codex against the standard pi already set.
"""

from __future__ import annotations

import base64
import json

import pytest

from probe.tap_core import codex_sanitize
from probe.tap_core.session_journal import (
    MAX_BODY_BYTES,
    MAX_SOLO_EVENT_BYTES,
    SERVER_BATCH_LIMIT,
)


def _pasted(payload_bytes: int, media: str = "image/png") -> dict:
    """A codex `input_image` line the way a real paste writes one."""
    blob = base64.b64encode(b"\x89PNG" + b"x" * payload_bytes).decode()
    return {
        "type": "response_item",
        "timestamp": "2026-09-13T02:01:36.000Z",
        "payload": {
            "type": "message",
            "role": "user",
            "content": [
                {"type": "input_text", "text": '<image name=[Image #1] path="/tmp/shot.png">'},
                {"type": "input_image", "image_url": f"data:{media};base64,{blob}"},
            ],
        },
    }


def _blocks(event) -> list[dict]:
    event = event[0] if isinstance(event, list) else event
    return event["message"]["content"]


def test_the_pixels_never_leave_the_machine() -> None:
    blocks = _blocks(codex_sanitize.sanitize_event(_pasted(64_000)))
    image = next(b for b in blocks if b["type"] == "image")
    assert "source" not in image, "the data URL must not survive sanitization"
    assert image["mimeType"] == "image/png"
    assert image["bytes"] > 64_000
    assert "base64" not in json.dumps(blocks)
    assert "iVBOR" not in json.dumps(blocks)


def test_the_conversation_still_says_an_image_was_there() -> None:
    """Dropping the bytes must not drop the fact. The text block beside it
    already names the file, and the image block still records type and size."""
    blocks = _blocks(codex_sanitize.sanitize_event(_pasted(1_000)))
    assert [b["type"] for b in blocks] == ["text", "image"]
    assert "[Image #1]" in blocks[0]["text"]
    assert blocks[1]["bytes"] > 1_000


def test_a_remote_reference_is_kept_because_it_is_not_file_content() -> None:
    """An https URL is a pointer, costs nothing, and is worth following later."""
    event = {
        "type": "response_item",
        "payload": {
            "type": "message", "role": "user",
            "content": [{"type": "input_image", "image_url": "https://example.com/a.png"}],
        },
    }
    image = _blocks(codex_sanitize.sanitize_event(event))[0]
    assert image["source"] == {"type": "url", "url": "https://example.com/a.png"}


def test_an_absurdly_long_value_claiming_to_be_a_url_is_still_dropped() -> None:
    """`data:` is not the only way to smuggle a megabyte into a URL field."""
    event = {
        "type": "response_item",
        "payload": {
            "type": "message", "role": "user",
            "content": [{"type": "input_image", "image_url": "https://x/" + "a" * 50_000}],
        },
    }
    image = _blocks(codex_sanitize.sanitize_event(event))[0]
    assert "source" not in image
    assert image["bytes"] > 50_000


@pytest.mark.parametrize("media", ["image/png", "image/jpeg", "image/svg+xml"])
def test_the_media_type_survives(media: str) -> None:
    blocks = _blocks(codex_sanitize.sanitize_event(_pasted(500, media)))
    assert next(b for b in blocks if b["type"] == "image")["mimeType"] == media


def test_a_malformed_data_url_still_yields_a_bounded_block() -> None:
    """No comma, no media type — it must not raise and must not ship the blob."""
    event = {
        "type": "response_item",
        "payload": {
            "type": "message", "role": "user",
            "content": [{"type": "input_image", "image_url": "data:" + "z" * 30_000}],
        },
    }
    image = _blocks(codex_sanitize.sanitize_event(event))[0]
    assert "source" not in image
    assert len(json.dumps(image)) < 200


def test_a_paste_that_used_to_kill_the_session_now_fits_a_batch() -> None:
    """THE FAILURE THIS EXISTS FOR: a 3 MiB screenshot, the size of the largest
    real one found on disk. Before, its sanitized event exceeded the batch
    budget by itself and no batch could ever carry it."""
    encoded = codex_sanitize.sanitize_event(_pasted(3 * 1024 * 1024))
    items = encoded if isinstance(encoded, list) else [encoded]
    wire = json.dumps([{"line_no": i, "raw": e} for i, e in enumerate(items)],
                      separators=(",", ":")).encode()
    assert len(wire) < MAX_BODY_BYTES, "must now fit the ordinary packing target"
    assert len(wire) < 1_000, "and it should be tiny, not merely under the cap"


def test_the_solo_allowance_matches_what_the_route_accepts() -> None:
    """`app/ingestion/sessions_router.py` caps a batch at 2,000,000 bytes. The
    client's packing target is deliberately smaller, but refusing a LONE event
    on the packing target rejected batches the server would have taken -- and
    did it permanently, since a single event cannot be split."""
    assert SERVER_BATCH_LIMIT == 2_000_000
    assert MAX_BODY_BYTES < MAX_SOLO_EVENT_BYTES < SERVER_BATCH_LIMIT
    assert SERVER_BATCH_LIMIT - MAX_SOLO_EVENT_BYTES >= 8 * 1024, "envelope needs real slack"


# --- the journal side: one event that cannot be packed beside anything -------


def _one_event_transcript(tmp_path, size: int):
    """A claude_code transcript whose single event is `size` bytes of text."""
    from probe.cli import backfill_transcripts as bt

    sid = "11111111-2222-3333-4444-555555555555"
    path = tmp_path / f"{sid}.jsonl"
    event = {
        "type": "user",
        "sessionId": sid,
        "cwd": "/synthetic",
        "message": {"role": "user", "content": "x" * size},
    }
    path.write_bytes(json.dumps(event).encode() + b"\n")
    stat = path.stat()
    return bt.Transcript(path, sid, "claude_code", "/synthetic", stat.st_size, stat.st_mtime)


def _journal(tmp_path, transcript, monkeypatch):
    from test_backfill_transcripts_upload import FakeWire
    from probe.tap_core.session_identity import validate_identity
    from probe.tap_core.session_journal import Journal

    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    wire = FakeWire()
    journal = Journal(wire.base_url, "synthetic", transcript.agent)
    journal.ensure(
        transcript.session_id, transcript.path, wire.receipts(transcript.session_id),
        historical=True,
        provenance=validate_identity(transcript.path, transcript.agent, transcript.session_id),
    )
    return journal


def test_a_lone_event_over_the_packing_target_now_ships(tmp_path, monkeypatch) -> None:
    """It could be put in no batch, so it was refused forever. The server would
    have taken it: the route's cap is 2,000,000, not the packing target."""
    transcript = _one_event_transcript(tmp_path, int(MAX_BODY_BYTES * 1.4))
    journal = _journal(tmp_path, transcript, monkeypatch)
    try:
        body = journal.stage(transcript.session_id, cwd="/synthetic", historical_only=True)
        assert body is not None
        assert MAX_BODY_BYTES < len(body) <= SERVER_BATCH_LIMIT
        assert len(json.loads(body)["events"]) == 1
    finally:
        journal.close()


def test_an_event_beyond_what_the_route_accepts_is_still_refused(tmp_path, monkeypatch) -> None:
    """The boundary is the SERVER's, and it is honest: sending this would be a
    413, so it is retained locally rather than thrown at the gateway."""
    from probe.tap_core.session_journal import DeliveryPending

    transcript = _one_event_transcript(tmp_path, SERVER_BATCH_LIMIT + 1024)
    journal = _journal(tmp_path, transcript, monkeypatch)
    try:
        with pytest.raises(DeliveryPending, match="gateway batch budget"):
            journal.stage(transcript.session_id, cwd="/synthetic", historical_only=True)
    finally:
        journal.close()


def test_packed_batches_still_respect_the_smaller_target(tmp_path, monkeypatch) -> None:
    """The solo allowance must not become the packing size — batching to the
    route's ceiling leaves no room for the envelope and earns a 413."""
    from probe.cli import backfill_transcripts as bt

    sid = "66666666-7777-8888-9999-000000000000"
    path = tmp_path / f"{sid}.jsonl"
    line = json.dumps({
        "type": "user", "sessionId": sid, "cwd": "/synthetic",
        "message": {"role": "user", "content": "y" * 40_000},
    }).encode() + b"\n"
    path.write_bytes(line * 80)          # ~3.2MB across 80 packable events
    stat = path.stat()
    transcript = bt.Transcript(path, sid, "claude_code", "/synthetic", stat.st_size, stat.st_mtime)
    journal = _journal(tmp_path, transcript, monkeypatch)
    try:
        body = journal.stage(transcript.session_id, cwd="/synthetic", historical_only=True)
        assert body is not None
        assert len(body) <= MAX_BODY_BYTES, "a packed batch must stay at the target"
        assert len(json.loads(body)["events"]) > 1
    finally:
        journal.close()
