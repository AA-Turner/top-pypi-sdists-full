"""Folders every walk of a researcher's tree skips: rebuilt by a tool, never authored.
Each walk adds its own names to GENERATED_DIRS."""

from __future__ import annotations

import os

#: In every walk's skip list (the daemon's folder check, code snapshots, folder imports).
GENERATED_DIRS = frozenset({
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", ".ipynb_checkpoints",
})

#: The Cache Directory Tagging Specification (https://bford.info/cachedir/): a
#: tool that writes a cache or build tree marks it with a `CACHEDIR.TAG` file
#: whose first bytes are this signature. Cargo tags `target/`, Gradle its caches,
#: pytest `.pytest_cache`. A name list cannot cover these (`target` is also an
#: ordinary folder name); the folder's own declaration can. Live 2026-10-17: a
#: non-git run swept 3,674 files of cargo's `target/` (575 MB) up as its code.
CACHEDIR_TAG = "CACHEDIR.TAG"
CACHEDIR_SIGNATURE = b"Signature: 8a477f597d28d172789f06886806bc55"


def is_tagged_cache_dir(path: str) -> bool:
    """Does the folder at ``path`` declare itself a cache (``CACHEDIR.TAG``)?

    A tagged folder is rebuilt by the tool that tagged it, so it is never a
    run's code or output, whatever it is named. Unreadable means no."""
    try:
        with open(os.path.join(path, CACHEDIR_TAG), "rb") as fh:
            return fh.read(len(CACHEDIR_SIGNATURE)) == CACHEDIR_SIGNATURE
    except OSError:
        return False
