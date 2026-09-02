from __future__ import annotations

import gzip as gzip_mod
import io

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


class _Flags:
    __slots__ = ("decompress", "keep", "stdout", "force", "test", "verbose", "level")

    def __init__(self) -> None:
        self.decompress: bool = False
        self.keep: bool = False
        self.stdout: bool = False
        self.force: bool = False
        self.test: bool = False
        self.verbose: bool = False
        self.level: int = 6


def _parse_args(args: list[str]) -> tuple[_Flags, list[str], str | None]:
    flags = _Flags()
    files: list[str] = []
    err: str | None = None
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        if a == "--":
            files.extend(args[i + 1 :])
            break
        if a == "-d" or a == "--decompress" or a == "--uncompress":
            flags.decompress = True
        elif a == "-k" or a == "--keep":
            flags.keep = True
        elif a == "-c" or a == "--stdout" or a == "--to-stdout":
            flags.stdout = True
        elif a == "-f" or a == "--force":
            flags.force = True
        elif a == "-t" or a == "--test":
            flags.test = True
            flags.decompress = True
        elif a == "-v" or a == "--verbose":
            flags.verbose = True
        elif a == "-n" or a == "--no-name":
            pass
        elif a == "-N" or a == "--name":
            pass
        elif a.startswith("-") and len(a) > 1 and a[1].isdigit():
            try:
                flags.level = int(a[1:])
            except ValueError:
                err = f"gzip: invalid compression level '{a}'\n"
                break
        elif a.startswith("--"):
            err = f"gzip: unrecognized option '{a}'\n"
            break
        elif a.startswith("-") and len(a) > 1:
            for ch in a[1:]:
                if ch == "d":
                    flags.decompress = True
                elif ch == "k":
                    flags.keep = True
                elif ch == "c":
                    flags.stdout = True
                elif ch == "f":
                    flags.force = True
                elif ch == "t":
                    flags.test = True
                    flags.decompress = True
                elif ch == "v":
                    flags.verbose = True
                elif ch == "n":
                    pass
                elif ch == "N":
                    pass
                else:
                    err = f"gzip: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            files.append(a)
        i += 1
    return flags, files, err


def _gz_compress(data: bytes, level: int) -> bytes:
    buf = io.BytesIO()
    # mtime=0 for byte-stable output (matches gzip --no-name behavior).
    with gzip_mod.GzipFile(fileobj=buf, mode="wb", compresslevel=level, mtime=0) as gz:
        gz.write(data)
    return buf.getvalue()


def _gz_decompress(data: bytes) -> tuple[bytes | None, str | None]:
    try:
        with gzip_mod.GzipFile(fileobj=io.BytesIO(data), mode="rb") as gz:
            return gz.read(), None
    except (OSError, gzip_mod.BadGzipFile, EOFError) as e:
        return None, str(e)


async def _compress_file(
    ctx: CommandContext, flags: _Flags, path_label: str
) -> tuple[bytes, bytes, int]:
    src = resolve_cwd(ctx.env, path_label)
    if not await ctx.vfs._exists(src):
        return b"", encode(f"gzip: {path_label}: No such file or directory\n"), 1
    if await ctx.vfs._isdir(src):
        if not flags.force:
            return (
                b"",
                encode(f"gzip: {path_label} is a directory -- ignored\n"),
                1,
            )
        return b"", b"", 0
    data = await ctx.vfs._cat_file(src)
    compressed = _gz_compress(data, flags.level)

    if flags.stdout:
        return compressed, b"", 0

    dst_label = path_label + ".gz"
    dst = src + ".gz"
    if await ctx.vfs._exists(dst) and not flags.force:
        return (
            b"",
            encode(
                f"gzip: {dst_label} already exists; "
                "do you wish to overwrite (y or n)? not overwriting\n"
            ),
            2,
        )
    await ctx.vfs._pipe_file(dst, compressed)
    if not flags.keep:
        await ctx.vfs._rm(src)
    return b"", b"", 0


async def _decompress_file(
    ctx: CommandContext, flags: _Flags, path_label: str
) -> tuple[bytes, bytes, int]:
    src = resolve_cwd(ctx.env, path_label)
    if not await ctx.vfs._exists(src):
        cmd = "gunzip" if flags.test else "gzip"
        return b"", encode(f"{cmd}: {path_label}: No such file or directory\n"), 1
    if await ctx.vfs._isdir(src):
        return b"", encode(f"gzip: {path_label} is a directory\n"), 1

    data = await ctx.vfs._cat_file(src)
    decompressed, dec_err = _gz_decompress(data)
    if decompressed is None:
        cmd = "gunzip" if flags.test else "gzip"
        _ = dec_err
        return b"", encode(f"{cmd}: {path_label}: not in gzip format\n"), 1

    if flags.test:
        return b"", b"", 0

    if flags.stdout:
        return decompressed, b"", 0

    if path_label.endswith(".gz"):
        dst_label = path_label[:-3]
    elif path_label.endswith(".tgz"):
        dst_label = path_label[:-4] + ".tar"
    else:
        return (
            b"",
            encode(f"gzip: {path_label}: unknown suffix -- ignored\n"),
            1,
        )

    if src.endswith(".gz"):
        dst = src[:-3]
    elif src.endswith(".tgz"):
        dst = src[:-4] + ".tar"
    else:
        return (
            b"",
            encode(f"gzip: {path_label}: unknown suffix -- ignored\n"),
            1,
        )

    if await ctx.vfs._exists(dst) and not flags.force:
        return (
            b"",
            encode(
                f"gzip: {dst_label} already exists; "
                "do you wish to overwrite (y or n)? not overwriting\n"
            ),
            2,
        )
    await ctx.vfs._pipe_file(dst, decompressed)
    if not flags.keep:
        await ctx.vfs._rm(src)
    return b"", b"", 0


async def _run(ctx: CommandContext, decompress_default: bool) -> CommandResult:
    flags, files, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    if decompress_default:
        flags.decompress = True

    if not files:
        # Operate on stdin -> stdout
        if flags.decompress:
            decompressed, dec_err = _gz_decompress(ctx.stdin)
            if decompressed is None:
                cmd = "gunzip" if decompress_default else "gzip"
                return fail(1, encode(f"{cmd}: stdin: not in gzip format\n"))
            return ok(decompressed)
        compressed = _gz_compress(ctx.stdin, flags.level)
        return ok(compressed)

    out = bytearray()
    err_out = bytearray()
    exit_code = 0
    for f in files:
        if flags.decompress:
            so, se, ec = await _decompress_file(ctx, flags, f)
        else:
            so, se, ec = await _compress_file(ctx, flags, f)
        out.extend(so)
        err_out.extend(se)
        if ec != 0:
            exit_code = max(exit_code, ec)

    if exit_code != 0:
        return fail(exit_code, stdout=bytes(out), stderr=bytes(err_out))
    return ok(stdout=bytes(out), stderr=bytes(err_out))


@register("gzip")
async def cmd_gzip(ctx: CommandContext) -> CommandResult:
    return await _run(ctx, decompress_default=False)


@register("gunzip")
async def cmd_gunzip(ctx: CommandContext) -> CommandResult:
    return await _run(ctx, decompress_default=True)
