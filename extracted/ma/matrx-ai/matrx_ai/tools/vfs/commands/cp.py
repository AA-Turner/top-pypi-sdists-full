from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import cp_no_src, cp_omit_dir, from_oserror
from matrx_ai.tools.vfs.paths import basename, join
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_args(args: list[str]) -> tuple[dict[str, object], list[str], str | None]:
    flags: dict[str, object] = {
        "force": False,
        "recursive": False,
        "verbose": False,
        "preserve": False,
        "no_clobber": False,
        "target_dir": None,
        "no_target_dir": False,
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
        elif a == "-p":
            flags["preserve"] = True
        elif a == "-n" or a == "--no-clobber":
            flags["no_clobber"] = True
        elif a == "-i":
            pass
        elif a == "-T" or a == "--no-target-directory":
            flags["no_target_dir"] = True
        elif a == "-t":
            if i + 1 >= n:
                err = "cp: option requires an argument -- 't'\n"
                break
            flags["target_dir"] = args[i + 1]
            i += 1
        elif a.startswith("--target-directory="):
            flags["target_dir"] = a.split("=", 1)[1]
        elif a == "-a":
            flags["recursive"] = True
            flags["preserve"] = True
        elif a.startswith("-") and len(a) > 1 and a != "-":
            if a[1] == "-":
                err = f"cp: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "f":
                    flags["force"] = True
                elif ch in ("r", "R"):
                    flags["recursive"] = True
                elif ch == "v":
                    flags["verbose"] = True
                elif ch == "p":
                    flags["preserve"] = True
                elif ch == "n":
                    flags["no_clobber"] = True
                elif ch == "i":
                    pass
                elif ch == "T":
                    flags["no_target_dir"] = True
                elif ch == "a":
                    flags["recursive"] = True
                    flags["preserve"] = True
                else:
                    err = f"cp: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


async def _copy_recursive(
    ctx: CommandContext,
    src: str,
    dst: str,
    src_label: str,
    dst_label: str,
    *,
    preserve: bool,
    no_clobber: bool,
    verbose: bool,
) -> tuple[bytes, bytes, int]:
    stdout = b""
    stderr = b""
    exit_code = 0

    is_dir = await ctx.vfs._isdir(src)
    if is_dir:
        # Make dst dir if needed.
        if not await ctx.vfs._exists(dst):
            try:
                await ctx.vfs._mkdir(dst, create_parents=False)
            except OSError as e:
                return stdout, encode(from_oserror("cp", dst_label, e)), 1
        elif not await ctx.vfs._isdir(dst):
            return (
                stdout,
                encode(f"cp: cannot overwrite non-directory '{dst_label}' with directory '{src_label}'\n"),
                1,
            )
        if verbose:
            stdout += encode(f"'{src_label}' -> '{dst_label}'\n")
        # Recurse into children.
        try:
            entries = await ctx.vfs._ls(src, detail=True)
        except OSError as e:
            return stdout, encode(from_oserror("cp", src_label, e)), 1
        for entry in entries:
            child_name = basename(entry["name"])
            child_src = join(src, child_name)
            child_dst = join(dst, child_name)
            child_src_label = src_label.rstrip("/") + "/" + child_name
            child_dst_label = dst_label.rstrip("/") + "/" + child_name
            so, se, ec = await _copy_recursive(
                ctx,
                child_src,
                child_dst,
                child_src_label,
                child_dst_label,
                preserve=preserve,
                no_clobber=no_clobber,
                verbose=verbose,
            )
            stdout += so
            stderr += se
            if ec != 0:
                exit_code = 1
    else:
        if no_clobber and await ctx.vfs._exists(dst):
            return stdout, stderr, exit_code
        try:
            await ctx.vfs._cp_file(src, dst)
        except OSError as e:
            return stdout, encode(from_oserror("cp", src_label, e)), 1
        if preserve:
            try:
                src_inode = await ctx.vfs._resolve(src)
                dst_inode = await ctx.vfs._resolve(dst)
                await ctx.vfs.backend.update_inode(
                    dst_inode.id,
                    mode=src_inode.mode,
                    mtime=src_inode.mtime,
                    atime=src_inode.atime,
                )
            except OSError:
                pass
        if verbose:
            stdout += encode(f"'{src_label}' -> '{dst_label}'\n")

    return stdout, stderr, exit_code


@register("cp")
async def cmd_cp(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    recursive = bool(flags["recursive"])
    verbose = bool(flags["verbose"])
    preserve = bool(flags["preserve"])
    no_clobber = bool(flags["no_clobber"])
    no_target_dir = bool(flags["no_target_dir"])
    target_dir_arg = flags["target_dir"]

    if target_dir_arg is not None:
        sources = paths
        dst_label = str(target_dir_arg)
    else:
        if len(paths) < 2:
            return fail(1, encode("cp: missing destination file operand\n"))
        sources = paths[:-1]
        dst_label = paths[-1]

    dst_target = resolve_cwd(ctx.env, dst_label)
    dst_is_dir = await ctx.vfs._isdir(dst_target)

    if (len(sources) > 1 or target_dir_arg is not None) and not dst_is_dir:
        return fail(1, encode(f"cp: target '{dst_label}' is not a directory\n"))
    if no_target_dir and len(sources) != 1:
        return fail(1, encode(f"cp: extra operand after '{dst_label}'\n"))

    stdout = b""
    stderr = b""
    exit_code = 0

    for src_label in sources:
        src_target = resolve_cwd(ctx.env, src_label)
        if not await ctx.vfs._exists(src_target):
            stderr += encode(cp_no_src(src_label))
            exit_code = 1
            continue

        src_is_dir = await ctx.vfs._isdir(src_target)
        if src_is_dir and not recursive:
            stderr += encode(cp_omit_dir(src_label))
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

        so, se, ec = await _copy_recursive(
            ctx,
            src_target,
            final_target,
            src_label,
            final_label,
            preserve=preserve,
            no_clobber=no_clobber,
            verbose=verbose,
        )
        stdout += so
        stderr += se
        if ec != 0:
            exit_code = 1

    return ok(stdout=stdout, stderr=stderr) if exit_code == 0 else fail(
        exit_code, stderr=stderr, stdout=stdout
    )
