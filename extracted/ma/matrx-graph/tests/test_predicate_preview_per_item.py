"""W57 — an author-written predicate must be TRYABLE against a sample.

W58 closed the mechanism (an inert predicate now fails the step) and made
``dry_run`` WARN when a predicate answers the same thing for every sample item.
A warning is not the affordance. The wall W57 left open is this: the author who
wrote ``kept == 0`` as if the filter kept the BAD ids had no way, anywhere, to
see what the filter actually answered before the run was paid for.

So ``dry_run`` now carries a ``predicate_preview`` — the expression, the binding
``inputs`` was given, and ONE ROW PER SAMPLE ITEM with the item, the value the
predicate returned, and kept/dropped (or passed/failed). One evaluation:
``_evaluate_predicate`` is called once and both the warnings and this table come
out of it.

Every fixture here is the real 2026-09-12 incident: the recovered v43 predicate
and the 14 ids "Watson's" case reader really cited
(``tests/fixtures/watson_rulebook_ids.json``), all 14 of which are real rules.
"""

from __future__ import annotations

import json
import pathlib

from matrx_graph import NodeRegistry, compile_graph
from matrx_graph.dry_run import (
    PREDICATE_PREVIEW_ROW_LIMIT,
    DryRunSample,
    _evaluate_predicate,
    dry_run,
)
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.types.definition import Definition



def _registry() -> NodeRegistry:
    """A registry of this test's OWN — never ``default_registry()``. Mutating
    the process-wide registry at import time leaks into every other test in the
    session (it flipped the live judge e2e into replay mode when this file was
    collected beside it)."""
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


_FIXTURE = json.loads(
    (pathlib.Path(__file__).parent / "fixtures" / "watson_rulebook_ids.json").read_text()
)
RULEBOOK_IDS: list[str] = _FIXTURE["rulebook_ids"]
CITED_IDS: list[str] = _FIXTURE["cited_ids"]

#: The v43 predicate, verbatim from the authoring tool_trace.
V43_PREDICATE = "('|' + str(inputs) + '|') not in '|" + "|".join(RULEBOOK_IDS) + "|'"

#: The SAME expression with the sandbox's invisible wrapper written out — this
#: is exactly what v43 computed at run time, spelled so the W58 refusal (which
#: only fires on bare `inputs`) lets it through. It kept all 14 real ids, and
#: that is the answer the author needed to SEE.
V43_AS_EVALUATED = (
    "('|' + str({'value': inputs['value']}) + '|') not in '|" + "|".join(RULEBOOK_IDS) + "|'"
)

#: What the author meant: keep the ids that are NOT in the rulebook.
CORRECT_PREDICATE = "('|' + inputs['value'] + '|') not in '|" + "|".join(RULEBOOK_IDS) + "|'"


