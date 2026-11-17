# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A warning issued to the caller, attributed to the caller's own line, never to this package's.

In one sentence: warn(text) → the stack is walked past every frame of this package's own code → warnings.warn names the
first frame outside it, so a robot's program reads `my_robot.py:42: UserWarning: …`, not a line of this package.
WHY walk the frames and not a fixed stacklevel: one warning is reached at different depths, and a depth off by one names
a file and line of this package. A warning issued on a thread with no frame of the caller's code under it is shown as
Python shows one with no frame left ("sys:1", "<sys>:1" from 3.13).
"""
from __future__ import annotations

import concurrent.futures
import os
import sys
import threading
import warnings

# this package, as the path its files are run from, and the thread machinery a call on a pool's thread runs under
_OWN = (os.path.dirname(os.path.abspath(__file__)) + os.sep,
        os.path.abspath(threading.__file__), os.path.dirname(os.path.abspath(concurrent.futures.__file__)) + os.sep)


def warn(message: str, category: type[Warning] = UserWarning) -> None:
    """Warn with `message`, attributed to the first frame of the caller's own code (outside this package) on the
    stack."""
    level, frame = 2, sys._getframe(1)
    while frame is not None and os.path.abspath(frame.f_code.co_filename).startswith(_OWN):
        frame, level = frame.f_back, level + 1
    warnings.warn(message, category, stacklevel=level)
