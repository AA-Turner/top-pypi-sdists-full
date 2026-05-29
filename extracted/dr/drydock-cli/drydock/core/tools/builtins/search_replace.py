from __future__ import annotations

from collections.abc import AsyncGenerator
import difflib
from pathlib import Path
import re
import shutil
from typing import ClassVar, NamedTuple, final

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
from drydock.core.types import ToolResultEvent, ToolStreamEvent

SEARCH_REPLACE_BLOCK_RE = re.compile(
    r"<{5,}\s*(?:SEARCH\s*)+\r?\n(.*?)\r?\n?={5,}\r?\n(.*?)\r?\n?>{5,}\s*(?:REPLACE\s*)+",
    flags=re.DOTALL,
)

SEARCH_REPLACE_BLOCK_WITH_FENCE_RE = re.compile(
    r"```[\s\S]*?\n<{5,}\s*(?:SEARCH\s*)+\r?\n(.*?)\r?\n?={5,}\r?\n(.*?)\r?\n?>{5,}\s*(?:REPLACE\s*)+\s*\n```",
    flags=re.DOTALL,
)


class SearchReplaceBlock(NamedTuple):
    search: str
    replace: str


class FuzzyMatch(NamedTuple):
    similarity: float
    start_line: int
    end_line: int
    text: str


class BlockApplyResult(NamedTuple):
    content: str
    applied: int
    errors: list[str]
    warnings: list[str]


class SearchReplaceArgs(BaseModel):
    file_path: str = Field(default="", description="Path to the file to edit")
    content: str = Field(default="", description="SEARCH/REPLACE blocks or JSON with old_string/new_string")
    # Gemma 4 sometimes sends these directly instead of in content
    old_string: str | None = Field(default=None, description="Text to find (alternative to content blocks)")
    new_string: str | None = Field(default=None, description="Replacement text (alternative to content blocks)")


class SearchReplaceResult(BaseModel):
    file: str
    blocks_applied: int
    lines_changed: int
    content: str
    warnings: list[str] = Field(default_factory=list)


class SearchReplaceConfig(BaseToolConfig):
    max_content_size: int = 100_000
    create_backup: bool = False
    fuzzy_threshold: float = 0.9


