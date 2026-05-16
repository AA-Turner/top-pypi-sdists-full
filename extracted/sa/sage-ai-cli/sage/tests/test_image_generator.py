"""Tests for ImageGenerator — sage's answer to DALL·E / Imagen / Midjourney.

Backend: Vertex AI Imagen (Google's image-gen model on GCP). Matches the
"everything on GCP" architecture used by the cloud:* model fleet.

TDD: tests describe the contract; implementation must satisfy all of these.
"""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from sage.core.image_generator import (
    GeneratedImage,
    ImageGenerator,
    ImageGenerationError,
)


# ── GeneratedImage data shape ─────────────────────────────────────────────────


class TestGeneratedImage:
    def test_image_carries_bytes_and_prompt(self):
        img = GeneratedImage(prompt="a red apple", image_bytes=b"\x89PNG\r\n", mime_type="image/png")
        assert img.prompt == "a red apple"
        assert img.image_bytes.startswith(b"\x89PNG")
        assert img.mime_type == "image/png"

    def test_image_saves_to_disk(self, tmp_path):
        img = GeneratedImage(
            prompt="cat", image_bytes=b"\x89PNG\r\nfake-png-data", mime_type="image/png",
        )
        out = tmp_path / "cat.png"
        path = img.save(out)
        assert path == out
        assert out.exists()
        assert out.read_bytes() == b"\x89PNG\r\nfake-png-data"

    def test_save_defaults_to_prompt_based_filename(self, tmp_path):
        """When the user passes a directory (not a file), we generate a
        filename from the prompt for a friendly UX."""
        img = GeneratedImage(prompt="a happy DOG!!!", image_bytes=b"PNG", mime_type="image/png")
        path = img.save(tmp_path)
        assert path.parent == tmp_path
        # Filename should be safe: lowercased, slugified, .png extension
        assert path.suffix == ".png"
        assert "happy" in path.name.lower()
        assert "dog" in path.name.lower()
        # No special characters made it through
        assert not any(c in path.name for c in "!@#$%^&*")


# ── ImageGenerator main API ──────────────────────────────────────────────────


class TestImageGenerator:
    def test_generate_returns_image_with_bytes(self):
        client = _FakeImagenClient(
            response=_fake_imagen_response(b"\x89PNG\r\nbytes", mime="image/png"),
        )
        gen = ImageGenerator(api_client=client)
        result = gen.generate("a sunset over the ocean")
        assert isinstance(result, GeneratedImage)
        assert result.prompt == "a sunset over the ocean"
        assert result.image_bytes.startswith(b"\x89PNG")
        assert result.mime_type == "image/png"

    def test_generate_accepts_aspect_ratio(self):
        """Imagen supports 1:1, 9:16, 16:9, 3:4, 4:3. We pass through."""
        client = _FakeImagenClient(response=_fake_imagen_response(b"PNG"))
        gen = ImageGenerator(api_client=client)
        gen.generate("anything", aspect_ratio="16:9")
        # Verify the client got the aspect ratio in its kwargs
        assert client.last_call_kwargs.get("aspect_ratio") == "16:9"

    def test_generate_rejects_invalid_aspect_ratio(self):
        gen = ImageGenerator(api_client=_FakeImagenClient(response=None))
        with pytest.raises(ValueError, match="aspect"):
            gen.generate("x", aspect_ratio="42:7")

    def test_generate_empty_prompt_raises(self):
        gen = ImageGenerator(api_client=_FakeImagenClient(response=None))
        with pytest.raises(ValueError, match="empty"):
            gen.generate("")

    def test_generate_api_failure_raises_typed_error(self):
        client = _FakeImagenClient(raises=ConnectionError("Vertex AI down"))
        gen = ImageGenerator(api_client=client)
        with pytest.raises(ImageGenerationError) as exc_info:
            gen.generate("x")
        # Original error chained for debugging
        assert isinstance(exc_info.value.__cause__, ConnectionError)

    def test_generate_handles_safety_blocks(self):
        """Imagen blocks unsafe prompts. We surface this as a typed error
        with a clear message — not a generic 500."""
        client = _FakeImagenClient(response=_fake_imagen_safety_block())
        gen = ImageGenerator(api_client=client)
        with pytest.raises(ImageGenerationError, match="safety"):
            gen.generate("inappropriate content")

    def test_generate_returns_only_first_image_by_default(self):
        """Imagen can return multiple variants. Default is 1; we surface it."""
        # Construct the mock with explicit was_safety_filtered=False; otherwise
        # MagicMock auto-creates a truthy attr and our safety-check trips.
        multi_response = MagicMock(
            images=[
                MagicMock(image_bytes=b"img1", mime_type="image/png"),
                MagicMock(image_bytes=b"img2", mime_type="image/png"),
            ],
            was_safety_filtered=False,
        )
        client = _FakeImagenClient(response=multi_response)
        gen = ImageGenerator(api_client=client)
        result = gen.generate("apple")
        assert result.image_bytes == b"img1"


# ── Test fakes ────────────────────────────────────────────────────────────────


class _FakeImagenClient:
    def __init__(self, response=None, raises=None):
        self._response = response
        self._raises = raises
        self.last_call_kwargs: dict = {}

    def generate_images(self, prompt: str, **kwargs):
        self.last_call_kwargs = kwargs
        if self._raises:
            raise self._raises
        return self._response


def _fake_imagen_response(image_bytes: bytes, mime: str = "image/png"):
    return MagicMock(
        images=[MagicMock(image_bytes=image_bytes, mime_type=mime)],
        was_safety_filtered=False,
    )


def _fake_imagen_safety_block():
    return MagicMock(images=[], was_safety_filtered=True)
