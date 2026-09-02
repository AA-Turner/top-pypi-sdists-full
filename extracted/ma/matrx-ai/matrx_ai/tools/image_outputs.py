"""The single funnel that turns "image bytes from a tool" into "MediaRef".

Any tool — server-side (cloud_browser action=screenshot, sandbox image gen) or
client-delegated (extension screenshots posted to /tool_results) — that
emits an image as part of its output goes through this module exactly
once. After it runs:

- The master image lives in ``cld_files`` with a deterministic path,
  permissions, versioning, share links, all the platform machinery.
- The tool's ``output`` dict is rewritten to a structured shape that
  carries a ``MediaRef`` instead of a base64 blob.
- Provider serialisers downstream see an ``ImageContent`` block backed
  by a resolved cloud URL, never a raw base64 string in a text block.

The funnel is process-wide. Its callers today:

- `external_handlers._normalise_result` — sandbox / MCP / desktop handlers.
- `aidream/services/ai_execution/tool_results.py::resolve_client_tool_results`
  — client-delegated results posted to `/tool_results`.
- `aidream/services/cloud_browser/tools.py::cloud_browser` (action=screenshot) — the
  server-side tool (host-registered; matrx-ai has no in-package browser tools).

Every future image-producing tool inherits the behaviour for free. AI image
GENERATION is a separate path (`providers/base_media.py::_persist_asset`),
which persists and emits an `ImageContent` block carrying the `file_id`.
"""

from __future__ import annotations

import base64
import logging
import uuid
from typing import Any

from matrx_ai._ext import get_ext, has_ext

logger = logging.getLogger(__name__)


# Keys we treat as carrying a base64-encoded image blob in tool outputs.
# All of these are stripped from the rewritten output and replaced with
# the canonical ``media_ref`` key.
_IMAGE_BASE64_KEYS: frozenset[str] = frozenset({
    "image_base64",
    "screenshot_base64",
    "img_base64",
    "picture_base64",
    "photo_base64",
    "base64_data",
})


# Output keys we strip when rewriting (so we don't leak duplicates).
_STRIP_ON_REWRITE: frozenset[str] = frozenset(_IMAGE_BASE64_KEYS) | {
    # Any url the producer attached alongside the blob — replaced by media_ref.
    #
    # ORDERING STILL MATTERS, and it is the caller's job: this strip only fires
    # for an output that reaches the funnel with its ``*_base64`` blob STILL
    # PRESENT, because `is_image_shaped_output` keys off that blob. Run
    # `persist_media_blobs_async` first and it deletes the blob, so the funnel
    # declines the output and the image never gets the tool-images master path
    # or an `ImageContent` block built from THIS module's shape. That persister
    # no longer manufactures a signed url (it emits the same media_ref
    # envelope), so the old "expiring link frozen in chat history" failure is
    # closed on both paths — but every image-producing caller still funnels
    # FIRST; `persist_media_blobs_async` is for the non-image blobs (audio,
    # video, pdf, opaque files) that this module does not handle.
    "screenshot_url",
    "image_url",
    "img_url",
}


def is_image_shaped_output(output: Any) -> bool:
    """True iff ``output`` looks like a tool-produced image dict.

    Heuristic:
      - dict with a ``media_type`` (or ``mime_type``) starting with ``image/``
      - and at least one ``*_base64`` key from ``_IMAGE_BASE64_KEYS``.
    """
    if not isinstance(output, dict):
        return False
    nested = output.get("image")
    if isinstance(nested, dict) and is_image_shaped_output(nested):
        return True
    media_type = (output.get("media_type") or output.get("mime_type") or "").lower()
    if not media_type.startswith("image/"):
        return False
    return any(k in output for k in _IMAGE_BASE64_KEYS)


def _extract_image_blob(output: dict) -> tuple[str, bytes] | None:
    """Pull out the first base64 image blob — returns (mime_type, bytes).

    Returns None when nothing usable is found.
    """
    mime_type = output.get("media_type") or output.get("mime_type")
    if not isinstance(mime_type, str) or not mime_type.startswith("image/"):
        return None
    for key in _IMAGE_BASE64_KEYS:
        b64 = output.get(key)
        if not isinstance(b64, str) or not b64:
            continue
        try:
            return mime_type, base64.b64decode(b64, validate=False)
        except Exception:
            continue
    return None


def _ext_for_mime(mime: str) -> str:
    norm = mime.lower().split(";", 1)[0].strip()
    return {
        "image/jpeg": "jpg",
        "image/jpg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
        "image/gif": "gif",
        "image/heic": "heic",
    }.get(norm, "bin")


