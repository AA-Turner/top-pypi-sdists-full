import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Type alias for the gitignore-style predicate
_IgnoreFn = Optional[Callable[[Path], bool]]


def list_directory_entries(
    dir_path: Path,
    is_ignored_fn: _IgnoreFn = None,
) -> List[Dict[str, Any]]:
    """List the *immediate* children of *dir_path* (non-recursive).

    Entries are sorted with directories first, then files, both groups
    ordered case-insensitively by name.

    Args:
        dir_path: Absolute path to the directory to inspect.
        is_ignored_fn: Optional predicate; a child is excluded when this
            returns True for its path.

    Returns:
        List of dicts, each with keys:

        - name - basename of the entry
        - type - "file" or "dir"
        - extension - lowercase extension including the dot ("" for dirs)
        - size_bytes - file size in bytes (0 for directories)
    """
    if not dir_path.is_dir():
        return []

    try:
        children = sorted(
            dir_path.iterdir(),
            key=lambda p: (p.is_file(), p.name.lower()),
        )
    except PermissionError:
        return []

    entries: List[Dict[str, Any]] = []
    for child in children:
        if is_ignored_fn is not None and is_ignored_fn(child):
            continue

        is_dir = child.is_dir()
        try:
            size = child.stat().st_size if not is_dir else 0
        except OSError:
            size = 0

        entries.append(
            {
                "name": child.name,
                "type": "dir" if is_dir else "file",
                "extension": "" if is_dir else child.suffix.lower(),
                "size_bytes": size,
            }
        )

    return entries


def find_files_by_glob(
    root: Path,
    pattern: str,
    is_ignored_fn: _IgnoreFn = None,
    max_results: int = 200,
) -> List[str]:
    """Find *files* (not directories) matching *pattern* under *root*.

    Supports ** for recursive matching.  A bare word with no slashes,
    wildcards, or dots (e.g. "utils") is automatically expanded to
    "**/utils*" so that it finds files whose name *starts with* the
    word anywhere in the tree.

    Args:
        root: Project root directory.
        pattern: Glob pattern relative to *root*.
            Examples: "**/*.py", "src/**/*.ts", "utils".
        is_ignored_fn: Optional predicate to exclude gitignored paths.
        max_results: Hard cap on the number of results.  Stops early to
            avoid flooding the AI context window.

    Returns:
        Sorted list of POSIX path strings relative to *root*.
    """
    if not root.is_dir():
        return []

    # Expand bare words into a recursive glob so the AI doesn't need to
    # know glob syntax to find a file by partial name.
    if "/" not in pattern and "*" not in pattern and "." not in pattern:
        pattern = f"**/{pattern}*"

    results: List[str] = []
    try:
        for match in sorted(root.glob(pattern), key=lambda p: p.as_posix()):
            if len(results) >= max_results:
                break
            if not match.is_file():
                continue
            if is_ignored_fn is not None and is_ignored_fn(match):
                continue
            results.append(match.relative_to(root).as_posix())
    except (OSError, ValueError):
        pass

    return results


def grep_files(
    root: Path,
    query: str,
    file_pattern: str = "**/*",
    case_sensitive: bool = True,
    max_results: int = 100,
    is_ignored_fn: _IgnoreFn = None,
) -> List[Dict[str, Any]]:
    """Search for *query* across files that match *file_pattern* under *root*.

    *query* is compiled as a Python regex.  If it is not a valid regex it
    is automatically escaped and treated as a literal string, so plain text
    searches always work.

    Iteration stops as soon as *max_results* matching lines have been
    collected, preventing context-window overflows for queries that match
    thousands of lines.

    Per-file encoding errors are silently skipped (errors="replace"),
    so binary files do not break the search.

    Args:
        root: Project root directory.
        query: Plain text or Python regex to search for.
        file_pattern: Glob selecting which files to search.
            "**/*.py" for Python files, "**/*" for everything.
        case_sensitive: Whether matching is case-sensitive.
        max_results: Maximum number of matching lines returned across all
            files combined.
        is_ignored_fn: Optional predicate to exclude gitignored paths.

    Returns:
        List of dicts with keys:

        - file - relative POSIX path of the file containing the match
        - line_number - 1-indexed line number
        - line - the matched line (trailing newline stripped)
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        regex = re.compile(query, flags)
    except re.error:
        # Treat an invalid regex as a literal string so the caller does
        # not need to escape special characters for simple text searches.
        regex = re.compile(re.escape(query), flags)

    results: List[Dict[str, Any]] = []

    try:
        candidates = sorted(root.glob(file_pattern), key=lambda p: p.as_posix())
    except (OSError, ValueError):
        return results

    for file_path in candidates:
        if len(results) >= max_results:
            break
        if not file_path.is_file():
            continue
        if is_ignored_fn is not None and is_ignored_fn(file_path):
            continue
        try:
            with file_path.open("r", encoding="utf-8", errors="replace") as fh:
                for line_number, line in enumerate(fh, start=1):
                    if len(results) >= max_results:
                        break
                    if regex.search(line):
                        results.append(
                            {
                                "file": file_path.relative_to(root).as_posix(),
                                "line_number": line_number,
                                "line": line.rstrip("\n"),
                            }
                        )
        except OSError:
            continue

    return results
