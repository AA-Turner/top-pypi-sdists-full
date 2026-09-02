from __future__ import annotations

import asyncio
import re
import traceback
from pathlib import Path
from typing import Any

import httpx

from matrx_ai.tools._sandbox_runtime import scoped_base_for
from matrx_ai.tools.kinds.execution import ShellExecution
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

_MAX_OUTPUT = 10_240


def _workspace_dir(ctx: ToolContext) -> Path:
    base = scoped_base_for(ctx.user_id, ctx.project_id)
    base.mkdir(parents=True, exist_ok=True)
    return base


async def code_execute_python(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import CodeExecutePythonArgs
    parsed = CodeExecutePythonArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    code_input = parsed.code_input
    timeout = parsed.timeout_seconds

    if not code_input:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="code_input is required."),
        )

    # Strip ```python ... ``` markers if present
    match = re.search(r"```python\s*(.*?)\s*```", code_input, re.DOTALL)
    code = match.group(1).strip() if match else code_input.strip()

    if not code:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="No Python code found after stripping markdown markers.",
            ),
        )

    workspace = _workspace_dir(ctx)
    script_path = workspace / "_execute_python.py"

    try:
        script_path.write_text(code)

        process = await asyncio.create_subprocess_exec(
            "python3",
            str(script_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(workspace),
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
        except TimeoutError:
            process.kill()
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="timeout",
                    message=f"Python execution timed out after {timeout}s.",
                    is_retryable=True,
                    suggested_action="Simplify the code or increase timeout_seconds.",
                ),
            )
        finally:
            try:
                script_path.unlink()
            except Exception:
                pass

        stdout_text = stdout.decode("utf-8", errors="replace")
        stderr_text = stderr.decode("utf-8", errors="replace")

        stdout_str = stdout_text
        if len(stdout_text) > _MAX_OUTPUT:
            log_path = workspace / "_python_stdout.log"
            log_path.write_text(stdout_text)
            stdout_str = f"...(Truncated {len(stdout_text)} bytes. Full output written to {log_path})...\n" + stdout_text[-_MAX_OUTPUT:]
            
        stderr_str = stderr_text
        if len(stderr_text) > _MAX_OUTPUT:
            err_path = workspace / "_python_stderr.log"
            err_path.write_text(stderr_text)
            stderr_str = f"...(Truncated {len(stderr_text)} bytes. Full output written to {err_path})...\n" + stderr_text[-_MAX_OUTPUT:]
        success = process.returncode == 0

        return ToolResult(
            success=success,
            # KindModel result (KIND_TOOL_LEDGER): shared shell_execution shape.
            output=ShellExecution(
                stdout=stdout_str,
                stderr=stderr_str,
                exit_code=process.returncode,
            ).model_dump(mode="json"),
            error=ToolError(
                error_type="python_error",
                message=f"Python exited with code {process.returncode}: {stderr_str[:500]}",
            )
            if not success
            else None,
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def code_store_html(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import CodeStoreHtmlArgs
    CodeStoreHtmlArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    html_input = args.get("html_input", "")
    if not html_input:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="html_input is required."),
        )

    api_url = "http://d88ooscwwggkcwswg8gks4s8.matrxserver.com:3000/store-html"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(api_url, json={"html": html_input})
        response.raise_for_status()
        return ToolResult(success=True, output={"id": response.json().get("id")})
    except httpx.HTTPError as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=f"Failed to store HTML: {e}"
            ),
        )


def _resolve_project_root(project_root: str) -> str | None:
    if not project_root:
        return None
    p = Path(project_root)
    if not p.is_absolute():
        # Resolve relative to cwd
        p = Path.cwd() / p
    p = p.resolve()
    return str(p) if p.is_dir() else None


async def code_fetch_code(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Fetch full file content from a directory using CodeContextBuilder.

    output_mode controls token cost:
      "original"   — raw content, unmodified (100% tokens)
      "clean"      — content with comments stripped (~70-80% tokens)
      "signatures" — function/class signatures only (~5-10% tokens)

    Use "signatures" for large modules where you just need the API surface.
    Use "clean" or "original" for focused editing or review of small modules.
    """
    from matrx_ai.tools._generated_declarations import CodeFetchCodeArgs
    CodeFetchCodeArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    from matrx_utils.code_context import CodeContextBuilder

    project_root_raw = args.get("project_root", "")
    subdirectory = args.get("subdirectory", "") or None
    output_mode = args.get("output_mode", "clean")

    valid_modes = ["original", "clean", "signatures"]
    if output_mode not in valid_modes:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"output_mode must be one of {valid_modes}.",
                suggested_action="Use 'signatures' for large codebases, 'clean' for focused review, 'original' when comments matter.",
            ),
        )

    project_root = _resolve_project_root(project_root_raw)
    if not project_root:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"project_root '{project_root_raw}' is not a valid directory.",
                suggested_action="Provide an absolute path or a path relative to the current working directory.",
            ),
        )

    # Validate subdirectory if provided
    if subdirectory:
        full_path = Path(project_root) / subdirectory
        if not full_path.is_dir():
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"subdirectory '{subdirectory}' does not exist under '{project_root}'.",
                ),
            )

    try:
        builder = CodeContextBuilder(
            project_root=project_root,
            subdirectory=subdirectory,
            output_mode=output_mode,
        )
        result = builder.build()
        return ToolResult(
            success=True,
            output={
                "output_mode": output_mode,
                "project_root": project_root,
                "subdirectory": subdirectory or "",
                "files_included": result.stats["total_files"],
                "directories": result.stats["total_directories"],
                "content": result.combined_text,
            },
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def code_fetch_tree(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Get the directory and file tree of a project or subdirectory.

    Uses CodeContextBuilder in "tree_only" mode — returns just the directory structure
    with no file content (~1% of full token cost). Ideal for orientation before deciding
    which subdirectory to fetch in full with code_fetch_code.
    """
    from matrx_ai.tools._generated_declarations import CodeFetchTreeArgs
    CodeFetchTreeArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    from matrx_utils.code_context import CodeContextBuilder

    project_root_raw = args.get("project_root", "")
    subdirectory = args.get("subdirectory", "") or None
    show_all_directories = args.get("show_all_directories", False)

    project_root = _resolve_project_root(project_root_raw)
    if not project_root:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"project_root '{project_root_raw}' is not a valid directory.",
                suggested_action="Provide an absolute path or a path relative to the current working directory.",
            ),
        )

    if subdirectory:
        full_path = Path(project_root) / subdirectory
        if not full_path.is_dir():
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"subdirectory '{subdirectory}' does not exist under '{project_root}'.",
                ),
            )

    try:
        builder = CodeContextBuilder(
            project_root=project_root,
            subdirectory=subdirectory,
            output_mode="tree_only",
            show_all_tree_directories=show_all_directories,
        )
        from matrx_ai.tools.kinds.code_docs import CodeTreeResult

        result = builder.build()
        return ToolResult(
            success=True,
            output=CodeTreeResult(
                project_root=project_root,
                subdirectory=subdirectory or "",
                files_included=result.stats["total_files"],
                directories=result.stats["total_directories"],
                file_types=result.stats["file_types"],
                tree=result.combined_text,
            ),
        )
    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )
