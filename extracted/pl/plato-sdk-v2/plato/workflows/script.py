"""Workflow script compilation.

A workflow script is a plain Python source string that may use top-level
``await`` AND top-level ``return`` (the return value becomes the workflow
result). Both are made legal by wrapping the source in an async function::

    async def __workflow_main__():
        <script, indented>
        pass

The wrapper adds exactly ONE line above the user's source, so every
wrapped line number maps back to user coordinates with ``lineno - 1``.

``compile_workflow_script`` performs, in order:

1. Wrap + ``ast.parse`` — ``SyntaxError`` is remapped to user coordinates and
   re-raised as :class:`WorkflowScriptError`.
2. AST pre-checks — reject ``from __future__ import ...`` anywhere,
   ``global``/``nonlocal`` at the script's top level (they would silently
   bind into the exec globals / fail at compile with a confusing message),
   and bare un-awaited ``agent()``/``parallel()``/``pipeline()`` calls at the
   top level (they'd produce never-executed coroutines; thunk-wrapped calls
   inside lambdas/defs are exempt — the runtime awaits those).
3. Determinism lint — flag call sites whose results change across runs
   (``time.time``, ``datetime.now``/``utcnow``, ``random.*``, ``uuid.uuid*``,
   ``os.urandom``). Non-fatal: collected into ``lint_warnings`` because they
   break journal-replay stability, not execution.
4. ``compile`` to a code object.
"""

from __future__ import annotations

import ast
import hashlib
import textwrap
import types
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from plato.workflows.errors import WorkflowScriptError

WRAPPER_NAME = "__workflow_main__"
SCRIPT_FILENAME = "<workflow>"

# Scope-introducing nodes: statements inside them are NOT the script's
# top level (a `global` inside a nested def is legitimate Python).
_SCOPE_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)

# Injected primitives that return coroutines. A bare top-level call silently
# yields a never-executed coroutine object instead of a result.
_ASYNC_PRIMITIVES = frozenset({"agent", "parallel", "pipeline", "workflow"})


def _wrap_source(source: str) -> str:
    # The trailing `pass` keeps the function body non-empty for empty or
    # comment-only scripts.
    return f"async def {WRAPPER_NAME}():\n" + textwrap.indent(source, "    ") + "\n    pass\n"


def _remap_lineno(wrapped_lineno: int | None, source: str) -> int | None:
    """Wrapped coordinates -> user coordinates (clamped to the source)."""
    if wrapped_lineno is None:
        return None
    user_lineno = wrapped_lineno - 1
    if user_lineno < 1:
        return None
    n_lines = len(source.splitlines())
    if n_lines and user_lineno > n_lines:
        user_lineno = n_lines
    return user_lineno


def _excerpt_for(lineno: int | None, source: str, fallback: str | None = None) -> str | None:
    if lineno is not None:
        lines = source.splitlines()
        if 1 <= lineno <= len(lines):
            stripped = lines[lineno - 1].strip()
            if stripped:
                return stripped
    return fallback.strip() if fallback else None


def _remap_syntax_error(exc: SyntaxError, source: str) -> WorkflowScriptError:
    lineno = _remap_lineno(exc.lineno, source)
    excerpt = _excerpt_for(lineno, source, fallback=exc.text)
    location = f" (line {lineno})" if lineno is not None else ""
    return WorkflowScriptError(f"workflow script syntax error{location}: {exc.msg}", lineno=lineno, excerpt=excerpt)


def _iter_top_level(main_fn: ast.AsyncFunctionDef) -> Iterator[ast.AST]:
    """Yield nodes at the script's top level (not inside nested scopes)."""
    stack: list[ast.AST] = list(main_fn.body)
    while stack:
        node = stack.pop()
        yield node
        if isinstance(node, _SCOPE_NODES):
            continue
        stack.extend(ast.iter_child_nodes(node))


