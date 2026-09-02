from __future__ import annotations

import difflib
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.paths import basename, join
from matrx_ai.tools.vfs.shell.runner import CommandResult

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.core import MatrxAsyncFS


class _Flags:
    __slots__ = (
        "unified",
        "context",
        "recursive",
        "brief",
        "treat_absent_as_empty",
        "ignore_case",
        "ignore_whitespace",
        "ignore_blank_lines",
        "context_lines",
    )

    def __init__(self) -> None:
        self.unified: bool = False
        self.context: bool = False
        self.recursive: bool = False
        self.brief: bool = False
        self.treat_absent_as_empty: bool = False
        self.ignore_case: bool = False
        self.ignore_whitespace: bool = False
        self.ignore_blank_lines: bool = False
        self.context_lines: int = 3


def _parse_args(args: list[str]) -> tuple[_Flags, list[str], str | None]:
    flags = _Flags()
    paths: list[str] = []
    err: str | None = None
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        if a == "--":
            paths.extend(args[i + 1 :])
            break
        if a == "-u" or a == "--unified":
            flags.unified = True
        elif a == "-c" or a == "--context":
            flags.context = True
        elif a == "-r" or a == "--recursive":
            flags.recursive = True
        elif a == "-q" or a == "--brief":
            flags.brief = True
        elif a == "-N" or a == "--new-file":
            flags.treat_absent_as_empty = True
        elif a == "-i" or a == "--ignore-case":
            flags.ignore_case = True
        elif a == "-w" or a == "--ignore-all-space":
            flags.ignore_whitespace = True
        elif a == "-B" or a == "--ignore-blank-lines":
            flags.ignore_blank_lines = True
        elif a == "--color" or a.startswith("--color="):
            pass
        elif a.startswith("-U"):
            try:
                flags.unified = True
                flags.context_lines = int(a[2:]) if len(a) > 2 else 3
            except ValueError:
                err = f"diff: invalid context length '{a[2:]}'\n"
                break
        elif a.startswith("--unified="):
            try:
                flags.unified = True
                flags.context_lines = int(a.split("=", 1)[1])
            except ValueError:
                err = f"diff: invalid context length '{a}'\n"
                break
        elif a.startswith("-") and len(a) > 1 and not a.lstrip("-").isdigit():
            if a.startswith("--"):
                err = f"diff: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "u":
                    flags.unified = True
                elif ch == "c":
                    flags.context = True
                elif ch == "r":
                    flags.recursive = True
                elif ch == "q":
                    flags.brief = True
                elif ch == "N":
                    flags.treat_absent_as_empty = True
                elif ch == "i":
                    flags.ignore_case = True
                elif ch == "w":
                    flags.ignore_whitespace = True
                elif ch == "B":
                    flags.ignore_blank_lines = True
                else:
                    err = f"diff: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


def _split_lines(data: bytes) -> list[str]:
    text = data.decode("utf-8", errors="surrogateescape")
    if not text:
        return []
    return text.splitlines(keepends=True)


def _normalize_line(line: str, flags: _Flags) -> str:
    s = line
    if flags.ignore_case:
        s = s.lower()
    if flags.ignore_whitespace:
        # Collapse all whitespace runs to nothing for comparison
        s = "".join(ch for ch in s if not ch.isspace() or ch == "\n")
    return s


def _filter_lines(
    lines: list[str], flags: _Flags
) -> tuple[list[str], list[str]]:
    """Return (kept_lines, normalized_for_compare)."""
    kept: list[str] = []
    cmp: list[str] = []
    for ln in lines:
        if flags.ignore_blank_lines:
            stripped = ln.strip()
            if stripped == "":
                continue
        kept.append(ln)
        cmp.append(_normalize_line(ln, flags))
    return kept, cmp


def _format_iso_mtime(mtime: datetime | None) -> str:
    if mtime is None:
        mtime = datetime.now(UTC)
    if mtime.tzinfo is None:
        mtime = mtime.replace(tzinfo=UTC)
    # Match GNU diff: "YYYY-MM-DD HH:MM:SS.ffffffff +0000"
    return mtime.strftime("%Y-%m-%d %H:%M:%S.%f000 +0000")


async def _read_file_or_empty(
    vfs: MatrxAsyncFS, path: str, treat_absent: bool
) -> tuple[bytes, datetime | None, bool]:
    """Returns (data, mtime, exists)."""
    if await vfs._exists(path):
        if await vfs._isdir(path):
            return b"", None, False
        info = await vfs._info(path)
        data = await vfs._cat_file(path)
        return data, info.get("mtime"), True
    if treat_absent:
        return b"", None, False
    return b"", None, False


