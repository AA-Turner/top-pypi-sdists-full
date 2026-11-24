"""C87: models send one search as a plain string ("queries": "boise population"); it is one query.

Live: 4 web search calls refused on 2026-11-09 (claude-sonnet-5-5) with "Input should be a valid list".
A broken array written as a string (it holds quotes, or starts with "[") is never run as one query.
"""
import pytest
from pydantic import ValidationError

from matrx_ai.tools.arg_models.web_args import WebArgs, WebResearchArgs, WebSearchArgs


def test_a_plain_string_is_one_query_on_the_wire_model():
    parsed = WebArgs.model_validate({"action": "search", "queries": "Boise city Idaho population 2024 estimate"}).root
    assert parsed.queries == ["Boise city Idaho population 2024 estimate"]


def test_a_plain_string_is_one_query_on_the_worker_models():
    assert WebSearchArgs(queries="mars facts").queries == ["mars facts"]
    assert WebResearchArgs(queries="mars facts", instructions="x").queries == ["mars facts"]


@pytest.mark.parametrize(
    "sent",
    [
        'Calvin Harris tour 2027", "Mau P tour 2027',  # a broken array: never one garbled query
        '["a", "b"',
        "   ",
        "None",
        "null",
        "{}",
        "boise population\nmars facts",  # two queries on two lines is not one query
    ],
)
def test_a_string_that_is_not_one_plain_query_is_still_refused(sent):
    with pytest.raises(ValidationError):
        WebArgs.model_validate({"action": "search", "queries": sent})


def test_more_than_five_queries_reach_the_search_which_runs_five():
    # Owner ruling, C87 round 2 (2026-11-10): strict providers strip maxItems, so the wire takes 6+ and the search
    # runs the first five and names the rest (test_a_search_past_five_queries_runs_five_and_names_the_rest.py).
    parsed = WebArgs.model_validate({"action": "search", "queries": [f"q{i}" for i in range(6)]})
    assert len(parsed.root.queries) == 6
