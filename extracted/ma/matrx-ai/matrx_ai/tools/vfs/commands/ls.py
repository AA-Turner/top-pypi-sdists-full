from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import (
    InodeView,
    format_date_ls,
    format_size_human,
    ls_no_access,
)
from matrx_ai.tools.vfs.paths import basename
from matrx_ai.tools.vfs.shell.runner import CommandResult

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.core import MatrxAsyncFS


_DEFAULT_USER = "user"
_DEFAULT_GROUP = "user"


class _Opts:
    __slots__ = (
        "long",
        "all",
        "almost_all",
        "human",
        "classify",
        "one_per_line",
        "recursive",
        "reverse",
        "sort_time",
        "sort_size",
        "directory",
        "inode",
    )

    def __init__(self) -> None:
        self.long: bool = False
        self.all: bool = False
        self.almost_all: bool = False
        self.human: bool = False
        self.classify: bool = False
        self.one_per_line: bool = False
        self.recursive: bool = False
        self.reverse: bool = False
        self.sort_time: bool = False
        self.sort_size: bool = False
        self.directory: bool = False
        self.inode: bool = False


_SHORT_FLAG_MAP = {
    "l": "long",
    "a": "all",
    "A": "almost_all",
    "h": "human",
    "F": "classify",
    "1": "one_per_line",
    "R": "recursive",
    "r": "reverse",
    "t": "sort_time",
    "S": "sort_size",
    "d": "directory",
    "i": "inode",
}

_LONG_FLAG_MAP = {
    "--all": "all",
    "--almost-all": "almost_all",
    "--human-readable": "human",
    "--classify": "classify",
    "--recursive": "recursive",
    "--reverse": "reverse",
    "--directory": "directory",
    "--inode": "inode",
}


def _parse_args(argv: list[str]) -> tuple[_Opts, list[str], str | None]:
    opts = _Opts()
    paths: list[str] = []
    end_of_opts = False
    for arg in argv[1:]:
        if end_of_opts:
            paths.append(arg)
            continue
        if arg == "--":
            end_of_opts = True
            continue
        if arg == "-" or not arg.startswith("-"):
            paths.append(arg)
            continue
        if arg.startswith("--"):
            target = _LONG_FLAG_MAP.get(arg)
            if target is None:
                return opts, paths, arg
            setattr(opts, target, True)
            continue
        # Clustered short options.
        for ch in arg[1:]:
            target = _SHORT_FLAG_MAP.get(ch)
            if target is None:
                return opts, paths, f"-{ch}"
            setattr(opts, target, True)
    return opts, paths, None


def _unrecognized_option(name: str) -> CommandResult:
    return fail(
        2,
        encode(f"ls: unrecognized option '{name}'\nTry 'ls --help' for more information.\n"),
    )


def _to_epoch(value: object) -> float:
    if isinstance(value, datetime):
        return value.timestamp()
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def _info_to_view(info: dict, override_name: str | None = None) -> InodeView:
    raw_type = info.get("type", "file")
    if raw_type == "directory":
        itype = "dir"
    elif raw_type == "link":
        itype = "link"
    else:
        itype = "file"

    name = override_name if override_name is not None else basename(info["name"])
    mode = info.get("mode")
    if mode is None:
        if itype == "dir":
            mode = 0o755
        elif itype == "link":
            mode = 0o777
        else:
            mode = 0o644

    nlink = info.get("nlink")
    if nlink is None:
        nlink = 2 if itype == "dir" else 1

    return InodeView(
        name=name,
        type=itype,  # type: ignore[typeddict-item]
        mode=int(mode),
        uid=int(info.get("uid", 0) or 0),
        gid=int(info.get("gid", 0) or 0),
        user=_DEFAULT_USER,
        group=_DEFAULT_GROUP,
        size=int(info.get("size", 0) or 0),
        nlink=int(nlink),
        mtime=_to_epoch(info.get("mtime", 0.0)),
        ctime=_to_epoch(info.get("ctime", 0.0)),
        atime=_to_epoch(info.get("atime", 0.0)),
        symlink_target=info.get("symlink_target"),
    )


def _perm_string(itype: str, mode: int) -> str:
    if itype == "dir":
        prefix = "d"
    elif itype == "link":
        prefix = "l"
    else:
        prefix = "-"
    bits = ""
    for shift in (6, 3, 0):
        chunk = (mode >> shift) & 0o7
        bits += "r" if chunk & 0o4 else "-"
        bits += "w" if chunk & 0o2 else "-"
        bits += "x" if chunk & 0o1 else "-"
    return prefix + bits