def _ed_diff(a: list[str], b: list[str]) -> str:
    """Render an ed-style diff (default GNU diff format)."""
    out: list[str] = []
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        a_range = _ed_range(i1, i2)
        b_range = _ed_range(j1, j2)
        if tag == "replace":
            out.append(f"{a_range}c{b_range}\n")
            for line in a[i1:i2]:
                out.append("< " + _ensure_newline(line))
            out.append("---\n")
            for line in b[j1:j2]:
                out.append("> " + _ensure_newline(line))
        elif tag == "delete":
            out.append(f"{a_range}d{j1}\n")
            for line in a[i1:i2]:
                out.append("< " + _ensure_newline(line))
        elif tag == "insert":
            out.append(f"{i1}a{b_range}\n")
            for line in b[j1:j2]:
                out.append("> " + _ensure_newline(line))
    return "".join(out)


def _ed_range(lo: int, hi: int) -> str:
    if hi == lo:
        return str(lo)
    if hi == lo + 1:
        return str(lo + 1)
    return f"{lo + 1},{hi}"


def _ensure_newline(line: str) -> str:
    if line.endswith("\n"):
        return line
    return line + "\n\\ No newline at end of file\n"


async def _diff_pair(
    vfs: MatrxAsyncFS,
    a_path: str,
    b_path: str,
    a_label: str,
    b_label: str,
    flags: _Flags,
) -> tuple[bytes, int]:
    a_exists = await vfs._exists(a_path) and not await vfs._isdir(a_path)
    b_exists = await vfs._exists(b_path) and not await vfs._isdir(b_path)

    if not a_exists and not flags.treat_absent_as_empty:
        return encode(f"diff: {a_label}: No such file or directory\n"), 2
    if not b_exists and not flags.treat_absent_as_empty:
        return encode(f"diff: {b_label}: No such file or directory\n"), 2

    a_data, a_mtime, _ = await _read_file_or_empty(vfs, a_path, flags.treat_absent_as_empty)
    b_data, b_mtime, _ = await _read_file_or_empty(vfs, b_path, flags.treat_absent_as_empty)

    a_lines = _split_lines(a_data)
    b_lines = _split_lines(b_data)

    a_keep, a_cmp = _filter_lines(a_lines, flags)
    b_keep, b_cmp = _filter_lines(b_lines, flags)

    if a_cmp == b_cmp:
        return b"", 0

    if flags.brief:
        return encode(f"Files {a_label} and {b_label} differ\n"), 1

    if flags.unified:
        a_ts = _format_iso_mtime(a_mtime)
        b_ts = _format_iso_mtime(b_mtime)
        # difflib.unified_diff uses given fromfile/tofile and ndate strings
        out_lines = list(
            difflib.unified_diff(
                a_cmp,
                b_cmp,
                fromfile=a_label,
                tofile=b_label,
                fromfiledate=a_ts,
                tofiledate=b_ts,
                n=flags.context_lines,
            )
        )
        # When using normalized lines, the patch content diverges from original
        # unless the normalization is a no-op. For accurate file content we
        # rebuild using original kept lines if no normalization was applied.
        if a_cmp == a_keep and b_cmp == b_keep:
            out_lines = list(
                difflib.unified_diff(
                    a_keep,
                    b_keep,
                    fromfile=a_label,
                    tofile=b_label,
                    fromfiledate=a_ts,
                    tofiledate=b_ts,
                    n=flags.context_lines,
                )
            )
        # Ensure each line ends with \n.
        rendered = "".join(_ensure_newline(ln) for ln in out_lines)
        return encode(rendered), 1

    if flags.context:
        a_ts = _format_iso_mtime(a_mtime)
        b_ts = _format_iso_mtime(b_mtime)
        if a_cmp == a_keep and b_cmp == b_keep:
            out_lines = list(
                difflib.context_diff(
                    a_keep,
                    b_keep,
                    fromfile=a_label,
                    tofile=b_label,
                    fromfiledate=a_ts,
                    tofiledate=b_ts,
                    n=flags.context_lines,
                )
            )
        else:
            out_lines = list(
                difflib.context_diff(
                    a_cmp,
                    b_cmp,
                    fromfile=a_label,
                    tofile=b_label,
                    fromfiledate=a_ts,
                    tofiledate=b_ts,
                    n=flags.context_lines,
                )
            )
        rendered = "".join(_ensure_newline(ln) for ln in out_lines)
        return encode(rendered), 1

    # Default: ed-style.
    if a_cmp == a_keep and b_cmp == b_keep:
        rendered = _ed_diff(a_keep, b_keep)
    else:
        rendered = _ed_diff(a_cmp, b_cmp)
    return encode(rendered), 1


