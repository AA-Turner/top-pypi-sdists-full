"""Shared implementation helpers for sandbox-backed CLI tools.

Used by both ``ClaudeCodeToolset`` and ``CLIToolset`` so the bash/glob/grep/
read/write/edit/multi_edit logic lives in exactly one place. The two toolsets
declare their own Pydantic parameter models (with whatever field names their
agent surface expects) and delegate the actual work to the ``_*_impl`` helpers
defined here.

Public exports:

* :func:`download_text` / :func:`upload_text` — small text I/O helpers over
  the sandbox's bytes-only ``download``/``check_run`` API. Re-exported from
  ``openreward.environments`` for env-side use (e.g. an env's custom ``@tool``
  needs to upload a generated manifest into the sandbox before running it).
"""
from __future__ import annotations

import base64
import os
from typing import Any, Dict, List, Optional

from .types import TextBlock, ToolOutput


# ── Public text helpers ─────────────────────────────────────────────────────

async def download_text(sandbox: Any, path: str, encoding: str = "utf-8") -> str:
    """Read a text file from the sandbox.

    The SDK's ``sandbox.download`` returns raw bytes; this is the
    canonical way for env-side code to read a file as a string.
    """
    data = await sandbox.download(path)
    return data.decode(encoding)


async def upload_text(
    sandbox: Any,
    path: str,
    content: str,
    *,
    ensure_trailing_newline: bool = True,
) -> None:
    """Write text content to a file in the sandbox.

    Uses ``check_run`` with a base64-encoded payload so binary-safe
    transfer works without depending on ``sandbox.upload`` (which expects
    a local-FS path, not in-memory bytes).
    """
    if ensure_trailing_newline and not content.endswith("\n"):
        content = content + "\n"
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    await sandbox.check_run(f"echo '{encoded}' | base64 -d > {path}")


# ── Tool body helpers ───────────────────────────────────────────────────────
#
# These functions take primitive Python values (not Pydantic models) so the
# two toolsets can have independent param model definitions if they need to —
# e.g. ClaudeCodeToolset names grep's filter field ``glob`` while the legacy
# CLIToolset names it ``include``. Both toolsets unpack their params and call
# the same helper.

async def _bash_impl(sandbox: Any, command: str) -> ToolOutput:
    try:
        output, code = await sandbox.run(command.strip())
        return ToolOutput(
            blocks=[TextBlock(text=f"{output}\n\n(exit {code})")],
            metadata={"output": output, "exit_code": code},
            reward=0.0,
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error executing command: {str(e)}")],
            finished=False,
        )


async def _glob_impl(sandbox: Any, pattern: str, path: Optional[str]) -> ToolOutput:
    try:
        search_path = path or "."
        cmd = f"find {search_path} -name '{pattern}' -type f | sort"
        output, code = await sandbox.run(cmd)
        return ToolOutput(
            metadata={"output": output, "exit_code": code},
            blocks=[TextBlock(text=f"{output}\n\n(exit {code})")],
            reward=0.0,
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error in glob search: {str(e)}")],
            finished=False,
        )


async def _grep_impl(
    sandbox: Any,
    pattern: str,
    path: Optional[str],
    file_filter: Optional[str],
) -> ToolOutput:
    try:
        search_path = path or "."
        if file_filter:
            cmd = (
                f"find {search_path} -name '{file_filter}' -type f "
                f"-exec grep -Hn '{pattern}' {{}} \\;"
            )
        else:
            cmd = f"grep -r -n '{pattern}' {search_path}"
        output, code = await sandbox.run(cmd)
        return ToolOutput(
            metadata={"output": output, "exit_code": code},
            blocks=[TextBlock(text=f"{output}\n\n(exit {code})")],
            reward=0.0,
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error in grep search: {str(e)}")],
            finished=False,
        )


async def _ls_impl(sandbox: Any, path: str) -> ToolOutput:
    try:
        output, code = await sandbox.run(f"ls -la {path}")
        return ToolOutput(
            metadata={"output": output, "exit_code": code},
            blocks=[TextBlock(text=f"{output}\n\n(exit {code})")],
            reward=0.0,
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error listing directory: {str(e)}")],
            finished=False,
        )


