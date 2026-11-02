"""Blur, sharpen, denoise, vignette, grain — frequency-domain effects."""

from __future__ import annotations

import math
import random
from typing import Literal

from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageChops

from .base import ImageOp, OpParams, register_op


class BlurParams(OpParams):
    kind: Literal["gaussian", "box", "motion"] = "gaussian"
    radius: float = 4.0          # pixels
    angle: float = 0.0           # for motion blur (degrees)


@register_op
class BlurOp(ImageOp):
    name = "blur"
    params_model = BlurParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: BlurParams) -> Image.Image:
        r = max(0.0, params.radius)
        if params.kind == "gaussian":
            return image.filter(ImageFilter.GaussianBlur(r))
        if params.kind == "box":
            return image.filter(ImageFilter.BoxBlur(r))
        if params.kind == "motion":
            return _motion_blur(image, r, params.angle)
        raise ValueError(f"Unknown blur kind: {params.kind!r}")


def _motion_blur(img: Image.Image, radius: float, angle_deg: float) -> Image.Image:
    # Approximate directional blur by rotating, BoxBlur on one axis, rotating back.
    if radius <= 0:
        return img
    rotated = img.rotate(-angle_deg, resample=Image.BICUBIC, expand=True)
    blurred = rotated.filter(ImageFilter.GaussianBlur(radius=radius))
    # Approximate horizontal-only directional smear via additional box blur:
    blurred = blurred.filter(ImageFilter.BoxBlur((radius, 0)))
    out = blurred.rotate(angle_deg, resample=Image.BICUBIC, expand=True)
    # Crop back to original size, centered.
    ow, oh = img.size
    bw, bh = out.size
    left = (bw - ow) // 2
    top = (bh - oh) // 2
    return out.crop((left, top, left + ow, top + oh))


class SharpenParams(OpParams):
    amount: float = 1.0          # multiplier on Pillow's UnsharpMask
    radius: float = 2.0
    threshold: int = 3


@register_op
class SharpenOp(ImageOp):
    name = "sharpen"
    params_model = SharpenParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: SharpenParams) -> Image.Image:
        percent = max(0, int(round(params.amount * 150)))
        return image.filter(
            ImageFilter.UnsharpMask(radius=params.radius, percent=percent, threshold=params.threshold)
        )


class DenoiseParams(OpParams):
    strength: float = 1.0  # 0..3 — Pillow median filter size scales with this


@register_op
class DenoiseOp(ImageOp):
    name = "denoise"
    params_model = DenoiseParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: DenoiseParams) -> Image.Image:
        # Median filter at odd sizes 3/5/7 depending on strength.
        s = max(0.0, min(3.0, params.strength))
        size = 3 if s <= 1.0 else (5 if s <= 2.0 else 7)
        return image.filter(ImageFilter.MedianFilter(size=size))


class VignetteParams(OpParams):
    intensity: float = 0.6       # 0..1
    radius: float = 0.75         # 0..1 — fraction of half-diagonal where falloff starts
    color: str = "#000000"


@register_op
class VignetteOp(ImageOp):
    name = "vignette"
    params_model = VignetteParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: VignetteParams) -> Image.Image:
        w, h = image.size
        # Build radial mask: white in center fading to black at corners.
        cx, cy = w / 2.0, h / 2.0
        max_d = math.hypot(cx, cy)
        falloff_start = max(0.01, min(0.99, params.radius)) * max_d
        intensity = max(0.0, min(1.0, params.intensity))

        gradient = Image.new("L", (w, h), 0)
        # Build via per-pixel lookup is too slow for big images; use a radial
        # gradient via ImageDraw rings:
        n_steps = 64
        for i in range(n_steps, 0, -1):
            r = (i / n_steps) * max_d
            val = 0 if r > falloff_start else int(255 * (1.0 - (r / falloff_start)) ** 1.6)
            box = (cx - r, cy - r, cx + r, cy + r)
            ImageDraw.Draw(gradient).ellipse(box, fill=val)
        # Compose: darken the source by ``intensity * (1 - gradient)``.
        from PIL import ImageColor
        rgba = image.convert("RGBA") if image.mode != "RGBA" else image
        overlay = Image.new("RGB", (w, h), ImageColor.getrgb(params.color))
        # invert gradient so corners (0 → 255) drive darkening.
        darken_mask = ImageOps.invert(gradient)
        # scale by intensity:
        darken_mask = darken_mask.point(lambda v: int(v * intensity))
        out = Image.composite(overlay, rgba.convert("RGB"), darken_mask)
        if image.mode == "RGBA":
            out = out.convert("RGBA")
            out.putalpha(image.split()[-1])
        return out


