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
    FsPatchEdit,
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
from matrx_ai.tools.surface_write import (
    SurfaceWriteFormat,
    SurfaceWriteMode,
    attach_surface_write,
)

logger = logging.getLogger(__name__)

MAX_READ_SIZE = 1_048_576  # 1 MB
#: The most one ``fs_read`` result carries (chars/bytes of file content). Under
#: the size gate's 50K soft cap with room for the envelope, so the result is
#: honestly ``output_self_capped``. Production (ops ``tool_result_overflow:fs_read``):
#: page.html 423,130; content-splitter-v2.ts 76,087; limit=60000 → 53K. A larger
#: ``limit`` is clamped; ``truncated`` + ``next_offset`` say where to continue.
FS_READ_MAX_CHARS = 40_000
MAX_PATCH_SIZE = 5_242_880  # 5 MB hard cap on file size patches will touch
MAX_LIST_ENTRIES = 500
# Keep ample headroom for the listing envelope while staying below the universal
# 50K result gate. Paths are user-controlled and a 500-row count cap alone is
# not a character bound.
MAX_LIST_OUTPUT_CHARS = 40_000


def _bounded_listing(
    *,
    entries: list[dict[str, Any]],
    path: str,
    recursive: bool | None = None,
    pattern: str | None = None,
    limit: int | None = None,
    truncated: bool = False,
) -> DirectoryListing:
    """Build an honest, provider-safe directory listing from compact entries."""
    shown, cap = cap_json_list(entries, max_chars=MAX_LIST_OUTPUT_CHARS)
    return DirectoryListing(
        entries=[DirectoryEntry(**entry) for entry in shown],
        count=len(shown),
        path=path,
        recursive=recursive,
        pattern=pattern,
        limit=limit,
        truncated=truncated or cap.truncated,
    )


def _normalize_sandbox_search_results(raw_results: Any) -> list[dict[str, Any]]:
    """Project daemon-specific search rows into the public tool contract.

    The sandbox content endpoint is ripgrep-backed and returns useful transport
    fields such as ``lines``, ``line_number``, and ``submatches``. Those are
    deliberately not part of ``FileSearchMatch``: the tool's cross-runtime
    result contract is just a path plus matching snippets. Accepting the
    daemon row directly made its harmless extra fields turn a successful
    search into a Pydantic validation failure.
    """
    if not isinstance(raw_results, list):
        return []

    normalized: list[dict[str, Any]] = []
    for row in raw_results:
        # The path-search endpoint supplies bare path strings; content search
        # supplies ripgrep-style objects. Keep both daemon variants behind the
        # same documented result shape.
        if isinstance(row, str):
            normalized.append({"path": row})
            continue
        if not isinstance(row, dict):
            continue

        path = row.get("path")
        if not isinstance(path, str):
            continue

        match: dict[str, Any] = {"path": path}
        snippets: list[str] = []
        lines = row.get("lines")
        if isinstance(lines, str):
            snippets.append(lines)
        else:
            for submatch in row.get("submatches", []):
                candidate = submatch.get("match") if isinstance(submatch, dict) else None
                text = candidate.get("text") if isinstance(candidate, dict) else None
                if isinstance(text, str):
                    snippets.append(text)
        if snippets:
            match["matches"] = snippets
        elif isinstance(row.get("size"), int):
            match["size"] = row["size"]
        normalized.append(match)
    return normalized


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
        # is_retryable / suggested_action ride the exception (a transient
        # orchestrator-restart outage is retryable and carries the wait-once
        # instruction); anything else keeps the old non-retryable default.
        error=ToolError(
            error_type=error_type,
            message=str(exc),
            is_retryable=bool(getattr(exc, "is_retryable", False)),
            suggested_action=getattr(exc, "suggested_action", None),
        ),
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


