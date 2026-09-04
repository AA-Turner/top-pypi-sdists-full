"""Shared parsing of tool-result content blocks into ATIF observation parts.

Every agent harness gets its tool results as a list of content blocks — the
codex CLI's ``item.completed`` event carries ``result.content`` in MCP wire
shape, the Claude Code transcript carries ``tool_result.content`` in Anthropic
messages shape — and the trace needs the same three things from each: the text
the model read, the frame to show in the viewer (``atif.step.screenshot``), and
any non-text payloads as attachments. This is the one place that knows how to
walk those blocks, so no harness re-derives it (a harness that only joined
``text`` blocks is exactly how computer-use screenshots vanished from codex
traces).

Image blocks come in two wire shapes and both are handled::

    {"type": "image", "data": "<b64>", "mimeType": "image/png"}                 # MCP
    {"type": "image", "source": {"data": "<b64>", "media_type": "image/png"}}   # Anthropic
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

DEFAULT_IMAGE_FORMAT = "image/png"


@dataclass
class ParsedToolContent:
    """What a tool result contributes to its ATIF step."""

    text: str
    screenshot: str | None = None
    screenshot_format: str | None = None
    attachments: list[dict[str, Any]] = field(default_factory=list)


def image_block_data(block: dict[str, Any]) -> tuple[str, str] | None:
    """``(base64, media_type)`` for an image block in either wire shape, else None."""
    if block.get("type") != "image":
        return None
    source = block.get("source")
    if isinstance(source, dict):
        data = source.get("data")
        media_type = source.get("media_type") or source.get("mimeType")
    else:
        data = block.get("data")
        media_type = block.get("mimeType") or block.get("media_type")
    if not isinstance(data, str) or not data:
        return None
    return data, media_type if isinstance(media_type, str) and media_type else DEFAULT_IMAGE_FORMAT


def parse_content_blocks(
    blocks: Any,
    *,
    tool_name: str,
    file_path: str | None = None,
) -> ParsedToolContent:
    """Split tool-result content blocks into text, the first image, and attachments.

    ``blocks`` is normally the content-block list; a bare string is treated as
    one text block and anything else is JSON-dumped into the text. The first
    image with data becomes the step screenshot; every image is also kept as
    an ``attachments`` entry (``{"type": "image", "base64", "media_type"}``),
    and non-text/non-image blocks are attached as-is. When there is no text,
    the text describes the attachments so the observation is never blank.
    """
    text_parts: list[str] = []
    attachments: list[dict[str, Any]] = []
    screenshot: str | None = None
    screenshot_format: str | None = None

    if isinstance(blocks, str):
        blocks = [blocks]
    elif not isinstance(blocks, list):
        blocks = [json.dumps(blocks, default=str)]

    for block in blocks:
        if isinstance(block, str):
            text_parts.append(block)
            continue
        if not isinstance(block, dict):
            text_parts.append(json.dumps(block, default=str))
            continue
        if block.get("type") == "text":
            text_parts.append(str(block.get("text", "")))
            continue
        image = image_block_data(block)
        if image is not None:
            data, media_type = image
            if screenshot is None:
                screenshot, screenshot_format = data, media_type
            attachments.append(
                {
                    "type": "image",
                    "base64": data,
                    "media_type": media_type,
                    **({"file_path": file_path} if file_path else {}),
                }
            )
            continue
        attachments.append(block)

    text = "\n".join(part for part in text_parts if part).strip()
    if not text:
        if attachments and file_path:
            text = f"Read image file: {file_path}"
        elif attachments:
            text = f"{tool_name} returned {len(attachments)} attachment(s)"

    return ParsedToolContent(
        text=text,
        screenshot=screenshot,
        screenshot_format=screenshot_format,
        attachments=attachments,
    )
