"""Cheap call-stack inspection (stdlib only, no package imports — safe anywhere).

``inspect.stack()`` reads source for every frame, which calls
``inspect.getmodule`` and so touches every module in ``sys.modules``; each
LazyLoader dependency (pandas, geopandas, PyPDF2, ...) is then really imported.
``light_stack()`` walks frames directly and returns the fields callers use.
"""
import sys
from collections import namedtuple

FrameLite = namedtuple("FrameLite", "frame filename lineno function")


def light_stack():
    """Like ``inspect.stack()`` called from the caller: index 0 is the caller."""
    frame = sys._getframe(1)
    out = []
    while frame is not None:
        code = frame.f_code
        out.append(FrameLite(frame, code.co_filename, frame.f_lineno, code.co_name))
        frame = frame.f_back
    return out
