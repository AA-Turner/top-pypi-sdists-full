from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import from_oserror, mkdir_exists, mkdir_no_parent
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_args(args: list[str]) -> tuple[dict[str, object], list[str], str | None]:
    flags: dict[str, object] = {"parents": False, "verbose": False, "mode": None}
    paths: list[str] = []
    err: str | None = None
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        if a == "--":
            paths.extend(args[i + 1 :])
            break
        if a == "-p" or a == "--parents":
            flags["parents"] = True
        elif a == "-v" or a == "--verbose":
            flags["verbose"] = True
        elif a == "-m" or a == "--mode":
            if i + 1 >= n:
                err = "mkdir: option requires an argument -- 'm'\n"
                break
            flags["mode"] = args[i + 1]
            i += 1
        elif a.startswith("--mode="):
            flags["mode"] = a.split("=", 1)[1]
        elif a.startswith("-") and len(a) > 1 and a != "-":
            # Combined short flags like -pv
            if a[1] == "-":
                err = f"mkdir: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "p":
                    flags["parents"] = True
                elif ch == "v":
                    flags["verbose"] = True
                else:
                    err = f"mkdir: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


@register("mkdir")
async def cmd_mkdir(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    if not paths:
        return fail(1, encode("mkdir: missing operand\nTry 'mkdir --help' for more information.\n"))

    parents = bool(flags["parents"])
    verbose = bool(flags["verbose"])

    stdout = b""
    stderr = b""
    exit_code = 0

    for p in paths:
        target = resolve_cwd(ctx.env, p)
        try:
            if parents:
                await ctx.vfs._makedirs(target, exist_ok=True)
            else:
                await ctx.vfs._mkdir(target, create_parents=False)
        except FileExistsError:
            if parents:
                continue
            stderr += encode(mkdir_exists(p))
            exit_code = 1
            continue
        except FileNotFoundError:
            stderr += encode(mkdir_no_parent(p))
            exit_code = 1
            continue
        except NotADirectoryError as e:
            stderr += encode(from_oserror("mkdir", p, e))
            exit_code = 1
            continue
        except OSError as e:
            stderr += encode(from_oserror("mkdir", p, e))
            exit_code = 1
            continue
        if verbose:
            stdout += encode(f"mkdir: created directory '{p}'\n")

    return ok(stdout=stdout, stderr=stderr) if exit_code == 0 else fail(
        exit_code, stderr=stderr, stdout=stdout
    )