def _refuse_if_their_machine_is_down(tool_name: str, ctx: ToolContext) -> ToolResult | None:
    """🚨 "NO BOX ATTACHED" AND "THEIR BOX IS DOWN" ARE DIFFERENT ANSWERS.

    Every branch below this line is about to serve the durable VFS as a
    substitute for a real filesystem. When nobody attached a box that is the
    right answer — there is no box to be down, and the emulator is honest about
    being what it is.

    When the HOST has stamped an outage on this run, it is not. That stamp only
    ever appears for a person whose machine is supposed to be up right now, and
    serving them an emulator over their code library while they believe their
    own files are being read is the silent degrade the sandbox hard-gate exists
    to prevent — reaching them through the one door that gate cannot close,
    because a conversation with NO binding raises no refusal and never should.

    The refusal is one sentence the host wrote for the person, and it names
    what the staff still can do. Called at the top of every durable-VFS branch;
    ``test_a_tool_that_needs_the_box_says_so.py`` walks this file's AST and
    fails if a branch is ever added without it.
    """

    from matrx_ai.tools.workspace_outage import refuse_if_workspace_is_down

    return refuse_if_workspace_is_down(tool_name, ctx)


def _read_prior_local(filepath: Path) -> str | None:
    """Prior content of a local file for the receipt: missing → ``""``; not showable → ``None``."""
    if not filepath.exists():
        return ""
    if not filepath.is_file() or filepath.stat().st_size > MAX_PATCH_SIZE:
        return None
    return decode_prior(filepath.read_bytes())


def _showable(text: str | None) -> str | None:
    """A sandbox read decodes lossily; a replacement char means binary — skip the receipt."""
    if text is None or "\ufffd" in text:
        return None
    return text


async def _proxy_read_prior(
    binding: SandboxBinding, sandbox_path: str, *, bounded: bool
) -> tuple[bool, str | None]:
    """Read a sandbox file whole through the proxy: ``(exists, text)``.

    Missing (404) → ``(False, "")``. With ``bounded``, a file over
    MAX_PATCH_SIZE stops after the first page → ``(True, None)``. Any other
    proxy failure raises ``SandboxProxyError``.
    """
    chunks: list[str] = []
    offset = 0
    try:
        while True:
            page = await _proxy_fs_read(
                binding,
                sandbox_path,
                encoding="utf8",
                offset=offset,
                limit=MAX_READ_SIZE,
            )
            if bounded and page.size > MAX_PATCH_SIZE:
                return True, None
            chunks.append(page.content)
            if not page.truncated:
                break
            if page.next_offset <= offset:
                raise SandboxProxyError(
                    "Sandbox read pagination did not advance",
                    error_type="protocol_error",
                )
            offset = page.next_offset
    except SandboxProxyError as exc:
        if exc.status != 404:
            raise
        return False, ""
    return True, "".join(chunks)


