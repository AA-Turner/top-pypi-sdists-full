from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import format_size_human
from matrx_ai.tools.vfs.shell.runner import CommandResult

# Synthesized constants describing the single virtual filesystem.
_FS_NAME = "vfs"
_FS_MOUNT = "/"
_TOTAL_BYTES = 100 * 1024 * 1024 * 1024  # 100 GiB
_USED_BYTES = 8 * 1024 * 1024 * 1024  # 8 GiB
_AVAIL_BYTES = _TOTAL_BYTES - _USED_BYTES
_TOTAL_INODES = 9_999_999
_USED_INODES = 1_000
_FREE_INODES = _TOTAL_INODES - _USED_INODES


class _DfOpts:
    __slots__ = ("human", "human_si", "inodes", "block_size", "block_size_arg", "show_all", "type_filter")

    def __init__(self) -> None:
        self.human: bool = False
        self.human_si: bool = False
        self.inodes: bool = False
        self.block_size: int = 1024  # default 1K-blocks
        self.block_size_arg: str | None = None
        self.show_all: bool = False
        self.type_filter: str | None = None


def _parse_args(args: list[str]) -> tuple[_DfOpts, list[str], CommandResult | None]:
    opts = _DfOpts()
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
        if a == "--human-readable":
            opts.human = True
            i += 1
            continue
        if a == "--si":
            opts.human_si = True
            opts.human = True
            i += 1
            continue
        if a == "--inodes":
            opts.inodes = True
            i += 1
            continue
        if a == "--all":
            opts.show_all = True
            i += 1
            continue
        if a.startswith("--block-size="):
            try:
                opts.block_size = int(a.split("=", 1)[1])
            except ValueError:
                return opts, paths, fail(1, encode("df: invalid --block-size argument\n"))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1 and a != "-":
            for ch in a[1:]:
                if ch == "h":
                    opts.human = True
                elif ch == "H":
                    opts.human_si = True
                    opts.human = True
                elif ch == "i":
                    opts.inodes = True
                elif ch == "k":
                    opts.block_size = 1024
                elif ch == "B":
                    pass  # consume next arg
                elif ch == "T":
                    pass
                elif ch == "a":
                    opts.show_all = True
                elif ch == "P":
                    pass
                else:
                    return opts, paths, fail(
                        1,
                        encode(
                            f"df: invalid option -- '{ch}'\nTry 'df --help' for more information.\n"
                        ),
                    )
            i += 1
            continue
        paths.append(a)
        i += 1
    return opts, paths, None


def _format_block_size(b: int, opts: _DfOpts) -> str:
    if opts.human:
        return format_size_human(b)
    units = (b + opts.block_size - 1) // opts.block_size
    return str(units)


def _row_inodes() -> tuple[list[str], list[str]]:
    headers = ["Filesystem", "Inodes", "IUsed", "IFree", "IUse%", "Mounted on"]
    use_pct = (
        f"{int(round(_USED_INODES * 100 / _TOTAL_INODES))}%" if _TOTAL_INODES else "-"
    )
    row = [
        _FS_NAME,
        str(_TOTAL_INODES),
        str(_USED_INODES),
        str(_FREE_INODES),
        use_pct,
        _FS_MOUNT,
    ]
    return headers, row


def _row_blocks(opts: _DfOpts) -> tuple[list[str], list[str]]:
    if opts.human:
        size_label = "Size"
        used_label = "Used"
        avail_label = "Avail"
    else:
        size_label = f"{opts.block_size // 1024 if opts.block_size >= 1024 else 1}K-blocks"
        if opts.block_size != 1024:
            size_label = f"{opts.block_size}-blocks"
        used_label = "Used"
        avail_label = "Available"
    headers = ["Filesystem", size_label, used_label, avail_label, "Use%", "Mounted on"]
    use_pct = (
        f"{int(round(_USED_BYTES * 100 / _TOTAL_BYTES))}%" if _TOTAL_BYTES else "-"
    )
    row = [
        _FS_NAME,
        _format_block_size(_TOTAL_BYTES, opts),
        _format_block_size(_USED_BYTES, opts),
        _format_block_size(_AVAIL_BYTES, opts),
        use_pct,
        _FS_MOUNT,
    ]
    return headers, row


def _render_table(headers: list[str], rows: list[list[str]]) -> str:
    # Compute column widths: max of header and any row in that column.
    cols = len(headers)
    widths = [len(headers[c]) for c in range(cols)]
    for row in rows:
        for c in range(cols):
            if len(row[c]) > widths[c]:
                widths[c] = len(row[c])
    lines: list[str] = []

    def fmt_row(cells: list[str]) -> str:
        # GNU df: filesystem column left-justified, last column left, numeric cols right.
        parts: list[str] = []
        for c, cell in enumerate(cells):
            if c == 0:
                parts.append(cell.ljust(widths[c]))
            elif c == cols - 1:
                parts.append(cell)
            else:
                parts.append(cell.rjust(widths[c]))
        return " ".join(parts)

    lines.append(fmt_row(headers))
    for row in rows:
        lines.append(fmt_row(row))
    return "\n".join(lines) + "\n"


@register("df")
async def cmd_df(ctx: CommandContext) -> CommandResult:
    opts, paths, err = _parse_args(ctx.args)
    if err is not None:
        return err

    err_out = bytearray()
    exit_code = 0

    # Validate any explicit paths exist.
    if paths:
        for display in paths:
            abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
            if not await ctx.vfs._exists(abs_path):
                err_out.extend(
                    encode(f"df: {display}: No such file or directory\n")
                )
                exit_code = 1
        if exit_code != 0 and len(paths) == 1:
            return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=1)

    if opts.inodes:
        headers, row = _row_inodes()
    else:
        headers, row = _row_blocks(opts)

    rows = [row]
    out = _render_table(headers, rows)

    return CommandResult(stdout=encode(out), stderr=bytes(err_out), exit_code=exit_code)