async def upload_image_master(
    output: dict,
    *,
    tool_name: str = "",
    folder: str = "tool-images",
) -> dict:
    """Upload an image-shaped tool output's master to cloud storage.

    Returns a *new* dict with:

      - All ``*_base64`` blob keys stripped.
      - A ``media_ref`` key carrying ``{"file_id": <uuid>, "vision_class": None}``.
      - ``kind`` set to ``"image_ref"``.
      - Source dimensions preserved as ``source_width`` / ``source_height``
        when the original output supplied ``width`` / ``height``.

    On upload failure, returns a copy of the original output with all
    base64 keys still stripped and ``media_ref`` set to None plus a
    ``media_ref_error`` key — the model can detect the failure and the
    LLM context never sees a multi-megabyte blob.
    """
    extracted = _extract_image_blob(output)
    if extracted is None:
        return output  # Not actually image-shaped after all.

    mime_type, blob_bytes = extracted

    rewritten: dict[str, Any] = {
        k: v for k, v in output.items() if k not in _STRIP_ON_REWRITE
    }
    rewritten["kind"] = "image_ref"
    rewritten["media_type"] = mime_type
    rewritten["size_bytes"] = len(blob_bytes)
    if "width" in output and "source_width" not in rewritten:
        rewritten["source_width"] = output["width"]
    if "height" in output and "source_height" not in rewritten:
        rewritten["source_height"] = output["height"]

    if not has_ext("get_cloud_file_manager"):
        logger.warning(
            "[image_outputs] get_cloud_file_manager not configured; "
            "cannot persist tool image (tool=%s).",
            tool_name,
        )
        rewritten["media_ref"] = None
        rewritten["media_ref_error"] = "cloud_file_manager_unavailable"
        return rewritten

    try:
        fm = get_ext("get_cloud_file_manager")()
    except Exception as exc:
        logger.warning(
            "[image_outputs] get_cloud_file_manager() raised: %s (tool=%s)",
            exc, tool_name,
        )
        rewritten["media_ref"] = None
        rewritten["media_ref_error"] = f"file_manager_unavailable: {type(exc).__name__}"
        return rewritten

    master_uuid = str(uuid.uuid4())
    ext = _ext_for_mime(mime_type)
    file_path = f"{folder}/{master_uuid}/master.{ext}"

    try:
        result = await fm.sync_engine.managed_write_async(
            file_path,
            blob_bytes,
            mime_type=mime_type,
            visibility="personal",
            change_summary=f"tool image master ({tool_name})" if tool_name else "tool image master",
            metadata={
                "source": "tool_image_master",
                "tool_name": tool_name,
                "media_type": mime_type,
            },
        )
    except Exception as exc:
        logger.warning(
            "[image_outputs] master upload failed: %s (tool=%s)",
            exc, tool_name, exc_info=True,
        )
        rewritten["media_ref"] = None
        rewritten["media_ref_error"] = f"upload_failed: {type(exc).__name__}: {exc}"
        return rewritten

    rewritten["media_ref"] = {
        "file_id": result.file_id,
        "vision_class": None,
    }
    rewritten["file_id"] = result.file_id
    return rewritten


async def normalize_tool_output_async(output: Any, *, tool_name: str = "") -> Any:
    """Top-level entry: detect image-shaped dicts and rewrite to ``image_ref``.

    Accepts any tool ``output`` value. When it isn't an image-shaped dict,
    returns the input unchanged. When it is, returns a new dict with the
    base64 stripped and a ``media_ref`` key pointing at the cloud master.

    Idempotent: a dict whose ``kind`` is already ``"image_ref"`` is
    returned unchanged.
    """
    if isinstance(output, dict) and output.get("kind") == "image_ref":
        return output
    if not is_image_shaped_output(output):
        return output
    nested = output.get("image") if isinstance(output, dict) else None
    if isinstance(nested, dict) and is_image_shaped_output(nested):
        rewritten = await upload_image_master(nested, tool_name=tool_name)
        # matrx-local historically wrapped screenshots as
        # {text, image:{media_type,base64_data}}. Flatten that envelope at the
        # ingress boundary so base64 cannot survive into Content IR, logging,
        # or provider serialization.
        if isinstance(output.get("text"), str) and output["text"]:
            rewritten["text"] = output["text"]
        if isinstance(output.get("output"), str) and output["output"]:
            rewritten["text"] = output["output"]
        if isinstance(output.get("metadata"), dict):
            rewritten["metadata"] = output["metadata"]
        return rewritten
    return await upload_image_master(output, tool_name=tool_name)


def is_image_ref_output(output: Any) -> bool:
    """True iff ``output`` is the rewritten image_ref shape produced by
    ``upload_image_master``."""
    return (
        isinstance(output, dict)
        and output.get("kind") == "image_ref"
        and "media_ref" in output
    )


async def upload_image_masters(
    items: list[dict],
    *,
    tool_name: str = "",
    folder: str = "tool-images",
) -> dict:
    """Multi-image sibling of ``upload_image_master`` — for a tool call that
    produces several screenshots/images in one result (e.g. multi-viewport
    page capture), rather than exactly one.

    Uploads each image-shaped item in ``items`` (order preserved) and returns
    a single ``image_ref_list`` output: ``{"kind": "image_ref_list", "items":
    [<image_ref>, ...], "count": N}``. Non-image-shaped items pass through
    unchanged (mirrors ``normalize_tool_output_async``'s no-op behavior).
    Feeds ``ToolResult.to_tool_result_content()`` the same way a single
    ``image_ref`` does — see ``models.py::_build_image_ref_list_blocks``.
    """
    uploaded = [
        await upload_image_master(item, tool_name=tool_name, folder=folder)
        if is_image_shaped_output(item)
        else item
        for item in items
    ]
    return {"kind": "image_ref_list", "items": uploaded, "count": len(uploaded)}


def is_image_ref_list_output(output: Any) -> bool:
    """True iff ``output`` is the rewritten image_ref_list shape produced by
    ``upload_image_masters``."""
    return (
        isinstance(output, dict)
        and output.get("kind") == "image_ref_list"
        and isinstance(output.get("items"), list)
    )


__all__ = [
    "is_image_shaped_output",
    "is_image_ref_output",
    "is_image_ref_list_output",
    "upload_image_master",
    "upload_image_masters",
    "normalize_tool_output_async",
]
