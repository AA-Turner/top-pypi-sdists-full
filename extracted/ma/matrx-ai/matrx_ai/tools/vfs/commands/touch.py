from __future__ import annotations

from datetime import UTC, datetime

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import from_oserror
from matrx_ai.tools.vfs.paths import basename, dirname
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _parse_date(spec: str) -> datetime | None:
    spec = spec.strip()
    if not spec:
        return None
    if spec.startswith("@"):
        try:
            return datetime.fromtimestamp(float(spec[1:]), tz=UTC)
        except ValueError:
            return None
    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            dt = datetime.strptime(spec, fmt)
            return dt.replace(tzinfo=UTC)
        except ValueError:
            continue
    return None


def _parse_t_stamp(spec: str) -> datetime | None:
    # [[CC]YY]MMDDhhmm[.SS]
    s = spec
    seconds = 0
    if "." in s:
        s, ss = s.split(".", 1)
        try:
            seconds = int(ss)
        except ValueError:
            return None
    if len(s) == 8:  # MMDDhhmm
        year = datetime.now(UTC).year
        month, day, hour, minute = int(s[0:2]), int(s[2:4]), int(s[4:6]), int(s[6:8])
    elif len(s) == 10:  # YYMMDDhhmm
        yy = int(s[0:2])
        year = 2000 + yy if yy < 69 else 1900 + yy
        month, day, hour, minute = int(s[2:4]), int(s[4:6]), int(s[6:8]), int(s[8:10])
    elif len(s) == 12:  # CCYYMMDDhhmm
        year = int(s[0:4])
        month, day, hour, minute = int(s[4:6]), int(s[6:8]), int(s[8:10]), int(s[10:12])
    else:
        return None
    try:
        return datetime(year, month, day, hour, minute, seconds, tzinfo=UTC)
    except ValueError:
        return None


def _parse_args(args: list[str]) -> tuple[dict[str, object], list[str], str | None]:
    flags: dict[str, object] = {
        "no_create": False,
        "atime_only": False,
        "mtime_only": False,
        "date": None,
        "tstamp": None,
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
        if a == "-c" or a == "--no-create":
            flags["no_create"] = True
        elif a == "-a":
            flags["atime_only"] = True
        elif a == "-m":
            flags["mtime_only"] = True
        elif a == "-d" or a == "--date":
            if i + 1 >= n:
                err = "touch: option requires an argument -- 'd'\n"
                break
            flags["date"] = args[i + 1]
            i += 1
        elif a.startswith("--date="):
            flags["date"] = a.split("=", 1)[1]
        elif a == "-t":
            if i + 1 >= n:
                err = "touch: option requires an argument -- 't'\n"
                break
            flags["tstamp"] = args[i + 1]
            i += 1
        elif a.startswith("-") and len(a) > 1 and a != "-":
            if a[1] == "-":
                err = f"touch: unrecognized option '{a}'\n"
                break
            for ch in a[1:]:
                if ch == "c":
                    flags["no_create"] = True
                elif ch == "a":
                    flags["atime_only"] = True
                elif ch == "m":
                    flags["mtime_only"] = True
                else:
                    err = f"touch: invalid option -- '{ch}'\n"
                    break
            if err:
                break
        else:
            paths.append(a)
        i += 1
    return flags, paths, err


@register("touch")
async def cmd_touch(ctx: CommandContext) -> CommandResult:
    flags, paths, err = _parse_args(ctx.args)
    if err is not None:
        return fail(1, encode(err))

    if not paths:
        return fail(1, encode("touch: missing file operand\nTry 'touch --help' for more information.\n"))

    no_create = bool(flags["no_create"])

    explicit_dt: datetime | None = None
    if flags["date"] is not None:
        dt = _parse_date(str(flags["date"]))
        if dt is None:
            return fail(1, encode(f"touch: invalid date format '{flags['date']}'\n"))
        explicit_dt = dt
    if flags["tstamp"] is not None:
        dt = _parse_t_stamp(str(flags["tstamp"]))
        if dt is None:
            return fail(1, encode(f"touch: invalid date format '{flags['tstamp']}'\n"))
        explicit_dt = dt

    atime_only = bool(flags["atime_only"])
    mtime_only = bool(flags["mtime_only"])
    # If neither -a nor -m given, both are updated; if both flags given, both updated.
    update_atime = (not mtime_only) or atime_only
    update_mtime = (not atime_only) or mtime_only

    stderr = b""
    exit_code = 0

    for p in paths:
        target = resolve_cwd(ctx.env, p)
        existed = await ctx.vfs._exists(target)
        if not existed and no_create:
            continue
        if not existed:
            # Need parent to exist.
            parent = dirname(target)
            if parent != "/" and not await ctx.vfs._exists(parent):
                stderr += encode(
                    f"touch: cannot touch '{p}': No such file or directory\n"
                )
                exit_code = 1
                continue
            if not await ctx.vfs._isdir(parent):
                stderr += encode(
                    f"touch: cannot touch '{p}': Not a directory\n"
                )
                exit_code = 1
                continue
            try:
                await ctx.vfs._touch(target, truncate=False)
            except OSError as e:
                stderr += encode(from_oserror("touch", p, e))
                exit_code = 1
                continue
            if explicit_dt is not None:
                # Apply explicit timestamp via backend update.
                inode = await ctx.vfs._resolve(target)
                fields: dict[str, object] = {}
                if update_atime:
                    fields["atime"] = explicit_dt
                if update_mtime:
                    fields["mtime"] = explicit_dt
                if fields:
                    await ctx.vfs.backend.update_inode(inode.id, **fields)
        else:
            # Update timestamps only — never truncate.
            try:
                inode = await ctx.vfs._resolve(target)
            except OSError as e:
                stderr += encode(from_oserror("touch", p, e))
                exit_code = 1
                continue
            now = datetime.now(UTC)
            ts = explicit_dt if explicit_dt is not None else now
            fields = {}
            if update_atime:
                fields["atime"] = ts
            if update_mtime:
                fields["mtime"] = ts
            if fields:
                # basename of `name=basename` is unchanged; just update times.
                # Avoid passing 'name' to keep current name.
                _ = basename  # silence unused if path manipulations needed
                await ctx.vfs.backend.update_inode(inode.id, **fields)

    return ok(stderr=stderr) if exit_code == 0 else fail(exit_code, stderr=stderr)
