"""Background removal via rembg.

rembg is an OPTIONAL dependency. Install with the ``image-segmentation``
extra: ``pip install matrx-utils[image-segmentation]``. The first call
downloads the ONNX model (~170 MB for u2net) to ``~/.u2net/``.

If rembg is missing, calling this op raises an actionable RuntimeError
that tells the operator how to install. The matrx-utils package itself
still imports cleanly.
"""

from __future__ import annotations

from io import BytesIO
from typing import Literal

from PIL import Image, ImageChops

from .base import ImageOp, OpParams, register_op


# Lazy module-level cache for rembg session — model load is expensive.
_REMBG_SESSION: object | None = None
_REMBG_MODEL_NAME: str | None = None


def _get_rembg_session(model: str):
    global _REMBG_SESSION, _REMBG_MODEL_NAME
    if _REMBG_SESSION is not None and _REMBG_MODEL_NAME == model:
        return _REMBG_SESSION
    try:
        from rembg import new_session  # type: ignore[import-not-found]
    except ImportError as e:
        from matrx_files._extras import missing_extra_message

        raise RuntimeError(missing_extra_message("media", "rembg", "Background removal")) from e
    _REMBG_SESSION = new_session(model)
    _REMBG_MODEL_NAME = model
    return _REMBG_SESSION


def is_rembg_available() -> bool:
    try:
        import rembg  # noqa: F401  # type: ignore[import-not-found]
        return True
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# Params
# ---------------------------------------------------------------------------

class BgRemoveParams(OpParams):
    # Model selection. u2net is the default; isnet/birefnet are more accurate
    # at higher cost. silueta is the smallest. u2netp is the lightweight u2net.
    model: Literal[
        "u2net",
        "u2netp",
        "u2net_human_seg",
        "u2net_cloth_seg",
        "silueta",
        "isnet-general-use",
        "isnet-anime",
        "birefnet-general",
        "birefnet-portrait",
    ] = "u2net"
    # Alpha matting refines edges — slower but cleaner hair/fur.
    alpha_matting: bool = False
    alpha_matting_foreground_threshold: int = 240
    alpha_matting_background_threshold: int = 10
    alpha_matting_erode_size: int = 10
    # Replace removed background with a solid color or a tiled image.
    background_color: str | None = None  # hex (e.g. "#ffffff") — None = transparent
    # Output edge cleanup.
    post_process_mask: bool = True


def remove_background(
    image_bytes: bytes,
    *,
    params: BgRemoveParams | None = None,
    mask_bytes: bytes | None = None,
) -> Image.Image:
    """Core bg-removal primitive — callable outside the ImageOp protocol.

    When ``mask_bytes`` is supplied, the mask is OR'd into the rembg alpha
    output: pixels marked in the mask stay opaque even if rembg would have
    removed them. Semantics: "definitely foreground, never strip these."
    """
    from matrx_files._extras import require

    rembg_remove = require("rembg", "media", "Background removal").remove
    p = params or BgRemoveParams()
    session = _get_rembg_session(p.model)
    out_bytes = rembg_remove(
        image_bytes,
        session=session,
        alpha_matting=p.alpha_matting,
        alpha_matting_foreground_threshold=p.alpha_matting_foreground_threshold,
        alpha_matting_background_threshold=p.alpha_matting_background_threshold,
        alpha_matting_erode_size=p.alpha_matting_erode_size,
        post_process_mask=p.post_process_mask,
    )
    cut = Image.open(BytesIO(out_bytes)).convert("RGBA")

    if mask_bytes is not None:
        from .base import load_mask_from_png_bytes
        keep = load_mask_from_png_bytes(mask_bytes, target_size=cut.size)
        # Force every "keep" pixel to fully opaque alpha by OR'ing into alpha.
        r, g, b, a = cut.split()
        a = ImageChops.lighter(a, keep)
        cut = Image.merge("RGBA", (r, g, b, a))
        # Also restore original color in the kept region (rembg may have
        # zeroed RGB outside the mask). Pull the source RGB back in.
        src = Image.open(BytesIO(image_bytes)).convert("RGBA")
        if src.size != cut.size:
            src = src.resize(cut.size, Image.LANCZOS)
        cut = Image.composite(src, cut, keep)

    if p.background_color:
        from PIL import ImageColor
        bg = Image.new("RGBA", cut.size, (*ImageColor.getrgb(p.background_color), 255))
        cut = Image.alpha_composite(bg, cut)
    return cut


@register_op
class BgRemoveOp(ImageOp):
    """Op-registry entry — accessible via the unified /images/edit endpoint."""
    name = "bg_remove"
    params_model = BgRemoveParams
    preserves_alpha = True
    supports_mask = True
    compose_with_mask = False  # we handle mask intersection ourselves

    def apply(self, image: Image.Image, mask, params: BgRemoveParams) -> Image.Image:
        # Convert PIL image back to bytes for the rembg call (rembg works
        # on bytes for best perf with its ONNX runtime).
        from io import BytesIO
        buf = BytesIO()
        image.save(buf, "PNG")
        mask_bytes: bytes | None = None
        if mask is not None:
            mbuf = BytesIO()
            # Encode the L mask as RGBA PNG (white-on-transparent) to match
            # the standard mask wire format used everywhere else.
            from PIL import Image as PImage
            rgba = PImage.new("RGBA", mask.size, (255, 255, 255, 0))
            white = PImage.new("RGBA", mask.size, (255, 255, 255, 255))
            rgba = PImage.composite(white, rgba, mask)
            rgba.save(mbuf, "PNG")
            mask_bytes = mbuf.getvalue()
        return remove_background(buf.getvalue(), params=params, mask_bytes=mask_bytes)
