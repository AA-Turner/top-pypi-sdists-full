"""Message ↔ request-payload conversion helpers."""

import base64
import contextlib
import typing as t

from dreadnode.generators.message import Message


def extract_parts(message: Message) -> dict[str, str]:
    """Pull text + base64 of the first image/audio/video from a message's parts."""
    out = {"prompt": "", "image_b64": "", "audio_b64": "", "video_b64": ""}
    texts: list[str] = []
    for part in getattr(message, "content_parts", None) or []:
        ptype = getattr(part, "type", None)
        if ptype == "text" and getattr(part, "text", None):
            texts.append(part.text)
        elif ptype == "image_url" and not out["image_b64"]:
            with contextlib.suppress(Exception):
                out["image_b64"] = base64.b64encode(part.to_bytes()).decode("ascii")
        elif ptype == "input_audio" and not out["audio_b64"]:
            with contextlib.suppress(Exception):
                out["audio_b64"] = base64.b64encode(part.to_bytes()).decode("ascii")
        elif ptype == "video_url" and not out["video_b64"]:
            with contextlib.suppress(Exception):
                raw = getattr(getattr(part, "file", None), "file_data", "") or ""
                out["video_b64"] = raw.split(",", 1)[1] if "," in raw else raw
    out["prompt"] = "\n".join(texts)
    return out


def extract_media_bytes(message: Message, kind: str) -> bytes:
    """Return the raw bytes of the first ``kind`` (``audio``/``image``/``video``) part.

    For endpoints that take a media file body (e.g. a SageMaker ASR container) rather than
    a JSON payload. Returns ``b""`` when the message has no part of that kind.
    """
    part_type = {"audio": "input_audio", "image": "image_url", "video": "video_url"}[kind]
    for part in getattr(message, "content_parts", None) or []:
        if getattr(part, "type", None) == part_type:
            with contextlib.suppress(Exception):
                return part.to_bytes()
    return b""


def extract_response_text(data: t.Any, path: str) -> str:
    """Resolve the response text from a JSON body via a JSONPath expression."""
    from jsonpath_ng.ext import parse as jp_parse

    matches = [m.value for m in jp_parse(path).find(data)]
    value = matches[0] if matches else data
    return value if isinstance(value, str) else str(value)
