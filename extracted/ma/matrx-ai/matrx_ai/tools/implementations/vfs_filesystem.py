from __future__ import annotations

import fnmatch
import re
import time
from typing import Any

from matrx_ai.tools.arg_models.fs_args import (
    FsEditArgs,
    FsListArgs,
    FsMkdirArgs,
    FsPatchArgs,
    FsReadArgs,
    FsSearchArgs,
    FsWriteArgs,
)
from matrx_ai.tools.kinds.filesystem import (
    DirectoryCreateResult,
    DirectoryEntry,
    DirectoryListing,
    FileEditApplied,
    FileEditResult,
    FilePatchResult,
    FileReadResult,
    FileSearchMatch,
    FileSearchResults,
    FileWriteResult,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult
from matrx_ai.tools.output_caps import cap_json_list
from matrx_ai.tools.vfs.mimicry import claude_tool
from matrx_ai.tools.vfs.paths import dirname, join, normalize
from matrx_ai.tools.vfs.workspace import get_workspace_fs

MAX_READ_SIZE = 1_048_576  # 1 MB
MAX_LIST_ENTRIES = 500
MAX_PATCH_SIZE = 5_242_880  # 5 MB — same cap the local-disk fs_patch enforces
MAX_LIST_OUTPUT_CHARS = 40_000


def _abs(path: str) -> str:
    return path if path.startswith("/") else "/" + path


def _err(
    started_at: float,
    ctx: ToolContext,
    tool_name: str,
    error_type: str,
    message: str,
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type=error_type, message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=ctx.call_id,
    )


def _ok(
    started_at: float,
    ctx: ToolContext,
    tool_name: str,
    output: Any,
) -> ToolResult:
    return ToolResult(
        success=True,
        output=output,
        output_self_capped=tool_name == "fs_list",
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=ctx.call_id,
    )


async def fs_read(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsReadArgs(**args)
    vfs = await get_workspace_fs(ctx)
    path = _abs(parsed.path)

    try:
        data = await vfs._cat_file(path)
    except FileNotFoundError:
        return _err(started_at, ctx, "fs_read", "not_found", f"File not found: {parsed.path}")
    except IsADirectoryError:
        return _err(started_at, ctx, "fs_read", "filesystem", f"Is a directory: {parsed.path}")
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_read", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_read", "filesystem", f"Read failed: {exc}")

    from matrx_ai.tools.implementations.filesystem import FS_READ_MAX_CHARS

    full_size = len(data)
    start = min(parsed.offset, full_size)
    read_limit = min(parsed.limit, FS_READ_MAX_CHARS) if parsed.limit > 0 else FS_READ_MAX_CHARS
    end = min(full_size, start + read_limit)
    # Never split a UTF-8 sequence at the page edge (next_offset is a byte offset).
    while end < full_size and end > start and (data[end] & 0xC0) == 0x80:
        end -= 1
    truncated = end < full_size

    text = data[start:end].decode("utf-8", errors="replace")
    result = _ok(
        started_at,
        ctx,
        "fs_read",
        FileReadResult(
            content=text,
            size=full_size,
            truncated=truncated,
            offset=start,
            limit=read_limit,
            next_offset=end if truncated else None,
            path=parsed.path,
        ).model_dump(mode="json"),
    )
    result.output_self_capped = True
    return result


async def fs_write(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools.implementations.filesystem import decode_prior, with_file_surface_write

    started_at = time.time()
    parsed = FsWriteArgs(**args)
    vfs = await get_workspace_fs(ctx)
    path = _abs(parsed.path)

    try:
        if parsed.create_dirs:
            parent = dirname(path)
            if parent and parent != "/":
                await vfs._makedirs(parent, exist_ok=True)

        # The prior content is the receipt's "before" (and append's base).
        existed = True
        try:
            existing = await vfs._cat_file(path)
        except FileNotFoundError:
            existing = b""
            existed = False
        before = decode_prior(existing)

        content_bytes = parsed.content.encode("utf-8")
        if parsed.append:
            content_bytes = existing + content_bytes

        await vfs._pipe_file(path, content_bytes)
    except IsADirectoryError:
        return _err(started_at, ctx, "fs_write", "filesystem", f"Is a directory: {parsed.path}")
    except NotADirectoryError as exc:
        return _err(started_at, ctx, "fs_write", "filesystem", str(exc))
    except FileNotFoundError as exc:
        # Parent missing and create_dirs=False
        return _err(started_at, ctx, "fs_write", "not_found", str(exc))
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_write", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_write", "filesystem", f"Write failed: {exc}")

    return with_file_surface_write(
        _ok(
            started_at,
            ctx,
            "fs_write",
            FileWriteResult(
                path=parsed.path,
                bytes_written=len(parsed.content.encode("utf-8")),
                mode="append" if parsed.append else "write",
            ).model_dump(mode="json"),
        ),
        path=parsed.path,
        before=before,
        after=(before + parsed.content) if (parsed.append and before is not None) else parsed.content,
        mode="append" if parsed.append else "overwrite",
        existed=existed,
    )


async def fs_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsListArgs(**args)
    vfs = await get_workspace_fs(ctx)
    path = _abs(parsed.path)

    try:
        if not await vfs._isdir(path):
            return _err(
                started_at,
                ctx,
                "fs_list",
                "not_found",
                f"Directory not found: {parsed.path}",
            )

        entries: list[dict[str, Any]] = []
        entry_limit_reached = False
        pattern = parsed.pattern or None

        if parsed.recursive:
            async for root, _dirs, files in vfs._walk(path, topdown=True):
                rel_root = _relative(root, path)
                # Include subdirectories themselves
                listing = await vfs._ls(root, detail=True)
                for info in listing:
                    name = info["name"].rsplit("/", 1)[-1]
                    if pattern and not fnmatch.fnmatch(name, pattern):
                        continue
                    rel_path = name if rel_root in ("", ".") else f"{rel_root}/{name}"
                    entries.append(
                        {
                            "name": name,
                            "path": rel_path,
                            "is_dir": info["type"] == "directory",
                            "size": info["size"] if info["type"] == "file" else 0,
                        }
                    )
                    if len(entries) > MAX_LIST_ENTRIES:
                        entries.pop()
                        entry_limit_reached = True
                        break
                _ = files  # used by _walk filter — not needed here
                if entry_limit_reached:
                    break
        else:
            listing = await vfs._ls(path, detail=True)
            for info in listing:
                name = info["name"].rsplit("/", 1)[-1]
                if pattern and not fnmatch.fnmatch(name, pattern):
                    continue
                entries.append(
                    {
                        "name": name,
                        "path": name,
                        "is_dir": info["type"] == "directory",
                        "size": info["size"] if info["type"] == "file" else 0,
                    }
                )
                if len(entries) > MAX_LIST_ENTRIES:
                    entries.pop()
                    entry_limit_reached = True
                    break
    except NotADirectoryError as exc:
        return _err(started_at, ctx, "fs_list", "filesystem", str(exc))
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_list", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_list", "filesystem", f"List failed: {exc}")

    shown, cap = cap_json_list(entries, max_chars=MAX_LIST_OUTPUT_CHARS)
    return _ok(
        started_at,
        ctx,
        "fs_list",
        DirectoryListing(
            entries=[DirectoryEntry(**entry) for entry in shown],
            count=len(shown),
            path=parsed.path,
            limit=MAX_LIST_ENTRIES,
            truncated=entry_limit_reached or cap.truncated,
        ).model_dump(mode="json"),
    )


