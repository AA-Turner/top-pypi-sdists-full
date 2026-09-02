from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import format_size_human
from matrx_ai.tools.vfs.paths import join
from matrx_ai.tools.vfs.shell.runner import CommandResult


class _DuOpts:
    __slots__ = (
        "human",
        "summarize",
        "all_files",
        "total",
        "max_depth",
        "block_size",
        "bytes_mode",
        "kibibytes",
        "si",
    )

    def __init__(self) -> None:
        self.human: bool = False
        self.summarize: bool = False
        self.all_files: bool = False
        self.total: bool = False
        self.max_depth: int | None = None
        self.block_size: int = 1024  # default `du` reports 1 KiB blocks
        self.bytes_mode: bool = False
        self.kibibytes: bool = False
        self.si: bool = False


def _parse_args(args: list[str]) -> tuple[_DuOpts, list[str], CommandResult | None]:
    opts = _DuOpts()
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
        if a.startswith("--max-depth="):
            try:
                opts.max_depth = int(a.split("=", 1)[1])
            except ValueError:
                return opts, paths, fail(1, encode(f"du: invalid maximum depth '{a}'\n"))
            i += 1
            continue
        if a == "--max-depth":
            if i + 1 >= len(args):
                return opts, paths, fail(1, encode("du: option requires an argument\n"))
            try:
                opts.max_depth = int(args[i + 1])
            except ValueError:
                return opts, paths, fail(1, encode(f"du: invalid maximum depth '{args[i + 1]}'\n"))
            i += 2
            continue
        if a == "--human-readable":
            opts.human = True
            i += 1
            continue
        if a == "--summarize":
            opts.summarize = True
            i += 1
            continue
        if a == "--all":
            opts.all_files = True
            i += 1
            continue
        if a == "--total":
            opts.total = True
            i += 1
            continue
        if a == "--bytes":
            opts.bytes_mode = True
            opts.block_size = 1
            i += 1
            continue
        if a == "--si":
            opts.si = True
            opts.human = True
            i += 1
            continue
        if a.startswith("--block-size="):
            try:
                opts.block_size = int(a.split("=", 1)[1])
            except ValueError:
                return opts, paths, fail(1, encode("du: invalid --block-size argument\n"))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1 and a != "-":
            j = 1
            while j < len(a):
                ch = a[j]
                if ch == "h":
                    opts.human = True
                elif ch == "s":
                    opts.summarize = True
                elif ch == "a":
                    opts.all_files = True
                elif ch == "c":
                    opts.total = True
                elif ch == "k":
                    opts.kibibytes = True
                    opts.block_size = 1024
                elif ch == "b":
                    opts.bytes_mode = True
                    opts.block_size = 1
                elif ch == "B":
                    # -B SIZE
                    rest = a[j + 1 :]
                    if rest:
                        try:
                            opts.block_size = int(rest)
                        except ValueError:
                            return opts, paths, fail(1, encode("du: invalid --block-size\n"))
                        break
                    if i + 1 >= len(args):
                        return opts, paths, fail(1, encode("du: option requires argument\n"))
                    try:
                        opts.block_size = int(args[i + 1])
                    except ValueError:
                        return opts, paths, fail(1, encode("du: invalid --block-size\n"))
                    i += 1
                    break
                elif ch == "d":
                    rest = a[j + 1 :]
                    if rest:
                        try:
                            opts.max_depth = int(rest)
                        except ValueError:
                            return opts, paths, fail(
                                1, encode(f"du: invalid maximum depth '{rest}'\n")
                            )
                        break
                    if i + 1 >= len(args):
                        return opts, paths, fail(1, encode("du: option requires argument\n"))
                    try:
                        opts.max_depth = int(args[i + 1])
                    except ValueError:
                        return opts, paths, fail(
                            1, encode(f"du: invalid maximum depth '{args[i + 1]}'\n")
                        )
                    i += 1
                    break
                elif ch == "S" or ch == "x" or ch == "L" or ch == "P":
                    pass
                else:
                    return opts, paths, fail(
                        1,
                        encode(
                            f"du: invalid option -- '{ch}'\nTry 'du --help' for more information.\n"
                        ),
                    )
                j += 1
            i += 1
            continue
        paths.append(a)
        i += 1
    return opts, paths, None


