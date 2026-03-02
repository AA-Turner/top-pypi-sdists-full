"""High-level SAM3 SDK clients."""

from __future__ import annotations

import base64
import io
import os
from typing import Any

import httpx

from plato.sam3.models import BatchResult, PredictionResult

_DEFAULT_SAM3_URL = "http://sam3:8100"

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
) -> dict[str, Any]:
    return {
        "image": _encode_image(image),
        "prompt": prompt,
        "confidence_threshold": confidence_threshold,
        "boxes": boxes,
        "box_labels": box_labels,
    }


class Sam3ServerError(Exception):
    """Raised when the SAM3 server is unreachable or unhealthy."""


def _wrap_connection_error(exc: Exception, base_url: str) -> Sam3ServerError:
    """Convert connection errors to a clear user-facing message."""
    return Sam3ServerError(
        f"SAM3 server is not running at {base_url}. "
        f"Make sure the server is up (e.g. python serve.py). "
        f"Original error: {exc}"
    )


class Sam3:
    """Synchronous SAM3 client."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 120.0,
    ):
        self._base_url = (base_url or os.environ.get("SAM3_BASE_URL") or _DEFAULT_SAM3_URL).rstrip("/")
        self._client = httpx.Client(base_url=self._base_url, timeout=timeout)

    # -- Predictions --

    def predict(
        self,
        image: ImageInput | list[ImageInput],
        prompt: str,
        confidence_threshold: float = 0.5,
        boxes: list[list[float]] | None = None,
        box_labels: list[bool] | None = None,
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
        """
        if isinstance(image, list):
            queries = [
                {
                    "image": img,
                    "prompt": prompt,
                    "confidence_threshold": confidence_threshold,
                    "boxes": boxes,
                    "box_labels": box_labels,
                }
                for img in image
            ]
            return self.predict_batch(queries)
        query = _build_query(image, prompt, confidence_threshold, boxes, box_labels)
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
                     boxes (optional), box_labels (optional).
        """
        encoded = [
            _build_query(
                image=q["image"],
                prompt=q["prompt"],
                confidence_threshold=q.get("confidence_threshold", 0.5),
                boxes=q.get("boxes"),
                box_labels=q.get("box_labels"),
            )
            for q in queries
        ]
        try:
            resp = self._client.post("/predict/batch", json={"queries": encoded})
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return BatchResult.model_validate(resp.json())

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

    def __enter__(self) -> Sam3:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncSam3:
    """Asynchronous SAM3 client."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 120.0,
    ):
        self._base_url = (base_url or os.environ.get("SAM3_BASE_URL") or _DEFAULT_SAM3_URL).rstrip("/")
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=timeout)

    # -- Predictions --

    async def predict(
        self,
        image: ImageInput | list[ImageInput],
        prompt: str,
        confidence_threshold: float = 0.5,
        boxes: list[list[float]] | None = None,
        box_labels: list[bool] | None = None,
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
                }
                for img in image
            ]
            return await self.predict_batch(queries)
        query = _build_query(image, prompt, confidence_threshold, boxes, box_labels)
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
            )
            for q in queries
        ]
        try:
            resp = await self._client.post("/predict/batch", json={"queries": encoded})
        except httpx.ConnectError as exc:
            raise _wrap_connection_error(exc, self._base_url) from exc
        resp.raise_for_status()
        return BatchResult.model_validate(resp.json())

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

    async def __aenter__(self) -> AsyncSam3:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
