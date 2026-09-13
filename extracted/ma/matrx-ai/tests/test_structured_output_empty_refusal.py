"""THE ALL-ZERO ANSWER IS REFUSED — proven on the live run that shipped one.

WALL W59 (Expert Book Challenge, 2026-09-12). Production run
``9347de24-efcf-4a4f-876a-b00aa4e13f34`` of "Watson Parenting Adviser": the
prescriber step (``n-5e3a67afcd``, agent
``13085498-e146-46fa-bbfe-31354afda5cc``, Sonnet 5, provider-enforced output
schema) got a complete, correct case reading and answered in 93 output tokens
with every field at its zero value. ``structured_output_contract_satisfied``
was true, ``finish_reason`` was ``stop``, the step SUCCEEDED, the run
COMPLETED, and a parent was shown that hollow object as her regimen beside a
full letter. Nothing screamed.

WHY THIS IS A FORCING TEST, not a green rubber stamp:

* The three payloads are the REAL ones, read out of the production database
  and saved verbatim in ``tests/fixtures/w59_prescriber_outputs.json`` —
  the empty answer that shipped, the 9-instruction regimen the same node
  produced on run ``60166914-b34b-4705-9991-6786da3e0d97``, and the agent's
  own declared ``required`` list.
* They run through the REAL ``normalize_completed_result`` — the one function
  every ai.* graph node's answer is accepted by — against a REAL
  ``response_format``, with the real JSON text parsed by the real funnel.
  Nothing about the refusal is simulated.
* It fails on the code as it stood this morning: delete the emptiness check in
  ``matrx_ai.graph_nodes.shared`` and ``test_the_empty_answer_that_shipped_is_refused``
  goes red, because the shipped payload is a Success there.

Run with:
  uv run pytest packages/matrx-ai/tests/test_structured_output_empty_refusal.py -v
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.graph_nodes.shared import (
    configure_empty_structured_output,
    normalize_completed_result,
)
from matrx_graph.types.result import Failure, Success

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "w59_prescriber_outputs.json").read_text()
)
REQUIRED_SCHEMA: dict[str, Any] = FIXTURE["required_schema"]
EMPTY: dict[str, Any] = FIXTURE["empty"]
GOOD: dict[str, Any] = FIXTURE["good"]
# The 60166914 run ran on the PRIOR prescriber agent, whose contract had no
# ``all_cited_rule_ids`` — so its answer is judged against the contract it was
# actually given, never against a later one.
PRIOR_SCHEMA: dict[str, Any] = FIXTURE["required_schema_prior"]


def _completed(payload: Any, *, schema: dict[str, Any] | None = REQUIRED_SCHEMA) -> Any:
    """A CompletedRequest stand-in carrying a REAL response_format and the
    REAL assistant text — the two facts the choke point reads."""
    response_format = (
        {
            "type": "json_schema",
            "json_schema": {"name": "the_regimen", "schema": schema, "strict": True},
        }
        if schema is not None
        else None
    )
    text = json.dumps(payload)
    return SimpleNamespace(
        request=SimpleNamespace(
            config=SimpleNamespace(response_format=response_format),
            conversation_id="ac91fc6a-7889-40e2-b123-0880031c6b55",
            request_id="b6156e7b-9b75-4738-8558-0c04d9bd0477",
        ),
        final_response=SimpleNamespace(
            messages=[
                SimpleNamespace(role="assistant", content=[{"type": "text", "text": text}])
            ],
            finish_reason="stop",
        ),
        total_usage=None,
        timing_stats={},
        tool_call_stats={},
        iterations=1,
        metadata={"finish_reason": "stop"},
    )


@pytest.fixture(autouse=True)
def _platform_default_is_refuse():
    """Every case runs on the shipped default, restored after."""
    configure_empty_structured_output(allow_empty=False)
    yield
    configure_empty_structured_output(allow_empty=False)


def test_the_empty_answer_that_shipped_is_refused():
    """(i) The exact payload run 9347de24 delivered to a parent."""
    result = normalize_completed_result(_completed(EMPTY))

    assert isinstance(result, Failure), "the all-zero regimen passed as a success again"
    assert result.error.code == "structured_output_empty"
    message = result.error.message
    assert "empty but valid" in message
    assert "the_regimen" in message, "the sentence must name what came back empty"
    assert "nothing to deliver" in message
    # Every required field is named, so a human reading the run box sees which.
    for field in REQUIRED_SCHEMA["required"]:
        assert field in message
    details = result.error.details or {}
    assert set(details["empty_fields"]) == set(REQUIRED_SCHEMA["required"])
    assert details["fields_considered"] == "required"
    assert "allow_empty_structured_output" in details["remedy"]


def test_the_real_regimen_passes():
    """(ii) The SAME node's answer on run 60166914 — 9 instructions."""
    result = normalize_completed_result(_completed(GOOD, schema=PRIOR_SCHEMA))

    assert isinstance(result, Success), "a real 9-instruction regimen was refused"
    assert len(result.result.structured_output["instructions"]) == 9
    assert result.result.structured_output["headline_finding"].startswith("The handling has built")


def test_one_filled_field_is_enough():
    """This refuses NOTHING-AT-ALL, never a thin answer. A single real field —
    here the honest 'I cannot reach this case' headline — passes."""
    partial = dict(EMPTY, headline_finding="No rule in the book reaches this household.")
    assert isinstance(normalize_completed_result(_completed(partial)), Success)


def test_a_legitimately_empty_step_passes_with_the_node_knob():
    """(iii) 'No issues found' is a real answer where the AUTHOR says it is.

    The knob is read off the node's own config object — exactly what
    ``ai.agent.start`` hands the choke point.
    """
    config = SimpleNamespace(allow_empty_structured_output=True)
    result = normalize_completed_result(_completed(EMPTY), step_config=config)

    assert isinstance(result, Success), "the author's allow-empty knob was ignored"
    assert result.result.structured_output == EMPTY


def test_the_org_knob_can_allow_empty_and_the_node_still_overrules_it():
    """The organization decides the floor; the step decides itself."""
    configure_empty_structured_output(allow_empty=True)
    assert isinstance(normalize_completed_result(_completed(EMPTY)), Success)

    refusing_node = SimpleNamespace(allow_empty_structured_output=False)
    result = normalize_completed_result(_completed(EMPTY), step_config=refusing_node)
    assert isinstance(result, Failure)
    assert result.error.code == "structured_output_empty"


def test_a_step_with_no_declared_schema_is_untouched():
    """Prose steps have no contract to be empty against — nothing changes."""
    result = normalize_completed_result(_completed(EMPTY, schema=None))
    assert isinstance(result, Success)
