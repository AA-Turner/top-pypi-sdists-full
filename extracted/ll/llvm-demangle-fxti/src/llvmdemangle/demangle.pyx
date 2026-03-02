# distutils: language = c++

"""Python bindings for LLVM Demangle library.

Exposes Itanium, Microsoft, Rust, and D language demanglers,
plus the ItaniumPartialDemangler for querying symbol components.
"""

from libc.stdlib cimport free
from libc.stddef cimport size_t
from libcpp.string cimport string
from libcpp cimport bool as cbool

# ---------------------------------------------------------------------------
# C++ declarations: ItaniumPartialDemangler (must come before shim decls)
# ---------------------------------------------------------------------------
cdef extern from "llvm/Demangle/Demangle.h" namespace "llvm":
    cdef cppclass CppItaniumPartialDemangler "llvm::ItaniumPartialDemangler":
        CppItaniumPartialDemangler() except +
        cbool partialDemangle(const char *MangledName)
        cbool hasFunctionQualifiers() const
        cbool isCtorOrDtor() const
        cbool isFunction() const
        cbool isData() const
        cbool isSpecialName() const

# ---------------------------------------------------------------------------
# C++ declarations: shim functions
# ---------------------------------------------------------------------------
cdef extern from "demangle_shim.h":
    const cbool SHIM_HAS_RUST
    const cbool SHIM_HAS_DLANG
    const cbool SHIM_HAS_NON_MICROSOFT
    const cbool SHIM_HAS_PARSE_PARAMS
    const cbool SHIM_HAS_NO_VARIABLE_TYPE
    const cbool SHIM_HAS_ARM64EC

    string shim_demangle(const char *name)
    char *shim_itanium_demangle(const char *name, cbool parse_params)
    char *shim_microsoft_demangle(const char *name, int flags, size_t *n_read)
    char *shim_rust_demangle(const char *name)
    char *shim_dlang_demangle(const char *name)
    int shim_non_microsoft_demangle(const char *name,
                                    cbool can_have_leading_dot,
                                    cbool parse_params,
                                    string *out_result)
    long long shim_get_arm64ec_insertion_point(const char *name)

    # Batch extraction for ItaniumPartialDemangler
    cdef cppclass ShimIPDResult:
        string full_name
        string base_name
        string decl_context
        string func_name
        string params
        string return_type
        cbool has_full_name
        cbool has_base_name
        cbool has_decl_context
        cbool has_func_name
        cbool has_params
        cbool has_return_type

    void shim_ipd_extract_all(CppItaniumPartialDemangler *d, ShimIPDResult *r)

# ---------------------------------------------------------------------------
# LLVM version constant (injected by setup.py via -DLLVM_MAJOR)
# ---------------------------------------------------------------------------
cdef extern from *:
    """
    #ifndef LLVM_MAJOR
    #define LLVM_MAJOR 0
    #endif
    static const int _LLVM_MAJOR = LLVM_MAJOR;
    """
    int _LLVM_MAJOR

LLVM_VERSION = _LLVM_MAJOR

# ---------------------------------------------------------------------------
# Microsoft demangle flag constants
# ---------------------------------------------------------------------------
MSDF_NONE = 0
MSDF_DUMP_BACKREFS = 1 << 0
MSDF_NO_ACCESS_SPECIFIER = 1 << 1
MSDF_NO_CALLING_CONVENTION = 1 << 2
MSDF_NO_RETURN_TYPE = 1 << 3
MSDF_NO_MEMBER_TYPE = 1 << 4
MSDF_NO_VARIABLE_TYPE = 1 << 5  # LLVM >= 14

# ---------------------------------------------------------------------------
# Helper: extract C string to Python, then free
# ---------------------------------------------------------------------------
cdef inline object _cstr_to_py_or_none(char *p):
    """Convert malloc'd C string to Python str (or None), then free it."""
    if p == NULL:
        return None
    try:
        return p.decode("utf-8")
    finally:
        free(p)

# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

def demangle(name):
    """Auto-detect mangling scheme and demangle.

    Returns the demangled string, or the original string if unrecognized.

    >>> demangle("_Z3fooi")
    'foo(int)'
    >>> demangle("?foo@@YAHH@Z")
    'int __cdecl foo(int)'
    """
    cdef bytes b = name.encode("utf-8")
    cdef string result = shim_demangle(b)
    return result.decode("utf-8")


