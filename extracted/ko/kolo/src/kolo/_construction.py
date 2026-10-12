"""Find the objects whose constructor is still running.

Kolo serializes values with `repr()` while the program runs: arguments when a
function is called, locals when it returns, and with `line_events` every
assigned value. Inside `__new__` or `__init__` (and in anything they call)
that reaches objects that are only partly built. A `__repr__` is written for
finished objects, so running it there can raise, or, worse, change the
object: a property that computes and caches a value on first read caches one
derived from fields that are not set yet, and the program then reads the wrong
value for the rest of the object's life.

So the serializers never run user code for an object under construction and
record a placeholder instead (`under_construction_repr`). An object is under
construction while one of these is on the calling thread's stack and has not
reached its `return`:

* `__init__`, `__post_init__` or `__setstate__` with the object as its first
  argument;
* `__new__(cls, ...)`, for instances of `cls` (the objects `__init__` would
  then run on), other than the arguments `__new__` was called with (a
  parameter its code never rebinds still holds one). When `__new__` returns,
  the object is finished only if no `__init__` will run on it.

Frames are recognised by the name and first local of their code, so this
covers every constructor written in Python, traced by Kolo or not, including
generated ones (dataclasses, attrs, namedtuple). What it cannot see:

* a constructor wrapped by a decorator, while the wrapper's own frame (which
  has another name) is the one running;
* a code object rebuilt by hand with a `str` subclass as its name;
* an object made with a bare `cls.__new__(cls)` and filled in by its caller
  (an alternative constructor), which no frame marks as unfinished;
* an object that some *other* object's `__repr__` reaches;
* an object its constructor has handed to another thread, whose stack shows
  no constructor;
* a constructor that takes no positional parameter but has keyword-only ones
  (`def __init__(*args, flag=False)`);
* a class while `type.__new__` is still creating it (`__init_subclass__`,
  `__set_name__`), for a metaclass with a `__repr__` of its own;
* an existing instance that `__new__` was passed and returns, on which
  `__init__` then runs again.

Two environment variables, read once when Kolo is imported, switch this off:
`KOLO_CONSTRUCTION_CHECK=0` altogether (values are serialized as before,
whatever is running), and `KOLO_CONSTRUCTION_NATIVE=0` only the native stack
walk, which reads private CPython structures, leaving every stack to the
reference implementation below.

`objects_under_construction` is the reference implementation. The native
encoder has its own stack walk (`rust/src/utils/construction.rs`) for the
case that matters for speed, a stack with no `__new__` on it, and calls this
one for the rest.
"""

from __future__ import annotations

import opcode
import os
import sys
import types
import weakref
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

CHECK = os.environ.get("KOLO_CONSTRUCTION_CHECK") != "0"
_INIT_NAMES = frozenset(("__init__", "__post_init__", "__setstate__"))
_RETURN_OPCODES = frozenset(
    opcode.opmap[name]
    for name in ("RETURN_VALUE", "RETURN_CONST")
    if name in opcode.opmap
)
_CO_VARARGS = 0x04
_TPFLAGS_HEAPTYPE = 1 << 9
_CPYTHON = sys.implementation.name == "cpython"
_MISSING = object()

# Read through `type`'s own descriptors: `cls.__mro__` and friends go through
# the metaclass, which can run user code.
_TYPE: Any = type.__dict__
_type_mro = _TYPE["__mro__"].__get__
_type_dict = _TYPE["__dict__"].__get__
_type_flags = _TYPE["__flags__"].__get__ if _CPYTHON else None
_type_qualname = _TYPE["__qualname__"].__get__
_OBJECT_INIT = object.__dict__["__init__"]
_OBJECT_REPR = object.__dict__["__repr__"]
# The type slots `msgpack_encode_hook` runs for a value, by the id of the first
# of these types in its class's MRO (a class has one of them at most,
# `datetime` coming before `date`); `repr()` for any other value. None where
# the hook looks a method up on the instance (`obj.isoformat()`), which an
# instance attribute or `__getattribute__` can answer.
_HOOK_SLOTS = {
    id(tuple): ("__iter__", "__len__"),
    id(set): ("__iter__", "__len__"),
    id(frozenset): ("__iter__", "__len__"),
    id(dict): ("__iter__", "__len__", "keys", "__getitem__"),
    id(datetime): None,
    id(date): None,
    id(time): None,
    id(int): None,
    id(Decimal): ("__str__",),
}
_REPR_ONLY = ("__repr__",)
# The hook's `isinstance()` checks read `obj.__class__`.
_HOOK_LOOKUPS = ("__getattribute__", "__class__")


