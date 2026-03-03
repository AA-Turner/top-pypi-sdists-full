"""High-level segmentation SDK clients."""

from __future__ import annotations

import base64
import io
import os
from typing import Any

import httpx

from plato.segmentation.models import BatchResult, PredictionResult, UIParseResult

_DEFAULT_URL = "http://sam3:8100"

ImageInput = str | bytes | Any  # str path, raw bytes, PIL.Image, np.ndarray


def _encode_image(image: ImageInput) -> str:
    """Encode an image to base64 string."""
    if isinstance(image, str):
        with open(image, "rb") as f:
            return base64.b64encode(f.read()).decode()
    if isinstance(image, bytes):
        return base64.b64encode(image).decode()
    # PIL.Image or numpy array
    try:
        import numpy as np
        from PIL import Image

        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        if isinstance(image, Image.Image):
            buf = io.BytesIO()
            image.save(buf, format="PNG")
            return base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        pass
    raise TypeError(f"Unsupported image type: {type(image)}")


def _build_query(
    image: ImageInput,
    prompt: str,
    confidence_threshold: float = 0.5,
    boxes: list[list[float]] | None = None,
    box_labels: list[bool] | None = None,
    return_masks: bool = True,
) -> dict[str, Any]:
    return {
        "image": _encode_image(image),
        "prompt": prompt,
        "confidence_threshold": confidence_threshold,
        "boxes": boxes,
        "box_labels": box_labels,
        "return_masks": return_masks,
    }


class SegmentationServerError(Exception):
    """Raised when the segmentation server is unreachable or unhealthy."""


def _wrap_connection_error(exc: Exception, base_url: str) -> SegmentationServerError:
    """Convert connection errors to a clear user-facing message."""
    return SegmentationServerError(
        f"Segmentation server is not running at {base_url}. "
        f"Make sure the server is up (e.g. python serve.py). "
        f"Original error: {exc}"
    )


