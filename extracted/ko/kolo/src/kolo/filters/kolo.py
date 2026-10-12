from __future__ import annotations

import os
import types

# Every module and subpackage of the kolo package. Kolo's own code must never
# show up in a user's trace, whichever thread runs it. Keep in sync with
# KOLO_MODULES in rust/src/filters.rs; tests/test_internal_threads.py and the
# Rust filter tests fail when a module is missing.
KOLO_MODULES = (
    "__init__.py",
    "__main__.py",
    "_attach.py",
    "_construction.py",
    "_emit_auto.py",
    "_kolotxt.py",
    "_paths.py",
    "_repr_audit.py",
    "build_frame_tree.py",
    "checks.py",
    "cli_mcp_shared.py",
    "config.py",
    "core.py",
    "db.py",
    "emit.py",
    "emit_flat.py",
    "filters/",
    "git.py",
    "kv.py",
    "mcp_plumbing.py",
    "mcp_server.py",
    "middleware.py",
    "monitoring.py",
    "navigator.py",
    "node.py",
    "open_in_pycharm.py",
    "plugins.py",
    "profiler.py",
    "pth_init.py",
    "pytest_plugin.py",
    "serialize.py",
    "settings.py",
    "sql_overview.py",
    "subtree_flush.py",
    "threads.py",
    "trace.py",
    "trace_build.py",
    "trace_container.py",
    "types.py",
    "upload.py",
    "utils.py",
    "version.py",
    "web/",
)
KOLO_MODULES = tuple(module.replace("/", os.sep) for module in KOLO_MODULES)
_KOLO_DIR = os.sep + "kolo" + os.sep


def kolo_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """Don't profile kolo code"""
    filename = frame.f_code.co_filename
    return kolo_filter_filename(filename)


def kolo_filter_filename(filename):
    start = filename.find(_KOLO_DIR)
    while start != -1:
        if filename.startswith(KOLO_MODULES, start + len(_KOLO_DIR)):
            return True
        start = filename.find(_KOLO_DIR, start + len(_KOLO_DIR) - 1)
    return False
