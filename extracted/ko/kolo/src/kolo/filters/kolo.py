from __future__ import annotations

import os
import types

KOLO_PATHS = (
    "/kolo/checks.py",
    "/kolo/config.py",
    "/kolo/core.py",
    "/kolo/db.py",
    "/kolo/filters/",
    "/kolo/git.py",
    "/kolo/__init__.py",
    "/kolo/__main__.py",
    "/kolo/middleware.py",
    "/kolo/monitoring.py",
    "/kolo/_paths.py",
    "/kolo/plugins.py",
    "/kolo/profiler.py",
    "/kolo/pth_init.py",
    "/kolo/pytest_plugin.py",
    "/kolo/serialize.py",
    "/kolo/trace_container.py",
    "/kolo/trace_build.py",
    "/kolo/utils.py",
    "/kolo/version.py",
)
KOLO_PATHS = tuple(os.path.normpath(path) for path in KOLO_PATHS)


def kolo_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """Don't profile kolo code"""
    filename = frame.f_code.co_filename
    return kolo_filter_filename(filename)


def kolo_filter_filename(filename):
    return any(path in filename for path in KOLO_PATHS)
