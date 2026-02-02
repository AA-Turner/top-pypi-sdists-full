"""Generalized truncation framework for tool results."""

import os
import tempfile
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast

from msgspec.structs import replace

from exponent.core.config import get_chat_artifacts_dir
from exponent.core.remote_execution.cli_rpc_types import (
    BashToolResult,
    ErrorToolResult,
    GlobToolResult,
    GrepToolResult,
    ReadToolResult,
    ToolResult,
    WriteToolResult,
)
from exponent.core.remote_execution.utils import truncate_output

DEFAULT_CHARACTER_LIMIT = 20_000
BASH_CHARACTER_LIMIT = 8_000
MAX_FILE_CHARS = 2_000_000  # 2M character limit for full output file
DEFAULT_LIST_ITEM_LIMIT = 1000
DEFAULT_LIST_PREVIEW_ITEMS = 10


def _write_full_output_to_file(output: str, chat_uuid: str) -> str | None:
    """Write full output to a temp file, truncated to last MAX_FILE_CHARS characters.

    Files are written to the per-chat artifacts directory (~/.indent/chats/{uuid}/).
    """
    try:
        if len(output) > MAX_FILE_CHARS:
            output = output[-MAX_FILE_CHARS:]

        artifacts_dir = get_chat_artifacts_dir(chat_uuid)
        os.makedirs(artifacts_dir, exist_ok=True)

        fd, path = tempfile.mkstemp(
            prefix="bash_output_", suffix=".txt", dir=artifacts_dir
        )
        try:
            os.write(fd, output.encode("utf-8", errors="replace"))
        finally:
            os.close(fd)
        return path
    except Exception:
        return None


_T = TypeVar("_T", bound=ToolResult)


class TruncationStrategy(ABC, Generic[_T]):
    @abstractmethod
    def should_truncate(self, result: _T) -> bool:
        """Return True if the result should be truncated."""

    @abstractmethod
    def truncate(self, result: _T, chat_uuid: str | None = None) -> _T:
        """Truncate the result and return the truncated version."""


class StringFieldTruncation(TruncationStrategy[_T]):
    def __init__(
        self,
        field_name: str,
        character_limit: int = DEFAULT_CHARACTER_LIMIT,
    ):
        self.field_name = field_name
        self.character_limit = character_limit

    def should_truncate(self, result: _T) -> bool:
        if hasattr(result, self.field_name):
            value = getattr(result, self.field_name)
            if isinstance(value, str):
                return len(value) > self.character_limit
        return False

    def truncate(self, result: _T, chat_uuid: str | None = None) -> _T:
        if not hasattr(result, self.field_name):
            return result

        value = getattr(result, self.field_name)
        if not isinstance(value, str):
            return result

        truncated_value, was_truncated = truncate_output(value, self.character_limit)

        updates: dict[str, Any] = {self.field_name: truncated_value}
        if hasattr(result, "truncated") and was_truncated:
            updates["truncated"] = True

        return replace(result, **updates)


class ListFieldTruncation(TruncationStrategy[_T]):
    def __init__(
        self,
        field_name: str,
        item_limit: int = DEFAULT_LIST_ITEM_LIMIT,
        preview_items: int = DEFAULT_LIST_PREVIEW_ITEMS,
    ):
        self.field_name = field_name
        self.item_limit = item_limit
        self.preview_items = preview_items

    def should_truncate(self, result: _T) -> bool:
        if hasattr(result, self.field_name):
            value = getattr(result, self.field_name)
            if isinstance(value, list):
                return len(value) > self.item_limit
        return False

    def truncate(self, result: _T, chat_uuid: str | None = None) -> _T:
        if not hasattr(result, self.field_name):
            return result

        value = getattr(result, self.field_name)
        if not isinstance(value, list):
            return result

        total_items = len(value)
        if total_items <= self.item_limit:
            return result

        truncated_count = max(0, total_items - 2 * self.preview_items)
        truncated_list = (
            value[: self.preview_items]
            + [f"... {truncated_count} items truncated ..."]
            + value[-self.preview_items :]
        )

        updates: dict[str, Any] = {self.field_name: truncated_list}
        if hasattr(result, "truncated"):
            updates["truncated"] = True

        return replace(result, **updates)


class CompositeTruncation(TruncationStrategy[_T]):
    def __init__(self, strategies: list[TruncationStrategy[_T]]):
        self.strategies = strategies

    def should_truncate(self, result: _T) -> bool:
        return any(strategy.should_truncate(result) for strategy in self.strategies)

    def truncate(self, result: _T, chat_uuid: str | None = None) -> _T:
        for strategy in self.strategies:
            if strategy.should_truncate(result):
                result = strategy.truncate(result, chat_uuid)
        return result


