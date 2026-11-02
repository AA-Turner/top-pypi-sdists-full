"""
A warning the SDK gives its caller, pointed at the caller's own line - never at the SDK's.

In one sentence: warn(text) → the stack is walked past every frame of this distribution's own code (sequence_ai/, and
seq/ beside it) → warnings.warn names the first frame outside it, so a robot's program reads
`my_robot.py:42: UserWarning: …` where it read `…/site-packages/sequence_ai/act/run_loop.py:422: UserWarning: …` and
the SDK's own source line under it.
WHY walk the frames and not a fixed stacklevel: one warning is reached from act(), observe() and wait_until_ready() at
different depths, and a release keeps every line (tools/release/strip.py), so a depth off by one names a real SDK file
and line.
A warning given on one of the SDK's own threads (an act sent from its pool) has no line of the caller's under it: the
pool's frames are walked past too, and it is said as Python says one with no frame left ("sys:1", "<sys>:1" from 3.13),
never at a file of the SDK's or of the thread machinery's.

"""
from __future__ import annotations

import concurrent.futures
import os
import sys
import threading
import warnings



_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OWN = (*(os.path.join(os.path.dirname(_HERE), name) + os.sep for name in ("sequence_ai", "seq")),
        os.path.abspath(threading.__file__), os.path.dirname(os.path.abspath(concurrent.futures.__file__)) + os.sep)


def warn(message: str, category: type[Warning] = UserWarning) -> None:
    """Warn with `message`, as said at the first line of the caller's own code (outside this SDK) on the stack."""
    level, frame = 2, sys._getframe(1)
    while frame is not None and os.path.abspath(frame.f_code.co_filename).startswith(_OWN):
        frame, level = frame.f_back, level + 1
    warnings.warn(message, category, stacklevel=level)