# Backward-compatible alias
def llvm_demangle(name):
    """Alias for demangle(). Kept for backward compatibility."""
    return demangle(name)


def itanium_demangle(name, *, bint parse_params=True):
    """Demangle an Itanium C++ ABI mangled symbol.

    Args:
        name: Mangled symbol name (e.g. '_Z3fooi').
        parse_params: If False, omit function parameters from the result.
            Effective on LLVM >= 18; ignored on older versions.

    Returns:
        Demangled string, or None if the input is not a valid Itanium mangling.

    >>> itanium_demangle("_Z3fooi")
    'foo(int)'
    >>> itanium_demangle("_Z3fooi", parse_params=False)  # LLVM 18+
    'foo'
    """
    cdef bytes b = name.encode("utf-8")
    cdef char *result = shim_itanium_demangle(b, parse_params)
    return _cstr_to_py_or_none(result)


def microsoft_demangle(name, *, int flags=0):
    """Demangle a Microsoft Visual C++ mangled symbol.

    Args:
        name: Mangled symbol name (e.g. '?foo@@YAHH@Z').
        flags: Bitwise OR of MSDF_* constants to control output format.

    Returns:
        Tuple of (demangled_name, n_read) on success, or None on failure.
        n_read is the number of input bytes consumed.

    >>> microsoft_demangle("?foo@@YAHH@Z")
    ('int __cdecl foo(int)', 12)
    >>> microsoft_demangle("?foo@@YAHH@Z", flags=MSDF_NO_CALLING_CONVENTION)
    ('int foo(int)', 12)
    """
    cdef bytes b = name.encode("utf-8")
    cdef size_t n_read = 0
    cdef char *result = shim_microsoft_demangle(b, flags, &n_read)
    if result == NULL:
        return None
    try:
        py_str = result.decode("utf-8")
    finally:
        free(result)
    return (py_str, <int>n_read)


def rust_demangle(name):
    """Demangle a Rust v0 mangled symbol.

    Requires LLVM >= 13.

    Args:
        name: Mangled symbol name (e.g. '_RNvC8my_crate3foo').

    Returns:
        Demangled string, or None if the input is not a valid Rust mangling.

    Raises:
        NotImplementedError: If compiled with LLVM < 13.

    >>> rust_demangle("_RNvC8my_crate3foo")
    'my_crate::foo'
    """
    if not SHIM_HAS_RUST:
        raise NotImplementedError(
            f"rust_demangle() requires LLVM >= 13 (compiled with LLVM {LLVM_VERSION})")
    cdef bytes b = name.encode("utf-8")
    cdef char *result = shim_rust_demangle(b)
    return _cstr_to_py_or_none(result)


def dlang_demangle(name):
    """Demangle a D language mangled symbol.

    Requires LLVM >= 14.

    Args:
        name: Mangled symbol name (e.g. '_Dmain').

    Returns:
        Demangled string, or None if the input is not a valid D mangling.

    Raises:
        NotImplementedError: If compiled with LLVM < 14.

    >>> dlang_demangle("_Dmain")
    'D main'
    """
    if not SHIM_HAS_DLANG:
        raise NotImplementedError(
            f"dlang_demangle() requires LLVM >= 14 (compiled with LLVM {LLVM_VERSION})")
    cdef bytes b = name.encode("utf-8")
    cdef char *result = shim_dlang_demangle(b)
    return _cstr_to_py_or_none(result)


def non_microsoft_demangle(name, *, bint can_have_leading_dot=True,
                           bint parse_params=True):
    """Demangle a non-Microsoft symbol (Itanium, Rust, or D).

    Requires LLVM >= 14. The parse_params option requires LLVM >= 18
    (ignored on older versions).

    Args:
        name: Mangled symbol name.
        can_have_leading_dot: If True, a leading '.' is preserved in output.
        parse_params: If False, omit function parameters.

    Returns:
        Demangled string, or None on failure.

    Raises:
        NotImplementedError: If compiled with LLVM < 14.
    """
    if not SHIM_HAS_NON_MICROSOFT:
        raise NotImplementedError(
            f"non_microsoft_demangle() requires LLVM >= 14 "
            f"(compiled with LLVM {LLVM_VERSION})")
    cdef bytes b = name.encode("utf-8")
    cdef string out
    cdef int rc = shim_non_microsoft_demangle(b, can_have_leading_dot,
                                              parse_params, &out)
    if rc <= 0:
        return None
    return out.decode("utf-8")


