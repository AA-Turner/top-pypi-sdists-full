"""A step that OFFERS ``allow_empty_structured_output`` must hand it to the all-zero refusal.

Run Mandate and Produce share Run Agent's ``AgentStartConfig`` (which carries the setting) but
called ``normalize_completed_result`` without ``step_config``, so an author's "nothing found is a
real answer here" was silently ignored and the step failed anyway (Vision Interview answer
tracker, 2026-10-27). Every call in a module that offers the setting must pass ``step_config``.
"""

from __future__ import annotations

import ast
from pathlib import Path

GRAPH_NODES = Path(__file__).resolve().parents[1] / "matrx_ai" / "graph_nodes"
OFFERS = ("AgentStartConfig", "allow_empty_structured_output")


def _calls_without_step_config(tree: ast.AST) -> list[int]:
    missing = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)
        direct = name == "normalize_completed_result"
        threaded = (
            name == "to_thread"
            and node.args
            and isinstance(node.args[0], ast.Name)
            and node.args[0].id == "normalize_completed_result"
        )
        if (direct or threaded) and not any(k.arg == "step_config" for k in node.keywords):
            missing.append(node.lineno)
    return missing


def offenders(root: Path = GRAPH_NODES) -> dict[str, list[int]]:
    found = {}
    for path in sorted(root.glob("*.py")):
        if path.name == "shared.py":
            continue
        text = path.read_text()
        if not any(word in text for word in OFFERS):
            continue
        missing = _calls_without_step_config(ast.parse(text))
        if missing:
            found[path.name] = missing
    return found


def test_every_step_that_offers_the_setting_passes_it():
    assert offenders() == {}, (
        "these steps offer allow_empty_structured_output but never pass it to "
        f"normalize_completed_result(step_config=...): {offenders()}"
    )


def test_the_guard_can_fail(tmp_path):
    (tmp_path / "bad_action.py").write_text(
        "from x import AgentStartConfig\n"
        "async def run(completed):\n"
        "    return await asyncio.to_thread(normalize_completed_result, completed)\n"
    )
    assert offenders(tmp_path) == {"bad_action.py": [3]}
