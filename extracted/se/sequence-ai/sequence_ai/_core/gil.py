"""
How soon a thread of the robot's program that wants the GIL takes it behind a busy one: Python's switch interval, which
sequence-ai shortens from Python's own 5 ms to 0.5 ms as it connects, unless the program set its own.

In one sentence: connect() → the switch interval still Python's own → 0.5 ms in its place, for the whole process → each
of an act's threads (the robot's, the act's, the stream's) takes the GIL within 0.5 ms behind a thread of pure Python,
not 5 ms. A program that set its own interval (sys.setswitchinterval) keeps it.

WHY: an act crosses three threads and its socket's reads and writes, each a wait for the GIL, and a robot's program runs
threads of its own beside the SDK (its arm's SDK reading the arm's state, its cameras). With one of them busy, each wait
was Python's 5 ms. {worker 4 10-31, dev, an act every 7 s beside one thread of pure Python: 190 ms an act at Python's
5 ms, 96 ms at 0.5 ms, 93 ms with no such thread; a real arm's act spent some 20 ms more outside its worker than a
lab robot's}
"""
from __future__ import annotations

import sys

PYTHON_S = 0.005
SHORT_S = 0.0005


def shorten() -> None:
    """The process's switch interval SHORT_S, from Python's own alone: one the program set stays as it set it."""
    if abs(sys.getswitchinterval() - PYTHON_S) < 1e-9:
        sys.setswitchinterval(SHORT_S)
