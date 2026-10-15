"""Static certification of ``__repr__`` code for cross-event repr reuse.

Kolo's native encoder may reuse the text of an earlier ``repr()`` of the same
object when it can prove the repr would produce the same text again (see
``rust/src/utils/repr_reuse.rs``). That proof has two halves:

* this module decides, once per code object, *what a function does*: either
  its bytecode is identical to one of a small set of audited reference
  implementations, or it is a straight-line f-string over attributes of
  ``self`` that the verifier below fully understands;
* the native side then models exactly what that code reads (attributes,
  slots, globals, closure cells, nested reprs) and guards every read.

Code is identified by its bytecode, constants, names and shape, never by its
name, module or qualname: a function with identical bytecode has identical
semantics given identical inputs, and the native side guards the inputs
(globals, builtins, closure cells, attribute resolution) separately.

``classify`` runs Python, so the native side only calls it outside the window
between taking a dependency snapshot and running the real repr.
"""

from __future__ import annotations

import dis
import sys
import types
from typing import Any, List

# Verdict kinds. Mirrored in rust/src/utils/repr_reuse.rs.
FSTRING = 1
DC_WRAPPER_312 = 2
RECURSIVE_REPR_WRAPPER = 3
SIMPLE_GETTER = 4
NAMEDTUPLE_REPR = 5
JINJA_CONTEXT_REPR = 10
JINJA_GET_ALL = 11
JINJA_MACRO_REPR = 12
RICH_AUTO_REPR = 20
RICH_STYLE_RICH_REPR = 21
RICH_BIT_GET = 22
RICH_COLOR_RICH_REPR = 23
RICH_TEXT_PLAIN = 26
ENUM_PROPERTY_GET = 30

# f-string field conversions, mirrored natively.
CONV_FORMAT = 0
CONV_STR = 1
CONV_REPR = 2
CONV_EXACT_STR = 3

ROOT_SELF = 0
ROOT_TYPE_OF_SELF = 1

_CO_SEMANTIC_FLAGS = (
    0x0001 | 0x0002 | 0x0004 | 0x0008 | 0x0020 | 0x0080 | 0x0100 | 0x0200
)

# 3.12.5 is the oldest 3.12 the sys.monitoring use in `_runs_what_it_shows` was checked on
# (early 3.12 releases crashed instrumenting code with live frames).
SUPPORTED = (
    (3, 12, 5) <= sys.version_info[:3]
    and sys.version_info[:2] <= (3, 15)
    and (sys.implementation.name == "cpython")
)


_CONST_TYPES = (str, bytes, int, float, complex, bool, type(None), type(Ellipsis))


def _const_key(value):
    if isinstance(value, types.CodeType):
        return ("code", _code_key(value))
    if type(value) is tuple:
        return ("tuple", tuple(_const_key(item) for item in value))
    if type(value) is slice:
        # 3.14+ folds constant slices (`x[:]`) into `co_consts`.
        return (
            "slice",
            tuple(_const_key(v) for v in (value.start, value.stop, value.step)),
        )
    if type(value) is frozenset:
        return ("frozenset", tuple(sorted(repr(_const_key(item)) for item in value)))
    # Only exact compiled literal types match references; preserve repr’s distinction between -0.0 and 0.0.
    if type(value) in _CONST_TYPES:
        return (type(value).__name__, repr(value))
    return ("unknown", id(value))


# Set on interpreter shims; changes how RESUME interacts with monitoring.
_CO_NO_MONITORING_EVENTS = 0x2000000


def _localsplus_names(code):
    """Every local, cell and free variable slot, in frame order.

    The public name tables are filtered views: a code object built with
    marshal can carry extra slots that appear in none of them but still
    move where free variables are copied (and so what LOAD_DEREF reads).
    """
    names: List[str] = []
    while True:
        try:
            names.append(code._varname_from_oparg(len(names)))
        except IndexError:
            return tuple(names)