class GrainParams(OpParams):
    amount: float = 0.15         # 0..1 — fraction of luminance noise to add
    monochrome: bool = True


@register_op
class GrainOp(ImageOp):
    name = "grain"
    params_model = GrainParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: GrainParams) -> Image.Image:
        amount = max(0.0, min(1.0, params.amount))
        if amount == 0.0:
            return image
        w, h = image.size
        # Generate per-pixel noise — Pillow has no built-in, but
        # we can fake it with ImageDraw on a small noise tile scaled up.
        # For speed, use a sparse random dot field at full resolution.
        noise = Image.new("L", (w, h), 128)
        px = noise.load()
        spread = int(amount * 80)  # +/- amplitude
        for y in range(h):
            for x in range(0, w, 1):
                px[x, y] = max(0, min(255, 128 + random.randint(-spread, spread)))
        if params.monochrome:
            noise_rgb = Image.merge("RGB", (noise, noise, noise))
        else:
            # Independent channels for color grain.
            other = noise.copy()
            other2 = noise.copy()
            for y in range(h):
                for x in range(w):
                    other.putpixel((x, y), max(0, min(255, 128 + random.randint(-spread, spread))))
                    other2.putpixel((x, y), max(0, min(255, 128 + random.randint(-spread, spread))))
            noise_rgb = Image.merge("RGB", (noise, other, other2))
        base = image.convert("RGB") if image.mode != "RGB" else image
        # Blend in additive mode: result = base + (noise - 128).
        offset = ImageChops.subtract(noise_rgb, Image.new("RGB", (w, h), (128, 128, 128)))
        out = ImageChops.add(base, offset)
        if image.mode == "RGBA":
            out = out.convert("RGBA")
            out.putalpha(image.split()[-1])
        return out


class EdgeDetectParams(OpParams):
    mode: Literal["find", "enhance", "enhance_more"] = "find"


@register_op
class EdgeDetectOp(ImageOp):
    name = "edge_detect"
    params_model = EdgeDetectParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: EdgeDetectParams) -> Image.Image:
        flt = {
            "find": ImageFilter.FIND_EDGES,
            "enhance": ImageFilter.EDGE_ENHANCE,
            "enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
        }[params.mode]
        return image.filter(flt)


class EmbossParams(OpParams):
    pass


@register_op
class EmbossOp(ImageOp):
    name = "emboss"
    params_model = EmbossParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        return image.filter(ImageFilter.EMBOSS)


class PosterizeParams(OpParams):
    bits: int = 3  # 1..8 — bits per channel; lower = stronger posterize


@register_op
class PosterizeOp(ImageOp):
    name = "posterize"
    params_model = PosterizeParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: PosterizeParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        bits = max(1, min(8, params.bits))
        work = ImageOps.posterize(work, bits)
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class SolarizeParams(OpParams):
    threshold: int = 128  # 0..255 — pixels above this get inverted


@register_op
class SolarizeOp(ImageOp):
    name = "solarize"
    params_model = SolarizeParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: SolarizeParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        work = ImageOps.solarize(work, threshold=max(0, min(255, params.threshold)))
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work
