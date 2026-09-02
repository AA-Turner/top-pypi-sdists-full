from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import chmod_no_access
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_octal_mode(spec: str) -> int | None:
    if not spec:
        return None
    if not all(c in "01234567" for c in spec):
        return None
    if len(spec) > 4:
        return None
    try:
        return int(spec, 8)
    except ValueError:
        return None


def _apply_symbolic_clause(current: int, clause: str, is_dir: bool) -> int | None:
    # clause = "[ugoa]*[-+=][rwxX]*"
    # split who from rest
    i = 0
    who: str = ""
    while i < len(clause) and clause[i] in "ugoa":
        who += clause[i]
        i += 1
    if i >= len(clause):
        return None
    op = clause[i]
    if op not in "+-=":
        return None
    perms_str = clause[i + 1 :]
    for c in perms_str:
        if c not in "rwxXst":
            return None

    # Compute affected bit mask per "who".
    if not who:
        who = "a"

    perm_mask = 0
    for c in perms_str:
        if c == "r":
            perm_mask |= 0o4
        elif c == "w":
            perm_mask |= 0o2
        elif c == "x":
            perm_mask |= 0o1
        elif c == "X":
            # Set x only if dir or any execute already set.
            any_x = (current & 0o111) != 0
            if is_dir or any_x:
                perm_mask |= 0o1
        elif c == "s" or c == "t":
            # ignore setuid/setgid/sticky for now
            pass

    new_mode = current
    for w in who:
        if w == "u":
            shift = 6
            who_mask = 0o700
        elif w == "g":
            shift = 3
            who_mask = 0o070
        elif w == "o":
            shift = 0
            who_mask = 0o007
        elif w == "a":
            for shift_, who_mask_ in ((6, 0o700), (3, 0o070), (0, 0o007)):
                pmask_shifted = perm_mask << shift_
                if op == "+":
                    new_mode = new_mode | pmask_shifted
                elif op == "-":
                    new_mode = new_mode & ~pmask_shifted
                else:  # "="
                    new_mode = (new_mode & ~who_mask_) | pmask_shifted
            continue
        else:
            return None
        pmask_shifted = perm_mask << shift
        if op == "+":
            new_mode = new_mode | pmask_shifted
        elif op == "-":
            new_mode = new_mode & ~pmask_shifted
        else:  # "="
            new_mode = (new_mode & ~who_mask) | pmask_shifted

    return new_mode & 0o7777


def _apply_mode_spec(current: int, spec: str, is_dir: bool) -> int | None:
    octal = _parse_octal_mode(spec)
    if octal is not None:
        return octal & 0o7777
    parts = spec.split(",")
    new_mode = current
    for clause in parts:
        if not clause:
            return None
        result = _apply_symbolic_clause(new_mode, clause, is_dir)
        if result is None:
            return None
        new_mode = result
    return new_mode & 0o7777


def _perm_string(itype: str, mode: int) -> str:
    bits = ""
    for shift in (6, 3, 0):
        chunk = (mode >> shift) & 0o7
        bits += "r" if chunk & 0o4 else "-"
        bits += "w" if chunk & 0o2 else "-"
        bits += "x" if chunk & 0o1 else "-"
    _ = itype
    return bits


class _ChmodOpts:
    __slots__ = ("recursive", "verbose", "changes", "quiet")

    def __init__(self) -> None:
        self.recursive: bool = False
        self.verbose: bool = False
        self.changes: bool = False
        self.quiet: bool = False