def _code_key(code):
    """Everything about a code object that affects what it executes.

    Names, qualnames, filenames and line tables are excluded; so are the
    informational CO_NESTED and `from __future__` flags, which do not change
    how already-compiled bytecode runs.
    """
    return (
        code.co_code,
        tuple(_const_key(const) for const in code.co_consts),
        code.co_names,
        code.co_varnames,
        code.co_freevars,
        code.co_cellvars,
        code.co_argcount,
        code.co_posonlyargcount,
        code.co_kwonlyargcount,
        code.co_nlocals,
        code.co_flags & _CO_SEMANTIC_FLAGS,
        code.co_stacksize,
        code.co_exceptiontable,
        _localsplus_names(code),
    )


def _find_code(code, qualname):
    if code.co_qualname == qualname:
        return code
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            found = _find_code(const, qualname)
            if found is not None:
                return found
    return None


# Copied verbatim from the audited library versions: any bytecode difference fails certification.
_REFERENCES = [
    (
        DC_WRAPPER_312,
        "_recursive_repr.<locals>.wrapper",
        """
import functools
import _thread

def _recursive_repr(user_function):
    # Decorator to make a repr function return "..." for a recursive
    # call.
    repr_running = set()

    @functools.wraps(user_function)
    def wrapper(self):
        key = id(self), _thread.get_ident()
        if key in repr_running:
            return '...'
        repr_running.add(key)
        try:
            result = user_function(self)
        finally:
            repr_running.discard(key)
        return result
    return wrapper
""",
    ),
    (
        RECURSIVE_REPR_WRAPPER,
        "recursive_repr.<locals>.decorating_function.<locals>.wrapper",
        """
def recursive_repr(fillvalue='...'):
    'Decorator to make a repr function return fillvalue for a recursive call'

    def decorating_function(user_function):
        repr_running = set()

        def wrapper(self):
            key = id(self), get_ident()
            if key in repr_running:
                return fillvalue
            repr_running.add(key)
            try:
                result = user_function(self)
            finally:
                repr_running.discard(key)
            return result

        return wrapper

    return decorating_function
""",
    ),
    (
        NAMEDTUPLE_REPR,
        "namedtuple.<locals>.__repr__",
        """
def namedtuple(typename, field_names, *, rename=False, defaults=None, module=None):
    repr_fmt = None
    def __repr__(self):
        'Return a nicely formatted representation string'
        return self.__class__.__name__ + repr_fmt % self
    return __repr__
""",
    ),
    (
        JINJA_CONTEXT_REPR,
        "Context.__repr__",
        """
class Context:
    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.get_all()!r} of {self.name!r}>"
""",
    ),
    (
        JINJA_GET_ALL,
        "Context.get_all",
        '''
class Context:
    def get_all(self) -> t.Dict[str, t.Any]:
        """Return the complete context as dict including the exported
        variables.  For optimizations reasons this might not return an
        actual copy so be careful with using it.
        """
        if not self.vars:
            return self.parent
        if not self.parent:
            return self.vars
        return dict(self.parent, **self.vars)
''',
    ),
    (
        JINJA_MACRO_REPR,
        "Macro.__repr__",
        """
class Macro:
    def __repr__(self) -> str:
        name = "anonymous" if self.name is None else repr(self.name)
        return f"<{type(self).__name__} {name}>"
""",
    ),
    (
        RICH_AUTO_REPR,
        "auto.<locals>.do_replace.<locals>.auto_repr",
        '''
def auto(
    cls: Optional[Type[T]] = None, *, angular: Optional[bool] = None
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    """Class decorator to create __repr__ from __rich_repr__"""

    def do_replace(cls: Type[T], angular: Optional[bool] = None) -> Type[T]:
        def auto_repr(self: T) -> str:
            """Create repr string from __rich_repr__"""
            repr_str: List[str] = []
            append = repr_str.append

            angular: bool = getattr(self.__rich_repr__, "angular", False)  # type: ignore[attr-defined]
            for arg in self.__rich_repr__():  # type: ignore[attr-defined]
                if isinstance(arg, tuple):
                    if len(arg) == 1:
                        append(repr(arg[0]))
                    else:
                        key, value, *default = arg
                        if key is None:
                            append(repr(value))
                        else:
                            if default and default[0] == value:
                                continue
                            append(f"{key}={value!r}")
                else:
                    append(repr(arg))
            if angular:
                return f"<{self.__class__.__name__} {' '.join(repr_str)}>"
            else:
                return f"{self.__class__.__name__}({', '.join(repr_str)})"
''',
    ),
    (
        RICH_STYLE_RICH_REPR,
        "Style.__rich_repr__",
        """
class Style:
    def __rich_repr__(self) -> Result:
        yield "color", self.color, None
        yield "bgcolor", self.bgcolor, None
        yield "bold", self.bold, None,
        yield "dim", self.dim, None,
        yield "italic", self.italic, None
        yield "underline", self.underline, None,
        yield "blink", self.blink, None
        yield "blink2", self.blink2, None
        yield "reverse", self.reverse, None
        yield "conceal", self.conceal, None
        yield "strike", self.strike, None
        yield "underline2", self.underline2, None
        yield "frame", self.frame, None
        yield "encircle", self.encircle, None
        yield "link", self.link, None
        if self._meta:
            yield "meta", self.meta
""",
    ),
    (
        RICH_BIT_GET,
        "_Bit.__get__",
        """
class _Bit:
    def __get__(self, obj: "Style", objtype: Type["Style"]) -> Optional[bool]:
        if obj._set_attributes & self.bit:
            return obj._attributes & self.bit != 0
        return None
""",
    ),
    (
        RICH_COLOR_RICH_REPR,
        "Color.__rich_repr__",
        """
class Color:
    def __rich_repr__(self) -> Result:
        yield self.name
        yield self.type
        yield "number", self.number, None
        yield "triplet", self.triplet, None
""",
    ),
    (
        RICH_TEXT_PLAIN,
        "Text.plain",
        '''
class Text:
    @property
    def plain(self) -> str:
        """Get the text as a single string."""
        if len(self._text) != 1:
            self._text[:] = ["".join(self._text)]
        return self._text[0]
''',
    ),
    (
        ENUM_PROPERTY_GET,
        "property.__get__",
        """
class property:
    def __get__(self, instance, ownerclass=None):
        if instance is None:
            if self.member is not None:
                return self.member
            else:
                raise AttributeError(
                        '%r has no attribute %r' % (ownerclass, self.name)
                        )
        if self.fget is not None:
            # use previous enum.property
            return self.fget(instance)
        elif self._attr_type == 'attr':
            # look up previous attibute
            return getattr(self._cls_type, self.name)
        elif self._attr_type == 'desc':
            # use previous descriptor
            return getattr(instance._value_, self.name)
        # look for a member by this name.
        try:
            return ownerclass._member_map_[self.name]
        except KeyError:
            raise AttributeError(
                    '%r has no attribute %r' % (ownerclass, self.name)
                    ) from None
""",
    ),
]

