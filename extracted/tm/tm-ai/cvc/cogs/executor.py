"""
cvc.cogs.executor — Sandboxed execution for compiled Cogs.

Security model (v1)
-------------------
Defense is layered:

1. **AST whitelist** (pre-execution).  Source is parsed with :mod:`ast`;
   forbidden node types (``Import`` of non-allowlisted modules, ``Exec``-style
   calls, attribute access to dunder names, disallowed builtins) cause
   :class:`ExecutionError` before any code runs.
2. **Process isolation.**  Approved source is executed in a separate Python
   interpreter (``sys.executable -I``), which disables ``PYTHONPATH``, user
   site-packages, and environment-driven configuration.  I/O is JSON over
   stdin/stdout.
3. **Wall-clock timeout** via :func:`asyncio.wait_for` — the subprocess is
   killed on timeout.

Known limitations: CPU/memory quotas and network namespaces are out of scope
for v1 (Windows parity).  The AST whitelist blocks ``socket``, ``urllib``,
``http.client``, and ``subprocess`` imports at the source level, which is
sufficient for artifacts whose bodies are LLM-distilled *pure functions*.
Rule-DAG bodies are interpreted in-process (no Python execution at all).
"""

from __future__ import annotations

import ast
import asyncio
import json
import os
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cvc.cogs.models import Cog, CogBodyKind

# Modules the Cog source may import. Keep this list tight.
ALLOWED_IMPORTS: frozenset[str] = frozenset(
    {
        "math",
        "re",
        "json",
        "datetime",
        "statistics",
        "string",
        "typing",
        "collections",
        "itertools",
        "functools",
        "dataclasses",
        "decimal",
        "fractions",
        "textwrap",
        "unicodedata",
    }
)

# Names the Cog source may NOT reference (beyond those in builtins blacklist).
FORBIDDEN_NAMES: frozenset[str] = frozenset(
    {
        "eval",
        "exec",
        "compile",
        "open",
        "input",
        "__import__",
        "globals",
        "locals",
        "vars",
        "breakpoint",
        "memoryview",
        "help",
    }
)


class ExecutionError(Exception):
    """Raised when a Cog fails to execute, validate, or pass the AST whitelist."""


@dataclass
class ExecutionResult:
    ok: bool
    output: Any
    error: str = ""
    elapsed_ms: float = 0.0


# ---------------------------------------------------------------------------
# AST validation
# ---------------------------------------------------------------------------


