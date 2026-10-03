"""The MCP's retrieval-query guidance keeps the two search tools apart.

This file used to hold the MCP copy identical to the dashboard assistant's
(`app/assistant/tools.py`). The assistant now reads through the hosted MCP and
its own copy is gone (#2223), so there is nothing to compare: the backend's
`tests/unit/test_query_bag_parity.py` pins that the guidance lives once, and
what it says.
"""

from __future__ import annotations


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