_reference_keys = None
_reference_codes: frozenset = frozenset()


def _references():
    global _reference_keys, _reference_codes
    if _reference_keys is None:
        keys = {}
        for kind, qualname, source in _REFERENCES:
            module = compile(source, "<kolo-repr-audit>", "exec")
            code = _find_code(module, qualname)
            assert code is not None, qualname
            keys[_code_key(code)] = (kind, code)
        _reference_codes = frozenset(key[0] for key in keys)
        _reference_keys = keys
    return _reference_keys


def _freevar_indices(code, *names):
    return tuple(code.co_freevars.index(name) for name in names)


class _Reject(Exception):
    pass


# `dis`'s decoder (EXTENDED_ARG folded, inline caches skipped), private but
# present with this name in 3.12 to 3.15.
_dis: Any = dis

_NB_ADD = 0
# Instructions whose argument indexes `co_names` shifted by one bit.
_SHIFTED_NAMES = ("LOAD_ATTR", "LOAD_GLOBAL")


def _ops(code):
    """`(opname, arg, argval)` per instruction of `co_code`: what the
    verifiers need, without `dis.get_instructions` (which also computes
    positions and reprs, the bulk of classifying under tracing).
    `dis._unpack_opargs` folds EXTENDED_ARG and skips inline caches."""
    for item in _dis._unpack_opargs(code.co_code):
        op, arg = item[-2], item[-1]
        name = _ALL_OPNAME[op]
        if name in ("LOAD_CONST", "RETURN_CONST"):
            argval = code.co_consts[arg]
        elif name in _SHIFTED_NAMES:
            argval = code.co_names[arg >> 1]
        else:
            argval = None
        yield name, arg, argval


