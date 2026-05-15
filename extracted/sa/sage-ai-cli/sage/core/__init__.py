"""Sage core.

Re-exports the most commonly-imported public API surface so callers can
write `from sage.core import FileDiscovery` without remembering which
submodule each class lives in. These exports are also asserted in
test_imports.py to catch accidental API breakage from refactors.
"""

# Public API — keep this list in sync with the assertion in
# sage/tests/test_imports.py::TestPublicAPI.
from sage.core.discovery import FileDiscovery, discover_files
from sage.core.task_priority import TaskPrioritizer
from sage.core.shell import safe_shell_exec


__all__ = [
    "FileDiscovery",
    "discover_files",
    "TaskPrioritizer",
    "safe_shell_exec",
]
