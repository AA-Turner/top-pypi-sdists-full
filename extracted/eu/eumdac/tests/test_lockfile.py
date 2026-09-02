import pytest
import tempfile
import os

from datetime import timedelta
from eumdac.lockfile import open_locked


@pytest.fixture(scope="function")
def lockfile_path(tmp_path):
    lockfile = tmp_path / "lockfile"
    yield lockfile
    if os.path.exists(lockfile):
        os.remove(lockfile)


def test_open_lock(lockfile_path):
    with open_locked(lockfile_path) as lf:
        assert os.path.exists(lockfile_path)


def test_multiple_lock(lockfile_path):
    with open_locked(lockfile_path) as lf:
        with open_locked(lockfile_path, timeout=timedelta(seconds=1)) as lf2:
            assert lf2 is None
