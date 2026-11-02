"""Mask manipulation: feather, expand/contract, combine, threshold, from-color-key.

These ops take a mask as input/output. The "image" arg is the source image
the mask refines against — for ops that need pixel data (color-key) — or
is treated as the canvas to render the result mask onto for visualisation.

The output of every mask op is a single-channel "L" mode image at the
source size, returned via the standard ImageOp protocol. The dispatcher
turns it into an RGBA PNG (white-on-transparent) via ``preserves_alpha``.
"""

from __future__ import annotations

import math
from typing import Literal

from PIL import Image, ImageChops, ImageColor, ImageFilter

from .base import ImageOp, OpParams, register_op


# ---------------------------------------------------------------------------
# Mask helpers (used by color.py + by mask ops)
# ---------------------------------------------------------------------------

def generate_mask_from_color_key(
    rgba: Image.Image,
    target_color: str,
    *,
    tolerance: int = 32,
    feather: int = 0,
) -> Image.Image:
    """Return an "L" mask where pixels within ``tolerance`` of ``target_color``
    are white (255) and the rest are black (0)."""
    try:
        tr, tg, tb = ImageColor.getrgb(target_color)[:3]
    except ValueError as e:
        raise ValueError(f"Bad target_color {target_color!r}: {e}") from e
    tol = max(0, tolerance)
    tol_sq = tol * tol
    rgb = rgba.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    mask = Image.new("L", (w, h), 0)
    mpx = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            dr, dg, db = r - tr, g - tg, b - tb
            d_sq = dr * dr + dg * dg + db * db
            if d_sq <= tol_sq:
                mpx[x, y] = 255
    if feather > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=feather))
    return mask


def _wrap_mask_as_rgba_visualization(mask: Image.Image) -> Image.Image:
    """Turn an L mask into a PNG-saveable RGBA image (white on transparent)."""
    rgba = Image.new("RGBA", mask.size, (255, 255, 255, 0))
    white = Image.new("RGBA", mask.size, (255, 255, 255, 255))
    rgba = Image.composite(white, rgba, mask)
    return rgba


# ---------------------------------------------------------------------------
# Mask ops
# ---------------------------------------------------------------------------

class FromColorKeyParams(OpParams):
    target_color: str
    tolerance: int = 32
    feather: int = 0


@register_op
class MaskFromColorKeyOp(ImageOp):
    """Generate a mask from a color-key — outputs a PNG mask, not a recolored image."""
    name = "mask.from_color_key"
    params_model = FromColorKeyParams
    preserves_alpha = True
    supports_mask = False
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params: FromColorKeyParams) -> Image.Image:
        rgba = image.convert("RGBA")
        m = generate_mask_from_color_key(
            rgba, params.target_color, tolerance=params.tolerance, feather=params.feather,
        )
        return _wrap_mask_as_rgba_visualization(m)


class FeatherParams(OpParams):
    radius: float = 4.0


@register_op
class MaskFeatherOp(ImageOp):
    """Soften mask edges via Gaussian blur."""
    name = "mask.feather"
    params_model = FeatherParams
    preserves_alpha = True
    supports_mask = True
    requires_mask = True
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params: FeatherParams) -> Image.Image:
        if mask is None:
            raise ValueError("mask.feather requires a mask")
        blurred = mask.filter(ImageFilter.GaussianBlur(params.radius))
        return _wrap_mask_as_rgba_visualization(blurred)


class GrowShrinkParams(OpParams):
    pixels: int = 4  # negative = shrink (erode), positive = grow (dilate)


@register_op
class MaskGrowOp(ImageOp):
    """Expand (dilate) or shrink (erode) a mask."""
    name = "mask.grow"
    params_model = GrowShrinkParams
    preserves_alpha = True
    supports_mask = True
    requires_mask = True
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params: GrowShrinkParams) -> Image.Image:
        if mask is None:
            raise ValueError("mask.grow requires a mask")
        # MaxFilter (dilation) for grow, MinFilter (erosion) for shrink.
        # Filter sizes must be odd, so quantize per pixel iteration.
        steps = abs(params.pixels)
        if steps == 0:
            return _wrap_mask_as_rgba_visualization(mask)
        kernel = ImageFilter.MaxFilter(3) if params.pixels > 0 else ImageFilter.MinFilter(3)
        m = mask.copy()
        for _ in range(steps):
            m = m.filter(kernel)
        return _wrap_mask_as_rgba_visualization(m)


