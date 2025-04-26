import pytest

import snowflake.core._http_requests


@pytest.mark.parametrize(
    ("inputs", "expected_output"),
    (
        # Simplest case
        (("simple_url", {}, {}, ""), "simple_url"),
        # Embedding case
        (("databases/{database}", {"database": "asd"}, {}, ""), "databases/asd"),
        # Collections formats
        (
            (
                "items/{items}",
                {"items": ["bread", "butter", "cheese", "cold_cuts"]},
                {"items": "csv"},
                "",
            ),
            "items/bread%2Cbutter%2Ccheese%2Ccold_cuts",
        ),
        # Safe quoting (same as last one, but don't change ',' into '%2C')
        (
            (
                "items/{items}",
                {"items": ["bread", "butter", "cheese", "cold_cuts"]},
                {"items": "csv"},
                ",/",
            ),
            "items/bread,butter,cheese,cold_cuts",
        ),
    )
)
def test_resolve_url(inputs, expected_output):
    assert snowflake.core._http_requests.resolve_url(*inputs) == expected_output
