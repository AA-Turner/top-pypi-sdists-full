"""
Content search tool — find files containing a regex pattern.

Uses ripgrep (rg) when available for speed and .gitignore awareness.
Falls back to pure-Python regex search otherwise.
"""

import json
import mimetypes
import re
import typing as t
from collections import defaultdict
from pathlib import Path

import aiofiles

from dreadnode.agents.tools import tool
from dreadnode.tools._ripgrep import find_rg, run_rg

DEFAULT_LIMIT = 100
"""Default cap on total matches/files returned."""

MAX_LIMIT = 1000
"""Hard upper bound on the configurable limit."""

MAX_LINE_LENGTH = 2000
"""Truncate individual matching lines longer than this."""

MAX_CONTEXT = 20
"""Maximum context lines per side; protects against runaway output."""

_MAX_FILE_SIZE = 5 * 1024 * 1024
"""Skip files larger than 5 MB in the Python fallback."""

_MAX_FILES_FALLBACK = 200
"""Max files to scan in the Python fallback."""

_TEXT_MIME_PREFIXES = ("text/",)
_TEXT_MIME_EXTRAS = frozenset(
    {
        "application/json",
        "application/xml",
        "application/javascript",
        "application/x-yaml",
        "application/toml",
        "application/x-sh",
        "application/x-python",
    }
)

OutputMode = t.Literal["content", "files", "count"]


def _is_text_file(filepath: Path) -> bool:
    """Heuristic check for text files."""
    mime, _ = mimetypes.guess_type(str(filepath))
    if mime is None:
        return True  # Unknown = try it.
    if any(mime.startswith(p) for p in _TEXT_MIME_PREFIXES):
        return True
    return mime in _TEXT_MIME_EXTRAS


def _resolve_target(path: str | None, cwd: str | None) -> tuple[Path, Path, Path | None]:
    """Resolve the search target into (rg_cwd, display_root, single_file).

    ``rg_cwd`` is what we pass as the subprocess working directory; it must
    be a directory. ``display_root`` is the user's requested root (used for
    walking in the Python fallback). ``single_file`` is set when the user
    pointed at a specific file, so callers can scope the search to it.
    """
    base = Path(cwd) if cwd else Path.cwd()
    if path is None:
        resolved = base
    else:
        candidate = Path(path)
        resolved = candidate if candidate.is_absolute() else base / candidate

    if not resolved.exists():
        raise FileNotFoundError(f"Path not found: {resolved}")

    if resolved.is_file():
        return resolved.parent, resolved.parent, resolved
    return resolved, resolved, None


# --- Ripgrep backend ----------------------------------------------------------


# Excluded even when the user passes an explicit ``--include`` that would
# otherwise bypass .gitignore. These are universally noise for code search.
_ALWAYS_EXCLUDE = (".git", "node_modules", ".venv", "__pycache__")


def _build_rg_args(
    *,
    pattern: str,
    output_mode: OutputMode,
    ignore_case: bool,
    literal: bool,
    context: int,
    include: str | None,
    target: str,
) -> list[str]:
    args: list[str] = ["--hidden"]

    # Bound line width at ripgrep so a single 1MB minified line can't bloat
    # our buffer. ``--max-columns-preview`` keeps a usable head of the line.
    args.extend([f"--max-columns={MAX_LINE_LENGTH}", "--max-columns-preview"])

    if ignore_case:
        args.append("--ignore-case")
    if literal:
        args.append("--fixed-strings")
    if include:
        args.extend(["--glob", include])

    # Exclusions go LAST: ripgrep's glob system is last-match-wins, so a
    # user's permissive include (e.g. ``*``) would otherwise re-include
    # ``.git``, ``node_modules``, etc.
    for excluded in _ALWAYS_EXCLUDE:
        args.extend(["--glob", f"!**/{excluded}/**"])

    if output_mode == "files":
        args.append("--files-with-matches")
    elif output_mode == "count":
        args.append("--count")
    else:
        args.append("--json")
        if context > 0:
            args.extend(["--context", str(context)])

    args.extend(["--regexp", pattern, target])
    return args


