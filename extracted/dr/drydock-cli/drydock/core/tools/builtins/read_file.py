from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, NamedTuple, final

import anyio
from pydantic import BaseModel, Field

from drydock.core.tools.base import (
    BaseTool,
    BaseToolConfig,
    BaseToolState,
    InvokeContext,
    ToolError,
    ToolPermission,
)
from drydock.core.tools.ui import ToolCallDisplay, ToolResultDisplay, ToolUIData
from drydock.core.tools.utils import resolve_file_tool_permission
from drydock.core.types import ToolStreamEvent

if TYPE_CHECKING:
    from drydock.core.types import ToolResultEvent


class _ReadResult(NamedTuple):
    lines: list[str]
    bytes_read: int
    was_truncated: bool


class ReadFileArgs(BaseModel):
    path: str
    offset: int = Field(
        default=0,
        description="Line number to start reading from (0-indexed, inclusive).",
    )
    limit: int | None = Field(
        default=None, description="Maximum number of lines to read."
    )


class ReadFileResult(BaseModel):
    path: str
    content: str
    lines_read: int
    was_truncated: bool = Field(
        description="True if the reading was stopped due to the line limit or max_read_bytes limit."
    )


class ReadFileToolConfig(BaseToolConfig):
    permission: ToolPermission = ToolPermission.ALWAYS

    max_read_bytes: int = Field(
        default=64_000, description="Maximum total bytes to read from a file in one go."
    )


