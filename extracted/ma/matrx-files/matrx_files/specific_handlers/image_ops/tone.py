"""Tonal adjustments: curves, levels, shadows/highlights, white-balance probe, document clean."""

from __future__ import annotations

from typing import Literal

from PIL import Image

from .base import ImageOp, OpParams, register_op


class CurvesParams(OpParams):
    """Per-channel curves. Each curve is a list of (input, output) points
    in 0..255, sorted by input. Linear interpolation between points.

    Provide a single ``rgb`` curve OR per-channel curves. When both are
    given, ``rgb`` is applied first, then per-channel."""
    rgb: list[tuple[int, int]] | None = None
    r: list[tuple[int, int]] | None = None
    g: list[tuple[int, int]] | None = None
    b: list[tuple[int, int]] | None = None


@register_op
class CurvesOp(ImageOp):
    name = "curves"
    params_model = CurvesParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: CurvesParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image

        if params.rgb:
            lut = _build_curve_lut(params.rgb)
            work = work.point(lut * 3)

        r_lut = _build_curve_lut(params.r) if params.r else list(range(256))
        g_lut = _build_curve_lut(params.g) if params.g else list(range(256))
        b_lut = _build_curve_lut(params.b) if params.b else list(range(256))
        if any((params.r, params.g, params.b)):
            work = work.point(r_lut + g_lut + b_lut)

        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


def _build_curve_lut(points: list[tuple[int, int]]) -> list[int]:
    pts = sorted([(max(0, min(255, x)), max(0, min(255, y))) for x, y in points])
    if not pts or pts[0][0] > 0:
        pts.insert(0, (0, pts[0][1] if pts else 0))
    if pts[-1][0] < 255:
        pts.append((255, pts[-1][1]))
    lut: list[int] = []
    seg = 0
    for i in range(256):
        while seg < len(pts) - 1 and i > pts[seg + 1][0]:
            seg += 1
        x0, y0 = pts[seg]
        x1, y1 = pts[seg + 1] if seg + 1 < len(pts) else pts[seg]
        if x1 == x0:
            lut.append(y0)
        else:
            t = (i - x0) / (x1 - x0)
            lut.append(int(round(y0 + t * (y1 - y0))))
    return lut


class LevelsParams(OpParams):
    """Photoshop-style levels: clip input black/white, gamma-curve midtones,
    then remap to output black/white range."""
    in_black: int = 0
    in_white: int = 255
    gamma: float = 1.0
    out_black: int = 0
    out_white: int = 255


@register_op
class LevelsOp(ImageOp):
    name = "levels"
    params_model = LevelsParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: LevelsParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        ib, iw = max(0, params.in_black), max(0, min(255, params.in_white))
        ob, ow = max(0, params.out_black), max(0, min(255, params.out_white))
        if iw <= ib:
            iw = ib + 1
        inv_gamma = 1.0 / max(0.01, params.gamma)
        lut: list[int] = []
        for i in range(256):
            t = max(0.0, min(1.0, (i - ib) / (iw - ib)))
            t = t ** inv_gamma
            lut.append(int(round(ob + t * (ow - ob))))
        work = work.point(lut * 3)
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class ShadowsHighlightsParams(OpParams):
    shadows: float = 0.0     # -100..100 — positive lifts shadows
    highlights: float = 0.0  # -100..100 — positive recovers highlights


@register_op
class ShadowsHighlightsOp(ImageOp):
    name = "shadows_highlights"
    params_model = ShadowsHighlightsParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: ShadowsHighlightsParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        s = max(-100.0, min(100.0, params.shadows)) / 100.0
        h = max(-100.0, min(100.0, params.highlights)) / 100.0

        lut: list[int] = []
        for i in range(256):
            v = i / 255.0
            # Shadow lift: stronger boost for low values.
            shadow_weight = (1.0 - v) ** 2
            # Highlight recovery: stronger pull for high values.
            highlight_weight = v ** 2
            new = v + s * shadow_weight * 0.5 - h * highlight_weight * 0.5
            lut.append(max(0, min(255, int(round(new * 255)))))
        work = work.point(lut * 3)
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class WhiteBalanceParams(OpParams):
    """Simple white-balance: gray-world or known-neutral pixel."""
    method: str = "gray_world"  # "gray_world" or "neutral"
    # When method == "neutral", give the pixel coords of a neutral patch.
    neutral_x: int | None = None
    neutral_y: int | None = None


