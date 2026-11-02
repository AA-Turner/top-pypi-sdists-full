"""unpack the updater archive into staging: no path escapes, entry and size caps."""

from __future__ import annotations
import contextlib
import os
import stat
import unicodedata
from pathlib import Path
from probe.service.updater.app.errors import InstallError
#: The archive (7 MB in 0.1.52) and what it unpacks to, at most.
ARCHIVE_MAX_BYTES = 256 * 1024 * 1024
UNPACKED_MAX_BYTES = 1024 * 1024 * 1024
MAX_ENTRIES = 20_000


# -- the archive -------------------------------------------------------------------


def _parts(name: str) -> tuple[str, ...]:
    if "\0" in name or "\\" in name:
        raise InstallError(f"the archive has an unsafe name {name!r}")
    if name.startswith("/"):
        raise InstallError(f"the archive has an absolute path {name!r}")
    parts = tuple(p for p in name.split("/") if p not in ("", "."))
    if ".." in parts:
        raise InstallError(f"the archive has a path outside it {name!r}")
    return parts


def _fold(parts: tuple[str, ...]) -> tuple[str, ...]:
    # APFS and HFS+ compare names case- and normalization-insensitively by default.
    return tuple(unicodedata.normalize("NFD", p).casefold() for p in parts)


def _real_dir(path: Path) -> bool:
    try:
        return stat.S_ISDIR(os.lstat(path).st_mode)
    except OSError:
        return False


def _mkdir(path: Path) -> None:
    # 0755 whatever the umask: every user of the Mac launches the app.
    os.mkdir(path, 0o700)
    os.chmod(path, 0o755)


def extract(archive: Path, root: Path) -> None:
    """Unpack a Tauri updater archive (`Probe.app/...`) into `root`, the
    bundle's own folder (its first path component dropped, as the updater's
    macOS install does), refusing anything unsafe. `root` exists and is empty."""
    import tarfile
    import zlib

    seen: set = set()
    links: set = set()
    top: str | None = None
    count = total = 0
    try:
        with tarfile.open(archive, mode="r:gz") as tar:
            for member in tar:
                count += 1
                if count > MAX_ENTRIES:
                    raise InstallError(f"the archive has more than {MAX_ENTRIES} entries")
                parts = _parts(member.name)
                if not parts:
                    continue
                if top is None:
                    if not parts[0].endswith(".app"):
                        raise InstallError(f"the archive holds {parts[0]!r}, not an app bundle")
                    top = parts[0]
                elif parts[0] != top:
                    raise InstallError("the archive holds more than one top-level folder")
                rel = parts[1:]
                if not rel:
                    if not member.isdir():
                        raise InstallError("the archive's bundle is not a folder")
                    continue
                key = _fold(rel)
                if key in seen:
                    raise InstallError(f"the archive has {'/'.join(rel)!r} twice")
                for i in range(1, len(rel)):
                    if _fold(rel[:i]) in links:
                        raise InstallError(f"the archive writes through the link {'/'.join(rel[:i])!r}")
                seen.add(key)
                target = root.joinpath(*rel)
                parent = target.parent
                # Parents the archive did not list: made here, each a real folder.
                for i in range(1, len(rel)):
                    step = root.joinpath(*rel[:i])
                    if not _real_dir(step):
                        if os.path.lexists(step):
                            raise InstallError(f"{'/'.join(rel[:i])!r} is not a folder")
                        _mkdir(step)
                if not _real_dir(parent):
                    raise InstallError(f"{'/'.join(rel[:-1])!r} is not a folder")
                if member.isdir():
                    if os.path.lexists(target):
                        if not _real_dir(target):
                            raise InstallError(f"{'/'.join(rel)!r} is not a folder")
                    else:
                        _mkdir(target)
                elif member.isreg():
                    total += member.size
                    if total > UNPACKED_MAX_BYTES:
                        raise InstallError(f"the archive unpacks to more than {UNPACKED_MAX_BYTES} bytes")
                    source = tar.extractfile(member)
                    if source is None:
                        raise InstallError(f"{'/'.join(rel)!r} cannot be read")
                    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
                    fd = os.open(target, flags, 0o600)
                    with os.fdopen(fd, "wb") as out:
                        copied = 0
                        for chunk in iter(lambda: source.read(1024 * 1024), b""):
                            copied += len(chunk)
                            out.write(chunk)
                        if copied != member.size:
                            raise InstallError(f"{'/'.join(rel)!r} is cut short")
                        # Never setuid, setgid, sticky or writable by others.
                        os.fchmod(out.fileno(), 0o755 if member.mode & 0o111 else 0o644)
                    with contextlib.suppress(OSError):
                        os.utime(target, (member.mtime, member.mtime))
                elif member.issym():
                    link = member.linkname
                    if not link or "\0" in link or link.startswith("/"):
                        raise InstallError(f"the link {'/'.join(rel)!r} points outside the bundle")
                    resolved = os.path.normpath(os.path.join(*rel[:-1], link) if len(rel) > 1 else link)
                    if resolved == ".." or resolved.startswith("../") or resolved.startswith("/"):
                        raise InstallError(f"the link {'/'.join(rel)!r} points outside the bundle")
                    os.symlink(link, target)
                    links.add(key)
                else:
                    raise InstallError(f"the archive has {'/'.join(rel)!r}, which is not a file, folder or link")
    except InstallError:
        raise
    except (tarfile.TarError, OSError, EOFError, zlib.error) as exc:
        raise InstallError(f"the archive could not be unpacked: {exc}") from exc
    if top is None:
        raise InstallError("the archive is empty")
