"""Transcript-line decoders survive deeply nested JSON (ISS-01 follow-up).

Transcript files are client-written, so a line is untrusted input. Each
decoder here used to catch only ``json.JSONDecodeError``; a 200 KB
nested-array line (well under the 1 MiB line cap) raised ``RecursionError``
out of the streaming loop, so one bad line killed the tail for the whole
session instead of being rejected on its own.
"""

from __future__ import annotations

import json
from pathlib import Path

from runlayer_cli.hook import transcript_stream
from tests.hostile_inputs import DEEP_NESTING


def _assistant_line(text: str) -> str:
    return json.dumps(
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": text}],
            },
        }
    )


def test_transcript_line_events_rejects_deep_nesting():
    assert (
        transcript_stream.transcript_line_events(DEEP_NESTING, fallback_session_id="s1")
        == []
    )


def test_transcript_line_is_terminal_rejects_deep_nesting():
    assert transcript_stream.transcript_line_is_terminal(DEEP_NESTING) is False


def test_buffer_is_complete_json_line_rejects_deep_nesting():
    assert transcript_stream._buffer_is_complete_json_line(DEEP_NESTING) is False


def test_stream_drops_poisoned_line_and_keeps_later_records(tmp_path: Path):
    transcript_path = tmp_path / "transcript.jsonl"
    transcript_path.write_text(
        "\n".join(
            [
                _assistant_line("first"),
                DEEP_NESTING,
                _assistant_line("second"),
                json.dumps({"type": "result"}),
            ]
        )
        + "\n"
    )
    delivered: list[tuple[str, dict]] = []

    transcript_stream.run_transcript_stream(
        client_name="claude_code",
        payload={"session_id": "s1", "transcript_path": str(transcript_path)},
        post_event=lambda _client_name, event_name, payload: delivered.append(
            (event_name, payload)
        ),
        max_seconds=1,
        idle_seconds=0.02,
        poll_seconds=0.01,
    )

    assert [payload["message"]["content"] for _, payload in delivered] == [
        "first",
        "second",
    ]
