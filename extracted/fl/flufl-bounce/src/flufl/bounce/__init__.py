"""Email bounce detectors.

scan_message() returns the original recipients a bounce message reports as permanently failing, and
all_failures() returns the temporary and permanent failures as a pair.  Anyone writing a detector of
their own implements the BounceDetector protocol, returning Recipients sets or one of the
NoFailures, NoTemporaryFailures, and NoPermanentFailures constants.  Everything public is
re-exported here, so flufl.bounce is the only import path any consumer needs.
"""

from flufl.bounce._interfaces import (
    BounceDetector,
    NoFailures,
    NoPermanentFailures,
    NoTemporaryFailures,
    Recipients,
)
from flufl.bounce._scan import all_failures, scan_message


__version__ = '6.0.0'


# These names are re-exports, and a type checker has no way to tell a re-export from an
# implementation detail that merely happens to be imported.  mypy under --strict, and pyright in its
# default mode, reject `from flufl.bounce import scan_message` for an installed package unless the
# intent is stated, and this list states it.  (pyrefly and ty accept it either way.)
#
# A literal list is what makes that work, which is why this module doesn't use @public: the
# decorator builds __all__ at runtime, where no type checker can see it.  The list is kept honest in
# both directions: ruff's F401 flags an import missing from it, and tests/test_api.py a name in it
# that nothing defines.  (ruff's F822 would catch the latter too, but outside preview it skips
# __init__.py, where an undefined name might be a submodule.)
__all__ = [
    'BounceDetector',
    'NoFailures',
    'NoPermanentFailures',
    'NoTemporaryFailures',
    'Recipients',
    'all_failures',
    'scan_message',
]
