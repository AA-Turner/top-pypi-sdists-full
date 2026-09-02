from __future__ import annotations

from datetime import datetime

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import (
    InodeView,
    format_stat_default,
    format_stat_format_string,
)
from matrx_ai.tools.vfs.paths import basename
from matrx_ai.tools.vfs.shell.runner import CommandResult

_DEFAULT_USER = "user"
_DEFAULT_GROUP = "user"


def _to_epoch(value: object) -> float:
    if isinstance(value, datetime):
        return value.timestamp()
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _info_to_view(info: dict, override_name: str | None = None) -> InodeView:
    raw_type = info.get("type", "file")
    if raw_type == "directory":
        itype = "dir"
    elif raw_type == "link":
        itype = "link"
    else:
        itype = "file"

    name = override_name if override_name is not None else basename(info.get("name") or "/")
    if not name:
        name = "/"
    mode = info.get("mode")
    if mode is None:
        if itype == "dir":
            mode = 0o755
        elif itype == "link":
            mode = 0o777
        else:
            mode = 0o644

    nlink = info.get("nlink")
    if nlink is None:
        nlink = 2 if itype == "dir" else 1

    return InodeView(
        name=name,
        type=itype,  # type: ignore[typeddict-item]
        mode=int(mode),
        uid=int(info.get("uid", 0) or 0),
        gid=int(info.get("gid", 0) or 0),
        user=_DEFAULT_USER,
        group=_DEFAULT_GROUP,
        size=int(info.get("size", 0) or 0),
        nlink=int(nlink),
        mtime=_to_epoch(info.get("mtime", 0.0)),
        ctime=_to_epoch(info.get("ctime", 0.0)),
        atime=_to_epoch(info.get("atime", 0.0)),
        symlink_target=info.get("symlink_target"),
    )


class _StatOpts:
    __slots__ = ("format_str", "filesystem", "dereference", "terse", "printf_str")

    def __init__(self) -> None:
        self.format_str: str | None = None
        self.printf_str: str | None = None
        self.filesystem: bool = False
        self.dereference: bool = False
        self.terse: bool = False


def _parse_args(args: list[str]) -> tuple[_StatOpts, list[str], CommandResult | None]:
    opts = _StatOpts()
    paths: list[str] = []
    i = 0
    end_of_opts = False
    while i < len(args):
        a = args[i]
        if end_of_opts:
            paths.append(a)
            i += 1
            continue
        if a == "--":
            end_of_opts = True
            i += 1
            continue
        if a.startswith("--format="):
            opts.format_str = a.split("=", 1)[1]
            i += 1
            continue
        if a == "--format":
            if i + 1 >= len(args):
                return opts, paths, fail(
                    1, encode("stat: option requires an argument -- 'format'\n")
                )
            opts.format_str = args[i + 1]
            i += 2
            continue
        if a.startswith("--printf="):
            opts.printf_str = a.split("=", 1)[1]
            i += 1
            continue
        if a == "--printf":
            if i + 1 >= len(args):
                return opts, paths, fail(
                    1, encode("stat: option requires an argument -- 'printf'\n")
                )
            opts.printf_str = args[i + 1]
            i += 2
            continue
        if a == "--file-system" or a == "-f":
            opts.filesystem = True
            i += 1
            continue
        if a == "--dereference" or a == "-L":
            opts.dereference = True
            i += 1
            continue
        if a == "--terse" or a == "-t":
            opts.terse = True
            i += 1
            continue
        if a.startswith("-c"):
            if a == "-c":
                if i + 1 >= len(args):
                    return opts, paths, fail(
                        1, encode("stat: option requires an argument -- 'c'\n")
                    )
                opts.format_str = args[i + 1]
                i += 2
                continue
            opts.format_str = a[2:]
            i += 1
            continue
        if a.startswith("-") and len(a) > 1 and a != "-":
            return opts, paths, fail(
                1,
                encode(
                    f"stat: invalid option -- '{a[1:]}'\n"
                    "Try 'stat --help' for more information.\n"
                ),
            )
        paths.append(a)
        i += 1
    return opts, paths, None


def _format_filesystem(view: InodeView, path: str) -> str:
    # Synthesized filesystem stat output — not byte-identical to real `stat -f`
    # but the structure is recognizable.
    lines = [
        f'  File: "{path}"',
        "    ID: 0        Namelen: 255     Type: matrxfs",
        "Block size: 4096       Fundamental block size: 4096",
        "Blocks: Total: 26214400   Free: 24117248   Available: 24117248",
        "Inodes: Total: 9999999    Free: 9999000",
    ]
    _ = view
    return "\n".join(lines) + "\n"


@register("stat")
async def cmd_stat(ctx: CommandContext) -> CommandResult:
    opts, paths, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not paths:
        return fail(
            1,
            encode(
                "stat: missing operand\nTry 'stat --help' for more information.\n"
            ),
        )

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    for idx, display in enumerate(paths):
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
        try:
            info = await ctx.vfs._info(abs_path)
        except FileNotFoundError:
            err_out.extend(
                encode(
                    f"stat: cannot statx '{display}': No such file or directory\n"
                )
            )
            exit_code = 1
            continue
        except OSError:
            err_out.extend(
                encode(
                    f"stat: cannot statx '{display}': No such file or directory\n"
                )
            )
            exit_code = 1
            continue

        view_name = display if display else "/"
        view = _info_to_view(info, override_name=view_name)

        if opts.filesystem:
            out.extend(encode(_format_filesystem(view, display)))
        elif opts.format_str is not None:
            text = format_stat_format_string(view, opts.format_str)
            out.extend(encode(text + "\n"))
        elif opts.printf_str is not None:
            text = format_stat_format_string(view, opts.printf_str)
            out.extend(encode(text))
        else:
            out.extend(encode(format_stat_default(view, display)))
            if idx < len(paths) - 1:
                out.extend(b"\n")

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