async def fs_read(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsReadArgs(**args)

    # No sandbox + a durable VFS backend → serve from the durable code_files filesystem.
    if _should_use_durable_vfs():
        if (refusal := _refuse_if_their_machine_is_down("fs_read", ctx)) is not None:
            return refusal
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_read(args, ctx)

    # Sandbox-bound chats: route to the matrx_agent inside the container
    # via the orchestrator. Same /fs/read endpoint the admin inspector
    # uses, so the agent's view is identical to the operator's view.
    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            read_limit = min(parsed.limit, FS_READ_MAX_CHARS) if parsed.limit > 0 else FS_READ_MAX_CHARS
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
                output_self_capped=True,
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
        read_limit = min(parsed.limit, FS_READ_MAX_CHARS) if parsed.limit > 0 else FS_READ_MAX_CHARS

        with open(filepath, "rb") as f:
            if parsed.offset:
                f.seek(parsed.offset)
            raw = f.read(read_limit)
            end = f.tell()
        # Never split a UTF-8 sequence at the page edge: back off to a boundary
        # so next_offset (a byte offset) resumes on a whole character.
        cut = len(raw)
        while cut > 0 and end < size and (raw[cut - 1] & 0xC0) == 0x80:
            cut -= 1
        if cut > 0 and end < size and raw[cut - 1] >= 0xC0:
            cut -= 1
        if cut != len(raw):
            end -= len(raw) - cut
            raw = raw[:cut]
        content = raw.decode("utf-8", errors="replace")
        truncated = end < size

        return ToolResult(
            success=True,
            output=FileReadResult(
                content=content,
                size=size,
                truncated=truncated,
                offset=parsed.offset,
                limit=read_limit,
                next_offset=end if truncated else None,
                path=parsed.path,
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="fs_read",
            call_id=ctx.call_id,
            output_self_capped=True,
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
        if (refusal := _refuse_if_their_machine_is_down("fs_write", ctx)) is not None:
            return refusal
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_write(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            # The matrx_agent /fs/write replaces the file. ``append`` mode
            # has no direct daemon equivalent — fall back to read+append+write
            # so the public tool contract still works. The same read is the
            # receipt's "before"; an overwrite whose prior cannot be read just
            # skips the receipt — it never fails the write.
            before: str | None
            proxy_existed: bool | None = None
            if parsed.append:
                _, existing = await _proxy_read_prior(binding, sandbox_path, bounded=False)
                existing = existing or ""
                content = existing + parsed.content
                before = _showable(existing)
            else:
                content = parsed.content
                try:
                    proxy_existed, prior = await _proxy_read_prior(binding, sandbox_path, bounded=True)
                    before = _showable(prior)
                except SandboxProxyError as exc:
                    logger.info("fs_write: prior read of %s failed (%s); receipt skipped", sandbox_path, exc)
                    before = None
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
            return with_file_surface_write(
                ToolResult(
                    success=True,
                    output=FileWriteResult(
                        path=sandbox_path, size=stat.get("size"), stat=stat
                    ).model_dump(mode="json"),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="fs_write",
                    call_id=ctx.call_id,
                ),
                path=sandbox_path,
                before=before,
                after=content,
                mode="append" if parsed.append else "overwrite",
                existed=None if parsed.append else proxy_existed,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_write", call_id=ctx.call_id, started_at=started_at
            )

    try:
        filepath = _resolve_path(parsed.path, ctx)
        existed_before = filepath.exists()
        before = _read_prior_local(filepath)
        if parsed.create_dirs:
            filepath.parent.mkdir(parents=True, exist_ok=True)

        mode = "a" if parsed.append else "w"
        with open(filepath, mode, encoding="utf-8") as f:
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

        return with_file_surface_write(
            ToolResult(
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
            ),
            path=parsed.path,
            before=before,
            after=(before + parsed.content) if (parsed.append and before is not None) else parsed.content,
            mode="append" if parsed.append else "overwrite",
            existed=existed_before,
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
        if (refusal := _refuse_if_their_machine_is_down("fs_list", ctx)) is not None:
            return refusal
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
                output=_bounded_listing(
                    entries=entries,
                    path=sandbox_path,
                    recursive=parsed.recursive,
                    pattern=parsed.pattern or None,
                    limit=MAX_LIST_ENTRIES,
                    truncated=bool(data.get("truncated", False) or data.get("nextPageToken")),
                ).model_dump(mode="json"),
                output_self_capped=True,
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
        entry_limit_reached = False
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
            if len(entries) > MAX_LIST_ENTRIES:
                entries.pop()
                entry_limit_reached = True
                break

        return ToolResult(
            success=True,
            output=_bounded_listing(
                entries=entries,
                path=parsed.path,
                limit=MAX_LIST_ENTRIES,
                truncated=entry_limit_reached,
            ).model_dump(mode="json"),
            output_self_capped=True,
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
        if (refusal := _refuse_if_their_machine_is_down("fs_search", ctx)) is not None:
            return refusal
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
            results = _normalize_sandbox_search_results(data.get("results"))
            return ToolResult(
                success=True,
                output=FileSearchResults(
                    results=[FileSearchMatch(**result) for result in results],
                    count=len(results),
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


def _fs_error(
    tool_name: str,
    call_id: str,
    started_at: float,
    error_type: str,
    message: str,
    suggested_action: str | None = None,
) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type=error_type, message=message, suggested_action=suggested_action),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


def _missing_file_refusal(
    parsed: FsPatchArgs, tool_name: str, call_id: str, started_at: float
) -> ToolResult | None:
    """fs_patch on a missing file: refuse unless create_if_missing with an insert-mode first edit."""
    if not parsed.create_if_missing:
        return _fs_error(
            tool_name,
            call_id,
            started_at,
            "not_found",
            f"File not found: {parsed.path}",
            "Set create_if_missing=True to create the file with the patch's first edit.",
        )
    if parsed.edits[0].old_text != "":
        return _fs_error(
            tool_name,
            call_id,
            started_at,
            "invalid_input",
            "create_if_missing=True requires the first edit to have empty old_text (insert mode).",
        )
    return None


def _daemon_failure_result(
    data: dict[str, Any],
    *,
    tool_name: str,
    path: str,
    total_edits: int,
    call_id: str,
    started_at: float,
) -> ToolResult:
    """The sandbox daemon refused edits we could not pre-verify (or the file moved under us).

    Loud, typed like every other patch failure — and honest that the daemon may
    have applied the edits it did not report as failed.
    """
    failures: list[dict[str, Any]] = []
    for f in data.get("edits_failed") or []:
        reason = str(f.get("reason") or "")
        failures.append(
            {
                "edit_index": int(f.get("edit_index", 0) or 0),
                "error_type": PATCH_NO_MATCH if "not found" in reason.lower() else PATCH_AMBIGUOUS,
                "reason": reason,
                "match_count": 0,
                "match_lines": [],
                "old_text_preview": str(f.get("old_text_preview") or ""),
            }
        )
    return patch_failure_result(
        failures,
        tool_name=tool_name,
        path=path,
        total_edits=total_edits,
        call_id=call_id,
        started_at=started_at,
        applied_elsewhere=len(failures) < total_edits,
    )


async def _sandbox_patch(
    binding: SandboxBinding,
    parsed: FsPatchArgs,
    *,
    tool_name: str,
    call_id: str,
    started_at: float,
) -> tuple[ToolResult | None, dict[str, Any], str | None, str | None, list[dict[str, Any]]]:
    """fs_patch / fs_edit through the sandbox proxy — all-or-nothing, with the receipt's sides.

    Reads the prior content through the proxy, runs :func:`apply_patch_edits`
    locally (the same contract as every backend) and only when EVERY edit names
    exactly one place asks the daemon to apply them. Returns
    ``(refusal, daemon_data, before, after, applied)``; a prior that is not
    showable (binary / over MAX_PATCH_SIZE) goes straight to the daemon with no
    receipt (``before`` None).
    """
    sandbox_path = _resolve_sandbox_path(binding, parsed.path)
    exists, prior = await _proxy_read_prior(binding, sandbox_path, bounded=True)
    if not exists:
        if tool_name == "fs_edit":
            return (
                _fs_error(tool_name, call_id, started_at, "not_found", f"File not found: {parsed.path}"),
                {},
                None,
                None,
                [],
            )
        if (refusal := _missing_file_refusal(parsed, tool_name, call_id, started_at)) is not None:
            return refusal, {}, None, None, []
    before = _showable(prior) if exists else ""
    after: str | None = None
    applied: list[dict[str, Any]] = []
    if before is not None:
        after, applied, failures = apply_patch_edits(before, parsed.edits, existed=exists)
        if failures:
            return (
                patch_failure_result(
                    failures,
                    tool_name=tool_name,
                    path=parsed.path,
                    total_edits=len(parsed.edits),
                    call_id=call_id,
                    started_at=started_at,
                ),
                {},
                None,
                None,
                [],
            )
    data = await _proxy_fs_patch(
        binding,
        sandbox_path,
        [
            {"old_text": e.old_text, "new_text": e.new_text, "replace_all": e.replace_all}
            for e in parsed.edits
        ],
        create_if_missing=parsed.create_if_missing,
    )
    if data.get("edits_failed"):
        return (
            _daemon_failure_result(
                data,
                tool_name=tool_name,
                path=parsed.path,
                total_edits=len(parsed.edits),
                call_id=call_id,
                started_at=started_at,
            ),
            data,
            None,
            None,
            [],
        )
    return None, data, before, after, applied


async def fs_patch(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Anchor-based file edit — apply 1-N old_text→new_text edits in order.

    The single most useful coding tool for an LLM agent. Models reliably
    produce small "find this exact block, replace with this exact block"
    edits; they're notoriously bad at re-emitting an entire file or at
    composing multi-line shell heredocs. fs_patch leans into that strength.

    ALL-OR-NOTHING on every backend: each edit must name exactly one place
    (or opt into several with replace_all). If ANY edit fails the file is not
    written and one error names every failing edit — ``patch_no_match`` or
    ``patch_ambiguous`` (with the match count and line numbers). On success the
    surface-write receipt carries before → after.
    """
    started_at = time.time()
    parsed = FsPatchArgs(**args)
    if _should_use_durable_vfs():
        if (refusal := _refuse_if_their_machine_is_down("fs_patch", ctx)) is not None:
            return refusal
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_patch(args, ctx)

    if (binding := get_active_sandbox()) is not None:
        try:
            refusal, data, before, after, applied = await _sandbox_patch(
                binding, parsed, tool_name="fs_patch", call_id=ctx.call_id, started_at=started_at
            )
            if refusal is not None:
                return refusal
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            await emit_fs_changed(
                action="modified",
                path=sandbox_path,
                metadata={"tool": "fs_patch", "edits": len(parsed.edits)},
            )
            return with_file_surface_write(
                ToolResult(
                    success=True,
                    output=FilePatchResult(
                        path=sandbox_path,
                        created=bool(data.get("created", False)),
                        edits_applied=[
                            FileEditApplied(**s) for s in (applied or data.get("edits_applied", []))
                        ],
                        edits_failed=[],
                        size_before=int(data.get("size_before", 0) or 0),
                        size_after=int(data.get("size_after", 0) or 0),
                    ).model_dump(mode="json"),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="fs_patch",
                    call_id=ctx.call_id,
                ),
                path=sandbox_path,
                before=before,
                after=after,
                mode="patch",
                edits=len(parsed.edits),
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_patch", call_id=ctx.call_id, started_at=started_at
            )

    try:
        filepath = _resolve_path(parsed.path, ctx)
        existed = filepath.exists()

        if not existed:
            if (refusal := _missing_file_refusal(parsed, "fs_patch", ctx.call_id, started_at)) is not None:
                return refusal
            content = ""
        else:
            size = filepath.stat().st_size
            if size > MAX_PATCH_SIZE:
                return _fs_error(
                    "fs_patch",
                    ctx.call_id,
                    started_at,
                    "too_large",
                    f"File is {size} bytes; fs_patch refuses files over {MAX_PATCH_SIZE}.",
                    "Use shell_execute with sed/awk/perl for very large files.",
                )
            content = filepath.read_bytes().decode("utf-8")

        original_content = content
        content, applied_summaries, failures = apply_patch_edits(
            content, parsed.edits, existed=existed
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

        if not existed:
            filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding="utf-8")

        await emit_fs_changed(
            action="created" if not existed else "modified",
            path=str(filepath),
            metadata={
                "size": len(content),
                "edits_applied": len(applied_summaries),
                "edits_failed": 0,
                "mtime": filepath.stat().st_mtime,
            },
        )

        return with_file_surface_write(
            ToolResult(
                success=True,
                output=FilePatchResult(
                    path=parsed.path,
                    created=not existed,
                    edits_applied=[FileEditApplied(**s) for s in applied_summaries],
                    edits_failed=[],
                    size_before=len(original_content),
                    size_after=len(content),
                ).model_dump(mode="json"),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="fs_patch",
                call_id=ctx.call_id,
            ),
            path=parsed.path,
            before=original_content,
            after=content,
            mode="patch",
            edits=len(applied_summaries),
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


def edit_as_patch(parsed: FsEditArgs) -> FsPatchArgs:
    """fs_edit IS a one-edit fs_patch — one contract, one failure vocabulary."""
    return FsPatchArgs(
        path=parsed.path,
        edits=[
            FsPatchEdit(old_text=parsed.old_str, new_text=parsed.new_str, replace_all=parsed.replace_all)
        ],
    )


def edit_counts(applied: list[dict[str, Any]]) -> tuple[int, int]:
    """``(old_str_count, replaced)`` for fs_edit's result from the one applied summary."""
    if not applied:
        return 0, 0
    n = int(applied[0].get("matches_replaced", 1) or 1)
    return n, n


async def fs_edit(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Edit a file by a single exact string replacement (old_str → new_str).

    A focused, single-edit companion to fs_patch — the same contract on every
    backend: old_str must name exactly one place unless replace_all=True, else
    ``patch_no_match`` / ``patch_ambiguous`` and nothing is written. Mirrors
    fs_patch's sandbox-delegation + local-disk behavior so it is ALWAYS
    available, independent of the MATRX_VFS_ENABLED flag.
    """
    started_at = time.time()
    parsed = FsEditArgs(**args)
    if _should_use_durable_vfs():
        if (refusal := _refuse_if_their_machine_is_down("fs_edit", ctx)) is not None:
            return refusal
        from matrx_ai.tools.implementations import vfs_filesystem

        return await vfs_filesystem.fs_edit(args, ctx)

    patch = edit_as_patch(parsed)

    if (binding := get_active_sandbox()) is not None:
        try:
            # The sandbox daemon has no /fs/edit endpoint; fs_edit is a
            # single-edit fs_patch, so it rides the same verified patch path.
            refusal, data, before, after, applied = await _sandbox_patch(
                binding, patch, tool_name="fs_edit", call_id=ctx.call_id, started_at=started_at
            )
            if refusal is not None:
                return refusal
            sandbox_path = _resolve_sandbox_path(binding, parsed.path)
            await emit_fs_changed(
                action="modified",
                path=sandbox_path,
                metadata={"tool": "fs_edit"},
            )
            count, replaced = edit_counts(applied)
            return with_file_surface_write(
                ToolResult(
                    success=True,
                    output=FileEditResult(
                        path=sandbox_path,
                        old_str_count=count or int(data.get("old_str_count", 0) or 0),
                        replaced=replaced or int(data.get("replaced", 0) or 0),
                        size_before=int(data.get("size_before", 0) or 0),
                        size_after=int(data.get("size_after", 0) or 0),
                    ).model_dump(mode="json"),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name="fs_edit",
                    call_id=ctx.call_id,
                ),
                path=sandbox_path,
                before=before,
                after=after,
                mode="patch",
                edits=1,
            )
        except SandboxProxyError as exc:
            return _proxy_error(
                exc, tool_name="fs_edit", call_id=ctx.call_id, started_at=started_at
            )

    try:
        filepath = _resolve_path(parsed.path, ctx)
        if not filepath.exists():
            return _fs_error("fs_edit", ctx.call_id, started_at, "not_found", f"File not found: {parsed.path}")
        if filepath.is_dir():
            return _fs_error("fs_edit", ctx.call_id, started_at, "filesystem", f"Is a directory: {parsed.path}")
        size = filepath.stat().st_size
        if size > MAX_PATCH_SIZE:
            return _fs_error(
                "fs_edit",
                ctx.call_id,
                started_at,
                "too_large",
                f"File is {size} bytes; fs_edit refuses files over {MAX_PATCH_SIZE}.",
                "Use shell_execute with sed/awk/perl for very large files.",
            )

        content = filepath.read_bytes().decode("utf-8")
        new_content, applied, failures = apply_patch_edits(content, patch.edits, existed=True)
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

        filepath.write_text(new_content, encoding="utf-8")
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
        return with_file_surface_write(
            ToolResult(
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
            ),
            path=parsed.path,
            before=content,
            after=new_content,
            mode="patch",
            edits=1,
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


# ── The surface-write receipt for files ─────────────────────────────────────
#
# Every fs_write / fs_edit / fs_patch backend (local disk, active-sandbox proxy,
# durable VFS) reads the prior content, writes, then attaches ONE receipt
# (``matrx_ai.tools.surface_write``) so the chat's tool card shows the shared
# before → after diff. A prior the receipt cannot honestly show (binary,
# undecodable, over MAX_PATCH_SIZE) SKIPS the receipt — it never fails the write.

#: Extension → diff-engine (Monaco) language id. ``.md`` is markdown, not code.
_CODE_LANGUAGES: dict[str, str] = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".json": "json",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".sql": "sql",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "shell",
}
_MARKDOWN_SUFFIXES = frozenset({".md", ".markdown", ".mdx"})


def file_content_format(path: str) -> tuple[SurfaceWriteFormat, str | None]:
    """``(content_format, language)`` for a file path, inferred from its extension."""
    suffix = PurePosixPath(path.replace("\\", "/")).suffix.lower()
    if suffix in _MARKDOWN_SUFFIXES:
        return "markdown", None
    language = _CODE_LANGUAGES.get(suffix)
    if language is not None:
        return "code", language
    return "text", None


def decode_prior(data: bytes) -> str | None:
    """Strict UTF-8 decode of a file's prior bytes; ``None`` = not showable (skip the receipt)."""
    if len(data) > MAX_PATCH_SIZE:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def with_file_surface_write(
    result: ToolResult,
    *,
    path: str,
    before: str | None,
    after: str | None,
    mode: SurfaceWriteMode,
    edits: int | None = None,
    existed: bool | None = None,
) -> ToolResult:
    """Attach the file receipt to a successful write; ``before``/``after`` None = skip it.

    ``existed=False`` on an overwrite means the write CREATED the file — the
    card says "Created", never "Replaced" (nothing was replaced).
    """
    if before is None or after is None:
        return result
    if existed is False and mode == "overwrite":
        mode = "create"
    content_format, language = file_content_format(path)
    return attach_surface_write(
        result,
        before=before,
        after=after,
        target_type="file",
        target_id=path,
        target_label=path,
        mode=mode,
        content_format=content_format,
        language=language,
        edits=edits,
    )


# ── The patch contract ──────────────────────────────────────────────────────
#
# A patch names exactly ONE place or fails loudly — never a silent overwrite,
# never a partial apply. ``fs_edit`` and ``fs_patch`` on every backend fail with
# exactly one of these error types, each carrying a remedy the model can act on.
PATCH_NO_MATCH = "patch_no_match"
PATCH_AMBIGUOUS = "patch_ambiguous"
_MAX_MATCH_LINES = 20


def _match_lines(content: str, needle: str) -> list[int]:
    """1-based line numbers where ``needle`` starts (first ``_MAX_MATCH_LINES``)."""
    lines: list[int] = []
    if not needle:
        return lines
    start = 0
    while len(lines) < _MAX_MATCH_LINES:
        idx = content.find(needle, start)
        if idx < 0:
            break
        lines.append(content.count("\n", 0, idx) + 1)
        start = idx + len(needle)
    return lines


def apply_patch_edits(
    content: str,
    edits: Sequence[Any],
    *,
    existed: bool,
) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply an ordered list of ``FsPatchEdit``s to ``content`` — backend-agnostic.

    Pure string work: no filesystem, no VFS, no I/O. Every fs_edit / fs_patch
    backend (local disk, sandbox proxy, durable VFS) runs THIS function, so the
    backends cannot drift in what an edit means or how a failure reads.

    Returns ``(new_content, applied_summaries, failures)``. Each failure carries
    ``error_type`` (``patch_no_match`` | ``patch_ambiguous``), ``match_count``
    and ``match_lines``. ANY failure means the caller must NOT write — a patch is
    all-or-nothing (:func:`patch_failure_result`).
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
                    "error_type": PATCH_NO_MATCH,
                    "reason": "old_text not found in current file content",
                    "match_count": 0,
                    "match_lines": [],
                    "old_text_preview": _preview(edit.old_text),
                }
            )
            continue
        if count > 1 and not edit.replace_all:
            lines = _match_lines(content, edit.old_text)
            where = f" (lines {', '.join(str(n) for n in lines)})" if lines else ""
            failures.append(
                {
                    "edit_index": i,
                    "error_type": PATCH_AMBIGUOUS,
                    "reason": (
                        f"old_text matches {count} places{where} — add surrounding context "
                        f"to make it unique, or set replace_all=true to update every match."
                    ),
                    "match_count": count,
                    "match_lines": lines,
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


def patch_failure_result(
    failures: list[dict[str, Any]],
    *,
    tool_name: str,
    path: str,
    total_edits: int,
    call_id: str,
    started_at: float,
    applied_elsewhere: bool = False,
) -> ToolResult:
    """The ONE loud refusal for a patch that could not name exactly one place.

    ``error_type`` is the first failing edit's (``patch_no_match`` or
    ``patch_ambiguous``); the message names every failing edit's index and
    reason; nothing was written. ``applied_elsewhere`` is the one honest
    exception: the sandbox daemon patched a prior we could not pre-verify and
    applied the edits it did not report as failed.
    """
    first = failures[0]
    error_type = str(first["error_type"])
    if tool_name == "fs_edit":
        # fs_edit is one edit, spelled old_str; keep the model's own vocabulary.
        if error_type == PATCH_NO_MATCH:
            message = f"old_str not found in {path}; nothing was written."
            remedy = (
                "Re-read the file with fs_read and copy old_str exactly as it appears, "
                "including whitespace and indentation."
            )
        else:
            count = first["match_count"]
            where = ", ".join(str(n) for n in first["match_lines"])
            message = (
                f"old_str matches {count} places in {path} (lines {where}); nothing was written."
            )
            remedy = (
                "Add surrounding lines to old_str so it names exactly one place, "
                f"or set replace_all=true to change all {count}."
            )
    else:
        parts = [f"edit {f['edit_index']}: {f['reason']}" for f in failures]
        outcome = (
            "the sandbox applied the OTHER edits (the file's prior content could not be "
            "verified before patching) — re-read it with fs_read before retrying"
            if applied_elsewhere
            else f"the patch applied NOTHING and {path} is unchanged"
        )
        message = (
            f"{len(failures)} of {total_edits} edit(s) failed, so {outcome} — "
            + "; ".join(parts)
            + "."
        )
        remedy = (
            "Fix each failing edit (re-read the file with fs_read and copy old_text exactly; "
            "add surrounding context to an ambiguous old_text, or set replace_all=true) and "
            "resend the WHOLE patch — none of its edits were applied."
        )
    return ToolResult(
        success=False,
        error=ToolError(error_type=error_type, message=message, suggested_action=remedy),
        output={"failures": failures, "path": path},
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_name,
        call_id=call_id,
    )


async def fs_mkdir(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = FsMkdirArgs(**args)
    if _should_use_durable_vfs():
        if (refusal := _refuse_if_their_machine_is_down("fs_mkdir", ctx)) is not None:
            return refusal
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
