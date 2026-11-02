"""Crop, rotate, flip, perspective, EXIF strip — geometric transforms."""

from __future__ import annotations

from typing import Literal

from PIL import Image, ImageOps

from .base import ImageOp, OpParams, register_op


# Aspect-ratio presets the FE picker exposes. Adding here = picker gets it.
ASPECT_RATIO_PRESETS: dict[str, tuple[int, int]] = {
    "1:1": (1, 1),
    "4:3": (4, 3),
    "3:2": (3, 2),
    "16:9": (16, 9),
    "9:16": (9, 16),
    "4:5": (4, 5),
    "5:4": (5, 4),
    "3:4": (3, 4),
    "2:3": (2, 3),
    "21:9": (21, 9),
}


class CropParams(OpParams):
    # Either a rectangle in pixels (left/top/right/bottom) OR an aspect-ratio name.
    left: int | None = None
    top: int | None = None
    right: int | None = None
    bottom: int | None = None
    aspect: str | None = None  # e.g. "16:9" — auto-centred crop to this aspect
    # When using ``aspect``, anchor controls where the kept region sits.
    anchor: Literal["center", "top", "bottom", "left", "right"] = "center"


@register_op
class CropOp(ImageOp):
    name = "crop"
    params_model = CropParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: CropParams) -> Image.Image:
        if params.aspect is not None:
            return _crop_to_aspect(image, params.aspect, params.anchor)
        box = (
            params.left or 0,
            params.top or 0,
            params.right if params.right is not None else image.size[0],
            params.bottom if params.bottom is not None else image.size[1],
        )
        return image.crop(box)


def _crop_to_aspect(img: Image.Image, aspect: str, anchor: str) -> Image.Image:
    if aspect not in ASPECT_RATIO_PRESETS:
        raise ValueError(
            f"Unknown aspect ratio {aspect!r}. Known: {sorted(ASPECT_RATIO_PRESETS)}"
        )
    aw, ah = ASPECT_RATIO_PRESETS[aspect]
    w, h = img.size
    target_ratio = aw / ah
    src_ratio = w / h
    if src_ratio > target_ratio:
        # Too wide — crop horizontally.
        new_w = int(h * target_ratio)
        if anchor == "left":
            left = 0
        elif anchor == "right":
            left = w - new_w
        else:
            left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    # Too tall — crop vertically.
    new_h = int(w / target_ratio)
    if anchor == "top":
        top = 0
    elif anchor == "bottom":
        top = h - new_h
    else:
        top = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


class RotateParams(OpParams):
    degrees: float = 0.0
    expand: bool = True
    fill: str = "#00000000"  # transparent default


@register_op
class RotateOp(ImageOp):
    name = "rotate"
    params_model = RotateParams
    preserves_alpha = True
    supports_mask = False  # rotation changes dims; mask compose isn't meaningful

    def apply(self, image: Image.Image, mask, params: RotateParams) -> Image.Image:
        from PIL import ImageColor
        rgba = image.convert("RGBA") if image.mode != "RGBA" else image
        try:
            fill = ImageColor.getrgb(params.fill) if not params.fill.endswith("00") else (0, 0, 0, 0)
        except ValueError:
            fill = (0, 0, 0, 0)
        return rgba.rotate(
            params.degrees,
            resample=Image.BICUBIC,
            expand=params.expand,
            fillcolor=fill,
        )


class FlipParams(OpParams):
    direction: Literal["horizontal", "vertical", "both"] = "horizontal"


@register_op
class FlipOp(ImageOp):
    name = "flip"
    params_model = FlipParams
    preserves_alpha = True
    supports_mask = False

    def apply(self, image: Image.Image, mask, params: FlipParams) -> Image.Image:
        if params.direction == "horizontal":
            return ImageOps.mirror(image)
        if params.direction == "vertical":
            return ImageOps.flip(image)
        return ImageOps.flip(ImageOps.mirror(image))


class ResizeParams(OpParams):
    width: int | None = None
    height: int | None = None
    fit: Literal["cover", "contain", "fill", "inside"] = "fill"
    background: str = "#ffffff"


@register_op
class ResizeOp(ImageOp):
    name = "resize"
    params_model = ResizeParams
    preserves_alpha = True
    supports_mask = False

    def apply(self, image: Image.Image, mask, params: ResizeParams) -> Image.Image:
        from PIL import ImageColor
        ow, oh = image.size
        if params.width is None and params.height is None:
            return image
        if params.width is None:
            assert params.height is not None
            tw = int(ow * (params.height / oh))
            th = params.height
        elif params.height is None:
            tw = params.width
            th = int(oh * (params.width / ow))
        else:
            tw = params.width
            th = params.height
        if params.fit == "fill":
            return image.resize((tw, th), Image.LANCZOS)
        if params.fit == "inside":
            img = image.copy()
            img.thumbnail((tw, th), Image.LANCZOS)
            return img
        if params.fit == "cover":
            return ImageOps.fit(image, (tw, th), method=Image.LANCZOS)
        if params.fit == "contain":
            img = image.copy()
            img.thumbnail((tw, th), Image.LANCZOS)
            bg = Image.new(
                "RGBA" if image.mode == "RGBA" else "RGB",
                (tw, th),
                ImageColor.getrgb(params.background) if image.mode != "RGBA"
                else (*ImageColor.getrgb(params.background), 255),
            )
            ox = (tw - img.size[0]) // 2
            oy = (th - img.size[1]) // 2
            if image.mode == "RGBA":
                bg.paste(img, (ox, oy), img if img.mode == "RGBA" else None)
            else:
                bg.paste(img, (ox, oy))
            return bg
        return image


