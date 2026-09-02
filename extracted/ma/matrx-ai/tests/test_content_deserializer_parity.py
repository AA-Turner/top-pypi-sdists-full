"""THE guard for the lossy-round-trip class of bug.

A stored ``cx_message.content`` block has exactly ONE meaning. It is rebuilt on
two hot paths — ``reconstruct_content`` (the DB rebuild) and
``UnifiedMessage.parse_content`` (dicts from the wire, config hydration,
``MessageList.__post_init__``, ``from_dict``). For years those were two
INDEPENDENT implementations of the same shape, and they drifted. Every drift
was a production outage:

* 2026-07-16 — ``citations`` erased on every reparse of a stored message.
* 2026-07-18 — ``call_id`` erased → ``tool_use.id=""`` → Anthropic 400
  ("String should match pattern") on EVERY later turn of the conversation,
  plus the paired tool_result dropped as an orphan.
* 2026-07-18 — Gemini's ``google_thought_signature`` (a ``<key>__b64`` metadata
  entry) left undecoded → ``to_google()`` emitted a functionCall part with no
  ``thoughtSignature`` → Gemini 3 400 on replay.

The mechanism was always identical: ``parse_content`` rebuilt the dataclass via
``_filter_kwargs``, which keeps only keys whose NAME matches a dataclass field.
Any storage key spelled differently (``call_id`` → ``id``) or needing decoding
(``__b64`` → bytes) vanished SILENTLY — no exception, no log, just missing data
that a provider rejects several turns later.

``parse_content`` now delegates the canonical types to ``reconstruct_content``.
These tests pin the two properties that keep it that way:

1. **PARITY** — both paths produce a semantically identical object.
2. **IDEMPOTENCE** — storing a rebuilt object reproduces the same storage dict,
   so a row never degrades by being read and written repeatedly.

Adding a content class or a storage key? Add a sample below. If parity fails,
the fix is to make ``reconstruct_content`` handle it — never to special-case
``parse_content`` again.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import (
    TextContent,
    ThinkingContent,
    reconstruct_content,
)

# (label, object) — one entry per content class × per storage key that needs
# translation (aliased name, base64 bytes, nested metadata).
SAMPLES: list[tuple[str, Any]] = [
    ("text_plain", TextContent(text="hello", id="t1")),
    (
        "text_with_citations",
        TextContent(
            text="cited",
            id="t2",
            metadata={
                "citations": [
                    {
                        "kind": "document_char",
                        "provider": "anthropic",
                        "cited_text": "x",
                        "source_index": 0,
                        "source_start": 0,
                        "source_end": 1,
                    }
                ]
            },
        ),
    ),
    ("text_with_metadata", TextContent(text="m", metadata={"custom_key": "keep_me"})),
    # The 2026-07-18 incident: call_id is the tool-pairing join key.
    ("tool_call", ToolCallContent(id="toolu_ABC", name="my_tool", arguments={"a": 1})),
    (
        "tool_call_openai_item_id",
        ToolCallContent(
            id="call_1", name="t", arguments={}, metadata={"openai_item_id": "fc_1"}
        ),
    ),
    # Gemini 3 hard-requires thoughtSignature on a replayed functionCall part.
    (
        "tool_call_google_signature_bytes",
        ToolCallContent(
            id="toolu_G",
            name="t",
            arguments={"x": 1},
            metadata={"google_thought_signature": b"\x00\x01SIGBYTES"},
        ),
    ),
    (
        "tool_result",
        ToolResultContent(
            tool_use_id="toolu_ABC",
            call_id="toolu_ABC",
            name="my_tool",
            content="output",
            output_chars=6,
        ),
    ),
    (
        "tool_result_error",
        ToolResultContent(
            tool_use_id="toolu_E", call_id="toolu_E", name="t", content="boom", is_error=True
        ),
    ),
    ("thinking_str_signature", ThinkingContent(text="th", provider="anthropic", signature="opaque")),
    (
        "thinking_bytes_signature",
        ThinkingContent(text="th", provider="google", signature=b"\x00\x01SIG"),
    ),
]


def _storage(obj: Any) -> dict[str, Any]:
    return obj.to_storage_dict()


@pytest.mark.parametrize("label,obj", SAMPLES, ids=[s[0] for s in SAMPLES])
def test_both_rebuild_paths_agree(label: str, obj: Any) -> None:
    """reconstruct_content and parse_content must produce the SAME object.

    A divergence here is the exact shape of all three historical incidents.
    """
    stored = _storage(obj)

    via_reconstruct = reconstruct_content(stored)
    via_parse = UnifiedMessage.parse_content([stored])[0]

    assert type(via_reconstruct) is type(via_parse), (
        f"{label}: the two rebuild paths produced DIFFERENT TYPES "
        f"({type(via_reconstruct).__name__} vs {type(via_parse).__name__})."
    )
    assert _storage(via_reconstruct) == _storage(via_parse), (
        f"{label}: the two rebuild paths DISAGREE.\n"
        f"  reconstruct_content -> {_storage(via_reconstruct)}\n"
        f"  parse_content       -> {_storage(via_parse)}\n"
        f"Fix reconstruct_content (the ONE deserializer) — never special-case "
        f"parse_content."
    )


@pytest.mark.parametrize("label,obj", SAMPLES, ids=[s[0] for s in SAMPLES])
def test_storage_round_trip_is_idempotent(label: str, obj: Any) -> None:
    """store → rebuild → store must be stable on BOTH paths.

    Without this, a row degrades a little on every read/write cycle — the
    silent-data-loss shape that only surfaces as a provider 400 much later.
    """
    stored = _storage(obj)

    for path_name, rebuilt in (
        ("reconstruct_content", reconstruct_content(stored)),
        ("parse_content", UnifiedMessage.parse_content([stored])[0]),
    ):
        again = _storage(rebuilt)
        assert again == stored, (
            f"{label} via {path_name}: storage round-trip LOST OR CHANGED data.\n"
            f"  before: {stored}\n"
            f"  after : {again}"
        )


@pytest.mark.parametrize("label,obj", SAMPLES, ids=[s[0] for s in SAMPLES])
def test_in_memory_binary_fields_survive_as_bytes(label: str, obj: Any) -> None:
    """``<key>__b64`` metadata must decode back to bytes on BOTH paths.

    A base64 STRING where bytes are expected is invisible to a ``in metadata``
    check, so the provider payload silently omits the value (Gemini's
    ``thoughtSignature`` → 400 "Function call is missing a thought_signature").
    """
    original_meta = getattr(obj, "metadata", None) or {}
    binary_keys = {k for k, v in original_meta.items() if isinstance(v, bytes)}
    original_sig = getattr(obj, "signature", None)
    if not binary_keys and not isinstance(original_sig, bytes):
        pytest.skip("no binary fields on this sample")

    stored = _storage(obj)
    for path_name, rebuilt in (
        ("reconstruct_content", reconstruct_content(stored)),
        ("parse_content", UnifiedMessage.parse_content([stored])[0]),
    ):
        for key in binary_keys:
            got = (getattr(rebuilt, "metadata", None) or {}).get(key)
            assert isinstance(got, bytes), (
                f"{label} via {path_name}: metadata[{key!r}] came back as "
                f"{type(got).__name__}, not bytes. A base64 string here is "
                f"silently dropped at the provider boundary."
            )
            assert got == original_meta[key]
        if isinstance(original_sig, bytes):
            got_sig = getattr(rebuilt, "signature", None)
            assert isinstance(got_sig, bytes), (
                f"{label} via {path_name}: signature came back as "
                f"{type(got_sig).__name__}, not bytes."
            )
            assert got_sig == original_sig


@pytest.mark.parametrize("label,obj", SAMPLES, ids=[s[0] for s in SAMPLES])
def test_to_dict_is_lossless_for_binary_material(label: str, obj: Any) -> None:
    """``to_dict()`` is a SERIALIZER, not a display form — it must round-trip.

    2026-08-16: ``to_dict()`` replaced binary provider-continuity material with
    the human-readable ``<bytes length=N>`` placeholder that ``__repr__`` uses.
    ``chat.request_snapshot.unified_payload`` — the ONLY sanctioned re-entry
    point for wire replay — is built from ``AIMatrixRequest.to_dict()``, so
    EVERY recorded Gemini call carrying a ``thoughtSignature`` was unreplayable:
    the rebuilt request died inside the Google SDK with 151 validation errors
    before it left the process, and the replay's own fidelity check said
    ``faithful: true`` because the placeholder is structurally a string in the
    right place. A whole provider's history was unusable as evidence.
    """
    original_meta = getattr(obj, "metadata", None) or {}
    binary_keys = {k for k, v in original_meta.items() if isinstance(v, bytes)}
    original_sig = getattr(obj, "signature", None)
    if not binary_keys and not isinstance(original_sig, bytes):
        pytest.skip("no binary fields on this sample")

    wire = obj.to_dict()
    # It must survive the jsonb write the snapshot performs.
    json.dumps(wire)

    rebuilt = UnifiedMessage.parse_content([wire])[0]
    for key in binary_keys:
        got = (getattr(rebuilt, "metadata", None) or {}).get(key)
        assert isinstance(got, bytes) and got == original_meta[key], (
            f"{label}: to_dict() → parse_content LOST metadata[{key!r}] "
            f"(got {type(got).__name__}). A request rebuilt from a snapshot "
            f"cannot be re-issued without it."
        )
    if isinstance(original_sig, bytes):
        got_sig = getattr(rebuilt, "signature", None)
        assert isinstance(got_sig, bytes) and got_sig == original_sig, (
            f"{label}: to_dict() → parse_content LOST the signature bytes."
        )


@pytest.mark.parametrize("label,obj", SAMPLES, ids=[s[0] for s in SAMPLES])
def test_no_serializer_ever_emits_a_display_placeholder(label: str, obj: Any) -> None:
    """The redacting placeholders belong to ``__repr__`` and nowhere else."""
    for serializer in ("to_dict", "to_storage_dict"):
        method = getattr(obj, serializer, None)
        if method is None:
            continue
        emitted = json.dumps(method())
        for placeholder in ("<bytes length=", "<str length="):
            assert placeholder not in emitted, (
                f"{label}: {serializer}() emitted the DISPLAY placeholder "
                f"{placeholder!r}. That value cannot be rebuilt from — use "
                f"encode_binary_metadata (base64 under `<key>__b64`) instead."
            )


def test_tool_call_join_key_survives_every_spelling() -> None:
    """The tool-pairing join key must survive whichever key the writer used.

    Storage writes ``call_id``; some clients/legacy rows write ``id``. Losing it
    yields ``tool_use.id=""`` → Anthropic 400 and an orphaned tool_result.
    """
    for block in (
        {"type": "tool_call", "name": "t", "call_id": "toolu_X", "arguments": {}},
        {"type": "tool_call", "name": "t", "id": "toolu_X", "arguments": {}},
        {"type": "function_call", "name": "t", "call_id": "toolu_X", "arguments": {}},
    ):
        for path_name, rebuilt in (
            ("reconstruct_content", reconstruct_content(block)),
            ("parse_content", UnifiedMessage.parse_content([block])[0]),
        ):
            assert rebuilt.id == "toolu_X", (
                f"{path_name} lost the join key from block {block!r} "
                f"(got {rebuilt.id!r})"
            )


def test_deserializer_never_raises_on_a_cosmetic_bad_field() -> None:
    """A malformed cosmetic field must not take the whole request down.

    This is the ONE deserializer for every rebuild path — an exception here
    fails a real, paid user request over a display counter.
    """
    block = {
        "type": "tool_result",
        "tool_use_id": "toolu_Z",
        "name": "t",
        "content": "ok",
        "output_chars": "not-a-number",
    }
    for rebuilt in (
        reconstruct_content(block),
        UnifiedMessage.parse_content([block])[0],
    ):
        assert rebuilt.tool_use_id == "toolu_Z"
        assert rebuilt.output_chars == 0
