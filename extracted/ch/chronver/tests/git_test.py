"""test git version

:copyright: Copyright (c) 2024 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

import contextlib


def test_basic():
    from pykern import pkunit
    from chronver import git
    import datetime
    import os
    import time

    with _setup():
        e = datetime.datetime.utcnow().strftime("%Y%m%d.%H%M%S")
        pkunit.pkeq(
            0,
            os.system("git init && echo x > x && git add x && git commit -m x"),
        )
        a = git.version()
        pkunit.pkeq(len(e), len(a))
        pkunit.pkok(e <= a, "expect={} is greater than actual={}", e, a)
        time.sleep(1)
        with open("x", "wt") as f:
            f.write("change")
        b = git.version()
        pkunit.pkok(a < b, "expect={} should be older than={}", a, b)


def test_git_status_error(capsys):
    from pykern import pkunit, pkio, pkdebug
    from chronver import git
    import os
    import subprocess

    with _setup() as d:
        pkio.mkdir_parent(d)
        with pkunit.pkexcept(subprocess.CalledProcessError):
            git.version()
        _, e = capsys.readouterr()
        pkunit.pkre("not a git repository", e)


@contextlib.contextmanager
def _setup():
    from pykern import pkunit, pkio, pkdebug
    from chronver import git
    import os

    with pkunit.save_chdir_work() as d:
        rv = d.join(".git")
        os.environ["GIT_DIR"] = str(rv)
        pkunit.pkeq(None, git.version())
        yield rv
