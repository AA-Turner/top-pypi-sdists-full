from __future__ import annotations

import io
import tarfile
from datetime import UTC, datetime
from fnmatch import fnmatch
from typing import TYPE_CHECKING

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.paths import basename, dirname, join, normalize
from matrx_ai.tools.vfs.shell.runner import CommandResult

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.core import MatrxAsyncFS


class _Flags:
    __slots__ = (
        "create",
        "extract",
        "list",
        "file",
        "gzip",
        "bzip2",
        "xz",
        "verbose",
        "chdir",
        "strip_components",
        "exclude",
    )

    def __init__(self) -> None:
        self.create: bool = False
        self.extract: bool = False
        self.list: bool = False
        self.file: str | None = None
        self.gzip: bool = False
        self.bzip2: bool = False
        self.xz: bool = False
        self.verbose: bool = False
        self.chdir: str | None = None
        self.strip_components: int = 0
        self.exclude: list[str] = []


def _parse_args(args: list[str]) -> tuple[_Flags, list[str], str | None]:
    flags = _Flags()
    paths: list[str] = []
    err: str | None = None
    i = 0
    n = len(args)
    while i < n:
        a = args[i]
        if a == "--":
            paths.extend(args[i + 1 :])
            break
        if a.startswith("--"):
            if a == "--create":
                flags.create = True
            elif a == "--extract" or a == "--get":
                flags.extract = True
            elif a == "--list":
                flags.list = True
            elif a == "--gzip" or a == "--gunzip" or a == "--ungzip":
                flags.gzip = True
            elif a == "--bzip2":
                flags.bzip2 = True
            elif a == "--xz":
                flags.xz = True
            elif a == "--verbose":
                flags.verbose = True
            elif a == "--file":
                if i + 1 >= n:
                    err = "tar: option '--file' requires an argument\n"
                    break
                flags.file = args[i + 1]
                i += 1
            elif a.startswith("--file="):
                flags.file = a.split("=", 1)[1]
            elif a == "--directory":
                if i + 1 >= n:
                    err = "tar: option '--directory' requires an argument\n"
                    break
                flags.chdir = args[i + 1]
                i += 1
            elif a.startswith("--directory="):
                flags.chdir = a.split("=", 1)[1]
            elif a.startswith("--strip-components="):
                try:
                    flags.strip_components = int(a.split("=", 1)[1])
                except ValueError:
                    err = f"tar: invalid strip count '{a}'\n"
                    break
            elif a == "--strip-components":
                if i + 1 >= n:
                    err = "tar: option '--strip-components' requires an argument\n"
                    break
                try:
                    flags.strip_components = int(args[i + 1])
                except ValueError:
                    err = f"tar: invalid strip count '{args[i + 1]}'\n"
                    break
                i += 1
            elif a.startswith("--exclude="):
                flags.exclude.append(a.split("=", 1)[1])
            elif a == "--exclude":
                if i + 1 >= n:
                    err = "tar: option '--exclude' requires an argument\n"
                    break
                flags.exclude.append(args[i + 1])
                i += 1
            else:
                err = f"tar: unrecognized option '{a}'\n"
                break
        elif a.startswith("-") and len(a) > 1:
            # Short flags, possibly clustered (e.g., -czf, czf).
            err = _parse_short_cluster(a[1:], flags, args, i)
            if err is not None and err.startswith("__SKIP_NEXT__"):
                i += int(err[len("__SKIP_NEXT__"):])
                err = None
            elif err is not None:
                break
        elif i == 0 and not a.startswith("-"):
            # Old-style first-arg cluster: "czf"
            err = _parse_short_cluster(a, flags, args, i)
            if err is not None and err.startswith("__SKIP_NEXT__"):
                i += int(err[len("__SKIP_NEXT__"):])
                err = None
            elif err is not None:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