@register_op
class WhiteBalanceOp(ImageOp):
    name = "white_balance"
    params_model = WhiteBalanceParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: WhiteBalanceParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        from PIL import ImageStat

        if params.method == "neutral" and params.neutral_x is not None and params.neutral_y is not None:
            r, g, b = work.getpixel((params.neutral_x, params.neutral_y))[:3]
        else:
            stat = ImageStat.Stat(work)
            r, g, b = stat.mean

        # Target: equal channel means. Compute scale per channel.
        target = (r + g + b) / 3.0
        if r <= 0 or g <= 0 or b <= 0:
            return image
        sr, sg, sb = target / r, target / g, target / b
        r_lut = [max(0, min(255, int(i * sr))) for i in range(256)]
        g_lut = [max(0, min(255, int(i * sg))) for i in range(256)]
        b_lut = [max(0, min(255, int(i * sb))) for i in range(256)]
        work = work.point(r_lut + g_lut + b_lut)
        if alpha is not None:
            work = work.convert("RGBA")
            work.putalpha(alpha)
        return work


class DocumentCleanParams(OpParams):
    """Flatten uneven lighting on a photographed page.

    ``gray`` = clean grayscale (default, best for text), ``color`` = keep
    ink colors, ``bw`` = pure black-and-white (Otsu threshold)."""
    mode: Literal["gray", "color", "bw"] = "gray"


# Background estimation runs on a downscaled copy — the paper's lighting
# field is low-frequency, so full resolution is pure waste.
_CLEAN_BG_MAX_DIM = 1000


@register_op
class DocumentCleanOp(ImageOp):
    """Scanner-style cleanup: estimate the paper's lighting (dilate to erase
    ink, median-blur to smooth), divide it out so shadows and gradients
    vanish, then push paper to white and ink to black."""
    name = "document_clean"
    params_model = DocumentCleanParams
    preserves_alpha = False

    def apply(self, image: Image.Image, mask, params: DocumentCleanParams) -> Image.Image:
        try:
            import cv2  # type: ignore[import-not-found]
            import numpy as np  # type: ignore[import-not-found]
        except ImportError as e:
            from matrx_files._extras import missing_extra_message

            raise RuntimeError(missing_extra_message("media", e.name or "cv2", "Document clean")) from e

        if params.mode == "color":
            src = np.array(image.convert("RGB"))
            channels = [src[:, :, i] for i in range(3)]
        else:
            channels = [np.array(image.convert("L"))]

        h, w = channels[0].shape
        scale = min(1.0, _CLEAN_BG_MAX_DIM / max(h, w))
        sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
        kernel = np.ones((7, 7), np.uint8)

        cleaned = []
        for ch in channels:
            small = cv2.resize(ch, (sw, sh), interpolation=cv2.INTER_AREA)
            bg = cv2.medianBlur(cv2.dilate(small, kernel), 21)
            bg = cv2.resize(bg, (w, h), interpolation=cv2.INTER_LINEAR)
            flat = cv2.divide(ch, np.maximum(bg, 1), scale=255)
            # Paper → white, faint ink → solid; same push as the scanner's B&W levels.
            lut = np.clip((np.arange(256) - 60) * 255.0 / (235 - 60), 0, 255).astype(np.uint8)
            cleaned.append(cv2.LUT(flat, lut))

        if params.mode == "color":
            return Image.fromarray(np.dstack(cleaned), "RGB")
        out = cleaned[0]
        if params.mode == "bw":
            _, out = cv2.threshold(out, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return Image.fromarray(out, "L").convert("RGB")
