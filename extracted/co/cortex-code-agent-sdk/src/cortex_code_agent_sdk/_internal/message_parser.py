"""Message parser for Cortex Code SDK responses."""

import logging
from typing import Any

from .._errors import MessageParseError
from ..types import (
    AssistantMessage,
    ContentBlock,
    InitSystemMessage,
    Message,
    ResultMessage,
    StreamEvent,
    SystemMessage,
    SystemTextMessage,
    TaskNotificationMessage,
    TaskProgressMessage,
    TaskStartedMessage,
    TextBlock,
    ThinkingBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
)

logger = logging.getLogger(__name__)


def parse_message(data: dict[str, Any]) -> Message | None:
    """
    Parse message from CLI output into typed Message objects.

    Args:
        data: Raw message dictionary from CLI output

    Returns:
        Parsed Message object

    Raises:
        MessageParseError: If parsing fails or message type is unrecognized
    """
    if not isinstance(data, dict):
        raise MessageParseError(
            f"Invalid message data type (expected dict, got {type(data).__name__})",
            data,
        )

    message_type = data.get("type")
    if not message_type:
        raise MessageParseError("Message missing 'type' field", data)

    match message_type:
        case "user":
            try:
                parent_tool_use_id = data.get("parent_tool_use_id")
                tool_use_result = data.get("tool_use_result")
                uuid = data.get("uuid")
                if isinstance(data["message"]["content"], list):
                    user_content_blocks: list[ContentBlock] = []
                    for block in data["message"]["content"]:
                        match block["type"]:
                            case "text":
                                user_content_blocks.append(
                                    TextBlock(text=block["text"])
                                )
                            case "tool_use":
                                user_content_blocks.append(
                                    ToolUseBlock(
                                        id=block["id"],
                                        name=block["name"],
                                        input=block["input"],
                                    )
                                )
                            case "tool_result":
                                user_content_blocks.append(
                                    ToolResultBlock(
                                        tool_use_id=block["tool_use_id"],
                                        content=block.get("content"),
                                        is_error=block.get("is_error"),
                                    )
                                )
                    return UserMessage(
                        content=user_content_blocks,
                        uuid=uuid,
                        parent_tool_use_id=parent_tool_use_id,
                        tool_use_result=tool_use_result,
                    )
                return UserMessage(
                    content=data["message"]["content"],
                    uuid=uuid,
                    parent_tool_use_id=parent_tool_use_id,
                    tool_use_result=tool_use_result,
                )
            except KeyError as e:
                raise MessageParseError(
                    f"Missing required field in user message: {e}", data
                ) from e

        case "assistant":
            try:
                content_blocks: list[ContentBlock] = []
                for block in data["message"]["content"]:
                    match block["type"]:
                        case "text":
                            content_blocks.append(TextBlock(text=block["text"]))
                        case "thinking":
                            content_blocks.append(
                                ThinkingBlock(
                                    thinking=block["thinking"],
                                    signature=block.get("signature", ""),
                                )
                            )
                        case "tool_use":
                            content_blocks.append(
                                ToolUseBlock(
                                    id=block["id"],
                                    name=block["name"],
                                    input=block["input"],
                                )
                            )
                        case "tool_result":
                            content_blocks.append(
                                ToolResultBlock(
                                    tool_use_id=block["tool_use_id"],
                                    content=block.get("content"),
                                    is_error=block.get("is_error"),
                                )
                            )

                return AssistantMessage(
                    content=content_blocks,
                    model=data["message"]["model"],
                    message_id=data["message"].get("id"),
                    parent_tool_use_id=data.get("parent_tool_use_id"),
                    error=data.get("error"),
                    usage=data["message"].get("usage"),
                )
            except KeyError as e:
                raise MessageParseError(
                    f"Missing required field in assistant message: {e}", data
                ) from e

        case "system":
            try:
                subtype = data["subtype"]
                match subtype:
                    case "init":
                        return InitSystemMessage(
                            subtype=subtype,
                            data=data,
                            uuid=data["uuid"],
                            session_id=data["session_id"],
                            cwd=data["cwd"],
                            model=data["model"],
                            tools=data["tools"],
                            mcp_servers=data["mcp_servers"],
                            permission_mode=data["permissionMode"],
                            api_key_source=data.get("apiKeySource"),
                            agents=data.get("agents"),
                            betas=data.get("betas"),
                            slash_commands=data.get("slash_commands"),
                            output_style=data.get("output_style"),
                            skills=data.get("skills"),
                            plugins=data.get("plugins"),
                        )
                    case "task_started":
                        return TaskStartedMessage(
                            subtype=subtype,
                            data=data,
                            task_id=data["task_id"],
                            description=data["description"],
                            uuid=data["uuid"],
                            session_id=data["session_id"],
                            tool_use_id=data.get("tool_use_id"),
                            task_type=data.get("task_type"),
                        )
                    case "task_progress":
                        return TaskProgressMessage(
                            subtype=subtype,
                            data=data,
                            task_id=data["task_id"],
                            description=data["description"],
                            usage=data["usage"],
                            uuid=data["uuid"],
                            session_id=data["session_id"],
                            tool_use_id=data.get("tool_use_id"),
                            last_tool_name=data.get("last_tool_name"),
                        )
                    case "task_notification":
                        return TaskNotificationMessage(
                            subtype=subtype,
                            data=data,
                            task_id=data["task_id"],
                            status=data["status"],
                            output_file=data["output_file"],
                            summary=data["summary"],
                            uuid=data["uuid"],
                            session_id=data["session_id"],
                            tool_use_id=data.get("tool_use_id"),
                            usage=data.get("usage"),
                        )
                    case _:
                        return SystemMessage(
                            subtype=subtype,
                            data=data,
                        )
            except KeyError as e:
                raise MessageParseError(
                    f"Missing required field in system message: {e}", data
                ) from e

        case "system_message":
            try:
                return SystemTextMessage(
                    subtype="system_message",
                    data=data,
                    content=data["content"],
                    session_id=data.get("session_id"),
                )
            except KeyError as e:
                raise MessageParseError(
                    f"Missing required field in system_message: {e}", data
                ) from e

        case "result":
            try:
                return ResultMessage(
                    subtype=data["subtype"],
                    duration_ms=data.get("duration_ms", 0),
                    duration_api_ms=data.get("duration_api_ms", 0),
                    is_error=data.get("is_error", data.get("subtype") == "error"),
                    num_turns=data.get("num_turns", 0),
                    session_id=data.get("session_id", ""),
                    stop_reason=data.get("stop_reason"),
                    total_cost_usd=data.get("total_cost_usd"),
                    usage=data.get("usage"),
                    result=data.get("result"),
                    structured_output=data.get("structured_output"),
                    errors=data.get("errors"),
                    permission_denials=data.get("permission_denials"),
                    uuid=data.get("uuid"),
                )
            except KeyError as e:
                raise MessageParseError(
                    f"Missing required field in result message: {e}", data
                ) from e

        case "stream_event":
            try:
                return StreamEvent(
                    uuid=data["uuid"],
                    session_id=data["session_id"],
                    event=data["event"],
                    parent_tool_use_id=data.get("parent_tool_use_id"),
                )
            except KeyError as e:
                raise MessageParseError(
                    f"Missing required field in stream_event message: {e}", data
                ) from e

        case _:
            # Forward-compatible: skip unrecognized message types so newer
            # CLI versions don't crash older SDK versions.
            logger.debug("Skipping unknown message type: %s", message_type)
            return None