def _parse_short_cluster(
    cluster: str, flags: _Flags, args: list[str], i: int
) -> str | None:
    consumed_extra = 0
    n = len(args)
    j = 0
    needs_file_arg = False
    while j < len(cluster):
        ch = cluster[j]
        if ch == "c":
            flags.create = True
        elif ch == "x":
            flags.extract = True
        elif ch == "t":
            flags.list = True
        elif ch == "z":
            flags.gzip = True
        elif ch == "j":
            flags.bzip2 = True
        elif ch == "J":
            flags.xz = True
        elif ch == "v":
            flags.verbose = True
        elif ch == "f":
            needs_file_arg = True
        elif ch == "C":
            # -C must be followed by a directory.
            if i + 1 + consumed_extra >= n:
                return "tar: option '-C' requires an argument\n"
            flags.chdir = args[i + 1 + consumed_extra]
            consumed_extra += 1
        else:
            return f"tar: invalid option -- '{ch}'\n"
        j += 1
    if needs_file_arg:
        if i + 1 + consumed_extra >= n:
            return "tar: option '-f' requires an argument\n"
        flags.file = args[i + 1 + consumed_extra]
        consumed_extra += 1
    if consumed_extra:
        return f"__SKIP_NEXT__{consumed_extra}"
    return None


def _format_member(info: tarfile.TarInfo) -> str:
    # tar -tv style: -rw-r--r-- root/root 12 2026-05-07 17:53 path
    if info.isdir():
        type_char = "d"
    elif info.issym():
        type_char = "l"
    else:
        type_char = "-"

    perms_bits = info.mode & 0o777
    perms = ""
    for shift in (6, 3, 0):
        b = (perms_bits >> shift) & 0b111
        perms += "r" if b & 0b100 else "-"
        perms += "w" if b & 0b010 else "-"
        perms += "x" if b & 0b001 else "-"

    user = info.uname or str(info.uid)
    group = info.gname or str(info.gid)
    user_group = f"{user}/{group}"
    size = info.size
    mtime = datetime.fromtimestamp(info.mtime, tz=UTC).strftime("%Y-%m-%d %H:%M")
    return f"{type_char}{perms} {user_group:<13s} {size:>9d} {mtime} {info.name}\n"


def _excluded(name: str, patterns: list[str]) -> bool:
    for p in patterns:
        if fnmatch(name, p) or fnmatch(basename(name), p):
            return True
    return False


async def _walk_for_archive(
    vfs: MatrxAsyncFS, src: str, exclude: list[str]
) -> list[tuple[str, dict]]:
    """Return list of (absolute_path, info_dict)."""
    results: list[tuple[str, dict]] = []
    info = await vfs._info(src)
    rel_root = basename(src) or src
    if info["type"] == "directory":
        results.append((src, info))
        async for cur, dirs, files in vfs._walk(src, topdown=True):
            for d in sorted(dirs):
                full = join(cur, d)
                if _excluded(full, exclude):
                    continue
                ds = await vfs._info(full)
                results.append((full, ds))
            for f in sorted(files):
                full = join(cur, f)
                if _excluded(full, exclude):
                    continue
                fs = await vfs._info(full)
                results.append((full, fs))
    else:
        results.append((src, info))
    _ = rel_root
    return results


def _archive_name(src: str, abs_path: str, base_root: str) -> str:
    """Compute the in-archive name for `abs_path` when source label is `src`.
    Mirrors GNU tar's preserved leading path of src."""
    # If src is absolute, GNU tar normally strips leading "/" with a warning;
    # we strip silently (conservative behavior).
    rel_under_src = abs_path[len(base_root):].lstrip("/")
    src_clean = src.lstrip("/")
    if rel_under_src:
        return f"{src_clean}/{rel_under_src}" if src_clean else rel_under_src
    return src_clean if src_clean else basename(abs_path)


