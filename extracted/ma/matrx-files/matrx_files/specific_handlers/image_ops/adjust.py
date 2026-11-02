"""Color/light adjustments — brightness, contrast, saturation, hue, etc."""

from __future__ import annotations

from PIL import Image, ImageEnhance, ImageOps

from .base import ImageOp, OpParams, register_op


class AdjustParams(OpParams):
    # Each setting is a multiplier centered on 1.0 (1.0 = no change).
    brightness: float = 1.0     # 0.0..3.0 — 1.0 unchanged
    contrast: float = 1.0       # 0.0..3.0
    saturation: float = 1.0     # 0.0..3.0 — 0.0 = grayscale
    sharpness: float = 1.0      # 0.0..3.0 — 1.0 unchanged, >1 sharpens
    # Hue rotation in degrees (-180..180). 0 leaves the image unchanged.
    hue_rotate: float = 0.0
    # Gamma correction. 1.0 = no change; >1 brightens midtones.
    gamma: float = 1.0
    # Exposure (in stops). Each stop doubles or halves the luminance.
    # Range typically -3.0..3.0.
    exposure: float = 0.0
    # Temperature in degrees Kelvin offset (-100..100, approximate).
    # Positive = warmer (more red); negative = cooler (more blue).
    temperature: float = 0.0
    # Tint (-100..100). Positive = magenta; negative = green.
    tint: float = 0.0
    # Vibrance — saturation that favors less-saturated colors (-100..100).
    vibrance: float = 0.0


@register_op
class AdjustOp(ImageOp):
    name = "adjust"
    params_model = AdjustParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: AdjustParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image

        if params.brightness != 1.0:
            work = ImageEnhance.Brightness(work).enhance(params.brightness)
        if params.contrast != 1.0:
            work = ImageEnhance.Contrast(work).enhance(params.contrast)
        if params.saturation != 1.0:
            work = ImageEnhance.Color(work).enhance(params.saturation)
        if params.sharpness != 1.0:
            work = ImageEnhance.Sharpness(work).enhance(params.sharpness)

        if params.exposure != 0.0:
            factor = 2.0 ** params.exposure
            work = ImageEnhance.Brightness(work).enhance(factor)

        if params.gamma != 1.0 and params.gamma > 0:
            inv = 1.0 / params.gamma
            lut = [min(255, int(((i / 255.0) ** inv) * 255 + 0.5)) for i in range(256)]
            work = work.point(lut * 3)

        if params.temperature != 0.0 or params.tint != 0.0:
            work = _apply_temperature_tint(work, params.temperature, params.tint)

        if params.vibrance != 0.0:
            work = _apply_vibrance(work, params.vibrance)

        if params.hue_rotate != 0.0:
            work = _apply_hue_rotate(work, params.hue_rotate)

        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


def _apply_temperature_tint(img: Image.Image, temperature: float, tint: float) -> Image.Image:
    # Simple per-channel curve: temperature shifts R/B, tint shifts G.
    t = max(-100.0, min(100.0, temperature)) / 100.0
    g = max(-100.0, min(100.0, tint)) / 100.0
    r_shift = int(round(t * 30))
    b_shift = int(round(-t * 30))
    g_shift = int(round(g * 30))
    r_lut = [max(0, min(255, i + r_shift)) for i in range(256)]
    g_lut = [max(0, min(255, i + g_shift)) for i in range(256)]
    b_lut = [max(0, min(255, i + b_shift)) for i in range(256)]
    return img.point(r_lut + g_lut + b_lut)


def _apply_vibrance(img: Image.Image, vibrance: float) -> Image.Image:
    # Vibrance protects already-saturated colors. Approximation via HSV:
    # boost saturation by a factor scaled inverse to current saturation.
    v = max(-100.0, min(100.0, vibrance)) / 100.0
    hsv = img.convert("HSV")
    h, s, val = hsv.split()
    # Boost desaturated pixels more than saturated ones.
    s_lut = []
    for i in range(256):
        # i is current S in [0..255]. Less-saturated → larger boost.
        ratio = 1.0 - (i / 255.0)
        new = i + v * 100.0 * ratio
        s_lut.append(max(0, min(255, int(round(new)))))
    s = s.point(s_lut)
    return Image.merge("HSV", (h, s, val)).convert("RGB")


def _apply_hue_rotate(img: Image.Image, degrees: float) -> Image.Image:
    # Pillow HSV channel is 0..255 mapping to 0..360°. Shift the H channel.
    shift = int(round((degrees / 360.0) * 255)) % 255
    hsv = img.convert("HSV")
    h, s, v = hsv.split()
    h_lut = [(i + shift) % 255 for i in range(256)]
    h = h.point(h_lut)
    return Image.merge("HSV", (h, s, v)).convert("RGB")


# ---------------------------------------------------------------------------
# Auto-* ops — one-shot heuristics
# ---------------------------------------------------------------------------

class AutoLevelsParams(OpParams):
    cutoff: float = 1.0  # Percent of pixels to clip from each end (0..10).


@register_op
class AutoLevelsOp(ImageOp):
    name = "auto_levels"
    params_model = AutoLevelsParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: AutoLevelsParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        cutoff = max(0.0, min(10.0, params.cutoff))
        work = ImageOps.autocontrast(work, cutoff=cutoff)
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class AutoColorParams(OpParams):
    pass


@register_op
class AutoColorOp(ImageOp):
    """Per-channel autocontrast — corrects color casts."""
    name = "auto_color"
    params_model = AutoColorParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        r, g, b = work.split()
        r = ImageOps.autocontrast(r)
        g = ImageOps.autocontrast(g)
        b = ImageOps.autocontrast(b)
        work = Image.merge("RGB", (r, g, b))
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class EqualizeParams(OpParams):
    pass


@register_op
class EqualizeOp(ImageOp):
    name = "equalize"
    params_model = EqualizeParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        work = ImageOps.equalize(work)
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class GrayscaleParams(OpParams):
    pass


@register_op
class GrayscaleOp(ImageOp):
    name = "grayscale"
    params_model = GrayscaleParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = ImageOps.grayscale(image).convert("RGB")
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class InvertParams(OpParams):
    pass


@register_op
class InvertOp(ImageOp):
    name = "invert"
    params_model = InvertParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        work = ImageOps.invert(work)
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class SepiaParams(OpParams):
    intensity: float = 1.0  # 0..1 — full sepia at 1.0


@register_op
class SepiaOp(ImageOp):
    name = "sepia"
    params_model = SepiaParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: SepiaParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        gs = ImageOps.grayscale(work)
        # Sepia palette via colorize: dark → black, light → light tan.
        sepia = ImageOps.colorize(gs, black=(20, 5, 0), white=(255, 230, 200))
        i = max(0.0, min(1.0, params.intensity))
        if i < 1.0:
            sepia = Image.blend(work, sepia, i)
        if alpha is not None:
            sepia = sepia.convert("RGBA")
            sepia.putalpha(alpha)
        return sepia
