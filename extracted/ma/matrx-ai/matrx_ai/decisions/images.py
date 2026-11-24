"""Images beside decision questions — one preparation for every decision route.

A decision's state is its MESSAGE (``translate.py``). When the model reads
images (catalog ``capabilities.input`` has ``image``), the image parts of the
question's message are part of that state too, in the order the author placed
them: image 0, image 1, ... Questions and Box answers name images by that
position, so the same question means the same picture on every route.

* **Native** (TypeSafe Jev): each image's bytes come through the host file
  system (``resolve_media_block`` — we never fetch a URL ourselves), are fitted
  inside Jev's accepted bounds (``processing.vision.fit_for_vision_class``,
  class ``typesafe_jev``), and go on the wire as an asset placed by an opaque
  reference in ``state.images``.
* **Verbalized** (a vision chat model): the image parts simply stay in the
  message, and the chat translator sends them as it sends any image.

The durable identity of each image (its file id, else its url — never bytes
or a signed url) rides the answers as ``DecisionAnswers.images``, so a surface
can draw a Box on the picture it was found in.
"""

from __future__ import annotations

import asyncio
import base64
import binascii
import uuid
from dataclasses import dataclass
from typing import Any

from matrx_ai.decisions.kinds import DecisionImage
from matrx_ai.processing.vision import FittedImage, fit_for_vision_class, resolve_vision_class

__all__ = [
    "DecisionImageError",
    "PreparedDecisionImage",
    "history_image_blocks",
    "image_blocks",
    "require_images_fit_one_request",
    "turn_image_blocks",
    "is_image_block",
    "prepare_decision_images",
    "decision_image_identity",
]


class DecisionImageError(ValueError):
    """An image beside decision questions that cannot be put on the wire."""


def _block_type(block: Any) -> str:
    value = getattr(block, "type", None)
    if value is None and isinstance(block, dict):
        value = block.get("type")
    return str(value or "")


def _field(block: Any, name: str) -> Any:
    if isinstance(block, dict):
        return block.get(name)
    return getattr(block, name, None)


def is_image_block(block: Any) -> bool:
    """An image part: ``image`` / ``input_image``, or a ``media`` part of kind image."""
    block_type = _block_type(block)
    if block_type in ("image", "input_image"):
        return True
    return block_type == "media" and str(_field(block, "kind") or "") == "image"


def image_blocks(message: Any) -> list[Any]:
    """The image parts of one message, in the order the author placed them."""
    return [block for block in (getattr(message, "content", None) or []) if is_image_block(block)]


def history_image_blocks(messages: list[Any], question_index: int) -> list[Any]:
    """Images in the conversation BEFORE the questions — history, sent as such (never
    numbered as image 0, 1, which name the turn's own pictures)."""
    return [block for message in messages[:question_index] for block in image_blocks(message)]


def turn_image_blocks(messages: list[Any], question_index: int) -> list[Any]:
    """The images of the decision TURN: the questions' own message, then every message
    after it (the person's turn after an agent's template — a photo attached when the
    agent runs), in order. Images before the questions are history, as text is."""
    return [block for message in messages[question_index:] for block in image_blocks(message)]


def decision_image_identity(block: Any) -> DecisionImage:
    """The durable handle a surface redraws the picture from: file id, else a real url."""
    file_id = _field(block, "file_id")
    url = _field(block, "url")
    if isinstance(url, str) and url.startswith("data:"):
        url = None
    return DecisionImage(
        file_id=str(file_id) if file_id else None,
        url=str(url) if url and not file_id else None,
        width=_field(block, "width") if isinstance(_field(block, "width"), int) else None,
        height=_field(block, "height") if isinstance(_field(block, "height"), int) else None,
    )


#: All images of one native request, raw bytes after fitting. TypeSafe caps the body at
#: 32 MiB with base64 (~4/3 larger) and the processed images at 32 MiB together, so the
#: raw sum is held well under both; past it the request is refused here, by name, instead
#: of an opaque 413 after upload.
MAX_TOTAL_IMAGE_BYTES = 22 * 1024 * 1024


def require_images_fit_one_request(images: list[PreparedDecisionImage]) -> None:
    total = sum(len(image.fitted.data) for image in images)
    if total > MAX_TOTAL_IMAGE_BYTES:
        raise DecisionImageError(
            f"The {len(images)} images beside the decision questions come to "
            f"{total // (1024 * 1024)} MiB after fitting; one decision request holds about "
            f"{MAX_TOTAL_IMAGE_BYTES // (1024 * 1024)} MiB. Send fewer images or split the questions."
        )


@dataclass(frozen=True)
class PreparedDecisionImage:
    """One image ready for a native decision wire."""

    index: int
    reference: str
    fitted: FittedImage
    identity: DecisionImage

    @property
    def data_base64(self) -> str:
        return base64.b64encode(self.fitted.data).decode("ascii")

    def to_asset(self) -> dict[str, str]:
        return {"type": "image", "format": self.fitted.format, "data_base64": self.data_base64}


async def _image_bytes(block: Any, index: int) -> bytes:
    """The image's bytes: already resolved at the request boundary, else through the file system."""
    data = _field(block, "base64_data")
    if not data:
        from matrx_ai.media.media_blocks import resolve_media_block

        resolved = await resolve_media_block(
            {
                key: value
                for key in ("file_id", "url", "file_uri", "mime_type")
                if (value := _field(block, key))
            },
            access_label="decision_image",
        )
        data = (resolved or {}).get("base64_data")
    if not data:
        raise DecisionImageError(
            f"Image {index} beside the decision questions could not be read: it has no "
            "bytes and its file or url did not resolve. Re-attach the image."
        )
    text = str(data)
    if text.startswith("data:") and "," in text:
        text = text.split(",", 1)[1]
    try:
        return base64.b64decode(text, validate=False)
    except (binascii.Error, ValueError) as exc:
        raise DecisionImageError(f"Image {index} beside the decision questions is not valid base64.") from exc


async def prepare_decision_images(
    blocks: list[Any], *, model: str | None, wire_format: str
) -> list[PreparedDecisionImage]:
    """Resolve, fit and reference every image, in order. Raises by name, never drops one."""
    cls = resolve_vision_class(model, wire_format)
    prepared: list[PreparedDecisionImage] = []
    for index, block in enumerate(blocks):
        raw = await _image_bytes(block, index)
        try:
            # CPU-bound Pillow work never runs on the event loop.
            fitted = await asyncio.to_thread(fit_for_vision_class, raw, cls)
        except ValueError as exc:
            raise DecisionImageError(
                f"Image {index} beside the decision questions cannot be sent: {exc}. "
                "Re-export it as a PNG or JPEG."
            ) from exc
        identity = decision_image_identity(block)
        prepared.append(
            PreparedDecisionImage(
                index=index,
                reference=f"img-{uuid.uuid4().hex}",
                fitted=fitted,
                identity=identity.model_copy(
                    update={"width": fitted.source_width, "height": fitted.source_height}
                ),
            )
        )
    return prepared