# On CPython 3.12 and older, `frame.f_locals` copies every local into a dict
# the frame keeps, so a local the constructor then drops would stay alive. 3.12
# can read one variable instead; 3.13's `f_locals` is a view that copies
# nothing. Older releases have no other way, and Kolo's own capture reads
# `f_locals` of every frame it records there anyway.
def _load_native_frame_local():
    if not _CPYTHON or sys.version_info[:2] != (3, 12):
        return None
    try:
        from ._kolo import _frame_local
    except ImportError:  # pragma: no cover - source-only installs
        return None
    return _frame_local


_native_frame_local = _load_native_frame_local()


def _local(frame, name):
    if _native_frame_local is not None:
        found = _native_frame_local(frame, name)
        return found[0] if found else _MISSING
    try:
        return frame.f_locals[name]
    except KeyError:
        # Unbound: deleted, or a cell that is empty.
        return _MISSING


def _inherited(cls, name):
    """`cls.<name>` as the type slot sees it, or `_MISSING` if `cls` is not a
    type."""
    try:
        mro = _type_mro(cls)
    except TypeError:
        return _MISSING
    for klass in mro:
        found = _type_dict(klass).get(name, _MISSING)
        if found is not _MISSING:
            return found
    return _MISSING


def _returning(frame, code):
    """Whether `frame` has reached its `return`: Kolo (or another tool) is
    being told about the return, and the frame runs no more code."""
    lasti = frame.f_lasti
    bytecode = code.co_code
    return 0 <= lasti < len(bytecode) and bytecode[lasti] in _RETURN_OPCODES


def _first_local(frame, code):
    varnames = code.co_varnames
    if not varnames:
        return _MISSING
    return _local(frame, varnames[0])


# id(code) -> (weak reference to the code, names). The entry goes when the
# code object does, so tracing keeps none alive and no id is another's.
_REBOUND: dict = {}
_REBOUND_LIMIT = 512


def _rebound_names(code):
    """The variables `code` may assign, or a function nested in it through
    its closure: a parameter among them need not hold the argument any
    more."""
    cached = _REBOUND.get(id(code))
    if cached is not None and cached[0]() is code:
        return cached[1]
    import dis

    names: set = set()
    # (code, the variables of the outermost code it shares); None for the
    # outermost code itself, whose every store counts.
    pending: list = [(code, None)]
    while pending:
        current, shared = pending.pop()
        for instruction in dis.get_instructions(current):
            opname = instruction.opname
            argval = instruction.argval
            if shared is not None:
                if opname == "STORE_DEREF" and argval in shared:
                    names.add(argval)
            elif opname == "STORE_DEREF" or "STORE_FAST" in opname:
                if type(argval) is not tuple:
                    names.add(argval)
                elif opname == "STORE_FAST_LOAD_FAST":
                    # (stored, loaded)
                    names.add(argval[0])
                else:
                    names.update(argval)
        cells = current.co_cellvars if shared is None else shared
        for const in current.co_consts:
            if isinstance(const, types.CodeType):
                # A nested function reaches an outer variable only as one of
                # its free variables.
                reached = frozenset(cells).intersection(const.co_freevars)
                if reached:
                    pending.append((const, reached))
    if len(_REBOUND) >= _REBOUND_LIMIT:
        _REBOUND.clear()
    rebound = frozenset(names)
    key = id(code)
    _REBOUND[key] = (weakref.ref(code, lambda _: _REBOUND.pop(key, None)), rebound)
    return rebound


def _new_arguments(frame, code, starred):
    """ids of the values `__new__` was called with, apart from `cls`: its
    positional and keyword-only parameters and the items of `*args`."""
    varnames = code.co_varnames
    rebound = _rebound_names(code)
    count = code.co_argcount + code.co_kwonlyargcount
    ids = []
    for name in varnames[0 if starred else 1 : count]:
        if name not in rebound:
            value = _local(frame, name)
            if value is not _MISSING:
                ids.append(id(value))
    if code.co_flags & _CO_VARARGS and varnames[count] not in rebound:
        extra = _local(frame, varnames[count])
        if type(extra) is tuple:
            ids.extend(id(item) for item in extra[1 if starred else 0 :])
    return ids