def _run_prechecks(tree: ast.Module, source: str) -> None:
    # `from __future__ import ...` is illegal anywhere inside the wrapper —
    # reject it with a clear message before compile() produces a cryptic one.
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            lineno = _remap_lineno(node.lineno, source)
            raise WorkflowScriptError(
                "workflow scripts cannot use 'from __future__' imports",
                lineno=lineno,
                excerpt=_excerpt_for(lineno, source),
            )

    main_fn = tree.body[0]
    assert isinstance(main_fn, ast.AsyncFunctionDef)  # by construction of the wrapper
    for node in _iter_top_level(main_fn):
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            keyword = "global" if isinstance(node, ast.Global) else "nonlocal"
            lineno = _remap_lineno(node.lineno, source)
            raise WorkflowScriptError(
                f"workflow scripts cannot use '{keyword}' at the top level",
                lineno=lineno,
                excerpt=_excerpt_for(lineno, source),
            )

    # agent()/parallel()/pipeline()/workflow() are async: a bare call produces
    # a coroutine that never runs and poisons results/journal records. Three
    # placements are legitimate and exempt:
    #   1. directly awaited (`await agent(...)`);
    #   2. inside a lambda/def thunk (the runtime awaits those) —
    #      _iter_top_level already skips nested scopes;
    #   3. anywhere inside the ARGUMENTS of an awaited parallel(...)/
    #      pipeline(...) call — the runtime accepts bare coroutines as thunks
    #      (`await parallel([agent("a"), agent("b")])` and the comprehension
    #      form are both valid), so the lint must not contradict it.
    awaited_call_ids = {id(node.value) for node in _iter_top_level(main_fn) if isinstance(node, ast.Await)}
    exempt_ids: set[int] = set(awaited_call_ids)
    for node in _iter_top_level(main_fn):
        if (
            id(node) in awaited_call_ids
            and isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in ("parallel", "pipeline")
        ):
            for arg in [*node.args, *node.keywords]:
                for sub in ast.walk(arg):
                    exempt_ids.add(id(sub))
    for node in _iter_top_level(main_fn):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in _ASYNC_PRIMITIVES
            and id(node) not in exempt_ids
        ):
            lineno = _remap_lineno(node.lineno, source)
            raise WorkflowScriptError(
                f"'{node.func.id}(...)' is async and must be awaited — write 'await {node.func.id}(...)'",
                lineno=lineno,
                excerpt=_excerpt_for(lineno, source),
            )


def _dotted_name(node: ast.expr) -> str | None:
    """Render an Attribute/Name chain as a dotted string ('datetime.datetime.now')."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name):
        return None
    parts.append(node.id)
    return ".".join(reversed(parts))


def _is_nondeterministic(dotted: str) -> bool:
    parts = dotted.split(".")
    root, leaf = parts[0], parts[-1]
    if dotted == "time.time":
        return True
    if root == "os" and leaf == "urandom":
        return True
    if root == "random" and len(parts) > 1:
        return True
    if leaf in ("now", "utcnow") and "datetime" in parts[:-1]:
        return True
    if root == "uuid" and leaf.startswith("uuid"):
        return True
    return False


def _lint_determinism(tree: ast.Module, source: str) -> list[str]:
    warnings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        dotted = _dotted_name(node.func)
        if dotted is None or not _is_nondeterministic(dotted):
            continue
        lineno = _remap_lineno(node.lineno, source)
        location = f"line {lineno}: " if lineno is not None else ""
        warnings.append(
            f"{location}non-deterministic call '{dotted}()' — its value changes across runs, "
            "so journal replay on resume may diverge"
        )
    return warnings


@dataclass
class CompiledWorkflow:
    """A compiled workflow script, ready to execute against a runtime namespace."""

    code: types.CodeType
    source: str
    fingerprint: str  # sha256 hex digest of the ORIGINAL (unwrapped) source
    lint_warnings: list[str] = field(default_factory=list)

    async def run(self, namespace: dict[str, Any]) -> Any:
        """Execute the script with ``namespace`` injected as globals.

        Injected names live in the exec globals, so they are visible to
        nested ``def``s and lambdas inside the script (plain Python scoping).
        Returns the script's return value. Script exceptions re-raise with
        the wrapper machinery's frames stripped from the traceback (the
        traceback starts at the first ``<workflow>`` frame).
        """
        globals_ns: dict[str, Any] = dict(namespace)
        exec(self.code, globals_ns)  # noqa: S102 — deliberate: this IS the script engine
        main = globals_ns[WRAPPER_NAME]
        try:
            return await main()
        except Exception as exc:
            tb = exc.__traceback__
            while tb is not None and tb.tb_frame.f_code.co_filename != SCRIPT_FILENAME:
                tb = tb.tb_next
            if tb is not None:
                raise exc.with_traceback(tb)
            raise


def compile_workflow_script(source: str) -> CompiledWorkflow:
    """Compile a workflow script string into a :class:`CompiledWorkflow`.

    Raises :class:`WorkflowScriptError` (with user-coordinate ``lineno`` and
    ``excerpt``) on syntax errors or pre-check violations.
    """
    wrapped = _wrap_source(source)
    try:
        tree = ast.parse(wrapped, filename=SCRIPT_FILENAME)
    except SyntaxError as exc:
        raise _remap_syntax_error(exc, source) from None

    _run_prechecks(tree, source)
    lint_warnings = _lint_determinism(tree, source)

    try:
        code = compile(wrapped, SCRIPT_FILENAME, "exec")
    except SyntaxError as exc:
        # ast.parse does not run symbol-table checks (e.g. "no binding for
        # nonlocal 'x'"); compile() does.
        raise _remap_syntax_error(exc, source) from None

    return CompiledWorkflow(
        code=code,
        source=source,
        fingerprint=hashlib.sha256(source.encode("utf-8")).hexdigest(),
        lint_warnings=lint_warnings,
    )
