"""Read manifest-selected bytes without materializing archive links or metadata."""
from __future__ import annotations

import gzip
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
import re
import shutil
import tarfile
import zlib

from .errors import DownloadError
from .layout import relative_path
from .tar_reader import ArchiveBudget, ArchiveLimitExceeded, open_archive

MAX_LINK_HOPS = 40


class ArchiveSelectionUnavailable(DownloadError):
    """The archive cannot reliably reproduce the manifest's selected files."""


def _canonical_member_name(member: tarfile.TarInfo) -> str:
    name = member.name.rstrip('/') if member.isdir() else member.name
    while name.startswith('./'):
        name = name[2:]
    if member.isdir() and name in ('', '.'):
        return ''
    if any(part in ('', '.', '..') for part in name.split('/')):
        raise ArchiveSelectionUnavailable('noncanonical archive member may alias another path')
    return name


def _safe_link_target(member: tarfile.TarInfo) -> str:
    link = member.linkname
    if (not link or link.startswith('/') or '\\' in link or '\x00' in link
            or re.match(r'^[A-Za-z]:', link)):
        raise DownloadError('unsafe selected archive link')
    return link


@dataclass
class _ArchiveIndex:
    """Resolve file content without replaying archive filesystem mutations."""

    budget: ArchiveBudget
    members_by_path: dict[str, list[tarfile.TarInfo]] = field(default_factory=dict)
    directory_paths: set[str] = field(default_factory=set)
    link_paths: set[str] = field(default_factory=set)

    def add(self, member: tarfile.TarInfo) -> None:
        name = _canonical_member_name(member)
        if not name:
            return
        self.members_by_path.setdefault(name, []).append(member)
        parent = ''
        for part in name.split('/')[:-1]:
            parent = parent + '/' + part if parent else part
            self._add_directory(parent)
        if member.isdir():
            self._add_directory(name)
        if member.issym() or member.islnk():
            self.link_paths.add(name)

    def _add_directory(self, name: str) -> None:
        if name not in self.directory_paths:
            self.budget.add_index_path(name)
            self.directory_paths.add(name)

    def validate_writes(self) -> None:
        # Writes below a directory link can overwrite a differently named
        # member. Avoid replaying filesystem mutations in the reader.
        if self.link_paths & self.directory_paths:
            raise ArchiveSelectionUnavailable('archive writes through directory links')
        # A later write through a hard-link alias can change another member's
        # bytes. Let the existing file service resolve that ambiguity.
        has_hard_links = any(member.islnk() for entries in self.members_by_path.values()
                             for member in entries)
        if not has_hard_links:
            return
        has_duplicate_files = any(len(entries) > 1 and not all(member.isdir() for member in entries)
                                  for entries in self.members_by_path.values())
        if has_duplicate_files:
            raise ArchiveSelectionUnavailable('ambiguous archive hard-link writes')

    def resolve_file(self, name: str) -> tarfile.TarInfo:
        relative_path(name, DownloadError)
        pending = deque(name.split('/'))
        resolved: list[str] = []
        link_hops = 0
        # Expand intermediate links before interpreting "..": lexical normpath
        # would both change the target and hide unsafe intermediate links.
        while pending:
            part = pending.popleft()
            if part in ('', '.'):
                continue
            if part == '..':
                if not resolved:
                    raise DownloadError('selected archive link escapes archive')
                resolved.pop()
                continue
            prefix = '/'.join([*resolved, part])
            relative_path(prefix, DownloadError)
            entries = self.members_by_path.get(prefix, [])
            if len(entries) > 1:
                raise ArchiveSelectionUnavailable('ambiguous selected archive member')
            if not entries:
                if prefix not in self.directory_paths or not pending:
                    raise ArchiveSelectionUnavailable('selected archive member missing')
                resolved.append(part)
                continue
            member = entries[0]
            if member.issym() or member.islnk():
                target = _safe_link_target(member)
                link_hops += 1
                if link_hops > MAX_LINK_HOPS:
                    raise ArchiveSelectionUnavailable('selected archive link cycle')
                if member.islnk():
                    resolved = []
                pending.extendleft(reversed(target.split('/')))
                continue
            if pending:
                if not member.isdir():
                    raise ArchiveSelectionUnavailable('selected archive parent is not a directory')
                resolved.append(part)
            elif member.isfile():
                return member
            else:
                raise ArchiveSelectionUnavailable('selected archive member is not a file')
        raise ArchiveSelectionUnavailable('selected archive member is not a file')


def _copy_selected_files(tar: tarfile.TarFile, members: list[tuple[tarfile.TarInfo, str]],
                         directory: Path) -> None:
    # Read in archive order after the index scan, so backward seeks do not
    # re-inflate the gzip stream once per file. Aliases copy an existing output.
    copied: dict[tarfile.TarInfo, Path] = {}
    for member, logical in sorted(members, key=lambda item: item[0].offset_data):
        destination = directory / logical
        destination.parent.mkdir(parents=True, exist_ok=True)
        if member in copied:
            shutil.copyfile(copied[member], destination)
            continue
        source = tar.extractfile(member)
        if source is None:
            raise ArchiveSelectionUnavailable('selected archive member has no content')
        with source, destination.open('wb') as output:
            shutil.copyfileobj(source, output)
        copied[member] = destination


def extract_selected(archive: Path, selected: list[tuple[str, str]], directory: Path) -> None:
    """Copy selected content as ordinary files, using manifest output paths."""
    try:
        budget = ArchiveBudget()
        with open_archive(archive, budget) as (tar, members):
            index = _ArchiveIndex(budget)
            for member in members:
                index.add(member)
            selected_members = [(index.resolve_file(raw), relative_path(logical, DownloadError))
                                for raw, logical in selected]
            index.validate_writes()
            _copy_selected_files(tar, selected_members, directory)
    except (tarfile.TarError, gzip.BadGzipFile, EOFError, zlib.error, ValueError,
            IndexError, RecursionError, ArchiveLimitExceeded):
        raise ArchiveSelectionUnavailable('cannot read selected archive content') from None