def _parse_rg_json(stdout: str) -> list[dict[str, t.Any]]:
    """Parse ripgrep --json output into match/context records.

    Each record has keys: path, line_num, line_text, kind ('match' or
    'context'). Records appear in file order, matching ripgrep's emission.
    """
    out: list[dict[str, t.Any]] = []
    for raw in stdout.splitlines():
        if not raw:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        etype = event.get("type")
        if etype not in ("match", "context"):
            continue
        data = event.get("data") or {}
        path = (data.get("path") or {}).get("text")
        line_num = data.get("line_number")
        line_text = (data.get("lines") or {}).get("text", "")
        if not path or not isinstance(line_num, int):
            continue
        out.append(
            {
                "path": path,
                "line_num": line_num,
                "line_text": line_text.rstrip("\r\n"),
                "kind": etype,
            }
        )
    return out


async def _grep_rg_content(
    *,
    pattern: str,
    rg_cwd: Path,
    target: str,
    include: str | None,
    ignore_case: bool,
    literal: bool,
    context: int,
) -> tuple[list[dict[str, t.Any]], str]:
    args = _build_rg_args(
        pattern=pattern,
        output_mode="content",
        ignore_case=ignore_case,
        literal=literal,
        context=context,
        include=include,
        target=target,
    )
    exit_code, stdout, stderr = await run_rg(args, cwd=str(rg_cwd))

    if exit_code == 1:
        return [], ""
    if exit_code not in (0, 2):
        return [], stderr.strip()

    records = _parse_rg_json(stdout)
    # Stat each unique path once; a noisy file might appear in hundreds of records.
    mtimes: dict[str, float] = {}
    for rec in records:
        path = rec["path"]
        if path not in mtimes:
            try:
                mtimes[path] = Path(path).stat().st_mtime
            except OSError:
                mtimes[path] = 0.0
        rec["mtime"] = mtimes[path]
    return records, stderr.strip() if exit_code == 2 else ""


async def _grep_rg_lines(
    *,
    pattern: str,
    rg_cwd: Path,
    target: str,
    include: str | None,
    ignore_case: bool,
    literal: bool,
    output_mode: OutputMode,
) -> tuple[str, str]:
    args = _build_rg_args(
        pattern=pattern,
        output_mode=output_mode,
        ignore_case=ignore_case,
        literal=literal,
        context=0,
        include=include,
        target=target,
    )
    exit_code, stdout, stderr = await run_rg(args, cwd=str(rg_cwd))
    if exit_code == 1:
        return "", ""
    if exit_code not in (0, 2):
        return "", stderr.strip()
    return stdout, stderr.strip() if exit_code == 2 else ""


# --- Python fallback ----------------------------------------------------------


def _normalize_fallback_glob(include: str | None) -> str:
    """Mirror ripgrep's per-segment glob semantics in ``Path.glob``.

    ``rg --glob '*.py'`` matches ``*.py`` at any depth. ``Path.glob('*.py')``
    only matches the top level. Prepend ``**/`` unless the user already
    rooted the pattern.
    """
    if not include:
        return "**/*"
    if include.startswith(("**/", "/")):
        return include
    return f"**/{include}"


def _iter_candidate_files(
    root: Path,
    *,
    include: str | None,
    single_file: Path | None,
) -> t.Iterator[Path]:
    if single_file is not None:
        yield single_file
        return
    glob_pat = _normalize_fallback_glob(include)
    excluded = set(_ALWAYS_EXCLUDE)
    count = 0
    for match in root.glob(glob_pat):
        try:
            rel_parts = match.relative_to(root).parts
        except ValueError:
            rel_parts = match.parts
        if any(part in excluded for part in rel_parts):
            continue
        if any(part.startswith(".") and part not in (".", "..") for part in rel_parts):
            # Skip hidden directories/files; rg with --hidden would search
            # them but is also gitignore-aware, which the fallback isn't.
            continue
        if not match.is_file() or not _is_text_file(match):
            continue
        try:
            if match.stat().st_size > _MAX_FILE_SIZE:
                continue
        except OSError:
            continue
        yield match
        count += 1
        if count >= _MAX_FILES_FALLBACK:
            return


