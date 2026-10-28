"""A mandated call never pins a model in code.

The mandate's agent owns the model. ``summarize_content`` passed
``config_overrides={"model": model_id}`` with ``model_id="gemini-3.5-flash"``
as its default, so every web summary ran on that model while the
``tools.summarize_content`` agent named Gemini 3.8 Flash (2026-10-23).

The guard: inside ``matrx_ai``, no ``config_overrides`` dict carries a
``"model"`` whose value is a string literal, or a parameter whose default is
a string literal. A caller that genuinely chooses a model passes it in
explicitly (default ``None``), which stays allowed.
"""

from __future__ import annotations

import ast
from pathlib import Path

import matrx_ai

ROOT = Path(matrx_ai.__file__).parent


def _literal_defaults(fn: ast.AST) -> set[str]:
    if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return set()
    args = fn.args
    positional = args.posonlyargs + args.args
    pairs = list(zip(positional[len(positional) - len(args.defaults):], args.defaults))
    pairs += [(a, d) for a, d in zip(args.kwonlyargs, args.kw_defaults) if d is not None]
    return {
        a.arg for a, d in pairs if isinstance(d, ast.Constant) and isinstance(d.value, str)
    }


def pinned_models(source: str) -> list[int]:
    tree = ast.parse(source)
    found: list[int] = []

    def visit(node: ast.AST, defaults: set[str]) -> None:
        defaults = defaults | _literal_defaults(node)
        if isinstance(node, ast.keyword) and node.arg == "config_overrides" and isinstance(
            node.value, ast.Dict
        ):
            for key, value in zip(node.value.keys, node.value.values):
                if not (isinstance(key, ast.Constant) and key.value == "model"):
                    continue
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    found.append(node.value.lineno)
                elif isinstance(value, ast.Name) and value.id in defaults:
                    found.append(node.value.lineno)
        for child in ast.iter_child_nodes(node):
            visit(child, defaults)

    visit(tree, set())
    return found


def test_the_detector_catches_both_shapes():
    assert pinned_models(
        'async def f(x, model_id: str = "m"):\n    run(config_overrides={"model": model_id})\n'
    )
    assert pinned_models('run(config_overrides={"model": "gemini-3.5-flash"})\n')
    assert not pinned_models(
        'async def f(x, model_id: str | None = None):\n'
        '    run(config_overrides={"model": model_id} if model_id else None)\n'
    )


def test_no_mandated_call_in_matrx_ai_pins_a_model():
    offenders = [
        f"{path.relative_to(ROOT)}:{line}"
        for path in sorted(ROOT.rglob("*.py"))
        # A test that proves an override is carried passes one on purpose; only shipped code is held.
        if "tests" not in path.relative_to(ROOT).parts
        for line in pinned_models(path.read_text(encoding="utf-8"))
    ]
    assert not offenders, (
        "A model is pinned in code where the mandate's agent should decide: "
        + ", ".join(offenders)
    )
