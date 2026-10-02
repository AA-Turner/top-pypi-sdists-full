"""The MCP copy of the retrieval-query guidance matches the backend's.

The same check as `tests/unit/test_query_bag_parity.py`, from the other side of
the path filter: a change under `agent/` does not run the backend lanes, and a
change under `app/` does not run agent-ci, so one copy of this test cannot see
both kinds of edit. Skipped -- not failed -- when `app/` is absent, because this
tree is also published on its own as `probe-research`.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_BACKEND = _ROOT / "app" / "assistant" / "tools.py"
_MCP = Path(__file__).resolve().parents[1] / "src" / "probe" / "mcp" / "server.py"
_NAMES = ("_QUERY_BAG_DOC", "_PAPER_QUERY_DOC", "_FILTER_NARROWS_DOC")


def _constant(path: Path, name: str) -> str:
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            value = ast.literal_eval(node.value)
            assert isinstance(value, str)
            return value
    raise AssertionError(f"{path} no longer defines a module-level {name}")


@pytest.mark.parametrize("name", _NAMES)
def test_mcp_retrieval_guidance_matches_the_backend(name: str) -> None:
    if not _BACKEND.exists():
        pytest.skip("standalone agent checkout: no backend copy to compare against")
    assert _constant(_MCP, name) == _constant(_BACKEND, name), (
        f"{name} differs between the MCP and assistant surfaces -- edit both."
    )


def test_find_papers_asks_for_natural_language_and_search_knowledge_for_a_bag() -> None:
    """The two tools sit on different engines and must keep saying so."""
    from probe.mcp import server

    assert server._PAPER_QUERY_DOC in server._FP_QUERY_DOC
    assert "A BAG of keywords" not in server._FP_QUERY_DOC
    assert server._QUERY_BAG_DOC in server._SK_QUERY_DOC
    assert "natural-language description" not in server._SK_QUERY_DOC


def test_every_search_filter_says_it_narrows() -> None:
    """The bag belongs to `query` alone. Each argument that ANDs against it has
    to say so where the model reads it, or the dump lands on the filters."""
    from probe.mcp import server

    for doc in (
        server._FP_CATEGORIES_DOC,
        server._FP_AUTHORS_DOC,
        server._FP_PUB_FROM_DOC,
        server._FP_PUB_TO_DOC,
        server._SK_SEARCH_IN_DOC,
    ):
        assert server._FILTER_NARROWS_DOC in doc
