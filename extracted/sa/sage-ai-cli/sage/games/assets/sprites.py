"""Sprite generator — Vertex AI Imagen primary, procedural fallback.

Sage already wires Imagen for `sage image`; we reuse the same auth path
(Google Application Default Credentials + the `love-in-da-house` project).
When Imagen is unavailable (no creds, offline, quota), we fall back to
generating a flat-color PNG so the pipeline keeps moving and the build
still produces an output. That's better than failing the whole game on
one missing sprite.
"""

from __future__ import annotations

import os
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class SpriteResult:
    role: str
    path: Path
    backend: str           # "imagen" | "placeholder"
    width: int
    height: int


class SpriteGenerator:
    """One instance per build. Holds the output dir + a counter for retries."""

    def __init__(self, out_dir: Path, *, style: str = "pixel") -> None:
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.style = style

    def generate(
        self,
        role: str,
        prompt: str,
        *,
        size: tuple[int, int] = (256, 256),
    ) -> SpriteResult:
        path = self.out_dir / f"{role}.png"
        try:
            if _vertex_available():
                _imagen_generate(prompt, size, path, style=self.style)
                return SpriteResult(role, path, "imagen", *size)
        except Exception:  # noqa: BLE001 — fallback below
            pass
        # Placeholder — a single-color PNG so the build still has the file.
        _write_placeholder_png(path, size, _role_color(role))
        return SpriteResult(role, path, "placeholder", *size)


# ─────────────────────────── helpers ───────────────────────────────────


def _vertex_available() -> bool:
    """Cheap probe: do we have a project ID + creds set?"""
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        return True
    if os.environ.get("VERTEX_AI_PROJECT") or os.environ.get("GCP_PROJECT"):
        return True
    return False


def _imagen_generate(
    prompt: str,
    size: tuple[int, int],
    out_path: Path,
    *,
    style: str,
) -> None:
    """Call Vertex AI Imagen and write the first image to `out_path`.

    Imports `google.cloud.aiplatform` lazily so installs without Vertex
    don't pay the import cost.
    """
    from google.cloud import aiplatform_v1beta1 as aip  # type: ignore[import-untyped]

    project = (os.environ.get("VERTEX_AI_PROJECT")
               or os.environ.get("GCP_PROJECT")
               or "love-in-da-house")
    location = os.environ.get("VERTEX_AI_LOCATION", "us-central1")
    client = aip.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"},
    )
    endpoint = (
        f"projects/{project}/locations/{location}/publishers/google/"
        f"models/imagen-3.0-generate-001"
    )
    full_prompt = f"{style} game sprite of {prompt}, transparent background"
    response = client.predict(
        endpoint=endpoint,
        instances=[{"prompt": full_prompt}],
        parameters={
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "outputOptions": {"mimeType": "image/png"},
        },
    )
    if not response.predictions:
        raise RuntimeError("imagen returned no predictions")
    b64 = response.predictions[0].get("bytesBase64Encoded")
    if not b64:
        raise RuntimeError("imagen response missing image bytes")
    import base64
    out_path.write_bytes(base64.b64decode(b64))


# ── Procedural placeholder PNG (no PIL dependency) ─────────────────────


def _role_color(role: str) -> tuple[int, int, int]:
    """Deterministic color per role so placeholder sprites are visually
    distinguishable in a build."""
    h = hash(role) & 0xFFFFFF
    return (h >> 16) & 0xFF, (h >> 8) & 0xFF, h & 0xFF


def _write_placeholder_png(
    path: Path,
    size: tuple[int, int],
    rgb: tuple[int, int, int],
) -> None:
    """Emit a minimal valid PNG of `size` filled with `rgb`. Pure stdlib —
    no PIL or numpy dependency."""
    width, height = size
    r, g, b = rgb
    # PNG = signature + IHDR + IDAT + IEND.
    def _chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    raw = bytearray()
    row = bytes([r, g, b]) * width
    for _ in range(height):
        raw.append(0)  # filter byte: None
        raw.extend(row)
    idat = zlib.compress(bytes(raw), level=9)
    path.write_bytes(sig + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b""))
