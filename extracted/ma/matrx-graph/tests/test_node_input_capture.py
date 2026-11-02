"""Per-step INPUT capture (contract C-30) — the half the platform never kept.

`workflow.node_outcome` always recorded what a node PRODUCED. What it was
GIVEN was computed, streamed once as a NodeStartedEvent, and dropped — so a
replay of one node had no starting point, the C-27 drill-down walk hit a wall at
the first workflow node, and a per-node reviewer could not be enrolled at all.

These pins are about the two distinctions that are easy to erase.
"""

from __future__ import annotations

from matrx_graph.checkpoint.protocol import NodeOutcome


def _outcome(**kwargs) -> NodeOutcome:
    base = dict(run_id="r", step=1, node_id="n", attempt=1, output={})
    base.update(kwargs)
    return NodeOutcome(**base)


def test_inputs_default_to_none_not_empty():
    """🚨 None and {} are DIFFERENT FACTS. None = "we never recorded the
    arguments" (a pre-C-30 row, or an outcome with no executor invocation such
    as user_skip / user_manual). {} = "the node was called with no arguments"
    — which is the correct, ordinary state of an entry node.

    Defaulting to {} would make every un-captured occurrence claim it was
    called with nothing, and a replay built on that would faithfully reproduce
    a call that never happened.
    """
    assert _outcome().inputs is None
    assert _outcome(inputs={}).inputs == {}


def test_an_entry_node_records_empty_inputs_and_that_is_a_recording():
    outcome = _outcome(inputs={})
    assert outcome.inputs is not None
    assert outcome.inputs == {}


def test_inputs_and_output_ride_the_same_occurrence():
    """Both halves share one correlation key. A sibling table would let them
    disagree about which attempt they describe."""
    outcome = _outcome(
        inputs={"topic": "x"}, output={"result": "y"}, dispatch_id="d1", item_index=3, attempt=2
    )
    assert outcome.inputs == {"topic": "x"}
    assert outcome.output == {"result": "y"}
    assert (outcome.dispatch_id, outcome.item_index, outcome.attempt) == ("d1", 3, 2)


def test_input_kind_has_no_ok_twin():
    """The input contract is FATAL at the binding: a violating input parks the
    run BEFORE the node executes, so a stored input is by construction one that
    passed. An `input_kind_ok` column could only ever be true, and a column that
    can only be true is a lie waiting to happen."""
    assert not hasattr(
        NodeOutcome(run_id="r", step=1, node_id="n", attempt=1, output={}), "input_kind_ok"
    )
    assert _outcome(input_kind="doc").input_kind == "doc"
    assert _outcome().input_kind is None
