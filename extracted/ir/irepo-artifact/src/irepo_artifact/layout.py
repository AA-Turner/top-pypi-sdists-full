"""Manifest selection and transactional local output; no network operations."""
from __future__ import annotations

import os
import hashlib
import getpass
import logging
from pathlib import Path
import re
import shutil
import stat
import tarfile
import tempfile

from .errors import ArtifactError, ConfigurationError, DownloadError, ProtocolError
from .tar_reader import open_archive

logger = logging.getLogger(__name__)


def relative_path(path: str, error=ProtocolError) -> str:
    if (not isinstance(path, str) or not path or path.startswith('/') or '\\' in path
            or '\x00' in path or re.match(r'^[A-Za-z]:', path)
            or any(part in ('', '.', '..') for part in path.split('/'))):
        raise error('unsafe artifact relative path')
    return path


def selectors(values):
    if values is None:
        return []
    if not isinstance(values, (list, tuple)):
        raise ConfigurationError('file selectors must be a list of strings')
    result = []
    for value in values:
        if not isinstance(value, str):
            raise ConfigurationError('file selectors must be strings')
        value = value.strip()
        while value.startswith('./'):
            value = value[2:]
        value = relative_path(value.rstrip('/'), ConfigurationError)
        if value not in result:
            result.append(value)
    return result


def _matches(path, selector):
    if '/' in selector:
        return path == selector or path.startswith(selector + '/')
    return selector in path.split('/')


def select_files(manifest, include_files, exclude_files, *, ap_export=False):
    includes, excludes = selectors(include_files), selectors(exclude_files)
    files, directories = [], set()
    seen_files = set()
    for row in manifest:
        if not isinstance(row, dict):
            raise ProtocolError('invalid manifest entry')
        path = relative_path(row.get('path'))
        if row.get('type') == 'dir':
            directories.add(path)
        elif row.get('type') == 'file':
            if path not in seen_files:
                files.append(path)
                seen_files.add(path)
        else:
            raise ProtocolError('unsupported manifest entry type')
    if seen_files & directories:
        raise ProtocolError('manifest path is both file and directory')
    roots = ({p.split('/')[0] for p in files if '/' in p} if ap_export
             else {p.split('/')[0] for p in [*files, *directories]})
    root = next(iter(roots)) if len(roots) == 1 else None
    strip = root if root in directories and all('/' in p for p in files) else None
    selected = []
    for path in files:
        logical = path[len(strip) + 1:] if strip else path
        matches = lambda s: _matches(path, s) or _matches(logical, s)
        if (not includes or any(matches(s) for s in includes)) and not any(matches(s) for s in excludes):
            selected.append((path, logical))
    destinations = [p for _, p in selected]
    destination_set = set(destinations)
    if len(destination_set) != len(destinations):
        raise ProtocolError('colliding artifact file destinations')
    for dest in destinations:
        if any(str(parent) in destination_set for parent in Path(dest).parents if str(parent) != '.'):
            raise ProtocolError('artifact file path conflicts with parent file')
    return selected


