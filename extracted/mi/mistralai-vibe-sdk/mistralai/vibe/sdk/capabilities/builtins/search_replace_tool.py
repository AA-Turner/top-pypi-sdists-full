import os
import stat
import tempfile
from contextlib import suppress
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, JsonValue, StringConstraints

from mistralai.vibe.sdk.capabilities import ToolResult, tool
from mistralai.vibe.sdk.capabilities.builtins.search_replace_preview import (
    preview_fits,
    replace_with_preview,
)
from mistralai.vibe.sdk.capabilities.builtins.text_file import read_text_file
from mistralai.vibe.sdk.capabilities.utils import resolve_path

MAX_EDIT_FILE_SIZE_BYTES = 512 * 1_024 * 1_024
SEARCH_REPLACE_ANNOTATION_KEY = "mistralai.vibe.sdk.search_replace"


class SearchReplaceBlock(BaseModel):
    old_str: str = Field(
        min_length=1,
        description=(
            "Exact text to replace. Must match the file including whitespace, indentation, "
            "and line endings, and be unique unless replace_all is set."
        ),
    )
    new_str: str = Field(description="Replacement text for this block.")
    replace_all: bool = Field(
        default=False,
        description="Replace every occurrence of old_str instead of requiring it to be unique.",
    )


class SearchReplaceArgs(BaseModel):
    file_path: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    content: list[SearchReplaceBlock] = Field(
        min_length=1,
        description="One or more search/replace blocks applied in order to file_path.",
    )


class SearchReplaceContext(BaseModel):
    max_file_size_bytes: int = Field(default=MAX_EDIT_FILE_SIZE_BYTES, gt=0)


class SearchReplaceResult(BaseModel):
    file: str
    lines_changed: int = Field(
        description="Sum of logical lines affected by the applied replacement blocks.",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-fatal conditions the caller may need to account for.",
    )


class SearchReplacePreviewBlock(BaseModel):
    old_start_line: int
    new_start_line: int
    old_lines: list[str]
    new_lines: list[str]


class SearchReplaceAnnotations(BaseModel):
    blocks: list[SearchReplacePreviewBlock]


@tool(
    name="search_replace",
    description=(
        "Edit an existing text file by applying one or more search/replace blocks. "
        "Each block's 'old_str' must match the file exactly (whitespace and indentation "
        "included) and be unique in the file; if it occurs more than once, add surrounding "
        "context or set 'replace_all' to change every occurrence. Blocks are applied in "
        "order. Prefer this over rewriting a whole file; use write_file to create new files."
    ),
    input_schema=SearchReplaceArgs,
    result_schema=SearchReplaceResult,
    ctx_schema=SearchReplaceContext,
    ctx=SearchReplaceContext(),
)
def search_replace(
    ctx: SearchReplaceContext,
    args: SearchReplaceArgs,
) -> ToolResult[SearchReplaceResult]:
    try:
        file_path = resolve_path(args.file_path)
    except (OSError, RuntimeError) as exc:
        raise ValueError(f"Error resolving path {args.file_path!r}: {exc}") from exc

    original, encoding = read_text_file(file_path, max_bytes=ctx.max_file_size_bytes)

    updated = original
    preview_blocks: list[SearchReplacePreviewBlock] = []
    lines_changed = 0
    warnings: list[str] = []
    for index, block in enumerate(args.content):
        if block.old_str == block.new_str:
            raise ValueError(f"block {index}: old_str and new_str must differ")

        matches = updated.count(block.old_str)
        if matches == 0:
            raise ValueError(f"block {index}: old_str not found in {file_path}")
        if matches > 1 and not block.replace_all:
            raise ValueError(
                f"block {index}: old_str is not unique — found {matches} times in {file_path}. "
                "Add surrounding context to identify a single occurrence, or set replace_all=true."
            )

        replacement_count = matches if block.replace_all else 1
        replacement = replace_with_preview(
            content=updated,
            old_str=block.old_str,
            new_str=block.new_str,
            count=replacement_count,
        )
        preview_blocks.extend(
            SearchReplacePreviewBlock(
                old_start_line=preview.old_start_line,
                new_start_line=preview.new_start_line,
                old_lines=preview.old_lines,
                new_lines=preview.new_lines,
            )
            for preview in replacement.previews
        )
        lines_changed += replacement.lines_changed
        updated = replacement.content

    file_changed = updated != original
    if not file_changed:
        warnings.append("search/replace blocks leave the file unchanged")

    annotation = SearchReplaceAnnotations(
        blocks=preview_blocks,
    )
    annotations: dict[str, JsonValue] = (
        {SEARCH_REPLACE_ANNOTATION_KEY: annotation.model_dump(mode="json")}
        if preview_fits(annotation.blocks)
        else {}
    )
    result = ToolResult(
        value=SearchReplaceResult(
            file=str(file_path),
            lines_changed=lines_changed,
            warnings=warnings,
        ),
        annotations=annotations,
    )

    if not file_changed:
        return result

    temporary_path: Path | None = None
    try:
        file_mode = stat.S_IMODE(file_path.stat().st_mode)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            errors="strict",
            newline="",
            dir=file_path.parent,
            prefix=f".{file_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(updated)
            handle.flush()
            os.fsync(handle.fileno())

        temporary_path.chmod(file_mode)
        os.replace(temporary_path, file_path)
        temporary_path = None
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"Error writing {file_path}: {exc}") from exc
    finally:
        if temporary_path is not None:
            with suppress(OSError):
                temporary_path.unlink(missing_ok=True)
    return result