def _fstring_program(code):
    """Verify a straight-line f-string repr over attributes of `self`.

    Accepted: string constants, `self`, `self.a.b`, `type(self)` (with the
    real builtin `type`, guarded natively), f-string fields with no format
    spec, `+` on strings, and returning the result. Returns
    (globals_used, fields) where each field is (root, names, conversion), in
    evaluation order.
    """
    if (
        code.co_argcount != 1
        or code.co_posonlyargcount
        or code.co_kwonlyargcount
        or code.co_nlocals != 1
        or code.co_freevars
        or code.co_cellvars
        or _localsplus_names(code) != code.co_varnames
        or code.co_exceptiontable
        or code.co_flags & (0x0004 | 0x0008 | 0x0020 | 0x0080 | 0x0100 | 0x0200)
    ):
        raise _Reject
    stack: List[Any] = []
    globals_used: List[str] = []
    result: Any = None
    # The deepest value stack the program reaches: `co_stacksize` is not
    # checked by the interpreter, and a smaller one would let the program
    # write past its frame.
    peak = 0
    for op, raw_arg, argval in _ops(code):
        arg: int = raw_arg if raw_arg is not None else -1
        if op in ("RESUME", "NOP"):
            continue
        if result is not None:
            raise _Reject
        # 3.14+ loads `self` with LOAD_FAST_BORROW (same value, no new
        # reference).
        if op in ("LOAD_FAST", "LOAD_FAST_BORROW") and arg == 0:
            stack.append(("self",))
        elif op == "LOAD_CONST":
            if type(argval) is not str:
                raise _Reject
            stack.append(("const",))
        elif op == "LOAD_ATTR":
            if arg & 1:
                raise _Reject
            base = stack.pop()
            if base[0] not in ("self", "attr", "type_of_self"):
                raise _Reject
            stack.append(("attr", base, argval))
        elif op == "LOAD_GLOBAL":
            if argval != "type" or not arg & 1:
                raise _Reject
            if "type" not in globals_used:
                globals_used.append("type")
            stack.append(("global_type",))
        elif op == "CALL":
            if arg != 1 or len(stack) < 2:
                raise _Reject
            argument = stack.pop()
            function = stack.pop()
            if function != ("global_type",) or argument != ("self",):
                raise _Reject
            stack.append(("type_of_self",))
        elif op == "FORMAT_VALUE":
            if arg & 4:
                raise _Reject
            value = stack.pop()
            stack.append(
                (
                    "fmt",
                    value,
                    (CONV_FORMAT, CONV_STR, CONV_REPR, CONV_REPR)[arg & 3],
                )
            )
        elif op == "CONVERT_VALUE":
            if arg not in (1, 2, 3):
                raise _Reject
            value = stack.pop()
            stack.append(("fmt", value, (None, CONV_STR, CONV_REPR, CONV_REPR)[arg]))
        elif op == "FORMAT_SIMPLE":
            value = stack.pop()
            if value[0] != "fmt":
                value = ("fmt", value, CONV_FORMAT)
            stack.append(value)
        elif op == "BUILD_STRING":
            count = arg
            if count < 1 or len(stack) < count:
                raise _Reject
            parts = stack[-count:]
            del stack[-count:]
            stack.append(("join", parts))
        elif op == "BINARY_OP":
            if arg != _NB_ADD:
                raise _Reject
            right = stack.pop()
            left = stack.pop()
            stack.append(("concat", left, right))
        elif op == "RETURN_VALUE":
            if len(stack) != 1:
                raise _Reject
            result = stack.pop()
        elif op == "RETURN_CONST":
            if stack or type(argval) is not str:
                raise _Reject
            result = ("const",)
        else:
            raise _Reject
        # `type` is loaded with a NULL (two slots).
        peak = max(peak, len(stack) + stack.count(("global_type",)))
    if result is None or code.co_stacksize < peak:
        raise _Reject

    fields: List[Any] = []

    def path(value):
        names = []
        while value[0] == "attr":
            names.append(value[2])
            value = value[1]
        names.reverse()
        if value[0] == "self":
            return ROOT_SELF, tuple(names)
        if value[0] == "type_of_self":
            return ROOT_TYPE_OF_SELF, tuple(names)
        raise _Reject

    def emit_str(value):
        """`value` is used where an exact str is required."""
        kind = value[0]
        if kind == "const":
            return
        if kind == "join":
            for part in value[1]:
                if part[0] not in ("fmt", "const"):
                    raise _Reject
                emit_str(part)
            return
        if kind == "fmt":
            root, names = path(value[1])
            fields.append((root, names, value[2]))
            return
        if kind == "concat":
            emit_str(value[1])
            emit_str(value[2])
            return
        root, names = path(value)
        fields.append((root, names, CONV_EXACT_STR))

    emit_str(result)
    return tuple(globals_used), tuple(fields)


