"""Fixed, no-follow local file inventory shared by validation and delivery."""
from __future__ import annotations

import hashlib
import os
import stat
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .errors import LayoutError


def _identity(st):
    return (st.st_dev, st.st_ino, st.st_mode, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns)


# Keep capability references stable when calls are instrumented for race tests.
_DIR_FD_OPERATIONS = (os.open, os.stat, os.readlink)
_FD_LISTDIR = os.listdir
_NOFOLLOW_STAT = os.stat


def _require_capabilities():
    if (not all(getattr(os, flag, 0) for flag in
                ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
            or not all(op in os.supports_dir_fd for op in _DIR_FD_OPERATIONS)
            or _FD_LISTDIR not in os.supports_fd
            or _NOFOLLOW_STAT not in os.supports_follow_symlinks):
        raise LayoutError(".: secure descriptor traversal is not supported")


def _open_dir(name, *, dir_fd=None, search_only=False):
    access = os.O_RDONLY
    if search_only:
        # Ancestors are path anchors, not directories to inventory.
        access = getattr(os, "O_PATH", 0) or getattr(os, "O_SEARCH", os.O_RDONLY)
    return os.open(name, access | os.O_DIRECTORY | os.O_NOFOLLOW,
                   dir_fd=dir_fd)


def _check_bindings(bindings):
    for parent, name, fd, expected in bindings:
        if (_identity(os.fstat(fd))[:len(expected)] != expected
                or _identity(os.stat(name, dir_fd=parent,
                                     follow_symlinks=False))[:len(expected)] != expected):
            raise LayoutError(".: source path changed after validation")


def _digest(stream):
    stream.seek(0)
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1 << 20), b""):
        digest.update(chunk)
    stream.seek(0)
    return digest.digest()


@dataclass(frozen=True)
class Entry:
    path: str
    kind: str
    mode: int
    identity: tuple
    link: str = ""


