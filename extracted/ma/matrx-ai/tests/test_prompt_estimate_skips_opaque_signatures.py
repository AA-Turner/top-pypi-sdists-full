"""A generated image's Google thought signature is never counted as prompt text.

W4 2026-11-04 (live): Chief of Staff on Nano Banana 2.1 replied with an image whose block kept a 1.7 MB
``metadata.thought_signature``. The prompt pre-check measured it as text, so every next turn of that chat was
"an estimated 612,346 tokens" for a 65,536 window and refused before the provider.
"""

from __future__ import annotations

from matrx_ai.config.context_preflight import _block_chars
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.unified_content import TextContent

SIGNATURE = "A" * 1_700_000


def test_a_generated_images_nested_thought_signature_counts_nothing() -> None:
    image = ImageContent(
        url="https://server.app.matrxserver.com/files/efcb4882-cbd8-4673-9e96-36896657fe1c/download?inline=1",
        file_id="efcb4882-cbd8-4673-9e96-36896657fe1c",
        mime_type="image/png",
        metadata={"thought_signature": SIGNATURE, "model": "gemini-nano-banana-2.1"},
    )
    assert SIGNATURE in str(image.to_storage_dict())  # the stored block really carries it
    assert _block_chars(image) < 5_000


def test_a_text_parts_google_thought_signature_counts_nothing() -> None:
    text = TextContent(text="Hi there.", metadata={"google_thought_signature": SIGNATURE})
    assert _block_chars(text) < 5_000


def test_a_text_parts_binary_signature_counts_nothing_in_its_stored_form() -> None:
    """The real shape: bytes, stored base64 under ``stored_google_thought_signature__b64``."""
    text = TextContent(text="Hi there.", metadata={"google_thought_signature": b"A" * 1_700_000})
    assert _block_chars(text) < 5_000


def test_the_words_still_count() -> None:
    assert _block_chars(TextContent(text="x" * 40_000)) >= 40_000


def test_a_tool_argument_named_signature_still_counts() -> None:
    """Only metadata is opaque: an email tool's ``signature`` argument is words the model reads."""

    class _Call:
        def to_storage_dict(self) -> dict:
            return {"type": "tool_call", "arguments": {"to": "a@b.c", "signature": "s" * 40_000}}

    assert _block_chars(_Call()) >= 40_000
