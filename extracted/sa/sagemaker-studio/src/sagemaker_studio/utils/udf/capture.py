"""Capture a UDF as portable metadata, and refuse the ones that are not portable.

The sidecar rebuilds the function from *source text* plus *plain picklable
values*, which is portable across CPython minor versions in a way pickled
bytecode is not. This module decides what is capturable and produces the request
payload; anything it cannot ship raises :class:`UDFRegistrationError` HERE, at
definition time, rather than failing confusingly at ``.show()``.

Both halves of the closure are captured. ``inspect.getclosurevars`` reports
enclosing-scope names in ``.nonlocals`` and module- or notebook-level names in
``.globals``; a notebook cell's constants land in the latter, so shipping only
nonlocals made the most ordinary notebook UDF -- one referring to a constant
defined in an earlier cell -- fail with ``NameError`` on the worker. Globals are
handled by kind: a module becomes a synthesised ``import`` statement (modules are
unpicklable), any other value goes through the same :func:`validate_freevar`
gate as a nonlocal, and whatever neither can carry is refused by name, here.
"""

from __future__ import annotations

import ast
import base64
import dataclasses
import inspect
import pickle
import textwrap
from typing import Any, Dict, List, Optional

from sagemaker_studio.utils.udf.errors import UDFRegistrationError

# Prepended to every captured body. Annotations become strings, so a pandas_udf
# annotated with `pd.Series` does not require pandas inside the sidecar -- which
# keeps the "no data-plane libraries in the sidecar" property intact. The eval
# type and return type are decided on the client, where the real annotations are
# visible, so nothing is inferred from these strings.
FUTURE_PREAMBLE = "from __future__ import annotations\n"

PROTOCOL_VERSION = 1

# Type names that mean "a live connection got captured" -- only when they come
# from a module that owns such things. Matching the bare name would refuse
# ordinary picklable data: a pandas DataFrame is also `type(v).__name__ ==
# "DataFrame"`, and closing over a small lookup table is a normal notebook
# pattern, so an unqualified match rejected it claiming it "holds a live
# DataFrame".
_LIVE_TYPE_NAMES = frozenset(
    {
        "SparkSession",
        "SparkConnectClient",
        "RemoteSparkSession",
        "DataFrame",
        "LazySparkSession",
    }
)
# Modules that own live sessions/clients. `sagemaker_studio` is here because
# `LazySparkSession` is ours, not pyspark's.
_LIVE_OWNER_MODULES = ("pyspark", "sagemaker_studio")
_LIVE_MODULE_PREFIXES = ("grpc", "socket", "botocore", "boto3")


def _module_matches(module: str, prefixes: tuple) -> bool:
    """True if ``module`` is one of ``prefixes`` or a submodule of one.

    A raw `startswith` would match on a shared leading substring, so "socket"
    would also claim `socketserver`.
    """
    return any(module == p or module.startswith(p + ".") for p in prefixes)


@dataclasses.dataclass(frozen=True)
class CapturedFunction:
    """Everything the sidecar needs to rebuild one function."""

    name: str
    source: str
    freevars: Dict[str, Any]
    imports: List[str]