async def _gather_relative(
    vfs: MatrxAsyncFS, root: str
) -> tuple[set[str], dict[str, str]]:
    """Walk root (which must exist as dir) and return relative-path set and
    mapping of relative -> absolute path. Files only."""
    rels: set[str] = set()
    mapping: dict[str, str] = {}
    async for cur, _dirs, files in vfs._walk(root):
        for f in files:
            full = join(cur, f)
            rel = full[len(root):].lstrip("/")
            rels.add(rel)
            mapping[rel] = full
    return rels, mapping


async def _diff_recursive(
    vfs: MatrxAsyncFS,
    a_root: str,
    b_root: str,
    a_label: str,
    b_label: str,
    flags: _Flags,
) -> tuple[bytes, int]:
    a_rels, a_map = await _gather_relative(vfs, a_root)
    b_rels, b_map = await _gather_relative(vfs, b_root)

    out = bytearray()
    exit_code = 0

    only_a = sorted(a_rels - b_rels)
    only_b = sorted(b_rels - a_rels)
    in_both = sorted(a_rels & b_rels)

    # GNU diff -r emits "Only in" + per-pair diffs interleaved by directory.
    # We collect everything then sort by (directory, filename) for determinism.
    entries: list[tuple[str, str, bytes]] = []
    for rel in only_a:
        d = a_label.rstrip("/") + ("/" + _dir_of(rel) if _dir_of(rel) else "")
        entries.append((d, basename(rel), encode(f"Only in {d}: {basename(rel)}\n")))
    for rel in only_b:
        d = b_label.rstrip("/") + ("/" + _dir_of(rel) if _dir_of(rel) else "")
        entries.append((d, basename(rel), encode(f"Only in {d}: {basename(rel)}\n")))
    for rel in in_both:
        a_full = a_map[rel]
        b_full = b_map[rel]
        a_lab = a_label.rstrip("/") + "/" + rel
        b_lab = b_label.rstrip("/") + "/" + rel
        header = encode(f"diff {a_lab} {b_lab}\n")
        body, ec = await _diff_pair(vfs, a_full, b_full, a_lab, b_lab, flags)
        if ec == 2:
            return bytes(body), 2
        if ec == 1:
            entries.append((_dir_of(rel) or "", basename(rel), header + body))
            exit_code = max(exit_code, 1)

    entries.sort(key=lambda e: (e[0], e[1]))
    for _d, _n, payload in entries:
        out.extend(payload)
    return bytes(out), exit_code


def _dir_of(rel: str) -> str:
    if "/" in rel:
        return rel.rsplit("/", 1)[0]
    return ""


@register("diff")
async def cmd_diff(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(2, encode(err))

    if len(paths) < 2:
        return fail(2, encode("diff: missing operand\n"))
    if len(paths) > 2:
        return fail(2, encode("diff: extra operand\n"))

    a_label, b_label = paths[0], paths[1]
    a_path = resolve_cwd(ctx.env, a_label)
    b_path = resolve_cwd(ctx.env, b_label)

    a_is_dir = await ctx.vfs._isdir(a_path)
    b_is_dir = await ctx.vfs._isdir(b_path)
    a_exists = await ctx.vfs._exists(a_path)
    b_exists = await ctx.vfs._exists(b_path)

    if not a_exists and not flags.treat_absent_as_empty:
        return fail(2, encode(f"diff: {a_label}: No such file or directory\n"))
    if not b_exists and not flags.treat_absent_as_empty:
        return fail(2, encode(f"diff: {b_label}: No such file or directory\n"))

    if a_is_dir and b_is_dir:
        if flags.recursive:
            out, exit_code = await _diff_recursive(
                ctx.vfs, a_path, b_path, a_label, b_label, flags
            )
            return CommandResult(stdout=out, stderr=b"", exit_code=exit_code)
        # Compare top-level files only.
        out, exit_code = await _diff_recursive(
            ctx.vfs, a_path, b_path, a_label, b_label, flags
        )
        return CommandResult(stdout=out, stderr=b"", exit_code=exit_code)

    if a_is_dir and not b_is_dir:
        # diff DIR FILE: diff DIR/basename(FILE) FILE
        a_path = join(a_path, basename(b_path))
        a_label = a_label.rstrip("/") + "/" + basename(b_label)
    elif b_is_dir and not a_is_dir:
        b_path = join(b_path, basename(a_path))
        b_label = b_label.rstrip("/") + "/" + basename(a_label)

    body, exit_code = await _diff_pair(ctx.vfs, a_path, b_path, a_label, b_label, flags)
    if exit_code == 2:
        return fail(2, body)
    return CommandResult(stdout=body, stderr=b"", exit_code=exit_code)
