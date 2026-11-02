"""Inpainting via OpenCV (Telea / Navier-Stokes).

OpenCV is an OPTIONAL dependency. Install with the ``image-inpaint`` extra:
``pip install matrx-utils[image-inpaint]``. Without it, the op raises an
actionable error pointing operators at the install command. A naïve
fallback using PIL's Gaussian-blur-fill is intentionally NOT provided
because it produces visibly wrong results; explicit failure is better.

For Wave 2, diffusion-based inpainting (Stable Diffusion / Flux) should
back the same wire shape — the host swaps the dispatcher target without
changing the FE.
"""

from __future__ import annotations

from typing import Literal

from PIL import Image

from .base import ImageOp, OpParams, register_op


def is_opencv_available() -> bool:
    try:
        import cv2  # type: ignore[import-not-found]  # noqa: F401
        return True
    except ImportError:
        return False


class InpaintParams(OpParams):
    method: Literal["telea", "ns"] = "telea"
    radius: int = 3        # inpaint radius in pixels; 1..10 typical


@register_op
class InpaintOp(ImageOp):
    """Content-aware fill within the masked region.

    Mask convention: opaque pixels in the mask = "inpaint this region".
    """
    name = "inpaint"
    params_model = InpaintParams
    preserves_alpha = False  # OpenCV inpaint runs on 3-channel BGR
    supports_mask = True
    requires_mask = True
    compose_with_mask = False  # OpenCV consumes the mask directly

    def apply(self, image: Image.Image, mask, params: InpaintParams) -> Image.Image:
        if mask is None:
            raise ValueError("inpaint requires a mask")
        try:
            import cv2  # type: ignore[import-not-found]
            import numpy as np  # type: ignore[import-not-found]
        except ImportError as e:
            from matrx_files._extras import missing_extra_message

            raise RuntimeError(missing_extra_message("media", e.name or "cv2", "Inpainting")) from e

        rgb = image.convert("RGB")
        src = np.array(rgb)  # H×W×3 RGB
        bgr = src[:, :, ::-1].copy()
        mask_arr = np.array(mask.convert("L"))
        # Pillow uses 0..255; OpenCV expects a binary-ish mask (255 = inpaint).
        # Apply a soft threshold so feathered masks still drive valid inpainting.
        mask_bin = (mask_arr > 0).astype("uint8") * 255

        flags = cv2.INPAINT_TELEA if params.method == "telea" else cv2.INPAINT_NS
        result_bgr = cv2.inpaint(bgr, mask_bin, params.radius, flags)
        result_rgb = result_bgr[:, :, ::-1]
        out = Image.fromarray(result_rgb, "RGB")
        # Preserve source alpha if it had one.
        if image.mode == "RGBA":
            out = out.convert("RGBA")
            out.putalpha(image.split()[-1])
        return out


def inpaint_image(
    image_bytes: bytes,
    mask_bytes: bytes,
    *,
    method: Literal["telea", "ns"] = "telea",
    radius: int = 3,
) -> Image.Image:
    """Functional entry-point for inpainting outside the op registry."""
    from io import BytesIO
    from .base import load_mask_from_png_bytes, normalize_input_image
    src = Image.open(BytesIO(image_bytes))
    src.load()
    src = normalize_input_image(src, want_alpha=False)
    mask = load_mask_from_png_bytes(mask_bytes, target_size=src.size)
    op = InpaintOp()
    return op.apply(src, mask, InpaintParams(method=method, radius=radius))
