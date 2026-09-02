from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from matrx_ai.tools.vfs.mimicry.dates import format_iso_nanos
from matrx_ai.tools.vfs.mimicry.ls import _perm_string

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.mimicry import InodeView


_TYPE_DESCRIPTIONS = {
    "file": "regular file",
    "dir": "directory",
    "link": "symbolic link",
}


def _type_description(inode: InodeView) -> str:
    itype = inode["type"]
    if itype == "file" and inode["size"] == 0:
        return "regular empty file"
    return _TYPE_DESCRIPTIONS.get(itype, "regular file")


def _fake_inode_number(name: str) -> int:
    # Deterministic fake inode number derived from the entry's name. Phase A1
    # may pass a UUID through `name` or a future field; we hash whatever we
    # have so tests can still assert determinism without coupling to A1.
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % 9999999


def _blocks_for(size: int) -> int:
    # GNU stat reports 512-byte blocks. Round up to nearest 4 KiB filesystem block,
    # then express as 512-byte units.
    if size == 0:
        return 0
    return ((size + 4095) // 4096) * 8


def format_stat_default(inode: InodeView, path: str) -> str:
    size = inode["size"]
    blocks = _blocks_for(size)
    type_desc = _type_description(inode)
    fake_inode = _fake_inode_number(inode["name"])
    sym_mode = _perm_string(inode["type"], inode["mode"])
    octal_mode = f"{inode['mode'] & 0o7777:04o}"

    access = format_iso_nanos(inode["atime"])
    modify = format_iso_nanos(inode["mtime"])
    change = format_iso_nanos(inode["ctime"])
    birth = format_iso_nanos(inode["ctime"])

    nlink = inode["nlink"]
    uid = inode["uid"]
    gid = inode["gid"]
    user = inode["user"]
    group = inode["group"]

    lines = [
        f"  File: {path}",
        f"  Size: {size}\t\tBlocks: {blocks}          IO Block: 4096   {type_desc}",
        f"Device: 254,0\tInode: {fake_inode}      Links: {nlink}",
        f"Access: ({octal_mode}/{sym_mode})  Uid: ( {uid:>4d}/{user:>8s})   "
        f"Gid: ( {gid:>4d}/{group:>8s})",
        f"Access: {access}",
        f"Modify: {modify}",
        f"Change: {change}",
        f" Birth: {birth}",
    ]
    return "\n".join(lines) + "\n"


def format_stat_format_string(inode: InodeView, fmt: str) -> str:
    sym_mode = _perm_string(inode["type"], inode["mode"])
    octal_mode = f"{inode['mode'] & 0o777:o}"
    fake_inode = _fake_inode_number(inode["name"])

    out: list[str] = []
    i = 0
    while i < len(fmt):
        ch = fmt[i]
        if ch == "%" and i + 1 < len(fmt):
            spec = fmt[i + 1]
            i += 2
            match spec:
                case "n":
                    out.append(inode["name"])
                case "s":
                    out.append(str(inode["size"]))
                case "a":
                    out.append(octal_mode)
                case "A":
                    out.append(sym_mode)
                case "U":
                    out.append(inode["user"])
                case "G":
                    out.append(inode["group"])
                case "u":
                    out.append(str(inode["uid"]))
                case "g":
                    out.append(str(inode["gid"]))
                case "F":
                    out.append(_type_description(inode))
                case "y":
                    out.append(format_iso_nanos(inode["mtime"]))
                case "Y":
                    out.append(str(int(inode["mtime"])))
                case "i":
                    out.append(str(fake_inode))
                case "h":
                    out.append(str(inode["nlink"]))
                case "%":
                    out.append("%")
                case "n_":
                    out.append("\n")
                case _:
                    out.append("%" + spec)
        elif ch == "\\" and i + 1 < len(fmt):
            esc = fmt[i + 1]
            i += 2
            match esc:
                case "n":
                    out.append("\n")
                case "t":
                    out.append("\t")
                case "\\":
                    out.append("\\")
                case _:
                    out.append("\\" + esc)
        else:
            out.append(ch)
            i += 1
    return "".join(out)
