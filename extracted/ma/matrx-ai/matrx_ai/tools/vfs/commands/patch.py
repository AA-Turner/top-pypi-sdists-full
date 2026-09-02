from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.paths import join, normalize
from matrx_ai.tools.vfs.shell.runner import CommandResult

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.core import MatrxAsyncFS


@dataclass(slots=True)
class _Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[str] = field(default_factory=list)


@dataclass(slots=True)
class _FilePatch:
    old_name: str
    new_name: str
    hunks: list[_Hunk] = field(default_factory=list)


class _Flags:
    __slots__ = ("strip", "reverse", "input_file", "directory")

    def __init__(self) -> None:
        self.strip: int = 0
        self.reverse: bool = False
        self.input_file: str | None = None
        self.directory: str | None = None


def _parse_args(args: list[str]) -> tuple[_Flags, list[str], str | None]:
    flags = _Flags()
    extras: list[str] = []
    err: str | None = None
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        if a == "--":
            extras.extend(args[i + 1 :])
            break
        if a == "-R" or a == "--reverse":
            flags.reverse = True
        elif a == "-i" or a == "--input":
            if i + 1 >= n:
                err = "patch: option requires an argument -- 'i'\n"
                break
            flags.input_file = args[i + 1]
            i += 1
        elif a.startswith("--input="):
            flags.input_file = a.split("=", 1)[1]
        elif a == "-d" or a == "--directory":
            if i + 1 >= n:
                err = "patch: option requires an argument -- 'd'\n"
                break
            flags.directory = args[i + 1]
            i += 1
        elif a.startswith("--directory="):
            flags.directory = a.split("=", 1)[1]
        elif a == "-p":
            if i + 1 >= n:
                err = "patch: option requires an argument -- 'p'\n"
                break
            try:
                flags.strip = int(args[i + 1])
            except ValueError:
                err = f"patch: invalid strip count '{args[i + 1]}'\n"
                break
            i += 1
        elif a.startswith("-p"):
            try:
                flags.strip = int(a[2:])
            except ValueError:
                err = f"patch: invalid strip count '{a[2:]}'\n"
                break
        elif a.startswith("--strip="):
            try:
                flags.strip = int(a.split("=", 1)[1])
            except ValueError:
                err = f"patch: invalid strip count '{a}'\n"
                break
        elif a.startswith("-") and len(a) > 1:
            err = f"patch: unrecognized option '{a}'\n"
            break
        else:
            extras.append(a)
        i += 1
    return flags, extras, err


_HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _parse_unified(text: str) -> tuple[list[_FilePatch], str | None]:
    lines = text.splitlines(keepends=False)
    patches: list[_FilePatch] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("--- "):
            if i + 1 >= n or not lines[i + 1].startswith("+++ "):
                return patches, f"malformed patch at line {i + 1}"
            old_field = line[4:].split("\t", 1)[0]
            new_field = lines[i + 1][4:].split("\t", 1)[0]
            i += 2
            fp = _FilePatch(old_name=old_field, new_name=new_field)
            # Parse hunks.
            while i < n and lines[i].startswith("@@"):
                m = _HUNK_RE.match(lines[i])
                if not m:
                    return patches, f"malformed hunk header at line {i + 1}"
                old_start = int(m.group(1))
                old_count = int(m.group(2)) if m.group(2) else 1
                new_start = int(m.group(3))
                new_count = int(m.group(4)) if m.group(4) else 1
                i += 1
                hunk_lines: list[str] = []
                old_seen = 0
                new_seen = 0
                while i < n and (old_seen < old_count or new_seen < new_count):
                    hl = lines[i]
                    if not hl:
                        # Blank line in hunk = empty context line.
                        hunk_lines.append(" ")
                        old_seen += 1
                        new_seen += 1
                        i += 1
                        continue
                    tag = hl[0]
                    if tag == " ":
                        hunk_lines.append(hl)
                        old_seen += 1
                        new_seen += 1
                    elif tag == "-":
                        hunk_lines.append(hl)
                        old_seen += 1
                    elif tag == "+":
                        hunk_lines.append(hl)
                        new_seen += 1
                    elif tag == "\\":
                        # "\ No newline at end of file" — pass through.
                        hunk_lines.append(hl)
                    else:
                        # End of hunk on unknown prefix.
                        break
                    i += 1
                fp.hunks.append(
                    _Hunk(
                        old_start=old_start,
                        old_count=old_count,
                        new_start=new_start,
                        new_count=new_count,
                        lines=hunk_lines,
                    )
                )
            patches.append(fp)
        else:
            i += 1
    if not patches:
        return patches, "malformed patch: no file headers found"
    return patches, None


def _strip_path(path: str, n: int) -> str:
    if path == "/dev/null":
        return path
    parts = path.split("/")
    if n >= len(parts):
        return parts[-1]
    return "/".join(parts[n:])


def _reverse_hunk(hunk: _Hunk) -> _Hunk:
    new_lines: list[str] = []
    for ln in hunk.lines:
        if not ln:
            new_lines.append(" ")
            continue
        if ln[0] == "-":
            new_lines.append("+" + ln[1:])
        elif ln[0] == "+":
            new_lines.append("-" + ln[1:])
        else:
            new_lines.append(ln)
    return _Hunk(
        old_start=hunk.new_start,
        old_count=hunk.new_count,
        new_start=hunk.old_start,
        new_count=hunk.old_count,
        lines=new_lines,
    )