def _classify_suffix(itype: str, mode: int) -> str:
    if itype == "dir":
        return "/"
    if itype == "link":
        return "@"
    if (mode & 0o111) and itype == "file":
        return "*"
    return ""


def _name_for_listing(entry: InodeView, classify: bool, *, long: bool = False) -> str:
    name = entry["name"]
    if classify:
        name += _classify_suffix(entry["type"], entry["mode"])
    if long and entry["type"] == "link" and entry.get("symlink_target"):
        name = f"{name} -> {entry['symlink_target']}"
    return name


def _block_total(entries: list[InodeView]) -> int:
    total = 0
    for e in entries:
        size = e["size"]
        total += ((size + 4095) // 4096) * 4
    return total


def _format_total(total_blocks: int, human: bool) -> str:
    if not human:
        return f"total {total_blocks}"
    if total_blocks < 1024:
        return f"total {total_blocks}K"
    return f"total {format_size_human(total_blocks * 1024)}"


def _filter_visible(entries: list[InodeView], opts: _Opts) -> list[InodeView]:
    if opts.all or opts.almost_all:
        return list(entries)
    return [e for e in entries if not e["name"].startswith(".")]


def _apply_sort(entries: list[InodeView], opts: _Opts) -> list[InodeView]:
    # Default: ASCII case-sensitive by name.
    if opts.sort_time:
        sorted_list = sorted(entries, key=lambda e: e["name"])
        sorted_list.sort(key=lambda e: e["mtime"], reverse=True)
    elif opts.sort_size:
        sorted_list = sorted(entries, key=lambda e: e["name"])
        sorted_list.sort(key=lambda e: e["size"], reverse=True)
    else:
        sorted_list = sorted(entries, key=lambda e: e["name"])
    if opts.reverse:
        sorted_list.reverse()
    return sorted_list


def _format_long(
    entries: list[InodeView],
    opts: _Opts,
    *,
    show_total: bool,
    now: float | None = None,
) -> str:
    if not entries:
        return ""

    nlink_strs = [str(e["nlink"]) for e in entries]
    user_strs = [e["user"] for e in entries]
    group_strs = [e["group"] for e in entries]
    size_strs = [format_size_human(e["size"]) if opts.human else str(e["size"]) for e in entries]

    nlink_w = max(len(s) for s in nlink_strs)
    user_w = max(len(s) for s in user_strs)
    group_w = max(len(s) for s in group_strs)
    size_w = max(len(s) for s in size_strs)

    lines: list[str] = []
    if show_total:
        lines.append(_format_total(_block_total(entries), opts.human))

    for entry, nlink_s, user_s, group_s, size_s in zip(
        entries, nlink_strs, user_strs, group_strs, size_strs, strict=True
    ):
        perms = _perm_string(entry["type"], entry["mode"])
        date_str = format_date_ls(entry["mtime"], now)
        name = _name_for_listing(entry, opts.classify, long=True)
        lines.append(
            f"{perms} {nlink_s:>{nlink_w}} {user_s:<{user_w}} {group_s:<{group_w}} "
            f"{size_s:>{size_w}} {date_str} {name}"
        )
    return "\n".join(lines) + "\n"


def _format_simple(entries: list[InodeView], opts: _Opts) -> str:
    if not entries:
        return ""
    names = [_name_for_listing(e, opts.classify) for e in entries]
    return "\n".join(names) + "\n"


def _make_dot_entries(
    self_info: dict,
    parent_info: dict | None,
) -> list[InodeView]:
    items = [_info_to_view(self_info, override_name=".")]
    if parent_info is not None:
        items.append(_info_to_view(parent_info, override_name=".."))
    else:
        items.append(_info_to_view(self_info, override_name=".."))
    return items


async def _list_directory(
    vfs: MatrxAsyncFS,
    path: str,
    opts: _Opts,
) -> list[InodeView]:
    raw = await vfs._ls(path, detail=True)
    entries = [_info_to_view(info) for info in raw]

    visible = _filter_visible(entries, opts)
    sorted_entries = _apply_sort(visible, opts)

    if opts.all:
        try:
            self_info = await vfs._info(path)
        except FileNotFoundError:
            self_info = {"name": path, "type": "directory", "size": 0}
        parent_path = path.rsplit("/", 1)[0] or "/"
        try:
            parent_info = await vfs._info(parent_path)
        except FileNotFoundError:
            parent_info = None
        dot_entries = _make_dot_entries(self_info, parent_info)
        # Strip any `.` / `..` that may have come back from `_ls` (defensive — VFS
        # doesn't currently surface them, but ensure spec ordering: dots before
        # the sorted others).
        without_dots = [e for e in sorted_entries if e["name"] not in (".", "..")]
        return dot_entries + without_dots

    return sorted_entries


def _render_listing(entries: list[InodeView], opts: _Opts, *, show_total: bool) -> str:
    if opts.long:
        return _format_long(entries, opts, show_total=show_total)
    return _format_simple(entries, opts)


@register("ls", "dir")
async def cmd_ls(ctx: CommandContext) -> CommandResult:
    opts, raw_paths, bad = _parse_args(ctx.argv)
    if bad is not None:
        return _unrecognized_option(bad)

    if not raw_paths:
        raw_paths = [ctx.env.cwd]

    # Resolve all paths against cwd.
    resolved: list[tuple[str, str]] = []  # (display, absolute)
    for p in raw_paths:
        abs_path = p if p.startswith("/") else resolve_cwd(ctx.env, p)
        resolved.append((p, abs_path))

    # Classify each path: missing, file, dir.
    stderr_chunks: list[str] = []
    files: list[tuple[str, str, dict]] = []  # (display, abs, info)
    dirs: list[tuple[str, str]] = []  # (display, abs)
    for display, abs_path in resolved:
        try:
            info = await ctx.vfs._info(abs_path)
        except FileNotFoundError:
            stderr_chunks.append(ls_no_access(display))
            continue
        except OSError:
            stderr_chunks.append(ls_no_access(display))
            continue
        if opts.directory:
            files.append((display, abs_path, info))
            continue
        if info.get("type") == "directory":
            dirs.append((display, abs_path))
        else:
            files.append((display, abs_path, info))

    stdout_parts: list[str] = []

    # Render single-file/non-dir entries first as a single block.
    if files:
        file_entries = [_info_to_view(info, override_name=display) for display, _, info in files]
        # Sort the file group like a directory listing.
        file_entries = _apply_sort(file_entries, opts)
        if opts.long:
            stdout_parts.append(_format_long(file_entries, opts, show_total=False))
        else:
            stdout_parts.append(_format_simple(file_entries, opts))

    # Render directory listings (with section headers when more than one path).
    multi_section = (len(dirs) + len(files) > 1) or opts.recursive
    dirs.sort(key=lambda item: item[0], reverse=opts.reverse)

    async def render_dir(display: str, abs_path: str, *, force_header: bool) -> None:
        try:
            entries = await _list_directory(ctx.vfs, abs_path, opts)
        except PermissionError:
            stderr_chunks.append(f"ls: cannot open directory '{display}': Permission denied\n")
            return
        except FileNotFoundError:
            stderr_chunks.append(ls_no_access(display))
            return

        chunk = ""
        if multi_section or force_header:
            chunk = f"{display}:\n"
        chunk += _render_listing(entries, opts, show_total=True)
        stdout_parts.append(chunk)

        if opts.recursive:
            subdirs = [e for e in entries if e["type"] == "dir" and e["name"] not in (".", "..")]
            for sub in subdirs:
                sub_abs = (
                    abs_path.rstrip("/") + "/" + sub["name"]
                    if abs_path != "/"
                    else "/" + sub["name"]
                )
                sub_display = (
                    display.rstrip("/") + "/" + sub["name"] if display != "/" else "/" + sub["name"]
                )
                await render_dir(sub_display, sub_abs, force_header=True)

    for display, abs_path in dirs:
        await render_dir(display, abs_path, force_header=False)

    # Join stdout sections: when we have multiple sections, separate with a blank line
    # between them. Each section already ends in a newline, so a single extra "\n" between
    # sections produces the required blank line.
    non_empty = [p for p in stdout_parts if p]
    if multi_section and len(non_empty) > 1:
        out = "\n".join(non_empty)
    else:
        out = "".join(non_empty)

    stdout_bytes = encode(out)
    stderr_bytes = encode("".join(stderr_chunks))
    exit_code = 2 if stderr_chunks else 0
    return CommandResult(stdout=stdout_bytes, stderr=stderr_bytes, exit_code=exit_code)
