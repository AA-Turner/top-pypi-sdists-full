"""This process's open-file limit, raised for a process that holds many files at once (the Probe
service: every `probe` command's sockets; the daemon host: every session's stores and logs).

One helper for both: the soft RLIMIT_NOFILE goes up to the hard one (macOS defaults to 256), at
most MAX_OPEN_FILES (macOS's hard limit is unlimited, which no setrlimit takes). Stdlib only.
"""

from __future__ import annotations

import contextlib

MAX_OPEN_FILES = 10_240
#: What a process reads when the limit cannot be read at all (no `resource`).
UNKNOWN_LIMIT = 1024


def raise_open_files() -> int:
    """Raise the soft limit as far as MAX_OPEN_FILES; the soft limit in force afterwards, as
    `getrlimit` reads it (a raise that failed leaves the old one). Never raises."""
    try:
        import resource
    except ImportError:
        return UNKNOWN_LIMIT
    with contextlib.suppress(Exception):
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        want = MAX_OPEN_FILES if hard == resource.RLIM_INFINITY else min(hard, MAX_OPEN_FILES)
        if soft != resource.RLIM_INFINITY and soft < want:
            resource.setrlimit(resource.RLIMIT_NOFILE, (want, hard))
    try:
        soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    except (OSError, ValueError):
        return UNKNOWN_LIMIT
    return MAX_OPEN_FILES if soft == resource.RLIM_INFINITY else int(soft)
