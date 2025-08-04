"""Module to daemonize the current process on Unix.

This module is intended to detach the current process from the controlling
terminal and run it in the background as a daemon, following the standard
Unix double-fork technique.

Only works on POSIX-compliant systems.
"""
#
# (C) Pywikibot team, 2007–2025
#
# Distributed under the terms of the MIT license.
#
from __future__ import annotations

import os
import stat
import sys
from enum import IntEnum
from pathlib import Path


class StandardFD(IntEnum):

    """File descriptors for standard input, output, and error."""

    STDIN = 0
    STDOUT = 1
    STDERR = 2


#: Global flag indicating whether the current process is daemonized.
is_daemon = False


def daemonize(close_fd: bool = True,
              chdir: bool = True,
              redirect_std: str | None = None) -> None:
    """Detach the current process and run as a daemon (Unix only).

    This function performs a standard double-fork to ensure that the
    calling process detaches from the terminal and runs in the background.

    :param close_fd: If ``True``, close stdin, stdout, and stderr and
        redirect them to ``/dev/null`` or the provided output file.
    :param chdir: If ``True``, change the current working directory to ``/``.
    :param redirect_std: If specified, redirect stdout and stderr to this file.
        Otherwise, output is discarded to ``/dev/null``.
    :raises NotImplementedError: If called on a non-POSIX system.
    :raises RuntimeError: If the fork or session creation fails.
    """
    if os.name != 'posix':
        raise NotImplementedError('daemonize() is only supported on Unix/POSIX systems.')

    # First fork
    try:
        if os.fork() > 0:
            os._exit(os.EX_OK)
    except OSError as e:
        raise RuntimeError(f'First fork failed: {e}')

    os.setsid()

    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            # Save child PID to .pid file
            pidfile = Path(sys.argv[0]).with_suffix('.pid')
            pidfile.write_text(str(pid), encoding='utf-8')
            os._exit(os.EX_OK)
    except OSError as e:
        raise RuntimeError(f'Second fork failed: {e}')

    global is_daemon
    is_daemon = True

    if chdir:
        os.chdir('/')

    if close_fd:
        _redirect_file_descriptors(redirect_std)


def _redirect_file_descriptors(output_file: str | None) -> None:
    """Redirect stdin, stdout, and stderr to /dev/null or a specified file.

    :param output_file: Path to the file where stdout and stderr should be redirected.
                        If None, all streams are redirected to ``/dev/null``.
    :type output_file: str or None
    """
    # Close STDIN, STDOUT, STDERR safely
    for fd in StandardFD:
        try:
            os.close(fd)
        except OSError:
            pass  # Already closed

    # Reopen STDIN to /dev/null
    dev_null = os.open('/dev/null', os.O_RDWR)
    os.dup2(dev_null, StandardFD.STDIN)

    # Open target file or use /dev/null for STDOUT and STDERR
    if output_file:
        mode = (
            stat.S_IRUSR | stat.S_IWUSR |
            stat.S_IRGRP | stat.S_IWGRP |
            stat.S_IROTH | stat.S_IWOTH
        )
        out_fd = os.open(output_file, os.O_WRONLY | os.O_APPEND | os.O_CREAT, mode)
    else:
        out_fd = os.open('/dev/null', os.O_RDWR)

    os.dup2(out_fd, StandardFD.STDOUT)
    os.dup2(out_fd, StandardFD.STDERR)
