"""Compositing: text overlay, shape draw, watermark plus, layer paste."""

from __future__ import annotations

from typing import Literal

from PIL import Image, ImageColor, ImageDraw, ImageFont

from .base import ImageOp, OpParams, register_op


# ---------------------------------------------------------------------------
# Font loading
# ---------------------------------------------------------------------------

_FONT_CACHE: dict[tuple[str, int], ImageFont.ImageFont] = {}


def _load_font(family: str | None, size: int) -> ImageFont.ImageFont:
    """Best-effort font loader.

    Tries: requested file path, common system fonts, then Pillow's default.
    Cached by (family, size).
    """
    key = (family or "default", size)
    cached = _FONT_CACHE.get(key)
    if cached is not None:
        return cached

    candidates: list[str] = []
    if family:
        candidates.append(family)
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "DejaVuSans-Bold.ttf",
        "Arial.ttf",
    ]
    for path in candidates:
        try:
            font = ImageFont.truetype(path, size=size)
            _FONT_CACHE[key] = font
            return font
        except OSError:
            continue
    fallback = ImageFont.load_default()
    _FONT_CACHE[key] = fallback
    return fallback


# ---------------------------------------------------------------------------
# Text overlay
# ---------------------------------------------------------------------------

class TextOverlayParams(OpParams):
    text: str
    font_family: str | None = None      # path or filename; falls back to system fonts
    font_size: int = 48
    color: str = "#ffffff"
    # Position: hex anchor + offsets, OR explicit (x, y).
    anchor: Literal[
        "center", "top", "bottom", "left", "right",
        "top-left", "top-right", "bottom-left", "bottom-right",
    ] = "center"
    offset_x: int = 0
    offset_y: int = 0
    x: int | None = None
    y: int | None = None
    # Outline / stroke
    stroke_width: int = 0
    stroke_color: str = "#000000"
    # Drop shadow
    shadow_offset: tuple[int, int] | None = None
    shadow_color: str = "#000000aa"
    shadow_blur: float = 2.0
    # Opacity 0..1
    opacity: float = 1.0
    # Optional background pill for legibility
    background: str | None = None
    background_padding: int = 8
    background_radius: int = 12


@register_op
class TextOverlayOp(ImageOp):
    name = "text"
    params_model = TextOverlayParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: TextOverlayParams) -> Image.Image:
        rgba = image.convert("RGBA") if image.mode != "RGBA" else image.copy()
        layer = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)

        font = _load_font(params.font_family, params.font_size)
        # Pillow >=9.5: textbbox returns full bounding box including descenders.
        bbox = draw.textbbox((0, 0), params.text, font=font, stroke_width=params.stroke_width)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        x, y = _resolve_anchor(rgba.size, (tw, th), params)

        # Background pill, behind shadow + text.
        if params.background:
            pad = params.background_padding
            bg_box = (x - pad, y - pad, x + tw + pad, y + th + pad)
            try:
                draw.rounded_rectangle(
                    bg_box,
                    radius=params.background_radius,
                    fill=_parse_color(params.background),
                )
            except (AttributeError, TypeError):
                draw.rectangle(bg_box, fill=_parse_color(params.background))

        # Drop shadow.
        if params.shadow_offset is not None:
            from PIL import ImageFilter
            sx, sy = params.shadow_offset
            shadow_layer = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(shadow_layer)
            sdraw.text(
                (x + sx - bbox[0], y + sy - bbox[1]),
                params.text,
                font=font,
                fill=_parse_color(params.shadow_color),
            )
            if params.shadow_blur > 0:
                shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(params.shadow_blur))
            layer = Image.alpha_composite(layer, shadow_layer)
            draw = ImageDraw.Draw(layer)

        # Main text + stroke.
        draw.text(
            (x - bbox[0], y - bbox[1]),
            params.text,
            font=font,
            fill=_parse_color(params.color),
            stroke_width=params.stroke_width,
            stroke_fill=_parse_color(params.stroke_color) if params.stroke_width > 0 else None,
        )

        if params.opacity < 1.0:
            alpha = layer.split()[-1].point(lambda v: int(v * max(0.0, min(1.0, params.opacity))))
            layer.putalpha(alpha)

        return Image.alpha_composite(rgba, layer)


def _parse_color(spec: str | None) -> tuple[int, int, int, int]:
    if spec is None:
        return (0, 0, 0, 0)
    parsed = ImageColor.getrgb(spec)
    if len(parsed) == 3:
        return (*parsed, 255)
    return parsed  # type: ignore[return-value]