def _validate_ast(source: str) -> None:
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        raise ExecutionError(f"Syntax error in Cog body: {exc}") from exc

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root not in ALLOWED_IMPORTS:
                    raise ExecutionError(f"Forbidden import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            if module and module not in ALLOWED_IMPORTS:
                raise ExecutionError(f"Forbidden import-from: {node.module}")
        elif isinstance(node, ast.Attribute):
            if (
                isinstance(node.attr, str)
                and node.attr.startswith("__")
                and node.attr.endswith("__")
            ):
                if node.attr not in {"__len__", "__iter__", "__next__", "__str__", "__repr__"}:
                    raise ExecutionError(f"Forbidden dunder access: {node.attr}")
        elif isinstance(node, ast.Name):
            if node.id in FORBIDDEN_NAMES:
                raise ExecutionError(f"Forbidden name reference: {node.id}")


# ---------------------------------------------------------------------------
# Subprocess bootstrap
# ---------------------------------------------------------------------------

_RUNNER_TEMPLATE = """\
import importlib.util
import json
import sys
import traceback

src_path = sys.argv[1]
entry = sys.argv[2]
try:
    spec = importlib.util.spec_from_file_location("cog_module", src_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load cog module spec")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, entry, None)
    if fn is None:
        raise RuntimeError(f"entrypoint '{entry}' not found in cog body")
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    if isinstance(payload, dict):
        result = fn(**payload)
    else:
        result = fn(payload)
    sys.stdout.write(json.dumps({"ok": True, "result": result}, default=str))
except BaseException as exc:
    sys.stdout.write(
        json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc()[:2000]})
    )
"""


# ---------------------------------------------------------------------------
# Rule-DAG interpreter
# ---------------------------------------------------------------------------


def _eval_rule_dag(dag: dict[str, Any], inputs: dict[str, Any]) -> Any:
    """
    Minimal JSON rule-DAG interpreter.

    Schema:
        {"if": [[{"field": "x", "op": ">=", "value": 10}, ...], "then": "...",
                else: "..."]} — simplified AND conditions with a single output.

    For v1 we implement a flat rule table:
        {"rules": [{"when": {"field": "x", "op": "==", "value": 1}, "then": "A"}],
         "default": "B"}
    """
    rules = dag.get("rules", [])
    for rule in rules:
        when = rule.get("when", {})
        field = when.get("field")
        op = when.get("op", "==")
        value = when.get("value")
        actual = inputs.get(field) if field is not None else None
        if _compare(actual, op, value):
            return rule.get("then")
    return dag.get("default")


def _compare(actual: Any, op: str, expected: Any) -> bool:
    try:
        if op == "==":
            return actual == expected
        if op == "!=":
            return actual != expected
        if op == ">":
            return actual > expected
        if op == ">=":
            return actual >= expected
        if op == "<":
            return actual < expected
        if op == "<=":
            return actual <= expected
        if op == "in":
            return actual in expected
        if op == "contains":
            return expected in actual
    except Exception:
        return False
    return False


# ---------------------------------------------------------------------------
# Safe executor
# ---------------------------------------------------------------------------


class SafeExecutor:
    """Execute a Cog body safely with a wall-clock timeout."""

    def __init__(self, *, timeout_s: float = 5.0, python_exe: str | None = None) -> None:
        self.timeout_s = timeout_s
        self.python_exe = python_exe or sys.executable

    async def execute(self, cog: Cog, inputs: dict[str, Any]) -> ExecutionResult:
        """Execute *cog* on *inputs*. Never raises; returns an ExecutionResult."""
        start = time.perf_counter()
        try:
            if cog.body.kind == CogBodyKind.RULE_DAG:
                return self._execute_rule_dag(cog, inputs, start)
            if cog.body.kind == CogBodyKind.PYTHON:
                return await self._execute_python(cog, inputs, start)
            return ExecutionResult(
                ok=False,
                output=None,
                error=f"unsupported cog body kind: {cog.body.kind}",
                elapsed_ms=(time.perf_counter() - start) * 1000,
            )
        except ExecutionError as exc:
            return ExecutionResult(
                ok=False,
                output=None,
                error=str(exc),
                elapsed_ms=(time.perf_counter() - start) * 1000,
            )
        except Exception as exc:
            return ExecutionResult(
                ok=False,
                output=None,
                error=f"{type(exc).__name__}: {exc}",
                elapsed_ms=(time.perf_counter() - start) * 1000,
            )

    # -- backends ----------------------------------------------------------

    def _execute_rule_dag(self, cog: Cog, inputs: dict[str, Any], start: float) -> ExecutionResult:
        try:
            dag = json.loads(cog.body.source)
        except json.JSONDecodeError as exc:
            return ExecutionResult(
                ok=False,
                output=None,
                error=f"invalid rule_dag JSON: {exc}",
                elapsed_ms=(time.perf_counter() - start) * 1000,
            )
        result = _eval_rule_dag(dag, inputs)
        return ExecutionResult(
            ok=True,
            output=result,
            elapsed_ms=(time.perf_counter() - start) * 1000,
        )

    async def _execute_python(
        self, cog: Cog, inputs: dict[str, Any], start: float
    ) -> ExecutionResult:
        _validate_ast(cog.body.source)

        tmpdir = Path(tempfile.mkdtemp(prefix="cvc_cog_"))
        try:
            src_path = tmpdir / "cog_body.py"
            runner_path = tmpdir / "_runner.py"
            src_path.write_text(cog.body.source, encoding="utf-8")
            runner_path.write_text(_RUNNER_TEMPLATE, encoding="utf-8")

            payload = json.dumps(inputs, default=str).encode("utf-8")

            env = {
                "PATH": os.environ.get("PATH", ""),
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONIOENCODING": "utf-8",
            }
            if sys.platform == "win32":
                env["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", "")

            proc = await asyncio.create_subprocess_exec(
                self.python_exe,
                "-I",
                "-B",
                str(runner_path),
                str(src_path),
                cog.body.entrypoint,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )

            try:
                stdout_b, stderr_b = await asyncio.wait_for(
                    proc.communicate(input=payload), timeout=self.timeout_s
                )
            except asyncio.TimeoutError:
                try:
                    proc.kill()
                except ProcessLookupError:
                    pass
                await proc.wait()
                return ExecutionResult(
                    ok=False,
                    output=None,
                    error=f"timeout after {self.timeout_s}s",
                    elapsed_ms=(time.perf_counter() - start) * 1000,
                )

            elapsed_ms = (time.perf_counter() - start) * 1000
            stdout = stdout_b.decode("utf-8", errors="replace").strip()
            stderr = stderr_b.decode("utf-8", errors="replace").strip()
            if not stdout:
                return ExecutionResult(
                    ok=False,
                    output=None,
                    error=f"subprocess produced no output; stderr={stderr[:500]}",
                    elapsed_ms=elapsed_ms,
                )
            try:
                parsed = json.loads(stdout)
            except json.JSONDecodeError:
                return ExecutionResult(
                    ok=False,
                    output=None,
                    error=f"subprocess returned non-JSON: {stdout[:500]}",
                    elapsed_ms=elapsed_ms,
                )
            if parsed.get("ok"):
                return ExecutionResult(ok=True, output=parsed.get("result"), elapsed_ms=elapsed_ms)
            return ExecutionResult(
                ok=False,
                output=None,
                error=parsed.get("error", "unknown execution error"),
                elapsed_ms=elapsed_ms,
            )
        finally:
            for p in tmpdir.iterdir():
                try:
                    p.unlink()
                except OSError:
                    pass
            try:
                tmpdir.rmdir()
            except OSError:
                pass
