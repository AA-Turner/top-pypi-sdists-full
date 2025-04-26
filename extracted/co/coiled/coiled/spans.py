import time
import uuid
from contextlib import contextmanager
from typing import Iterable, Optional

import dask.config

try:
    from distributed import span as distributed_span  # type: ignore
except ImportError:

    @contextmanager
    def distributed_span(*tags: str):
        yield str(uuid.uuid4())


@contextmanager
def span(cluster, name: Optional[str] = None, **kwargs):
    t0 = time.time()
    with distributed_span(name or "") as s:
        yield
    t1 = time.time()
    data = {
        **kwargs,
        "start": t0,
        "stop": t1,
        "callstack": callstack(*kwargs["callstack"]) if "callstack" in kwargs else None,
    }
    if not dask.config.get("coiled.analytics.computation.code.transmit", True):
        del data["callstack"]
    if hasattr(cluster, "add_span"):
        cluster.add_span(span_identifier=s, data=data)


def _callstack_item(idx, item):
    code = None
    relative_line = None
    filename = None

    if isinstance(item, dict):
        return {
            "frame_index": idx,
            "code": item.get("code"),
            "relative_line": item.get("relative_line"),
            "filename": item.get("filename"),
        }

    if isinstance(item, str):
        code = item
    elif isinstance(item, Iterable):
        code, filename, relative_line, *_ = *item, None, None
    return {
        "frame_index": idx,
        "code": code,
        "relative_line": relative_line,
        "filename": filename,
    }


def callstack(*args):
    """
    Format callstack to be collected by Coiled.

    Each argument is a callstack item (e.g., frame), and can be
    - string (just the code, no metadata)
    - tuple: (code,) or (code, filename) or (code, filename, line number)
    - dict: optional keys are "code", "relative_line", and "filename"

    For example, you might call this function as:
        callstack("python foo.py", ("print('hello')", "foo.py"))
    """
    return [_callstack_item(i, arg) for i, arg in enumerate(args)]
