from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from matrx_ai.tools.vfs.mimicry.dates import format_date_ls
from matrx_ai.tools.vfs.mimicry.sizes import format_size_human

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.mimicry import InodeView


class LsOpts(BaseModel):
    long: bool = False
    all: bool = False
    human: bool = False
    classify: bool = False
    one_per_line: bool = False
    recursive: bool = False
    show_hidden: bool = False
    list_single_file: bool = False
    now: float | None = None


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


def _name_for_listing(entry: InodeView, classify: bool) -> str:
    name = entry["name"]
    if classify:
        name += _classify_suffix(entry["type"], entry["mode"])
    if entry["type"] == "link" and entry.get("symlink_target"):
        name = f"{name} -> {entry['symlink_target']}"
    return name


def _sort_entries(entries: list[InodeView], show_hidden: bool) -> list[InodeView]:
    filtered = [e for e in entries if show_hidden or not e["name"].startswith(".")]
    filtered.sort(key=lambda e: e["name"])
    return filtered


def _block_total(entries: list[InodeView]) -> int:
    total = 0
    for e in entries:
        size = e["size"]
        # 1 KiB blocks (default for `ls -l`); round up to 4 KiB filesystem blocks.
        total += ((size + 4095) // 4096) * 4
    return total


def _format_size(size: int, human: bool) -> str:
    if human:
        return format_size_human(size)
    return str(size)


def _format_total(total_blocks: int, human: bool) -> str:
    if not human:
        return f"total {total_blocks}"
    # `ls -lh` uses a human-readable total in K/M/G with the suffix attached.
    if total_blocks < 1024:
        return f"total {total_blocks}K"
    return f"total {format_size_human(total_blocks * 1024)}"


def _format_long(entries: list[InodeView], opts: LsOpts) -> str:
    sorted_entries = _sort_entries(entries, opts.show_hidden or opts.all)
    if not sorted_entries:
        # Empty directory, no total line per coreutils when no entries.
        return ""

    nlink_strs = [str(e["nlink"]) for e in sorted_entries]
    user_strs = [e["user"] for e in sorted_entries]
    group_strs = [e["group"] for e in sorted_entries]
    size_strs = [_format_size(e["size"], opts.human) for e in sorted_entries]

    nlink_w = max(len(s) for s in nlink_strs)
    user_w = max(len(s) for s in user_strs)
    group_w = max(len(s) for s in group_strs)
    size_w = max(len(s) for s in size_strs)

    lines: list[str] = []
    if not opts.list_single_file:
        lines.append(_format_total(_block_total(sorted_entries), opts.human))

    for entry, nlink_s, user_s, group_s, size_s in zip(
        sorted_entries, nlink_strs, user_strs, group_strs, size_strs, strict=True
    ):
        perms = _perm_string(entry["type"], entry["mode"])
        date_str = format_date_ls(entry["mtime"], opts.now)
        name = _name_for_listing(entry, opts.classify)
        lines.append(
            f"{perms} {nlink_s:>{nlink_w}} {user_s:<{user_w}} {group_s:<{group_w}} "
            f"{size_s:>{size_w}} {date_str} {name}"
        )
    return "\n".join(lines) + "\n"


def format_ls_l(entries: list[InodeView], opts: LsOpts) -> str:
    o = opts.model_copy(update={"long": True, "human": False})
    return _format_long(entries, o)


def format_ls_lh(entries: list[InodeView], opts: LsOpts) -> str:
    o = opts.model_copy(update={"long": True, "human": True})
    return _format_long(entries, o)


def format_ls_simple(entries: list[InodeView], opts: LsOpts) -> str:
    sorted_entries = _sort_entries(entries, opts.show_hidden or opts.all)
    if not sorted_entries:
        return ""
    names = [_name_for_listing(e, opts.classify) for e in sorted_entries]
    return "\n".join(names) + "\n"
