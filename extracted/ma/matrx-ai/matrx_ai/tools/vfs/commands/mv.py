from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import from_oserror, mv_no_src
from matrx_ai.tools.vfs.paths import basename, join
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_args(args: list[str]) -> tuple[dict[str, object], list[str], str | None]:
    flags: dict[str, object] = {
        "force": False,
        "no_clobber": False,
        "verbose": False,
        "no_target_dir": False,
        "target_dir": None,
    }
    paths: list[str] = []
    err: str | None = None
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        if a == "--":
            paths.extend(args[i + 1 :])
            break
        if a == "-f" or a == "--force":
            flags["force"] = True
        elif a == "-n" or a == "--no-clobber":
            flags["no_clobber"] = True
        elif a == "-v" or a == "--verbose":
            flags["verbose"] = True
        elif a == "-i":
            pass  # refuse to mimic interactive
        elif a == "-T" or a == "--no-target-directory":
            flags["no_target_dir"] = True
        elif a == "-t":
            if i + 1 >= n:
                err = "mv: option requires an argument -- 't'\n"
                break
            flags["target_dir"] = args[i + 1]
            i += 1
        elif a.startswith("--target-directory="):
            flags["target_dir"] = a.split("=", 1)[1]
        elif a.startswith("-") and len(a) > 1 and a != "-":
            if a[1] == "-":
                err = f"mv: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "f":
                    flags["force"] = True
                elif ch == "n":
                    flags["no_clobber"] = True
                elif ch == "v":
                    flags["verbose"] = True
                elif ch == "i":
                    pass
                elif ch == "T":
                    flags["no_target_dir"] = True
                else:
                    err = f"mv: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


@register("mv")
async def cmd_mv(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    no_clobber = bool(flags["no_clobber"])
    verbose = bool(flags["verbose"])
    no_target_dir = bool(flags["no_target_dir"])
    target_dir_arg = flags["target_dir"]

    if target_dir_arg is not None:
        sources = paths
        dst_label = str(target_dir_arg)
    else:
        if len(paths) < 2:
            return fail(
                1,
                encode("mv: missing destination file operand\n"),
            )
        sources = paths[:-1]
        dst_label = paths[-1]

    dst_target = resolve_cwd(ctx.env, dst_label)
    dst_is_dir = await ctx.vfs._isdir(dst_target)

    # If multi-source, dst must be a dir (unless target_dir form already implies dir).
    if len(sources) > 1 and not dst_is_dir and not target_dir_arg:
        return fail(1, encode(f"mv: target '{dst_label}' is not a directory\n"))
    if target_dir_arg is not None and not dst_is_dir:
        return fail(1, encode(f"mv: target '{dst_label}' is not a directory\n"))
    if no_target_dir and len(sources) != 1:
        return fail(
            1,
            encode("mv: extra operand after '" + dst_label + "'\n"),
        )

    stdout = b""
    stderr = b""
    exit_code = 0

    for src_label in sources:
        src_target = resolve_cwd(ctx.env, src_label)
        if not await ctx.vfs._exists(src_target):
            stderr += encode(mv_no_src(src_label))
            exit_code = 1
            continue

        if dst_is_dir and not no_target_dir:
            final_target = join(dst_target, basename(src_target))
            final_label = (
                dst_label.rstrip("/") + "/" + basename(src_target)
                if dst_label not in ("/", "")
                else "/" + basename(src_target)
            )
        else:
            final_target = dst_target
            final_label = dst_label

        if no_clobber and await ctx.vfs._exists(final_target):
            continue

        try:
            await ctx.vfs._mv(src_target, final_target)
        except OSError as e:
            stderr += encode(from_oserror("mv", src_label, e))
            exit_code = 1
            continue

        if verbose:
            stdout += encode(f"renamed '{src_label}' -> '{final_label}'\n")

    return ok(stdout=stdout, stderr=stderr) if exit_code == 0 else fail(
        exit_code, stderr=stderr, stdout=stdout
    )
