"""The one Replicate client for image and video generation, and how a prediction is waited on.

A Replicate image or video prediction runs for seconds to many minutes. ``replicate.async_run``
creates it with ``Prefer: wait`` (the POST is held open until the output is ready) and the library
gives that one request its OWN read window of 60.5 s, overriding the client's timeout. A video
render outlasts it, so the create POST raised ``httpx.ReadTimeout`` while the prediction kept
running (and billing) on Replicate; the timeout was classified as a text-model timeout ("very long
prompts or high token limits") and retried, buying the render again. Live 2026-11-16: podcast
``video_0`` (system_error fd9ee1bb), both its model and the fallback.

So a prediction is CREATED without ``Prefer: wait`` (the POST returns at once with an id), then
POLLED to a terminal state under a per-modality deadline that is a knob
(``ai.media_providers.replicate_{image,video}_deadline_seconds``). Past the deadline the
prediction is cancelled at Replicate and the failure names what happened. The client keeps a
generous read window for the create itself (reference media upload on a busy provider).
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
import replicate

REPLICATE_CREATE_READ_TIMEOUT_S: float = 120.0

REPLICATE_HTTP_TIMEOUT = httpx.Timeout(
    5.0,
    read=REPLICATE_CREATE_READ_TIMEOUT_S,
    write=60.0,
    connect=5.0,
    pool=10.0,
)

REPLICATE_DEADLINE_FEATURE = "ai.media_providers"
#: KNOB MIRROR of platform.feature_knob "ai.media_providers" "replicate_image_deadline_seconds"
REPLICATE_IMAGE_DEADLINE_MIRROR = 600.0
#: KNOB MIRROR of platform.feature_knob "ai.media_providers" "replicate_video_deadline_seconds"
REPLICATE_VIDEO_DEADLINE_MIRROR = 1800.0
REPLICATE_POLL_INTERVAL_S: float = 2.0

_TERMINAL = frozenset({"succeeded", "failed", "canceled"})

_client: replicate.Client | None = None


def get_replicate_client() -> replicate.Client:
    """Process-wide client (token from REPLICATE_API_TOKEN, like the stock one)."""
    global _client
    if _client is None:
        _client = replicate.Client(timeout=REPLICATE_HTTP_TIMEOUT)
    return _client


def replicate_deadline_seconds(modality: str) -> float:
    """How long a Replicate prediction of this modality may run before it is cancelled (live knob)."""
    from matrx_ai.knobs import package_knob_number

    if modality == "video":
        return package_knob_number(
            REPLICATE_DEADLINE_FEATURE, "replicate_video_deadline_seconds",
            REPLICATE_VIDEO_DEADLINE_MIRROR, low=60.0, high=7200.0,
        )
    return package_knob_number(
        REPLICATE_DEADLINE_FEATURE, "replicate_image_deadline_seconds",
        REPLICATE_IMAGE_DEADLINE_MIRROR, low=30.0, high=3600.0,
    )


class ReplicatePredictionTimeout(TimeoutError):
    """A Replicate prediction did not finish inside its deadline (it was cancelled at Replicate)."""

    def __init__(self, *, prediction_id: str, modality: str, ref: str, deadline_s: float, status: str):
        self.prediction_id = prediction_id
        self.modality = modality
        self.ref = ref
        self.deadline_s = deadline_s
        self.status = status
        super().__init__(
            f"Replicate {modality} prediction {prediction_id} ({ref}) was still {status!r} after "
            f"{deadline_s:.0f}s (ai.media_providers.replicate_{modality}_deadline_seconds); cancelled"
        )
        from matrx_ai.providers.errors import RetryableError

        self.error_info = RetryableError(
            error_type="media_generation_timeout",
            message=str(self),
            status_code=504,
            is_retryable=False,
            user_message=(
                f"The {modality} took longer than {deadline_s / 60:.0f} minutes to generate "
                "and was stopped."
            ),
            details={
                "provider": "replicate",
                "modality": modality,
                "prediction_id": prediction_id,
                "deadline_seconds": deadline_s,
                "last_status": status,
            },
        )


async def create_prediction(client: replicate.Client, ref: str, model_input: dict[str, Any]) -> Any:
    """Create a prediction WITHOUT ``Prefer: wait`` — the POST returns as soon as it is queued."""
    from replicate import identifier

    version, owner, name, version_id = identifier._resolve(ref)
    if version or version_id:
        return await client.predictions.async_create(
            version=(version or version_id), input=model_input, wait=False
        )
    if owner and name:
        return await client.models.predictions.async_create(
            model=(owner, name), input=model_input, wait=False
        )
    raise ValueError(f"Invalid Replicate model reference {ref!r} (expected owner/name[:version])")


async def await_prediction(
    prediction: Any,
    *,
    modality: str,
    ref: str,
    deadline_s: float | None = None,
    poll_interval_s: float | None = None,
    sleep: Callable[[float], Awaitable[Any]] = asyncio.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> Any:
    """Poll a created prediction to a terminal state; return its output as file objects.

    ``failed`` raises the library's ``ModelError`` (classified as before); ``canceled`` raises;
    past the deadline the prediction is cancelled and ``ReplicatePredictionTimeout`` is raised.
    """
    from replicate.exceptions import ModelError
    from replicate.helpers import transform_output

    deadline = replicate_deadline_seconds(modality) if deadline_s is None else deadline_s
    interval = REPLICATE_POLL_INTERVAL_S if poll_interval_s is None else poll_interval_s
    started = clock()
    while prediction.status not in _TERMINAL:
        if clock() - started >= deadline:
            try:
                await prediction.async_cancel()
            except Exception as exc:  # noqa: BLE001 — the timeout is the failure; the cancel is said
                print(f"[replicate] cancel of {prediction.id} after deadline failed: {exc!r}")
            raise ReplicatePredictionTimeout(
                prediction_id=str(prediction.id), modality=modality, ref=ref,
                deadline_s=deadline, status=str(prediction.status),
            )
        await sleep(interval)
        await prediction.async_reload()

    if prediction.status == "failed":
        raise ModelError(prediction)
    if prediction.status == "canceled":
        raise RuntimeError(f"Replicate {modality} prediction {prediction.id} ({ref}) was canceled")
    return transform_output(prediction.output, prediction._client)
