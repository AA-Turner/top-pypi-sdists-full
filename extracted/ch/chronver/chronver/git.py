"""Get version from Git

:copyright: Copyright (c) 2024 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

import datetime
import locale
import os
import os.path
import re
import subprocess
import sys
import time

#: Where version is stored when _is_edited() is true
_CACHE_FILE = "._chronver_cache"

_FMT = "%Y%m%d.%H%M%S"

_FMT_TIME_LEN = len(_FMT) + 2


def version():
    """Chronological version string for most recent commit or current time

    Finds the commit date of git HEAD. Uses ``git status``
    to find files under git control which are modified or to be
    deleted, in which case we assume this is a developer, and we
    should just use the current time for the version. It will be newer
    than any committed version, which is all we care about for
    upgrades.

    Returns:
        str: canonicalized "yyyymmdd.hhmmss" or ``None`` if not a git repo
    """

    def _fmt(value):
        return datetime.datetime.fromtimestamp(value).strftime(_FMT)

    def _head():
        return _fmt(
            float(
                _sh(
                    (
                        "git",
                        "log",
                        "-1",
                        "--format=%ct",
                        _sh(("git", "rev-parse", "--abbrev-ref", "HEAD")),
                    ),
                ),
            ),
        )

    def _is_edited():
        """Determine if any files are changed

        Untracked files are hard to know. Could be junk files in
        a developer's repo. This only necessary for development anyway.
        """
        return bool(
            _sh(
                (
                    "git",
                    "status",
                    "--ignore-submodules",
                    "--porcelain",
                    "--untracked-files=no",
                ),
            ),
        )

    def _is_repo():
        return os.path.isdir(".git")

    def _now():
        """Cache time now in a file

        `version` is called multiple times during a wheel build in
        separate processes so can't cache in memory. Need to have the
        same version every time. Only called when editing, not
        production.
        """
        # POSIT: pip sets this to the build dir; Otherwise is "build", guess pwd doesn't change
        p = os.getenv("PIP_BUILD_TRACKER", os.getcwd()) + "/" + _CACHE_FILE
        try:
            f = open(p, "rt")
            rv = f.read()
            f.close()
            if len(rv) == _FMT_TIME_LEN:
                return rv
        except FileNotFoundError:
            pass
        f = open(p, "wt")
        rv = _fmt(time.time())
        f.write(rv)
        f.close()
        return rv

    def _sh(cmd):
        try:
            res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            if isinstance(res, bytes):
                return res.decode(locale.getpreferredencoding()).rstrip()
            return None
        except subprocess.CalledProcessError as e:
            if hasattr(e, "output") and len(e.output):
                sys.stderr.write(e.output.decode(locale.getpreferredencoding()))
            raise

    if not _is_repo():
        return None
    return _now() if _is_edited() else _head()
