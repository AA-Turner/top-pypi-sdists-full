from __future__ import annotations

import fnmatch
import logging
import time
from collections.abc import Sequence
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from matrx_ai.tools._change_events import emit_fs_changed
from matrx_ai.tools._sandbox_proxy import (
    SandboxBinding,
    SandboxProxyError,
    get_active_sandbox,
)
from matrx_ai.tools._sandbox_proxy import (
    fs_list as _proxy_fs_list,
)
from matrx_ai.tools._sandbox_proxy import (
    fs_mkdir as _proxy_fs_mkdir,
)
from matrx_ai.tools._sandbox_proxy import (
    fs_patch as _proxy_fs_patch,
)
from matrx_ai.tools._sandbox_proxy import (
    fs_read as _proxy_fs_read,
)
from matrx_ai.tools._sandbox_proxy import (
    fs_search as _proxy_fs_search,
)
from matrx_ai.tools._sandbox_proxy import (
    fs_write as _proxy_fs_write,
)
from matrx_ai.tools._sandbox_runtime import scoped_base_for
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
    FileEditFailure,
    FileEditResult,
    FilePatchResult,
    FileReadResult,
    FileSearchMatch,
    FileSearchResults,
    FileWriteResult,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)

MAX_READ_SIZE = 1_048_576  # 1 MB
MAX_PATCH_SIZE = 5_242_880  # 5 MB hard cap on file size patches will touch
MAX_LIST_ENTRIES = 500


