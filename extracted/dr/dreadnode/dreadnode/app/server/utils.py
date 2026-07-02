"""Server utility functions."""

from __future__ import annotations

import typing as t

import orjson


def _default_serializer(obj: t.Any) -> t.Any:
    """Default serializer for types orjson doesn't handle natively."""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if hasattr(obj, "__str__"):
        return str(obj)
    raise TypeError(f"Type is not JSON serializable: {type(obj).__name__}")


def safe_json_dumps(obj: t.Any) -> str:
    """JSON dumps using orjson (handles NaN/Infinity as null, faster serialization)."""
    return orjson.dumps(
        obj,
        default=_default_serializer,
        option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS,
    ).decode("utf-8")


# Outbound runtime WS frames are capped so a single oversized agent event
# (e.g. a huge tool output or a pickle blob) cannot breach the receiver's
# websockets frame limit and close the connection with 1009 "message too big",
# failing the whole turn (ENG-7237). Kept under the platform API's 32 MiB
# inbound ceiling (RUNTIME_WS_MAX_MESSAGE_BYTES) so any frame we send fits.
MAX_WS_FRAME_BYTES = 30 * 1024 * 1024


def serialize_ws_frame(envelope: dict[str, t.Any]) -> str:
    """Serialize an outbound WS envelope, replacing an oversized ``payload``
    with a truncation marker so the frame never exceeds ``MAX_WS_FRAME_BYTES``.

    Truncation only fires for frames that would otherwise be rejected with a
    1009 close (and thus fail the turn), so it is strictly safer than sending
    them. Envelope metadata (kind, seq, terminal, …) is preserved, and the full
    event is still persisted to the platform trajectory out-of-band.
    """
    encoded = orjson.dumps(
        envelope,
        default=_default_serializer,
        option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS,
    )
    if len(encoded) <= MAX_WS_FRAME_BYTES:
        return encoded.decode("utf-8")
    capped = dict(envelope)
    capped["payload"] = {
        "dreadnode_truncated": True,
        "reason": "runtime websocket frame exceeded size cap",
        "original_bytes": len(encoded),
        "cap_bytes": MAX_WS_FRAME_BYTES,
    }
    return safe_json_dumps(capped)
