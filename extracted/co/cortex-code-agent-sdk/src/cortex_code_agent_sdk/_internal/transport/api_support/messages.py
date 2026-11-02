"""SDK/API message conversion helpers for direct Agent API transport."""

from __future__ import annotations

from typing import Any

from .utils import _as_record


def _to_api_user_message(message: dict[str, Any]) -> dict[str, Any]:
    content = message.get("message", {}).get("content")
    if not isinstance(content, list):
        return {"role": "user", "content": []}
    api_content: list[dict[str, Any]] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "text":
            api_content.append({
                "type": "text",
                "text": str(block.get("text", "")),
                "is_user_prompt": True,
            })
        elif block.get("type") == "tool_result":
            block_content = block.get("content")
            api_content.append({
                "type": "tool_result",
                "tool_result": {
                    "name": "tool",
                    "tool_use_id": block.get("tool_use_id"),
                    "status": "error" if block.get("is_error") else "success",
                    "content": (
                        [{"type": "text", "text": block_content}]
                        if isinstance(block_content, str)
                        else block_content
                    ),
                },
            })
    return {"role": "user", "content": api_content}

def _to_api_assistant_content_block(block: dict[str, Any]) -> dict[str, Any]:
    if block.get("type") == "text":
        return block
    if block.get("type") == "thinking":
        return {"type": "text", "text": str(block.get("thinking", ""))}
    if block.get("type") == "tool_use":
        return {
            "type": "tool_use",
            "tool_use": {
                "tool_use_id": block.get("id"),
                "name": block.get("name"),
                "input": _as_record(block.get("input")),
            },
        }
    return {
        "type": "tool_result",
        "tool_result": {
            "name": "tool",
            "tool_use_id": block.get("tool_use_id"),
            "status": "error" if block.get("is_error") else "success",
            "content": (
                [{"type": "text", "text": block.get("content")}]
                if isinstance(block.get("content"), str)
                else block.get("content")
            ),
        },
    }
