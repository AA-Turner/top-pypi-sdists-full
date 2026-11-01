"""agent/twins.json: every Client resource module is listed, names its app/ twins in its header,
and each twin exists in this repo (plan: wire twins table)."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[2]
REPO = AGENT.parent
TABLE = json.loads((AGENT / "twins.json").read_text())["client_resources"]
RESOURCES = AGENT / "src/probe/sdk/client/resources"


def test_every_client_resource_module_is_in_the_table() -> None:
    found = {p.relative_to(REPO).as_posix() for p in RESOURCES.rglob("*.py") if p.name != "__init__.py"}
    assert found == set(TABLE)


@pytest.mark.parametrize(("module", "twins"), sorted(TABLE.items()))
def test_each_module_header_names_its_twins(module: str, twins: list[str]) -> None:
    header = (ast.get_docstring(ast.parse((REPO / module).read_text())) or "").split("\n\n")[0]
    named = header.rsplit("(twin", 1)[-1]
    assert all(twin in named for twin in twins), f"{module}: header must name {twins}"


@pytest.mark.skipif(not (REPO / "app").is_dir(), reason="the server tree is not beside this checkout")
@pytest.mark.parametrize("twin", sorted({t for twins in TABLE.values() for t in twins}))
def test_each_twin_is_a_server_domain(twin: str) -> None:
    assert (REPO / twin / "__init__.py").is_file()