async def _grep_fallback(
    *,
    pattern: str,
    root: Path,
    include: str | None,
    single_file: Path | None,
    ignore_case: bool,
    literal: bool,
    context: int,
    limit: int,
    output_mode: OutputMode,
) -> tuple[list[dict[str, t.Any]] | str, str, bool]:
    """Pure-Python regex search fallback.

    Returns ``(payload, stderr_text, capped)`` where ``payload`` is the
    records list for content mode or a preformatted string for files/count
    modes, ``stderr_text`` summarizes per-file read errors, and ``capped``
    is True when we hit the ``_MAX_FILES_FALLBACK`` ceiling.
    """
    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(re.escape(pattern) if literal else pattern, flags)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}") from e

    errors: list[str] = []
    files_seen = 0

    def _candidates() -> t.Iterator[Path]:
        nonlocal files_seen
        for f in _iter_candidate_files(root, include=include, single_file=single_file):
            files_seen += 1
            yield f

    if output_mode == "files":
        files: list[str] = []
        for filepath in _candidates():
            try:
                async with aiofiles.open(filepath, errors="replace") as f:
                    async for line in f:
                        if regex.search(line):
                            files.append(str(filepath))
                            break
            except OSError as e:
                errors.append(f"{filepath}: {e}")
            if len(files) >= limit:
                break
        return (
            "\n".join(files),
            "; ".join(errors[:5]),
            files_seen >= _MAX_FILES_FALLBACK,
        )

    if output_mode == "count":
        counts: dict[str, int] = {}
        for filepath in _candidates():
            n = 0
            try:
                async with aiofiles.open(filepath, errors="replace") as f:
                    async for line in f:
                        if regex.search(line):
                            n += 1
            except OSError as e:
                errors.append(f"{filepath}: {e}")
                continue
            if n:
                counts[str(filepath)] = n
            if len(counts) >= limit:
                break
        return (
            "\n".join(f"{path}:{count}" for path, count in counts.items()),
            "; ".join(errors[:5]),
            files_seen >= _MAX_FILES_FALLBACK,
        )

    # content mode (with optional context)
    records: list[dict[str, t.Any]] = []
    for filepath in _candidates():
        try:
            async with aiofiles.open(filepath, errors="replace") as f:
                lines = await f.readlines()
        except (OSError, UnicodeDecodeError) as e:
            errors.append(f"{filepath}: {e}")
            continue

        try:
            mtime = filepath.stat().st_mtime
        except OSError:
            mtime = 0.0

        match_indexes = [i for i, line in enumerate(lines) if regex.search(line)]
        if not match_indexes:
            continue

        if context > 0:
            wanted: set[int] = set()
            for i in match_indexes:
                for j in range(max(0, i - context), min(len(lines), i + context + 1)):
                    wanted.add(j)
            match_set = set(match_indexes)
            for j in sorted(wanted):
                records.append(
                    {
                        "path": str(filepath),
                        "line_num": j + 1,
                        "line_text": lines[j].rstrip("\r\n"),
                        "kind": "match" if j in match_set else "context",
                        "mtime": mtime,
                    }
                )
        else:
            for i in match_indexes:
                records.append(
                    {
                        "path": str(filepath),
                        "line_num": i + 1,
                        "line_text": lines[i].rstrip("\r\n"),
                        "kind": "match",
                        "mtime": mtime,
                    }
                )

        if sum(1 for r in records if r["kind"] == "match") >= limit:
            break

    return records, "; ".join(errors[:5]), files_seen >= _MAX_FILES_FALLBACK


