"""Tests for vision input — let users send images to multimodal cloud models.

The cloud:llava-next-7b model (Cloud Run GPU) accepts image+text input
via OpenAI-compatible multimodal content arrays. This module turns a
local file path or URL into the right payload shape.

TDD: tests describe how a local PNG/JPEG/URL gets turned into the
OpenAI vision-API message content list. The actual model call uses
sage's existing CloudRuntime forwarding.
"""

from __future__ import annotations

import base64
from pathlib import Path

import pytest

from sage.core.vision_input import (
    VisionAttachment,
    build_vision_message,
    encode_image_for_vision,
)


# ── encode_image_for_vision ──────────────────────────────────────────────────


class TestEncodeImage:
    @pytest.fixture
    def png_file(self, tmp_path):
        # Minimal valid PNG (1x1 transparent pixel)
        p = tmp_path / "tiny.png"
        p.write_bytes(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
            b"\x00\x00\x00\rIDATx\x9cc\x00\x01\x00\x00\x05\x00"
            b"\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        return p

    def test_encodes_png_as_data_url(self, png_file):
        attachment = encode_image_for_vision(png_file)
        assert isinstance(attachment, VisionAttachment)
        assert attachment.mime_type == "image/png"
        # Data URL embeds the base64 image inline — compatible with the
        # OpenAI vision API spec used by LLaVA-NeXT.
        assert attachment.data_url.startswith("data:image/png;base64,")
        # Verify the base64 decodes back to the original bytes
        b64 = attachment.data_url.split(",", 1)[1]
        assert base64.b64decode(b64) == png_file.read_bytes()

    def test_encodes_jpeg(self, tmp_path):
        p = tmp_path / "x.jpg"
        # Minimal JPEG header (SOI + APP0 marker)
        p.write_bytes(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00")
        attachment = encode_image_for_vision(p)
        assert attachment.mime_type == "image/jpeg"
        assert attachment.data_url.startswith("data:image/jpeg;base64,")

    def test_rejects_non_image_file(self, tmp_path):
        p = tmp_path / "note.txt"
        p.write_text("just text")
        with pytest.raises(ValueError, match="not an image"):
            encode_image_for_vision(p)

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            encode_image_for_vision(tmp_path / "missing.png")

    def test_oversized_image_rejected(self, tmp_path):
        """LLaVA-NeXT has a context limit; very large images blow the
        token budget. Reject anything over 10 MB up-front."""
        p = tmp_path / "huge.png"
        # Write a valid PNG header followed by lots of zero padding
        p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * (11 * 1024 * 1024))
        with pytest.raises(ValueError, match="too large"):
            encode_image_for_vision(p)


# ── build_vision_message ─────────────────────────────────────────────────────


class TestBuildVisionMessage:
    """The agent loop sends OpenAI-compatible messages. For vision input,
    the user-role message's content becomes a LIST of typed parts:
        [{"type": "text", "text": "..."},
         {"type": "image_url", "image_url": {"url": "data:..."}}]
    """

    @pytest.fixture
    def png_file(self, tmp_path):
        p = tmp_path / "p.png"
        p.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00")
        return p

    def test_message_has_text_and_image_parts(self, png_file):
        msg = build_vision_message(
            prompt="What's in this image?",
            image_paths=[png_file],
        )
        assert msg["role"] == "user"
        content = msg["content"]
        assert isinstance(content, list)
        # Order: text first, then image(s). OpenAI's docs recommend text
        # first for best results.
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "What's in this image?"
        assert content[1]["type"] == "image_url"
        assert content[1]["image_url"]["url"].startswith("data:image/png;base64,")

    def test_supports_multiple_images(self, png_file, tmp_path):
        png2 = tmp_path / "p2.png"
        png2.write_bytes(b"\x89PNG\r\n\x1a\n\x01\x02")
        msg = build_vision_message(
            prompt="Compare these two",
            image_paths=[png_file, png2],
        )
        image_parts = [p for p in msg["content"] if p["type"] == "image_url"]
        assert len(image_parts) == 2

    def test_empty_image_list_falls_back_to_plain_text(self, png_file):
        """No images = regular text message, not a malformed multimodal
        payload with empty parts."""
        msg = build_vision_message(prompt="hi", image_paths=[])
        # Should be the simple string-content shape, not a parts list
        assert isinstance(msg["content"], str)
        assert msg["content"] == "hi"

    def test_empty_prompt_with_image_still_valid(self, png_file):
        """User might attach an image with no text — common 'what is this?'
        gesture. We send the image with an implicit prompt."""
        msg = build_vision_message(prompt="", image_paths=[png_file])
        # The text part should still exist (even if empty) so providers
        # treating empty text as a hint don't reject the message.
        assert msg["content"][0]["type"] == "text"
