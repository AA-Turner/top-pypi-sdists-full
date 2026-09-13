"""THE OUTPUT-CEILING CLASSIFIER — a cut-off reply says so, with the remedy.

Live defect this guards (2026-09-12, workflow run
23e72bf5-8b41-496e-a475-428f880d219f, step "The evidence ledger"): a saved
agent with a declared structured output hit exactly 32,000 output tokens
(claude-sonnet-5, finish_reason=max_tokens). The JSON was therefore
incomplete, and the workflow node reported ``structured_output_invalid``
("could not be parsed and validated") — the wrong cause, with no remedy. Same
masking class as night-1 walls W9 and W17.

Before the fix these tests fail: every truncated case surfaced as a parse
failure.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_graph.failure import Cause, failure_from_text
from matrx_graph.types.result import Failure, Success

from matrx_ai.graph_nodes.shared import normalize_completed_result

# The new names are imported INSIDE the tests on purpose: the behavioural
# tests below must fail with a real assertion (the wrong error surfaced), not
# with a collection-time ImportError, when run against the code as it was
# before this fix.
TRUNCATION_METADATA_KEY = "truncation"

_ENVELOPE = {
    "name": "ledger",
    "schema": {"type": "object", "properties": {"entries": {"type": "array"}}},
}

# The live row: finish_reason=max_tokens, output_tokens exactly at the ceiling.
_LIVE_CEILING = 32_000


def _completed(
    *,
    final_text: str,
    truncated: bool,
    response_format: dict[str, Any] | None = None,
    output_tokens: int = _LIVE_CEILING,
) -> SimpleNamespace:
    config = SimpleNamespace(
        messages=[],
        response_format=response_format,
        model="claude-sonnet-5",
        max_output_tokens=_LIVE_CEILING,
    )
    request = SimpleNamespace(config=config, conversation_id="conv-1", request_id="req-1")
    metadata: dict[str, Any] = {}
    finish_reason = "stop"
    if truncated:
        finish_reason = "max_tokens"
        metadata = {
            "status": "truncated",
            "finish_reason": "max_tokens",
            "error_type": "truncated_response",
            TRUNCATION_METADATA_KEY: {
                "reason": "max_tokens",
                "model": "claude-sonnet-5",
                "max_output_tokens": _LIVE_CEILING,
                "interrupted_tool_calls": [],
            },
        }
    final_response = SimpleNamespace(
        messages=None, text=final_text, finish_reason=finish_reason
    )
    usage = SimpleNamespace(
        total=SimpleNamespace(
            input_tokens=118_587,
            output_tokens=output_tokens,
            total_tokens=118_587 + output_tokens,
            total_cost=0.0,
        ),
        by_model={},
    )
    return SimpleNamespace(
        request=request,
        final_response=final_response,
        total_usage=usage,
        timing_stats={},
        tool_call_stats={},
        iterations=1,
        metadata=metadata,
    )


def test_truncated_completion_is_classified_as_an_output_ceiling_hit() -> None:
    from matrx_ai.config.finish_reason import completion_truncation

    ceiling = completion_truncation(_completed(final_text='{"entries": [', truncated=True))
    assert ceiling is not None
    assert ceiling.finish_reason == "max_tokens"
    assert ceiling.max_output_tokens == _LIVE_CEILING
    assert ceiling.output_tokens == _LIVE_CEILING
    assert ceiling.model == "claude-sonnet-5"


def test_a_clean_completion_is_never_called_truncated() -> None:
    from matrx_ai.config.finish_reason import completion_truncation

    assert completion_truncation(_completed(final_text="prose", truncated=False)) is None


def test_the_message_names_the_limit_and_the_remedy() -> None:
    from matrx_ai.config.finish_reason import completion_truncation, output_ceiling_message

    ceiling = completion_truncation(_completed(final_text='{"entries": [', truncated=True))
    assert ceiling is not None
    message = output_ceiling_message(ceiling, what="the structured answer")
    assert "cut off at its output limit (32,000 tokens)" in message
    assert "the structured answer" in message
    assert "Split the input into smaller pieces or raise the step's output limit." in message


def test_declared_structured_output_cut_at_the_ceiling_surfaces_as_truncation() -> None:
    """THE LIVE CASE. Incomplete JSON + finish_reason=max_tokens must NOT be
    reported as a parse failure."""
    result = normalize_completed_result(
        _completed(
            # Cut off before the JSON ever started — the live shape, where
            # nothing (not even the repair pass) can recover an object.
            final_text="Working through the exhibits one by one: exhibit 1 shows",
            truncated=True,
            response_format={"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )

    assert isinstance(result, Failure)
    assert result.error.code == "output_truncated"
    assert "could not be parsed" not in result.error.message
    assert "cut off at its output limit (32,000 tokens)" in result.error.message
    details = result.error.details or {}
    assert details["finish_reason"] == "max_tokens"
    assert details["max_output_tokens"] == _LIVE_CEILING
    assert details["output_tokens"] == _LIVE_CEILING
    assert details["masked_code"] == "structured_output_invalid"
    # The billed usage still travels for cost settlement.
    assert details["usage"]["output_tokens"] == _LIVE_CEILING


def test_genuinely_malformed_output_keeps_the_parse_failure_wording() -> None:
    result = normalize_completed_result(
        _completed(
            final_text="I'm afraid I can't answer that in JSON.",
            truncated=False,
            response_format={"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )

    assert isinstance(result, Failure)
    assert result.error.code == "structured_output_invalid"
    assert "could not be parsed" in result.error.message


def test_valid_structured_output_still_succeeds() -> None:
    # The payload carries a real entry on purpose: `{"entries": []}` is
    # schema-valid and semantically EMPTY, and since W59 (2026-09-12) the same
    # choke point refuses that by name — see
    # tests/test_structured_output_empty_refusal.py. This case is about the
    # ceiling classifier, so it uses an answer that actually says something.
    result = normalize_completed_result(
        _completed(
            final_text='{"entries": [{"title": "one real row"}]}',
            truncated=False,
            response_format={"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )
    assert isinstance(result, Success)


def test_any_caller_code_is_reclassified_by_the_one_classifier() -> None:
    """``ai.extract`` and the kind-bound produce node route through the same
    door — a truncated turn is never their own parse-failure code."""
    from matrx_ai.graph_nodes.shared import ai_output_failure

    truncated = _completed(final_text="", truncated=True)
    for code in ("extract_parse_failed", "kind_output_missing"):
        result = ai_output_failure(
            truncated, code=code, message="…parse failure wording…", what="the extraction"
        )
        assert isinstance(result, Failure)
        assert result.error.code == "output_truncated"
        assert (result.error.details or {})["masked_code"] == code


def test_the_engine_maps_the_truncation_to_its_own_cause() -> None:
    """A node code the workflow engine cannot classify lands as engine_error
    and the person is told nothing useful — so the ladder must know both the
    code and the sentence."""
    from matrx_ai.config.finish_reason import completion_truncation, output_ceiling_message

    ceiling = completion_truncation(_completed(final_text="", truncated=True))
    assert ceiling is not None
    sentence = output_ceiling_message(ceiling, what="the structured answer")
    assert failure_from_text(f"output_truncated {sentence}").cause == Cause.OUTPUT_TRUNCATED
    assert (
        failure_from_text(
            "structured_output_invalid AI completed, but its declared structured "
            "output could not be parsed and validated."
        ).cause
        == Cause.AI_OUTPUT_UNUSABLE
    )


def test_a_truncated_turn_whose_json_repair_salvages_a_partial_never_succeeds() -> None:
    """THE SILENT-PARTIAL CASE. json-repair can CLOSE an object the model never
    finished, so a turn cut off at the ceiling used to come back successful
    carrying half a ledger. A declared schema + a truncated turn fails — and
    the salvage is visible, never the answer."""
    cut_off_mid_object = (
        '{"entries": [{"claim": "exhibit 1 is dated 2019", "source": "Ex. 1"}, '
        '{"claim": "exhibit 2 contradicts it", "source": "Ex'
    )
    result = normalize_completed_result(
        _completed(
            final_text=cut_off_mid_object,
            truncated=True,
            response_format={"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )

    assert isinstance(result, Failure), "a salvaged partial must never be a silent success"
    assert result.error.code == "output_truncated"
    details = result.error.details or {}
    assert details["structured_output_partial"] is True
    # The salvage is carried, so the run box and a human can see how far it got.
    assert details["partial_structured_output"]["entries"][0]["source"] == "Ex. 1"
    assert details["masked_code"] == "structured_output_invalid"


def test_an_untruncated_turn_with_a_valid_object_is_not_marked_partial() -> None:
    result = normalize_completed_result(
        _completed(
            final_text='{"entries": [{"claim": "complete", "source": "Ex. 1"}]}',
            truncated=False,
            response_format={"type": "json_schema", "json_schema": _ENVELOPE},
        )
    )
    assert isinstance(result, Success)
    assert result.result.structured_output == {
        "entries": [{"claim": "complete", "source": "Ex. 1"}]
    }
