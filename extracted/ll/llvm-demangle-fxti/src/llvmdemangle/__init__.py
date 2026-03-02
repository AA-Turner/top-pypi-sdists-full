import importlib

_ALL_VERSIONS = list(range(11, 22))
DEFAULT_VERSION = _ALL_VERSIONS[-1]

# Detect which backends are actually installed
SUPPORTED_VERSIONS = []
for _v in _ALL_VERSIONS:
    try:
        importlib.import_module(f"llvmdemangle._backend_{_v}")
        SUPPORTED_VERSIONS.append(_v)
    except ImportError:
        pass

_backend_cache = {}


def backend(llvm_version):
    """Return the backend module for a specific LLVM version.

    >>> v18 = backend(18)
    >>> v18.demangle("_Z3fooi")
    'foo(int)'
    >>> v18.LLVM_VERSION
    18
    """
    if llvm_version not in SUPPORTED_VERSIONS:
        raise ValueError(
            f"LLVM {llvm_version} backend not available. "
            f"Supported: {SUPPORTED_VERSIONS}"
        )
    if llvm_version not in _backend_cache:
        _backend_cache[llvm_version] = importlib.import_module(
            f"llvmdemangle._backend_{llvm_version}"
        )
    return _backend_cache[llvm_version]


# ---------------------------------------------------------------------------
# Re-export everything from the default backend for backward compatibility
# ---------------------------------------------------------------------------
_default = backend(max(SUPPORTED_VERSIONS))

LLVM_VERSION = _default.LLVM_VERSION

# Functions
demangle = _default.demangle
llvm_demangle = _default.llvm_demangle
itanium_demangle = _default.itanium_demangle
microsoft_demangle = _default.microsoft_demangle
rust_demangle = _default.rust_demangle
dlang_demangle = _default.dlang_demangle
non_microsoft_demangle = _default.non_microsoft_demangle
get_arm64ec_insertion_point = _default.get_arm64ec_insertion_point

# Flag constants
MSDF_NONE = _default.MSDF_NONE
MSDF_DUMP_BACKREFS = _default.MSDF_DUMP_BACKREFS
MSDF_NO_ACCESS_SPECIFIER = _default.MSDF_NO_ACCESS_SPECIFIER
MSDF_NO_CALLING_CONVENTION = _default.MSDF_NO_CALLING_CONVENTION
MSDF_NO_RETURN_TYPE = _default.MSDF_NO_RETURN_TYPE
MSDF_NO_MEMBER_TYPE = _default.MSDF_NO_MEMBER_TYPE
MSDF_NO_VARIABLE_TYPE = _default.MSDF_NO_VARIABLE_TYPE

# Class
ItaniumPartialDemangler = _default.ItaniumPartialDemangler

__all__ = [
    "DEFAULT_VERSION",
    "SUPPORTED_VERSIONS",
    "backend",
    "LLVM_VERSION",
    "demangle",
    "llvm_demangle",
    "itanium_demangle",
    "microsoft_demangle",
    "rust_demangle",
    "dlang_demangle",
    "non_microsoft_demangle",
    "get_arm64ec_insertion_point",
    "MSDF_NONE",
    "MSDF_DUMP_BACKREFS",
    "MSDF_NO_ACCESS_SPECIFIER",
    "MSDF_NO_CALLING_CONVENTION",
    "MSDF_NO_RETURN_TYPE",
    "MSDF_NO_MEMBER_TYPE",
    "MSDF_NO_VARIABLE_TYPE",
    "ItaniumPartialDemangler",
]