class TailTruncation(TruncationStrategy[_T]):
    """Truncation strategy that keeps the end of the output (tail) instead of the beginning.

    Writes full output to a temp file before truncating.
    """

    def __init__(
        self,
        field_name: str,
        character_limit: int = DEFAULT_CHARACTER_LIMIT,
    ):
        self.field_name = field_name
        self.character_limit = character_limit

    def should_truncate(self, result: _T) -> bool:
        if hasattr(result, self.field_name):
            value = getattr(result, self.field_name)
            if isinstance(value, str):
                return len(value) > self.character_limit
        return False

    def truncate(self, result: _T, chat_uuid: str | None = None) -> _T:
        if not hasattr(result, self.field_name):
            return result

        value = getattr(result, self.field_name)
        if not isinstance(value, str):
            return result

        file_path = _write_full_output_to_file(value, chat_uuid) if chat_uuid else None

        updates: dict[str, Any] = {}
        if file_path and hasattr(result, "output_file"):
            updates["output_file"] = file_path

        if len(value) <= self.character_limit:
            if updates:
                return replace(result, **updates)
            return result

        truncated_value = value[-self.character_limit :]

        newline_pos = truncated_value.find("\n")
        if newline_pos != -1 and newline_pos < 1000:
            truncated_value = truncated_value[newline_pos + 1 :]

        if file_path:
            truncation_msg = f"[Truncated to last {self.character_limit} characters. Full output written to: {file_path}]\n"
        else:
            truncation_msg = f"[Truncated to last {self.character_limit} characters.]\n"
        truncated_value = truncation_msg + truncated_value

        updates[self.field_name] = truncated_value
        if hasattr(result, "truncated"):
            updates["truncated"] = True

        return replace(result, **updates)


class NoOpTruncation(TruncationStrategy[_T]):
    def should_truncate(self, result: _T) -> bool:
        return False

    def truncate(self, result: _T, chat_uuid: str | None = None) -> _T:
        return result


class StringListTruncation(TruncationStrategy[_T]):
    """Truncation for lists of strings that limits both number of items and individual string length."""

    def __init__(
        self,
        field_name: str,
        max_items: int = DEFAULT_LIST_ITEM_LIMIT,
        preview_items: int = DEFAULT_LIST_PREVIEW_ITEMS,
        max_item_length: int = 1000,
    ):
        self.field_name = field_name
        self.max_items = max_items
        self.preview_items = preview_items
        self.max_item_length = max_item_length

    def should_truncate(self, result: _T) -> bool:
        if not hasattr(result, self.field_name):
            return False

        items = getattr(result, self.field_name)
        if not isinstance(items, list):
            return False

        # Check if we need to truncate number of items
        if len(items) > self.max_items:
            return True

        # Check if any individual item is too long
        for item in items:
            if isinstance(item, str) and len(item) > self.max_item_length:
                return True
            # Handle dict items (e.g., with metadata like file path and line number)
            elif isinstance(item, dict) and "content" in item:
                if len(item["content"]) > self.max_item_length:
                    return True

        return False

    def _truncate_item_content(
        self, item: str | dict[str, Any]
    ) -> str | dict[str, Any]:
        """Truncate an individual item's content."""
        if isinstance(item, str):
            if len(item) <= self.max_item_length:
                return item
            # Truncate string item
            truncated, _ = truncate_output(item, self.max_item_length)
            return truncated
        elif isinstance(item, dict) and "content" in item:
            # Handle dict-style items (e.g., with metadata like file path and line number)
            if len(item["content"]) <= self.max_item_length:
                return item
            truncated_content, _ = truncate_output(
                item["content"], self.max_item_length
            )
            return {**item, "content": truncated_content}
        else:
            return item

    def truncate(self, result: _T, chat_uuid: str | None = None) -> _T:
        if not hasattr(result, self.field_name):
            return result

        items = getattr(result, self.field_name)
        if not isinstance(items, list):
            return result

        # First, truncate individual item contents
        truncated_items = [self._truncate_item_content(item) for item in items]

        # Then, limit the number of items if needed
        total_items = len(truncated_items)
        if total_items > self.max_items:
            truncated_count = max(0, total_items - 2 * self.preview_items)
            final_items = (
                truncated_items[: self.preview_items]
                + [f"... {truncated_count} items truncated ..."]
                + truncated_items[-self.preview_items :]
            )
        else:
            final_items = truncated_items

        updates: dict[str, Any] = {self.field_name: final_items}
        if hasattr(result, "truncated"):
            updates["truncated"] = True

        return replace(result, **updates)


TRUNCATION_REGISTRY: dict[type[ToolResult], TruncationStrategy[Any]] = {
    ReadToolResult: StringFieldTruncation("content"),
    WriteToolResult: StringFieldTruncation("message"),
    GrepToolResult: StringListTruncation("matches"),
    GlobToolResult: StringListTruncation("filenames", max_item_length=4096),
    BashToolResult: TailTruncation(
        "shell_output", character_limit=BASH_CHARACTER_LIMIT
    ),
}


T = TypeVar("T", bound=ToolResult)


def truncate_tool_result(result: T, chat_uuid: str | None = None) -> T:
    if isinstance(result, ErrorToolResult):
        return result

    result_type = type(result)
    if result_type in TRUNCATION_REGISTRY:
        strategy = TRUNCATION_REGISTRY[result_type]
        if isinstance(result, BashToolResult):
            return cast(T, strategy.truncate(result, chat_uuid))
        elif strategy.should_truncate(result):
            return cast(T, strategy.truncate(result, chat_uuid))

    return result