def get_arm64ec_insertion_point(name):
    """Get the Arm64EC insertion point in a mangled name.

    Requires LLVM >= 19.

    Returns:
        Integer index, or None if not applicable.

    Raises:
        NotImplementedError: If compiled with LLVM < 19.
    """
    if not SHIM_HAS_ARM64EC:
        raise NotImplementedError(
            f"get_arm64ec_insertion_point() requires LLVM >= 19 "
            f"(compiled with LLVM {LLVM_VERSION})")
    cdef bytes b = name.encode("utf-8")
    cdef long long result = shim_get_arm64ec_insertion_point(b)
    if result < 0:
        return None
    return int(result)


# ---------------------------------------------------------------------------
# ItaniumPartialDemangler wrapper
# ---------------------------------------------------------------------------

cdef class ItaniumPartialDemangler:
    """Parse Itanium C++ ABI symbols into an AST and query components.

    Usage::

        d = ItaniumPartialDemangler("_ZN3Foo3barEid")
        print(d.full_name)           # 'Foo::bar(int, double)'
        print(d.function_base_name)  # 'bar'
        print(d.function_parameters) # '(int, double)'
        print(d.is_function)         # True

    Raises:
        ValueError: If the mangled name cannot be parsed.
    """
    cdef CppItaniumPartialDemangler _impl
    # Cached string results (extracted in batch at parse time)
    cdef object _full_name
    cdef object _base_name
    cdef object _decl_context
    cdef object _func_name
    cdef object _params
    cdef object _return_type

    def __cinit__(self, name):
        cdef bytes b = name.encode("utf-8")
        cdef cbool err = self._impl.partialDemangle(b)
        if err:
            raise ValueError(f"Failed to parse mangled name: {name}")
        self._full_name = None
        self._base_name = None
        self._decl_context = None
        self._func_name = None
        self._params = None
        self._return_type = None
        self._extract_all()

    cdef void _extract_all(self):
        """Extract all string properties in a single C++ call."""
        cdef ShimIPDResult r
        shim_ipd_extract_all(&self._impl, &r)
        if r.has_full_name:
            self._full_name = r.full_name.decode("utf-8")
        if r.has_base_name:
            self._base_name = r.base_name.decode("utf-8")
        if r.has_decl_context:
            self._decl_context = r.decl_context.decode("utf-8")
        if r.has_func_name:
            self._func_name = r.func_name.decode("utf-8")
        if r.has_params:
            self._params = r.params.decode("utf-8")
        if r.has_return_type:
            self._return_type = r.return_type.decode("utf-8")

    @property
    def full_name(self):
        """Full demangled name, e.g. 'void Foo::bar<int>(int)'."""
        return self._full_name

    @property
    def function_base_name(self):
        """Base name without namespace or template args.

        e.g. 'bar' for '_ZN3Foo3barIiEEvT_' (Foo::bar<int>).
        Returns None if not a function.
        """
        return self._base_name

    @property
    def function_decl_context(self):
        """Namespace/class context.

        e.g. 'Foo' for 'Foo::bar'. Empty string for top-level functions.
        """
        return self._decl_context

    @property
    def function_name(self):
        """Full function name with context and template args.

        e.g. 'Foo::bar<int>'. Returns None if not a function.
        """
        return self._func_name

    @property
    def function_parameters(self):
        """Parameter types string.

        e.g. '(int, double)'. Returns None if not a function.
        """
        return self._params

    @property
    def function_return_type(self):
        """Return type string.

        e.g. 'void'. Empty string if not applicable.
        """
        return self._return_type

    @property
    def has_function_qualifiers(self):
        """Whether the function has cv or reference qualifiers.

        This implies the function is a non-static member function.
        """
        return self._impl.hasFunctionQualifiers()

    @property
    def is_ctor_or_dtor(self):
        """Whether the symbol describes a constructor or destructor."""
        return self._impl.isCtorOrDtor()

    @property
    def is_function(self):
        """Whether the symbol describes a function."""
        return self._impl.isFunction()

    @property
    def is_data(self):
        """Whether the symbol describes a variable/data."""
        return self._impl.isData()

    @property
    def is_special_name(self):
        """Whether the symbol is a compiler-generated special name.

        Examples: vtables, typeinfo, guard variables.
        """
        return self._impl.isSpecialName()
