"""Color operations: palette extraction, color-key select, color replace, quantize."""

from __future__ import annotations

from collections import Counter
from typing import Literal

from PIL import Image, ImageColor

from .base import ImageOp, OpParams, register_op


class PaletteExtractParams(OpParams):
    colors: int = 8                 # number of dominant colors to return
    method: Literal["median_cut", "fast"] = "median_cut"


class PaletteExtractResultMixin:
    """Carries the extracted palette as info on the result image.

    The image returned by ``apply()`` is the source itself (the op
    doesn't visually edit anything), but the dispatcher attaches the
    palette to the output info dict via the ``palette`` attribute on
    the op instance.
    """
    palette: list[dict] | None = None


@register_op
class PaletteExtractOp(ImageOp, PaletteExtractResultMixin):
    name = "palette_extract"
    params_model = PaletteExtractParams
    preserves_alpha = True
    supports_mask = True
    compose_with_mask = False  # we don't change pixels

    def apply(self, image: Image.Image, mask, params: PaletteExtractParams) -> Image.Image:
        n = max(1, min(64, params.colors))
        if params.method == "median_cut":
            quantized = image.convert("RGB").quantize(colors=n, method=Image.Quantize.MEDIANCUT)
            pal = quantized.getpalette() or []
            counts = Counter(quantized.getdata())
            total = sum(counts.values()) or 1
            self.palette = []
            for idx, count in counts.most_common(n):
                r, g, b = pal[idx * 3:idx * 3 + 3]
                self.palette.append({
                    "rgb": [r, g, b],
                    "hex": f"#{r:02x}{g:02x}{b:02x}",
                    "weight": count / total,
                })
        else:
            # Fast: nearest-neighbor count of downsampled pixels.
            small = image.convert("RGB").resize((64, 64), Image.LANCZOS)
            counts = Counter(small.getdata())
            total = sum(counts.values()) or 1
            self.palette = [
                {
                    "rgb": list(rgb),
                    "hex": "#{:02x}{:02x}{:02x}".format(*rgb),
                    "weight": count / total,
                }
                for rgb, count in counts.most_common(n)
            ]
        return image  # unchanged


class ColorKeyParams(OpParams):
    """Generate a mask from pixels close to a target color (chroma-key style).

    The op replaces matching pixels — outside-mask if a mask was given,
    everywhere otherwise — with ``replacement`` color or transparency.
    Use ``mask_ops/from_color_key`` if you only want the mask itself.
    """
    target_color: str               # hex color, e.g. "#00ff00"
    tolerance: int = 32             # 0..200 — RGB Euclidean distance
    replacement: str = "transparent"  # hex or "transparent"
    feather: int = 0                # px feathering on the generated mask


@register_op
class ColorKeyOp(ImageOp):
    name = "color_key"
    params_model = ColorKeyParams
    preserves_alpha = True
    compose_with_mask = False  # op handles mask combination itself

    def apply(self, image: Image.Image, mask, params: ColorKeyParams) -> Image.Image:
        rgba = image.convert("RGBA")
        from .mask_ops import generate_mask_from_color_key
        gen_mask = generate_mask_from_color_key(
            rgba, params.target_color, tolerance=params.tolerance, feather=params.feather,
        )
        if mask is not None:
            # Limit replacement to the intersection of the user mask and the
            # color-key mask. Pixels in BOTH get replaced.
            from PIL import ImageChops
            gen_mask = ImageChops.multiply(gen_mask, mask)
        if params.replacement.lower() == "transparent":
            # Subtract the mask from existing alpha.
            r, g, b, a = rgba.split()
            from PIL import ImageChops
            a = ImageChops.subtract(a, gen_mask)
            return Image.merge("RGBA", (r, g, b, a))
        # Replace with a solid color.
        try:
            rgb = ImageColor.getrgb(params.replacement)
        except ValueError as e:
            raise ValueError(f"Bad replacement color {params.replacement!r}: {e}") from e
        fill = Image.new("RGBA", rgba.size, (*rgb, 255))
        return Image.composite(fill, rgba, gen_mask)


class ColorReplaceParams(OpParams):
    target_color: str
    replacement_color: str
    tolerance: int = 32
    feather: int = 0


@register_op
class ColorReplaceOp(ImageOp):
    name = "color_replace"
    params_model = ColorReplaceParams
    preserves_alpha = True
    compose_with_mask = False

    def apply(self, image: Image.Image, mask, params: ColorReplaceParams) -> Image.Image:
        rgba = image.convert("RGBA")
        from .mask_ops import generate_mask_from_color_key
        gen_mask = generate_mask_from_color_key(
            rgba, params.target_color, tolerance=params.tolerance, feather=params.feather,
        )
        if mask is not None:
            from PIL import ImageChops
            gen_mask = ImageChops.multiply(gen_mask, mask)
        try:
            rgb = ImageColor.getrgb(params.replacement_color)
        except ValueError as e:
            raise ValueError(f"Bad replacement color: {e}") from e
        fill = Image.new("RGBA", rgba.size, (*rgb, 255))
        return Image.composite(fill, rgba, gen_mask)


class QuantizeParams(OpParams):
    colors: int = 16
    dither: bool = True


@register_op
class QuantizeOp(ImageOp):
    name = "quantize"
    params_model = QuantizeParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: QuantizeParams) -> Image.Image:
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        work = image.convert("RGB") if image.mode != "RGB" else image
        n = max(2, min(256, params.colors))
        dither = Image.Dither.FLOYDSTEINBERG if params.dither else Image.Dither.NONE
        out = work.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=dither).convert("RGB")
        if alpha is not None:
            out = out.convert("RGBA")
            out.putalpha(alpha)
        return out


class DuotoneParams(OpParams):
    shadow: str = "#1f2937"   # dark color for shadows
    highlight: str = "#fef3c7"  # light color for highlights


@register_op
class DuotoneOp(ImageOp):
    name = "duotone"
    params_model = DuotoneParams
    preserves_alpha = True

    def apply(self, image: Image.Image, mask, params: DuotoneParams) -> Image.Image:
        from PIL import ImageOps
        alpha = image.split()[-1] if image.mode == "RGBA" else None
        gs = ImageOps.grayscale(image)
        try:
            black = ImageColor.getrgb(params.shadow)
            white = ImageColor.getrgb(params.highlight)
        except ValueError as e:
            raise ValueError(f"Bad duotone color: {e}") from e
        colored = ImageOps.colorize(gs, black=black, white=white)
        if alpha is not None:
            colored = colored.convert("RGBA")
            colored.putalpha(alpha)
        return colored