class ExifStripParams(OpParams):
    pass


@register_op
class ExifStripOp(ImageOp):
    """Apply EXIF orientation then strip all metadata. Privacy-preserving."""
    name = "exif_strip"
    params_model = ExifStripParams
    preserves_alpha = True
    supports_mask = False

    def apply(self, image: Image.Image, mask, params) -> Image.Image:
        # exif_transpose() applies rotation. Returning a new image with no
        # ``info`` dict effectively strips EXIF on encode.
        rotated = ImageOps.exif_transpose(image)
        clean = Image.new(rotated.mode, rotated.size)
        clean.paste(rotated)
        return clean


class PerspectiveParams(OpParams):
    """Four-corner perspective warp. Source corners are the image's
    natural corners (TL, TR, BR, BL); destination corners are the
    pixel coordinates where each should map to."""
    dest_top_left: tuple[float, float]
    dest_top_right: tuple[float, float]
    dest_bottom_right: tuple[float, float]
    dest_bottom_left: tuple[float, float]
    output_width: int | None = None
    output_height: int | None = None


@register_op
class PerspectiveOp(ImageOp):
    name = "perspective"
    params_model = PerspectiveParams
    preserves_alpha = True
    supports_mask = False

    def apply(self, image: Image.Image, mask, params: PerspectiveParams) -> Image.Image:
        w, h = image.size
        ow = params.output_width or w
        oh = params.output_height or h
        src = [
            (0, 0), (w, 0), (w, h), (0, h),
        ]
        dst = [
            tuple(params.dest_top_left),
            tuple(params.dest_top_right),
            tuple(params.dest_bottom_right),
            tuple(params.dest_bottom_left),
        ]
        coeffs = _perspective_coeffs(dst, src)
        return image.transform(
            (ow, oh),
            Image.PERSPECTIVE,
            coeffs,
            resample=Image.BICUBIC,
        )


class PerspectiveCropParams(OpParams):
    """Rectify a quadrilateral region to a flat rectangle (document scan).

    The four corners are pixel coordinates in the source image, in
    **post-EXIF-transpose space** — the orientation a browser displays.
    Callers must apply ``ImageOps.exif_transpose`` before computing or
    consuming these coordinates (``/images/detect-document`` returns
    them in the same space).

    Output size defaults to the quad's max opposing edge lengths so the
    rectified document keeps full source resolution.
    """
    top_left: tuple[float, float]
    top_right: tuple[float, float]
    bottom_right: tuple[float, float]
    bottom_left: tuple[float, float]
    output_width: int | None = None
    output_height: int | None = None


@register_op
class PerspectiveCropOp(ImageOp):
    name = "perspective_crop"
    params_model = PerspectiveCropParams
    preserves_alpha = True
    supports_mask = False

    def apply(self, image: Image.Image, mask, params: PerspectiveCropParams) -> Image.Image:
        import math

        tl = tuple(params.top_left)
        tr = tuple(params.top_right)
        br = tuple(params.bottom_right)
        bl = tuple(params.bottom_left)

        def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
            return math.hypot(a[0] - b[0], a[1] - b[1])

        ow = params.output_width or max(1, round(max(_dist(tl, tr), _dist(bl, br))))
        oh = params.output_height or max(1, round(max(_dist(tl, bl), _dist(tr, br))))
        # PIL PERSPECTIVE coeffs map output coords → source coords, so the
        # output rectangle is the "target" and the quad is the "source".
        coeffs = _perspective_coeffs(
            [(0, 0), (ow, 0), (ow, oh), (0, oh)],
            [tl, tr, br, bl],
        )
        return image.transform(
            (ow, oh),
            Image.PERSPECTIVE,
            coeffs,
            resample=Image.BICUBIC,
        )


def _perspective_coeffs(target_corners, source_corners) -> list[float]:
    """8 perspective coefficients via least-squares on 4 corner pairs."""
    from matrx_files._extras import require

    np = require("numpy", "media", "Perspective correction")
    matrix = []
    for s, t in zip(source_corners, target_corners):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = np.array(matrix, dtype=np.float64)
    B = np.array([c for pair in source_corners for c in pair], dtype=np.float64)
    res = np.linalg.solve(A, B) if A.shape[0] == A.shape[1] else np.linalg.lstsq(A, B, rcond=None)[0]
    return list(res)
