"""Live structural check for the Anthropic provider boundary."""

from __future__ import annotations

import os

import pytest

from matrx_graph.nodes.http.get import HttpGetConfig, HttpGetExecutor, HttpGetInput


async def test_anthropic_models_endpoint_returns_a_model_catalog() -> None:
    """The generic HTTP node can authenticate to and parse a live provider."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY is not available")

    outcome = await HttpGetExecutor().execute(
        ctx=None,  # type: ignore[arg-type]
        inputs=HttpGetInput(
            url="https://api.anthropic.com/v1/models",
            headers={
                "anthropic-version": "2023-06-01",
                "x-api-key": api_key,
            },
        ),
        config=HttpGetConfig(timeout_s=30.0),
    )

    assert outcome.status == "success", outcome
    response = outcome.result
    assert response.status == 200, response.text
    assert isinstance(response.body, dict)
    assert isinstance(response.body.get("data"), list)
    assert response.body["data"], "Anthropic returned an empty model catalog"
    assert all(isinstance(item.get("id"), str) for item in response.body["data"])