def _no_symlinks(path: Path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise DownloadError('symbolic links are not allowed in output paths')


def _retry_readonly(function, path, error):
    if not isinstance(error[1], PermissionError) or Path(path).is_symlink():
        raise error[1]
    entry = Path(path)
    entry.chmod(entry.stat().st_mode | stat.S_IWUSR)
    function(path)


def _remove(path):
    if path.is_symlink() or path.is_file():
        try:
            path.unlink()
        except PermissionError as exc:
            _retry_readonly(os.unlink, path, (type(exc), exc, exc.__traceback__))
    elif path.exists():
        # Extracted directory modes may be read-only. Only touch our retired
        # staging/backup tree, never follow a link into another directory.
        path.chmod(path.stat().st_mode | 0o700)
        for directory, children, _ in os.walk(path):
            for child in children:
                entry = Path(directory) / child
                if not entry.is_symlink():
                    entry.chmod(entry.stat().st_mode | 0o700)
        shutil.rmtree(path, onerror=_retry_readonly)


def _lock_path(job_dir):
    # Outside the export tree so AP's exported file set remains unchanged.
    identity = str(os.getuid()) if hasattr(os, 'getuid') else getpass.getuser()
    user_key = hashlib.sha256(identity.encode()).hexdigest()[:16]
    directory = Path(tempfile.gettempdir()).resolve() / ('irepo-artifact-locks-' + user_key)
    _no_symlinks(directory)
    directory.mkdir(mode=0o700, exist_ok=True)
    if os.name != 'nt':
        info = directory.stat()
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise DownloadError('artifact lock directory must be private to the current user')
    key = hashlib.sha256(os.fsencode(os.path.normcase(str(job_dir)))).hexdigest()
    return directory / (key + '.lock')


class JobOutput:
    """Own a per-Job lock and staging tree until cleanup (always use finally)."""
    def __init__(self, job_dir: Path, overwrite: bool, *, private_selected=False):
        self.job_dir = Path(os.path.abspath(job_dir))
        self.overwrite = overwrite
        self.stage = None
        self.lock = None
        self._lock_fd = None
        try:
            _no_symlinks(self.job_dir)
            self.job_dir.mkdir(parents=True, exist_ok=True)
            self.lock = _lock_path(self.job_dir)
            _no_symlinks(self.lock)
            fd = os.open(self.lock, os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0), 0o600)
            self._lock_fd = fd
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise DownloadError('artifact lock must be a regular file')
            if os.name == 'nt':
                import msvcrt
                # Windows byte-range locks may extend beyond EOF.
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            for name in ('result.tgz', 'artifacts'):
                path = self.job_dir / name
                _no_symlinks(path)
                if path.exists() and not overwrite:
                    raise DownloadError('artifact output exists; set overwrite=True to replace')
            self.stage = Path(tempfile.mkdtemp(prefix='.artifact-', dir=self.job_dir))
            self.archive_temp = self.stage / 'result.tgz'
            self.files_temp = self.stage / 'artifacts/output'
            self.files_temp.mkdir(parents=True)
            if private_selected:
                self.files_temp.parent.chmod(0o700)
        except (OSError, ArtifactError) as exc:
            self.cleanup()
            if isinstance(exc, ArtifactError):
                raise
            raise DownloadError('cannot prepare output; check directory or active download lock') from None

    def reset_selected(self) -> None:
        """Discard the archive attempt before falling back to individual files."""
        self.archive_temp.unlink(missing_ok=True)
        shutil.rmtree(self.files_temp)
        self.files_temp.mkdir(parents=True)

    def extract_archive(self):
        raw = self.stage / 'unpacked'
        raw.mkdir()
        try:
            directories = {}
            def contained(path):
                if not path.resolve().is_relative_to(raw.resolve()):
                    raise DownloadError('archive link escapes extraction directory')

            def restore(path, member):
                # Preserve ordinary modes and timestamps, never archive ownership
                # or privilege bits. Directory attributes are applied last.
                if not path.is_symlink():
                    path.chmod(member.mode & 0o777)
                    os.utime(path, (member.mtime, member.mtime))
                elif os.utime in os.supports_follow_symlinks:
                    os.utime(path, (member.mtime, member.mtime), follow_symlinks=False)

            with open_archive(self.archive_temp) as (tar, members):
                for member in members:
                    name = member.name.rstrip('/') if member.isdir() else member.name
                    # Conventional tar root '.' and './' prefixes carry no path traversal.
                    while name.startswith('./'):
                        name = name[2:]
                    if name in ('', '.') and member.isdir():
                        continue
                    relative_path(name, DownloadError)
                    if not (member.isfile() or member.isdir() or member.issym() or member.islnk()):
                        raise DownloadError('archive contains unsupported file type')
                    dest = raw / name
                    contained(dest)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if member.isfile():
                        # tar semantics: later regular entries overwrite earlier
                        # content, including content shared by safe hard links.
                        with tar.extractfile(member) as source, dest.open('wb') as output:
                            shutil.copyfileobj(source, output)
                        restore(dest, member)
                    elif member.isdir():
                        dest.mkdir(parents=True, exist_ok=True)
                        directories[name] = member
                    else:
                        link = member.linkname
                        if (not link or '\\' in link or '\x00' in link
                                or re.match(r'^[A-Za-z]:', link)):
                            raise DownloadError('unsafe archive link')
                        target = (dest.parent if member.issym() else raw) / link
                        if link.startswith('/') or not target.resolve().is_relative_to(raw.resolve()):
                            # Container-local convenience links cannot be recreated
                            # safely on the downloader's filesystem.
                            logger.warning('Skipping unsafe artifact link: %r -> %r', member.name, link)
                            continue
                        if member.islnk() and not target.is_file():
                            raise DownloadError('archive hard link target is not a regular file')
                        if dest.is_symlink() or dest.exists():
                            dest.unlink()
                        if member.issym():
                            dest.symlink_to(link)
                        else:
                            os.link(target.resolve(), dest)
                        restore(dest, member)
            entries = list(raw.iterdir())
            root = (entries[0] if len(entries) == 1 and entries[0].is_dir()
                    and not entries[0].is_symlink() else raw)
            # Validate links in the final layout as root stripping can turn an
            # in-archive reference into a reference outside artifacts/output.
            for entry in raw.rglob('*'):
                if entry.is_symlink() and not entry.resolve().is_relative_to(root.resolve()):
                    raise DownloadError('archive link escapes normalized output')
            prefix = root.relative_to(raw)
            if root != raw:
                self.files_temp.rmdir()
                root.replace(self.files_temp)
            else:
                for entry in root.iterdir():
                    entry.replace(self.files_temp / entry.name)
            for entry in self.files_temp.rglob('*'):
                if entry.is_symlink() and not entry.resolve().is_relative_to(self.files_temp.resolve()):
                    raise DownloadError('archive link escapes normalized output')
            files = tuple(sorted(p.relative_to(self.files_temp)
                                 for p in self.files_temp.rglob('*') if p.is_file()))
            for name, member in sorted(directories.items(), key=lambda row: len(Path(row[0]).parts), reverse=True):
                restore(self.files_temp / Path(name).relative_to(prefix), member)
            return files
        except ArtifactError:
            raise
        except (tarfile.TarError, OSError, EOFError, ValueError, OverflowError, RuntimeError):
            raise DownloadError('cannot safely extract artifact archive') from None

    def commit(self, mode):
        if mode not in ('archive', 'expanded', 'selected'):
            raise ConfigurationError('invalid output mode')
        installed, backups = [], []
        try:
            _no_symlinks(self.job_dir)
            for name in ('result.tgz', 'artifacts'):
                dest = self.job_dir / name
                _no_symlinks(dest)
                if dest.exists():
                    if not self.overwrite:
                        raise DownloadError('artifact output appeared during download')
                    backup = self.stage / ('previous-' + name)
                    dest.replace(backup)
                    backups.append((dest, backup))
            names = ['result.tgz'] if mode == 'archive' else ['artifacts'] if mode == 'selected' else ['result.tgz', 'artifacts']
            for name in names:
                dest = self.job_dir / name
                (self.stage / name).replace(dest)
                installed.append(dest)
        except (OSError, ArtifactError):
            try:
                for dest in reversed(installed):
                    _remove(dest)
                for dest, backup in reversed(backups):
                    backup.replace(dest)
            except OSError:
                # Keep the backups if rollback itself fails; cleanup must not delete them.
                self.stage = None
                raise DownloadError('output rollback failed; retained .artifact-* backup directory') from None
            raise DownloadError('cannot commit artifact output; previous output restored') from None

    def cleanup(self):
        if self.stage is not None:
            try:
                _remove(self.stage)
            except OSError:
                pass
            self.stage = None
        if self._lock_fd is not None:
            # Keep the inode: unlinking can let contenders lock different files.
            # Closing releases the OS lock, including after process termination.
            os.close(self._lock_fd)
            self._lock_fd = None
