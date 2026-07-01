"""
File pattern matching tool — find files by glob pattern.

Uses ripgrep (rg --files --glob) when available for speed and .gitignore
awareness.  Falls back to pathlib.glob when rg is not installed.
"""

import typing as t
from pathlib import Path

from dreadnode.agents.tools import tool
from dreadnode.tools._ripgrep import find_rg, run_rg

MAX_RESULTS = 100
"""Hard cap on returned file paths."""


# --- Backends -----------------------------------------------------------------


async def _glob_rg(pattern: str, search_dir: str) -> list[tuple[str, float]]:
    """Use ripgrep to find files matching a glob pattern.

    Returns list of (absolute_path, mtime) tuples.
    """
    args = [
        "--files",
        "--glob",
        pattern,
        "--hidden",
        "--glob=!.git/*",
    ]
    exit_code, stdout, _ = await run_rg(args, cwd=search_dir)

    if exit_code not in (0, 1):  # 1 = no matches
        return []

    results: list[tuple[str, float]] = []
    for line in stdout.splitlines():
        line = line.strip()  # noqa: PLW2901
        if not line:
            continue
        full = Path(search_dir) / line
        try:
            mtime = full.stat().st_mtime
        except OSError:
            mtime = 0.0
        results.append((str(full), mtime))
        if len(results) > MAX_RESULTS:
            break

    return results


async def _glob_fallback(pattern: str, search_dir: str) -> list[tuple[str, float]]:
    """Pure-Python fallback using pathlib.glob.

    No .gitignore awareness, but works everywhere.
    """
    base = Path(search_dir)
    results: list[tuple[str, float]] = []

    try:
        for match in base.glob(pattern):
            if ".git" in match.parts:
                continue
            try:
                mtime = match.stat().st_mtime
            except OSError:
                mtime = 0.0
            results.append((str(match), mtime))
            if len(results) >= MAX_RESULTS * 2:
                # Collect extra for sorting, but don't walk forever.
                break
    except OSError:
        pass

    return results


# --- Tool ---------------------------------------------------------------------


@tool
async def glob(
    pattern: t.Annotated[str, "Glob pattern to match files (e.g. '**/*.py', 'src/**/*.ts')"],
    path: t.Annotated[str | None, "Directory to search in (default: working directory)"] = None,
    *,
    cwd: t.Annotated[str | None, "Working directory for relative paths"] = None,
) -> str:
    """
    Find files matching a glob pattern, sorted by modification time.

    Returns matching file paths, one per line, most recently modified
    first. Results are capped at 100 files. Use this tool when you need
    to find files by name or extension patterns.

    - Supports patterns like ``**/*.py``, ``src/**/*.ts``, ``*.json``.
    - For open-ended searches requiring multiple rounds of globbing and
      grepping, consider using a sub-agent instead.
    - Call this tool in parallel with other searches when multiple
      patterns may be useful.

    Args:
        pattern: Glob pattern (e.g. ``**/*.py``, ``src/**/*.ts``).
        path: Directory to search in. Defaults to working directory.
        cwd: Working directory for resolving relative paths.

    Returns:
        Newline-joined list of file paths, sorted by modification time.
    """
    base = Path(cwd) if cwd else Path.cwd()
    search_dir = str(base / path) if path and not Path(path).is_absolute() else (path or str(base))

    if not Path(search_dir).is_dir():
        raise FileNotFoundError(f"Directory not found: {search_dir}")

    # Try ripgrep first, fall back to pathlib.
    rg = await find_rg()
    if rg is not None:
        results = await _glob_rg(pattern, search_dir)
    else:
        results = await _glob_fallback(pattern, search_dir)

    # Sort by mtime descending (newest first).
    results.sort(key=lambda x: x[1], reverse=True)

    truncated = len(results) > MAX_RESULTS
    results = results[:MAX_RESULTS]

    if not results:
        return "No files found"

    lines = [r[0] for r in results]

    if truncated:
        lines.append("")
        lines.append(
            f"(Results truncated: showing first {MAX_RESULTS} results. "
            f"Use a more specific path or pattern.)"
        )

    return "\n".join(lines)
