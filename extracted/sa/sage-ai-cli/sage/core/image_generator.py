"""Image generation — sage's answer to DALL·E / Imagen / Midjourney.

Backend: Vertex AI Imagen (Google's image-gen model). Same "everything
on GCP" pattern as the cloud:* LLM fleet. No third-party AI services.

Typical use:

    gen = ImageGenerator()
    image = gen.generate("a watercolor of a fox in autumn leaves")
    image.save("fox.png")

The CLI exposes this as ``sage image "prompt" [--out path/dir] [--aspect 16:9]``.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

logger = logging.getLogger("sage.image_generator")


# Imagen's supported aspect ratios. We validate up-front so users get a
# clear error rather than a cryptic API rejection.
_VALID_ASPECT_RATIOS: frozenset[str] = frozenset({"1:1", "9:16", "16:9", "3:4", "4:3"})


class ImageGenerationError(RuntimeError):
    """Raised when image generation fails — wraps the underlying cause.

    Two flavours of failure callers care about:
      - API/network errors: original exception in `__cause__`
      - Safety filter blocks: message contains "safety"
    """


# ── Data types ────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class GeneratedImage:
    """An image produced from a prompt. Carries enough metadata that the
    caller can save it or hand it to a UI without further inspection."""
    prompt: str
    image_bytes: bytes
    mime_type: str

    def save(self, path: str | Path) -> Path:
        """Save the image. If ``path`` is a directory, derive a filename
        from the prompt (slugified). If it's a file, save directly.

        Returns the actual file path written.
        """
        p = Path(path)
        if p.is_dir():
            slug = _slugify(self.prompt)[:60] or "image"
            ext = _extension_for(self.mime_type)
            p = p / f"{slug}{ext}"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(self.image_bytes)
        return p


# ── Imagen client protocol (for testability) ─────────────────────────────────


class _ImagenClient(Protocol):
    """Minimal slice of the Imagen client. Tests inject a fake; production
    builds a real Vertex AI client from GOOGLE_APPLICATION_CREDENTIALS."""
    def generate_images(self, prompt: str, **kwargs: Any) -> Any: ...


# ── Main API ──────────────────────────────────────────────────────────────────


class ImageGenerator:
    """Generates images via Vertex AI Imagen.

    Construct once; call ``generate()`` per request. Stateless beyond the
    client reference — safe to share across threads.
    """

    def __init__(self, api_client: _ImagenClient | None = None):
        self._client = api_client

    def generate(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "1:1",
        # Reserved for future: variants, negative_prompt, safety_level...
    ) -> GeneratedImage:
        """Generate an image from ``prompt``.

        Raises:
          ValueError: empty prompt or invalid aspect ratio
          ImageGenerationError: API failure or safety filter block
        """
        if not prompt or not prompt.strip():
            raise ValueError("Cannot generate image with empty prompt.")
        if aspect_ratio not in _VALID_ASPECT_RATIOS:
            raise ValueError(
                f"Invalid aspect ratio {aspect_ratio!r}. "
                f"Must be one of: {sorted(_VALID_ASPECT_RATIOS)}"
            )
        if self._client is None:
            raise ImageGenerationError(
                "No Imagen client configured. Pass `api_client` to ImageGenerator "
                "or set GOOGLE_APPLICATION_CREDENTIALS in the environment."
            )

        try:
            response = self._client.generate_images(
                prompt=prompt.strip(),
                aspect_ratio=aspect_ratio,
            )
        except Exception as exc:
            raise ImageGenerationError(
                f"Vertex AI Imagen call failed: {exc}"
            ) from exc

        return self._parse_response(prompt, response)

    @staticmethod
    def _parse_response(prompt: str, response: Any) -> GeneratedImage:
        """Extract the first image from an Imagen response.

        Imagen returns a list of generated images plus a safety-filter
        flag. If everything was filtered out the list is empty and we
        raise — caller surfaces "your prompt was blocked" UI.
        """
        # Safety filter: Imagen blocks the request and returns empty images.
        if getattr(response, "was_safety_filtered", False):
            raise ImageGenerationError(
                "Imagen safety filter blocked this prompt. "
                "Try a more specific or less sensitive description."
            )

        images = getattr(response, "images", None) or []
        if not images:
            raise ImageGenerationError(
                "Imagen returned no images (and no safety flag). "
                "This usually means the response shape changed — check logs."
            )

        first = images[0]
        return GeneratedImage(
            prompt=prompt,
            image_bytes=getattr(first, "image_bytes", b""),
            mime_type=getattr(first, "mime_type", "image/png"),
        )


# ── Filename slugify helper ───────────────────────────────────────────────────


def _slugify(text: str) -> str:
    """Lowercase + ascii-letters/digits-only + hyphens. Safe for filenames
    on every common OS. Empty string allowed (caller falls back to default)."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def _extension_for(mime_type: str) -> str:
    """Map MIME to file extension. Imagen produces image/png by default."""
    return {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/webp": ".webp",
    }.get(mime_type, ".png")


__all__ = [
    "GeneratedImage",
    "ImageGenerator",
    "ImageGenerationError",
]