class FileTree:
    """Capture all entries without following links; recheck identity on every read.

    Directory descriptors anchor traversal even when a parent pathname is swapped.
    Links are resolved against the captured inventory, never the outside filesystem.
    """

    def __init__(self, source: str | Path, *, allow_links: bool = True):
        _require_capabilities()
        self.source = Path(os.path.abspath(source))
        self.allow_links = allow_links
        self.entries: dict[str, Entry] = {}
        self.root_identity = None
        self._ancestors = None
        self._digests: dict[str, bytes] = {}
        try:
            with self._open_source() as (fd, root_stat, bindings):
                self.directory = stat.S_ISDIR(root_stat.st_mode)
                self.root_identity = _identity(root_stat)
                self._ancestors = tuple(binding[3] for binding in bindings[:-1])
                if self.directory:
                    self._walk(fd, "")
                else:
                    self._add(self.source.name, root_stat)
            self._check_links()
        except FileNotFoundError:
            raise LayoutError(f"{self.source.name}: path does not exist") from None
        except (OSError, NotImplementedError):
            raise LayoutError(f"{self.source.name}: cannot securely read input tree") from None

    @contextmanager
    def _open_source(self):
        """Open literal components from /; never resolve source ancestors by path."""
        descriptors, bindings = [], []
        try:
            fd = _open_dir(self.source.anchor, search_only=True)
            descriptors.append(fd)
            for index, part in enumerate(self.source.parts[1:-1]):
                child = _open_dir(part, dir_fd=fd, search_only=True)
                descriptors.append(child)
                identity = _identity(os.fstat(child))[:3]
                if self._ancestors is not None and identity != self._ancestors[index]:
                    raise LayoutError(".: source ancestor changed after validation")
                bindings.append((fd, part, child, identity))
                fd = child
            # Ancestor checks happen before even looking up the source leaf.
            _check_bindings(bindings)
            name = self.source.name or "."
            st = os.stat(name, dir_fd=fd, follow_symlinks=False)
            directory = stat.S_ISDIR(st.st_mode)
            if not directory and not stat.S_ISREG(st.st_mode):
                raise LayoutError(f"{self.source.name}: input must be a regular file or directory")
            if not st.st_mode & 0o444 or (directory and not st.st_mode & 0o111):
                raise LayoutError(f"{self.source.name}: input is not readable")
            expected = self.root_identity or _identity(st)
            if _identity(st) != expected:
                raise LayoutError(".: source changed after validation")
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            if directory:
                flags |= os.O_DIRECTORY
            root = os.open(name, flags, dir_fd=fd)
            descriptors.append(root)
            bindings.append((fd, name, root, expected))
            # Verify the opened inode AND its entire path before listing/reading it.
            _check_bindings(bindings)
            yield root, st, bindings
            _check_bindings(bindings)
        finally:
            for fd in reversed(descriptors):
                os.close(fd)

    @contextmanager
    def _entry_parent(self, root, rel):
        descriptors, bindings = [], []
        parts = rel.split("/")
        fd = root
        try:
            for index, part in enumerate(parts[:-1]):
                parent = self.entries["/".join(parts[:index + 1])]
                child = _open_dir(part, dir_fd=fd)
                descriptors.append(child)
                bindings.append((fd, part, child, parent.identity))
                _check_bindings(bindings[-1:])
                fd = child
            yield fd, parts[-1], bindings
        finally:
            for fd in reversed(descriptors):
                os.close(fd)

    def _check_link(self, root, rel):
        entry = self.entries[rel]
        with self._entry_parent(root, rel) as (parent, name, bindings):
            _check_bindings(bindings)
            if _identity(os.stat(name, dir_fd=parent, follow_symlinks=False)) != entry.identity:
                raise LayoutError(f"{rel}: link changed after validation")
            if os.readlink(name, dir_fd=parent) != entry.link:
                raise LayoutError(f"{rel}: link changed after validation")
            if _identity(os.stat(name, dir_fd=parent, follow_symlinks=False)) != entry.identity:
                raise LayoutError(f"{rel}: link changed during read")
            _check_bindings(bindings)

    def _add(self, rel, st, link="", *, entries=None):
        mode = st.st_mode
        if stat.S_ISREG(mode):
            kind = "file"
            if not mode & 0o444:
                raise LayoutError(f"{rel}: file is not readable")
        elif stat.S_ISDIR(mode):
            kind = "directory"
            if not mode & 0o444 or not mode & 0o111:
                raise LayoutError(f"{rel}: directory is not readable")
        elif stat.S_ISLNK(mode):
            kind = "link"
            if not self.allow_links:
                raise LayoutError(f"{rel}: custom assets cannot represent links")
            if (not link or link.startswith(("/", "\\")) or "\\" in link
                    or (len(link) > 1 and link[1] == ":")
                    or any(ord(c) < 32 or ord(c) == 127 for c in link)):
                raise LayoutError(f"{rel}: link target must be internal and relative")
        else:
            raise LayoutError(f"{rel}: special files are not supported")
        inventory = self.entries if entries is None else entries
        inventory[rel] = Entry(rel, kind, mode & 0o777, _identity(st), link)

    def _walk(self, fd, prefix, entries=None):
        before = _identity(os.fstat(fd))
        for name in sorted(os.listdir(fd)):
            rel = prefix + name
            if "\\" in name or any(ord(c) < 32 or ord(c) == 127 for c in name):
                raise LayoutError(f"{rel}: unsafe asset path")
            st = os.stat(name, dir_fd=fd, follow_symlinks=False)
            link = os.readlink(name, dir_fd=fd) if stat.S_ISLNK(st.st_mode) else ""
            self._add(rel, st, link, entries=entries)
            if stat.S_ISDIR(st.st_mode):
                child = _open_dir(name, dir_fd=fd)
                try:
                    if _identity(os.fstat(child)) != _identity(st):
                        raise LayoutError(f"{rel}: entry changed during inventory")
                    self._walk(child, rel + "/", entries)
                finally:
                    os.close(child)
            if _identity(os.stat(name, dir_fd=fd, follow_symlinks=False)) != _identity(st):
                raise LayoutError(f"{rel}: entry changed during inventory")
        if _identity(os.fstat(fd)) != before:
            raise LayoutError(f"{prefix or '.'}: directory changed during inventory")

    def resolve(self, rel: str) -> str:
        return self._resolve(rel, [])

    def _resolve(self, rel, links):
        pending = rel.split("/")
        resolved: list[str] = []
        visited = set()
        while pending:
            part = pending.pop(0)
            if part in ("", "."):
                continue
            if part == "..":
                if not resolved:
                    raise LayoutError(f"{rel}: link escapes task root")
                resolved.pop()
                continue
            key = "/".join(resolved + [part])
            entry = self.entries.get(key)
            if entry is None:
                raise LayoutError(f"{rel}: missing or dangling entry")
            if entry.kind == "link":
                if key in visited:
                    raise LayoutError(f"{rel}: cyclic link")
                visited.add(key)
                links.append(key)
                pending = entry.link.split("/") + pending
            else:
                if pending and entry.kind != "directory":
                    raise LayoutError(f"{rel}: non-directory path component")
                resolved.append(part)
        return "/".join(resolved)

    def _check_links(self):
        targets = {rel: self.resolve(rel) for rel, e in self.entries.items()
                   if e.kind == "link"}
        # Directory links may form expansion cycles even without a symlink chain.
        def visit(directory, stack):
            if directory in stack:
                raise LayoutError(f"{directory or '.'}: cyclic directory link")
            stack = stack | {directory}
            prefix = directory + "/" if directory else ""
            for rel, target in targets.items():
                if rel.startswith(prefix) and (target == "" or
                        self.entries[target].kind == "directory"):
                    visit(target, stack)
        visit("", set())

    def assert_unchanged(self):
        current = {}
        try:
            # Reconciliation must use the ORIGINAL root identity too, not recapture
            # a substituted tree and only compare identities after walking it.
            with self._open_source() as (fd, root_stat, _):
                if self.directory:
                    self._walk(fd, "", current)
                else:
                    self._add(self.source.name, root_stat, entries=current)
        except (OSError, NotImplementedError):
            raise LayoutError(".: source tree unreadable or replaced after validation") from None
        if self.entries != current:
            raise LayoutError(".: source tree changed after validation")

    @contextmanager
    def open_file(self, rel: str):
        links = []
        target = self._resolve(rel, links)
        entry = self.entries.get(target)
        if entry is None or entry.kind != "file":
            raise LayoutError(f"{rel}: expected a readable file")
        try:
            with self._open_source() as (root, _, source_bindings), \
                    self._entry_parent(root, target) as (parent, name, parent_bindings):
                for link in links:
                    self._check_link(root, link)
                if self.directory:
                    file_fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                      dir_fd=parent)
                    file_bindings = [(parent, name, file_fd, entry.identity)]
                else:
                    file_fd = os.dup(root)
                    file_bindings = []
                # Unbuffered reads also make digest rechecks observe the live inode,
                # not stale BufferedReader bytes after seek(0).
                with os.fdopen(file_fd, "rb", buffering=0) as stream:
                    def check_read_path():
                        _check_bindings(source_bindings + parent_bindings + file_bindings)
                        if _identity(os.fstat(stream.fileno())) != entry.identity:
                            raise LayoutError(f"{rel}: file changed during read")
                        for link in links:
                            self._check_link(root, link)

                    check_read_path()
                    before = _digest(stream)
                    previous = self._digests.get(target)
                    if previous is not None and before != previous:
                        raise LayoutError(f"{rel}: file bytes changed after validation")
                    check_read_path()
                    yield stream
                    check_read_path()
                    # Timestamps can be coarse; compare bytes as well as stat identity.
                    if _digest(stream) != before:
                        raise LayoutError(f"{rel}: file bytes changed during read")
                    check_read_path()
                    self._digests[target] = before
        except (OSError, NotImplementedError):
            raise LayoutError(f"{rel}: file unreadable or replaced after validation") from None

    def read_bytes(self, rel):
        with self.open_file(rel) as stream:
            return stream.read()

    def check_readable(self):
        self.assert_unchanged()
        for rel, entry in self.entries.items():
            if entry.kind == "file":
                with self.open_file(rel) as stream:
                    while stream.read(1 << 20):
                        pass
        self.assert_unchanged()

    def copy_to(self, destination: str | Path):
        """Create a safe private snapshot, retaining dirs/modes and relative links."""
        import shutil
        dest = Path(destination)
        self.assert_unchanged()
        if not self.directory:
            with self.open_file(self.source.name) as stream, dest.open("wb") as out:
                shutil.copyfileobj(stream, out)
            dest.chmod(self.entries[self.source.name].mode)
            self.assert_unchanged()
            return dest
        dest.mkdir()
        for rel, entry in sorted(self.entries.items()):
            output = dest / rel
            if entry.kind == "directory":
                output.mkdir()
            elif entry.kind == "link":
                output.symlink_to(entry.link)
            else:
                with self.open_file(rel) as stream, output.open("wb") as out:
                    shutil.copyfileobj(stream, out)
                output.chmod(entry.mode)
        for rel, entry in reversed(sorted(self.entries.items())):
            if entry.kind == "directory":
                (dest / rel).chmod(entry.mode)
        dest.chmod(self.root_identity[2] & 0o777)
        self.assert_unchanged()
        return dest
