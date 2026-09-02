from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import rmdir_not_empty
from matrx_ai.tools.vfs.paths import dirname
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_args(args: list[str]) -> tuple[dict[str, object], list[str], str | None]:
    flags: dict[str, object] = {"parents": False, "verbose": False, "ignore_fail": False}
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
        elif a == "--ignore-fail-on-non-empty":
            flags["ignore_fail"] = True
        elif a.startswith("-") and len(a) > 1 and a != "-":
            if a[1] == "-":
                err = f"rmdir: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "p":
                    flags["parents"] = True
                elif ch == "v":
                    flags["verbose"] = True
                else:
                    err = f"rmdir: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


def _format_err(label: str, reason: str) -> str:
    return f"rmdir: failed to remove '{label}': {reason}\n"


async def _remove_one(ctx: CommandContext, label: str) -> tuple[bool, str | None]:
    target = label if label.startswith("/") else resolve_cwd(ctx.env, label)
    exists = await ctx.vfs._exists(target)
    if not exists:
        return False, _format_err(label, "No such file or directory")
    is_dir = await ctx.vfs._isdir(target)
    if not is_dir:
        return False, _format_err(label, "Not a directory")
    try:
        await ctx.vfs._rmdir(target)
    except OSError as e:
        code = getattr(e, "errno", None)
        if code == 39:
            return False, rmdir_not_empty(label)
        if code == 20:
            return False, _format_err(label, "Not a directory")
        if code == 2:
            return False, _format_err(label, "No such file or directory")
        return False, _format_err(label, e.strerror or "I/O error")
    return True, None


@register("rmdir")
async def cmd_rmdir(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    if not paths:
        return fail(
            1,
            encode("rmdir: missing operand\nTry 'rmdir --help' for more information.\n"),
        )

    parents = bool(flags["parents"])
    verbose = bool(flags["verbose"])
    ignore_fail = bool(flags["ignore_fail"])

    stdout = b""
    stderr = b""
    exit_code = 0

    for p in paths:
        ok_, msg = await _remove_one(ctx, p)
        if not ok_:
            assert msg is not None
            if ignore_fail and "Directory not empty" in msg:
                continue
            stderr += encode(msg)
            exit_code = 1
            continue
        if verbose:
            stdout += encode(f"rmdir: removing directory, '{p}'\n")
        if parents:
            # Walk upward removing empty parents using the same path label form.
            cur_label = p
            cur_target = resolve_cwd(ctx.env, p)
            while True:
                parent_label = (
                    cur_label.rsplit("/", 1)[0] if "/" in cur_label else ""
                )
                parent_target = dirname(cur_target)
                if not parent_label or parent_target in ("/", ""):
                    break
                ok2, msg2 = await _remove_one(ctx, parent_label)
                if not ok2:
                    assert msg2 is not None
                    if ignore_fail and "Directory not empty" in msg2:
                        break
                    stderr += encode(msg2)
                    exit_code = 1
                    break
                if verbose:
                    stdout += encode(f"rmdir: removing directory, '{parent_label}'\n")
                cur_label = parent_label
                cur_target = parent_target

    return ok(stdout=stdout, stderr=stderr) if exit_code == 0 else fail(
        exit_code, stderr=stderr, stdout=stdout
    )
