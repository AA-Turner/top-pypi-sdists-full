"""Client for the controller's media-extract endpoint (transcription, OCR).

The SDK never talks to the voice or functions services directly - a self-hosted
worker has no route to them - so every conversion goes through the controller,
which proxies onward. Any failure returns None and the caller degrades to
url_only: a controller that predates the endpoint is an expected state.
"""

import asyncio
from typing import Any, Optional

from loguru import logger
from pydantic import BaseModel

from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.xpander_api_client import APIClient

# Transcription is minutes-long on a busy voice pod; past this the turn has waited
# too long and the URL-only path serves the user better than a stall.
MEDIA_EXTRACT_TIMEOUT_SECONDS = 300.0


class MediaExtractResult(BaseModel):
    text: str
    op: str
    language: Optional[str] = None
    duration: Optional[float] = None
    is_rtl: Optional[bool] = None
    truncated: bool = False
    cached: bool = False


async def aextract_media_text(
    configuration: Any,
    *,
    url: str,
    op: str,
    mime: Optional[str] = None,
    kind: Optional[str] = None,
    sha256: Optional[str] = None,
    language: Optional[str] = None,
    timeout: float = MEDIA_EXTRACT_TIMEOUT_SECONDS,
) -> Optional[MediaExtractResult]:
    """Convert one attachment to text via the controller; None on any failure."""
    path = APIRoute.MediaExtract.value
    payload = {
        "url": url,
        "op": op,
        "mime": mime,
        "kind": kind,
        "sha256": sha256,
        "language": language,
    }
    try:
        api_client = APIClient(configuration=configuration)
        result = await asyncio.wait_for(
            api_client.make_request(path=path, method="POST", payload=payload),
            timeout=timeout,
        )
        if not isinstance(result, dict) or not result.get("text"):
            return None
        return MediaExtractResult(**result)
    except Exception as e:
        # The URL is presigned - log the failure shape, never the URL.
        logger.debug(
            f"media extract skipped (POST {path}, op {op}): {type(e).__name__}"
        )
        return None
