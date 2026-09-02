"""Drift guard: the CLI regex_safe mirror vs the backend canonical (ENG-4910).

cli/runlayer_cli/regex_safe.py is a hand-trimmed mirror of the security-tier
backend/app/core/regex_safe.py. The trim is deliberate (no subn, no
decomposition helpers — see the module docstring for why), but for the
surface that IS shared, a backend correctness fix that doesn't get mirrored
is a silent security drift: the CLI would keep matching with semantics the
backend already corrected.

Comparison is AST-level with docstrings stripped — docstrings legitimately
differ (each side documents its own context), bodies must not. Runs only in
the monorepo (CI checks out the full repo); a packaged CLI has no backend
tree, and pytest never ships with it anyway.
"""

from __future__ import annotations

import ast
import copy
from pathlib import Path

import pytest

CLI_FILE = Path(__file__).parents[1] / "runlayer_cli" / "regex_safe.py"
BACKEND_FILE = (
    Path(__file__).parents[2] / "backend" / "app" / "core" / "regex_safe.py"
)

pytestmark = pytest.mark.skipif(
    not BACKEND_FILE.is_file(),
    reason="backend tree not present (packaged / partial checkout)",
)

# Everything the CLI defines with one of these names must be byte-for-byte
# semantically identical to the backend's definition. If the backend fixes
# one of them, CLI CI fails here until the fix is mirrored.
SHARED_FUNCTIONS = {
    "_wrap",
    "_as_pattern",
    # Security-tier helper: compile's body only CALLS it, so guarding compile
    # alone would let a backend fix to the helper drift silently.
    "_reject_byte_escape",
    "compile",
    "search",
    "match",
    "fullmatch",
    "findall",
    "sub",
    "split",
    "escape",
}
SHARED_CONSTANTS = {"STDLIB_WS_BODY", "STDLIB_WS"}
SHARED_CLASSES = {"Flags"}


def _strip_docstrings(node: ast.AST) -> ast.AST:
    node = copy.deepcopy(node)
    for child in ast.walk(node):
        body = getattr(child, "body", None)
        if (
            isinstance(body, list)
            and body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            body.pop(0)
            if not body:
                body.append(ast.Pass())
    return node


def _top_level(tree: ast.Module) -> dict[str, ast.stmt]:
    out: dict[str, ast.stmt] = {}
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[stmt.name] = stmt
        elif isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
            target = stmt.targets[0]
            if isinstance(target, ast.Name):
                out[target.id] = stmt
    return out


def _dump(stmt: ast.stmt) -> str:
    return ast.dump(_strip_docstrings(stmt), annotate_fields=True)


CLI_TOP = _top_level(ast.parse(CLI_FILE.read_text()))
# `pytestmark` skips the test FUNCTIONS when the backend tree is absent, but it
# does not stop this module-level parse from running at collection time — an
# unconditional read would raise FileNotFoundError before the skip applies,
# breaking the packaged/partial-checkout path the skipif documents. Parse only
# when present; when absent BACKEND_TOP stays empty and every test is skipped.
BACKEND_TOP = (
    _top_level(ast.parse(BACKEND_FILE.read_text())) if BACKEND_FILE.is_file() else {}
)


@pytest.mark.parametrize("name", sorted(SHARED_FUNCTIONS | SHARED_CLASSES))
def test_shared_definition_is_identical(name: str) -> None:
    assert name in CLI_TOP, f"{name} missing from the CLI mirror"
    assert name in BACKEND_TOP, (
        f"{name} missing from the backend canonical — if it was renamed or "
        "removed there, mirror the change (and this guard) deliberately"
    )
    assert _dump(CLI_TOP[name]) == _dump(BACKEND_TOP[name]), (
        f"{name} drifted between cli mirror and backend canonical — mirror "
        "the backend change (docstrings are exempt; bodies are not)"
    )


@pytest.mark.parametrize("name", sorted(SHARED_CONSTANTS))
def test_shared_constant_is_identical(name: str) -> None:
    assert _dump(CLI_TOP[name]) == _dump(BACKEND_TOP[name]), (
        f"{name} drifted — this constant pins stdlib-vs-RE2 semantics and "
        "was swept exhaustively on the backend; the CLI must carry the "
        "identical value"
    )


def test_cli_protocols_are_subset_of_backend() -> None:
    """The trimmed Match/Pattern protocols may omit methods, never diverge.

    Every method the CLI protocol declares must exist on the backend's with
    an identical signature, so a backend signature fix propagates.
    """
    for cls in ("Match", "Pattern"):
        cli_methods = {
            s.name: s
            for s in CLI_TOP[cls].body  # type: ignore[union-attr]
            if isinstance(s, ast.FunctionDef)
        }
        backend_methods = {
            s.name: s
            for s in BACKEND_TOP[cls].body  # type: ignore[union-attr]
            if isinstance(s, ast.FunctionDef)
        }
        assert cli_methods, cls
        for method_name, method in cli_methods.items():
            assert method_name in backend_methods, (
                f"{cls}.{method_name} exists only in the CLI mirror"
            )
            assert _dump(method) == _dump(backend_methods[method_name]), (
                f"{cls}.{method_name} signature drifted from backend"
            )


def test_guard_surface_is_not_vacuous() -> None:
    # A mass rename on either side must fail loudly here rather than let the
    # parametrized tests quietly compare a shrinking set.
    present = (SHARED_FUNCTIONS | SHARED_CLASSES | SHARED_CONSTANTS) & set(CLI_TOP)
    assert len(present) == len(SHARED_FUNCTIONS | SHARED_CLASSES | SHARED_CONSTANTS)