def _proxy_error(
    exc: SandboxProxyError | Exception,
    *,
    tool_name: str,
    call_id: str,
    started_at: float,
) -> ToolResult:
    """Translate a SandboxProxyError into a ToolResult so each fs_* tool
    can ``return _proxy_error(exc, ...)`` instead of re-mapping HTTP codes.
    """
    error_type = getattr(exc, "error_type", "sandbox_error")
    return ToolResult(
        success=False,
        error=ToolError(error_type=error_type, message=str(exc)),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


def _resolve_sandbox_path(binding: SandboxBinding, raw: str) -> str:
    """Resolve a target path without assuming the target operating system.

    The agent calls ``fs_list("aidream")`` expecting it to mean
    ``/home/agent/aidream`` (the workspace root). Rather than forcing the
    model to always produce absolute paths, we anchor relatives at the
    binding's ``root_path`` and accept ``""`` / ``"."`` / ``"./"`` as
    "the root itself". POSIX, Windows drive-letter, and UNC absolute paths
    pass through verbatim.  This resolver runs on the cloud server, so using
    ``os.path``/``Path`` would incorrectly apply the server OS's path rules to
    a Windows desktop target.
    """
    if not raw or raw in (".", "./", ".\\"):
        return binding.root_path
    windows_path = PureWindowsPath(raw)
    if windows_path.drive and not windows_path.is_absolute():
        raise SandboxProxyError(
            f"Drive-relative Windows path is ambiguous: {raw!r}",
            error_type="invalid_input",
        )
    if PurePosixPath(raw).is_absolute() or windows_path.is_absolute():
        return raw
    if raw.startswith(("~/", "~\\")):
        raw = raw[2:]

    root_as_windows = PureWindowsPath(binding.root_path)
    if root_as_windows.drive or "\\" in binding.root_path:
        return str(root_as_windows / PureWindowsPath(raw))
    return str(PurePosixPath(binding.root_path) / PurePosixPath(raw))


def _resolve_path(relative: str, ctx: ToolContext) -> Path:
    base = scoped_base_for(ctx.user_id, ctx.project_id)
    resolved = (base / relative).resolve()
    base_resolved = base.resolve()
    if not str(resolved).startswith(str(base_resolved)):
        # The agent gets the full picture: what they passed, where it
        # resolved to, what the workspace base actually is, and how to
        # recover. Common case: agent passed an absolute /home/agent/...
        # path expecting sandbox semantics, but the chat isn't bound to
        # a sandbox so we're in the multi-tenant /tmp/workspaces/<uid>/<pid>
        # layout. The remediation is to bind a sandbox.
        raise PermissionError(
            "Path escapes workspace.\n"
            f"  requested:        {relative}\n"
            f"  resolved to:      {resolved}\n"
            f"  workspace base:   {base_resolved}\n"
            "  recover by:\n"
            "    - binding a sandbox to this conversation (then absolute paths "
            "like /home/agent/aidream/... are valid — that's the sandbox's home)\n"
            "    - OR passing a path RELATIVE to the workspace base above\n"
            "    - OR using shell_execute if you need to read something outside "
            "the workspace (multi-tenant aidream still runs the file-system "
            "permission check; shell_execute follows POSIX permissions instead)"
        )
    return resolved


def _should_use_durable_vfs() -> bool:
    """No sandbox attached AND a host installed a durable VFS backend (aidream's code_files
    store) → serve fs/shell from the durable VFS instead of the ephemeral, host-coupled
    real-disk fallback under /tmp/workspaces. A sandbox always wins (real container); with
    no durable backend (standalone matrx-ai) this is False and behaviour is unchanged."""
    if get_active_sandbox() is not None:
        return False
    from matrx_ai.tools.vfs.workspace import has_durable_backend

    return has_durable_backend()


async def fs_read(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsReadArgs(**args)

    # No sandbox + a durable VFS backend → serve from the durable code_files filesystem.
    if _should_use_durable_vfs():
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_read(args, ctx)

    # Sandbox-bound chats: route to the matrx_agent inside the container
    # via the orchestrator. Same /fs/read endpoint the admin inspector
    # uses, so the agent's view is identical to the operator's view.
    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            read_limit = parsed.limit if parsed.limit > 0 else MAX_READ_SIZE
            page = await _proxy_fs_read(
                binding,
                sandbox_path,
                encoding="utf8",
                offset=parsed.offset,
                limit=read_limit,
            )
            return ToolResult(
                success=True,
                output=FileReadResult(
                    content=page.content,
                    size=page.size,
                    offset=page.offset,
                    limit=page.limit,
                    next_offset=page.next_offset,
                    truncated=page.truncated,
                    path=sandbox_path,
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_read",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_read", call_id=ctx.call_id, started_at=started_at
            )

    try:
        filepath = _resolve_path(parsed.path, ctx)
        if not filepath.exists():
            return ToolResult(
                success=False,
                error=ToolError(error_type="not_found", message=f"File not found: {parsed.path}"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_read",
                call_id=ctx.call_id,
            )

        size = filepath.stat().st_size
        read_limit = parsed.limit if parsed.limit > 0 else MAX_READ_SIZE
        truncated = size > read_limit

        with open(filepath, errors="replace") as f:
            if parsed.offset:
                f.seek(parsed.offset)
            content = f.read(read_limit)

        return ToolResult(
            success=True,
            output=FileReadResult(
                content=content,
                size=size,
                truncated=truncated,
                path=parsed.path,
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_read",
            call_id=ctx.call_id,
        )
    except PermissionError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="permission", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_read",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="filesystem", message=f"Read failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_read",
            call_id=ctx.call_id,
        )


async def fs_write(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsWriteArgs(**args)
    if _should_use_durable_vfs():
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_write(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            # The matrx_agent /fs/write replaces the file. ``append`` mode
            # has no direct daemon equivalent — fall back to read+append+write
            # so the public tool contract still works.
            content = parsed.content
            if parsed.append:
                try:
                    chunks: list[str] = []
                    offset = 0
                    while True:
                        page = await _proxy_fs_read(
                            binding,
                            sandbox_path,
                            encoding="utf8",
                            offset=offset,
                            limit=MAX_READ_SIZE,
                        )
                        chunks.append(page.content)
                        if not page.truncated:
                            break
                        if page.next_offset <= offset:
                            raise SandboxProxyError(
                                "Sandbox read pagination did not advance",
                                error_type="protocol_error",
                            )
                        offset = page.next_offset
                    existing = "".join(chunks)
                except SandboxProxyError as exc:
                    if exc.status != 404:
                        raise
                    existing = ""
                content = existing + parsed.content
            stat = await _proxy_fs_write(
                binding,
                sandbox_path,
                content,
                encoding="utf8",
                create_parents=parsed.create_dirs,
            )
            await emit_fs_changed(
                action="modified",
                path=sandbox_path,
                metadata={"size": stat.get("size"), "tool": "fs_write"},
            )
            return ToolResult(
                success=True,
                output=FileWriteResult(
                    path=sandbox_path, size=stat.get("size"), stat=stat
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_write",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_write", call_id=ctx.call_id, started_at=started_at
            )

    try:
        filepath = _resolve_path(parsed.path, ctx)
        existed_before = filepath.exists()
        if parsed.create_dirs:
            filepath.parent.mkdir(parents=True, exist_ok=True)

        mode = "a" if parsed.append else "w"
        with open(filepath, mode) as f:
            f.write(parsed.content)

        new_size = filepath.stat().st_size
        await emit_fs_changed(
            action="modified" if existed_before else "created",
            path=str(filepath),
            metadata={
                "size": new_size,
                "mode": "append" if parsed.append else "write",
                "mtime": filepath.stat().st_mtime,
            },
        )

        return ToolResult(
            success=True,
            output=FileWriteResult(
                path=parsed.path,
                bytes_written=len(parsed.content.encode()),
                mode="append" if parsed.append else "write",
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_write",
            call_id=ctx.call_id,
        )
    except PermissionError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="permission", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_write",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="filesystem", message=f"Write failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_write",
            call_id=ctx.call_id,
        )


async def fs_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsListArgs(**args)
    if _should_use_durable_vfs():
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_list(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            data = await _proxy_fs_list(
                binding,
                sandbox_path,
                recursive=parsed.recursive,
                # The shared proxy contract currently caps recursion depth at
                # 10.  Non-recursive remains depth 1.
                depth=10 if parsed.recursive else 1,
                pattern=parsed.pattern or None,
                limit=MAX_LIST_ENTRIES,
                page_token=None,
            )
            server_filtered = "truncated" in data or "nextPageToken" in data
            entries: list[dict[str, Any]] = []
            for e in data.get("entries", []):
                # matrx_agent uses {kind: "file"|"dir"|"symlink"}; matrx-ai's
                # local impl uses {is_dir: bool}. Normalize so consumers see
                # the same shape regardless of where the listing came from.
                kind = e.get("kind")
                name = e.get("name") or (e.get("path") or "").replace("\\", "/").rsplit("/", 1)[-1]
                entry_path = e.get("path") or ""
                if parsed.pattern and not server_filtered and not (
                    fnmatch.fnmatch(name, parsed.pattern)
                    or fnmatch.fnmatch(entry_path.replace("\\", "/"), parsed.pattern)
                ):
                    continue
                entries.append(
                    {
                        "name": name,
                        "path": entry_path,
                        "is_dir": kind == "dir" if kind is not None else bool(e.get("is_dir")),
                        "size": e.get("size"),
                        "mtime": e.get("mtime"),
                    }
                )
            return ToolResult(
                success=True,
                output=DirectoryListing(
                    entries=[DirectoryEntry(**e) for e in entries],
                    count=len(entries),
                    path=sandbox_path,
                    recursive=parsed.recursive,
                    pattern=parsed.pattern or None,
                    limit=MAX_LIST_ENTRIES,
                    truncated=bool(data.get("truncated", False)),
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_list",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_list", call_id=ctx.call_id, started_at=started_at
            )

    try:
        dirpath = _resolve_path(parsed.path, ctx)
        if not dirpath.is_dir():
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"Directory not found: {parsed.path}",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_list",
                call_id=ctx.call_id,
            )

        entries: list[dict[str, Any]] = []
        iterator = dirpath.rglob("*") if parsed.recursive else dirpath.iterdir()
        for entry in iterator:
            if parsed.pattern and not fnmatch.fnmatch(entry.name, parsed.pattern):
                continue
            entries.append(
                {
                    "name": entry.name,
                    "path": str(entry.relative_to(dirpath)),
                    "is_dir": entry.is_dir(),
                    "size": entry.stat().st_size if entry.is_file() else 0,
                }
            )
            if len(entries) >= 500:
                break

        return ToolResult(
            success=True,
            output=DirectoryListing(
                entries=[DirectoryEntry(**e) for e in entries],
                count=len(entries),
                path=parsed.path,
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_list",
            call_id=ctx.call_id,
        )
    except PermissionError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="permission", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_list",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="filesystem", message=f"List failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_list",
            call_id=ctx.call_id,
        )


async def fs_search(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsSearchArgs(**args)
    if _should_use_durable_vfs():
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_search(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            data = await _proxy_fs_search(
                binding,
                parsed.pattern,
                path=sandbox_path,
                content_search=parsed.content_search,
                max_results=parsed.max_results,
            )
            return ToolResult(
                success=True,
                output=FileSearchResults(
                    results=[FileSearchMatch(**r) for r in data.get("results", [])],
                    count=len(data.get("results", [])),
                    pattern=parsed.pattern,
                    path=sandbox_path,
                    content_search=parsed.content_search,
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_search",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_search", call_id=ctx.call_id, started_at=started_at
            )

    try:
        basepath = _resolve_path(parsed.path, ctx)
        if not basepath.is_dir():
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"Directory not found: {parsed.path}",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_search",
                call_id=ctx.call_id,
            )

        results: list[dict[str, Any]] = []
        import re

        for entry in basepath.rglob("*"):
            if len(results) >= parsed.max_results:
                break
            if entry.is_dir():
                continue

            if parsed.content_search:
                try:
                    content = entry.read_text(errors="replace")[:50000]
                    matches = [m.group() for m in re.finditer(parsed.pattern, content)]
                    if matches:
                        results.append(
                            {
                                "path": str(entry.relative_to(basepath)),
                                "matches": matches[:10],
                            }
                        )
                except Exception:
                    continue
            else:
                if fnmatch.fnmatch(entry.name, parsed.pattern):
                    results.append(
                        {
                            "path": str(entry.relative_to(basepath)),
                            "size": entry.stat().st_size,
                        }
                    )

        return ToolResult(
            success=True,
            output=FileSearchResults(
                results=[FileSearchMatch(**r) for r in results],
                count=len(results),
                content_search=parsed.content_search,
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_search",
            call_id=ctx.call_id,
        )
    except PermissionError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="permission", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_search",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="filesystem", message=f"Search failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_search",
            call_id=ctx.call_id,
        )


async def fs_patch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Anchor-based file edit — apply 1-N old_text→new_text edits in order.

    The single most useful coding tool for an LLM agent. Models reliably
    produce small "find this exact block, replace with this exact block"
    edits; they're notoriously bad at re-emitting an entire file or at
    composing multi-line shell heredocs. fs_patch leans into that strength.

    Failure modes are surfaced explicitly so the caller can recover:
      - old_text not found  → "edit_index N: old_text not found"
      - old_text not unique → "edit_index N: matches K times — add context or replace_all=True"
    Edits that succeed are committed as a single atomic write only when at
    least one edit succeeded; if every edit failed the file is untouched.
    """
    started_at = time.time()
    parsed = FsPatchArgs(**args)
    if _should_use_durable_vfs():
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_patch(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            edits = [
                {"old_text": e.old_text, "new_text": e.new_text, "replace_all": e.replace_all}
                for e in parsed.edits
            ]
            data = await _proxy_fs_patch(
                binding,
                sandbox_path,
                edits,
                create_if_missing=parsed.create_if_missing,
            )
            await emit_fs_changed(
                action="modified",
                path=sandbox_path,
                metadata={"tool": "fs_patch", "edits": len(edits)},
            )
            return ToolResult(
                success=True,
                output=FilePatchResult(
                    path=sandbox_path,
                    created=bool(data.get("created", False)),
                    edits_applied=[
                        FileEditApplied(**s) for s in data.get("edits_applied", [])
                    ],
                    edits_failed=[
                        FileEditFailure(**f) for f in data.get("edits_failed", [])
                    ],
                    size_before=int(data.get("size_before", 0) or 0),
                    size_after=int(data.get("size_after", 0) or 0),
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_patch",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_patch", call_id=ctx.call_id, started_at=started_at
            )

    try:
        filepath = _resolve_path(parsed.path, ctx)
        existed = filepath.exists()

        if not existed:
            if not parsed.create_if_missing:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="not_found",
                        message=f"File not found: {parsed.path}",
                        suggested_action="Set create_if_missing=True to create the file with the patch's first edit.",
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="fs_patch",
                    call_id=ctx.call_id,
                )
            first = parsed.edits[0]
            if first.old_text != "":
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="invalid_input",
                        message="create_if_missing=True requires the first edit to have empty old_text (insert mode).",
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="fs_patch",
                    call_id=ctx.call_id,
                )
            content = ""
        else:
            size = filepath.stat().st_size
            if size > MAX_PATCH_SIZE:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="too_large",
                        message=f"File is {size} bytes; fs_patch refuses files over {MAX_PATCH_SIZE}.",
                        suggested_action="Use shell_execute with sed/awk/perl for very large files.",
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="fs_patch",
                    call_id=ctx.call_id,
                )
            content = filepath.read_text()

        original_content = content
        content, applied_summaries, failures = apply_patch_edits(
            content, parsed.edits, existed=existed
        )

        if not applied_summaries:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="patch_failed",
                    message=f"All {len(parsed.edits)} edit(s) failed; file unchanged.",
                ),
                output={"failures": failures, "path": parsed.path},
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_patch",
                call_id=ctx.call_id,
            )

        if not existed:
            filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)

        await emit_fs_changed(
            action="created" if not existed else "modified",
            path=str(filepath),
            metadata={
                "size": len(content),
                "edits_applied": len(applied_summaries),
                "edits_failed": len(failures),
                "mtime": filepath.stat().st_mtime,
            },
        )

        return ToolResult(
            success=True,
            output=FilePatchResult(
                path=parsed.path,
                created=not existed,
                edits_applied=[FileEditApplied(**s) for s in applied_summaries],
                edits_failed=[FileEditFailure(**f) for f in failures],
                size_before=len(original_content),
                size_after=len(content),
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_patch",
            call_id=ctx.call_id,
        )

    except PermissionError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="permission", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_patch",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="filesystem", message=f"Patch failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_patch",
            call_id=ctx.call_id,
        )


async def fs_edit(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Edit a file by a single exact string replacement (old_str → new_str).

    A focused, single-edit companion to fs_patch: read the file, replace one
    exact substring, write it back. The match must be unique unless
    replace_all=True. Mirrors fs_patch's sandbox-delegation + local-disk
    behavior so it is ALWAYS available, independent of the MATRX_VFS_ENABLED
    flag (previously fs_edit only existed in the VFS layer, so on non-VFS
    servers the sandbox surface requested it and the registry dropped it).
    """
    started_at = time.time()
    parsed = FsEditArgs(**args)
    if _should_use_durable_vfs():
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_edit(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            # The sandbox daemon has no /fs/edit endpoint; fs_edit is a
            # single-edit fs_patch, so reuse the daemon's patch path verbatim.
            data = await _proxy_fs_patch(
                binding,
                sandbox_path,
                [
                    {
                        "old_text": parsed.old_str,
                        "new_text": parsed.new_str,
                        "replace_all": parsed.replace_all,
                    }
                ],
            )
            await emit_fs_changed(
                action="modified",
                path=sandbox_path,
                metadata={"tool": "fs_edit"},
            )
            return ToolResult(
                success=True,
                output=FileEditResult(
                    path=sandbox_path,
                    old_str_count=int(data.get("old_str_count", 0) or 0),
                    replaced=int(data.get("replaced", 0) or 0),
                    size_before=int(data.get("size_before", 0) or 0),
                    size_after=int(data.get("size_after", 0) or 0),
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_edit",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_edit", call_id=ctx.call_id, started_at=started_at
            )

    try:
        filepath = _resolve_path(parsed.path, ctx)
        if not filepath.exists():
            return ToolResult(
                success=False,
                error=ToolError(error_type="not_found", message=f"File not found: {parsed.path}"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_edit",
                call_id=ctx.call_id,
            )
        if filepath.is_dir():
            return ToolResult(
                success=False,
                error=ToolError(error_type="filesystem", message=f"Is a directory: {parsed.path}"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_edit",
                call_id=ctx.call_id,
            )
        size = filepath.stat().st_size
        if size > MAX_PATCH_SIZE:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="too_large",
                    message=f"File is {size} bytes; fs_edit refuses files over {MAX_PATCH_SIZE}.",
                    suggested_action="Use shell_execute with sed/awk/perl for very large files.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_edit",
                call_id=ctx.call_id,
            )

        content = filepath.read_text()
        count = content.count(parsed.old_str)
        if count == 0:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message="old_str not found in file.",
                    suggested_action="Copy the exact text to replace, including whitespace and indentation.",
                ),
                output={"path": parsed.path, "old_str_preview": _preview(parsed.old_str)},
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_edit",
                call_id=ctx.call_id,
            )
        if count > 1 and not parsed.replace_all:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=(
                        f"old_str matches {count} locations — add surrounding context to "
                        f"make it unique, or set replace_all=True to update every match."
                    ),
                ),
                output={"path": parsed.path, "old_str_count": count},
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_edit",
                call_id=ctx.call_id,
            )

        if parsed.replace_all:
            new_content = content.replace(parsed.old_str, parsed.new_str)
            replaced = count
        else:
            new_content = content.replace(parsed.old_str, parsed.new_str, 1)
            replaced = 1

        filepath.write_text(new_content)
        await emit_fs_changed(
            action="modified",
            path=str(filepath),
            metadata={
                "size": len(new_content),
                "tool": "fs_edit",
                "replaced": replaced,
                "mtime": filepath.stat().st_mtime,
            },
        )
        return ToolResult(
            success=True,
            output=FileEditResult(
                path=parsed.path,
                old_str_count=count,
                replaced=replaced,
                size_before=len(content),
                size_after=len(new_content),
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_edit",
            call_id=ctx.call_id,
        )
    except PermissionError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="permission", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_edit",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="filesystem", message=f"Edit failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_edit",
            call_id=ctx.call_id,
        )


def _preview(text: str, limit: int = 160) -> str:
    """Truncate a snippet for inclusion in error responses without dumping a whole block."""
    snippet = text.strip().splitlines()[0] if text else ""
    return (snippet[:limit] + "…") if len(snippet) > limit else snippet


def apply_patch_edits(
    content: str,
    edits: Sequence[Any],
    *,
    existed: bool,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply an ordered list of ``FsPatchEdit``s to ``content`` — backend-agnostic.

    Pure string work: no filesystem, no VFS, no I/O. Both ``fs_patch`` branches
    (local disk and the durable VFS in ``vfs_filesystem``) run THIS function, so
    the two backends cannot drift in what an edit means or how a failure reads.

    Returns ``(new_content, applied_summaries, failures)``. An empty
    ``applied_summaries`` means nothing applied and the caller must NOT write.
    """
    applied_summaries: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for i, edit in enumerate(edits):
        if not existed and i == 0 and edit.old_text == "":
            content = edit.new_text
            applied_summaries.append(
                {
                    "edit_index": i,
                    "mode": "create",
                    "added_chars": len(edit.new_text),
                }
            )
            continue

        count = content.count(edit.old_text)
        if count == 0:
            failures.append(
                {
                    "edit_index": i,
                    "reason": "old_text not found in current file content",
                    "old_text_preview": _preview(edit.old_text),
                }
            )
            continue
        if count > 1 and not edit.replace_all:
            failures.append(
                {
                    "edit_index": i,
                    "reason": (
                        f"old_text matches {count} locations — add surrounding context "
                        f"to make it unique, or set replace_all=True to update every match."
                    ),
                    "old_text_preview": _preview(edit.old_text),
                }
            )
            continue

        if edit.replace_all:
            content = content.replace(edit.old_text, edit.new_text)
            applied_summaries.append(
                {
                    "edit_index": i,
                    "mode": "replace_all",
                    "matches_replaced": count,
                    "delta_chars": (len(edit.new_text) - len(edit.old_text)) * count,
                }
            )
        else:
            content = content.replace(edit.old_text, edit.new_text, 1)
            applied_summaries.append(
                {
                    "edit_index": i,
                    "mode": "replace",
                    "delta_chars": len(edit.new_text) - len(edit.old_text),
                }
            )

    return content, applied_summaries, failures


async def fs_mkdir(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsMkdirArgs(**args)
    if _should_use_durable_vfs():
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_mkdir(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            data = await _proxy_fs_mkdir(binding, sandbox_path, parents=parsed.parents)
            await emit_fs_changed(
                action="created",
                path=sandbox_path,
                metadata={"tool": "fs_mkdir"},
            )
            return ToolResult(
                success=True,
                output=DirectoryCreateResult(
                    path=sandbox_path,
                    created=str(
                        (data or {}).get("created", sandbox_path)
                        if isinstance(data, dict)
                        else sandbox_path
                    ),
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_mkdir",
                call_id=ctx.call_id,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_mkdir", call_id=ctx.call_id, started_at=started_at
            )

    try:
        dirpath = _resolve_path(parsed.path, ctx)
        existed_before = dirpath.exists()
        dirpath.mkdir(parents=parsed.parents, exist_ok=True)

        if not existed_before:
            await emit_fs_changed(
                action="created",
                path=str(dirpath),
                is_dir=True,
                metadata={"parents": parsed.parents},
            )

        return ToolResult(
            success=True,
            output=DirectoryCreateResult(created=str(parsed.path)).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_mkdir",
            call_id=ctx.call_id,
        )
    except PermissionError as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="permission", message=str(exc)),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_mkdir",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="filesystem", message=f"Mkdir failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_mkdir",
            call_id=ctx.call_id,
        )
