"""THE LABEL THE ESTIMATE COUNTS IS THE LABEL THE WIRE CARRIES — TURN 1 AND REPLAY (CGU-10 AND-IMG18, finding N6).

Live AND-V IMG17: a replayed GPT turn came in 13-15 tokens UNDER its bill (Gemini 1). The picture was exact
(``responses/input_tokens``: 3,687 for the 2048x1536 variant); the label was not. The server then labeled a replayed
picture ``name="<id>.png"`` (60 tokens) while the estimator counted the newer ``name_unavailable`` label (49): two
label builders out of step. Both now go through ``_media_identity_label``; this guard renders the REAL provider
wire for each provider and checks the estimate covers the label it carries, for the turn-1 shape (inline bytes,
no stored name) and the replay shape (a storage-made ``<id>.png`` name on the part).
"""

from __future__ import annotations

import pytest

from matrx_ai.config.context_preflight import media_label_tokens
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent
from matrx_ai.memory.token_counter import count_tokens_tiktoken

FID = "ea1e35af-4521-475d-bf7e-dde5bcf71b4a"
SHAPES = {
    "turn_1": {},
    "replay_storage_name": {"file_name": f"{FID}.png"},
    "replay_person_name": {"file_name": "whiteboard photo.png"},
}


def _labels_in(value: object) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for v in value.values():
            found += _labels_in(v)
    elif isinstance(value, list):
        for v in value:
            found += _labels_in(v)
    elif isinstance(value, str) and value.startswith("<attachment "):
        found.append(value)
    return found


@pytest.mark.parametrize("shape", sorted(SHAPES))
def test_the_openai_estimate_covers_the_label_on_the_wire(shape: str) -> None:
    picture = ImageContent(base64_data="iVBORw0KGgo=", mime_type="image/png", file_id=FID, metadata=dict(SHAPES[shape]))
    message = UnifiedMessage(role="user", content=[TextContent(text="Reply with the single word ok."), picture])
    (label,) = _labels_in(message.to_openai_items())
    on_wire = count_tokens_tiktoken(label, "o200k_base")
    est = media_label_tokens(picture, "user", model="gpt-5.4-nano", wire_format="openai_chat")
    assert est >= on_wire, (shape, label, est, on_wire)


@pytest.mark.parametrize("shape", sorted(SHAPES))
@pytest.mark.parametrize(("model", "wire", "render"), [
    ("claude-sonnet-5-5", "anthropic_chat", "to_anthropic_blocks"),
    ("gemini-3.8-flash", "google_chat", "to_google_content"),
])
def test_every_provider_counts_the_label_it_sends(shape: str, model: str, wire: str, render: str) -> None:
    from matrx_ai.config.message_config import _media_identity_label

    picture = ImageContent(base64_data="iVBORw0KGgo=", mime_type="image/png", file_id=FID, metadata=dict(SHAPES[shape]))
    message = UnifiedMessage(role="user", content=[TextContent(text="Reply with the single word ok."), picture])
    (label,) = _labels_in(getattr(message, render)())
    assert label == _media_identity_label(picture, "user")  # the one builder the estimate reads
    assert media_label_tokens(picture, "user", model=model, wire_format=wire) > 0