def objects_under_construction(frame=None):
    """The objects under construction on the stack that ends at `frame` (by
    default the caller's), as a flat list of ints the native encoder can read:

        [n, id(obj) * n, (id(cls), returning, k, id(argument) * k) * m]

    `n` objects whose `__init__` (or `__post_init__`, `__setstate__`) is
    running, then one group for each running `__new__`: its `cls`, whether
    it has reached its `return` (1 or 0), and the arguments it was called
    with.
    """
    if frame is None:
        try:
            frame = sys._getframe(1)
        except ValueError:
            # Called from native code with no Python frame beneath it.
            return [0]
    objects = []
    classes: list = []
    while frame is not None:
        code = frame.f_code
        name = code.co_name
        if name == "__new__" or name in _INIT_NAMES:
            first = _first_local(frame, code)
            # `def __init__(*args, **kwargs)`: the object is `args[0]`.
            starred = type(first) is tuple
            if starred:
                first = first[0] if first else _MISSING
            if first is _MISSING:
                pass
            elif name != "__new__":
                if not _returning(frame, code):
                    objects.append(id(first))
            elif _inherited(first, "__init__") is not _MISSING:
                # `first` is a class.
                arguments = _new_arguments(frame, code, starred)
                classes.append(id(first))
                classes.append(1 if _returning(frame, code) else 0)
                classes.append(len(arguments))
                classes.extend(arguments)
        frame = frame.f_back
    return [len(objects), *objects, *classes]


def is_under_construction(found, obj):
    """Whether `obj` is one of the objects `objects_under_construction` found."""
    if len(found) == 1:
        return False
    count = found[0]
    start = count + 1
    obj_id = id(obj)
    if obj_id in found[1:start]:
        return True
    cls = type(obj)
    mro = None
    while start < len(found):
        end = start + 3 + found[start + 2]
        if obj_id not in found[start + 3 : end]:
            if mro is None:
                mro = [id(klass) for klass in _type_mro(cls)]
            # A returning `__new__` leaves the object to its `__init__`.
            if found[start] in mro and not (
                found[start + 1] and _inherited(cls, "__init__") is _OBJECT_INIT
            ):
                return True
        start = end
    return False


def may_run_user_code(cls):
    """Whether serializing an instance of `cls` can run user code at all:
    only instances of classes created by a `class` statement can be handed to
    a constructor written in Python."""
    return not _CPYTHON or bool(_type_flags(cls) & _TPFLAGS_HEAPTYPE)


def _all_builtin(mro, names):
    """Whether each of these methods comes from a builtin type, not from a
    class the program defines: code that was not written for this class
    cannot be surprised by its unfinished state."""
    for name in names:
        for klass in mro:
            found = _type_dict(klass).get(name, _MISSING)
            if found is not _MISSING:
                if _CPYTHON:
                    # Also `__repr__ = object.__repr__` in a class of the
                    # program: the type slot is `object`'s then. Not any
                    # builtin's method (`object.__str__` calls `repr()`).
                    builtin = not _type_flags(klass) & _TPFLAGS_HEAPTYPE or (
                        name == "__repr__" and found is _OBJECT_REPR
                    )
                else:
                    builtin = klass is object or klass is type
                if not builtin:
                    return False
                break
        else:
            return False
    return True


def under_construction_repr(obj, repr_only=False, lightweight=False):
    """What Kolo records for `obj` instead of serializing it while it is
    under construction. None if serializing it (or, with `repr_only`, its
    `repr()`) runs none of its class's own code: the default
    `object.__repr__`, or say an exception or a `dict` subclass that leaves
    the builtin's methods alone. `lightweight` is `lightweight_repr`, which
    calls no `repr()`."""
    cls = type(obj)
    mro = _type_mro(cls)
    names: Any = () if lightweight else _REPR_ONLY
    if not repr_only:
        for klass in mro:
            if id(klass) in _HOOK_SLOTS:
                names = _HOOK_SLOTS[id(klass)]
                break
        if names is not None:
            names += _HOOK_LOOKUPS
    if names is not None and _all_builtin(mro, names):
        return None
    module = _type_dict(cls).get("__module__")
    qualname = _exact_str(_type_qualname(cls))
    if type(module) is str:
        qualname = f"{module}.{qualname}"
    return f"<{qualname} object: Kolo skipped repr during construction>"