_NAME_TUPLES = ("co_names", "co_varnames", "co_freevars", "co_cellvars")


def _plain_tables(code):
    """`code.replace` accepts tuple subclasses (and str subclasses inside
    them), whose Python-level indexing can differ from what the interpreter
    reads, and keeps a bytes subclass passed as the exception table, whose
    truthiness and equality can differ from its contents. Only certify code
    built from exact tuples of exact str and exact bytes."""
    if type(code.co_code) is not bytes or type(code.co_exceptiontable) is not bytes:
        return False
    if code.co_flags & _CO_NO_MONITORING_EVENTS:
        return False
    if any(type(name) is not str for name in _localsplus_names(code)):
        return False
    for attr in _NAME_TUPLES:
        names = getattr(code, attr)
        if type(names) is not tuple or any(type(name) is not str for name in names):
            return False
    consts = code.co_consts
    if type(consts) is not tuple:
        return False
    return all(
        _plain_tables(const) for const in consts if isinstance(const, types.CodeType)
    )


_ALL_OPNAME = getattr(dis, "_all_opname", None) or dis.opname
# Inline cache fields per base instruction name, trusted from 3.13 on (where
# `dis` reports them as `Instruction.cache_info`).
_CACHE_FORMAT = getattr(__import__("opcode"), "_cache_format", {})
_CACHE_INFO = sys.version_info >= (3, 13)
_SPECIALIZED_BASE = {
    specialized: base
    for base, family in getattr(__import__("opcode"), "_specializations", {}).items()
    for specialized in family
}


_TOOL_NAME = "kolo repr audit"
# A general-purpose id, kept once taken: freeing a tool id makes every code
# object in the process re-instrument on its next call (a few hundred
# microseconds per classification under tracing). Not 3: Kolo's own monitor
# uses it (kolo.monitoring.KOLO_TOOL_ID).
_KEPT_TOOLS = (4,)
# The id this module holds for the process once taken (read and rebound in
# `_audit_tool` through `global`; deliberately never freed).
_kept_tool = None


def _audit_tool(monitoring):
    """A sys.monitoring tool id for laundering: a kept general-purpose one,
    else (borrowed and freed after use) one of those debuggers, coverage,
    profilers and optimizers ask for."""
    global _kept_tool
    if _kept_tool is not None and monitoring.get_tool(_kept_tool) == _TOOL_NAME:
        return _kept_tool
    _kept_tool = None
    for tool in _KEPT_TOOLS + (3, 0, 1, 2, 5):
        if monitoring.get_tool(tool) is None:
            monitoring.use_tool_id(tool, _TOOL_NAME)
            if tool in _KEPT_TOOLS:
                _kept_tool = tool
            return tool
    return None


