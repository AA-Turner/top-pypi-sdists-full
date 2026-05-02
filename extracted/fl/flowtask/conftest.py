"""Root conftest.py for the feat-007 flowtask-command-execution worktree.

Stubs out compiled Cython extension modules that are not built inside
this worktree so that test imports succeed without a full build step.
The stubs only need to satisfy Python's import machinery; their actual
attributes are not used by the workers test suite.
"""
import sys
from unittest.mock import MagicMock

# Stub all Cython-compiled and heavy modules that are compiled in the main
# repo but absent from this worktree.  These stubs only satisfy import
# machinery; no workers tests call into their implementations.
_STUB_MODULES = [
    # Parser Cython extensions
    "flowtask.parsers._yaml",
    "flowtask.parsers.toml",
    "flowtask.parsers.json",
    "flowtask.parsers.base",
    # Type stubs referenced transitively by parsers
    "flowtask.types.typedefs",
    # Utils modules that import Cython types
    "flowtask.utils.parserqs",
]

for _mod in _STUB_MODULES:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

# Ensure the stub for parserqs exports the two names used by argparser.py
_pqs = sys.modules["flowtask.utils.parserqs"]
if not hasattr(_pqs, "is_parseable"):
    _pqs.is_parseable = MagicMock(return_value=None)
if not hasattr(_pqs, "parse_arguments"):
    _pqs.parse_arguments = MagicMock(return_value=({}, {}))