def _relative(absolute: str, base: str) -> str:
    a = normalize(absolute)
    b = normalize(base)
    if a == b:
        return "."
    if b == "/":
        return a[1:] if a.startswith("/") else a
    if a.startswith(b + "/"):
        return a[len(b) + 1 :]
    return a


async def fs_search(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsSearchArgs(**args)
    vfs = await get_workspace_fs(ctx)
    base = _abs(parsed.path)

    try:
        if not await vfs._isdir(base):
            return _err(
                started_at,
                ctx,
                "fs_search",
                "not_found",
                f"Directory not found: {parsed.path}",
            )

        results: list[dict[str, Any]] = []

        if parsed.content_search:
            try:
                content_re = re.compile(parsed.pattern)
            except re.error as exc:
                return _err(
                    started_at,
                    ctx,
                    "fs_search",
                    "validation",
                    f"Invalid regex: {exc}",
                )
            async for root, _dirs, files in vfs._walk(base, topdown=True):
                for fname in files:
                    if len(results) >= parsed.max_results:
                        break
                    full = join(root, fname)
                    try:
                        data = await vfs._cat_file(full)
                    except OSError:
                        continue
                    text = data.decode("utf-8", errors="replace")[:50000]
                    matches = [m.group() for m in content_re.finditer(text)]
                    if matches:
                        results.append(
                            {
                                "path": _relative(full, base),
                                "matches": matches[:10],
                            }
                        )
                if len(results) >= parsed.max_results:
                    break
        else:
            async for root, _dirs, files in vfs._walk(base, topdown=True):
                for fname in files:
                    if len(results) >= parsed.max_results:
                        break
                    if not fnmatch.fnmatch(fname, parsed.pattern):
                        continue
                    full = join(root, fname)
                    try:
                        info = await vfs._info(full)
                    except OSError:
                        continue
                    results.append(
                        {
                            "path": _relative(full, base),
                            "size": info["size"],
                        }
                    )
                if len(results) >= parsed.max_results:
                    break
    except NotADirectoryError as exc:
        return _err(started_at, ctx, "fs_search", "filesystem", str(exc))
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_search", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_search", "filesystem", f"Search failed: {exc}")

    return _ok(
        started_at,
        ctx,
        "fs_search",
        FileSearchResults(
            results=[FileSearchMatch(**r) for r in results],
            count=len(results),
            content_search=parsed.content_search,
        ).model_dump(mode="json"),
    )