class ReadFile(
    BaseTool[ReadFileArgs, ReadFileResult, ReadFileToolConfig, BaseToolState],
    ToolUIData[ReadFileArgs, ReadFileResult],
):
    description: ClassVar[str] = (
        "Read a UTF-8 file, returning content from a specific line range. "
        "Reading is capped by a byte limit for safety."
    )

    @final
    async def run(
        self, args: ReadFileArgs, ctx: InvokeContext | None = None
    ) -> AsyncGenerator[ToolStreamEvent | ReadFileResult, None]:
        file_path = self._prepare_and_validate_path(args)

        # Handle PDF files
        if file_path.suffix.lower() == ".pdf":
            content = self._read_pdf(file_path)
            yield ReadFileResult(
                path=str(file_path), content=content,
                lines_read=content.count("\n"), was_truncated=False,
            )
            return

        # Handle Jupyter notebooks (.ipynb): strip cell outputs to save
        # context. Notebook JSON often has 80%+ of bytes in outputs
        # (base64-encoded images, repr() of large dataframes, etc.) that
        # the model rarely needs to read code. Operator observed
        # 2026-05-19: Google_Trends_Analysis/main.ipynb returned 64,073
        # chars (full read_file cap) and inflated the session to 31K
        # tokens vs the 7-9K baseline.
        if file_path.suffix.lower() == ".ipynb":
            try:
                slim = self._read_notebook_slim(file_path)
                yield ReadFileResult(
                    path=str(file_path), content=slim,
                    lines_read=slim.count("\n"), was_truncated=False,
                )
                return
            except Exception:
                # Fall through to plain UTF-8 read on parse error.
                pass

        # Handle image files (describe what we can)
        if file_path.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"):
            import os
            size = os.path.getsize(file_path)
            content = f"[Image file: {file_path.name}, {size} bytes, format: {file_path.suffix}]"
            yield ReadFileResult(
                path=str(file_path), content=content,
                lines_read=1, was_truncated=False,
            )
            return

        # mtime-based read dedup (Claude Code tool-contract pattern).
        # If the model reads a file it has already read this session and
        # nothing has changed on disk since, return a compact stub
        # pointing to the earlier tool_result. Saves context + kills the
        # "re-read 50x for no reason" pattern. Also preserves Read-before-
        # Write because the stub still counts as having read the file.
        #
        # Per-slot dedup: track ALL (offset, limit) combinations independently.
        # The old single-slot approach allowed alternating offsets to bypass
        # dedup (read offset=0, read offset=50, read offset=0 again — the
        # offset=50 read evicted the offset=0 cache entry each time).
        read_state = ctx.read_file_state if ctx else None
        path_key = str(file_path)
        try:
            current_mtime = file_path.stat().st_mtime_ns
        except OSError:
            current_mtime = 0
        slot_key = (args.offset, args.limit)
        existing_entry = read_state.get(path_key, {}) if read_state is not None else {}
        slots: dict = existing_entry.get("_slots", {})
        prior_slot = slots.get(slot_key)
        if prior_slot is not None and prior_slot.get("timestamp") == current_mtime:
            # Re-embed the cached content so the model has it even if the
            # earlier tool_result was truncated by _truncate_old_tool_results.
            # Pointing at a stale/truncated prior result causes re-read loops.
            cached_content = prior_slot.get("content", "")
            prior_lines = prior_slot.get("lines_read", 0)
            dedup_count = prior_slot.get("dedup_count", 0)
            if dedup_count == 0:
                # 2026-05-31: 2nd identical read. Operator session showed
                # Gemma 4 ignoring the gentle "unchanged" header and reading
                # the same file 3-4× before doing anything. Make it more
                # actionable on the 2nd read so the model is steered
                # toward an edit *immediately*, not 3 reads later.
                header = (
                    "[2nd identical read of this file — content is unchanged from "
                    "your 1st read. STOP READING — your NEXT tool call should be "
                    "search_replace or write_file with the edit. If you don't yet "
                    "know what to edit, emit a plain-text question instead.]\n"
                )
            else:
                header = (
                    f"[REPEATED READ #{dedup_count + 1}: file has not changed across your last "
                    f"{dedup_count + 1} reads with these exact arguments. "
                    f"Reading again will produce this same result. "
                    f"To make progress: write or edit a file, use offset= to read a different section, "
                    f"or move on to the next task.]\n"
                )
            if read_state is not None:
                slots[slot_key] = {**prior_slot, "dedup_count": dedup_count + 1}
                read_state[path_key] = {**existing_entry, "_slots": slots}
            yield ReadFileResult(
                path=path_key,
                content=f"{header}{cached_content}",
                lines_read=prior_lines,
                was_truncated=prior_slot.get("was_truncated", False),
            )
            return

        read_result = await self._read_file(args, file_path)
        content = "".join(read_result.lines)

        # When stopped by the line limit (not byte limit), append a hint so
        # the model knows to paginate with offset= instead of re-reading.
        if (
            read_result.was_truncated
            and args.limit is not None
            and len(read_result.lines) == args.limit
        ):
            next_offset = args.offset + args.limit
            content += (
                f"\n[lines {args.offset + 1}–{next_offset} shown; "
                f"use offset={next_offset} to read more]"
            )

        # Record read state so Write/Edit can enforce Read-before-Write
        # and so future re-reads can dedup against this one.
        # Top-level entry (backward-compat: write_file/search_replace check
        # read_state.get(path_key) is not None).  Per-slot entry enables
        # independent dedup for every (offset, limit) combination so that
        # alternating offsets can't bypass dedup.
        if read_state is not None:
            slots[slot_key] = {
                "content": content,
                "timestamp": current_mtime,
                "lines_read": len(read_result.lines),
                "was_truncated": read_result.was_truncated,
                "dedup_count": 0,
            }
            read_state[path_key] = {
                "content": content,
                "timestamp": current_mtime,
                "offset": args.offset,
                "limit": args.limit,
                "lines_read": len(read_result.lines),
                "was_truncated": read_result.was_truncated,
                "_slots": slots,
            }

        yield ReadFileResult(
            path=path_key,
            content=content,
            lines_read=len(read_result.lines),
            was_truncated=read_result.was_truncated,
        )

    def _read_notebook_slim(self, file_path: Path) -> str:
        """Read a Jupyter notebook and return a compact form: cell type,
        source, and execution_count only. Outputs are SUMMARIZED (count
        per type) rather than embedded — they're usually 80%+ of bytes
        and the model rarely needs them to read code.

        Raises on parse failure; caller falls back to a plain UTF-8 read.
        """
        import json as _json
        data = _json.loads(file_path.read_text(encoding="utf-8"))
        cells = data.get("cells") or []
        out_lines: list[str] = [
            f"# Notebook: {file_path.name} ({len(cells)} cells, "
            f"outputs stripped — use `bash cat {file_path.name}` to see raw JSON)",
            "",
        ]
        for i, cell in enumerate(cells):
            ctype = cell.get("cell_type", "?")
            src = cell.get("source", "")
            if isinstance(src, list):
                src = "".join(src)
            ec = cell.get("execution_count")
            outputs = cell.get("outputs") or []
            header = f"## Cell {i} [{ctype}]"
            if ec is not None:
                header += f" (exec={ec})"
            if outputs:
                kinds: dict[str, int] = {}
                for o in outputs:
                    k = o.get("output_type", "?")
                    kinds[k] = kinds.get(k, 0) + 1
                summary = ", ".join(f"{n} {k}" for k, n in kinds.items())
                header += f" — outputs: [{summary}]"
            out_lines.append(header)
            out_lines.append(src.rstrip())
            out_lines.append("")
        return "\n".join(out_lines)

    def _read_pdf(self, file_path: Path) -> str:
        """Extract text from a PDF file."""
        try:
            import pypdf
            reader = pypdf.PdfReader(str(file_path))
            pages = []
            for i, page in enumerate(reader.pages[:20]):  # Max 20 pages
                text = page.extract_text()
                if text:
                    pages.append(f"--- Page {i+1} ---\n{text}")
            return "\n\n".join(pages) if pages else "[PDF has no extractable text]"
        except ImportError:
            return "[PDF reading requires pypdf: pip install pypdf]"
        except Exception as e:
            return f"[Error reading PDF: {e}]"

    def resolve_permission(self, args: ReadFileArgs) -> ToolPermission | None:
        return resolve_file_tool_permission(
            args.path,
            allowlist=self.config.allowlist,
            denylist=self.config.denylist,
            config_permission=self.config.permission,
        )

    def _prepare_and_validate_path(self, args: ReadFileArgs) -> Path:
        self._validate_inputs(args)

        file_path = Path(args.path).expanduser()
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path

        self._validate_path(file_path)
        return file_path

    async def _read_file(self, args: ReadFileArgs, file_path: Path) -> _ReadResult:
        import asyncio

        def _sync_read() -> _ReadResult:
            lines_to_return: list[str] = []
            bytes_read = 0
            was_truncated = False

            with open(file_path, encoding="utf-8", errors="ignore") as f:
                for line_index, line in enumerate(f):
                    if line_index < args.offset:
                        continue

                    if args.limit is not None and len(lines_to_return) >= args.limit:
                        was_truncated = True
                        break

                    line_bytes = len(line.encode("utf-8"))
                    if bytes_read + line_bytes > self.config.max_read_bytes:
                        was_truncated = True
                        break

                    lines_to_return.append(line)
                    bytes_read += line_bytes

            return _ReadResult(
                lines=lines_to_return,
                bytes_read=bytes_read,
                was_truncated=was_truncated,
            )

        try:
            loop = asyncio.get_running_loop()
            return await asyncio.wait_for(
                loop.run_in_executor(None, _sync_read), timeout=10,
            )
        except asyncio.TimeoutError:
            raise ToolError(f"Timed out reading {file_path} after 10s.")
        except OSError as exc:
            raise ToolError(f"Error reading {file_path}: {exc}") from exc

    def _validate_inputs(self, args: ReadFileArgs) -> None:
        if not args.path.strip():
            raise ToolError("Path cannot be empty")
        if args.offset < 0:
            raise ToolError("Offset cannot be negative")
        if args.limit is not None and args.limit <= 0:
            raise ToolError("Limit, if provided, must be a positive number")

    def _validate_path(self, file_path: Path) -> None:
        try:
            resolved_path = file_path.resolve()
        except ValueError:
            raise ToolError(
                f"Security error: Cannot read path '{file_path}' outside of the project directory '{Path.cwd()}'."
            )
        except FileNotFoundError:
            raise ToolError(self._not_found_msg(file_path))

        if not resolved_path.exists():
            raise ToolError(self._not_found_msg(file_path))
        if resolved_path.is_dir():
            raise ToolError(self._is_dir_msg(file_path, resolved_path))

    @staticmethod
    def _not_found_msg(file_path: Path) -> str:
        """Return 'File not found' error with parent directory listing for context.

        Also tries GraphRAG context recovery — if the requested basename is
        defined elsewhere in the indexed corpus, the response includes the
        location so the agent retries with the correct path."""
        parent = file_path.parent if file_path.parent != file_path else Path(".")
        msg_parts: list[str] = [f"File not found at: {file_path}"]
        try:
            entries = sorted(p.name for p in parent.iterdir())
            if entries:
                listing = "\n".join(f"  {e}" for e in entries[:30])
                suffix = f"\n  ... ({len(entries) - 30} more)" if len(entries) > 30 else ""
                msg_parts.append(f"Contents of {parent}/:\n{listing}{suffix}")
        except (PermissionError, OSError):
            pass

        # Best-effort context recovery via GraphRAG (no-op if no index).
        try:
            from drydock.core.context_recovery import recover_for_read_file
            recovery = recover_for_read_file(str(file_path))
            if recovery:
                msg_parts.append(recovery.lstrip())
        except Exception:
            pass

        return "\n".join(msg_parts)

    @staticmethod
    def _is_dir_msg(file_path: Path, resolved_path: Path) -> str:
        """Return 'is a directory' error with directory listing so model can pick a file."""
        try:
            entries = sorted(p.name for p in resolved_path.iterdir())
            if entries:
                listing = "\n".join(f"  {e}" for e in entries[:30])
                suffix = f"\n  ... ({len(entries) - 30} more)" if len(entries) > 30 else ""
                return (
                    f"Path is a directory, not a file: {file_path}\n"
                    f"Contents of {file_path}/:\n{listing}{suffix}"
                )
        except (PermissionError, OSError):
            pass
        return f"Path is a directory, not a file: {file_path}"

    @classmethod
    def format_call_display(cls, args: ReadFileArgs) -> ToolCallDisplay:
        summary = f"Reading {args.path}"
        if args.offset > 0 or args.limit is not None:
            parts = []
            if args.offset > 0:
                parts.append(f"from line {args.offset}")
            if args.limit is not None:
                parts.append(f"limit {args.limit} lines")
            summary += f" ({', '.join(parts)})"
        return ToolCallDisplay(summary=summary)

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        if not isinstance(event.result, ReadFileResult):
            return ToolResultDisplay(
                success=False, message=event.error or event.skip_reason or "No result"
            )

        path_obj = Path(event.result.path)
        message = f"Read {event.result.lines_read} line{'' if event.result.lines_read <= 1 else 's'} from {path_obj.name}"
        if event.result.was_truncated:
            message += " (truncated)"

        return ToolResultDisplay(
            success=True,
            message=message,
            warnings=["File was truncated due to size limit"]
            if event.result.was_truncated
            else [],
        )

    @classmethod
    def get_status_text(cls) -> str:
        return "Reading file"
