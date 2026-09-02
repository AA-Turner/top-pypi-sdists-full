from __future__ import annotations

import hashlib

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _name_to_uid(name: str) -> int:
    if name == "root":
        return 0
    if name == "user":
        return 1000
    if name.isdigit():
        return int(name)
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()
    return 1001 + (int(digest[:8], 16) % 9000)


def _parse_owner_spec(spec: str) -> tuple[int | None, int | None, str | None, str | None] | None:
    # "USER", "USER:GROUP", ":GROUP", "USER:" — returns (uid, gid, user, group).
    if not spec:
        return None
    if ":" not in spec and "." not in spec:
        return _name_to_uid(spec), None, spec, None
    if ":" in spec:
        user_part, group_part = spec.split(":", 1)
    else:
        user_part, group_part = spec.split(".", 1)
    uid: int | None
    gid: int | None
    user_name: str | None
    group_name: str | None

    if user_part:
        uid = _name_to_uid(user_part)
        user_name = user_part
    else:
        uid = None
        user_name = None
    if group_part:
        gid = _name_to_uid(group_part)
        group_name = group_part
    else:
        gid = None
        group_name = None
    return uid, gid, user_name, group_name


class _ChownOpts:
    __slots__ = ("recursive", "verbose", "changes", "quiet")

    def __init__(self) -> None:
        self.recursive: bool = False
        self.verbose: bool = False
        self.changes: bool = False
        self.quiet: bool = False


def _parse_args(args: list[str]) -> tuple[_ChownOpts, str | None, list[str], CommandResult | None]:
    opts = _ChownOpts()
    spec: str | None = None
    paths: list[str] = []
    end_of_opts = False
    for a in args:
        if end_of_opts:
            if spec is None:
                spec = a
            else:
                paths.append(a)
            continue
        if a == "--":
            end_of_opts = True
            continue
        if a == "--recursive":
            opts.recursive = True
            continue
        if a == "--verbose":
            opts.verbose = True
            continue
        if a == "--changes":
            opts.changes = True
            continue
        if a == "--silent" or a == "--quiet":
            opts.quiet = True
            continue
        if a.startswith("-") and len(a) > 1 and not a.startswith("--") and spec is None:
            # may be a flag bundle
            ok_flags = True
            for ch in a[1:]:
                if ch == "R":
                    opts.recursive = True
                elif ch == "v":
                    opts.verbose = True
                elif ch == "c":
                    opts.changes = True
                elif ch == "f":
                    opts.quiet = True
                elif ch == "h":
                    pass
                else:
                    ok_flags = False
                    break
            if ok_flags:
                continue
            # Otherwise, treat as the spec.
            spec = a
            continue
        if spec is None:
            spec = a
            continue
        paths.append(a)
    return opts, spec, paths, None


async def _walk_paths(vfs, root: str) -> list[str]:
    out: list[str] = [root]
    info = await vfs._info(root)
    if info.get("type") != "directory":
        return out
    children = await vfs._ls(root, detail=True)
    children.sort(key=lambda c: c.get("name") or "")
    for child in children:
        cpath = child["name"]
        if child.get("type") == "directory":
            out.extend(await _walk_paths(vfs, cpath))
        else:
            out.append(cpath)
    return out


@register("chown")
async def cmd_chown(ctx: CommandContext) -> CommandResult:
    opts, spec, raw_paths, err = _parse_args(ctx.args)
    if err is not None:
        return err
    if spec is None:
        return fail(
            1,
            encode(
                "chown: missing operand\nTry 'chown --help' for more information.\n"
            ),
        )
    parsed = _parse_owner_spec(spec)
    if parsed is None:
        return fail(1, encode(f"chown: invalid spec: '{spec}'\n"))
    uid, gid, user_name, group_name = parsed

    if not raw_paths:
        return fail(
            1,
            encode(
                f"chown: missing operand after '{spec}'\n"
                "Try 'chown --help' for more information.\n"
            ),
        )

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    for display in raw_paths:
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
        if not await ctx.vfs._exists(abs_path):
            err_out.extend(
                encode(f"chown: cannot access '{display}': No such file or directory\n")
            )
            exit_code = 1
            continue

        try:
            info = await ctx.vfs._info(abs_path)
        except OSError:
            err_out.extend(
                encode(f"chown: cannot access '{display}': No such file or directory\n")
            )
            exit_code = 1
            continue

        targets: list[str] = []
        if opts.recursive and info.get("type") == "directory":
            targets = await _walk_paths(ctx.vfs, abs_path)
        else:
            targets = [abs_path]

        for tgt in targets:
            inode = await ctx.vfs.backend.get_inode_by_path(ctx.vfs.workspace_id, tgt)
            if inode is None:
                continue
            updates: dict = {}
            if uid is not None:
                updates["uid"] = uid
            if gid is not None:
                updates["gid"] = gid
            if updates:
                await ctx.vfs.backend.update_inode(inode.id, **updates)
            if opts.verbose:
                desc = user_name or ""
                if group_name:
                    desc = f"{desc}:{group_name}" if desc else f":{group_name}"
                tgt_display = display if tgt == abs_path else (
                    display + tgt[len(abs_path):] if abs_path != "/" else tgt
                )
                out.extend(
                    encode(f"changed ownership of '{tgt_display}' to {desc}\n")
                )

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