# --- Output formatting --------------------------------------------------------


def _truncate_line(text: str) -> str:
    if len(text) > MAX_LINE_LENGTH:
        return text[:MAX_LINE_LENGTH] + "..."
    return text


def _display_path(abs_path: str, anchor: Path) -> str:
    """Render ``abs_path`` relative to ``anchor`` when it sits underneath it.

    Falls back to the absolute path for anything outside ``anchor`` — that
    way the agent can still tell the file apart and re-read it.
    """
    try:
        rel = Path(abs_path).resolve().relative_to(anchor.resolve())
    except (ValueError, OSError):
        return abs_path
    return str(rel) if str(rel) != "." else abs_path


def _append_notices(
    lines: list[str],
    *,
    stderr: str,
    fallback_capped: bool | None,
) -> None:
    if stderr:
        lines.append("")
        # Cap stderr so a misbehaving rg can't dominate the response.
        snippet = stderr if len(stderr) <= 500 else stderr[:500] + "..."
        lines.append(f"(ripgrep stderr: {snippet})")
    # Only nag when the cap actually fired — the fallback otherwise mirrors rg
    # closely enough that the agent doesn't need to care which backend ran.
    if fallback_capped:
        lines.append("")
        lines.append(
            f"(Result is partial: Python fallback scanned the first {_MAX_FILES_FALLBACK} "
            f"files only. Install ripgrep for full coverage of larger trees.)"
        )


def _format_content(
    records: list[dict[str, t.Any]],
    *,
    limit: int,
    stderr: str,
    showed_context: bool,
    anchor: Path,
    fallback_capped: bool | None = None,
) -> str:
    """Format content/context records grouped by file and sorted by mtime."""
    # Group preserving per-file order, then sort groups by mtime descending.
    by_file: dict[str, list[dict[str, t.Any]]] = defaultdict(list)
    mtimes: dict[str, float] = {}
    for rec in records:
        by_file[rec["path"]].append(rec)
        mtimes[rec["path"]] = max(mtimes.get(rec["path"], 0.0), rec.get("mtime", 0.0))

    # Trim by match count (not record count) so context lines don't squeeze matches.
    seen_matches = 0
    truncated = False
    pruned_files: list[tuple[str, list[dict[str, t.Any]]]] = []
    for filename in sorted(by_file, key=lambda p: mtimes.get(p, 0.0), reverse=True):
        recs = by_file[filename]
        kept: list[dict[str, t.Any]] = []
        for rec in recs:
            if rec["kind"] == "match":
                if seen_matches >= limit:
                    truncated = True
                    break
                seen_matches += 1
            kept.append(rec)
        if kept:
            pruned_files.append((filename, kept))
        if seen_matches >= limit and any(r["kind"] == "match" for r in recs[len(kept) :]):
            truncated = True

    total_matches = sum(1 for rec in records if rec["kind"] == "match")

    if not pruned_files:
        out: list[str] = ["No matches found"]
        _append_notices(out, stderr=stderr, fallback_capped=fallback_capped)
        return "\n".join(out)

    lines: list[str] = []
    header = f"Found {total_matches} matches"
    if truncated:
        header += f" (showing first {limit})"
    lines.append(header)

    first = True
    for filename, recs in pruned_files:
        if not first:
            lines.append("")
        first = False
        lines.append(f"{_display_path(filename, anchor)}:")
        for rec in recs:
            text = _truncate_line(rec["line_text"])
            sep = ":" if rec["kind"] == "match" or not showed_context else "-"
            lines.append(f"  Line {rec['line_num']}{sep} {text}")

    if truncated:
        lines.append("")
        lines.append(
            f"(Results truncated: showing {limit} of {total_matches} matches "
            f"({total_matches - limit} hidden). Use a narrower pattern, "
            f"path, or `include`, or raise `limit`.)"
        )

    _append_notices(lines, stderr=stderr, fallback_capped=fallback_capped)
    return "\n".join(lines)