def validate_freevar(name: str, value: Any) -> None:
    """Raise :class:`UDFRegistrationError` if ``value`` cannot be shipped."""
    type_name = type(value).__name__
    module = type(value).__module__ or ""

    if (
        (type_name in _LIVE_TYPE_NAMES and _module_matches(module, _LIVE_OWNER_MODULES))
        or (_module_matches(module, ("pyspark.sql",)) and type_name.endswith(("Session", "Client")))
        or _module_matches(module, _LIVE_MODULE_PREFIXES)
    ):
        raise UDFRegistrationError(
            f"the UDF captures {name!r}, which holds a live {type_name}. A UDF that runs "
            "on a version-mismatched engine may only capture plain picklable data -- pass "
            "the values you need as explicit arguments, or read them outside the UDF."
        )

    if inspect.isfunction(value) or inspect.ismethod(value):
        nested = inspect.getclosurevars(value)
        if nested.nonlocals:
            raise UDFRegistrationError(
                f"the UDF captures {name!r}, which is itself a nested closure over "
                f"{sorted(nested.nonlocals)}. Nested closures cannot be shipped; define "
                "the helper at module level or inline it into the UDF."
            )

    # A function or class defined in the notebook / top-level script pickles
    # BY REFERENCE as ``__main__.<name>``, and the sidecar's ``__main__`` is the
    # sidecar server, not the caller's notebook -- so ``pickle.dumps`` below
    # succeeds locally and ``pickle.loads`` fails inside the sidecar. That is a
    # late failure, which the design rules out, so refuse here and name the
    # symbol. Shipping such a value by VALUE would need cloudpickle, whose
    # pickled bytecode is not portable across CPython minor versions -- the very
    # problem this whole path exists to avoid.
    if (inspect.isfunction(value) or inspect.isclass(value)) and getattr(
        value, "__module__", None
    ) == "__main__":
        kind = "function" if inspect.isfunction(value) else "class"
        raise UDFRegistrationError(
            f"the UDF references {name!r}, a {kind} defined in this notebook or script "
            "(`__main__`). Such a value can only be shipped by reference, and the UDF "
            "sidecar's `__main__` is not your notebook, so it could not resolve it. Move "
            f"{name!r} into an importable module and pass it via "
            "`imports=[...]`, or inline its body into the UDF."
        )

    # One level of indirection out from the check above, and just as ordinary a
    # notebook shape: the value is not itself a class, but its CLASS is defined in
    # the notebook. ``pickle`` stores an instance as a reference to its class
    # (``__main__.Cfg``) plus its state, so ``pickle.dumps`` succeeds here and
    # ``pickle.loads`` inside the sidecar raises ``AttributeError: Can't get
    # attribute 'Cfg' on <module '__main__'>``. Late, and confusing -- so refuse
    # here, naming both the symbol and the class that cannot be resolved.
    if module == "__main__":
        raise UDFRegistrationError(
            f"the UDF references {name!r}, whose class {type_name!r} is defined in this "
            "notebook or script (`__main__`). Such a value is pickled as a reference to "
            f"`__main__.{type_name}`, and the UDF sidecar's `__main__` is not your "
            f"notebook, so it could not resolve {type_name!r}. Move {type_name!r} into an "
            "importable module and pass it via `imports=[...]`, or pass the plain data you "
            f"need from {name!r} as explicit UDF arguments."
        )

    try:
        pickle.dumps(value, protocol=5)
    except Exception as e:
        raise UDFRegistrationError(
            f"the UDF captures {name!r} of type {type_name}, which is not picklable "
            f"({type(e).__name__}: {e}). Capture only plain data."
        ) from e


def _strip_decorators(source: str) -> str:
    """Re-emit ``source``'s function definition without its decorators.

    A textual "drop leading @ lines" approach breaks on a multi-line decorator
    call (``@udf(\\n    returnType=StringType()\\n)``), which leaves dangling
    continuation lines behind that will not ``exec`` -- the user would see a
    confusing ``SyntaxError`` from inside the sidecar instead of a clear
    message. Parsing and re-emitting via ``ast`` handles any decorator shape
    uniformly (we already use ``ast`` for the lambda path).

    ``ast.unparse`` drops comments and reformats, so sidecar tracebacks would
    point at code the user never wrote -- that's only an acceptable trade when
    there's actually a decorator to remove. When there isn't one, this returns
    ``source`` unchanged, verbatim, comments and all.
    """
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.decorator_list:
                return source
            node.decorator_list = []
    return ast.unparse(tree) + "\n"