async def _do_create(
    ctx: CommandContext, flags: _Flags, sources: list[str]
) -> CommandResult:
    if not sources:
        return fail(2, encode("tar: Cowardly refusing to create an empty archive\ntar: Exiting with failure status due to previous errors\n"))

    if flags.bzip2 or flags.xz:
        kind = "bzip2" if flags.bzip2 else "xz"
        return fail(2, encode(f"tar: {kind} compression not supported in matrx-ai vfs\n"))

    base = ctx.env.cwd if flags.chdir is None else resolve_cwd(ctx.env, flags.chdir)

    buf = io.BytesIO()
    mode = "w:gz" if flags.gzip else "w"
    stdout = bytearray()
    stderr = bytearray()
    exit_code = 0

    with tarfile.open(fileobj=buf, mode=mode) as tar:
        for src_label in sources:
            src_resolved = (
                normalize(join(base, src_label))
                if not src_label.startswith("/")
                else normalize(src_label)
            )
            if not await ctx.vfs._exists(src_resolved):
                stderr.extend(
                    encode(f"tar: {src_label}: Cannot stat: No such file or directory\n")
                )
                exit_code = 2
                continue

            entries = await _walk_for_archive(ctx.vfs, src_resolved, flags.exclude)
            for abs_path, info in entries:
                arc_name = _archive_name(src_label, abs_path, src_resolved)
                if abs_path == src_resolved:
                    arc_name = src_label.lstrip("./").lstrip("/")
                    if not arc_name:
                        arc_name = basename(abs_path)
                ti = tarfile.TarInfo(name=arc_name)
                mtime = info.get("mtime")
                if isinstance(mtime, datetime):
                    ti.mtime = int(mtime.timestamp())
                else:
                    ti.mtime = int(datetime.now(UTC).timestamp())
                ti.uid = info.get("uid", 0)
                ti.gid = info.get("gid", 0)
                ti.uname = "root"
                ti.gname = "root"

                if info["type"] == "directory":
                    ti.type = tarfile.DIRTYPE
                    ti.mode = info.get("mode", 0o755) & 0o777
                    ti.size = 0
                    tar.addfile(ti)
                elif info["type"] == "link":
                    ti.type = tarfile.SYMTYPE
                    ti.mode = info.get("mode", 0o777) & 0o777
                    ti.linkname = info.get("symlink_target") or ""
                    ti.size = 0
                    tar.addfile(ti)
                else:
                    ti.type = tarfile.REGTYPE
                    ti.mode = info.get("mode", 0o644) & 0o777
                    data = await ctx.vfs._cat_file(abs_path)
                    ti.size = len(data)
                    tar.addfile(ti, io.BytesIO(data))

                if flags.verbose:
                    stdout.extend(encode(f"{arc_name}\n"))

    archive_bytes = buf.getvalue()

    if flags.file is None or flags.file == "-":
        # stdout
        out = bytes(stdout) + archive_bytes
        return CommandResult(stdout=out, stderr=bytes(stderr), exit_code=exit_code)

    out_path = resolve_cwd(ctx.env, flags.file)
    # Ensure parent dir exists.
    parent = dirname(out_path)
    if parent and parent != "/" and not await ctx.vfs._exists(parent):
        await ctx.vfs._makedirs(parent, exist_ok=True)
    await ctx.vfs._pipe_file(out_path, archive_bytes)

    if exit_code != 0:
        stderr.extend(encode("tar: Exiting with failure status due to previous errors\n"))
        return fail(exit_code, stdout=bytes(stdout), stderr=bytes(stderr))
    return CommandResult(stdout=bytes(stdout), stderr=bytes(stderr), exit_code=0)


async def _read_archive(
    ctx: CommandContext, flags: _Flags
) -> tuple[bytes | None, bytes]:
    """Returns (archive_bytes, error_bytes)."""
    if flags.file is None or flags.file == "-":
        return ctx.stdin, b""
    in_path = resolve_cwd(ctx.env, flags.file)
    if not await ctx.vfs._exists(in_path):
        return None, encode(
            f"tar: {flags.file}: Cannot open: No such file or directory\n"
            "tar: Error is not recoverable: exiting now\n"
        )
    if await ctx.vfs._isdir(in_path):
        return None, encode(
            f"tar: {flags.file}: Cannot open: Is a directory\n"
            "tar: Error is not recoverable: exiting now\n"
        )
    return await ctx.vfs._cat_file(in_path), b""