class SearchReplace(
    BaseTool[
        SearchReplaceArgs, SearchReplaceResult, SearchReplaceConfig, BaseToolState
    ],
    ToolUIData[SearchReplaceArgs, SearchReplaceResult],
):
    description: ClassVar[str] = (
        "Replace sections of files using SEARCH/REPLACE blocks. "
        "Supports fuzzy matching and detailed error reporting. "
        "Format: <<<<<<< SEARCH\\n[text]\\n=======\\n[replacement]\\n>>>>>>> REPLACE"
    )

    @classmethod
    def format_call_display(cls, args: SearchReplaceArgs) -> ToolCallDisplay:
        blocks = cls._parse_search_replace_blocks(args.content)
        return ToolCallDisplay(
            summary=f"Patching {args.file_path} ({len(blocks)} blocks)",
            content=args.content,
        )

    @classmethod
    def get_result_display(cls, event: ToolResultEvent) -> ToolResultDisplay:
        if isinstance(event.result, SearchReplaceResult):
            if event.result.blocks_applied == 0:
                return ToolResultDisplay(
                    success=False,
                    message=event.result.content[:120].split("\n")[0],
                    warnings=event.result.warnings,
                )
            # 2026-05-19: ALREADY-APPLIED blocks count toward
            # blocks_applied so the model doesn't see an error — but the
            # UI used to show "✓ Applied N block(s)" with green check
            # even when nothing actually changed. That contradicted the
            # ⚠ ALREADY-APPLIED warnings underneath and confused
            # operators ("did it apply or not?"). When every applied
            # block was a no-op (lines_changed == 0 AND all warnings
            # start with "Block N: ALREADY"), downgrade to no-success
            # so the icon matches the substance.
            warns = event.result.warnings or []
            all_noop = (
                event.result.lines_changed == 0
                and warns
                and all(w.startswith(f"Block {i+1}: ALREADY")
                        for i, w in enumerate(warns[:event.result.blocks_applied]))
            )
            if all_noop:
                return ToolResultDisplay(
                    success=False,  # rendered as ⚠ warning, not ✓ success
                    message=f"No-op: {event.result.blocks_applied} block(s) already applied",
                    warnings=warns,
                )
            return ToolResultDisplay(
                success=True,
                message=f"Applied {event.result.blocks_applied} block{'' if event.result.blocks_applied == 1 else 's'}",
                warnings=warns,
            )

        return ToolResultDisplay(success=True, message="Patch applied")

    @classmethod
    def get_status_text(cls) -> str:
        return "Editing files"

    def resolve_permission(self, args: SearchReplaceArgs) -> ToolPermission | None:
        return resolve_file_tool_permission(
            args.file_path,
            allowlist=self.config.allowlist,
            denylist=self.config.denylist,
            config_permission=self.config.permission,
        )

    @final
    async def run(
        self, args: SearchReplaceArgs, ctx: InvokeContext | None = None
    ) -> AsyncGenerator[ToolStreamEvent | SearchReplaceResult, None]:
        try:
            file_path, search_replace_blocks = self._prepare_and_validate_args(args)
        except ToolError as e:
            err_msg = str(e)
            if err_msg.startswith("SEARCH_IS_ERROR:"):
                yield SearchReplaceResult(
                    file=args.file_path.strip() or "(unknown)",
                    blocks_applied=0,
                    lines_changed=0,
                    content=err_msg[len("SEARCH_IS_ERROR:"):].strip(),
                )
                return
            if err_msg.startswith("Empty content provided.") or err_msg.startswith("File path is required."):
                # Model sent search_replace with missing content or file_path.
                # Convert to a soft result so the model corrects — a ToolError
                # causes panic-retry loops (feedback: never raise ToolError for
                # loop detection). Track count to escalate on repeat offenses.
                empty_state = self.state.__dict__.setdefault("_sr_empty_history", {})
                key = args.file_path.strip() or "<no-path>"
                entry = empty_state.get(key, {"count": 0})
                entry["count"] += 1
                empty_state[key] = entry
                count = entry["count"]
                escalate = count >= 2
                extra = ""
                if escalate:
                    # Show project files so model can recover context
                    try:
                        py_files = sorted(
                            str(p.relative_to(Path.cwd()))
                            for p in Path.cwd().rglob("*.py")
                            if "__pycache__" not in str(p) and ".git" not in str(p)
                        )[:20]
                        extra = (
                            f"\n[This is the #{count} empty search_replace on '{key}'. "
                            f"Stop retrying. Current .py files in project:\n"
                            + "\n".join(f"  {f}" for f in py_files)
                            + "\nUse write_file to create a file, or read_file to "
                            f"see file contents before editing.]"
                        )
                    except Exception:
                        extra = (
                            f"\n[This is the #{count} empty search_replace on '{key}'. "
                            "Stop retrying. Use write_file or read the file first.]"
                        )
                yield SearchReplaceResult(
                    file=key,
                    blocks_applied=0,
                    lines_changed=0,
                    content=err_msg + extra,
                )
                return
            if err_msg.startswith("Path is not a file:"):
                # Model passed a directory instead of a file path.
                # Return a result (not raise) so the model corrects the call
                # rather than retrying the same directory path in a loop.
                # Track consecutive calls to escalate guidance on 2nd+ offense.
                dir_path_str = args.file_path.strip()
                dir_path = Path(dir_path_str).expanduser()
                if not dir_path.is_absolute():
                    dir_path = Path.cwd() / dir_path
                dir_path = dir_path.resolve()
                if dir_path.is_dir():
                    dir_state = self.state.__dict__.setdefault("_sr_dir_history", {})
                    dir_key = str(dir_path)
                    dir_entry = dir_state.get(dir_key, {"count": 0})
                    dir_entry["count"] += 1
                    dir_state[dir_key] = dir_entry
                    dir_count = dir_entry["count"]
                    try:
                        files = sorted(p.name for p in dir_path.iterdir() if p.is_file())
                    except OSError:
                        files = []
                    files_list = "\n".join(f"  {f}" for f in files[:20]) or "  (empty directory)"
                    if dir_count >= 2:
                        # Escalate: model retried the same directory path — add project listing
                        try:
                            py_files = sorted(
                                str(p.relative_to(Path.cwd()))
                                for p in Path.cwd().rglob("*.py")
                                if "__pycache__" not in str(p) and ".git" not in str(p)
                            )[:20]
                            project_listing = (
                                f"\n[REPEATED ERROR #{dir_count}: you have called search_replace on "
                                f"this directory {dir_count} times. You MUST specify a filename. "
                                f"Project .py files:\n"
                                + "\n".join(f"  {f}" for f in py_files)
                                + "\nUse the exact path from this list.]"
                            )
                        except Exception:
                            project_listing = (
                                f"\n[REPEATED ERROR #{dir_count}: stop passing the directory. "
                                "Use a full file path like 'tool_agent/cli.py'.]"
                            )
                    else:
                        project_listing = ""
                    yield SearchReplaceResult(
                        file=str(dir_path),
                        blocks_applied=0,
                        lines_changed=0,
                        content=(
                            f"PATH ERROR: '{dir_path}' is a directory, not a file. "
                            f"search_replace requires a path to a specific file.\n"
                            f"Files in that directory:\n{files_list}\n"
                            f"Specify the full path including the filename, e.g. "
                            f"'{dir_path}/{files[0] if files else '<filename.py>'}'"
                            + project_listing
                        ),
                    )
                    return
            if err_msg.startswith("File does not exist:"):
                # Convert to advisory result with directory listing so the
                # model can correct its path without retrying blindly.
                # Previously raised as ToolError → model retried 18+ times
                # (admiral_history shows "retry_after_error:search_replace:
                # <tool_error>search_replace failed: File does not exist").
                bad_path_str = args.file_path.strip()
                bad_path = Path(bad_path_str).expanduser()
                if not bad_path.is_absolute():
                    bad_path = Path.cwd() / bad_path
                bad_path = bad_path.resolve()
                parent = bad_path.parent
                # Track repeat offenses so escalation fires on 2nd+ call.
                fne_state = self.state.__dict__.setdefault("_sr_fne_history", {})
                fne_key = str(bad_path)
                fne_entry = fne_state.get(fne_key, {"count": 0})
                fne_entry["count"] += 1
                fne_state[fne_key] = fne_entry
                fne_count = fne_entry["count"]
                try:
                    if parent.is_dir():
                        sibling_files = sorted(
                            p.name for p in parent.iterdir() if p.is_file()
                        )[:20]
                        dir_listing = (
                            f"Files in {parent}:\n"
                            + "\n".join(f"  {f}" for f in sibling_files)
                        ) if sibling_files else f"Directory {parent} is empty."
                    else:
                        dir_listing = f"Parent directory {parent} does not exist."
                except OSError:
                    dir_listing = f"Could not list {parent}."
                extra = ""
                if fne_count >= 2:
                    try:
                        py_files = sorted(
                            str(p.relative_to(Path.cwd()))
                            for p in Path.cwd().rglob("*.py")
                            if "__pycache__" not in str(p) and ".git" not in str(p)
                        )[:20]
                        extra = (
                            f"\n[REPEATED ERROR #{fne_count}: '{bad_path.name}' still "
                            f"does not exist. Stop retrying this path. "
                            f"Project .py files you can edit:\n"
                            + "\n".join(f"  {f}" for f in py_files)
                            + "\nTo CREATE a new file use write_file instead of search_replace.]"
                        )
                    except Exception:
                        extra = (
                            f"\n[REPEATED ERROR #{fne_count}: use write_file to create "
                            f"'{bad_path.name}' before trying to edit it.]"
                        )
                yield SearchReplaceResult(
                    file=bad_path_str,
                    blocks_applied=0,
                    lines_changed=0,
                    content=(
                        f"FILE NOT FOUND: '{bad_path}' does not exist and cannot be edited.\n"
                        f"{dir_listing}\n"
                        f"If you need to CREATE this file, use write_file. "
                        f"If you meant to edit a different file, use the exact path from the listing above."
                        + extra
                    ),
                )
                return
            if err_msg.startswith("NO_BLOCKS:"):
                # Gemma 4 sent raw code without SEARCH/REPLACE markers.
                # CAREFULLY fall back to full file overwrite — but refuse if
                # the raw content is much shorter than the existing file
                # (would be catastrophic data loss). See CLAUDE.md learning
                # #39: drydock nuked a 5171-char cli.py with a 16-line fragment.
                raw_content = err_msg[len("NO_BLOCKS:"):]
                # Guard: if the raw content contains SEARCH/REPLACE markers, it's
                # a malformed block (e.g. missing >>>>>>> REPLACE closer). Writing
                # it verbatim would corrupt the file with conflict markers, causing
                # a retry loop. Return an error instead.
                if "<<<<<<<" in raw_content or ">>>>>>>" in raw_content:
                    yield SearchReplaceResult(
                        file=args.file_path.strip() or "(unknown)",
                        blocks_applied=0,
                        lines_changed=0,
                        warnings=[],
                        content=(
                            "PARSE ERROR: your search_replace content looks like a "
                            "SEARCH/REPLACE block but it could not be parsed — likely "
                            "the >>>>>>> REPLACE closer is missing or the markers are "
                            "malformed. Fix the format:\n"
                            "<<<<<<< SEARCH\n"
                            "[exact text to find]\n"
                            "=======\n"
                            "[replacement text]\n"
                            ">>>>>>> REPLACE\n"
                            "Do NOT send conflict markers as literal file content."
                        ),
                    )
                    return
                file_path_str = args.file_path.strip()
                if file_path_str and len(raw_content) > 20:
                    target = Path(file_path_str).expanduser()
                    if not target.is_absolute():
                        target = Path.cwd() / target
                    target = target.resolve()
                    if target.exists():
                        import logging as _log
                        existing_size = target.stat().st_size
                        # SAFETY CHECK: a raw-code overwrite that would shrink
                        # the file by >50% is almost certainly a partial patch
                        # the model intended to APPEND, not a full rewrite.
                        # Old behavior REFUSED — model retried the same broken
                        # call in a loop. Try APPEND first when the combined
                        # file still parses cleanly (Python only); fall back
                        # to the directive REFUSED only if append would break
                        # the syntax.
                        if existing_size > 500 and len(raw_content) < existing_size * 0.5:
                            _log.getLogger(__name__).warning(
                                "search_replace: shrink-overwrite would lose %d%% "
                                "of %s (existing=%d, new=%d) — trying APPEND instead",
                                100 - int(len(raw_content) * 100 / existing_size),
                                target, existing_size, len(raw_content),
                            )
                            existing_text = target.read_text(errors="replace")
                            sep = "\n\n" if not existing_text.endswith("\n") else "\n"
                            combined = existing_text + sep + raw_content + (
                                "" if raw_content.endswith("\n") else "\n"
                            )
                            append_safe = True
                            if target.suffix == ".py":
                                try:
                                    import ast as _ast
                                    _ast.parse(combined)
                                except SyntaxError:
                                    append_safe = False
                            if append_safe:
                                _log.getLogger(__name__).info(
                                    "search_replace: APPEND %d chars to %s (parsed clean)",
                                    len(raw_content), target,
                                )
                                await self._write_file(target, combined)
                                self.state.__dict__.setdefault(
                                    "_sr_refused_raw_history", {}
                                ).pop(str(target), None)
                                yield SearchReplaceResult(
                                    file=str(target),
                                    blocks_applied=1,
                                    lines_changed=raw_content.count("\n") + 1,
                                    warnings=[
                                        "Appended raw content to end of file (no "
                                        "SEARCH/REPLACE blocks sent). Use proper "
                                        "SEARCH/REPLACE blocks for non-append edits."
                                    ],
                                    content=raw_content[:100] + "...",
                                )
                                return
                            # Track consecutive REFUSED-raw failures per file
                            # so we can escalate when the model retries the same
                            # broken raw-content call. Pattern observed in
                            # admiral logs: 14 retry_after_error:search_replace
                            # fires per 6h, all with "REFUSED: the raw content".
                            refused_state = self.state.__dict__.setdefault(
                                "_sr_refused_raw_history", {}
                            )
                            refused_key = str(target)
                            refused_entry = refused_state.get(
                                refused_key, {"count": 0, "last_len": 0}
                            )
                            refused_entry["count"] += 1
                            refused_entry["last_len"] = len(raw_content)
                            refused_state[refused_key] = refused_entry
                            base_msg = (
                                f"REFUSED: the raw content you sent ({len(raw_content)} "
                                f"chars) is much shorter than the existing {target.name} "
                                f"({existing_size} chars), and appending it would break "
                                f"the file's syntax."
                            )
                            if refused_entry["count"] >= 2:
                                head = existing_text[:1500] if "existing_text" in locals() else target.read_text(errors="replace")[:1500]
                                tail_src = existing_text if "existing_text" in locals() else target.read_text(errors="replace")
                                tail = tail_src[-800:] if len(tail_src) > 2300 else ""
                                tail_block = (
                                    f"\n-----FILE TAIL (last 800 chars)-----\n{tail}\n"
                                    if tail else ""
                                )
                                yield SearchReplaceResult(
                                    file=str(target),
                                    blocks_applied=0,
                                    lines_changed=0,
                                    content=(
                                        f"{base_msg}\n\n[LOOP-BREAKER: this is the "
                                        f"#{refused_entry['count']} consecutive REFUSED on "
                                        f"{target.name}. Stop sending the same raw content. "
                                        f"Actual file content (first 1500 chars of "
                                        f"{existing_size} bytes):\n"
                                        f"-----FILE HEAD-----\n{head}\n-----FILE END HEAD-----"
                                        f"{tail_block}\n"
                                        f"Choose ONE: (a) call write_file with overwrite=True "
                                        f"to replace the whole file with your raw content, OR "
                                        f"(b) send a proper SEARCH/REPLACE block anchored on "
                                        f"text from the file head/tail above.]"
                                    ),
                                )
                                return
                            yield SearchReplaceResult(
                                file=str(target),
                                blocks_applied=0,
                                lines_changed=0,
                                content=(
                                    f"{base_msg} To add new code, use a SEARCH/REPLACE "
                                    f"block anchored on the last line of the file:\n"
                                    f"<<<<<<< SEARCH\n"
                                    f"[the file's actual final line, copied exactly]\n"
                                    f"=======\n"
                                    f"[the same final line]\n\n"
                                    f"[your new code]\n"
                                    f">>>>>>> REPLACE\n"
                                    f"If you intended a full rewrite, use write_file instead."
                                ),
                            )
                            return
                        _log.getLogger(__name__).info(
                            "search_replace: no blocks — overwriting %s", target,
                        )
                        await self._write_file(target, raw_content)
                        self.state.__dict__.setdefault(
                            "_sr_refused_raw_history", {}
                        ).pop(str(target), None)
                        yield SearchReplaceResult(
                            file=str(target),
                            blocks_applied=1,
                            lines_changed=0,
                            warnings=["Wrote entire file (no SEARCH/REPLACE blocks). "
                                      "Use write_file next time."],
                            content=raw_content[:100] + "...",
                        )
                        return
            raise

        # Read-before-Edit enforcement (Claude Code tool contract).
        # Editing a file without having seen it is the #1 cause of the
        # "SEARCH text not found" failure cascade. Require the model to
        # have read this path (or just written it) this session.
        # Structured rejection (not ToolError) — model sees guidance in
        # the result content and pivots to read_file.
        read_state = ctx.read_file_state if ctx else None
        path_key = str(file_path)
        # When the model passed a directory and we inferred the actual file,
        # we scanned the file content during inference — register it as "read"
        # so the read-before-edit check below passes instead of blocking.
        if read_state is not None:
            _orig = Path(args.file_path.strip()).expanduser()
            if not _orig.is_absolute():
                _orig = Path.cwd() / _orig
            _orig = _orig.resolve()
            if _orig.is_dir() and file_path.is_file() and _orig != file_path:
                import time as _time
                read_state.setdefault(path_key, {"timestamp": int(_time.time() * 1e9)})
        if read_state is not None and file_path.exists():
            prior = read_state.get(path_key)
            if prior is None:
                yield SearchReplaceResult(
                    file=path_key,
                    blocks_applied=0,
                    lines_changed=0,
                    warnings=[],
                    content=(
                        "<system-reminder>\n"
                        f"{file_path.name} has not been read this session. "
                        "Use read_file first so you can see the current "
                        "contents — then search_replace with the actual "
                        "text from the file. This edit was NOT applied.\n"
                        "</system-reminder>"
                    ),
                )
                return
            try:
                current_mtime = file_path.stat().st_mtime_ns
            except OSError:
                current_mtime = 0
            if prior.get("timestamp") and current_mtime and current_mtime > prior["timestamp"]:
                yield SearchReplaceResult(
                    file=path_key,
                    blocks_applied=0,
                    lines_changed=0,
                    warnings=[],
                    content=(
                        "<system-reminder>\n"
                        f"{file_path.name} was modified on disk since your "
                        "last read. Re-read before editing to avoid "
                        "clobbering changes you haven't seen. This edit "
                        "was NOT applied.\n"
                        "</system-reminder>"
                    ),
                )
                return

        # Injection guard: scan replacement content for suspicious patterns
        from drydock.core.tools.injection_guard import check_content_for_injection
        if warning := check_content_for_injection(args.content, args.file_path):
            import logging
            logging.getLogger(__name__).warning("search_replace: %s", warning)

        original_content = await self._read_file(file_path)

        # Detect placeholder/omission patterns that would delete code
        PLACEHOLDER_PATTERNS = [
            "# rest of code", "# ... rest", "# unchanged",
            "// rest of code", "// ... rest", "// unchanged",
            "# TODO: implement", "pass  # placeholder",
            "...",  # bare ellipsis as entire replacement
        ]
        for block in search_replace_blocks:
            replacement = block.replace.strip()
            if replacement in PLACEHOLDER_PATTERNS or any(
                p in replacement.lower() for p in [
                    "rest of code", "rest of the code", "unchanged",
                    "remaining code", "code continues", "etc.",
                ]
            ):
                yield SearchReplaceResult(
                    file=str(file_path),
                    blocks_applied=0,
                    lines_changed=0,
                    warnings=[],
                    content=(
                        f"REFUSED: your REPLACE block contains a placeholder "
                        f"('{replacement[:60]}') that would delete existing code. "
                        f"Provide the COMPLETE replacement — every line that should "
                        f"remain, plus your changes. Do NOT summarise unchanged code."
                    ),
                )
                return

        # Detect no-op edits where SEARCH and REPLACE are byte-identical.
        # Short-circuit before _apply_blocks so we never reach the ambiguous
        # "edited successfully (+0 lines)" path for this structural no-op.
        noop_blocks = [b for b in search_replace_blocks if b.search == b.replace]
        if noop_blocks:
            noop_state = self.state.__dict__.setdefault("_sr_noop_history", {})
            noop_key = str(file_path)
            noop_entry = noop_state.get(noop_key, {"count": 0})
            noop_entry["count"] += 1
            noop_state[noop_key] = noop_entry
            noop_count = noop_entry["count"]
            if noop_count >= 2:
                try:
                    body = original_content[:3000]
                    tail = (
                        f"\n...[truncated, {original_content.count(chr(10))} lines total]"
                        if len(original_content) > 3000 else ""
                    )
                    extra = (
                        f"\n\n[HARD-STOP: #{noop_count} consecutive SEARCH==REPLACE no-op "
                        f"on {file_path.name}. Your SEARCH and REPLACE blocks are still "
                        f"byte-identical — this call can never change anything. "
                        f"DO NOT retry search_replace on this file again. "
                        f"REQUIRED: call write_file with overwrite=True and the complete "
                        f"corrected file content. Current file:\n"
                        f"-----FILE START-----\n{body}{tail}\n-----FILE END-----]"
                    )
                except Exception:
                    extra = (
                        f"\n\n[HARD-STOP: #{noop_count} consecutive SEARCH==REPLACE no-op "
                        f"on {file_path.name}. Stop retrying. Use write_file overwrite=True.]"
                    )
            else:
                extra = (
                    f" Re-read the file with read_file, identify what you actually need "
                    f"to change, and send a corrected SEARCH/REPLACE block."
                )
            yield SearchReplaceResult(
                file=str(file_path),
                blocks_applied=0,
                lines_changed=0,
                warnings=[],
                content=(
                    f"{file_path.name}: ALREADY CORRECT — the SEARCH and REPLACE text "
                    f"are byte-identical, so this block can never make any change.{extra}"
                ),
            )
            return

        block_result = self._apply_blocks(
            original_content,
            search_replace_blocks,
            file_path,
            self.config.fuzzy_threshold,
            read_state,
        )

        # Auto-rename path: intercept performed the rename atomically — return
        # success immediately so the model knows it's done and doesn't retry.
        if (
            not block_result.errors
            and block_result.warnings
            and block_result.warnings[0].startswith("APPLIED:")
        ):
            yield SearchReplaceResult(
                file=str(file_path),
                blocks_applied=block_result.applied,
                lines_changed=-1,  # unknown — rename touched N files
                warnings=[],
                content=block_result.warnings[0],
            )
            return

        if block_result.errors:
            error_message = "SEARCH/REPLACE blocks failed:\n" + "\n\n".join(
                block_result.errors
            )
            if block_result.warnings:
                error_message += "\n\nWarnings encountered:\n" + "\n".join(
                    block_result.warnings
                )

            # Multi-file rename REFUSED loop-breaker: if the model keeps
            # retrying a search_replace that was REFUSED due to multi-file
            # identifier rename detection, escalate to HARD-STOP on the 2nd
            # consecutive REFUSED on the same file.  This makes the agent_loop
            # HARD-STOP detector (344b6a1) mute search_replace for 1 turn so
            # the model is forced to use mechanical_rename or write_file.
            if block_result.errors and block_result.errors[0].startswith("REFUSED:"):
                refused_state = self.state.__dict__.setdefault("_sr_refused_history", {})
                refused_key = str(file_path)
                refused_entry = refused_state.get(refused_key, {"count": 0})
                refused_entry["count"] += 1
                refused_state[refused_key] = refused_entry
                if refused_entry["count"] >= 2:
                    error_message += (
                        f"\n\n[HARD-STOP: #{refused_entry['count']} consecutive "
                        f"REFUSED on {file_path.name}. DO NOT retry search_replace "
                        f"on this file. Use `mechanical_rename` with explicit "
                        f"old_name and new_name instead.]"
                    )
            else:
                refused_state = self.state.__dict__.setdefault("_sr_refused_history", {})
                refused_state.pop(str(file_path), None)  # reset on non-REFUSED failure

            # Mechanical loop-breaker: if search_replace has failed with
            # "Search text not found" on the SAME file 2+ times in a row,
            # embed the current file head in the error so the model sees
            # actual file state and can't keep retrying phantom edits.
            # (One session had 8 consecutive identical search_replace
            # failures with 0 behavior change. Nudges didn't help.)
            state = self.state.__dict__.setdefault("_sr_fail_history", {})
            fail_key = str(file_path)
            entry = state.get(fail_key, {"count": 0})
            entry["count"] += 1
            state[fail_key] = entry
            if entry["count"] == 1:
                # First failure: embed file head so model sees actual content
                # without waiting for a second retry cycle. Reduces
                # retry_after_error:search_replace events significantly.
                try:
                    head = original_content[:1500]
                    line_count = original_content.count("\n")
                    # If write_file previously wrote this file, the stale
                    # SEARCH text is from the pre-write version — say so
                    # explicitly so the model uses write_file again rather
                    # than iterating on the wrong text.
                    path_writes = self.state.__dict__.get("_path_writes", {})
                    if path_writes.get(str(file_path), 0) > 0:
                        hint_prefix = (
                            f"[HINT: search text not found in {file_path.name}. "
                            f"This file was recently overwritten by write_file — "
                            f"your SEARCH text is from the PREVIOUS version. "
                            f"DO NOT retry search_replace; use write_file again "
                            f"with the complete new content. "
                            f"Current file ({line_count} lines):\n"
                            f"-----FILE HEAD-----\n{head}\n-----FILE HEAD END-----]"
                        )
                    else:
                        hint_prefix = (
                            f"[HINT: search text not found in {file_path.name}. "
                            f"File may have changed. Current file head "
                            f"({line_count} lines total):\n"
                            f"-----FILE HEAD-----\n{head}\n-----FILE HEAD END-----\n"
                            f"Adjust your SEARCH text to match the actual content above.]"
                        )
                    error_message += f"\n\n{hint_prefix}"
                except Exception:
                    pass
            elif entry["count"] >= 2:
                try:
                    line_count = original_content.count("\n")
                    count = entry["count"]
                    if count >= 3:
                        # Show full file (up to 4000 chars) and prohibit retry.
                        body = original_content[:4000]
                        tail = (
                            f"\n...[truncated, {line_count} lines total]"
                            if len(original_content) > 4000 else ""
                        )
                        error_message += (
                            f"\n\n[HARD-STOP: this is the #{count} consecutive "
                            f"search_replace failure on {file_path.name}. "
                            f"Your search text was NOT found in the file. "
                            f"DO NOT retry search_replace with the same or similar text. "
                            f"REQUIRED action: call write_file with overwrite=True "
                            f"and provide the complete new file content. "
                            f"Full file content below — use this as the basis "
                            f"for your write_file call:\n"
                            f"-----FILE START-----\n{body}{tail}\n-----FILE END-----]"
                        )
                    else:
                        head = original_content[:2000]
                        error_message += (
                            f"\n\n[LOOP-BREAKER: this is the #{count} "
                            f"consecutive search_replace failure on "
                            f"{file_path.name}. Stop retrying the same search. "
                            f"Actual file content (first 2000 chars of "
                            f"{line_count} lines):\n"
                            f"-----FILE START-----\n{head}\n-----FILE END-----\n"
                            f"Use THIS exact text as your search target, OR "
                            f"abandon this edit and try write_file.]"
                        )
                except Exception:
                    pass

            # Context recovery — query GraphRAG with the file basename
            # and the first symbol in the SEARCH text. If we find the
            # symbol elsewhere in the codebase, append it. Best-effort,
            # never blocks the original error.
            try:
                from drydock.core.context_recovery import (
                    recover_for_search_replace,
                )
                # Pick the first block's search text as the query source.
                first_search = ""
                if args.content:
                    import re as _re
                    m = _re.search(
                        r"<{3,}\s*SEARCH\s*\n(.*?)={3,}", args.content, _re.DOTALL
                    )
                    if m:
                        first_search = m.group(1)[:300]
                recovery = recover_for_search_replace(
                    str(file_path), first_search
                )
                if recovery:
                    error_message += recovery
            except Exception:
                pass  # never block on recovery

            # Return advisory result instead of raising ToolError.
            # Hard ToolError blocks cause their own retry loops on longer tasks
            # (model panics and re-calls the same failing search_replace). The
            # advisory result delivers the same guidance message + file head
            # without triggering the panic-retry pattern.
            yield SearchReplaceResult(
                file=str(file_path),
                blocks_applied=0,
                lines_changed=0,
                content=error_message,
            )
            return
        # Success → reset the fail counter for this file
        state = self.state.__dict__.setdefault("_sr_fail_history", {})
        state.pop(str(file_path), None)
        refused_state = self.state.__dict__.setdefault(
            "_sr_refused_raw_history", {}
        )
        refused_state.pop(str(file_path), None)

        modified_content = block_result.content

        # Calculate line changes
        if modified_content == original_content:
            lines_changed = 0
            # The SEARCH text was found and the REPLACE produced the SAME
            # content as the file already has. Tell the model. Track
            # consecutive no-ops per file so we can escalate — without
            # a counter the byte-identical path hard-stops at #2 but
            # this path lets the model loop indefinitely. Observed
            # 2026-05-20: 3+ no-op retries on the same file with the
            # same SEARCH text. Parity with the byte-identical
            # hard-stop below.
            noop_state = self.state.__dict__.setdefault(
                "_sr_noop_history", {}
            )
            n = noop_state.get(str(file_path), 0) + 1
            noop_state[str(file_path)] = n
            base_msg = (
                f"{file_path.name}: ALREADY CORRECT — the search text was found "
                f"but the replacement is identical to the current content. "
                f"No change was written. The file already has the desired state. "
                f"Move on to the next task."
            )
            if n >= 2:
                base_msg += (
                    f"\n\n[HARD-STOP: #{n} consecutive no-op on "
                    f"{file_path.name}. STOP retrying this file. Either: "
                    f"(a) move on to the NEXT task — your change is "
                    f"already done; (b) edit a DIFFERENT file; or "
                    f"(c) end your turn. The next identical-result "
                    f"search_replace on this file will produce the same "
                    f"no-op.]"
                )
            yield SearchReplaceResult(
                file=str(file_path),
                blocks_applied=block_result.applied,
                lines_changed=0,
                warnings=block_result.warnings,
                content=base_msg,
            )
            return
        else:
            # success-with-real-change path — reset the no-op counter
            noop_state = self.state.__dict__.setdefault(
                "_sr_noop_history", {}
            )
            noop_state.pop(str(file_path), None)
            original_lines = len(original_content.splitlines())
            new_lines = len(modified_content.splitlines())
            lines_changed = new_lines - original_lines

            # 2026-05-18: refuse to commit edits that break Python syntax
            # for files that PARSED CLEAN before the edit. Without this
            # rollback the operator hit Selenium-Login-Bot-style loops
            # (14+ repeated edits, each making things worse). Only block
            # the regression case — if the file was already broken
            # (e.g. the model is editing to FIX a syntax error), we ship
            # the edit so progress isn't blocked.
            if file_path.suffix == ".py":
                try:
                    import ast as _ast
                    _ast.parse(original_content)
                    original_parses = True
                except SyntaxError:
                    original_parses = False
                if original_parses:
                    try:
                        import ast as _ast
                        _ast.parse(modified_content)
                    except SyntaxError as e:
                        mod_lines_full = modified_content.splitlines()
                        snippet = "\n".join(
                            mod_lines_full[
                                max(0, (e.lineno or 1) - 3):
                                ((e.lineno or 1) + 2)
                            ]
                        )
                        # 2026-05-24: indent-mismatch errors are the
                        # most common Gemma 4 failure on search_replace
                        # — the model writes the right code but at the
                        # wrong indent level (drops a parent with/try
                        # scope, or mixes tabs+spaces). Compute the
                        # actual indent of the broken line vs the
                        # nearest preceding non-blank line so the model
                        # sees the numeric difference directly.
                        indent_hint = ""
                        if e.msg and (
                            "indent" in e.msg.lower()
                            or "dedent" in e.msg.lower()
                        ):
                            try:
                                bad_idx = (e.lineno or 1) - 1
                                if 0 <= bad_idx < len(mod_lines_full):
                                    bad_line = mod_lines_full[bad_idx]
                                    bad_lead = (
                                        len(bad_line)
                                        - len(bad_line.lstrip(" \t"))
                                    )
                                    bad_tabs = "\t" in bad_line[:bad_lead]
                                    prev_lead, prev_tabs = None, None
                                    for i in range(
                                        bad_idx - 1,
                                        max(-1, bad_idx - 8), -1,
                                    ):
                                        ln = mod_lines_full[i]
                                        if ln.strip():
                                            prev_lead = (
                                                len(ln)
                                                - len(ln.lstrip(" \t"))
                                            )
                                            prev_tabs = "\t" in ln[:prev_lead]
                                            break
                                    if (prev_lead is not None
                                            and prev_lead != bad_lead):
                                        if bad_tabs != prev_tabs:
                                            indent_hint = (
                                                f"\n\nINDENT MISMATCH: "
                                                f"line {e.lineno} uses "
                                                f"{'tabs' if bad_tabs else 'spaces'} "
                                                f"({bad_lead} char(s)); "
                                                f"previous non-blank line "
                                                f"uses "
                                                f"{'tabs' if prev_tabs else 'spaces'} "
                                                f"({prev_lead} char(s)). "
                                                f"Match the file's existing "
                                                f"indent style."
                                            )
                                        else:
                                            indent_hint = (
                                                f"\n\nINDENT MISMATCH: "
                                                f"line {e.lineno} has "
                                                f"{bad_lead}-char indent; "
                                                f"previous non-blank line "
                                                f"has {prev_lead}-char "
                                                f"indent. Your REPLACE "
                                                f"block likely dropped a "
                                                f"parent scope (with/try/"
                                                f"if/def) or was written "
                                                f"at the wrong level."
                                            )
                            except Exception:
                                pass
                        # Truncation heuristic: if every REPLACE block's
                        # last non-blank line looks incomplete (ends
                        # mid-statement: trailing `.`, `(`, `=`, `,`, or
                        # an identifier followed by nothing), the model
                        # almost certainly hit max_tokens mid-emission.
                        # Tell it so instead of a generic indent-error.
                        # Observed 2026-05-22 in mdparse/cli.py: REPLACE
                        # cut off at `group.a` and the resulting file
                        # had a dangling line; model got an indent-error
                        # message and tried to fix indentation when the
                        # real problem was the REPLACE was truncated.
                        truncation_hint = ""
                        try:
                            _last_replace_line = ""
                            for _blk in search_replace_blocks:
                                _rep_lines = _blk.replace.rstrip().splitlines()
                                if _rep_lines:
                                    _last_replace_line = _rep_lines[-1].rstrip()
                            if _last_replace_line and re.search(
                                r"(?:[\w.](?<![\)\]\}\":'])|[=,([{.]"
                                r"|\b(?:def|class|if|elif|else|for|while|"
                                r"try|except|with|return)\b)\s*$",
                                _last_replace_line,
                            ) and not _last_replace_line.endswith(
                                (":", ")", "]", "}", '"', "'", ",")
                            ):
                                truncation_hint = (
                                    "\n\nTRUNCATION SUSPECTED: the last line of "
                                    f"your REPLACE block was {_last_replace_line!r} "
                                    "— it looks incomplete (cut off mid-statement). "
                                    "The model's response likely hit max_tokens "
                                    "BEFORE finishing the REPLACE block. Split the "
                                    "edit into smaller search_replace calls "
                                    "(one function/class per call), or use "
                                    "write_file with the full new file content."
                                )
                        except Exception:
                            pass
                        yield SearchReplaceResult(
                            file=str(file_path),
                            blocks_applied=0,
                            lines_changed=0,
                            warnings=[
                                f"REJECTED — would introduce SyntaxError at "
                                f"line {e.lineno}: {e.msg}. Original file "
                                f"parsed clean; this edit did not. Common "
                                f"causes: tabs-vs-spaces mismatch in the "
                                f"REPLACE block, missing colon/paren, "
                                f"unbalanced brackets, indentation drift. "
                                f"File NOT modified.\n\nContext around the "
                                f"broken line:\n{snippet}"
                                f"{indent_hint}{truncation_hint}"
                            ],
                            content=(
                                f"{file_path.name}: edit REJECTED "
                                f"(would break syntax at line {e.lineno}: "
                                f"{e.msg}). File NOT modified. "
                                + (truncation_hint.strip() if truncation_hint
                                   else indent_hint.strip() if indent_hint
                                   else "Re-read the file, fix the REPLACE "
                                   "block's indentation/syntax, and retry.")
                            ),
                        )
                        return

            try:
                if self.config.create_backup:
                    await self._backup_file(file_path)
            except Exception:
                pass

            await self._write_file(file_path, modified_content)

            # Update read_file_state so chained edits don't trip Read-
            # before-Edit. We just wrote — we know disk state.
            if read_state is not None:
                try:
                    new_mtime = file_path.stat().st_mtime_ns
                except OSError:
                    new_mtime = 0
                read_state[path_key] = {
                    "content": modified_content,
                    "timestamp": new_mtime,
                    "offset": 0,
                    "limit": None,
                }

        # Terse success content (Claude Code pattern) — don't echo the
        # SEARCH/REPLACE payload back. Model already has it in history;
        # echoing wastes context and tempts re-reading. Warnings still go
        # through so the model sees actionable issues.
        # 2026-05-20: when ALL applied blocks are no-ops (already
        # applied / already correct) the content used to say "edited
        # successfully (N block(s), +0 line(s))". The model read
        # "successfully" and assumed the edit worked, then tried again.
        # Mirror the no-op detection from get_result_display so the LLM
        # sees the truth in its tool result.
        _warns = block_result.warnings or []
        _all_noop = (
            lines_changed == 0
            and block_result.applied > 0
            and _warns
            and all(w.startswith(f"Block {i+1}: ALREADY")
                    for i, w in enumerate(_warns[:block_result.applied]))
        )
        if _all_noop:
            content_msg = (
                f"{file_path.name}: NO-OP — all "
                f"{block_result.applied} block(s) were already applied. "
                f"The file's current state already matches what your "
                f"SEARCH/REPLACE would produce. DO NOT retry this edit; "
                f"move on to the next task or read_file to verify."
            )
        else:
            content_msg = (
                f"{file_path.name} edited successfully "
                f"({block_result.applied} block(s), "
                f"{lines_changed:+d} line(s))."
            )
        yield SearchReplaceResult(
            file=str(file_path),
            blocks_applied=block_result.applied,
            lines_changed=lines_changed,
            warnings=block_result.warnings,
            content=content_msg,
        )

    @final
    def _prepare_and_validate_args(
        self, args: SearchReplaceArgs
    ) -> tuple[Path, list[SearchReplaceBlock]]:
        file_path_str = args.file_path.strip()
        content = args.content.strip()

        # Handle direct old_string/new_string args (Gemma 4 sometimes sends these)
        if not content and args.old_string is not None and args.new_string is not None:
            content = f"<<<<<<< SEARCH\n{args.old_string}\n=======\n{args.new_string}\n>>>>>>> REPLACE"

        # Try to extract file_path from content if missing
        if not file_path_str and content:
            # Look for file path in the content (common when model puts everything in content)
            path_match = re.search(r'(?:file[_\s]?path|path|file)[\s:="\']+([^\s"\']+\.py)', content[:200], re.IGNORECASE)
            if path_match:
                file_path_str = path_match.group(1)

        # Last resort: if file_path is still missing but we have SEARCH text,
        # scan project files for a match.  Gemma 4 frequently drops file_path.
        # Limit scan to avoid hanging on large repos.
        if not file_path_str and content:
            blocks = self._parse_search_replace_blocks(content)
            if blocks:
                search_text = blocks[0].search.strip()
                if search_text and len(search_text) >= 10:
                    project_root = Path.cwd()
                    candidates: list[Path] = []
                    files_checked = 0
                    for ext in ("*.py",):  # Only scan Python files
                        for f in project_root.rglob(ext):
                            if files_checked > 200:
                                break
                            if "__pycache__" in str(f) or ".git" in str(f):
                                continue
                            files_checked += 1
                            try:
                                text = f.read_text(encoding="utf-8", errors="replace")
                                if len(text) > 100_000:
                                    continue
                                if search_text in text:
                                    candidates.append(f)
                            except Exception:
                                continue
                    if len(candidates) == 1:
                        file_path_str = str(candidates[0])
                    elif candidates:
                        candidates.sort(key=lambda p: len(str(p)))
                        file_path_str = str(candidates[0])

        # Detect model pasting a <tool_error> message as SEARCH content.
        # Gemma 4 pattern: receives a tool_error response, then retries
        # search_replace where the SEARCH block IS the error text — never
        # matches anything in source, triggering not_found cascade.
        if content.lstrip().startswith("<tool_error>"):
            raise ToolError(
                "SEARCH_IS_ERROR: Your search_replace content starts with "
                "'<tool_error>' — you have pasted a previous error message as "
                "the SEARCH target. That text does not exist in any source file. "
                "Discard this call. Use read_file to see actual file contents, "
                "then construct a SEARCH block from literal lines in that file."
            )

        if not file_path_str:
            raise ToolError(
                "File path is required. Use: search_replace(file_path='path/to/file.py', content='...')"
            )

        if len(content) > self.config.max_content_size:
            raise ToolError(
                f"Content size ({len(content)} bytes) exceeds max_content_size "
                f"({self.config.max_content_size} bytes)"
            )

        if not content:
            raise ToolError(
                "Empty content provided. You must include SEARCH/REPLACE blocks.\n"
                "Format:\n"
                "<<<<<<< SEARCH\n"
                "exact text to find\n"
                "=======\n"
                "replacement text\n"
                ">>>>>>> REPLACE\n"
                "If you want to create a new file instead, use write_file."
            )

        project_root = Path.cwd()
        file_path = Path(file_path_str).expanduser()
        if not file_path.is_absolute():
            file_path = project_root / file_path
        file_path = file_path.resolve()

        if not file_path.exists():
            raise ToolError(f"File does not exist: {file_path}")

        if not file_path.is_file():
            # Model passed a directory. Try to infer the correct file by
            # scanning for a file in the directory that contains the search text.
            # This avoids the retry loop where the model gets "is a directory"
            # and keeps passing the same directory path. Only attempt when we have
            # SEARCH content — otherwise fall through to the "Path is not a file" handler.
            dir_scan_file_list: list[Path] = []
            if file_path.is_dir() and content:
                blocks_for_infer = self._parse_search_replace_blocks(content)
                if blocks_for_infer:
                    search_text = blocks_for_infer[0].search.strip()
                    if search_text and len(search_text) >= 10:
                        # Scan files in the directory first (most likely match),
                        # then fall back to the entire project.
                        candidates: list[Path] = []
                        scan_dirs = [file_path] + [project_root]
                        files_checked = 0
                        for scan_dir in scan_dirs:
                            for f in scan_dir.rglob("*.py"):
                                if files_checked > 200:
                                    break
                                if "__pycache__" in str(f) or ".git" in str(f):
                                    continue
                                if f in candidates:
                                    continue
                                files_checked += 1
                                if scan_dir == file_path:
                                    dir_scan_file_list.append(f)
                                try:
                                    text = f.read_text(encoding="utf-8", errors="replace")
                                    if len(text) > 100_000:
                                        continue
                                    if search_text in text:
                                        candidates.append(f)
                                except Exception:
                                    continue
                            if candidates:
                                break
                        if len(candidates) == 1:
                            file_path = candidates[0]
                        elif candidates:
                            candidates.sort(key=lambda p: len(str(p)))
                            file_path = candidates[0]
            if not file_path.is_file():
                if dir_scan_file_list:
                    listing = "\n".join(
                        f"  {f.relative_to(file_path)}" for f in sorted(dir_scan_file_list)[:20]
                    )
                    raise ToolError(
                        f"Path is not a file: {file_path}\n"
                        f"Your SEARCH text was not found in any .py file in that directory. "
                        f"Files in {file_path.name}/:\n{listing}\n"
                        f"Specify one of those file paths explicitly."
                    )
                raise ToolError(f"Path is not a file: {file_path}")

        search_replace_blocks = self._parse_search_replace_blocks(content)
        if not search_replace_blocks:
            raise ToolError(
                "NO_BLOCKS:" + content  # sentinel for run() to handle fallback
            )

        # Detect garbled token output — only flag obvious corruption
        # (mixed angle brackets + repeated letters like <<t<ttt<t), not normal repeats
        for block in search_replace_blocks:
            if re.search(r'<[a-z]<[a-z]{2,}<[a-z]', block.search):
                raise ToolError(
                    "Your search text appears garbled (token corruption). "
                    "Use write_file to rewrite the function instead of search_replace."
                )

        return file_path, search_replace_blocks

    async def _read_file(self, file_path: Path) -> str:
        import asyncio

        def _sync_read():
            with open(file_path, encoding="utf-8") as f:
                return f.read()

        try:
            loop = asyncio.get_running_loop()
            return await asyncio.wait_for(
                loop.run_in_executor(None, _sync_read), timeout=30,
            )
        except asyncio.TimeoutError:
            raise ToolError(
                f"Timed out reading {file_path} after 30s. "
                f"The file may be very large or the system is under load. "
                f"Do NOT retry search_replace — use read_file on {file_path.name} "
                f"first to verify the file exists and see its current content."
            )
        except UnicodeDecodeError as e:
            raise ToolError(f"Unicode decode error reading {file_path}: {e}") from e
        except PermissionError:
            raise ToolError(f"Permission denied reading file: {file_path}")
        except Exception as e:
            raise ToolError(f"Unexpected error reading {file_path}: {e}") from e

    async def _backup_file(self, file_path: Path) -> None:
        shutil.copy2(file_path, file_path.with_suffix(file_path.suffix + ".bak"))

    async def _write_file(self, file_path: Path, content: str) -> None:
        import asyncio

        def _sync_write():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        try:
            loop = asyncio.get_running_loop()
            await asyncio.wait_for(
                loop.run_in_executor(None, _sync_write), timeout=30,
            )
        except asyncio.TimeoutError:
            raise ToolError(f"Timed out writing {file_path} after 30s.")
        except PermissionError:
            raise ToolError(f"Permission denied writing to file: {file_path}")
        except OSError as e:
            raise ToolError(f"OS error writing to {file_path}: {e}") from e
        except Exception as e:
            raise ToolError(f"Unexpected error writing to {file_path}: {e}") from e

    @final
    @staticmethod
    def _detect_multifile_rename(
        search: str, replace: str, filepath: Path,
        auto_apply: bool = True,
    ) -> str | None:
        """Pre-execution check: is this SEARCH→REPLACE a multi-file rename
        in disguise that should use `mechanical_rename` instead?

        Detection (v2, token-based — v1 required identical SEARCH text in
        2+ files which never triggered because Gemma 4 tailors per-file
        context):

        1. Compute the set of identifier tokens in SEARCH but NOT REPLACE
           (the "removed" tokens — the bug being renamed away).
        2. Compute the set of tokens in REPLACE but NOT SEARCH (the
           "added" tokens — what's replacing it).
        3. If there's exactly one removed token and the removed token
           appears in 2+ .py files of the same Python package
           (word-bounded), this is a multi-file identifier rename.

        Returns the redirect error string when the pattern matches; returns
        None to let the search_replace proceed normally.

        Gated by DRYDOCK_MULTIFILE_INTERCEPT=1 (default off).
        """
        import os as _os
        if _os.environ.get(
            "DRYDOCK_MULTIFILE_INTERCEPT", "1"
        ).strip().lower() not in ("1", "true", "yes"):
            return None

        # Need some meaningful diff to analyze — skip trivial edits.
        if len(search.strip()) < 30 or len(replace.strip()) < 5:
            return None

        # Locate the package root.
        pkg_root = None
        current = filepath.parent.resolve()
        for _ in range(6):
            if (current / "__init__.py").is_file():
                pkg_root = current
                # Walk up further while parent ALSO has __init__.py
                while (current.parent / "__init__.py").is_file():
                    current = current.parent
                    pkg_root = current
                break
            current = current.parent
            if current == current.parent:
                break
        if pkg_root is None:
            return None

        import re as _re
        s_tokens = set(_re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", search))
        r_tokens = set(_re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", replace))
        only_in_search = s_tokens - r_tokens
        only_in_replace = r_tokens - s_tokens

        # Filter out trivial tokens — too short or stdlib/keyword.
        _NOISE_TOKENS = {
            "self", "cls", "True", "False", "None", "and", "or", "not",
            "if", "else", "elif", "for", "while", "try", "except",
            "import", "from", "as", "def", "class", "return", "in", "is",
            "lambda", "with", "yield", "pass", "break", "continue",
            # missing Python keywords that triggered false-positive multi-file
            # rename detection (e.g. model removes `raise` statements, `raise`
            # was not in noise list so was treated as a user identifier)
            "raise", "del", "global", "nonlocal", "assert", "async", "await",
            "finally", "except", "match", "case",
            "int", "str", "float", "bool", "list", "dict", "set", "tuple",
            "len", "range", "print", "open", "type", "isinstance",
            "Path", "json", "os", "re", "sys",
            # Common English filler words in docstrings/comments. Without
            # these the guard refuses "Add storage backend" rewrites because
            # the new content drops a sentence containing "this/that/needed/etc"
            # while the old content had it — and these words trivially exist
            # in 5+ files across any project. Real cases captured 2026-05-25.
            "this", "that", "these", "those", "what", "which", "when",
            "where", "here", "there", "then", "than", "into", "onto",
            "needed", "uses", "used", "using", "make", "made", "data",
            "file", "files", "name", "names", "value", "values",
            "test", "tests", "method", "methods", "function", "functions",
        }
        candidates = {
            t for t in only_in_search
            if len(t) >= 4 and t not in _NOISE_TOKENS
        }
        if not candidates:
            return None

        # Pick the candidate that appears in the most OTHER .py files
        # within the package. If multiple, prefer the rarest in REPLACE
        # (most likely to be the actual identifier being renamed).
        best_token = None
        best_count = 0
        best_files: list[Path] = []
        scanned = 0
        for token in candidates:
            files_with_token: list[Path] = []
            scanned = 0
            pat = _re.compile(rf"\b{_re.escape(token)}\b")
            for fp in pkg_root.rglob("*.py"):
                scanned += 1
                if scanned > 30:
                    break
                if fp.resolve() == filepath.resolve():
                    continue
                try:
                    if pat.search(fp.read_text(errors="replace")):
                        files_with_token.append(fp)
                except OSError:
                    continue
                if len(files_with_token) >= 6:
                    break
            if len(files_with_token) > best_count:
                best_token = token
                best_count = len(files_with_token)
                best_files = files_with_token

        if best_count < 2:
            return None  # the removed token isn't in 2+ other files — proceed

        # Skip when the "removed" identifier is the package directory name
        # itself. The package name appears in every file via imports
        # (`from tool_agent.x import …`); a rewrite of one file inside the
        # package will trivially "remove" it locally even though the package
        # name is obviously not being renamed. Captured 2026-05-25 in
        # session_20260525_180113 where "Add storage backend: clickhouse"
        # got refused for "removing" `tool_agent`.
        if best_token == pkg_root.name:
            return None

        # A real rename has ONE removed identifier mapping to ONE added
        # identifier. When the new content introduces multiple unrelated
        # new identifiers, the diff is a feature-addition rewrite, not a
        # rename. Captured 2026-05-25 in session_20260525_173957 where
        # "Add storage backend: mongodb" got refused because the new
        # __init__.py adds Bolt/Ceph/LevelDB/MySQL backend classes — the
        # heuristic flagged the multiple-new-tokens as "ambiguous rename
        # target" and refused, when actually nothing is being renamed.
        added_candidates_preview = {
            t for t in only_in_replace
            if len(t) >= 4 and t not in _NOISE_TOKENS
        }
        if len(added_candidates_preview) > 1:
            return None

        # If exactly one new token, we can auto-apply the rename across the
        # package rather than refusing and hoping the model switches tools.
        # Prefix "APPLIED:" so the caller returns success instead of error.
        added_candidates = {
            t for t in only_in_replace
            if len(t) >= 4 and t not in _NOISE_TOKENS
        }
        if len(added_candidates) == 1 and auto_apply:
            new_name = next(iter(added_candidates))
            word_pat = _re.compile(rf"\b{_re.escape(best_token)}\b")
            files_changed: list[str] = []
            for fp in pkg_root.rglob("*.py"):
                parts = set(fp.parts)
                if parts & {"__pycache__", ".git", ".venv", "venv"}:
                    continue
                try:
                    old_text = fp.read_text(errors="replace")
                    new_text = word_pat.sub(new_name, old_text)
                    if new_text != old_text:
                        fp.write_text(new_text)
                        files_changed.append(str(fp.relative_to(pkg_root.parent)))
                except OSError:
                    continue
            if files_changed:
                return (
                    f"APPLIED: auto-renamed `{best_token}` → `{new_name}` "
                    f"across {len(files_changed)} file(s): "
                    f"{', '.join(files_changed[:8])}"
                    + (f" (+{len(files_changed)-8} more)" if len(files_changed) > 8 else "")
                    + ". Run pytest to verify."
                )

        other_files_summary = ", ".join(
            str(fp.relative_to(pkg_root.parent)) for fp in best_files[:5]
        )
        more = f" (+{best_count-5} more)" if best_count > 5 else ""
        added_hint = (
            f" (rename target is ambiguous — multiple new tokens: "
            f"{', '.join(sorted(added_candidates)[:4])})"
            if len(added_candidates) != 1 else ""
        )
        # Embed first 20 lines of the target file so the model has context
        # and stops retrying the same REFUSED search_replace.
        try:
            file_lines = filepath.read_text(errors="replace").splitlines()
            head_lines = file_lines[:20]
            file_head = "\n".join(
                f"{i+1}: {l}" for i, l in enumerate(head_lines)
            )
            file_hint = f"\n\nCurrent {filepath.name} (first 20 lines):\n{file_head}"
        except OSError:
            file_hint = ""
        return (
            f"REFUSED: this search_replace removes the identifier "
            f"`{best_token}`, which appears in {best_count+1} files across "
            f"the `{pkg_root.name}` package ({filepath.name}, "
            f"{other_files_summary}{more}).{added_hint} That's a multi-file "
            f"identifier rename — use `mechanical_rename` with explicit "
            f"old_name and new_name so the rename is unambiguous."
            f"{file_hint}"
        )

    @staticmethod
    def _apply_blocks(
        content: str,
        blocks: list[SearchReplaceBlock],
        filepath: Path,
        fuzzy_threshold: float = 0.9,
        read_state: dict | None = None,
    ) -> BlockApplyResult:
        applied = 0
        errors: list[str] = []
        warnings: list[str] = []
        current_content = content

        # Multi-file rename interception (DRYDOCK_MULTIFILE_INTERCEPT=1).
        # If ANY block's SEARCH text also appears in other .py files of the
        # same package, refuse all blocks and tell the model to use
        # mechanical_rename. Fast-fail before any disk write so we don't
        # leave the file half-edited.
        for search, replace in blocks:
            redirect = SearchReplace._detect_multifile_rename(
                search, replace, filepath,
            )
            if redirect:
                if redirect.startswith("APPLIED:"):
                    # Auto-rename succeeded — return as a warning (not error)
                    # so the model knows it's done and doesn't retry.
                    return BlockApplyResult(
                        content=content,
                        applied=len(blocks),
                        errors=[],
                        warnings=[redirect],
                    )
                return BlockApplyResult(
                    content=content,
                    applied=0,
                    errors=[redirect],
                    warnings=[],
                )

        for i, (search, replace) in enumerate(blocks, 1):
            if search not in current_content:
                # 2026-05-25: Mistral-vibe issue #272 — model sometimes
                # emits search/replace text with LITERAL '\\n' / '\\t'
                # / '\\r' escape sequences instead of real newlines/tabs.
                # The file has real newlines, the search doesn't match.
                # If the search contains escape sequences AND the file
                # doesn't have those literals, try the unescaped version
                # before giving up.
                _backslash_n_count = search.count("\\n")
                _real_newline_count = search.count("\n")
                if (_backslash_n_count >= 2
                        and _real_newline_count <= 1
                        and "\\n" not in current_content[:5000]):
                    try:
                        unescaped = (
                            search
                            .replace("\\n", "\n")
                            .replace("\\t", "\t")
                            .replace("\\r", "\r")
                        )
                        if unescaped in current_content:
                            warnings.append(
                                f"Block {i}: auto-unescaped literal "
                                f"\\n/\\t/\\r sequences in SEARCH text "
                                f"(model emitted escape literals, file "
                                f"has real newlines). Use real newlines "
                                f"in SEARCH/REPLACE blocks — backslash-n "
                                f"sequences won't match unless the file "
                                f"literally contains the two-char string."
                            )
                            search = unescaped
                            # Also unescape REPLACE in lock-step so we
                            # don't write back the broken escaped form.
                            if (replace.count("\\n") >= 1
                                    and replace.count("\n") <= 1):
                                replace = (
                                    replace
                                    .replace("\\n", "\n")
                                    .replace("\\t", "\t")
                                    .replace("\\r", "\r")
                                )
                    except Exception:
                        pass

            if search not in current_content:
                # Check if this change was ALREADY APPLIED — the replacement
                # text is in the file but the search text is not.  This is the
                # #1 cause of edit loops: the model successfully edits a file
                # then retries the same edit because it doesn't realise it
                # already worked.
                if (replace and replace.strip()
                        and len(replace.strip()) >= 10
                        and replace.strip() in current_content):
                    # 2026-05-23: previously the message said "Move on to the
                    # next task" — but when the original buggy pattern had
                    # MULTIPLE identical occurrences in the file, fixing one
                    # via search_replace doesn't fix the others. Telling the
                    # model to stop after the first match leaves the other
                    # instances broken (operator hit this in slides_gui/app.py
                    # where lines 101 and 124 had the same Path+str bug; only
                    # 101 got fixed, model loop-stopped after the warning).
                    #
                    # Heuristic: extract the "bug signature" — lines that
                    # appear in SEARCH but not in REPLACE — and check if any
                    # of them still occur in the file. If yes, the bug
                    # remains at another site.
                    bug_signatures = [
                        ln.strip() for ln in search.splitlines()
                        if ln.strip() and ln.strip() not in replace
                        and len(ln.strip()) >= 15      # avoid one-token false matches
                    ]
                    remaining_sites: list[tuple[str, int]] = []
                    for sig in bug_signatures:
                        # Count exact-line occurrences in the file.
                        occ = current_content.count(sig)
                        if occ > 0:
                            # Find first line number for the operator/model.
                            for ln_no, ln in enumerate(current_content.splitlines(), start=1):
                                if sig in ln:
                                    remaining_sites.append((sig[:60], ln_no))
                                    break
                    if remaining_sites:
                        sites_desc = "; ".join(
                            f"line {ln}: {sig!r}" for sig, ln in remaining_sites[:3]
                        )
                        warnings.append(
                            f"Block {i}: PARTIAL APPLY — the replacement was applied to "
                            f"ONE site but the original buggy pattern still appears at "
                            f"{len(remaining_sites)} other location(s) in {filepath.name}: "
                            f"{sites_desc}. Emit another search_replace with more "
                            f"surrounding context to target each remaining site, or "
                            f"re-read the file and verify what still needs fixing."
                        )
                    else:
                        warnings.append(
                            f"Block {i}: ALREADY APPLIED — the replacement text already "
                            f"exists in {filepath.name} and no other instances of the "
                            f"original pattern remain. Re-read the file to verify "
                            f"completeness before declaring done."
                        )
                    # Count as "applied" so we don't error — at least one site is correct.
                    applied += 1
                    continue
                # Also detect deletion that already happened (search text removed,
                # replace is empty — the line is simply gone).  Only trigger
                # for meaningful search strings to avoid false positives.
                if (not replace or not replace.strip()) and len(search.strip()) >= 10:
                    warnings.append(
                        f"Block {i}: ALREADY APPLIED — the text you want to remove "
                        f"is already absent from {filepath.name}. "
                        f"Move on to the next task."
                    )
                    applied += 1
                    continue

                # Try auto-applying high-confidence fuzzy match (>= 0.95 similarity)
                auto_apply_threshold = max(fuzzy_threshold, 0.95)
                best_match = SearchReplace._find_best_fuzzy_match(
                    current_content, search, auto_apply_threshold
                )
                if best_match and best_match.similarity >= auto_apply_threshold:
                    # SAFETY: only auto-apply if the diff between the
                    # model's SEARCH and the matched text is WHITESPACE
                    # only. Observed 2026-05-22: model's SEARCH ended
                    # with "@pytest.fixture(" but the file had
                    # "@pytest.fixture" (no paren). 96% similarity →
                    # auto-apply → REPLACE wrote the file with an
                    # unclosed paren → SyntaxError. The fuzzy matcher
                    # should only fix indent/space drift, not
                    # structural characters.
                    _normalize = lambda s: re.sub(r"\s+", " ", s).strip()
                    if _normalize(best_match.text) != _normalize(search):
                        # Diff includes non-whitespace chars — refuse
                        # auto-apply and fall through to the fuzzy
                        # context error path so the model can fix
                        # its SEARCH explicitly.
                        pass
                    else:
                        # Auto-apply: replace the fuzzy-matched text with the replacement
                        current_content = current_content.replace(best_match.text, replace, 1)
                        applied += 1
                        similarity_pct = best_match.similarity * 100
                        warnings.append(
                            f"Block {i}: auto-applied via fuzzy match ({similarity_pct:.1f}% similarity, "
                            f"lines {best_match.start_line}-{best_match.end_line}). "
                            f"Whitespace differences were normalized."
                        )
                        continue

                context = SearchReplace._find_search_context(current_content, search)
                fuzzy_context = SearchReplace._find_fuzzy_match_context(
                    current_content, search, fuzzy_threshold
                )

                error_msg = (
                    f"SEARCH/REPLACE block {i} failed: Search text not found in {filepath}\n"
                    f"Search text was:\n{search!r}\n"
                    f"Context analysis:\n{context}"
                )

                if fuzzy_context:
                    error_msg += f"\n{fuzzy_context}"
                elif "not found anywhere" in context:
                    # First search line not found at all — embed file head so the
                    # model can craft a correct SEARCH block without calling read_file.
                    head_lines = current_content.split("\n")[:30]
                    head = "\n".join(head_lines)
                    error_msg += (
                        f"\nFile head (first {len(head_lines)} lines of actual content):\n"
                        f"```\n{head}\n```\n"
                        "Read the file head above and craft your SEARCH block using "
                        "text that actually appears in the file."
                    )

                # If the model previously edited this file (its own SR or
                # write_file mutated current_content since the last read_file),
                # the search text it's using might be the PRE-EDIT version.
                # Surface this explicitly so the model re-reads instead of
                # retrying the stale text. Observed 2026-05-22: P4 pipeflow
                # SR for `v = row.get(col.name, "")` failed because the model
                # had ALREADY refactored that line earlier in the session to
                # `v = row.get(csv_name, "")`. Without this hint the model
                # just retries with the same wrong text.
                try:
                    if read_state is not None:
                        prior = read_state.get(str(filepath))
                        if (prior
                                and prior.get("content")
                                and search not in prior["content"]):
                            error_msg += (
                                "\n\n[POSSIBLE STALE SEARCH: you have edited "
                                f"{filepath.name} since your last read_file "
                                "on it — the SEARCH text doesn't appear in "
                                "the file's CURRENT state. The text you're "
                                "looking for may have been replaced by an "
                                "earlier edit this session. read_file "
                                f"{filepath.name} again to see the current "
                                "content before retrying.]"
                            )
                except Exception:
                    pass

                error_msg += (
                    "\nDebugging tips:\n"
                    "1. Check for exact whitespace/indentation match\n"
                    "2. Verify line endings match the file exactly (\\r\\n vs \\n)\n"
                    "3. Ensure the search text hasn't been modified by previous blocks or user edits\n"
                    "4. Check for typos or case sensitivity issues"
                )

                errors.append(error_msg)
                continue

            occurrences = current_content.count(search)
            if occurrences > 1:
                warning_msg = (
                    f"Search text in block {i} appears {occurrences} times in the file. "
                    f"Only the first occurrence will be replaced. Consider making your "
                    f"search pattern more specific to avoid unintended changes."
                )
                warnings.append(warning_msg)

            current_content = current_content.replace(search, replace, 1)
            applied += 1

        return BlockApplyResult(
            content=current_content, applied=applied, errors=errors, warnings=warnings
        )

    @final
    @staticmethod
    def _find_fuzzy_match_context(
        content: str, search_text: str, threshold: float = 0.9
    ) -> str | None:
        best_match = SearchReplace._find_best_fuzzy_match(
            content, search_text, threshold
        )

        if not best_match:
            return None

        diff = SearchReplace._create_unified_diff(
            search_text, best_match.text, "SEARCH", "CLOSEST MATCH"
        )

        similarity_pct = best_match.similarity * 100

        return (
            f"Closest fuzzy match (similarity {similarity_pct:.1f}%) "
            f"at lines {best_match.start_line}–{best_match.end_line}:\n"
            f"```diff\n{diff}\n```"
        )

    @final
    @staticmethod
    def _find_best_fuzzy_match(  # noqa: PLR0914
        content: str, search_text: str, threshold: float = 0.9
    ) -> FuzzyMatch | None:
        content_lines = content.split("\n")
        search_lines = search_text.split("\n")
        window_size = len(search_lines)

        if window_size == 0:
            return None

        non_empty_search = [line for line in search_lines if line.strip()]
        if not non_empty_search:
            return None

        first_anchor = non_empty_search[0]
        last_anchor = (
            non_empty_search[-1] if len(non_empty_search) > 1 else first_anchor
        )

        candidate_starts = set()
        spread = 5

        for i, line in enumerate(content_lines):
            if first_anchor in line or last_anchor in line:
                start_min = max(0, i - spread)
                start_max = min(len(content_lines) - window_size + 1, i + spread + 1)
                for s in range(start_min, start_max):
                    candidate_starts.add(s)

        if not candidate_starts:
            max_positions = min(len(content_lines) - window_size + 1, 100)
            candidate_starts = set(range(0, max_positions))

        best_match = None
        best_similarity = 0.0

        for start in candidate_starts:
            end = start + window_size
            window_text = "\n".join(content_lines[start:end])

            matcher = difflib.SequenceMatcher(None, search_text, window_text)
            similarity = matcher.ratio()

            if similarity >= threshold and similarity > best_similarity:
                best_similarity = similarity
                best_match = FuzzyMatch(
                    similarity=similarity,
                    start_line=start + 1,  # 1-based line numbers
                    end_line=end,
                    text=window_text,
                )

        return best_match

    @final
    @staticmethod
    def _create_unified_diff(
        text1: str, text2: str, label1: str = "SEARCH", label2: str = "CLOSEST MATCH"
    ) -> str:
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)

        lines1 = [line if line.endswith("\n") else line + "\n" for line in lines1]
        lines2 = [line if line.endswith("\n") else line + "\n" for line in lines2]

        diff = difflib.unified_diff(
            lines1, lines2, fromfile=label1, tofile=label2, lineterm="", n=3
        )

        diff_lines = list(diff)

        if diff_lines and not diff_lines[0].startswith("==="):
            diff_lines.insert(2, "=" * 67 + "\n")

        result = "".join(diff_lines)

        max_chars = 2000
        if len(result) > max_chars:
            result = result[:max_chars] + "\n...(diff truncated)"

        return result.rstrip()

    @final
    @staticmethod
    def _parse_search_replace_blocks(content: str) -> list[SearchReplaceBlock]:
        """Parse SEARCH/REPLACE blocks from content.

        Supports multiple formats for model compatibility:
        1. Standard: <<<<<<< SEARCH ... ======= ... >>>>>>> REPLACE
        2. With code fences: ```...<<<<<<< SEARCH...```
        3. Simple separator: old_text\n=======\nnew_text (Gemma 4 style)
        4. JSON: {"old_string": "...", "new_string": "..."} or {"search": "...", "replace": "..."}
        """
        # Try standard format first
        matches = SEARCH_REPLACE_BLOCK_WITH_FENCE_RE.findall(content)
        if not matches:
            matches = SEARCH_REPLACE_BLOCK_RE.findall(content)

        if matches:
            return [
                SearchReplaceBlock(
                    search=search.rstrip("\r\n"), replace=replace.rstrip("\r\n")
                )
                for search, replace in matches
            ]

        # Fallback: try JSON format (some models send structured args)
        import json
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                old = data.get("old_string") or data.get("search") or data.get("old")
                new = data.get("new_string") or data.get("replace") or data.get("new")
                if old is not None and new is not None:
                    return [SearchReplaceBlock(search=str(old), replace=str(new))]
        except (json.JSONDecodeError, TypeError):
            pass

        # Fallback: simple ======= separator (Gemma 4 often uses this)
        if "\n=======\n" in content:
            parts = content.split("\n=======\n", 1)
            if len(parts) == 2:
                search = parts[0].strip()
                replace = parts[1].strip()
                if search:
                    return [SearchReplaceBlock(search=search, replace=replace)]

        # Fallback: --- separator
        if "\n---\n" in content:
            parts = content.split("\n---\n", 1)
            if len(parts) == 2:
                search = parts[0].strip()
                replace = parts[1].strip()
                if search:
                    return [SearchReplaceBlock(search=search, replace=replace)]

        return []

    @final
    @staticmethod
    def _find_search_context(
        content: str, search_text: str, max_context: int = 5
    ) -> str:
        lines = content.split("\n")
        search_lines = search_text.split("\n")

        if not search_lines:
            return "Search text is empty"

        first_search_line = search_lines[0].strip()
        if not first_search_line:
            return "First line of search text is empty or whitespace only"

        matches = []
        for i, line in enumerate(lines):
            if first_search_line in line:
                matches.append(i)

        if not matches:
            return f"First search line '{first_search_line}' not found anywhere in file"

        context_lines = []
        for match_idx in matches[:3]:
            start = max(0, match_idx - max_context)
            end = min(len(lines), match_idx + max_context + 1)

            context_lines.append(f"\nPotential match area around line {match_idx + 1}:")
            for i in range(start, end):
                marker = ">>>" if i == match_idx else "   "
                context_lines.append(f"{marker} {i + 1:3d}: {lines[i]}")

        return "\n".join(context_lines)
