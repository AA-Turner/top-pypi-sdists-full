"""Public package surface for detecting test environments.

This module provides functions to detect if code is running in various test
environments including pytest, doctest, and setup.py test.
"""

from __future__ import annotations

from .behaviors import (
    CANONICAL_GREETING,
    emit_greeting,
    noop_main,
    raise_intentional_failure,
)
from .__init__conf__ import print_info
from .lib_detect_testenv import (
    PathLikeOrString,
    add_path_to_syspath,
    is_doctest_active,
    is_doctest_in_arg_string,
    is_pytest_active,
    is_setup_active,
    is_setup_test_active,
    is_testenv_active,
)

__all__ = [
    # Test environment detection functions
    "is_testenv_active",
    "is_doctest_active",
    "is_pytest_active",
    "is_setup_active",
    "is_setup_test_active",
    "is_doctest_in_arg_string",
    # Utility functions
    "add_path_to_syspath",
    "PathLikeOrString",
    # Legacy behavior functions
    "CANONICAL_GREETING",
    "emit_greeting",
    "noop_main",
    "print_info",
    "raise_intentional_failure",
]
