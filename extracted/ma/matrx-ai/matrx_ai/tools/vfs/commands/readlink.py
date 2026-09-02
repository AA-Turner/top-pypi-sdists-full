from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, resolve_cwd
from matrx_ai.tools.vfs.commands.realpath import _resolve_components
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


class _RlOpts:
    __slots__ = ("canonicalize", "must_exist", "missing_ok", "quiet", "verbose", "zero")

    def __init__(self) -> None:
        self.canonicalize: bool = False  # -f
        self.must_exist: bool = False  # -e
        self.missing_ok: bool = False  # -m
        self.quiet: bool = False  # -q (default in GNU)
        self.verbose: bool = False  # -v
        self.zero: bool = False  # -z


def _parse_args(args: list[str]) -> tuple[_RlOpts, list[str], CommandResult | None]:
    opts = _RlOpts()
    paths: list[str] = []
    end_of_opts = False
    for a in args:
        if end_of_opts:
            paths.append(a)
            continue
        if a == "--":
            end_of_opts = True
            continue
        if a.startswith("--"):
            if a == "--canonicalize":
                opts.canonicalize = True
            elif a == "--canonicalize-existing":
                opts.must_exist = True
                opts.canonicalize = True
            elif a == "--canonicalize-missing":
                opts.missing_ok = True
                opts.canonicalize = True
            elif a == "--no-newline":
                pass
            elif a == "--quiet" or a == "--silent":
                opts.quiet = True
            elif a == "--verbose":
                opts.verbose = True
            elif a == "--zero":
                opts.zero = True
            else:
                paths.append(a)
            continue
        if a.startswith("-") and len(a) > 1:
            for ch in a[1:]:
                if ch == "f":
                    opts.canonicalize = True
                elif ch == "e":
                    opts.must_exist = True
                    opts.canonicalize = True
                elif ch == "m":
                    opts.missing_ok = True
                    opts.canonicalize = True
                elif ch == "n":
                    pass
                elif ch == "q" or ch == "s":
                    opts.quiet = True
                elif ch == "v":
                    opts.verbose = True
                elif ch == "z":
                    opts.zero = True
            continue
        paths.append(a)
    return opts, paths, None


@register("readlink")
async def cmd_readlink(ctx: CommandContext) -> CommandResult:
    opts, paths, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not paths:
        return CommandResult(
            stdout=b"",
            stderr=encode(
                "readlink: missing operand\nTry 'readlink --help' for more information.\n"
            ),
            exit_code=1,
        )

    out = bytearray()
    err_out = bytearray()
    exit_code = 0
    sep = b"\x00" if opts.zero else b"\n"

    for display in paths:
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)

        if opts.canonicalize:
            resolved, problem = await _resolve_components(
                ctx.vfs,
                abs_path,
                follow_symlinks=True,
                must_exist=opts.must_exist,
                missing_ok=opts.missing_ok,
            )
            if problem is not None or resolved is None:
                if not opts.quiet and problem is not None:
                    err_out.extend(encode(f"readlink: {display}: No such file or directory\n"))
                exit_code = 1
                continue
            if opts.verbose:
                pass
            out.extend(encode(resolved))
            out.extend(sep)
            continue

        # Non-canonicalize: just print the symlink target string.
        try:
            info = await ctx.vfs._info(abs_path)
        except FileNotFoundError:
            exit_code = 1
            if opts.verbose:
                err_out.extend(
                    encode(f"readlink: {display}: No such file or directory\n")
                )
            continue
        except OSError:
            exit_code = 1
            continue

        if info.get("type") != "link":
            exit_code = 1
            if opts.verbose:
                err_out.extend(encode(f"readlink: {display}: Invalid argument\n"))
            continue
        target = info.get("symlink_target") or ""
        out.extend(encode(target))
        out.extend(sep)

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
