"""Generalized truncation framework for tool results."""

import os
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, cast

from msgspec.structs import replace

from exponent.core.file_layout import bash_result_path, generate_bash_id
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


def write_full_output_to_file(output: str, chat_uuid: str) -> str | None:
    try:
        if len(output) > MAX_FILE_CHARS:
            output = output[-MAX_FILE_CHARS:]

        bash_id = generate_bash_id()
        epoch_ms = int(__import__("time").time() * 1000)
        path, _ = bash_result_path(chat_uuid, bash_id, epoch_ms)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(output.encode("utf-8", errors="replace"))
        return path
    except Exception:
        return None


_T = TypeVar("_T", bound=ToolResult)


class TruncationStrategy(ABC, Generic[_T]):
    @abstractmethod
    def should_truncate(self, result: _T) -> bool:
        """Return True if the result should be truncated."""

    @abstractmethod
    def truncate(self, result: _T) -> _T:
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

    def truncate(self, result: _T) -> _T:
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

    def truncate(self, result: _T) -> _T:
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
            value[: self.preview_items] + [f"... {truncated_count} items truncated ..."] + value[-self.preview_items :]
        )

        updates: dict[str, Any] = {self.field_name: truncated_list}
        if hasattr(result, "truncated"):
            updates["truncated"] = True

        return replace(result, **updates)


class TailTruncation(TruncationStrategy[_T]):
    """Truncation strategy that keeps the end of the output (tail) instead of the beginning."""

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

    def truncate(self, result: _T) -> _T:
        if not hasattr(result, self.field_name):
            return result

        value = getattr(result, self.field_name)
        if not isinstance(value, str):
            return result

        if len(value) <= self.character_limit:
            return result

        truncated_value = value[-self.character_limit :]

        newline_pos = truncated_value.find("\n")
        if newline_pos != -1 and newline_pos < 1000:
            truncated_value = truncated_value[newline_pos + 1 :]

        truncation_msg = f"[Truncated to last {self.character_limit} characters.]\n"
        truncated_value = truncation_msg + truncated_value

        updates: dict[str, Any] = {self.field_name: truncated_value}
        if hasattr(result, "truncated"):
            updates["truncated"] = True

        return replace(result, **updates)


class StringListTruncation(TruncationStrategy[_T]):
    """Truncation for lists of strings that limits both number of items and individual string length."""

    def __init__(
        self,
        field_name: str,
        max_items: int = DEFAULT_LIST_ITEM_LIMIT,
        preview_items: int = DEFAULT_LIST_PREVIEW_ITEMS,
        max_item_length: int = 1000,
        max_total_length: int | None = None,
    ):
        self.field_name = field_name
        self.max_items = max_items
        self.preview_items = preview_items
        self.max_item_length = max_item_length
        self.max_total_length = max_total_length

    @staticmethod
    def _item_len(item: str | dict[str, Any]) -> int:
        if isinstance(item, str):
            return len(item)
        elif isinstance(item, dict) and "content" in item:
            return len(item["content"])
        return 0

    def _effective_item_limit(self, num_items: int) -> int:
        """Per-item length budget, derived from equal allocation of the total cap."""
        if self.max_total_length is None or num_items <= 0:
            return self.max_item_length
        return min(self.max_item_length, max(1, self.max_total_length // num_items))

    def _surviving_item_count(self, num_items: int) -> int:
        """Number of original items that survive after list-length truncation."""
        if num_items > self.max_items:
            return 2 * self.preview_items
        return num_items

    def should_truncate(self, result: _T) -> bool:
        if not hasattr(result, self.field_name):
            return False

        items = getattr(result, self.field_name)
        if not isinstance(items, list):
            return False

        # Check if we need to truncate number of items
        if len(items) > self.max_items:
            return True

        item_limit = self._effective_item_limit(self._surviving_item_count(len(items)))

        # Check if any individual item is too long under the effective per-item limit
        for item in items:
            if self._item_len(item) > item_limit:
                return True

        return False

    def _truncate_item_content(self, item: str | dict[str, Any], item_limit: int) -> str | dict[str, Any]:
        """Truncate an individual item's content."""
        if isinstance(item, str):
            if len(item) <= item_limit:
                return item
            truncated, _ = truncate_output(item, item_limit)
            return truncated
        elif isinstance(item, dict) and "content" in item:
            # Handle dict-style items (e.g., with metadata like file path and line number)
            if len(item["content"]) <= item_limit:
                return item
            truncated_content, _ = truncate_output(item["content"], item_limit)
            return {**item, "content": truncated_content}
        else:
            return item

    def truncate(self, result: _T) -> _T:
        if not hasattr(result, self.field_name):
            return result

        items = getattr(result, self.field_name)
        if not isinstance(items, list):
            return result

        total_items = len(items)
        # Limit the number of items first so the per-item budget is allocated
        # only across items that will actually be returned.
        if total_items > self.max_items:
            truncated_count = max(0, total_items - 2 * self.preview_items)
            kept_items = items[: self.preview_items] + items[-self.preview_items :]
            item_limit = self._effective_item_limit(len(kept_items))
            truncated_kept = [self._truncate_item_content(item, item_limit) for item in kept_items]
            final_items = (
                truncated_kept[: self.preview_items]
                + [f"... {truncated_count} items truncated ..."]
                + truncated_kept[self.preview_items :]
            )
        else:
            item_limit = self._effective_item_limit(total_items)
            final_items = [self._truncate_item_content(item, item_limit) for item in items]

        updates: dict[str, Any] = {self.field_name: final_items}
        if hasattr(result, "truncated"):
            updates["truncated"] = True

        return replace(result, **updates)


TRUNCATION_REGISTRY: dict[type[ToolResult], TruncationStrategy[Any]] = {
    ReadToolResult: StringFieldTruncation("content"),
    WriteToolResult: StringFieldTruncation("message"),
    GrepToolResult: StringListTruncation("matches", max_total_length=10_000),
    GlobToolResult: StringListTruncation("filenames", max_item_length=4096),
    BashToolResult: TailTruncation("output", character_limit=BASH_CHARACTER_LIMIT),
}


T = TypeVar("T", bound=ToolResult)


def truncate_tool_result(result: T) -> T:
    if isinstance(result, ErrorToolResult):
        return result

    result_type = type(result)
    if result_type in TRUNCATION_REGISTRY:
        strategy = TRUNCATION_REGISTRY[result_type]
        if isinstance(result, BashToolResult):
            return cast(T, strategy.truncate(result))
        elif strategy.should_truncate(result):
            return cast(T, strategy.truncate(result))

    return result