def _parse_args(args: list[str]) -> tuple[_ChmodOpts, str | None, list[str], CommandResult | None]:
    opts = _ChmodOpts()
    mode_spec: str | None = None
    paths: list[str] = []
    end_of_opts = False
    for a in args:
        if end_of_opts:
            if mode_spec is None:
                mode_spec = a
            else:
                paths.append(a)
            continue
        if a == "--":
            end_of_opts = True
            continue
        if mode_spec is None:
            if a.startswith("-") and len(a) > 1:
                # Could be a flag like -R, -v, etc. — distinguish from a numeric mode.
                # GNU chmod requires symbolic modes to lead with a non-flag token, but
                # if the token starts with a digit or +/=/-letter that isn't a flag,
                # treat it as a mode.
                rest = a[1:]
                if rest and rest[0].isdigit():
                    mode_spec = a[1:]
                    continue
                only_flags = True
                for ch in rest:
                    if ch in ("R", "v", "c", "f", "-"):
                        continue
                    only_flags = False
                    break
                if not only_flags:
                    # Probably a symbolic mode like -rwx — treat as mode.
                    mode_spec = a[1:]
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
                for ch in rest:
                    if ch == "R":
                        opts.recursive = True
                    elif ch == "v":
                        opts.verbose = True
                    elif ch == "c":
                        opts.changes = True
                    elif ch == "f":
                        opts.quiet = True
                continue
            mode_spec = a
            continue
        paths.append(a)

    if mode_spec is None:
        return opts, None, paths, fail(
            1,
            encode(
                "chmod: missing operand\nTry 'chmod --help' for more information.\n"
            ),
        )
    return opts, mode_spec, paths, None


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


@register("chmod")
async def cmd_chmod(ctx: CommandContext) -> CommandResult:
    opts, mode_spec, raw_paths, err = _parse_args(ctx.args)
    if err is not None:
        return err
    assert mode_spec is not None

    if not raw_paths:
        return fail(
            1,
            encode(
                f"chmod: missing operand after '{mode_spec}'\n"
                "Try 'chmod --help' for more information.\n"
            ),
        )

    out = bytearray()
    err_out = bytearray()
    exit_code = 0

    for display in raw_paths:
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
        try:
            info = await ctx.vfs._info(abs_path)
        except FileNotFoundError:
            err_out.extend(encode(chmod_no_access(display)))
            exit_code = 1
            continue
        except OSError:
            err_out.extend(encode(chmod_no_access(display)))
            exit_code = 1
            continue

        # Build a list of (display_path, abs_path) targets.
        if opts.recursive and info.get("type") == "directory":
            absolute_targets = await _walk_paths(ctx.vfs, abs_path)
        else:
            absolute_targets = [abs_path]

        for tgt in absolute_targets:
            try:
                tgt_info = await ctx.vfs._info(tgt)
            except FileNotFoundError:
                continue
            current_mode = int(tgt_info.get("mode") or 0o644) & 0o7777
            is_dir = tgt_info.get("type") == "directory"
            new_mode = _apply_mode_spec(current_mode, mode_spec, is_dir)
            if new_mode is None:
                err_out.extend(encode(f"chmod: invalid mode: '{mode_spec}'\n"))
                return CommandResult(
                    stdout=bytes(out), stderr=bytes(err_out), exit_code=1
                )
            inode = await ctx.vfs.backend.get_inode_by_path(ctx.vfs.workspace_id, tgt)
            if inode is None:
                continue
            await ctx.vfs.backend.update_inode(inode.id, mode=new_mode)
            tgt_display = display if tgt == abs_path else (
                display + tgt[len(abs_path):] if abs_path != "/" else tgt
            )
            if opts.verbose:
                if new_mode != current_mode:
                    out.extend(
                        encode(
                            f"mode of '{tgt_display}' changed from "
                            f"0{current_mode:04o} ({_perm_string('', current_mode)}) to "
                            f"0{new_mode:04o} ({_perm_string('', new_mode)})\n"
                        )
                    )
                else:
                    out.extend(
                        encode(
                            f"mode of '{tgt_display}' retained as "
                            f"0{new_mode:04o} ({_perm_string('', new_mode)})\n"
                        )
                    )
            elif opts.changes and new_mode != current_mode:
                out.extend(
                    encode(
                        f"mode of '{tgt_display}' changed from "
                        f"0{current_mode:04o} ({_perm_string('', current_mode)}) to "
                        f"0{new_mode:04o} ({_perm_string('', new_mode)})\n"
                    )
                )

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