class InvertMaskParams(OpParams):
    pass


@register_op
class MaskInvertOp(ImageOp):
    name = "mask.invert"
    params_model = InvertMaskParams
    preserves_alpha = True
    supports_mask = True
    requires_mask = True
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        if mask is None:
            raise ValueError("mask.invert requires a mask")
        from PIL import ImageOps
        return _wrap_mask_as_rgba_visualization(ImageOps.invert(mask))


class ThresholdParams(OpParams):
    threshold: int = 128


@register_op
class MaskThresholdOp(ImageOp):
    """Sharpen a feathered mask: every pixel above threshold → 255, below → 0."""
    name = "mask.threshold"
    params_model = ThresholdParams
    preserves_alpha = True
    supports_mask = True
    requires_mask = True
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params: ThresholdParams) -> Image.Image:
        if mask is None:
            raise ValueError("mask.threshold requires a mask")
        t = max(0, min(255, params.threshold))
        lut = [0 if v < t else 255 for v in range(256)]
        return _wrap_mask_as_rgba_visualization(mask.point(lut))


class SmoothEdgesParams(OpParams):
    radius: float = 2.0


@register_op
class MaskSmoothEdgesOp(ImageOp):
    """Apply a small Gaussian blur then a re-threshold to clean jagged edges."""
    name = "mask.smooth_edges"
    params_model = SmoothEdgesParams
    preserves_alpha = True
    supports_mask = True
    requires_mask = True
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params: SmoothEdgesParams) -> Image.Image:
        if mask is None:
            raise ValueError("mask.smooth_edges requires a mask")
        m = mask.filter(ImageFilter.GaussianBlur(params.radius))
        lut = [0 if v < 128 else 255 for v in range(256)]
        return _wrap_mask_as_rgba_visualization(m.point(lut))


class CombineParams(OpParams):
    """Combine the supplied mask with a second mask loaded by file_id elsewhere.

    The ``other_mask_b64`` is the base64-encoded PNG of the second mask
    so this op stays self-contained (no DB lookups inside matrx-utils).
    The host router decodes/encodes if it wants to pass file_ids; here
    we accept bytes-via-base64 to keep the protocol clean.
    """
    operation: Literal["union", "intersect", "difference", "xor"] = "union"
    other_mask_b64: str


@register_op
class MaskCombineOp(ImageOp):
    name = "mask.combine"
    params_model = CombineParams
    preserves_alpha = True
    supports_mask = True
    requires_mask = True
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params: CombineParams) -> Image.Image:
        if mask is None:
            raise ValueError("mask.combine requires a mask")
        import base64
        from io import BytesIO
        from .base import load_mask_from_png_bytes
        other_bytes = base64.b64decode(params.other_mask_b64)
        other = load_mask_from_png_bytes(other_bytes, target_size=mask.size)
        if params.operation == "union":
            out = ImageChops.lighter(mask, other)
        elif params.operation == "intersect":
            out = ImageChops.darker(mask, other)
        elif params.operation == "difference":
            out = ImageChops.subtract(mask, other)
        else:  # xor
            out = ImageChops.difference(mask, other)
        return _wrap_mask_as_rgba_visualization(out)


class FromAlphaParams(OpParams):
    pass


@register_op
class MaskFromAlphaOp(ImageOp):
    """Lift a source image's alpha channel into a mask."""
    name = "mask.from_alpha"
    params_model = FromAlphaParams
    preserves_alpha = True
    supports_mask = False
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        if image.mode != "RGBA":
            # No alpha → opaque mask.
            return _wrap_mask_as_rgba_visualization(
                Image.new("L", image.size, 255)
            )
        return _wrap_mask_as_rgba_visualization(image.split()[-1])
