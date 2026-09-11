"""SDK-owned, version-routed UDF construction.

Public surface (populated across Tasks 9-12):

  * :func:`register_sidecar` / :func:`get_sidecar` — the registry the kernel
    package registers its sidecar *implementation* into.
  * :func:`install_udf_interceptor` — installs version-routing ``udf`` /
    ``pandas_udf`` into a notebook namespace.
  * the error types.

This package never imports the kernel and never spawns a subprocess.
"""

from typing import Any

from sagemaker_studio.utils.udf.errors import (  # noqa: F401
    UDFRegistrationError,
    UDFSidecarError,
    UDFUnsupportedError,
    format_sidecar_error,
)
from sagemaker_studio.utils.udf.inline_guard import (  # noqa: F401
    install_inline_guard,
    uninstall_inline_guard,
)
from sagemaker_studio.utils.udf.registry import (  # noqa: F401
    SidecarEntry,
    clear_registry,
    client_python_version,
    get_sidecar,
    normalize_python_version,
    register_sidecar,
    registered_versions,
    unregister_sidecar,
)

_ROUTED_NAMES = frozenset(
    {
        "SidecarPythonUDF",
        "SidecarUserDefinedFunction",
        "install_udf_interceptor",
        "install_udf_register_routing",
        "pandas_udf",
        "udf",
        "uninstall_udf_register_routing",
    }
)


def __getattr__(name: str) -> Any:
    """Resolve the routed names on first use.

    ``routed`` imports pyspark's Spark Connect client at module level; nothing
    else in this package does. Deferring it keeps that import off callers who
    only want the errors, the registry or the runtime detection.
    """
    if name in _ROUTED_NAMES:
        from sagemaker_studio.utils.udf import routed

        return getattr(routed, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "UDFRegistrationError",
    "UDFSidecarError",
    "UDFUnsupportedError",
    "format_sidecar_error",
    "SidecarEntry",
    "clear_registry",
    "client_python_version",
    "get_sidecar",
    "normalize_python_version",
    "register_sidecar",
    "registered_versions",
    "unregister_sidecar",
    "SidecarPythonUDF",
    "SidecarUserDefinedFunction",
    "install_udf_interceptor",
    "install_udf_register_routing",
    "uninstall_udf_register_routing",
    "pandas_udf",
    "udf",
    "install_inline_guard",
    "uninstall_inline_guard",
]
