# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import collections
import itertools
import sys
import traceback
from functools import lru_cache
from types import FrameType

from contrast import AGENT_CURR_WORKING_DIR
from contrast.utils.decorators import fail_quietly
from contrast_fireball import AssessStackFrame
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


APPLIES_MARKER = "cs__"
PATCH_MARKER = "__cs"
PY_FILE_EXTENSION = ".py"
UTILS_MODULES = "contrast/utils"
NONETYPE = "NoneType"

CONTRAST_EXTENSIONS = (
    "contrast_vendor",
    "contrast_rewriter",
    "contrast/assess_extensions",
    "contrast/patches",
)
DJANGO_EXCEPTION_PATH = "core/handlers/exception.py"
DJANGO_DEPRECATION_PATH = "utils/deprecation.py"
SITE_PACKAGES = "site-packages"

# PERF: limit the number of stack frames to not use as much memory.
STACK_LIMIT = 20


@fail_quietly("Failed to build stacktrace for event", return_value=[])
def build_stack(limit=STACK_LIMIT) -> StackSummary:
    return extract_stack(limit=limit)


@fail_quietly("Failed to clean stacktrace for event", return_value=[])
def clean_stack(frames: StackSummary):
    return [to_element(x) for x in reversed(frames)]


@fail_quietly("Failed to convert event")
def to_element(summary: traceback.FrameSummary):
    from contrast.reporting.reporting_client import StackFrame

    return StackFrame(
        line_number=summary.lineno,
        file_name=filename_formatter(summary.filename),
        declaring_class=summary.filename,
        method_name=summary.name,
    )


@fail_quietly("Failed to clean assess stacktrace", return_value=[])
def to_assess_stack(summary: StackSummary):
    return [
        AssessStackFrame(
            line_number=frame.lineno or -1,
            file=filename_formatter(frame.filename),
            method=frame.name,
        )
        for frame in reversed(summary)
    ]


def extract_stack(f: FrameType | None = None, limit=None):
    """Extract the raw traceback from the current stack frame.

    Instrumentation frames are filtered out of the results and are
    not included in the calculation of limits.

    The return value has the same format as for extract_tb().  The
    optional 'f' and 'limit' arguments have the same meaning as for
    print_stack().  Each item in the list is a quadruple (filename,
    line number, function name, text), and the entries are in order
    from oldest to newest stack frame.
    """
    if f is None:
        f = sys._getframe().f_back
    if f is None:
        return StackSummary()
    stack = StackSummary.extract(walk_stack(f), limit=limit, lookup_lines=False)
    stack.reverse()
    return stack


def walk_stack(f: FrameType | None):
    """Walk a stack yielding the frame and line number for each frame.

    This will follow f.f_back from the given frame.

    Unlike traceback.walk_stack, if no frame is given, no frames are
    yielded.

    It will also filter out frames belonging to Contrast instrumentation.
    """
    while f is not None:
        if acceptable_frame(f):
            yield f, f.f_lineno
        f = f.f_back


def acceptable_frame(frame: FrameType):
    """
    Return true if frame does NOT belong to Contrast instrumentation.
    """

    filename = frame.f_code.co_filename
    name = frame.f_code.co_name
    return (
        "/contrast/" not in filename
        and UTILS_MODULES not in filename
        and not any(extension in filename for extension in CONTRAST_EXTENSIONS)
        and not name.startswith(APPLIES_MARKER)
        and not name.startswith(PATCH_MARKER)
        and not filename.endswith(DJANGO_EXCEPTION_PATH)
        and not filename.endswith(DJANGO_DEPRECATION_PATH)
    )


class StackSummary(list[traceback.FrameSummary]):
    """A stack of frames."""

    @classmethod
    def extract(cls, frame_gen, *, limit=None, lookup_lines=True, capture_locals=False):
        """Create a StackSummary from a traceback or stack object.

        Like traceback.StackSummary.extract, but without linecache to avoid
        os.stat calls and improve performance.

        :param frame_gen: A generator that yields (frame, lineno) tuples to
            include in the stack.
        :param limit: None to include all frames or the number of frames to
            include.
        :param lookup_lines: If True, lookup lines for each frame immediately,
            otherwise lookup is deferred until the frame is rendered.
        :param capture_locals: If True, the local variables from each frame will
            be captured as object representations into the FrameSummary.
        """
        if limit is None:
            limit = getattr(sys, "tracebacklimit", None)
            if limit is not None and limit < 0:
                limit = 0
        if limit is not None:
            if limit >= 0:
                frame_gen = itertools.islice(frame_gen, limit)
            else:
                frame_gen = collections.deque(frame_gen, maxlen=-limit)

        result = cls()
        fnames = set()
        for f, lineno in frame_gen:
            co = f.f_code
            filename = co.co_filename
            name = co.co_name

            fnames.add(filename)
            # Must defer line lookups until we have called checkcache.
            f_locals = f.f_locals if capture_locals else None
            result.append(
                traceback.FrameSummary(
                    filename, lineno, name, lookup_line=False, locals=f_locals
                )
            )
        # If immediate lookup was desired, trigger lookups now.
        if lookup_lines:
            for f in result:
                _ = f.line
        return result


def build_and_clean_stack(depth=STACK_LIMIT):
    """
    Perform both build and clean steps.
    """
    return clean_stack(build_stack(limit=depth))


SORTED_FILENAME_SEARCH_PATH = sorted(
    set(sys.path) | {AGENT_CURR_WORKING_DIR}, key=len, reverse=True
)


@fail_quietly("Unable to create file_name")
@lru_cache(maxsize=512)
def filename_formatter(file_name: str):
    # PERF: This method is called hundreds of times, so be mindful
    # of what additional computations are added.

    if file_name.startswith("<frozen"):
        return file_name

    for sys_path in SORTED_FILENAME_SEARCH_PATH:
        if file_name.startswith(sys_path):
            file_name = file_name.removeprefix(sys_path)
            break

    return file_name.replace("/", ".").lstrip(".")
