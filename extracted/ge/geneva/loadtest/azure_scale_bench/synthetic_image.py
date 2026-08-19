# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Real (synthetic) image generator whose ENCODED size hits the Atlas distribution.

Deterministic *structured* procedural images (no per-pixel white noise, no padding):
a smooth gradient background, a light low-frequency texture, a few large geometric
shapes, and thick lines/curves. The structure is what makes the images
pHash/dedupe-realistic — unlike white noise (whose perceptual hash is just an
artifact of where the noise lands after grayscale + downscale + DCT), these hashes
reflect genuine low-frequency content: they are well spread across distinct images
and stable under mild transforms (resize, blur, light JPEG). All geometry is laid
out in normalized coordinates and rendered at the target resolution, so the same
``image_id`` is perceptually the same image at any size.

PNG is written with no compression (``compress_level=0``) so the encoded size is a
predictable function of resolution (``W*H*3`` plus small overhead) independent of
pixel content, letting a short bounded correction loop converge on the target size
bucket. JPEG size is content-dependent (structured content compresses well), so the
same correction loop grows the resolution until the encoded size lands in-bucket.
Deterministic per ``image_id`` via the MMLB ``row_hash`` seed.

Pure module (Pillow + numpy; no Ray/Azure). The ``lt_1kib`` bucket is best-effort:
a valid image container has irreducible header overhead, so a sub-~150-byte target
lands at that floor (still within the <1 KiB bucket).
"""

from __future__ import annotations

import io
import math
from typing import TYPE_CHECKING, NamedTuple

from loadtest.azure_scale_bench import constants, image_distribution

if TYPE_CHECKING:
    import numpy as np
    from PIL import Image

_MIN_SIDE = 1
_MAX_CORRECTION_PASSES = 5
_MIN_GROWTH = 1.05  # JPEG size is sub-linear in side, so force >=5% growth below lo

# Below this side (px) the image is too small for meaningful overlays, so only the
# gradient + texture are rendered (drawing shapes/lines would degenerate or crash).
_MIN_OVERLAY_SIDE = 8
# Coarse texture grid upsampled to the full image for a light low-frequency field.
_TEXTURE_GRID = 6
# Amplitude of that texture (fraction of the 0-255 range); keeps it subtle, never
# per-pixel noise.
_TEXTURE_AMPLITUDE = 0.10


class RenderedImage(NamedTuple):
    """A rendered image and its concrete encoded size + dimensions."""

    image_bytes: bytes
    actual_bytes: int
    width: int
    height: int
    image_format: str


def normalize_format(image_format: str) -> str:
    """Map a user format string to a Pillow format ("png" or "jpeg")."""
    fmt = image_format.lower()
    return "jpeg" if fmt in ("jpg", "jpeg") else "png"


def _side_for_target(target_bytes: int) -> int:
    """Initial square side so an uncompressed PNG ~= target bytes.

    Uncompressed PNG ≈ ``3*s*s + s`` (pixels + per-row filter bytes) + a small
    constant header; invert ``3*s^2 + s = target`` for the first guess and let the
    correction loop absorb the constant overhead.
    """
    t = max(1, target_bytes)
    return max(_MIN_SIDE, round((-1.0 + math.sqrt(1.0 + 12.0 * t)) / 6.0))


def _gradient_background(
    rng: np.random.Generator, width: int, height: int
) -> np.ndarray:
    """A smooth two-color linear gradient across a random direction.

    Returns a ``(height, width, 3)`` ``float32`` array (float32 keeps the large
    intermediates ~2x smaller than float64 for the rare multi-MiB image, with no
    visible difference at 0-255). The direction angle and the two endpoint colors
    are drawn from ``rng``, so distinct seeds get distinct low-frequency structure;
    the gradient is parameterized in normalized coordinates, so the same seed is
    the same image at any resolution. Scalars are cast to ``float32`` explicitly so
    numpy's legacy promotion does not upcast the result back to float64.
    """
    import numpy as np

    angle = float(rng.uniform(0.0, 2.0 * math.pi))
    c0 = rng.integers(0, 256, size=3).astype(np.float32)
    c1 = rng.integers(0, 256, size=3).astype(np.float32)
    xs = np.linspace(0.0, 1.0, width, dtype=np.float32).reshape(1, width)
    ys = np.linspace(0.0, 1.0, height, dtype=np.float32).reshape(height, 1)
    t = xs * np.float32(math.cos(angle)) + ys * np.float32(math.sin(angle))
    span = float(t.max() - t.min()) or 1.0
    t = ((t - t.min()) / np.float32(span))[..., None]  # (H, W, 1) in [0, 1]
    return c0 * (np.float32(1.0) - t) + c1 * t


def _add_texture(
    rng: np.random.Generator, arr: np.ndarray, width: int, height: int
) -> np.ndarray:
    """Add a light low-frequency texture (a small coarse field upsampled smoothly).

    Not per-pixel white noise: a tiny ``_TEXTURE_GRID`` field is bicubically
    upsampled to the full size, so it stays low-frequency and survives downscale.
    """
    import numpy as np
    from PIL import Image

    coarse = rng.integers(
        0, 256, size=(_TEXTURE_GRID, _TEXTURE_GRID, 3), dtype=np.uint8
    )
    tex = np.asarray(
        Image.fromarray(coarse, mode="RGB").resize(
            (width, height), Image.Resampling.BICUBIC
        )
    ).astype(np.float32)
    arr += (tex - np.float32(128.0)) * np.float32(_TEXTURE_AMPLITUDE)
    return arr


def _draw_overlays(
    rng: np.random.Generator, img: Image.Image, width: int, height: int
) -> None:
    """Draw large geometric shapes and thick lines/curves over the gradient.

    All positions/sizes are drawn as fractions of the canvas, so the same seed
    yields the same layout at any resolution (perceptual identity across the size
    correction loop). Mutates ``img`` in place.
    """
    from PIL import ImageDraw

    draw = ImageDraw.Draw(img)
    side = min(width, height)

    def _color() -> tuple[int, int, int]:
        r, g, b = (int(c) for c in rng.integers(0, 256, size=3))
        return (r, g, b)

    def _point() -> tuple[int, int]:
        return (int(rng.uniform(0, width)), int(rng.uniform(0, height)))

    def _box() -> list[int]:
        w = max(1, int(rng.uniform(0.15, 0.5) * width))
        h = max(1, int(rng.uniform(0.15, 0.5) * height))
        x0 = int(rng.uniform(0, max(1, width - w)))
        y0 = int(rng.uniform(0, max(1, height - h)))
        return [x0, y0, x0 + w, y0 + h]

    for _ in range(int(rng.integers(3, 9))):  # 3-8 large shapes
        kind = int(rng.integers(0, 3))
        if kind == 0:
            draw.rectangle(_box(), fill=_color())
        elif kind == 1:
            draw.ellipse(_box(), fill=_color())
        else:
            pts = [_point() for _ in range(int(rng.integers(3, 6)))]
            draw.polygon(pts, fill=_color())

    line_width = max(1, side // 80)
    for _ in range(int(rng.integers(2, 7))):  # 2-6 thick lines/curves
        if float(rng.uniform(0, 1)) < 0.3:
            start = float(rng.uniform(0, 360))
            draw.arc(
                _box(),
                start,
                start + float(rng.uniform(30, 300)),
                fill=_color(),
                width=line_width,
            )
        else:
            draw.line(
                [_point() for _ in range(int(rng.integers(2, 5)))],
                fill=_color(),
                width=line_width,
            )


def _encode(seed: int, width: int, height: int, fmt: str) -> bytes:
    """Encode a deterministic structured ``width``x``height`` RGB image.

    Builds a smooth gradient + light low-frequency texture (numpy), then overlays
    large shapes and thick lines/curves (Pillow). The structure makes the image
    pHash/dedupe-realistic; it carries no per-pixel white noise and no padding.
    Tiny images (side < ``_MIN_OVERLAY_SIDE``) render the gradient/texture only.
    """
    import numpy as np
    from PIL import Image

    rng = np.random.default_rng(seed)
    arr = _gradient_background(rng, width, height)
    arr = _add_texture(rng, arr, width, height)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), mode="RGB")
    if min(width, height) >= _MIN_OVERLAY_SIDE:
        _draw_overlays(rng, img, width, height)
    buf = io.BytesIO()
    if fmt == "png":
        img.save(buf, format="PNG", compress_level=0)
    else:
        img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def render_sized_image(
    image_id: int,
    lo: int,
    hi: int,
    target_bytes: int,
    *,
    image_format: str = "png",
) -> RenderedImage:
    """Render a real image for ``image_id`` whose encoded size lands in ``[lo, hi)``.

    Deterministic in ``image_id``. Computes a starting resolution from the target,
    then runs a bounded correction loop (rescale the pixel count by
    ``target/actual``) until the encoded size is in-bucket or the pass budget is
    exhausted; returns whatever it produced (the caller records ``actual_bytes``).
    """
    fmt = normalize_format(image_format)
    seed = image_distribution.row_hash(image_id)
    width = height = _side_for_target(target_bytes)
    data = _encode(seed, width, height, fmt)
    for _ in range(_MAX_CORRECTION_PASSES):
        actual = len(data)
        if lo <= actual < hi:
            break
        scaled = round(
            math.sqrt(max(1.0, width * height * target_bytes / max(actual, 1)))
        )
        if actual < lo:
            # Below the floor: the area-ratio step stalls for JPEG (compression is
            # sub-linear in resolution), so enforce a minimum growth to climb in.
            new_side = max(width + 1, round(width * _MIN_GROWTH), scaled)
        else:  # actual >= hi
            new_side = max(_MIN_SIDE, scaled)
        if new_side == width:  # nudge to make progress when rounding stalls
            new_side = max(_MIN_SIDE, width + (1 if actual < lo else -1))
        if new_side == width:
            break
        width = height = new_side
        data = _encode(seed, width, height, fmt)
    return RenderedImage(
        image_bytes=data,
        actual_bytes=len(data),
        width=width,
        height=height,
        image_format=fmt,
    )


def bucket_of(size: int) -> str:
    """The ``SIZE_BUCKETS`` label whose ``[lo, hi)`` contains ``size``.

    Lets a caller record the bucket of the *actual* encoded size, so the manifest's
    bucket label never disagrees with its byte count (sizes outside the configured
    range clamp to the nearest end bucket).
    """
    for name, lo, hi, _ in constants.SIZE_BUCKETS:
        if lo <= size < hi:
            return name
    first, last = constants.SIZE_BUCKETS[0], constants.SIZE_BUCKETS[-1]
    return first[0] if size < first[1] else last[0]


def render_for_id(
    image_id: int,
    *,
    image_format: str = "png",
    include_large_tail: bool = False,
    max_bytes: int | None = None,
) -> RenderedImage:
    """Resolve the target size for ``image_id`` (Atlas distribution) and render it."""
    assignment = image_distribution.assign(
        image_id, include_large_tail=include_large_tail, max_bytes=max_bytes
    )
    return render_sized_image(
        image_id,
        assignment.lo,
        assignment.hi,
        assignment.target,
        image_format=image_format,
    )


def target_assignment(
    image_id: int, *, include_large_tail: bool = False, max_bytes: int | None = None
) -> image_distribution.BucketAssignment:
    """The (bucket, lo, hi, target) for ``image_id`` — exposed for the manifest."""
    return image_distribution.assign(
        image_id, include_large_tail=include_large_tail, max_bytes=max_bytes
    )
