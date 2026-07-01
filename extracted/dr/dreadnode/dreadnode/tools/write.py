"""File writing tool with automatic directory creation."""

import typing as t
from pathlib import Path

import aiofiles

from dreadnode.agents.tools import tool


@tool
async def write(
    file_path: t.Annotated[str, "Path to the file to write"],
    content: t.Annotated[str, "Content to write to the file"],
    *,
    cwd: t.Annotated[str | None, "Working directory for relative paths"] = None,
) -> str:
    """
    Write content to a file, creating parent directories as needed.

    This tool will overwrite the existing file if there is one at the
    provided path. If this is an existing file, you MUST use the ``read``
    tool first to understand the file's contents.

    - ALWAYS prefer editing existing files with ``edit_file`` or
      ``multiedit``. NEVER write new files unless explicitly required.
    - NEVER proactively create documentation files (``*.md``) or README
      files unless explicitly requested.
    - Always provide the complete intended file content.

    Args:
        file_path: Path to the file (absolute or relative to cwd).
        content: Complete file content to write.
        cwd: Working directory for resolving relative paths.

    Returns:
        Success message.
    """
    base = Path(cwd) if cwd else Path.cwd()
    path = base / file_path if not Path(file_path).is_absolute() else Path(file_path)

    # Ensure parent directories exist.
    path.parent.mkdir(parents=True, exist_ok=True)

    existed = path.exists() and path.is_file()

    # Write the file.
    async with aiofiles.open(path, "w") as f:
        await f.write(content)

    status = "overwritten" if existed else "created"
    return f"Wrote {path} ({status})"