def _exact_str(text):
    """`text` as an exact str: formatting a subclass would run its
    `__format__`."""
    return text if type(text) is str else str.__str__(text)


def method_under_construction_repr(method):
    """The `repr()` of a method bound to an object under construction, as
    `method_repr` writes it, around that object's placeholder. None if the
    object's own repr is safe to run."""
    bound_self = under_construction_repr(method.__self__, repr_only=True)
    if bound_self is None:
        return None
    function = method.__func__
    name = "?"
    # Any other callable could answer these lookups with its own code.
    if type(function) is types.FunctionType:
        name = _exact_str(function.__qualname__)
    return f"<bound method {name} of {bound_self}>"


def placeholder(found, obj, lightweight=False):
    """The placeholder to record for `obj`, or None to serialize it as usual."""
    if type(obj) is types.MethodType:
        # `lightweight_repr` does not `repr()` a method.
        if not lightweight and is_under_construction(found, obj.__self__):
            return method_under_construction_repr(obj)
        return None
    if is_under_construction(found, obj):
        return under_construction_repr(obj, False, lightweight)
    return None


# The rest checks the native stack walk against `objects_under_construction`
# on the running interpreter, once, before the native encoder relies on it:
# one constructor of every shape the walk reads, each comparing the two on
# its own stack.


def _compare(native, results):
    expected = objects_under_construction()
    found = native()
    # None: the native walk leaves this stack to `objects_under_construction`.
    results.append(None if found is None else found == expected)


class _Probe:
    def __init__(self, native, results, shape):
        if shape == "plain":
            _compare(native, results)
        elif shape == "nested":
            self._nested(native, results)
        elif shape == "post_init":
            self.__post_init__(native, results)
        elif shape == "setstate":
            self.__setstate__((native, results))
        elif shape == "innermost":
            found = native()
            expected = objects_under_construction(sys._getframe(0))
            results.append(None if found is None else found == expected)

    def _nested(self, native, results):
        _compare(native, results)

    def __post_init__(self, native, results):
        self._nested(native, results)

    def __setstate__(self, state):
        self._nested(*state)


class _CellProbe:
    def __init__(self, native, results):
        self.get = lambda: self
        _compare(native, results)


class _StarredProbe:
    def __init__(*args):
        _compare(args[1], args[2])


class _NewProbe:
    def __new__(cls, native, results):
        self = object.__new__(cls)
        results.append(native() is None)
        _compare(native, results)
        return self


def _probe_unbound(native, results):
    def __init__(self):
        del self
        _compare(native, results)

    __init__(None)


def _probe_no_locals(native, results):
    # The first slot of this frame is a closure variable, not a local.
    def __init__():
        _compare(native, results)

    __init__()


def _probe_empty_frame():
    # No slots at all.
    def __init__():
        _compare(*_PROBE_ARGUMENTS)

    __init__()


def _probe_computed_name():
    # A code object built by hand need not have an interned name.
    def template(self):
        _compare(*_PROBE_ARGUMENTS)

    name = "".join(("__in", "it__"))
    code = template.__code__.replace(co_name=name)
    types.FunctionType(code, globals())(object())


_PROBE_ARGUMENTS: Any = ()


def probe_native_walk(native):
    """Whether `native()` (the native stack walk) agrees with
    `objects_under_construction` for every constructor shape. None if that
    could not be told: the native walk declines every stack right now, as it
    does while a `__new__` is running further up."""
    global _PROBE_ARGUMENTS
    results: list = []
    for shape in ("plain", "nested", "post_init", "setstate", "innermost"):
        _Probe(native, results, shape)
    _CellProbe(native, results)
    _StarredProbe(native, results)  # type: ignore[arg-type]
    _probe_unbound(native, results)
    _probe_no_locals(native, results)
    _PROBE_ARGUMENTS = (native, results)
    try:
        _probe_empty_frame()
        _probe_computed_name()
    finally:
        _PROBE_ARGUMENTS = ()
    if False in results or len(results) != 11:
        return False
    if None in results:
        return None
    declined: list = []
    _NewProbe(native, declined)
    return declined == [True, None]
