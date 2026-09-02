from __future__ import annotations

import io
import zipfile
from datetime import datetime

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.paths import dirname, join, normalize
from matrx_ai.tools.vfs.shell.runner import CommandResult


class _Flags:
    __slots__ = ("list", "extract_dir", "overwrite", "no_overwrite", "quiet")

    def __init__(self) -> None:
        self.list: bool = False
        self.extract_dir: str | None = None
        self.overwrite: bool = False
        self.no_overwrite: bool = False
        self.quiet: bool = False


def _parse_args(args: list[str]) -> tuple[_Flags, list[str], str | None]:
    flags = _Flags()
    positional: list[str] = []
    err: str | None = None
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        if a == "--":
            positional.extend(args[i + 1 :])
            break
        if a == "-l":
            flags.list = True
        elif a == "-d":
            if i + 1 >= n:
                err = "unzip: option requires an argument -- 'd'\n"
                break
            flags.extract_dir = args[i + 1]
            i += 1
        elif a == "-o":
            flags.overwrite = True
        elif a == "-n":
            flags.no_overwrite = True
        elif a == "-q":
            flags.quiet = True
        elif a.startswith("-") and len(a) > 1:
            for ch in a[1:]:
                if ch == "l":
                    flags.list = True
                elif ch == "o":
                    flags.overwrite = True
                elif ch == "n":
                    flags.no_overwrite = True
                elif ch == "q":
                    flags.quiet = True
                else:
                    err = f"unzip: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            positional.append(a)
        i += 1
    return flags, positional, err


def _format_list(zf: zipfile.ZipFile) -> bytes:
    out: list[str] = []
    out.append("  Length      Date    Time    Name")
    out.append("---------  ---------- -----   ----")
    total_size = 0
    total_count = 0
    for info in zf.infolist():
        size = info.file_size
        try:
            dt = datetime(*info.date_time)
            date_str = dt.strftime("%Y-%m-%d")
            time_str = dt.strftime("%H:%M")
        except (ValueError, TypeError):
            date_str = "1980-00-00"
            time_str = "00:00"
        out.append(f"{size:>9d}  {date_str} {time_str}   {info.filename}")
        total_size += size
        total_count += 1
    out.append("---------                     -------")
    out.append(f"{total_size:>9d}                     {total_count} file{'s' if total_count != 1 else ''}")
    return ("\n".join(out) + "\n").encode("utf-8")


@register("unzip")
async def cmd_unzip(ctx: CommandContext) -> CommandResult:
    flags, positional, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    if not positional:
        return fail(
            9,
            encode("unzip:  cannot find or open , , or .zip.\n"),
        )

    zip_label = positional[0]
    zip_path = resolve_cwd(ctx.env, zip_label)

    if not await ctx.vfs._exists(zip_path):
        return fail(
            9,
            encode(f"unzip:  cannot find or open {zip_label}\n"),
        )
    if await ctx.vfs._isdir(zip_path):
        return fail(9, encode(f"unzip:  cannot find or open {zip_label}\n"))

    archive = await ctx.vfs._cat_file(zip_path)
    try:
        zf = zipfile.ZipFile(io.BytesIO(archive), "r")
    except zipfile.BadZipFile:
        return fail(
            9,
            encode(
                f"  End-of-central-directory signature not found.  "
                f"Either this file is not\n"
                f"  a zipfile, or it constitutes one disk of a multi-part archive.\n"
                f"  In the latter case the central directory and zipfile comment "
                f"will be\n"
                f"  found on the last disk(s) of this set.\n"
                f"unzip:  cannot find zipfile directory in one of {zip_label} or\n"
                f"        {zip_label}.zip, and cannot find {zip_label}.ZIP, period.\n"
            ),
        )

    if flags.list:
        out = b""
        if not flags.quiet:
            out += encode(f"Archive:  {zip_label}\n")
        out += _format_list(zf)
        return ok(stdout=out)

    base = ctx.env.cwd
    if flags.extract_dir is not None:
        base = resolve_cwd(ctx.env, flags.extract_dir)
        if not await ctx.vfs._exists(base):
            await ctx.vfs._makedirs(base, exist_ok=True)

    out = bytearray()
    if not flags.quiet:
        out.extend(encode(f"Archive:  {zip_label}\n"))

    with zf:
        for info in zf.infolist():
            target = normalize(join(base, info.filename))
            if info.is_dir():
                if not await ctx.vfs._exists(target):
                    await ctx.vfs._makedirs(target, exist_ok=True)
                if not flags.quiet:
                    out.extend(encode(f"   creating: {info.filename}\n"))
                continue
            parent = dirname(target)
            if parent and parent != "/" and not await ctx.vfs._exists(parent):
                await ctx.vfs._makedirs(parent, exist_ok=True)

            if await ctx.vfs._exists(target):
                if flags.no_overwrite:
                    if not flags.quiet:
                        out.extend(encode(f"  skipping: {info.filename}\n"))
                    continue
                if not flags.overwrite:
                    # Default: replace (we don't prompt — behave like -o for sanity).
                    pass

            data = zf.read(info.filename)
            await ctx.vfs._pipe_file(target, data)
            if not flags.quiet:
                out.extend(encode(f"  inflating: {info.filename}\n"))

    return ok(stdout=bytes(out))
