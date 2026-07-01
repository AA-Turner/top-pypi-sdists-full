"""Multimodal tool result detection and downgrading for non-vision models."""
from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


_IMAGE_KEYS = ("image", "image_url", "source", "data")


def _is_image_block(b: Any) -> bool:
    if not isinstance(b, dict):
        return False
    t = b.get("type")
    if t in ("image", "image_url", "input_image"):
        return True
    if "image_url" in b or ("source" in b and isinstance(b["source"], dict) and b["source"].get("type") in ("base64", "url")):
        return True
    return False


def is_multimodal_tool_result(result: Any) -> bool:
    if isinstance(result, str):
        return False
    if isinstance(result, dict):
        return any(_is_image_block(v) for v in result.values()) or _is_image_block(result)
    if isinstance(result, list):
        return any(_is_image_block(b) for b in result)
    return False


def _image_summary(b: Dict[str, Any]) -> str:
    if "image_url" in b:
        url = b["image_url"]
        if isinstance(url, dict):
            url = url.get("url", "")
        return f"[image: {url[:80]}{'…' if len(str(url)) > 80 else ''}]"
    src = b.get("source", {})
    if isinstance(src, dict):
        if src.get("type") == "url":
            return f"[image: {src.get('url', '')[:80]}]"
        if src.get("type") == "base64":
            mt = src.get("media_type", "image")
            data = src.get("data", "")
            return f"[image: {mt}, ~{len(data) * 3 // 4} bytes (base64-encoded)]"
    return "[image]"


def multimodal_text_summary(result: Any) -> str:
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        if _is_image_block(result):
            return _image_summary(result)
        parts = []
        for k, v in result.items():
            if _is_image_block(v):
                parts.append(f"{k}: {_image_summary(v)}")
            else:
                parts.append(f"{k}: {v}")
        return "\n".join(parts)
    if isinstance(result, list):
        out = []
        for blk in result:
            if isinstance(blk, dict):
                if _is_image_block(blk):
                    out.append(_image_summary(blk))
                elif blk.get("type") == "text":
                    out.append(str(blk.get("text", "")))
                else:
                    out.append(str(blk))
            else:
                out.append(str(blk))
        return "\n".join(out)
    return str(result)


def cache_image_block(block: Dict[str, Any], cache_dir: str | Path) -> str | None:
    """If the image is base64, write it to disk and return the absolute path.
    For URL images, returns the URL unchanged. Returns None on failure.
    """
    cache = Path(os.path.expanduser(str(cache_dir)))
    cache.mkdir(parents=True, exist_ok=True)
    src = block.get("source") if isinstance(block.get("source"), dict) else None
    if src and src.get("type") == "base64":
        data = src.get("data", "")
        media = src.get("media_type", "image/png")
        ext = media.split("/")[-1] or "png"
        try:
            raw = base64.b64decode(data)
        except Exception:  # noqa: BLE001
            return None
        h = hashlib.sha256(raw).hexdigest()[:16]
        path = cache / f"{h}.{ext}"
        try:
            path.write_bytes(raw)
        except OSError:
            return None
        return str(path)
    if src and src.get("type") == "url":
        return src.get("url")
    if "image_url" in block:
        url = block["image_url"]
        if isinstance(url, dict):
            return url.get("url")
        return str(url)
    return None


__all__ = [
    "is_multimodal_tool_result",
    "multimodal_text_summary",
    "cache_image_block",
]
