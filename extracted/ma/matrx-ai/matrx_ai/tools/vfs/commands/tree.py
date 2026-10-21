from __future__ import annotations

from matrx_utils.utils.text_tree import render_text_tree

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


class _TreeOpts:
    __slots__ = ("max_depth", "all_files", "dirs_only", "full_paths", "no_report")

    def __init__(self) -> None:
        self.max_depth: int | None = None
        self.all_files: bool = False
        self.dirs_only: bool = False
        self.full_paths: bool = False
        self.no_report: bool = False


def _parse_args(args: list[str]) -> tuple[_TreeOpts, list[str], CommandResult | None]:
    opts = _TreeOpts()
    paths: list[str] = []
    i = 0
    end_of_opts = False
    while i < len(args):
        a = args[i]
        if end_of_opts:
            paths.append(a)
            i += 1
            continue
        if a == "--":
            end_of_opts = True
            i += 1
            continue
        if a == "--noreport":
            opts.no_report = True
            i += 1
            continue
        if a == "-L":
            if i + 1 >= len(args):
                return opts, paths, CommandResult(
                    stdout=b"",
                    stderr=encode("tree: option -L requires an argument\n"),
                    exit_code=1,
                )
            try:
                opts.max_depth = int(args[i + 1])
            except ValueError:
                return opts, paths, CommandResult(
                    stdout=b"",
                    stderr=encode(f"tree: invalid level argument '{args[i + 1]}'\n"),
                    exit_code=1,
                )
            i += 2
            continue
        if a.startswith("-L"):
            try:
                opts.max_depth = int(a[2:])
            except ValueError:
                return opts, paths, CommandResult(
                    stdout=b"",
                    stderr=encode(f"tree: invalid level argument '{a[2:]}'\n"),
                    exit_code=1,
                )
            i += 1
            continue
        if a.startswith("-") and len(a) > 1 and not a.startswith("--"):
            for ch in a[1:]:
                if ch == "a":
                    opts.all_files = True
                elif ch == "d":
                    opts.dirs_only = True
                elif ch == "f":
                    opts.full_paths = True
                elif ch == "C" or ch == "n" or ch == "F" or ch == "i":
                    pass
                else:
                    return opts, paths, CommandResult(
                        stdout=b"",
                        stderr=encode(f"tree: invalid option -- '{ch}'\n"),
                        exit_code=1,
                    )
            i += 1
            continue
        paths.append(a)
        i += 1
    return opts, paths, None


def _format_count_line(dirs: int, files: int, dirs_only: bool) -> str:
    dir_word = "directory" if dirs == 1 else "directories"
    if dirs_only:
        return f"{dirs} {dir_word}\n"
    file_word = "file" if files == 1 else "files"
    return f"{dirs} {dir_word}, {files} {file_word}\n"


async def _render_tree(
    vfs, root_display: str, root_abs: str, opts: _TreeOpts
) -> tuple[str, int, int, bool]:
    # Returns (output, dir_count, file_count, error).
    if not await vfs._exists(root_abs):
        return f"{root_display} [error opening dir]\n", 0, 0, True

    # Entry display name -> its children (a directory) or None; drawn by the one renderer.
    tree: dict = {}
    dir_count = 0
    file_count = 0

    async def walk(path_abs: str, display_prefix: str, node: dict, depth: int) -> None:
        nonlocal dir_count, file_count
        if opts.max_depth is not None and depth > opts.max_depth:
            return
        try:
            children = await vfs._ls(path_abs, detail=True)
        except FileNotFoundError:
            return
        except OSError:
            return
        children.sort(key=lambda c: c.get("name") or "")
        # Filter dotfiles unless -a
        visible = []
        for c in children:
            cname = (c.get("name") or "").rsplit("/", 1)[-1]
            if not opts.all_files and cname.startswith("."):
                continue
            if opts.dirs_only and c.get("type") != "directory":
                continue
            visible.append(c)
        for child in visible:
            cname = (child.get("name") or "").rsplit("/", 1)[-1]
            ctype = child.get("type") or "file"
            cpath_abs = child["name"]
            if opts.full_paths:
                if display_prefix.endswith("/"):
                    display_name = display_prefix + cname
                elif display_prefix == "":
                    display_name = cname
                else:
                    display_name = display_prefix + "/" + cname
            else:
                display_name = cname
            if ctype == "link":
                display_name = f"{display_name} -> {child.get('symlink_target') or ''}"
            if ctype == "directory":
                dir_count += 1
                node[display_name] = children_node = {}
                next_prefix = (
                    (display_prefix.rstrip("/") + "/" + cname)
                    if display_prefix and display_prefix != "/"
                    else (display_prefix + cname if display_prefix == "/" else cname)
                )
                if opts.full_paths:
                    if display_prefix == "/":
                        next_prefix = "/" + cname
                    elif display_prefix == "":
                        next_prefix = cname
                    else:
                        next_prefix = display_prefix.rstrip("/") + "/" + cname
                await walk(cpath_abs, next_prefix, children_node, depth + 1)
            else:
                node[display_name] = None
                file_count += 1

    await walk(root_abs, root_display, tree, 1)
    return render_text_tree(root_display, tree, dir_suffix="") + "\n", dir_count, file_count, False


@register("tree")
async def cmd_tree(ctx: CommandContext) -> CommandResult:
    opts, raw_paths, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not raw_paths:
        raw_paths = ["."]

    out = bytearray()
    err_out = bytearray()
    exit_code = 0
    total_dirs = 0
    total_files = 0
    any_error = False

    for idx, display in enumerate(raw_paths):
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
        rendered, d, f, error = await _render_tree(ctx.vfs, display, abs_path, opts)
        out.extend(encode(rendered))
        if error:
            any_error = True
        else:
            total_dirs += d
            total_files += f
        if idx < len(raw_paths) - 1:
            out.extend(b"\n")

    if not opts.no_report:
        out.extend(b"\n")
        if any_error and total_dirs == 0 and total_files == 0:
            out.extend(encode("0 directories, 0 files\n"))
        else:
            out.extend(encode(_format_count_line(total_dirs, total_files, opts.dirs_only)))

    _ = ok  # silence unused import in case of future rework
    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