class Segmentation:
    """Synchronous segmentation client (SAM3 + OmniParser)."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 120.0,
    ):
        self._base_url = (base_url or os.environ.get("SEGMENTATION_BASE_URL") or _DEFAULT_URL).rstrip("/")
        self._client = httpx.Client(base_url=self._base_url, timeout=timeout)

    # -- Predictions --

    def predict(
        self,
        image: ImageInput | list[ImageInput],
        prompt: str,
        confidence_threshold: float = 0.5,
        boxes: list[list[float]] | None = None,
        box_labels: list[bool] | None = None,
        return_masks: bool = True,
    ) -> PredictionResult | BatchResult:
        """Run a text-prompted prediction.

        Args:
            image: File path, bytes, PIL Image, numpy array, **or a list** of
                any of these.  When a list is passed the call is automatically
                dispatched to :meth:`predict_batch` using the same *prompt* and
                *confidence_threshold* for every image.
            prompt: Text prompt describing what to segment.
            confidence_threshold: Minimum confidence score (0-1).
            boxes: Optional bounding boxes [[x0,y0,x1,y1], ...] in pixel coords.
            box_labels: Optional label per box (True=positive, False=negative).
            return_masks: Whether to return segmentation masks (default True).
                Set to False for boxes-only mode.
        """
        if isinstance(image, list):
            queries = [
                {
                    "image": img,
                    "prompt": prompt,
                    "confidence_threshold": confidence_threshold,
                    "boxes": boxes,
                    "box_labels": box_labels,
                    "return_masks": return_masks,
                }
                for img in image
            ]
            return self.predict_batch(queries)
        query = _build_query(image, prompt, confidence_threshold, boxes, box_labels, return_masks)
        try:
            resp = self._client.post("/predict/text", json=query)
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return PredictionResult.model_validate(resp.json())

    def predict_batch(
        self,
        queries: list[dict[str, Any]],
    ) -> BatchResult:
        """Run batched predictions in a single forward pass.

        Args:
            queries: List of dicts with keys: image, prompt, confidence_threshold (optional),
                     boxes (optional), box_labels (optional), return_masks (optional).
        """
        encoded = [
            _build_query(
                image=q["image"],
                prompt=q["prompt"],
                confidence_threshold=q.get("confidence_threshold", 0.5),
                boxes=q.get("boxes"),
                box_labels=q.get("box_labels"),
                return_masks=q.get("return_masks", True),
            )
            for q in queries
        ]
        try:
            resp = self._client.post("/predict/batch", json={"queries": encoded})
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return BatchResult.model_validate(resp.json())

    # -- UI Parsing (OmniParser) --

    def parse_ui(
        self,
        image: ImageInput,
        box_threshold: float = 0.05,
        iou_threshold: float = 0.1,
        imgsz: int = 640,
    ) -> UIParseResult:
        """Parse UI elements from a screenshot using OmniParser.

        Args:
            image: File path, bytes, PIL Image, or numpy array.
            box_threshold: Minimum YOLO confidence for icon detection.
            iou_threshold: IoU threshold for deduplication.
            imgsz: YOLO input image size.
        """
        payload = {
            "image": _encode_image(image),
            "box_threshold": box_threshold,
            "iou_threshold": iou_threshold,
            "imgsz": imgsz,
        }
        try:
            resp = self._client.post("/parse/ui", json=payload)
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return UIParseResult.model_validate(resp.json())

    # -- Health --

    def health(self) -> dict[str, Any]:
        try:
            resp = self._client.get("/health")
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return resp.json()

    # -- Lifecycle --

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Segmentation:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncSegmentation:
    """Asynchronous segmentation client (SAM3 + OmniParser)."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 120.0,
    ):
        self._base_url = (base_url or os.environ.get("SEGMENTATION_BASE_URL") or _DEFAULT_URL).rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=timeout)

    # -- Predictions --

    async def predict(
        self,
        image: ImageInput | list[ImageInput],
        prompt: str,
        confidence_threshold: float = 0.5,
        boxes: list[list[float]] | None = None,
        box_labels: list[bool] | None = None,
        return_masks: bool = True,
    ) -> PredictionResult | BatchResult:
        """Run a text-prompted prediction (single or list of images)."""
        if isinstance(image, list):
            queries = [
                {
                    "image": img,
                    "prompt": prompt,
                    "confidence_threshold": confidence_threshold,
                    "boxes": boxes,
                    "box_labels": box_labels,
                    "return_masks": return_masks,
                }
                for img in image
            ]
            return await self.predict_batch(queries)
        query = _build_query(image, prompt, confidence_threshold, boxes, box_labels, return_masks)
        try:
            resp = await self._client.post("/predict/text", json=query)
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return PredictionResult.model_validate(resp.json())

    async def predict_batch(
        self,
        queries: list[dict[str, Any]],
    ) -> BatchResult:
        """Run batched predictions in a single forward pass."""
        encoded = [
            _build_query(
                image=q["image"],
                prompt=q["prompt"],
                confidence_threshold=q.get("confidence_threshold", 0.5),
                boxes=q.get("boxes"),
                box_labels=q.get("box_labels"),
                return_masks=q.get("return_masks", True),
            )
            for q in queries
        ]
        try:
            resp = await self._client.post("/predict/batch", json={"queries": encoded})
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return BatchResult.model_validate(resp.json())

    # -- UI Parsing (OmniParser) --

    async def parse_ui(
        self,
        image: ImageInput,
        box_threshold: float = 0.05,
        iou_threshold: float = 0.1,
        imgsz: int = 640,
    ) -> UIParseResult:
        """Parse UI elements from a screenshot using OmniParser."""
        payload = {
            "image": _encode_image(image),
            "box_threshold": box_threshold,
            "iou_threshold": iou_threshold,
            "imgsz": imgsz,
        }
        try:
            resp = await self._client.post("/parse/ui", json=payload)
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return UIParseResult.model_validate(resp.json())

    # -- Health --

    async def health(self) -> dict[str, Any]:
        try:
            resp = await self._client.get("/health")
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return resp.json()

    # -- Lifecycle --

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncSegmentation:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
