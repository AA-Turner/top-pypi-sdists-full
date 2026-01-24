"""Exception hierarchy for C++ API system.

This module defines all custom exceptions used by the C++ API dynamic module system.
All exceptions inherit from CppApiError for easy catching of all API-related errors.
"""


class CppApiError(Exception):
    """Base exception for all C++ API errors.

    All custom exceptions in the C++ API system inherit from this base class,
    allowing users to catch all API-related errors with a single except clause.
    """
    pass


class CppBuildError(CppApiError):
    """Build or compilation failed.

    Raised when:
    - CMake configuration fails
    - C++ compilation fails
    - Plugin generator compilation fails
    - Build process times out
    - Build script not found
    """
    pass


class CppModuleNotFoundError(CppApiError):
    """Requested module not found in registry.

    Raised when:
    - include() called with non-existent module name
    - Module not registered in .module_registry.json
    - .cp file missing for requested module
    """
    pass


class CppModuleOutdatedError(CppApiError):
    """Module source files changed since last build.

    Raised when:
    - Source file hash mismatch detected
    - Header file hash mismatch detected
    - .cp file hash mismatch detected
    - auto_update=False and module is outdated
    """
    pass


class CppReloadWarning(UserWarning):
    """Warning about unsafe C extension reload.

    This warning is issued when:
    - rebuild() called but api module already loaded
    - User needs to restart Python to use new version
    - C extension hot-reload attempted (unsafe)
    """
    pass


class CppValidationError(CppApiError):
    """Generated code validation failed.

    Raised when:
    - Generated pybind11 code has syntax errors
    - Unbalanced braces detected
    - Missing required includes
    - Invalid generated code structure
    """
    pass


class CppParseError(CppApiError):
    """.cp file parsing failed.

    Raised when:
    - Malformed .cp file syntax
    - Invalid module name
    - Missing parentheses in FUNC/CLASS/VAR
    - Invalid syntax in PUBLIC() block
    """
    pass


class CppGeneratorError(CppApiError):
    """Plugin generator failed.

    Raised when:
    - Generator executable not found
    - Generator process crashed
    - Generator output invalid
    - Generator version mismatch
    """
    pass
