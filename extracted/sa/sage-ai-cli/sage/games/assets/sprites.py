"""Sprite generator — Vertex AI Imagen primary, no templated fallback.

Sage refuses to ship placeholder art. When Imagen credentials are
unavailable, every sprite generation call raises a clear error pointing
the user at the install path — that's the correct behavior. Silently
writing a flat-color PNG would mask the real problem and let games
"build" with fake assets.

For animated sprites, each state (idle/walk/attack) is a separate
horizontal frame strip. We generate N Imagen frames per state and stitch
them into one PNG so engine adapters can slice the sheet at the frame
width.
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
    backend: str           # always "imagen" — no other backend exists
    width: int
    height: int


@dataclass
class SpriteAnimationResult:
    """One animation state for a role — horizontal frame strip PNG."""

    role: str
    state: str             # "idle" | "walk" | "attack" | ...
    path: Path
    backend: str
    frame_count: int
    frame_size: tuple[int, int]


class SpriteMissingBackendError(RuntimeError):
    """Raised when sprite generation is requested but no real image-gen
    backend is configured. Carries a user-actionable install hint."""

    def __init__(self) -> None:
        super().__init__(
            "Sprite generation requires a real image model. Set up one of:\n"
            "  • Vertex AI Imagen: export GOOGLE_APPLICATION_CREDENTIALS or "
            "VERTEX_AI_PROJECT to a GCP project with the Imagen API enabled.\n"
            "  • Alternative: install local Stable Diffusion via `pip install "
            "diffusers torch` and a model checkpoint (see sage docs).\n"
            "Sage does NOT generate placeholder art — without a real model "
            "your sprites would be flat colors, not game assets."
        )


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
        if not _vertex_available():
            raise SpriteMissingBackendError()
        _imagen_generate(prompt, size, path, style=self.style)
        return SpriteResult(role, path, "imagen", *size)

    def generate_animated(
        self,
        role: str,
        prompt: str,
        state: str,
        *,
        frames: int = 4,
        frame_size: tuple[int, int] = (64, 64),
    ) -> SpriteAnimationResult:
        """Generate a horizontal frame-strip for one animation state.

        We invoke Imagen N times — once per frame — with state-aware
        prompt deltas ("walking, mid-stride", "attacking, sword raised")
        and stitch the results into a single (frames × frame_w, frame_h)
        sheet. Cost: N image-gen calls per state per role; the user pays
        for what they ask for — sage doesn't pretend to animate with a
        color cycle.
        """
        if not _vertex_available():
            raise SpriteMissingBackendError()
        path = self.out_dir / f"{role}_{state}.png"
        # Per-frame prompt suffixes nudge Imagen toward a varied frame
        # sequence. Without this, all frames come back nearly identical.
        suffixes = _state_frame_prompts(state, frames)
        frame_paths: list[Path] = []
        for i, suffix in enumerate(suffixes):
            frame_path = self.out_dir / f"_{role}_{state}_f{i}.png"
            _imagen_generate(
                f"{prompt}, {suffix}", frame_size, frame_path, style=self.style,
            )
            frame_paths.append(frame_path)
        # Stitch horizontally and delete per-frame intermediates.
        _stitch_strip(frame_paths, path, frame_size=frame_size)
        for p in frame_paths:
            try: p.unlink()
            except OSError: pass
        return SpriteAnimationResult(
            role=role, state=state, path=path, backend="imagen",
            frame_count=frames, frame_size=frame_size,
        )


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


def _state_frame_prompts(state: str, frames: int) -> list[str]:
    """Per-frame prompt deltas that push Imagen toward a varied sequence.

    The wording is intentionally cinematic ("mid-stride", "follow-through")
    because Imagen responds well to action descriptions. Generic numeric
    suffixes ("frame 1 of 4") tend to produce static repetition.
    """
    if state == "idle":
        return ["standing still, neutral pose",
                "subtle breath, weight shifted right",
                "head turned slightly",
                "weight shifted left"][:frames]
    if state == "walk":
        return ["mid-stride, right foot forward",
                "passing pose, both feet under center",
                "mid-stride, left foot forward",
                "passing pose, both feet under center"][:frames]
    if state == "attack":
        return ["wind-up, weapon raised",
                "strike, weapon mid-swing",
                "impact, weapon contact frame",
                "follow-through, weapon recovering"][:frames]
    # Unknown state — let Imagen interpolate from the base prompt.
    return [f"{state} pose {i+1}" for i in range(frames)]


def _stitch_strip(
    frame_paths: list[Path],
    out_path: Path,
    *,
    frame_size: tuple[int, int],
) -> None:
    """Concatenate frame PNGs horizontally into one strip PNG.

    Uses pure stdlib (struct + zlib) — no PIL. Each input is loaded into
    a row-major RGB buffer, then frames are interleaved column-by-column
    into the output. Inputs that don't match `frame_size` are decoded at
    whatever size Imagen returned and we still write `frame_size` cells —
    the visual result is slightly stretched / clipped but the sheet
    layout stays correct.
    """
    fw, fh = frame_size
    total_w = fw * len(frame_paths)

    def _chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    # Decode each input PNG into a flat (height × width × 3) RGB buffer.
    decoded: list[tuple[int, int, list[bytes]]] = []
    for p in frame_paths:
        decoded.append(_decode_png_rgb(p))

    out_rows: list[bytes] = []
    for y in range(fh):
        row = bytearray()
        row.append(0)  # PNG filter byte: None
        for (iw, ih, rows) in decoded:
            if y < ih and rows[y]:
                # Resample by truncating or padding to fw pixels.
                src = rows[y]
                if iw >= fw:
                    row.extend(src[: fw * 3])
                else:
                    row.extend(src)
                    row.extend(b"\x00" * ((fw - iw) * 3))
            else:
                row.extend(b"\x00" * (fw * 3))
        out_rows.append(bytes(row))
    raw = b"".join(out_rows)
    idat = zlib.compress(raw, level=6)
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", total_w, fh, 8, 2, 0, 0, 0)
    out_path.write_bytes(sig + _chunk(b"IHDR", ihdr) +
                          _chunk(b"IDAT", idat) + _chunk(b"IEND", b""))


def _decode_png_rgb(path: Path) -> tuple[int, int, list[bytes]]:
    """Best-effort stdlib PNG decoder.

    Returns (width, height, [row_bytes ...]) where each row is `width*3`
    bytes of RGB. Supports the subset Imagen produces (8-bit RGB or RGBA,
    no interlace). Anything else → (0, 0, []) and the stitch logic
    pads with zeros.
    """
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return (0, 0, [])
    pos = 8
    width = height = bit_depth = color_type = 0
    idat = bytearray()
    while pos < len(data):
        if pos + 8 > len(data): break
        length = struct.unpack(">I", data[pos:pos+4])[0]
        kind = data[pos+4:pos+8]
        body = data[pos+8:pos+8+length]
        pos += 8 + length + 4   # +4 for CRC
        if kind == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(
                ">IIBB", body[:10])
        elif kind == b"IDAT":
            idat.extend(body)
        elif kind == b"IEND":
            break
    if width == 0 or bit_depth != 8 or color_type not in (2, 6):
        return (0, 0, [])
    bytes_per_pixel = 3 if color_type == 2 else 4
    stride = width * bytes_per_pixel
    raw = zlib.decompress(bytes(idat))
    rows: list[bytes] = []
    prev_row = b"\x00" * stride
    cursor = 0
    for _ in range(height):
        if cursor >= len(raw): break
        filter_type = raw[cursor]; cursor += 1
        scanline = bytearray(raw[cursor:cursor + stride])
        cursor += stride
        rows.append(_defilter(filter_type, scanline, prev_row, bytes_per_pixel))
        prev_row = bytes(rows[-1])
    # Down-convert RGBA → RGB by dropping alpha (sprite sheets are flat).
    if color_type == 6:
        rgb_rows: list[bytes] = []
        for r in rows:
            out = bytearray()
            for i in range(0, len(r), 4):
                out.extend(r[i:i+3])
            rgb_rows.append(bytes(out))
        return (width, height, rgb_rows)
    return (width, height, rows)


def _defilter(
    filter_type: int, scanline: bytearray, prev_row: bytes, bpp: int,
) -> bytes:
    """Reverse the per-row PNG filter (types 0..4) into raw RGB bytes."""
    out = bytearray(len(scanline))
    for i in range(len(scanline)):
        left = out[i - bpp] if i >= bpp else 0
        up = prev_row[i] if i < len(prev_row) else 0
        up_left = prev_row[i - bpp] if i >= bpp and i - bpp < len(prev_row) else 0
        x = scanline[i]
        if filter_type == 0:    # None
            v = x
        elif filter_type == 1:  # Sub
            v = (x + left) & 0xFF
        elif filter_type == 2:  # Up
            v = (x + up) & 0xFF
        elif filter_type == 3:  # Average
            v = (x + ((left + up) >> 1)) & 0xFF
        elif filter_type == 4:  # Paeth
            p = left + up - up_left
            pa = abs(p - left); pb = abs(p - up); pc = abs(p - up_left)
            pred = left if pa <= pb and pa <= pc else (up if pb <= pc else up_left)
            v = (x + pred) & 0xFF
        else:
            v = x
        out[i] = v
    return bytes(out)
