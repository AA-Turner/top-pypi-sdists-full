"""Lifted verbatim from fitevict/serve/directory_browser.py (sha256 3ae53b45ed226f07): browse and what they reach in that file.
Written by tools/refactors/core-off-fitevict-20261110/lift.py; the definitions below are the original text."""
from __future__ import annotations

import os
import re
from pathlib import Path

# imports.constants.serving.DIRECTORY_BROWSER_PSEUDO: filesystems that are not places to look for models
PSEUDO = {'autofs', 'binfmt_misc', 'bpf', 'cgroup', 'cgroup2', 'configfs', 'debugfs', 'devpts', 'devtmpfs', 'efivarfs',
          'fusectl', 'hugetlbfs', 'mqueue', 'nsfs', 'proc', 'pstore', 'securityfs', 'squashfs', 'sysfs', 'tmpfs', 'tracefs'}


def locations(mountinfo='/proc/self/mountinfo'):
    """Mount names only; avoid probing every disk or waking network mounts."""
    rows = {'/': {'path': '/', 'name': 'Filesystem root', 'filesystem': ''}}
    try:
        for line in Path(mountinfo).read_text().splitlines():
            left, right = line.split(' - ', 1)
            fields, fs = left.split(), right.split()
            mount = re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), fields[4])
            if fs[0] not in PSEUDO:
                rows[mount] = {'path': mount, 'name': mount, 'filesystem': fs[0],
                               'device': re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), fs[1])}
    except (OSError, ValueError, IndexError):
        pass
    return sorted(rows.values(), key=lambda row: row['path'].casefold())


def browse(path='/', offset=0, limit=200, query='', hidden=False):
    if not isinstance(path, str) or not path.startswith('/') or '\x00' in path:
        raise ValueError('Choose an absolute directory path on the Wrapper host.')
    if offset < 0 or not 1 <= limit <= 500:
        raise ValueError('offset must be nonnegative and limit must be between 1 and 500.')
    path = os.path.realpath(path)
    entries = []
    scanned = 0
    partial = False
    with os.scandir(path) as listing:
        for entry in listing:
            scanned += 1
            if scanned > 20000:
                partial = True
                break
            if (not hidden and entry.name.startswith('.')) or query.casefold() not in entry.name.casefold():
                continue
            try:
                if entry.is_dir(follow_symlinks=True):
                    entries.append({'name': entry.name, 'path': os.path.join(path, entry.name),
                                    'symlink': entry.is_symlink()})
            except OSError:
                continue
    entries.sort(key=lambda entry: entry['name'].casefold())
    usage = {}
    try:
        fs = os.statvfs(path)
        usage = {'total_bytes': fs.f_blocks * fs.f_frsize, 'free_bytes': fs.f_bavail * fs.f_frsize}
    except OSError:
        pass
    return {'path': path, 'parent': os.path.dirname(path), 'directories': entries[offset:offset + limit],
            'offset': offset, 'limit': limit, 'more': offset + limit < len(entries),
            'partial': partial, 'locations': locations(), **usage}
