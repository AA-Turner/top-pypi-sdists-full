"""Image edit operations.

Every op registers itself in ``OP_REGISTRY`` at import time via the
``@register_op`` decorator. Importing the package is enough — callers
look up ops by name (``"adjust"``, ``"filter.blur"``, ``"bg_remove"``,
etc.) via ``get_op(name)`` or ``dispatch_op(name, bytes, ...)``.

Optional backends (rembg for ``bg_remove``, opencv for ``inpaint``) are
lazy-imported inside their respective op modules. The dispatcher raises
an actionable error if a backend dep is missing at call time; the
package itself imports cleanly without them.

Quick reference:

    from matrx_files.specific_handlers.image_ops import (
        dispatch_op, list_op_names, get_op, encode_image, OP_REGISTRY,
    )

Public sub-helpers:

    remove_background(image_bytes, params=..., mask_bytes=...) -> PIL.Image
    inpaint_image(image_bytes, mask_bytes, method="telea", radius=3) -> PIL.Image
"""

from .base import (
    OP_REGISTRY,
    ImageOp,
    OpParams,
    OpResult,
    compose_via_mask,
    dispatch_op,
    encode_image,
    get_op,
    list_op_names,
    load_mask_from_png_bytes,
    normalize_input_image,
    register_op,
)

# Importing each module registers its ops in OP_REGISTRY.
from . import adjust as _adjust  # noqa: F401
from . import filter as _filter  # noqa: F401
from . import geometry as _geometry  # noqa: F401
from . import color as _color  # noqa: F401
from . import mask_ops as _mask_ops  # noqa: F401
from . import composite as _composite  # noqa: F401
from . import tone as _tone  # noqa: F401
from . import bg_remove as _bg_remove  # noqa: F401
from . import inpaint as _inpaint  # noqa: F401

from .bg_remove import (
    BgRemoveParams,
    is_rembg_available,
    remove_background,
)
from .inpaint import (
    InpaintParams,
    inpaint_image,
    is_opencv_available,
)
from .detect import detect_document_quad
from .metadata import EXIF_BEARING_FORMATS, read_image_metadata
from .geometry import ASPECT_RATIO_PRESETS


# ---------------------------------------------------------------------------
# Catalog — describe every registered op for the FE.
# Used by GET /images/ops endpoint to render the UI dynamically.
# ---------------------------------------------------------------------------

OP_FAMILIES: dict[str, str] = {
    "adjust": "Color & light adjustments (brightness, contrast, saturation, hue)",
    "auto_levels": "Auto-contrast (clip histogram tails)",
    "auto_color": "Per-channel autocontrast — corrects color casts",
    "equalize": "Histogram equalization",
    "grayscale": "Convert to grayscale",
    "invert": "Invert colors",
    "sepia": "Sepia tone",
    "blur": "Gaussian / box / motion blur",
    "sharpen": "Unsharp mask sharpening",
    "denoise": "Median-filter denoise",
    "vignette": "Edge vignette",
    "grain": "Film grain noise",
    "edge_detect": "Edge detection filter",
    "emboss": "Emboss filter",
    "posterize": "Reduce color depth",
    "solarize": "Solarize (invert above threshold)",
    "curves": "Per-channel tone curves",
    "levels": "Photoshop-style levels (input/output black/white + gamma)",
    "shadows_highlights": "Recover shadows / pull back highlights",
    "white_balance": "Gray-world or neutral-pixel white balance",
    "document_clean": "Remove shadows and uneven lighting from a page photo (scanner clean)",
    "crop": "Crop to a rectangle or aspect-ratio preset",
    "rotate": "Rotate by arbitrary degrees",
    "flip": "Flip horizontal / vertical / both",
    "resize": "Resize (cover / contain / fill / inside)",
    "exif_strip": "Apply orientation and strip metadata",
    "perspective": "Four-corner perspective warp",
    "perspective_crop": "Rectify a quad region to a flat rectangle (document scan)",
    "palette_extract": "Extract dominant colors",
    "color_key": "Make pixels near a color transparent or replace",
    "color_replace": "Replace one color with another",
    "quantize": "Reduce to N-color palette",
    "duotone": "Map shadows/highlights to two colors",
    "mask.from_color_key": "Generate a mask from a color-key",
    "mask.from_alpha": "Lift a source's alpha channel into a mask",
    "mask.feather": "Soften mask edges",
    "mask.grow": "Dilate or erode a mask",
    "mask.invert": "Invert a mask",
    "mask.threshold": "Threshold a feathered mask",
    "mask.smooth_edges": "Clean jagged mask edges",
    "mask.combine": "Union / intersect / difference of two masks",
    "text": "Render text on the image (font / outline / shadow / pill)",
    "shape": "Draw rectangle / ellipse / line / polygon",
    "watermark_plus": "Overlay another image with opacity and anchoring",
    "bg_remove": "Background removal (rembg)",
    "inpaint": "Content-aware fill in masked region (OpenCV)",
}


def op_catalog() -> dict:
    """Machine-readable catalog of every registered op for the FE picker."""
    out: list[dict] = []
    for name in list_op_names():
        OpClass = OP_REGISTRY[name]
        # Pull the params model's JSON schema (minus refs we don't need).
        try:
            schema = OpClass.params_model.model_json_schema()
        except Exception:
            schema = {}
        out.append({
            "name": name,
            "family": name.split(".", 1)[0],
            "description": OP_FAMILIES.get(name, ""),
            "requires_mask": OpClass.requires_mask,
            "supports_mask": OpClass.supports_mask,
            "preserves_alpha": OpClass.preserves_alpha,
            "params_schema": schema,
        })
    return {
        "ops": out,
        "aspect_ratios": ASPECT_RATIO_PRESETS,
        "backends": {
            "rembg": is_rembg_available(),
            "opencv": is_opencv_available(),
        },
    }


__all__ = [
    "OP_REGISTRY",
    "ImageOp",
    "OpParams",
    "OpResult",
    "compose_via_mask",
    "dispatch_op",
    "encode_image",
    "get_op",
    "list_op_names",
    "load_mask_from_png_bytes",
    "normalize_input_image",
    "register_op",
    "BgRemoveParams",
    "InpaintParams",
    "is_rembg_available",
    "is_opencv_available",
    "remove_background",
    "inpaint_image",
    "detect_document_quad",
    "read_image_metadata",
    "EXIF_BEARING_FORMATS",
    "ASPECT_RATIO_PRESETS",
    "OP_FAMILIES",
    "op_catalog",
]