def _lambda_source(source: str, name: str, target_lineno: Optional[int]) -> Optional[str]:
    """Extract a lambda from its enclosing statement as ``<name> = lambda ...``.

    ``inspect.getsource`` on a lambda returns the whole statement it appears in
    (``my_udf = udf(lambda x: x + 1, "int")``), which will not ``exec`` on its
    own -- and if more than one lambda appears in that statement (a tuple
    assignment, two lambda arguments to one call, ...), blindly taking "the
    first ``ast.Lambda`` found" can silently capture the *wrong* one. A wrong
    answer is worse than a rejection, so this never guesses between several
    same-line candidates: it either finds exactly one, or raises.

    ``target_lineno`` is the target lambda's line *within* ``source`` (derived
    by the caller from ``func.__code__.co_firstlineno``), used to narrow to the
    candidate(s) that actually sit on the right line. If no candidate can be
    pinned down at all, this returns ``None`` and the caller raises an
    actionable error. If *more than one* candidate remains on that line, there
    is no reliable column-based way to tell them apart without reconciling
    absolute file coordinates against a re-parsed, dedented AST -- arithmetic
    that is itself easy to get subtly wrong, with the same silent-mis-capture
    failure mode this exists to prevent -- so this raises directly instead.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    candidates = [node for node in ast.walk(tree) if isinstance(node, ast.Lambda)]
    if target_lineno is not None:
        candidates = [node for node in candidates if node.lineno == target_lineno]
    if not candidates:
        return None
    if len(candidates) > 1:
        raise UDFRegistrationError(
            "could not tell which lambda to capture: several lambdas appear in the same "
            "statement, so the intended one cannot be identified. Convert it to a named "
            "`def` function, or move it to its own statement, and register that instead."
        )

    return f"{name} = {ast.unparse(candidates[0])}\n"


def _imported_names(statements: List[str]) -> set:
    """The names a list of import statements binds, so we never shadow the caller's.

    ``imports=`` is the user's explicit escape hatch; if they already import a
    name themselves, their statement wins and we must not append a synthesised
    one for the same name after it.
    """
    names: set = set()
    for statement in statements:
        try:
            tree = ast.parse(statement)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    names.add(alias.asname or alias.name.split(".")[0])
    return names


def _loaded_names(source: str) -> Optional[set]:
    """Plain names the body LOADS, or ``None`` if the source cannot be parsed.

    ``inspect.getclosurevars`` resolves ``code.co_names``, which holds attribute
    names as well as global names. So for ``lambda x: x.lock()`` the name
    ``lock`` is looked up in the module globals, and a module-level
    ``lock = threading.Lock()`` would be "captured" -- and then refused as
    unpicklable -- despite the UDF never referencing it. Intersecting with the
    names the source actually loads as bare identifiers removes that whole class
    of false rejection. Returning ``None`` means "could not tell", and the caller
    then ships everything ``getclosurevars`` reported rather than dropping a real
    capture.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    return {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def _self_bound_names(source: str) -> set:
    """Names that ``exec``-ing the captured source itself binds.

    This is how a self-recursive UDF works without being captured: the sidecar
    ``exec``s the source in a fresh namespace, and the ``def`` statement binds the
    function's own name in that namespace *before* the function is ever called.
    Since a body resolves its globals at CALL time, ``fact`` inside ``fact``
    resolves to the freshly exec'd function -- so the name must be skipped when
    scanning globals rather than captured (capturing it would pickle a
    ``__main__`` function by reference and be refused, with a message about
    inlining a helper that makes no sense for self-reference).

    For an ordinary ``def`` this is exactly ``{func.__name__}``; it is read back
    off the emitted source so it stays the name the sidecar will really bind --
    including the ``<name> = lambda ...`` form, where that is the assignment
    target rather than ``func.__name__`` (``"<lambda>"``).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return names


def _module_import_statement(name: str, module: Any) -> str:
    """An ``import`` statement that rebinds ``module`` under ``name``.

    A module cannot be pickled, so the portable way to ship one is to replay the
    import inside the sidecar -- which is exactly what ``imports=`` already does
    for the explicit case. Availability of the module inside the sidecar
    interpreter remains the environment's responsibility, unchanged by this.
    """
    module_name = getattr(module, "__name__", None)
    if not module_name:
        raise UDFRegistrationError(
            f"the UDF references the module bound to {name!r}, which has no "
            "`__name__`, so "
            "no import statement can be synthesised for it. Reference a normal, importable "
            "module instead."
        )
    if module_name == "__main__":
        raise UDFRegistrationError(
            f"the UDF references {name!r}, which is the "
            "`__main__` module of this notebook "
            "or script. The UDF sidecar's `__main__` is the sidecar server, not your "
            "notebook, so importing it there would not give you these names. Reference an "
            "importable module instead."
        )
    if module_name == name:
        return f"import {module_name}"
    return f"import {module_name} as {name}"


def capture(
    func: Any,
    *,
    imports: Optional[List[str]] = None,
    name: Optional[str] = None,
) -> CapturedFunction:
    """Capture ``func`` as source + validated freevar values."""
    func_name = name or getattr(func, "__name__", None) or "udf"
    is_lambda = getattr(func, "__name__", "") == "<lambda>"
    if is_lambda and name is None:
        func_name = "_smus_lambda_udf"

    try:
        src_lines, start_lineno = inspect.getsourcelines(func)
    except (OSError, TypeError) as e:
        raise UDFRegistrationError(
            "could not read this function's source, which the version-routed UDF path "
            f"requires ({type(e).__name__}: {e}). Define the UDF in a notebook cell or a "
            "module file rather than, for example, an interactive `exec` or a C extension."
        ) from e
    raw = "".join(src_lines)

    dedented = textwrap.dedent(raw)
    if is_lambda:
        # co_firstlineno is the lambda's absolute source line; start_lineno is
        # the absolute line the extracted block starts at, so their difference
        # gives the lambda's line *within* the (dedent-preserved-line-count)
        # extracted text -- used to pick the right lambda when several share
        # one statement.
        target_lineno = func.__code__.co_firstlineno - start_lineno + 1
        body = _lambda_source(dedented, func_name, target_lineno)
        if body is None:
            raise UDFRegistrationError(
                "could not extract this lambda's body from its source. Convert it to a "
                "named `def` function and register that instead."
            )
    else:
        body = _strip_decorators(dedented)

    closure = inspect.getclosurevars(func)
    freevars: Dict[str, Any] = dict(closure.nonlocals)
    for var_name, value in freevars.items():
        validate_freevar(var_name, value)

    # `getclosurevars` splits captured names into `.nonlocals` (enclosing
    # function scopes) and `.globals` (module-level, which in a notebook means
    # "defined in an earlier cell"). Shipping only nonlocals meant the single
    # most ordinary notebook UDF -- one referencing a constant from an earlier
    # cell -- raised NameError ON THE WORKER, while the identical notebook works
    # on Glue 5 because cloudpickle captures `__main__` globals by value. So
    # globals are captured too: modules become a synthesised import (they cannot
    # be pickled), everything else goes through the same `validate_freevar` gate
    # as nonlocals, and anything neither can carry is refused right here, by name.
    resolved_imports = list(imports or [])
    already_bound = _imported_names(resolved_imports)
    self_bound = _self_bound_names(body)
    referenced = _loaded_names(body)
    for var_name, value in closure.globals.items():
        if var_name in already_bound or var_name in self_bound:
            continue
        if referenced is not None and var_name not in referenced:
            continue
        if inspect.ismodule(value):
            resolved_imports.append(_module_import_statement(var_name, value))
            continue
        validate_freevar(var_name, value)
        freevars[var_name] = value

    return CapturedFunction(
        name=func_name,
        source=FUTURE_PREAMBLE + body,
        freevars=freevars,
        imports=resolved_imports,
    )


def build_request(
    captured: CapturedFunction,
    *,
    return_type_json: str,
    eval_type: int,
) -> Dict[str, Any]:
    """Assemble the sidecar build request. Metadata only -- never user data."""
    return {
        "protocol": PROTOCOL_VERSION,
        "name": captured.name,
        "source": captured.source,
        "imports": list(captured.imports),
        "return_type_json": return_type_json,
        "eval_type": int(eval_type),
        "freevars_pickle_b64": base64.b64encode(pickle.dumps(captured.freevars, protocol=5)).decode(
            "ascii"
        ),
    }