def _apply_hunk(
    src_lines: list[str], hunk: _Hunk
) -> tuple[list[str] | None, int]:
    """Return (new_lines, lines_consumed) or (None, _) on failure."""
    old_block: list[str] = []
    new_block: list[str] = []
    for hl in hunk.lines:
        if not hl or hl.startswith("\\"):
            continue
        tag = hl[0]
        rest = hl[1:]
        if tag == " ":
            old_block.append(rest)
            new_block.append(rest)
        elif tag == "-":
            old_block.append(rest)
        elif tag == "+":
            new_block.append(rest)

    start = hunk.old_start - 1
    if start < 0:
        start = 0
    end = start + len(old_block)
    actual = src_lines[start:end]
    if actual != old_block:
        return None, hunk.old_start

    new_src = src_lines[:start] + new_block + src_lines[end:]
    return new_src, hunk.old_start


async def _resolve_target(
    vfs: MatrxAsyncFS,
    fp: _FilePatch,
    flags: _Flags,
    base_dir: str,
) -> str:
    name = fp.new_name if fp.new_name != "/dev/null" else fp.old_name
    if name == "/dev/null":
        name = fp.old_name
    stripped = _strip_path(name, flags.strip)
    if stripped.startswith("/"):
        return normalize(stripped)
    return normalize(join(base_dir, stripped))


@register("patch")
async def cmd_patch(ctx: CommandContext) -> CommandResult:
    flags, extras, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    # Get patch text.
    if flags.input_file is not None:
        in_path = resolve_cwd(ctx.env, flags.input_file)
        if not await ctx.vfs._exists(in_path):
            return fail(1, encode(f"patch: **** Can't open patch file {flags.input_file}\n"))
        patch_bytes = await ctx.vfs._cat_file(in_path)
    else:
        patch_bytes = ctx.stdin

    if not patch_bytes:
        return fail(1, encode("patch: **** Only garbage was found in the patch input.\n"))

    patch_text = patch_bytes.decode("utf-8", errors="surrogateescape")
    patches, parse_err = _parse_unified(patch_text)
    if parse_err is not None:
        return fail(1, encode(f"patch: **** {parse_err}\n"))

    base_dir = ctx.env.cwd
    if flags.directory is not None:
        base_dir = resolve_cwd(ctx.env, flags.directory)

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    for fp in patches:
        target = await _resolve_target(ctx.vfs, fp, flags, base_dir)
        # Resolve a friendly label (relative to cwd if possible).
        label = _strip_path(
            fp.new_name if fp.new_name != "/dev/null" else fp.old_name,
            flags.strip,
        )
        out.extend(encode(f"patching file {label}\n"))

        if await ctx.vfs._exists(target):
            data = await ctx.vfs._cat_file(target)
        else:
            data = b""
        text = data.decode("utf-8", errors="surrogateescape")
        src_lines = text.splitlines(keepends=False)
        # Track presence of trailing newline.
        had_trailing_nl = text.endswith("\n")

        hunks = fp.hunks
        if flags.reverse:
            hunks = [_reverse_hunk(h) for h in hunks]

        new_lines = src_lines
        # Apply hunks in order, adjusting for prior offsets is not needed because
        # hunks are independent in the original file space; we rebuild progressively.
        # We apply each hunk against the current new_lines, treating old_start as
        # the line number in the *evolving* file. GNU patch tolerates fuzz; we don't.
        offset = 0
        for idx, h in enumerate(hunks, 1):
            adjusted = _Hunk(
                old_start=h.old_start + offset,
                old_count=h.old_count,
                new_start=h.new_start,
                new_count=h.new_count,
                lines=h.lines,
            )
            result, _ = _apply_hunk(new_lines, adjusted)
            if result is None:
                err_out.extend(encode(f"Hunk #{idx} FAILED at {h.old_start}.\n"))
                exit_code = max(exit_code, 1)
                # Skip remaining hunks on this file (matches GNU patch with no fuzz).
                new_lines = None  # type: ignore[assignment]
                break
            # Compute offset delta: new_count - old_count.
            offset += h.new_count - h.old_count
            new_lines = result

        if new_lines is None:
            continue

        # Reassemble file content.
        result_text = "\n".join(new_lines)
        # If original had trailing newline (or had no content but new file does),
        # add one. Look at last hunk to decide.
        if new_lines:
            last_hunk_lines = hunks[-1].lines if hunks else []
            no_newline_at_end = any(
                ln.startswith("\\ No newline at end of file") for ln in last_hunk_lines[-2:]
            )
            if not no_newline_at_end:
                result_text += "\n"
        elif had_trailing_nl:
            result_text = ""

        await ctx.vfs._pipe_file(
            target, result_text.encode("utf-8", errors="surrogateescape")
        )

    if exit_code != 0:
        return fail(exit_code, stdout=bytes(out), stderr=bytes(err_out))
    return ok(stdout=bytes(out), stderr=bytes(err_out))
