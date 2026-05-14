from inspect import findsource
from types import FrameType
from typing import Tuple


def get_source_object_starting(f: FrameType) -> Tuple[str, int, int]:
    start = f.f_lineno - 1
    lines, _ = findsource(f)
    start = max(start, 1)
    source_code = ""
    for i, cc in enumerate(lines[start:]):
        source_code += cc
        if cc.strip().endswith(")"):
            break
    # +1 to correct for 0 indexing
    return source_code, start + 1, start + i + 1
