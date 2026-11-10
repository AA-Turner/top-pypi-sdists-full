import os
import time as ttime

import pytest


@pytest.fixture(scope="session", autouse=True)
def print_open_file_descriptors(request):
    yield
    ttime.sleep(1)
    pid = os.getpid()
    fd_dir = f"/proc/{pid}/fd"
    fd_entries = sorted(os.listdir(fd_dir), key=int)
    msg = f"+++ PID={pid} OPEN FILE DESCRIPTORS = {len(fd_entries)}"
    # terminalreporter works on CI (it is supposed to work locally, but it doesn't)
    reporter = request.config.pluginmanager.get_plugin("terminalreporter")
    reporter.write_line(msg)
    # /dev/tty bypasses all pytest capture layers (local use only)
    try:
        with open("/dev/tty", "w") as tty:
            tty.write("\n" + msg + "\n")
    except OSError:
        import sys

        sys.stderr.write("\n" + msg + "\n")
        sys.stderr.flush()
