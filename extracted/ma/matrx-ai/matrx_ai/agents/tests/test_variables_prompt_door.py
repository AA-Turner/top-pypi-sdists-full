"""The prompt door — __kind never leaks into an agent's context.

Plan §4.2 / audit hard problem 4: a prompt is an external mind, and one of
exactly two places where stripping the discriminator remains law.
"""

from __future__ import annotations

import json

from matrx_ai.agents.variables import AgentVariable


def _var(value):
    var = AgentVariable.from_dict({"name": "materials"})
    var.value = value
    return var


def test_kind_markers_are_stripped_from_prompt_values() -> None:
    rendered = _var(
        {
            "__kind": "web_search_results",
            "query": "pizza",
            "web": [{"__kind": "web_result", "url": "https://a"}],
        }
    ).get_value()
    parsed = json.loads(rendered)
    assert "__kind" not in parsed
    assert "__kind" not in parsed["web"][0]
    # The DATA is fully intact — only the wire vocabulary is withheld.
    assert parsed["query"] == "pizza"
    assert parsed["web"][0]["url"] == "https://a"


def test_scalars_and_plain_structures_are_untouched() -> None:
    assert _var("plain text").get_value() == "plain text"
    assert json.loads(_var({"a": 1}).get_value()) == {"a": 1}