def _format_files(
    stdout: str,
    *,
    limit: int,
    stderr: str,
    anchor: Path,
    fallback_capped: bool | None = None,
) -> str:
    files = [line for line in stdout.splitlines() if line]
    truncated = len(files) > limit
    shown = files[:limit]
    if not shown:
        out: list[str] = ["No matches found"]
        _append_notices(out, stderr=stderr, fallback_capped=fallback_capped)
        return "\n".join(out)

    lines = [f"Found {len(files)} file{'s' if len(files) != 1 else ''} with matches"]
    if truncated:
        lines[0] += f" (showing first {limit})"
    lines.extend(_display_path(f, anchor) for f in shown)
    if truncated:
        lines.append("")
        lines.append(
            f"(Results truncated: showing {limit} of {len(files)} files. "
            f"Narrow the pattern or raise `limit`.)"
        )
    _append_notices(lines, stderr=stderr, fallback_capped=fallback_capped)
    return "\n".join(lines)


def _format_counts(
    stdout: str,
    *,
    limit: int,
    stderr: str,
    anchor: Path,
    fallback_capped: bool | None = None,
) -> str:
    parsed: list[tuple[str, int]] = []
    for line in stdout.splitlines():
        if not line:
            continue
        # rg -c emits "path:count"; paths may contain ":" (Windows drive), so split right.
        path, sep, count_str = line.rpartition(":")
        if not sep:
            continue
        try:
            parsed.append((path, int(count_str)))
        except ValueError:
            continue

    parsed.sort(key=lambda x: x[1], reverse=True)
    truncated = len(parsed) > limit
    shown = parsed[:limit]
    if not shown:
        out: list[str] = ["No matches found"]
        _append_notices(out, stderr=stderr, fallback_capped=fallback_capped)
        return "\n".join(out)

    total = sum(n for _, n in parsed)
    lines = [f"Found {total} matches across {len(parsed)} file{'s' if len(parsed) != 1 else ''}"]
    if truncated:
        lines[0] += f" (showing first {limit})"
    for path, count in shown:
        lines.append(f"{_display_path(path, anchor)}: {count}")
    if truncated:
        lines.append("")
        lines.append(
            f"(Results truncated: showing {limit} of {len(parsed)} files. "
            f"Narrow the pattern or raise `limit`.)"
        )
    _append_notices(lines, stderr=stderr, fallback_capped=fallback_capped)
    return "\n".join(lines)


# --- Tool ---------------------------------------------------------------------


