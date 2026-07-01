"""Directory listing tool — tree-style view of project structure."""

import asyncio
import os
import typing as t
from collections import defaultdict
from pathlib import Path

from dreadnode.agents.tools import tool
from dreadnode.tools._ripgrep import find_rg, run_rg

MAX_FILES = 100
"""Hard cap on collected files before truncation."""

IGNORE_PATTERNS: list[str] = [
    "node_modules/",
    "__pycache__/",
    ".git/",
    "dist/",
    "build/",
    "target/",
    "vendor/",
    "bin/",
    "obj/",
    ".idea/",
    ".vscode/",
    ".zig-cache/",
    "zig-out/",
    ".coverage",
    "coverage/",
    "tmp/",
    "temp/",
    ".cache/",
    "cache/",
    "logs/",
    ".venv/",
    "venv/",
    "env/",
]


# --- Backends ----------------------------------------------------------------


async def _ls_rg(
    search_dir: str,
    extra_ignores: list[str] | None = None,
) -> tuple[list[str], bool]:
    """Use ripgrep to list files, respecting .gitignore + ignore patterns.

    Returns (relative_paths, truncated).
    """
    args = ["--files", "--hidden", "--glob=!.git/*"]

    for pattern in IGNORE_PATTERNS:
        args.append(f"--glob=!{pattern}*")

    if extra_ignores:
        for pattern in extra_ignores:
            args.append(f"--glob=!{pattern}")

    exit_code, stdout, _ = await run_rg(args, cwd=search_dir)
    if exit_code not in (0, 1):
        return [], False

    paths: list[str] = []
    for line in stdout.splitlines():
        line = line.strip()  # noqa: PLW2901
        if not line:
            continue
        paths.append(line)
        if len(paths) > MAX_FILES:
            return paths[:MAX_FILES], True

    return paths, False


async def _ls_fallback(
    search_dir: str,
    extra_ignores: list[str] | None = None,
) -> tuple[list[str], bool]:
    """Pure-Python fallback using os.walk (runs in thread pool)."""
    return await asyncio.to_thread(_ls_fallback_sync, search_dir, extra_ignores)


def _ls_fallback_sync(
    search_dir: str,
    extra_ignores: list[str] | None = None,
) -> tuple[list[str], bool]:
    """Sync implementation of ls fallback — called via ``asyncio.to_thread``."""
    base = Path(search_dir)
    skip_dirs = {p.rstrip("/") for p in IGNORE_PATTERNS if p.endswith("/")}
    if extra_ignores:
        skip_dirs.update(p.rstrip("/") for p in extra_ignores if p.endswith("/"))

    paths: list[str] = []
    truncated = False

    for dirpath, dirnames, filenames in os.walk(base):
        # Prune ignored directories in-place.
        dirnames[:] = [
            d for d in dirnames if (d not in skip_dirs and not d.startswith(".")) or d == ".github"
        ]
        dirnames.sort()

        rel_dir = os.path.relpath(dirpath, base)

        for fname in sorted(filenames):
            if rel_dir == ".":
                paths.append(fname)
            else:
                paths.append(str(Path(rel_dir) / fname))

            if len(paths) > MAX_FILES:
                truncated = True
                break

        if truncated:
            break

    return paths[:MAX_FILES], truncated


# --- Tree rendering ----------------------------------------------------------


def _build_tree(paths: list[str]) -> str:
    """Build a tree-style string from a list of relative file paths."""
    # Collect all directories and their direct children.
    dirs: set[str] = set()
    children: dict[str, list[str]] = defaultdict(list)

    for p in paths:
        parts = Path(p).parts
        # Register all parent directories.
        for i in range(1, len(parts)):
            parent = str(Path(*parts[:i]))
            dirs.add(parent)
        # Add the file to its parent.
        parent_dir = str(Path(*parts[:-1])) if len(parts) > 1 else ""
        children[parent_dir].append(parts[-1])

    # Also register directories as children of their parents.
    for d in sorted(dirs):
        parts = Path(d).parts
        parent = str(Path(*parts[:-1])) if len(parts) > 1 else ""
        name = parts[-1] + "/"
        if name not in children[parent]:
            children[parent].append(name)

    # Render recursively.
    lines: list[str] = []

    def _render(prefix: str, depth: int) -> None:
        items = sorted(children.get(prefix, []), key=lambda x: (not x.endswith("/"), x.lower()))
        for item in items:
            indent = "  " * depth
            lines.append(f"{indent}{item}")
            if item.endswith("/"):
                child_prefix = str(Path(prefix) / item.rstrip("/")) if prefix else item.rstrip("/")
                _render(child_prefix, depth + 1)

    _render("", 0)
    return "\n".join(lines)


# --- Tool --------------------------------------------------------------------


@tool
async def ls(
    path: t.Annotated[str | None, "Directory to list (default: working directory)"] = None,
    *,
    ignore: t.Annotated[
        list[str] | None,
        "Additional glob patterns to ignore (e.g. ['*.log', 'tmp/'])",
    ] = None,
    cwd: t.Annotated[str | None, "Working directory for relative paths"] = None,
) -> str:
    """
    List files and directories in a tree-style view.

    Returns a hierarchical directory listing with 2-space indentation.
    Common directories (node_modules, __pycache__, .git, dist, build,
    .venv, etc.) are ignored by default.

    - Results are capped at 100 files. Use ``glob`` or ``grep`` if you
      know which files or patterns you are looking for.
    - You can provide additional ignore patterns to filter out files.
    - Prefer ``glob`` and ``grep`` over ``ls`` when you know the
      directory or pattern to search.

    Args:
        path: Directory to list. Defaults to working directory.
        ignore: Additional glob patterns to exclude.
        cwd: Working directory for resolving relative paths.

    Returns:
        Tree-style directory listing.
    """
    base = Path(cwd) if cwd else Path.cwd()
    search_dir = str(base / path) if path and not Path(path).is_absolute() else (path or str(base))

    if not Path(search_dir).is_dir():
        raise FileNotFoundError(f"Directory not found: {search_dir}")

    # Try ripgrep first, fall back to os.walk.
    rg = await find_rg()
    if rg is not None:
        paths, truncated = await _ls_rg(search_dir, ignore)
    else:
        paths, truncated = await _ls_fallback(search_dir, ignore)

    if not paths:
        return "Empty directory"

    tree = _build_tree(paths)

    if truncated:
        tree += (
            f"\n\n(Truncated: showing first {MAX_FILES} files. "
            f"Use glob or grep for targeted searches.)"
        )

    return tree