async def _read_impl(
    sandbox: Any,
    file_path: str,
    offset: Optional[int],
    limit: Optional[int],
) -> ToolOutput:
    try:
        if offset and limit:
            end_line = offset + limit
            cmd = f"sed -n '{offset},{end_line}p' {file_path} | cat -n"
            output, code = await sandbox.run(cmd)
        elif offset:
            cmd = f"tail -n +{offset} {file_path} | cat -n"
            output, code = await sandbox.run(cmd)
        elif limit:
            cmd = f"head -n {limit} {file_path} | cat -n"
            output, code = await sandbox.run(cmd)
        else:
            content = await download_text(sandbox, file_path)
            lines = content.splitlines()
            output = "\n".join(f"{idx + 1}\t{line}" for idx, line in enumerate(lines))
            if content.endswith("\n") and output:
                output += "\n"
            code = 0
        return ToolOutput(
            metadata={"output": output, "exit_code": code},
            blocks=[TextBlock(text=f"{output}\n\n(exit {code})")],
            reward=0.0,
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error reading file: {str(e)}")],
            finished=False,
        )


async def _write_impl(sandbox: Any, file_path: str, content: str) -> ToolOutput:
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name:
            await sandbox.run(f"mkdir -p {dir_name}")
        await upload_text(sandbox, file_path, content, ensure_trailing_newline=True)
        return ToolOutput(
            metadata={"output": "", "exit_code": 0},
            blocks=[TextBlock(text=f"Successfully wrote to {file_path}\n\n(exit 0)")],
            reward=0.0,
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error writing file: {str(e)}")],
            finished=False,
        )


async def _edit_impl(
    sandbox: Any,
    file_path: str,
    old_string: str,
    new_string: str,
    replace_all: bool,
) -> ToolOutput:
    """Strict-uniqueness edit: errors if ``old_string`` is non-unique and ``replace_all=False``.

    Output shape matches the historical ``ClaudeCodeToolset.edit`` exactly —
    both toolsets that delegate here see byte-identical responses to what
    ``ClaudeCodeToolset.edit`` returned before this refactor.

    Multiline patterns and regex metacharacters in ``old_string``/
    ``new_string`` work verbatim — no shell or regex interpretation happens.
    """
    try:
        content = await download_text(sandbox, file_path)

        count = content.count(old_string)
        if count == 0:
            return ToolOutput(
                metadata={"error": f"String not found in {file_path}"},
                blocks=[TextBlock(text=f"Error: old_string not found in {file_path}")],
                finished=False,
            )
        if not replace_all and count > 1:
            return ToolOutput(
                metadata={"error": f"old_string appears {count} times; use replace_all or provide more context"},
                blocks=[TextBlock(text=f"Error: old_string appears {count} times in {file_path}. Must be unique unless replace_all=true.")],
                finished=False,
            )

        if replace_all:
            new_content = content.replace(old_string, new_string)
        else:
            new_content = content.replace(old_string, new_string, 1)

        await upload_text(sandbox, file_path, new_content, ensure_trailing_newline=True)

        return ToolOutput(
            metadata={"output": "", "exit_code": 0},
            blocks=[TextBlock(text=f"Successfully edited {file_path}\n\n(exit 0)")],
            reward=0.0,
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error editing file: {str(e)}")],
            finished=False,
        )


async def _multi_edit_impl(
    sandbox: Any,
    file_path: str,
    edits: List[Dict[str, Any]],
) -> ToolOutput:
    """Apply a sequence of edits to a file in one round-trip.

    Output shape matches the historical env-local ``CLIEnvironment.multi_edit``
    exactly (this is the only multi_edit consumer; ``ClaudeCodeToolset``
    never exposed multi_edit), so envs migrating from local-copy
    ``CLIEnvironment`` to ``CLIToolset`` see byte-identical responses.

    Each edit is ``{old_string, new_string, replace_all?}``. Edits apply
    in order to the in-memory buffer; the file is only written back
    after all edits succeed. If any edit's ``old_string`` is missing
    from the current buffer the whole multi-edit fails and the file is
    left untouched.
    """
    try:
        content = await download_text(sandbox, file_path)
        total_replacements = 0

        for edit in edits:
            old_str = edit.get("old_string", "")
            new_str = edit.get("new_string", "")
            replace_all = bool(edit.get("replace_all", False))

            if old_str not in content:
                return ToolOutput(
                    metadata={"error": f"String '{old_str}' not found in file"},
                    blocks=[TextBlock(text=f"String '{old_str}' not found in file")],
                    finished=False,
                )

            if replace_all:
                replacements = content.count(old_str)
                content = content.replace(old_str, new_str)
            else:
                replacements = 1
                content = content.replace(old_str, new_str, 1)

            total_replacements += replacements

        await upload_text(sandbox, file_path, content, ensure_trailing_newline=True)

        return ToolOutput(
            metadata={"total_replacements": total_replacements, "edits_applied": len(edits)},
            blocks=[TextBlock(text=f"Successfully applied {len(edits)} edits with {total_replacements} total replacements")],
            finished=False,
        )
    except Exception as e:
        return ToolOutput(
            metadata={"error": str(e)},
            blocks=[TextBlock(text=f"Error in multi-edit: {str(e)}")],
            finished=False,
        )