def _open_for_read(
    archive: bytes, flags: _Flags
) -> tarfile.TarFile | None:
    buf = io.BytesIO(archive)
    if flags.gzip:
        try:
            return tarfile.open(fileobj=buf, mode="r:gz")
        except (tarfile.ReadError, OSError):
            return None
    try:
        return tarfile.open(fileobj=buf, mode="r:*")
    except (tarfile.ReadError, OSError):
        return None


def _strip_components(name: str, n: int) -> str | None:
    if n <= 0:
        return name
    parts = [p for p in name.split("/") if p]
    if len(parts) <= n:
        return None
    return "/".join(parts[n:])


async def _do_list(ctx: CommandContext, flags: _Flags) -> CommandResult:
    archive, err_b = await _read_archive(ctx, flags)
    if archive is None:
        return fail(2, err_b)

    tar = _open_for_read(archive, flags)
    if tar is None:
        return fail(
            2,
            encode(
                "tar: This does not look like a tar archive\n"
                "tar: Exiting with failure status due to previous errors\n"
            ),
        )

    out = bytearray()
    with tar:
        for member in tar.getmembers():
            if _excluded(member.name, flags.exclude):
                continue
            if flags.verbose:
                out.extend(encode(_format_member(member)))
            else:
                name = member.name
                if member.isdir() and not name.endswith("/"):
                    name += "/"
                out.extend(encode(name + "\n"))
    return ok(stdout=bytes(out))


async def _do_extract(ctx: CommandContext, flags: _Flags) -> CommandResult:
    archive, err_b = await _read_archive(ctx, flags)
    if archive is None:
        return fail(2, err_b)

    tar = _open_for_read(archive, flags)
    if tar is None:
        return fail(
            2,
            encode(
                "tar: This does not look like a tar archive\n"
                "tar: Exiting with failure status due to previous errors\n"
            ),
        )

    base = ctx.env.cwd if flags.chdir is None else resolve_cwd(ctx.env, flags.chdir)
    if flags.chdir is not None and not await ctx.vfs._exists(base):
        await ctx.vfs._makedirs(base, exist_ok=True)

    out = bytearray()
    stderr = bytearray()
    exit_code = 0

    with tar:
        for member in tar.getmembers():
            if _excluded(member.name, flags.exclude):
                continue
            stripped = _strip_components(member.name, flags.strip_components)
            if stripped is None or stripped == "":
                continue

            target = normalize(join(base, stripped))

            if flags.verbose:
                out.extend(encode(member.name + "\n"))

            if member.isdir():
                await ctx.vfs._makedirs(target, exist_ok=True)
            elif member.isreg():
                parent = dirname(target)
                if parent and parent != "/" and not await ctx.vfs._exists(parent):
                    await ctx.vfs._makedirs(parent, exist_ok=True)
                f = tar.extractfile(member)
                data = f.read() if f is not None else b""
                await ctx.vfs._pipe_file(target, data)
            elif member.issym():
                parent = dirname(target)
                if parent and parent != "/" and not await ctx.vfs._exists(parent):
                    await ctx.vfs._makedirs(parent, exist_ok=True)
                if await ctx.vfs._exists(target):
                    await ctx.vfs._rm(target)
                await ctx.vfs._symlink(member.linkname, target)
            # Other types (links, etc.) ignored.

    if exit_code != 0:
        return fail(exit_code, stdout=bytes(out), stderr=bytes(stderr))
    return CommandResult(stdout=bytes(out), stderr=bytes(stderr), exit_code=0)


@register("tar")
async def cmd_tar(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(2, encode(err))

    modes_set = sum([flags.create, flags.extract, flags.list])
    if modes_set == 0:
        return fail(
            2,
            encode(
                "tar: You must specify one of the '-Acdtrux', '--delete' or "
                "'--test-label' options\n"
                "Try 'tar --help' or 'tar --usage' for more information.\n"
            ),
        )
    if modes_set > 1:
        return fail(2, encode("tar: You may not specify more than one operation\n"))

    if flags.create:
        return await _do_create(ctx, flags, paths)
    if flags.list:
        return await _do_list(ctx, flags)
    return await _do_extract(ctx, flags)
