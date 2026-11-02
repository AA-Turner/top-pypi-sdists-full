"""Image-op infrastructure: protocol, params base, registry, mask helpers.

Every image edit operation (adjust, filter, color, geometry, composite,
mask_ops, transform, tone, bg_remove, inpaint) follows the same shape:

  - A Pydantic params model declares the wire shape.
  - A subclass of ``ImageOp`` implements ``apply(image, mask, params)``.
  - The class is registered into ``OP_REGISTRY`` with a stable string key
    so routers and dispatchers can look it up by name.

The host (an aidream router, a workflow node, a CLI) is responsible for
loading the source bytes and the optional mask bytes, calling
``dispatch(op_name, image_bytes, mask_bytes, params_dict)``, and
persisting the result. No piece of this module touches the network, the
database, or the user context — it is pure CPU work on PIL images.

Mask convention (matches the frontend uploader contract):

  - Mask is a PNG (RGBA). Any non-zero alpha pixel is "in mask."
  - Same width/height as the source image.
  - The mask is loaded as a single-channel ``L`` mode image inside the
    op runtime — the alpha channel becomes the mask data.
  - When an op is given a mask, it MUST only modify pixels where the
    mask is non-zero. Outside-mask pixels are copied verbatim from the
    source. ``apply_with_mask()`` is the helper that does this safely.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from io import BytesIO
from typing import Any, ClassVar

from PIL import Image
from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Pydantic base for op params
# ---------------------------------------------------------------------------

class OpParams(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ---------------------------------------------------------------------------
# Result envelope returned by every op
# ---------------------------------------------------------------------------

class OpResult:
    """In-process result. ``image`` is a PIL Image; the caller encodes it."""

    __slots__ = ("image", "info", "preferred_format")

    def __init__(
        self,
        image: Image.Image,
        *,
        info: dict[str, Any] | None = None,
        preferred_format: str | None = None,
    ) -> None:
        self.image = image
        self.info = info or {}
        self.preferred_format = preferred_format


# ---------------------------------------------------------------------------
# Base op
# ---------------------------------------------------------------------------

class ImageOp(ABC):
    """Base for every CPU-bound image operation.

    Subclasses declare:
        name: stable string identifier (e.g. "adjust", "filter.blur")
        params_model: Pydantic class — request body for this op
        preserves_alpha: True when output can keep an alpha channel
        requires_mask: True when the op needs a mask (e.g. inpaint)
        supports_mask: True when an optional mask narrows the effect

    Subclasses implement:
        apply(image, mask, params) -> Image
            - image is mode "RGBA" or "RGB" depending on source.
            - mask is None or a single-channel "L" mode image at the
              same size as ``image``; non-zero = "in mask".
            - return value is a PIL Image; the dispatcher composes it
              back over the source when ``mask`` was supplied and the
              op opted into ``compose_with_mask`` (the default).
    """

    name: ClassVar[str] = ""
    params_model: ClassVar[type[OpParams]] = OpParams
    preserves_alpha: ClassVar[bool] = True
    requires_mask: ClassVar[bool] = False
    supports_mask: ClassVar[bool] = True
    # When True, the dispatcher will copy untouched pixels from the
    # source over the op's output wherever the mask is zero. Set False
    # for ops that need to consume the mask themselves (inpaint,
    # bg_remove with mask intersection, mask_ops).
    compose_with_mask: ClassVar[bool] = True

    @abstractmethod
    def apply(
        self,
        image: Image.Image,
        mask: Image.Image | None,
        params: OpParams,
    ) -> Image.Image:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

OP_REGISTRY: dict[str, type[ImageOp]] = {}


def register_op(cls: type[ImageOp]) -> type[ImageOp]:
    if not cls.name:
        raise ValueError(f"ImageOp subclass {cls.__name__} must declare a non-empty .name")
    if cls.name in OP_REGISTRY:
        raise ValueError(f"Duplicate image op name: {cls.name!r}")
    OP_REGISTRY[cls.name] = cls
    return cls


def get_op(name: str) -> type[ImageOp]:
    try:
        return OP_REGISTRY[name]
    except KeyError as e:
        known = ", ".join(sorted(OP_REGISTRY.keys()))
        raise KeyError(f"Unknown image op {name!r}. Known ops: {known}") from e


def list_op_names() -> list[str]:
    return sorted(OP_REGISTRY.keys())


# ---------------------------------------------------------------------------
# Mask helpers
# ---------------------------------------------------------------------------

def load_mask_from_png_bytes(
    mask_bytes: bytes,
    *,
    target_size: tuple[int, int],
) -> Image.Image:
    """Decode the FE-uploaded mask PNG into a single-channel "L" image.

    Convention:
      - Mask is a PNG with an alpha channel; any non-zero alpha = "in mask".
      - Must match the source image's width/height exactly.

    Returns an "L"-mode image (0 = outside mask, 255 = fully inside, with
    intermediate values acting as a feathered alpha when the mask is
    soft-edged).
    """
    img = Image.open(BytesIO(mask_bytes))
    img.load()
    if img.size != target_size:
        raise ValueError(
            f"Mask size {img.size} does not match source size {target_size}. "
            f"Frontend must upload a mask with identical dimensions."
        )
    # Pull the alpha channel if RGBA, else use the image's own L data.
    if img.mode == "RGBA":
        alpha = img.split()[-1]
        return alpha.convert("L")
    if img.mode == "LA":
        return img.split()[-1].convert("L")
    if img.mode in ("L", "1"):
        return img.convert("L")
    if img.mode in ("RGB",):
        # No alpha — fall back to luminance. Documented in case a caller
        # uploads a non-RGBA mask by mistake; behavior stays predictable.
        return img.convert("L")
    return img.convert("RGBA").split()[-1].convert("L")


def compose_via_mask(
    source: Image.Image,
    edited: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    """Return source pixels where mask=0, edited pixels where mask=255.

    Intermediate mask values blend smoothly (feathered edges). Both
    images must be the same size; the mask is resampled if not.

    The result mode matches the source: an RGBA source yields RGBA;
    an RGB source yields RGB.
    """
    if mask.size != source.size:
        mask = mask.resize(source.size, Image.LANCZOS)
    if edited.size != source.size:
        edited = edited.resize(source.size, Image.LANCZOS)
    src_mode = source.mode
    if src_mode != edited.mode:
        edited = edited.convert(src_mode)
    return Image.composite(edited, source, mask)


def normalize_input_image(image: Image.Image, *, want_alpha: bool) -> Image.Image:
    """Ensure the input is in a mode the ops can rely on.

    EXIF rotation is applied so width/height are intuitive. When
    ``want_alpha`` is True the image is promoted to RGBA, otherwise to
    RGB.
    """
    from PIL import ImageOps
    image = ImageOps.exif_transpose(image)
    if want_alpha:
        if image.mode != "RGBA":
            image = image.convert("RGBA")
    else:
        if image.mode not in ("RGB", "L"):
            # Flatten alpha onto white for JPEG-friendly modes.
            if image.mode == "RGBA":
                bg = Image.new("RGB", image.size, (255, 255, 255))
                bg.paste(image, mask=image.split()[-1])
                image = bg
            else:
                image = image.convert("RGB")
    return image


# ---------------------------------------------------------------------------
# Encoding helpers
# ---------------------------------------------------------------------------

def encode_image(
    image: Image.Image,
    *,
    format: str = "png",
    quality: int = 90,
    background: tuple[int, int, int] = (255, 255, 255),
) -> tuple[bytes, str]:
    """Encode a PIL image to bytes + mime_type. Flattens alpha when needed.

    Returns (bytes, mime_type). Supported formats: png, jpeg, webp, avif.
    """
    fmt = format.lower()
    if fmt == "jpg":
        fmt = "jpeg"
    if fmt not in ("png", "jpeg", "webp", "avif"):
        raise ValueError(f"Unsupported encode format: {format!r}")

    buf = BytesIO()
    save_image = image
    if fmt == "jpeg":
        # JPEG can't carry alpha — flatten over background.
        if save_image.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", save_image.size, background)
            bg.paste(save_image, mask=save_image.split()[-1])
            save_image = bg
        elif save_image.mode != "RGB":
            save_image = save_image.convert("RGB")
        save_image.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        return buf.getvalue(), "image/jpeg"
    if fmt == "png":
        if save_image.mode == "P":
            save_image = save_image.convert("RGBA")
        save_image.save(buf, "PNG", optimize=True)
        return buf.getvalue(), "image/png"
    if fmt == "webp":
        save_image.save(buf, "WEBP", quality=quality, method=6)
        return buf.getvalue(), "image/webp"
    if fmt == "avif":
        save_image.save(buf, "AVIF", quality=quality)
        return buf.getvalue(), "image/avif"
    raise ValueError(f"Unsupported encode format: {format!r}")


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def dispatch_op(
    op_name: str,
    image_bytes: bytes,
    *,
    mask_bytes: bytes | None,
    params_dict: dict[str, Any],
) -> OpResult:
    """Run an op end-to-end on raw bytes.

    The dispatcher:
      1. Decodes the source bytes.
      2. Normalizes the input mode based on the op's ``preserves_alpha``.
      3. Decodes the mask (if supplied) and validates the size.
      4. Constructs the op params from the params model.
      5. Calls ``op.apply(image, mask, params)``.
      6. If ``compose_with_mask`` is True and a mask is present, composes
         the op output back over the source via the mask.

    This function is synchronous — call it from inside
    ``loop.run_in_executor(None, dispatch_op, ...)`` so the event loop
    doesn't block on CPU work.
    """
    OpClass = get_op(op_name)
    op = OpClass()

    if OpClass.requires_mask and mask_bytes is None:
        raise ValueError(f"Op {op_name!r} requires a mask but none was provided.")
    if not OpClass.supports_mask and mask_bytes is not None:
        raise ValueError(f"Op {op_name!r} does not accept a mask.")

    source = Image.open(BytesIO(image_bytes))
    source.load()
    source = normalize_input_image(source, want_alpha=OpClass.preserves_alpha)

    mask: Image.Image | None = None
    if mask_bytes is not None:
        mask = load_mask_from_png_bytes(mask_bytes, target_size=source.size)

    params = OpClass.params_model.model_validate(params_dict)
    edited = op.apply(source, mask, params)

    if mask is not None and OpClass.compose_with_mask:
        edited = compose_via_mask(source, edited, mask)

    return OpResult(image=edited)
