from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.paths import dirname, join, normalize, split_components
from matrx_ai.tools.vfs.shell.runner import CommandResult

_MAX_SYMLINK_DEPTH = 40


class _RpOpts:
    __slots__ = ("missing_ok", "must_exist", "no_symlinks", "quiet", "zero")

    def __init__(self) -> None:
        # Default GNU realpath: all components except the last must exist.
        self.missing_ok: bool = False  # -m
        self.must_exist: bool = False  # -e
        self.no_symlinks: bool = False  # -s
        self.quiet: bool = False  # -q
        self.zero: bool = False  # -z


def _parse_args(args: list[str]) -> tuple[_RpOpts, list[str], CommandResult | None]:
    opts = _RpOpts()
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
            if a == "--canonicalize-missing":
                opts.missing_ok = True
            elif a == "--canonicalize-existing":
                opts.must_exist = True
            elif a == "--no-symlinks" or a == "--strip" or a == "--logical":
                opts.no_symlinks = True
            elif a == "--quiet":
                opts.quiet = True
            elif a == "--zero":
                opts.zero = True
            else:
                paths.append(a)
            continue
        if a.startswith("-") and len(a) > 1:
            for ch in a[1:]:
                if ch == "m":
                    opts.missing_ok = True
                elif ch == "e":
                    opts.must_exist = True
                elif ch == "s" or ch == "L":
                    opts.no_symlinks = True
                elif ch == "P":
                    opts.no_symlinks = False
                elif ch == "q":
                    opts.quiet = True
                elif ch == "z":
                    opts.zero = True
            continue
        paths.append(a)
    return opts, paths, None


async def _resolve_components(
    ctx_vfs, path: str, *, follow_symlinks: bool, must_exist: bool, missing_ok: bool
) -> tuple[str | None, str | None]:
    # Returns (resolved_path, error_message). If path can't be resolved per
    # the policy, error_message is set; resolved_path may still be returned
    # for missing_ok policies.
    norm = normalize(path)
    components = split_components(norm)
    current = "/"
    depth = 0

    i = 0
    while i < len(components):
        comp = components[i]
        candidate = join(current, comp)
        try:
            info = await ctx_vfs._info(candidate)
        except FileNotFoundError:
            if must_exist:
                return None, f"realpath: {path}: No such file or directory"
            if missing_ok:
                # Append remaining components verbatim and return.
                tail = "/".join(components[i:])
                return normalize(join(current, tail)), None
            # Default: only the last component may be missing.
            if i == len(components) - 1:
                current = candidate
                i += 1
                continue
            return None, f"realpath: {path}: No such file or directory"
        except OSError:
            return None, f"realpath: {path}: No such file or directory"

        if follow_symlinks and info.get("type") == "link":
            depth += 1
            if depth > _MAX_SYMLINK_DEPTH:
                return None, f"realpath: {path}: Too many levels of symbolic links"
            target = info.get("symlink_target") or ""
            if target.startswith("/"):
                # absolute target replaces the candidate base — restart from root
                current = "/"
                target_components = split_components(target)
                # remaining components after the link itself:
                remaining = components[i + 1 :]
                components = target_components + list(remaining)
                i = 0
                continue
            # relative target: resolve relative to dirname(candidate)
            base_dir = dirname(candidate)
            target_components = split_components(target)
            remaining = components[i + 1 :]
            current = "/"
            components = split_components(base_dir) + target_components + list(remaining)
            i = 0
            continue
        else:
            current = candidate
            i += 1

    return normalize(current), None


@register("realpath")
async def cmd_realpath(ctx: CommandContext) -> CommandResult:
    opts, paths, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not paths:
        return CommandResult(
            stdout=b"",
            stderr=encode(
                "realpath: missing operand\nTry 'realpath --help' for more information.\n"
            ),
            exit_code=1,
        )

    out = bytearray()
    err_out = bytearray()
    exit_code = 0
    sep = b"\x00" if opts.zero else b"\n"

    for display in paths:
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
        resolved, problem = await _resolve_components(
            ctx.vfs,
            abs_path,
            follow_symlinks=not opts.no_symlinks,
            must_exist=opts.must_exist,
            missing_ok=opts.missing_ok,
        )
        if problem is not None:
            if not opts.quiet:
                err_out.extend(encode(problem + "\n"))
            exit_code = 1
            continue
        if resolved is None:
            exit_code = 1
            continue
        out.extend(encode(resolved))
        out.extend(sep)

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