async def fs_mkdir(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsMkdirArgs(**args)
    vfs = await get_workspace_fs(ctx)
    path = _abs(parsed.path)

    try:
        if parsed.parents:
            await vfs._makedirs(path, exist_ok=True)
        else:
            await vfs._mkdir(path, create_parents=False)
    except FileExistsError:
        return _err(
            started_at,
            ctx,
            "fs_mkdir",
            "filesystem",
            f"Directory already exists: {parsed.path}",
        )
    except FileNotFoundError as exc:
        return _err(started_at, ctx, "fs_mkdir", "not_found", str(exc))
    except NotADirectoryError as exc:
        return _err(started_at, ctx, "fs_mkdir", "filesystem", str(exc))
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_mkdir", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_mkdir", "filesystem", f"Mkdir failed: {exc}")

    return _ok(
        started_at,
        ctx,
        "fs_mkdir",
        DirectoryCreateResult(created=parsed.path).model_dump(mode="json"),
    )


async def fs_edit(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """``fs_edit`` against the durable VFS — a one-edit ``fs_patch``, same contract."""
    from matrx_ai.tools.implementations.filesystem import (
        apply_patch_edits,
        decode_prior,
        edit_as_patch,
        edit_counts,
        patch_failure_result,
        with_file_surface_write,
    )

    started_at = time.time()
    parsed = FsEditArgs(**args)
    vfs = await get_workspace_fs(ctx)
    path = _abs(parsed.path)

    try:
        data = await vfs._cat_file(path)
    except FileNotFoundError:
        return _err(started_at, ctx, "fs_edit", "not_found", claude_tool.edit_not_found())
    except IsADirectoryError:
        return _err(started_at, ctx, "fs_edit", "filesystem", f"Is a directory: {parsed.path}")
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_edit", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_edit", "filesystem", f"Read failed: {exc}")

    before = decode_prior(data)
    text = before if before is not None else data.decode("utf-8", errors="replace")
    new_text, applied, failures = apply_patch_edits(
        text, edit_as_patch(parsed).edits, existed=True
    )
    if failures:
        return patch_failure_result(
            failures,
            tool_name="fs_edit",
            path=parsed.path,
            total_edits=1,
            call_id=ctx.call_id,
            started_at=started_at,
        )
    count, replaced = edit_counts(applied)

    try:
        await vfs._pipe_file(path, new_text.encode("utf-8"))
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_edit", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_edit", "filesystem", f"Write failed: {exc}")

    return with_file_surface_write(
        _ok(
            started_at,
            ctx,
            "fs_edit",
            FileEditResult(
                path=parsed.path,
                old_str_count=count,
                replaced=replaced,
                size_before=len(text),
                size_after=len(new_text),
            ).model_dump(mode="json"),
        ),
        path=parsed.path,
        before=before,
        after=new_text if before is not None else None,
        mode="patch",
        edits=1,
    )


