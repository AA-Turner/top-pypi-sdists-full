"""Resolve where the testmu binding writes downloaded files.

Public API:
    testmu.downloads_path(name) — absolute path joining the resolved Downloads
                                  dir with the given filename. Used by
                                  generated tests for set_input_files().

Internal:
    _resolve_downloads_dir() — bare directory. Reused by _session.py so the
                               env-var precedence is defined once.
"""
import os


def _resolve_downloads_dir() -> str:
    env_path = os.getenv("TESTMU_DOWNLOAD_PATH", "").strip()
    if env_path:
        return env_path
    return os.path.join(os.path.expanduser("~"), "Downloads")


def downloads_path(name: str) -> str:
    return os.path.join(_resolve_downloads_dir(), name)
