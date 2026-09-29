"""There is ONE act-as-the-person wrapper: ``matrx_ai.tools.person_session.acts_as_the_person``.

A tool that grows its own copy (its own ROLLBACK exception, its own refusal
messages) drifts from the shared one the day either changes. The task tool
carried such a copy until 2026-09-27; this pins that every action of the
person-scoped tools is wrapped by the shared primitive and that no tool module
defines a private rollback wrapper again.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

_IMPL = Path(__file__).resolve().parents[1] / "matrx_ai" / "tools" / "implementations"

PERSON_SCOPED_ACTIONS = {
    "tasks": ["task_get", "task_list", "task_create", "task_update", "task_delete"],
    "notes": ["note_get", "note_list", "note_create"],
}


@pytest.mark.parametrize("module,actions", sorted(PERSON_SCOPED_ACTIONS.items()))
def test_person_scoped_actions_use_the_shared_wrapper(module: str, actions: list[str]) -> None:
    mod = importlib.import_module(f"matrx_ai.tools.implementations.{module}")
    for name in actions:
        fn = getattr(mod, name)
        assert getattr(fn, "__acts_as_the_person__", False), (
            f"{module}.{name} is not wrapped by person_session.acts_as_the_person"
        )


def test_no_tool_module_defines_its_own_rollback_wrapper() -> None:
    offenders = []
    for path in sorted(_IMPL.glob("*.py")):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "_RollBack":
                offenders.append(f"{path.name}:{node.lineno}")
    assert offenders == [], f"a private act-as-the-person copy lives in {offenders}"