async def fs_patch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """``fs_patch`` against the durable VFS — the same tool as the local-disk one.

    The multi-edit apply/failure logic is shared with the local branch
    (``filesystem.apply_patch_edits``); only the read and the write change.
    All-or-nothing: any failing edit writes nothing. Imported lazily because
    ``filesystem`` dispatches INTO this module.
    """
    from matrx_ai.tools.implementations.filesystem import (
        apply_patch_edits,
        decode_prior,
        patch_failure_result,
        with_file_surface_write,
    )

    started_at = time.time()
    parsed = FsPatchArgs(**args)
    vfs = await get_workspace_fs(ctx)
    path = _abs(parsed.path)

    existed = True
    try:
        data = await vfs._cat_file(path)
    except FileNotFoundError:
        existed = False
        data = b""
    except IsADirectoryError:
        return _err(started_at, ctx, "fs_patch", "filesystem", f"Is a directory: {parsed.path}")
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_patch", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_patch", "filesystem", f"Read failed: {exc}")

    if not existed:
        if not parsed.create_if_missing:
            return _err(
                started_at, ctx, "fs_patch", "not_found", f"File not found: {parsed.path}"
            )
        if parsed.edits[0].old_text != "":
            return _err(
                started_at,
                ctx,
                "fs_patch",
                "invalid_input",
                "create_if_missing=True requires the first edit to have empty old_text (insert mode).",
            )

    if len(data) > MAX_PATCH_SIZE:
        return _err(
            started_at,
            ctx,
            "fs_patch",
            "too_large",
            f"File is {len(data)} bytes; fs_patch refuses files over {MAX_PATCH_SIZE}.",
        )

    before = decode_prior(data)
    original_content = before if before is not None else data.decode("utf-8", errors="replace")
    content, applied_summaries, failures = apply_patch_edits(
        original_content, parsed.edits, existed=existed
    )

    if failures:
        return patch_failure_result(
            failures,
            tool_name="fs_patch",
            path=parsed.path,
            total_edits=len(parsed.edits),
            call_id=ctx.call_id,
            started_at=started_at,
        )

    try:
        if not existed:
            parent = dirname(path)
            if parent and parent != "/":
                await vfs._makedirs(parent, exist_ok=True)
        await vfs._pipe_file(path, content.encode("utf-8"))
    except PermissionError as exc:
        return _err(started_at, ctx, "fs_patch", "permission", str(exc))
    except OSError as exc:
        return _err(started_at, ctx, "fs_patch", "filesystem", f"Write failed: {exc}")

    return with_file_surface_write(
        _ok(
            started_at,
            ctx,
            "fs_patch",
            FilePatchResult(
                path=parsed.path,
                created=not existed,
                edits_applied=[FileEditApplied(**s) for s in applied_summaries],
                edits_failed=[],
                size_before=len(original_content),
                size_after=len(content),
            ).model_dump(mode="json"),
        ),
        path=parsed.path,
        before=before,
        after=content if before is not None else None,
        mode="patch",
        edits=len(applied_summaries),
    )


__all__ = [
    "fs_edit",
    "fs_list",
    "fs_mkdir",
    "fs_patch",
    "fs_read",
    "fs_search",
    "fs_write",
]