def _filter_definition(predicate: str, items: list) -> Definition:
    """A real one-step ``data.filter`` workflow whose items are the real ids."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "check_case_ids",
                    "type": "data",
                    "position": {"x": 0.0, "y": 0.0},
                    "data": {
                        "spec_type": "data.filter",
                        "label": "Check the cited rule ids",
                        "input": {"items": items},
                        "config": {"predicate": predicate},
                    },
                }
            ],
            "edges": [],
        }
    )


def _preview(predicate: str, items: list):
    registry = _registry()
    graph = compile_graph(_filter_definition(predicate, items), registry=registry)
    report = dry_run(graph, inputs={}, samples={}, registry=registry)
    return report.nodes["check_case_ids"].predicate_preview


# --------------------------------------------------------------------------
# 1. The table itself — 14 real ids, 14 rows, each labeled.
# --------------------------------------------------------------------------


def test_the_incident_data_is_the_real_thing() -> None:
    assert len(RULEBOOK_IDS) == 200
    assert len(CITED_IDS) == 14
    assert [c for c in CITED_IDS if c not in RULEBOOK_IDS] == []


def test_preview_shows_every_cited_id_as_a_kept_row_and_screams_constant() -> None:
    """The incident, made visible: 14 rows, all kept, and the scream."""
    preview = _preview(V43_AS_EVALUATED, list(CITED_IDS))
    assert preview is not None
    assert preview.kind == "filter"
    assert preview.expression == V43_AS_EVALUATED
    assert preview.total == 14
    assert (preview.kept, preview.dropped, preview.errors) == (14, 0, 0)
    assert len(preview.rows) == 14
    assert preview.truncated is False
    assert [r.verdict for r in preview.rows] == ["kept"] * 14
    assert [r.result for r in preview.rows] == [True] * 14
    # Each row names the REAL id it was tried against.
    for index, cited in enumerate(CITED_IDS):
        assert preview.rows[index].index == index
        assert cited in preview.rows[index].item
    # The constant-predicate scream rides the same one evaluation.
    assert preview.constant is True
    assert len(preview.warnings) == 1
    assert "returned the same value for every one of the 14 sample items" in preview.warnings[0]
    assert "kept all of them" in preview.warnings[0]
    assert "inputs['value']" in preview.warnings[0]
    assert "kept 14, dropped 0" in preview.summary
    # And the binding — the one fact W58 proved nobody could find before
    # writing the expression — is stated on the table.
    assert "inputs['value']" in preview.binding


def test_preview_rows_carry_the_sandbox_reason_when_an_item_raises() -> None:
    """The real v43 text: every row is an error row naming the remedy."""
    preview = _preview(V43_PREDICATE, list(CITED_IDS))
    assert preview is not None
    assert preview.total == 14
    assert preview.errors == 14
    assert (preview.kept, preview.dropped) == (0, 0)
    assert [r.verdict for r in preview.rows] == ["error"] * 14
    assert all(r.error and "inputs['value']" in r.error for r in preview.rows)
    assert "not evaluable against sample item 0 of 14" in preview.warnings[0]
    assert "could not be evaluated at all" in preview.summary


def test_preview_of_the_correct_gate_discriminates_and_does_not_scream() -> None:
    hallucinated = [*CITED_IDS, "a-rule-watson-invented"]
    preview = _preview(CORRECT_PREDICATE, hallucinated)
    assert preview is not None
    assert (preview.kept, preview.dropped, preview.errors) == (1, 14, 0)
    assert preview.constant is False
    assert preview.warnings == []
    kept_rows = [r for r in preview.rows if r.verdict == "kept"]
    assert len(kept_rows) == 1
    assert "a-rule-watson-invented" in kept_rows[0].item


# --------------------------------------------------------------------------
# 2. Bounded, and honest about it.
# --------------------------------------------------------------------------


def test_preview_is_bounded_and_says_so() -> None:
    preview = _preview(CORRECT_PREDICATE, list(RULEBOOK_IDS))
    assert preview is not None
    assert preview.total == 200
    assert len(preview.rows) == PREDICATE_PREVIEW_ROW_LIMIT
    assert preview.truncated is True
    assert f"showing the first {PREDICATE_PREVIEW_ROW_LIMIT} of 200" in preview.summary


def test_no_sample_items_means_no_table_rather_than_an_empty_one() -> None:
    assert _preview(CORRECT_PREDICATE, []) is None


# --------------------------------------------------------------------------
# 3. The other three predicate surfaces get the same one evaluation.
# --------------------------------------------------------------------------


def test_assert_predicate_preview_reports_a_single_verdict() -> None:
    preview = _evaluate_predicate(
        "inputs['kept'] == 0", kind="assert", items=None, payload={"kept": 14}, where="data.assert"
    )
    assert preview.total == 1
    assert preview.rows[0].verdict == "failed"
    assert preview.rows[0].result is False
    assert "passed 0, failed 1" in preview.summary


def test_conditional_edge_preview_rides_the_edge_report() -> None:
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "src",
                    "type": "data",
                    "position": {"x": 0.0, "y": 0.0},
                    "data": {
                        "spec_type": "data.transform",
                        "label": "Count the citations",
                        "config": {"expression": "{'kept': 14}"},
                    },
                },
                {
                    "id": "stop",
                    "type": "data",
                    "position": {"x": 200.0, "y": 0.0},
                    "data": {
                        "spec_type": "data.transform",
                        "label": "Stop the run",
                        "config": {"expression": "{'stopped': True}"},
                    },
                },
            ],
            "edges": [
                {
                    "id": "e1",
                    "source": "src",
                    "target": "stop",
                    "data": {"kind": "conditional", "condition": "inputs['kept'] == 0"},
                }
            ],
        }
    )
    registry = _registry()
    graph = compile_graph(definition, registry=registry)
    report = dry_run(
        graph,
        inputs={},
        samples={"src": DryRunSample(value={"kept": 14}, slot="last_live_output")},
        registry=registry,
    )
    preview = report.edges["e1"].predicate_preview
    assert preview is not None
    assert preview.kind == "edge"
    assert preview.expression == "inputs['kept'] == 0"
    assert preview.rows[0].verdict == "failed"
    assert "'kept': 14" in preview.rows[0].item


# --------------------------------------------------------------------------
# 4. THE CLASS BEHIND THE CLASS (found 2026-09-12 building this affordance).
#
# W58's constant-predicate warning read the predicate off `node.config` as a
# DICT. On a COMPILED graph — every real caller — `CompiledNode.config` is the
# validated pydantic model, so the read found nothing and the warning had never
# once fired outside its own unit test, which hand-fed an uncompiled NodeDef.
# These assertions go through the REAL compiled graph and the REAL report, so
# the warning can never again be green while being inert.
# --------------------------------------------------------------------------


def test_the_constant_warning_reaches_the_real_report_from_a_compiled_graph() -> None:
    registry = _registry()
    graph = compile_graph(_filter_definition(V43_AS_EVALUATED, list(CITED_IDS)), registry=registry)
    report = dry_run(graph, inputs={}, samples={}, registry=registry)
    node = report.nodes["check_case_ids"]
    assert any("returned the same value for every one of the 14" in d for d in node.diagnostics)
    assert any(
        "check_case_ids" in w and "kept all of them" in w for w in report.warnings
    ), report.warnings