@tool
async def grep(
    pattern: t.Annotated[str, "Regex pattern to search for in file contents"],
    path: t.Annotated[
        str | None, "File or directory to search in (default: working directory)"
    ] = None,
    *,
    include: t.Annotated[
        str | None,
        'File glob to filter searched files (e.g. "*.py", "*.{ts,tsx}")',
    ] = None,
    ignore_case: t.Annotated[bool, "Case-insensitive search."] = False,
    literal: t.Annotated[
        bool,
        "Treat the pattern as a literal string rather than a regex.",
    ] = False,
    context: t.Annotated[
        int,
        f"Lines of context to show before and after each match (max {MAX_CONTEXT}).",
    ] = 0,
    limit: t.Annotated[
        int,
        f"Maximum results to return (default {DEFAULT_LIMIT}, max {MAX_LIMIT}).",
    ] = DEFAULT_LIMIT,
    output_mode: t.Annotated[
        OutputMode,
        '"content" returns matching lines, "files" returns matching file '
        'paths, "count" returns per-file match counts.',
    ] = "content",
    cwd: t.Annotated[str | None, "Working directory for relative paths"] = None,
) -> str:
    """
    Search file contents for a regex pattern.

    Returns matches grouped by file and sorted by modification time (newest
    first). Respects ``.gitignore`` when ripgrep is installed. Use this when
    you need to find files containing specific text or patterns.

    - Pass a directory or a single file in ``path``.
    - Matching is **case-sensitive** by default; set ``ignore_case=True``
      for case-insensitive search.
    - Supports full regex syntax by default; set ``literal=True`` for
      fixed-string search.
    - Filter by file pattern with ``include`` (e.g. ``*.py``,
      ``*.{ts,tsx}``). The glob matches at any depth — ``*.py`` finds
      ``foo.py`` and ``a/b/foo.py``. **Note:** explicit ``include`` can
      bypass ``.gitignore`` for non-vendored paths.
    - Common noise directories (``.git``, ``node_modules``, ``.venv``,
      ``__pycache__``) are always skipped.
    - Use ``context`` to surface surrounding lines around each match.
    - Use ``output_mode="files"`` to list matching files only, or
      ``output_mode="count"`` for per-file match counts.
    - Paths are rendered relative to your working directory when possible.
    - For open-ended searches requiring multiple rounds, consider using
      a sub-agent instead.

    Args:
        pattern: Regular expression to search for.
        path: Directory or file to search. Defaults to working directory.
        include: Glob pattern to filter which files are searched.
        ignore_case: Case-insensitive matching.
        literal: Treat ``pattern`` as a literal string, not a regex.
        context: Number of context lines to include on each side of a match.
        limit: Maximum matches (content mode) or files (files/count modes).
        output_mode: ``content``, ``files``, or ``count``.
        cwd: Working directory for resolving relative paths.

    Returns:
        Formatted match results.
    """
    if not pattern:
        raise ValueError("pattern is required")
    limit = max(1, min(MAX_LIMIT, int(limit)))
    context = max(0, min(MAX_CONTEXT, int(context)))
    if output_mode not in ("content", "files", "count"):
        raise ValueError(
            f"output_mode must be 'content', 'files', or 'count' (got {output_mode!r})"
        )

    rg_cwd, fallback_root, single_file = _resolve_target(path, cwd)
    target = str(single_file) if single_file is not None else str(fallback_root)
    # Render paths relative to the agent's working directory when possible —
    # the agent passed us paths in that frame and reads them back the same way.
    display_anchor = Path(cwd) if cwd else Path.cwd()

    rg = await find_rg()
    if rg is not None:
        if output_mode == "content":
            records, stderr = await _grep_rg_content(
                pattern=pattern,
                rg_cwd=rg_cwd,
                target=target,
                include=include,
                ignore_case=ignore_case,
                literal=literal,
                context=context,
            )
            return _format_content(
                records,
                limit=limit,
                stderr=stderr,
                showed_context=context > 0,
                anchor=display_anchor,
            )

        stdout, stderr = await _grep_rg_lines(
            pattern=pattern,
            rg_cwd=rg_cwd,
            target=target,
            include=include,
            ignore_case=ignore_case,
            literal=literal,
            output_mode=output_mode,
        )
        if output_mode == "files":
            return _format_files(stdout, limit=limit, stderr=stderr, anchor=display_anchor)
        return _format_counts(stdout, limit=limit, stderr=stderr, anchor=display_anchor)

    result, fallback_stderr, fallback_capped = await _grep_fallback(
        pattern=pattern,
        root=fallback_root,
        include=include,
        single_file=single_file,
        ignore_case=ignore_case,
        literal=literal,
        context=context,
        limit=limit,
        output_mode=output_mode,
    )
    if output_mode == "content":
        return _format_content(
            t.cast("list[dict[str, t.Any]]", result),
            limit=limit,
            stderr=fallback_stderr,
            showed_context=context > 0,
            anchor=display_anchor,
            fallback_capped=fallback_capped,
        )
    if output_mode == "files":
        return _format_files(
            t.cast("str", result),
            limit=limit,
            stderr=fallback_stderr,
            anchor=display_anchor,
            fallback_capped=fallback_capped,
        )
    return _format_counts(
        t.cast("str", result),
        limit=limit,
        stderr=fallback_stderr,
        anchor=display_anchor,
        fallback_capped=fallback_capped,
    )