def _format_size(size_bytes: int, opts: _DuOpts) -> str:
    if opts.human:
        return format_size_human(size_bytes)
    blocks = (size_bytes + opts.block_size - 1) // opts.block_size if size_bytes > 0 else 0
    return str(blocks)


async def _walk_for_du(
    vfs, root: str, *, max_depth: int | None, current_depth: int = 0
) -> tuple[list[tuple[str, int, str]], int]:
    # Returns (entries, total_bytes_in_subtree).
    # entries is a list of (path, size_bytes, type) in post-order.
    try:
        info = await vfs._info(root)
    except FileNotFoundError:
        return [], 0
    except OSError:
        return [], 0

    kind = info.get("type", "file")
    if kind != "directory":
        return [(root, int(info.get("size", 0) or 0), "file")], int(info.get("size", 0) or 0)

    entries: list[tuple[str, int, str]] = []
    subtree_bytes = 0

    children = await vfs._ls(root, detail=True)
    children.sort(key=lambda c: c.get("name") or "")
    for child in children:
        cpath = child["name"]
        ctype = child.get("type", "file")
        if ctype == "directory":
            sub_entries, sub_bytes = await _walk_for_du(
                vfs, cpath, max_depth=max_depth, current_depth=current_depth + 1
            )
            entries.extend(sub_entries)
            subtree_bytes += sub_bytes
        else:
            csize = int(child.get("size", 0) or 0)
            subtree_bytes += csize
            entries.append((cpath, csize, "file"))

    entries.append((root, subtree_bytes, "directory"))
    return entries, subtree_bytes


def _filter_for_output(
    entries: list[tuple[str, int, str]],
    root: str,
    opts: _DuOpts,
) -> list[tuple[str, int, str]]:
    if opts.summarize:
        # Only the top-level entry.
        for path, size, kind in reversed(entries):
            if path == root:
                return [(path, size, kind)]
        return entries[-1:] if entries else []

    # Compute relative depth from root for each entry to apply --max-depth.
    def depth(path: str) -> int:
        if path == root:
            return 0
        if root == "/":
            tail = path
        else:
            tail = path[len(root):]
        return tail.count("/")

    out: list[tuple[str, int, str]] = []
    for path, size, kind in entries:
        if kind != "directory" and not opts.all_files and path != root:
            continue
        if opts.max_depth is not None and depth(path) > opts.max_depth:
            continue
        out.append((path, size, kind))
    return out


@register("du")
async def cmd_du(ctx: CommandContext) -> CommandResult:
    opts, raw_paths, err = _parse_args(ctx.args)
    if err is not None:
        return err

    if not raw_paths:
        raw_paths = [ctx.env.cwd or "."]

    out = bytearray()
    err_out = bytearray()
    exit_code = 0
    grand_total = 0

    for display in raw_paths:
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
        if not await ctx.vfs._exists(abs_path):
            err_out.extend(
                encode(f"du: cannot access '{display}': No such file or directory\n")
            )
            exit_code = 1
            continue
        entries, total_bytes = await _walk_for_du(
            ctx.vfs, abs_path, max_depth=opts.max_depth
        )
        # Reroute the recorded root entry to the displayed name.
        rerouted: list[tuple[str, int, str]] = []
        for p, s, k in entries:
            if p == abs_path:
                rerouted.append((display, s, k))
            else:
                # rewrite prefix abs_path -> display
                if abs_path != "/" and p.startswith(abs_path + "/"):
                    rerouted.append((display + p[len(abs_path):], s, k))
                else:
                    rerouted.append((p, s, k))

        filtered = _filter_for_output(rerouted, display, opts)
        for path, size, _kind in filtered:
            size_str = _format_size(size, opts)
            out.extend(encode(f"{size_str}\t{path}\n"))
        grand_total += total_bytes

    if opts.total:
        out.extend(encode(f"{_format_size(grand_total, opts)}\ttotal\n"))

    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)


def _join(*parts: str) -> str:
    return join(*parts)