def _resolve_anchor(
    canvas: tuple[int, int], item: tuple[int, int], p: TextOverlayParams
) -> tuple[int, int]:
    if p.x is not None and p.y is not None:
        return p.x + p.offset_x, p.y + p.offset_y
    cw, ch = canvas
    iw, ih = item
    anchor = p.anchor
    if anchor == "center":
        x, y = (cw - iw) // 2, (ch - ih) // 2
    elif anchor == "top":
        x, y = (cw - iw) // 2, 20
    elif anchor == "bottom":
        x, y = (cw - iw) // 2, ch - ih - 20
    elif anchor == "left":
        x, y = 20, (ch - ih) // 2
    elif anchor == "right":
        x, y = cw - iw - 20, (ch - ih) // 2
    elif anchor == "top-left":
        x, y = 20, 20
    elif anchor == "top-right":
        x, y = cw - iw - 20, 20
    elif anchor == "bottom-left":
        x, y = 20, ch - ih - 20
    elif anchor == "bottom-right":
        x, y = cw - iw - 20, ch - ih - 20
    else:
        x, y = (cw - iw) // 2, (ch - ih) // 2
    return x + p.offset_x, y + p.offset_y


# ---------------------------------------------------------------------------
# Shape draw
# ---------------------------------------------------------------------------

class Point(OpParams):
    x: int
    y: int


class ShapeParams(OpParams):
    shape: Literal["rectangle", "rounded_rect", "ellipse", "line", "polygon"]
    # For rect/ellipse: bbox
    left: int | None = None
    top: int | None = None
    right: int | None = None
    bottom: int | None = None
    # For polygon / line: list of (x, y) points
    points: list[tuple[int, int]] | None = None
    fill: str | None = None
    outline: str | None = None
    width: int = 1                  # stroke width
    radius: int = 12                # for rounded_rect


@register_op
class ShapeDrawOp(ImageOp):
    name = "shape"
    params_model = ShapeParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: ShapeParams) -> Image.Image:
        rgba = image.convert("RGBA") if image.mode != "RGBA" else image.copy()
        draw = ImageDraw.Draw(rgba)
        fill = _parse_color(params.fill) if params.fill else None
        outline = _parse_color(params.outline) if params.outline else None

        if params.shape in ("rectangle", "rounded_rect", "ellipse"):
            if None in (params.left, params.top, params.right, params.bottom):
                raise ValueError(
                    f"{params.shape} requires left/top/right/bottom."
                )
            box = (params.left, params.top, params.right, params.bottom)
            if params.shape == "rectangle":
                draw.rectangle(box, fill=fill, outline=outline, width=params.width)
            elif params.shape == "rounded_rect":
                try:
                    draw.rounded_rectangle(
                        box, radius=params.radius, fill=fill, outline=outline,
                        width=params.width,
                    )
                except AttributeError:
                    draw.rectangle(box, fill=fill, outline=outline, width=params.width)
            else:  # ellipse
                draw.ellipse(box, fill=fill, outline=outline, width=params.width)
        elif params.shape == "line":
            if not params.points or len(params.points) < 2:
                raise ValueError("line requires at least 2 points")
            draw.line([tuple(p) for p in params.points], fill=outline or fill, width=params.width)
        elif params.shape == "polygon":
            if not params.points or len(params.points) < 3:
                raise ValueError("polygon requires at least 3 points")
            draw.polygon([tuple(p) for p in params.points], fill=fill, outline=outline)
        return rgba


# ---------------------------------------------------------------------------
# Watermark plus — base64-encoded overlay image
# ---------------------------------------------------------------------------

class WatermarkParams(OpParams):
    """Place another image over the source. The watermark image is supplied
    as a base64-encoded PNG/JPEG so the op is self-contained (matrx-utils
    cannot resolve cld_files IDs by itself)."""
    overlay_b64: str
    opacity: float = 0.6
    scale: float = 0.25             # fraction of source min(width, height)
    anchor: Literal[
        "center", "top", "bottom", "left", "right",
        "top-left", "top-right", "bottom-left", "bottom-right",
    ] = "bottom-right"
    offset_x: int = 24
    offset_y: int = 24


@register_op
class WatermarkPlusOp(ImageOp):
    name = "watermark_plus"
    params_model = WatermarkParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: WatermarkParams) -> Image.Image:
        import base64
        from io import BytesIO
        rgba = image.convert("RGBA") if image.mode != "RGBA" else image.copy()
        wm_bytes = base64.b64decode(params.overlay_b64)
        wm = Image.open(BytesIO(wm_bytes)).convert("RGBA")

        sw, sh = rgba.size
        scale = max(0.01, min(1.0, params.scale))
        target = int(min(sw, sh) * scale)
        ww, wh = wm.size
        ratio = target / max(ww, wh)
        wm = wm.resize((max(1, int(ww * ratio)), max(1, int(wh * ratio))), Image.LANCZOS)

        if params.opacity < 1.0:
            alpha = wm.split()[-1].point(lambda v: int(v * max(0.0, min(1.0, params.opacity))))
            wm.putalpha(alpha)

        ww, wh = wm.size
        anchor_params = TextOverlayParams(text="", anchor=params.anchor,
                                          offset_x=params.offset_x,
                                          offset_y=params.offset_y)
        x, y = _resolve_anchor(rgba.size, (ww, wh), anchor_params)
        rgba.alpha_composite(wm, (x, y))
        return rgba
