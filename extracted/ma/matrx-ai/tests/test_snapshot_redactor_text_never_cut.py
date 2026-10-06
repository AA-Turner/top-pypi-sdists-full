"""Forcing-function: snapshot redaction never cuts TEXT; it replaces only inline
file data, by a marker that carries the file reference (owner ruling 2026-10-05).

Live, 3,863 of 26,410 snapshots in 30 days had a cut request: the redactor
treated ANY string over 64 KiB as binary, so a ~125 KB plain-text prompt at
``$.contents[0].parts[0].text`` was stored as 256 chars.
"""

from __future__ import annotations

import base64

from matrx_ai.providers.snapshot_redactors import (
    DEFAULT_SNAPSHOT_REDACTORS,
    MARKER_OPEN,
    apply_redactors,
)

PROMPT = ("Assign each keyword to a topic. Return JSON: {\"topic\": \"x\"}.\n" + "keyword electronics recycling near me, ") * 3000
BLOB = base64.b64encode(b"\x89PNG\r\n\x1a\n" + bytes(range(256)) * 800).decode("ascii")


def _run(payload):
    return apply_redactors(payload, DEFAULT_SNAPSHOT_REDACTORS)


def test_prompt_fixture_is_over_200kb() -> None:
    assert len(PROMPT) > 200_000


def test_anthropic_text_prompt_is_byte_identical() -> None:
    p = {"messages": [{"role": "user", "content": [{"type": "text", "text": PROMPT}]}], "system": PROMPT}
    assert _run(p) == p


def test_openai_text_prompt_is_byte_identical() -> None:
    p = {"input": [{"role": "user", "content": [{"type": "input_text", "text": PROMPT}]}], "instructions": PROMPT}
    assert _run(p) == p


def test_google_text_prompt_is_byte_identical() -> None:
    p = {"contents": [{"role": "user", "parts": [{"text": PROMPT}]}]}
    assert _run(p) == p


def test_json_code_and_markdown_in_a_string_are_kept() -> None:
    big_json = '{"k": [' + ",".join(["1"] * 120_000) + "]}"
    assert _run({"a": big_json}) == {"a": big_json}
    # even a prompt with no whitespace at a non-blob key survives
    dense = "abcdefgh" * 30_000
    assert _run({"contents": [{"parts": [{"text": dense}]}]}) == {"contents": [{"parts": [{"text": dense}]}]}


def test_anthropic_base64_image_is_replaced_without_reference() -> None:
    p = {"messages": [{"content": [{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": BLOB}}]}]}
    out = _run(p)["messages"][0]["content"][0]["source"]["data"]
    assert MARKER_OPEN in out and len(out) < 2000
    assert 'reference="none_sha256_only"' in out and 'mime="image/png"' in out and "original_sha256" in out


def test_openai_data_uri_is_replaced() -> None:
    uri = "data:image/png;base64," + BLOB
    out = _run({"input": [{"content": [{"type": "input_image", "image_url": uri}]}]})["input"][0]["content"][0]["image_url"]
    assert MARKER_OPEN in out and 'mime="image/png"' in out


def test_google_inline_data_is_replaced() -> None:
    out = _run({"contents": [{"parts": [{"inline_data": {"mime_type": "application/pdf", "data": BLOB}}]}]})
    assert MARKER_OPEN in out["contents"][0]["parts"][0]["inline_data"]["data"]


def test_unified_media_block_marker_carries_file_id() -> None:
    block = {"type": "image", "base64_data": BLOB, "file_id": "11111111-2222-3333-4444-555555555555", "mime_type": "image/png"}
    out = _run({"messages": [{"content": [block]}]})["messages"][0]["content"][0]
    assert MARKER_OPEN in out["base64_data"]
    assert 'ref_file_id="11111111-2222-3333-4444-555555555555"' in out["base64_data"]
    assert out["file_id"] == block["file_id"]


def test_redaction_is_idempotent() -> None:
    once = _run({"data": BLOB})
    assert _run(once) == once
