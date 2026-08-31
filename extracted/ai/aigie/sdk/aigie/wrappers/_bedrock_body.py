"""Reading bytes off a Bedrock response.

Bedrock hands back a stream rather than a parsed object, and a span needs the
completion inside it - so tracing has to read a thing that reads once, and put
something back. That exchange, and the JSON shapes different model families
wrap their output in, is what lives here.
"""

from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class _RaisesOnRead:
    """A raw stream that replays one failure, however it is read."""

    def __init__(self, error: BaseException) -> None:
        self._error = error

    def read(self, amt: int | None = None) -> bytes:
        raise self._error

    def stream(self, *args: Any, **kwargs: Any) -> Any:
        raise self._error

    def close(self) -> None:
        return None


def _failed_body(error: BaseException) -> Any:
    """A stand-in for a body whose read failed, that fails the same way.

    Wrapped in a real `StreamingBody` where possible so every method the caller
    might reach for - `read`, iteration, `iter_lines`, `close` - still exists
    and still raises.
    """
    try:
        from botocore.response import StreamingBody

        return StreamingBody(_RaisesOnRead(error), 0)
    except Exception as e:  # noqa: BLE001 - the stand-in goes back regardless
        logger.debug("[wrapper] Falling back to a bare failing stream: %s", e)
        return _RaisesOnRead(error)


def reusable_body(response: Any) -> bytes | None:
    """Read the response body, putting a readable copy back in its place.

    `StreamingBody` reads once, so reading it is unavoidable; handing the
    customer an emptied response is not. A *failed* read may have consumed an
    unknown number of bytes, so a body that replays the same error goes back
    rather than the partial bytes - a truncated response presented as a
    complete one is worse than the error they were already getting.
    """
    body = response.get("body") if isinstance(response, dict) else None
    if body is None or not hasattr(body, "read"):
        return None

    try:
        raw: bytes = body.read()
    except Exception as e:  # noqa: BLE001 - a broken stream can raise anything
        logger.debug("[wrapper] Could not read the Bedrock response body: %s", e)
        _release(body)
        response["body"] = _failed_body(e)
        return None

    _release(body)
    response["body"] = _rewound(raw)
    return raw


def _release(body: Any) -> None:
    """Close the original stream being replaced, so its connection goes back.

    The caller gets a different object either way, so nothing else will ever
    close this one, and an unreturned connection is a pool slot lost for good.
    """
    try:
        body.close()
    except Exception as e:  # noqa: BLE001 - closing is best-effort by nature
        logger.debug("[wrapper] Could not close the replaced Bedrock body: %s", e)


def _rewound(raw: bytes) -> Any:
    """A fresh, readable stand-in for the `StreamingBody` just consumed.

    Total by construction: the original is already consumed, so returning
    nothing would leave the customer a response they can no longer read.
    """
    import io

    try:
        from botocore.response import StreamingBody

        return StreamingBody(io.BytesIO(raw), len(raw))
    except Exception as e:  # noqa: BLE001 - the bytes go back regardless
        logger.debug("[wrapper] Falling back to a plain stream for the body: %s", e)
        return io.BytesIO(raw)


def parse_json(raw: Any) -> dict[str, Any]:
    """Decode a JSON payload to a dict, or `{}` for anything unreadable."""
    if raw is None:
        return {}
    try:
        decoded = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
    except (AttributeError, TypeError, ValueError, UnicodeDecodeError) as e:
        logger.debug("[wrapper] Could not decode a Bedrock payload: %s", e)
        return {}
    return decoded if isinstance(decoded, dict) else {}


def chunk_payload(event: Any) -> dict[str, Any]:
    """The decoded JSON carried by one event-stream chunk."""
    chunk = event.get("chunk") if isinstance(event, dict) else None
    raw = chunk.get("bytes") if isinstance(chunk, dict) else None
    return parse_json(raw)


def chunk_text(parsed: dict[str, Any]) -> str:
    """The text one chunk carries, across the shapes Bedrock models use."""
    if "completion" in parsed:  # Anthropic text-completions
        return str(parsed["completion"])
    if "outputText" in parsed:  # Amazon Titan
        return str(parsed["outputText"])
    delta = parsed.get("delta")  # Anthropic messages API
    if isinstance(delta, dict) and "text" in delta:
        return str(delta["text"])
    return ""


def extract_metrics(body: dict[str, Any]) -> dict[str, Any]:
    """Extract metrics from Bedrock response"""
    metrics: dict[str, Any] = {}

    # Different models have different response formats
    if "completion" in body:
        # Anthropic Claude
        metrics["completion"] = body["completion"]
        metrics["stopReason"] = body.get("stop_reason")

    if "results" in body:
        # AI21 Jurassic
        metrics["results"] = body["results"]

    if "generations" in body:
        # Cohere
        metrics["generations"] = body["generations"]

    if "outputText" in body:
        # Amazon Titan
        metrics["outputText"] = body["outputText"]

    # Token usage (if available)
    if "amazon-bedrock-invocationMetrics" in body:
        invocation_metrics = body["amazon-bedrock-invocationMetrics"]
        metrics["inputTokens"] = invocation_metrics.get("inputTokenCount")
        metrics["outputTokens"] = invocation_metrics.get("outputTokenCount")
        metrics["totalTokens"] = invocation_metrics.get(
            "inputTokenCount", 0
        ) + invocation_metrics.get("outputTokenCount", 0)
        metrics["latency"] = invocation_metrics.get("invocationLatency")

    return metrics
