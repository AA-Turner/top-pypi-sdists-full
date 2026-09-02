from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import from_oserror, rm_is_dir, rm_no_file
from matrx_ai.tools.vfs.paths import normalize
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_args(args: list[str]) -> tuple[dict[str, object], list[str], str | None]:
    flags: dict[str, object] = {
        "force": False,
        "recursive": False,
        "verbose": False,
        "dir": False,
        "no_preserve_root": False,
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
        elif a == "-r" or a == "-R" or a == "--recursive":
            flags["recursive"] = True
        elif a == "-v" or a == "--verbose":
            flags["verbose"] = True
        elif a == "-d" or a == "--dir":
            flags["dir"] = True
        elif a == "-i":
            # Refuse to mimic interactive — silently ignored (act non-interactive).
            pass
        elif a == "--no-preserve-root":
            flags["no_preserve_root"] = True
        elif a == "--preserve-root":
            pass
        elif a.startswith("-") and len(a) > 1 and a != "-":
            if a[1] == "-":
                err = f"rm: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "f":
                    flags["force"] = True
                elif ch in ("r", "R"):
                    flags["recursive"] = True
                elif ch == "v":
                    flags["verbose"] = True
                elif ch == "d":
                    flags["dir"] = True
                elif ch == "i":
                    pass
                else:
                    err = f"rm: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


@register("rm")
async def cmd_rm(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    force = bool(flags["force"])
    recursive = bool(flags["recursive"])
    verbose = bool(flags["verbose"])
    rm_dir = bool(flags["dir"])
    no_preserve_root = bool(flags["no_preserve_root"])

    if not paths:
        if force:
            return ok()
        return fail(1, encode("rm: missing operand\nTry 'rm --help' for more information.\n"))

    stdout = b""
    stderr = b""
    exit_code = 0

    for p in paths:
        target = resolve_cwd(ctx.env, p)
        if recursive and normalize(target) == "/" and not no_preserve_root:
            stderr += encode(
                "rm: it is dangerous to operate recursively on '/'\n"
                "rm: use --no-preserve-root to override this failsafe\n"
            )
            exit_code = 1
            continue

        exists = await ctx.vfs._exists(target)
        if not exists:
            if force:
                continue
            stderr += encode(rm_no_file(p))
            exit_code = 1
            continue

        is_dir = await ctx.vfs._isdir(target)
        if is_dir and not recursive and not rm_dir:
            stderr += encode(rm_is_dir(p))
            exit_code = 1
            continue

        try:
            if is_dir and rm_dir and not recursive:
                await ctx.vfs._rmdir(target)
            else:
                await ctx.vfs._rm(target, recursive=recursive)
        except OSError as e:
            if force and getattr(e, "errno", None) == 2:
                continue
            stderr += encode(from_oserror("rm", p, e))
            exit_code = 1
            continue

        if verbose:
            stdout += encode(f"removed '{p}'\n")

    return ok(stdout=stdout, stderr=stderr) if exit_code == 0 else fail(
        exit_code, stderr=stderr, stdout=stdout
    )