def _runs_what_it_shows(code):
    """Make `code` execute only the instructions `co_code` shows.

    `co_code` is the deoptimized view; the interpreter executes the adaptive
    copy, whose specialized instructions read inline caches. `code.replace`
    keeps specialized instructions passed in `co_code` (with caches from
    another function, they read other attributes or globals than the names
    say). Briefly enabling INSTRUCTION events on the code object makes
    CPython rewrite every instruction to its base form; later
    specializations are derived from the real names again. Returns False if
    that is impossible or anything specialized remains.
    """
    monitoring: Any = getattr(sys, "monitoring", None)
    if monitoring is None:
        return False
    tool = _audit_tool(monitoring)
    if tool is None:
        return False
    try:
        monitoring.set_local_events(tool, code, monitoring.events.INSTRUCTION)
    except Exception:
        return False
    finally:
        try:
            monitoring.set_local_events(tool, code, 0)
        finally:
            if tool not in _KEPT_TOOLS:
                monitoring.free_tool_id(tool)
    adaptive = code._co_code_adaptive
    plain = code.co_code
    if len(adaptive) != len(plain):
        return False
    offsets = [item[0] for item in _dis._unpack_opargs(plain)]
    ends = offsets[1:] + [len(plain)]
    for offset, end in zip(offsets, ends):
        if adaptive[offset] == plain[offset]:
            continue
        name = _ALL_OPNAME[adaptive[offset]]
        base = _ALL_OPNAME[plain[offset]]
        # Other tools' instrumentation of the base instruction is fine:
        # CPython keeps the deoptimized original aside.
        if name in ("INSTRUMENTED_LINE", "INSTRUMENTED_INSTRUCTION"):
            continue
        if name == "INSTRUMENTED_" + base:
            continue
        # Counter-only inline caches (e.g. RESUME_CHECK) hold no data that could come from elsewhere.
        # 3.12's `dis` reports no cache layout: only cache-free instructions qualify there.
        caches = (_CACHE_FORMAT.get(base) or {}) if _CACHE_INFO else {}
        counters_only = end == offset + 2 or (
            bool(caches) and all(field == "counter" for field in caches)
        )
        if _SPECIALIZED_BASE.get(name) == base and counters_only:
            continue
        return False
    return True


def classify(code):
    """Return the verdict for `code`, or None when it is not certified."""
    if not SUPPORTED or type(code) is not types.CodeType:
        return None
    try:
        if not _plain_tables(code):
            return None
        verdict = _verdict(code)
        # Laundering (which re-instruments the code) only for code that would
        # be certified: it is the costly step, and most code is refused.
        if verdict is None or not _runs_what_it_shows(code):
            return None
        return verdict
    except Exception:
        return None


def _verdict(code):
    """The verdict for `code` from what `co_code` shows (see `classify`)."""
    references = _references()
    reference = (
        references.get(_code_key(code)) if code.co_code in _reference_codes else None
    )
    if reference is not None:
        kind, _ = reference
        if kind == DC_WRAPPER_312:
            return (kind, _freevar_indices(code, "repr_running", "user_function"))
        if kind == RECURSIVE_REPR_WRAPPER:
            return (kind, _freevar_indices(code, "repr_running", "user_function"))
        if kind == NAMEDTUPLE_REPR:
            return (kind, _freevar_indices(code, "repr_fmt"))
        return (kind, None)
    try:
        globals_used, fields = _fstring_program(code)
    except (_Reject, IndexError):
        return None
    body = [(op, arg) for op, arg, _ in _ops(code) if op not in ("RESUME", "NOP")]
    if (
        len(body) == 3
        and body[0] in (("LOAD_FAST", 0), ("LOAD_FAST_BORROW", 0))
        and body[1][0] == "LOAD_ATTR"
        and body[2][0] == "RETURN_VALUE"
    ):
        return (SIMPLE_GETTER, fields[0][1][0])
    return (FSTRING, (globals_used, fields))
