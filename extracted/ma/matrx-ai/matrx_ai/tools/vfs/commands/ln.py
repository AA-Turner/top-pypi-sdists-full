from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import from_oserror, ln_exists
from matrx_ai.tools.vfs.paths import basename, join
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_args(args: list[str]) -> tuple[dict[str, object], list[str], str | None]:
    flags: dict[str, object] = {
        "symbolic": False,
        "force": False,
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
        if a == "-s" or a == "--symbolic":
            flags["symbolic"] = True
        elif a == "-f" or a == "--force":
            flags["force"] = True
        elif a == "-v" or a == "--verbose":
            flags["verbose"] = True
        elif a == "-T" or a == "--no-target-directory":
            flags["no_target_dir"] = True
        elif a == "-t":
            if i + 1 >= n:
                err = "ln: option requires an argument -- 't'\n"
                break
            flags["target_dir"] = args[i + 1]
            i += 1
        elif a.startswith("--target-directory="):
            flags["target_dir"] = a.split("=", 1)[1]
        elif a.startswith("-") and len(a) > 1 and a != "-":
            if a[1] == "-":
                err = f"ln: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "s":
                    flags["symbolic"] = True
                elif ch == "f":
                    flags["force"] = True
                elif ch == "v":
                    flags["verbose"] = True
                elif ch == "T":
                    flags["no_target_dir"] = True
                else:
                    err = f"ln: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


@register("ln")
async def cmd_ln(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    symbolic = bool(flags["symbolic"])
    force = bool(flags["force"])
    verbose = bool(flags["verbose"])
    no_target_dir = bool(flags["no_target_dir"])
    target_dir_arg = flags["target_dir"]

    if target_dir_arg is not None:
        targets = paths
        link_dir_label = str(target_dir_arg)
    else:
        if len(paths) < 1:
            return fail(1, encode("ln: missing file operand\n"))
        if len(paths) == 1:
            # ln T  -- create T-named link in cwd to T
            targets = [paths[0]]
            link_dir_label = "."
        else:
            targets = paths[:-1]
            link_dir_label = paths[-1]

    # Determine if link_dir_label refers to a directory or a single link path.
    link_dir_target = resolve_cwd(ctx.env, link_dir_label)
    last_is_dir = await ctx.vfs._isdir(link_dir_target)
    multi = len(targets) > 1 or target_dir_arg is not None

    if multi and not last_is_dir:
        return fail(1, encode(f"ln: target '{link_dir_label}' is not a directory\n"))

    stdout = b""
    stderr = b""
    exit_code = 0

    for src_label in targets:
        if multi or (target_dir_arg is None and len(paths) == 1):
            # link path is link_dir + basename(src_label)
            link_label = (
                link_dir_label.rstrip("/") + "/" + basename(src_label)
                if link_dir_label not in (".", "")
                else basename(src_label)
            )
            link_target = (
                join(link_dir_target, basename(src_label))
                if link_dir_target != "."
                else resolve_cwd(ctx.env, basename(src_label))
            )
        else:
            # 2-arg form: ln T L
            if last_is_dir and not no_target_dir:
                link_label = link_dir_label.rstrip("/") + "/" + basename(src_label)
                link_target = join(link_dir_target, basename(src_label))
            else:
                link_label = link_dir_label
                link_target = link_dir_target

        if not symbolic:
            stderr += encode(
                f"ln: failed to create hard link '{link_label}': Operation not supported\n"
            )
            exit_code = 1
            continue

        # Handle existing link target with -f
        if await ctx.vfs._exists(link_target):
            if not force:
                stderr += encode(ln_exists(link_label))
                exit_code = 1
                continue
            try:
                await ctx.vfs._rm(link_target, recursive=False)
            except OSError as e:
                stderr += encode(from_oserror("ln", link_label, e))
                exit_code = 1
                continue

        try:
            await ctx.vfs._symlink(src_label, link_target)
        except OSError as e:
            if getattr(e, "errno", None) == 17:
                stderr += encode(ln_exists(link_label))
            else:
                stderr += encode(from_oserror("ln", link_label, e))
            exit_code = 1
            continue

        if verbose:
            stdout += encode(f"'{link_label}' -> '{src_label}'\n")

    return ok(stdout=stdout, stderr=stderr) if exit_code == 0 else fail(
        exit_code, stderr=stderr, stdout=stdout
    )
