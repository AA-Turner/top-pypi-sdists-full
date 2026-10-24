"""THE FUNNEL LAW — raw Anthropic SDK use lives in the provider adapter, nowhere else.

A module that constructs its own ``AsyncAnthropic`` bypasses routing and cost
capture. Type-only SDK imports and annotations describe an injected client;
they do not construct one. The AST scan separates these from runtime use and
keeps aliased constructors and runtime uses of type-only imports blocking.

🚨 THE SCOPE, and why it moved (2026-09-08). This scan used to walk every ``.py``
under ``matrx_ai/`` and match the bare substring, so it went red the moment
``providers/tests/test_capture_client_sdk_flavor.py`` — the forcing-function test
for the httpx-flavor defect that killed EVERY Anthropic call at client
construction — named ``AsyncAnthropic`` in its provider census table. That test is
not a caller: it constructs SDK clients precisely to prove our capture client is
accepted, and it dials nothing. matrx-ai keeps its tests INSIDE the package (14
``tests/`` directories under ``matrx_ai/``), so a whole-package scan and a
"production callers only" rule were never the same rule; the scan now says which
one it is. Every production module is still scanned, and
``test_the_guard_still_bites`` is what keeps that claim honest — it plants a
violation in a scanned location and fails if the scan shrugs.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).parents[1] / "matrx_ai"

#: The one place raw SDK construction belongs.
SANCTIONED_ADAPTER = ("providers", "anthropic")


def _is_test_module(relative: Path) -> bool:
    """A test module — not a production path, and never a caller."""
    return (
        "tests" in relative.parts
        or relative.name.startswith("test_")
        or relative.name == "conftest.py"
    )


def _has_runtime_sdk_reference(source: str) -> bool:
    tree = ast.parse(source)
    postponed = any(isinstance(n, ast.ImportFrom) and n.module == "__future__" and any(a.name == "annotations" for a in n.names) for n in tree.body)
    # Only unique, unshadowed typing bindings can make a branch/type slot inert.
    typing_bindings: dict[str, str] = {}
    counts: dict[str, int] = {}
    sdk_names = {"AsyncAnthropic"}
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.ImportFrom):
            names = [a.asname or a.name for a in node.names]
            if node.module == "anthropic":
                sdk_names.update(a.asname or a.name for a in node.names if a.name == "AsyncAnthropic")
            if node in tree.body and node.module == "typing":
                typing_bindings.update({a.asname or a.name: "typing." + a.name for a in node.names})
        elif isinstance(node, ast.Import):
            names = [a.asname or a.name.split(".")[0] for a in node.names]
            if node in tree.body:
                typing_bindings.update({a.asname or "typing": "typing" for a in node.names if a.name == "typing"})
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            names = [node.id]
        elif isinstance(node, ast.arg):
            names = [node.arg]
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names = [node.name]
        elif isinstance(node, ast.ExceptHandler) and node.name:
            names = [node.name]
        elif type(node).__name__ in {"MatchAs", "MatchStar", "MatchMapping"}:
            names = [n for n in (getattr(node, "name", None), getattr(node, "rest", None)) if n]
        for name in names:
            counts[name] = counts.get(name, 0) + 1
    typing_bindings = {k: v for k, v in typing_bindings.items() if counts[k] == 1}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Attribute, ast.Subscript)) and isinstance(node.ctx, (ast.Store, ast.Del)):
            root = node
            while isinstance(root, (ast.Attribute, ast.Subscript)):
                root = root.value
            if isinstance(root, ast.Name) and typing_bindings.get(root.id) == "typing":
                typing_bindings.pop(root.id)
    if any(isinstance(n, ast.ImportFrom) and any(a.name == "*" for a in n.names) for n in ast.walk(tree)):
        typing_bindings.clear()

    def qualified(node):
        if isinstance(node, ast.Name):
            return typing_bindings.get(node.id)
        if isinstance(node, ast.Attribute) and qualified(node.value) == "typing":
            return "typing." + node.attr
        return None

    class Runtime(ast.NodeVisitor):
        found = False

        def visit_If(self, node):
            if qualified(node.test) == "typing.TYPE_CHECKING":
                for stmt in node.orelse:
                    self.visit(stmt)
            else:
                self.generic_visit(node)

        def visit_Name(self, node):
            self.found |= node.id in sdk_names

        def visit_Attribute(self, node):
            self.found |= node.attr == "AsyncAnthropic"
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            self.found |= any(a.name == "AsyncAnthropic" for a in node.names)

        def visit_Constant(self, node):
            self.found |= isinstance(node.value, str) and "AsyncAnthropic" in node.value

        def visit_Expr(self, node):
            if not isinstance(node.value, ast.Constant):
                self.generic_visit(node)

        def visit_arg(self, node):
            if node.annotation is not None and (not postponed or any(isinstance(n, ast.Call) for n in ast.walk(node.annotation))):
                self.visit(node.annotation)

        def visit_FunctionDef(self, node):
            for field, value in ast.iter_fields(node):
                if field == "returns" and postponed and (value is None or not any(isinstance(n, ast.Call) for n in ast.walk(value))):
                    continue
                for child in value if isinstance(value, list) else [value]:
                    if isinstance(child, ast.AST):
                        self.visit(child)

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_AnnAssign(self, node):
            self.visit(node.target)
            if not postponed or any(isinstance(n, ast.Call) for n in ast.walk(node.annotation)):
                self.visit(node.annotation)
            if node.value is not None:
                self.visit(node.value)

        def visit_Call(self, node):
            if qualified(node.func) == "typing.cast" and len(node.args) == 2 and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                self.visit(node.func)
                self.visit(node.args[1])
                for keyword in node.keywords:
                    self.visit(keyword.value)
            else:
                self.generic_visit(node)

    runtime = Runtime()
    runtime.visit(tree)
    return runtime.found


def _scan(root: Path) -> tuple[list[str], int]:
    """(violations, production modules actually read) — the second half matters.

    A scan that quietly stops reading files reports zero violations and reads
    identically to a clean repo. The count is returned so a caller can refuse
    a vacuous verdict.
    """
    violations: list[str] = []
    scanned = 0
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)
        if relative.parts[: len(SANCTIONED_ADAPTER)] == SANCTIONED_ADAPTER:
            continue
        if _is_test_module(relative):
            continue
        scanned += 1
        if _has_runtime_sdk_reference(path.read_text(encoding="utf-8")):
            violations.append(str(relative))
    return violations, scanned


def test_raw_anthropic_sdk_is_confined_to_provider_adapter():
    violations, scanned = _scan(PACKAGE_ROOT)

    assert scanned > 100, (
        "the funnel scan read only "
        f"{scanned} production modules — it has stopped walking the package, so a "
        "clean verdict here would mean nothing. Fix the scan, never this bound."
    )
    assert violations == [], (
        "Raw Anthropic SDK callers bypass routing and cost capture; route them "
        f"through execute_ai_request instead: {violations}"
    )


def test_the_guard_still_bites(tmp_path: Path) -> None:
    """Falsifiability: a planted off-funnel caller MUST be caught.

    Without this, the exemptions above could widen until the guard was quiet
    about everything — the exact way a guard rots into decoration.
    """
    fake_package = tmp_path / "matrx_ai"
    (fake_package / "providers" / "anthropic").mkdir(parents=True)
    (fake_package / "providers" / "tests").mkdir(parents=True)

    # The sanctioned adapter: allowed.
    (fake_package / "providers" / "anthropic" / "client.py").write_text(
        "from anthropic import AsyncAnthropic\n", encoding="utf-8"
    )
    # A test that names the class: allowed.
    (fake_package / "providers" / "tests" / "test_flavor.py").write_text(
        'SDKS = [("anthropic", "AsyncAnthropic")]\n', encoding="utf-8"
    )
    # A production module that builds its own client: NOT allowed.
    (fake_package / "rogue.py").write_text(
        "from anthropic import AsyncAnthropic\nclient = AsyncAnthropic()\n", encoding="utf-8"
    )

    violations, scanned = _scan(fake_package)

    assert violations == ["rogue.py"], (
        "the funnel scan no longer catches a production module constructing its own "
        f"Anthropic client (saw {violations!r}) — the exemptions have eaten the rule."
    )
    assert scanned == 1


@pytest.mark.parametrize("source", [
    "from anthropic import AsyncAnthropic as Raw\nclient = Raw()",
    "import anthropic as sdk\nclient = sdk.AsyncAnthropic()",
    "from typing import TYPE_CHECKING as TC\nTC = True\nif TC:\n from anthropic import AsyncAnthropic\n client = AsyncAnthropic()",
    "TYPE_CHECKING = True\nif TYPE_CHECKING:\n from anthropic import AsyncAnthropic",
    "from typing import TYPE_CHECKING\nfrom unknown import *\nif TYPE_CHECKING:\n from anthropic import AsyncAnthropic",
    "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n from anthropic import AsyncAnthropic as Raw\nclient = Raw()",
    "import typing as t\nt = other\nif t.TYPE_CHECKING:\n from anthropic import AsyncAnthropic",
    "import anthropic\nclient = getattr(anthropic, 'AsyncAnthropic')()",
    "from typing import cast\ncast = other\nx = cast('AsyncAnthropic', client)",
])
def test_runtime_sdk_construction_and_shadowed_typing_stay_blocking(source):
    assert _has_runtime_sdk_reference(source)


def test_type_only_sdk_contract_is_not_a_runtime_constructor():
    assert not _has_runtime_sdk_reference("from __future__ import annotations\nfrom typing import TYPE_CHECKING as TC, cast\nif TC:\n from anthropic import AsyncAnthropic as Raw\ndef f(client: 'Raw') -> Raw:\n return cast('Raw', client)")
    assert not _has_runtime_sdk_reference("from __future__ import annotations\nimport typing as t\nif t.TYPE_CHECKING:\n from anthropic import AsyncAnthropic\ndef f(client: AsyncAnthropic):\n return t.cast('AsyncAnthropic', client)")


@pytest.mark.parametrize("suffix", [
    "def f(x=Raw()): pass",
    "def f(x: Raw()): pass",
    "value: Raw = Raw()",
    "def f(x: Raw):\n return Raw()",
])
def test_type_only_import_cannot_hide_default_annotation_or_body_constructor(suffix):
    assert _has_runtime_sdk_reference("from __future__ import annotations\nfrom typing import TYPE_CHECKING\nif TYPE_CHECKING:\n from anthropic import AsyncAnthropic as Raw\n" + suffix)


@pytest.mark.parametrize("mutation", [
    "t.TYPE_CHECKING = True",
    "t.TYPE_CHECKING, spare = other",
    "t.__dict__['TYPE_CHECKING'] = True",
    "t.cast = other",
])
def test_mutated_typing_module_cannot_hide_runtime_sdk_use(mutation):
    assert _has_runtime_sdk_reference(f"import typing as t\n{mutation}\nif t.TYPE_CHECKING:\n from anthropic import AsyncAnthropic\n client = AsyncAnthropic()")
    assert _has_runtime_sdk_reference(f"import typing as t\n{mutation}\nclient = t.cast('AsyncAnthropic', other)")


def test_unaliased_typing_module_mutation_stays_blocking():
    assert _has_runtime_sdk_reference("import typing\ntyping.TYPE_CHECKING = True\nif typing.TYPE_CHECKING:\n from anthropic import AsyncAnthropic\n client = AsyncAnthropic()")
