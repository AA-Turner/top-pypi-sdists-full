"""THE second, independent layer for the Google wire-replay defect (2026-08-16).

`test_content_deserializer_parity.py` guards the SERIALIZERS. This guards the
END OF THE CHAIN: a recorded Gemini snapshot, rebuilt exactly the way
`aidream/services/hindsight/wire_replay.py` rebuilds it, must produce a payload
the Google SDK ACCEPTS. Either layer alone stops the bug; this one is what
notices the day a new serializer, translator, or SDK version breaks
replayability again — and it costs nothing, because the SDK validates the
parameters model long before any HTTP call.

The failure it pins: every replay of a recorded Gemini call died with
`ValidationError: 151 validation errors for _GenerateContentParameters` before
the request left the process, because `to_dict()` wrote the DISPLAY placeholder
`<bytes length=N>` where the `thoughtSignature` bytes belonged. Anthropic
replays worked, so a whole provider's history was silently unusable as
evidence — and C-16's own fidelity check reported `faithful: true`, since the
placeholder is structurally a string in exactly the right place.

The fixture is a minimized copy of production snapshot
`92702c2f-e252-489d-b1af-32dc5a3a4e09` (six messages, texts trimmed), with the
signature material as a POST-FIX capture writes it: base64 under `<key>__b64`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

FIXTURE = (
    Path(__file__).parent / "fixtures" / "wire_replay" / "gemini_tool_turn_snapshot.json"
)


def _load() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text())


def _rebuild_contents(unified: dict[str, Any]) -> list[dict[str, Any]]:
    """The replay rebuild, verbatim: `AIMatrixRequest.from_dict` on the stored
    `unified_payload`, then the Google message → contents translation."""
    from matrx_ai.orchestrator.requests import AIMatrixRequest

    request = AIMatrixRequest.from_dict(dict(unified))
    contents: list[dict[str, Any]] = []
    for message in request.config.messages:
        content = message.to_google_content()
        if content:
            contents.append(content)
    return contents


def test_recorded_gemini_snapshot_rebuilds_into_an_sdk_valid_payload() -> None:
    from google.genai import types as gtypes

    contents = _rebuild_contents(_load()["unified_payload"])
    assert contents, "the fixture rebuilt to zero contents — an empty Gemini request"

    # The SDK's own parameter model: exactly what `generate_content()` builds
    # and exactly where the 151 errors were raised.
    params = gtypes._GenerateContentParameters(model="gemini-3.1-flash-lite", contents=contents)
    assert params.contents is not None and len(params.contents) == len(contents)


def test_the_thought_signature_survives_the_rebuild_as_real_bytes() -> None:
    """Gemini 3 REJECTS a replayed functionCall part without its signature, so
    "the payload validates" is not enough — the material must be the original
    bytes, not a placeholder and not a base64 string."""
    contents = _rebuild_contents(_load()["unified_payload"])

    signatures = [
        part["thoughtSignature"]
        for content in contents
        for part in content["parts"]
        if "thoughtSignature" in part
    ]
    assert signatures, (
        "the fixture carries signed tool-call turns; none survived the rebuild. "
        "A serializer dropped the provider-continuity metadata."
    )
    for signature in signatures:
        assert isinstance(signature, bytes), (
            f"thoughtSignature came back as {type(signature).__name__}. A str "
            f"here is either the `<bytes length=N>` display placeholder or an "
            f"undecoded base64 blob — the SDK rejects both."
        )


def test_the_display_placeholder_is_rejected_by_the_sdk() -> None:
    """Proves the fixture is a real reproduction, not a tautology: put the old
    placeholder back and the SDK fails exactly as production did."""
    from google.genai import types as gtypes
    from pydantic import ValidationError

    fixture = _load()
    for message in fixture["unified_payload"]["config"]["messages"]:
        for part in message.get("content") or []:
            metadata = part.get("metadata")
            if isinstance(metadata, dict) and "google_thought_signature__b64" in metadata:
                metadata.pop("google_thought_signature__b64")
                metadata["google_thought_signature"] = "<bytes length=411>"

    contents = _rebuild_contents(fixture["unified_payload"])
    with pytest.raises(ValidationError) as excinfo:
        gtypes._GenerateContentParameters(model="gemini-3.1-flash-lite", contents=contents)

    assert any(
        error["type"] == "bytes_invalid_encoding" for error in excinfo.value.errors()
    ), "the reproduction no longer fails the way the production defect did"
