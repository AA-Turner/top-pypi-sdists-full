"""Tests for the detector-coverage signal (v0.1.221 / DECISIONS 2026-06-08).

A KSI with a registered IaC detector ("detector-covered") that produces zero
evidence must classify `not_implemented`, not `evidence_layer_inapplicable`.
The deterministic plumbing is what these tests lock:

  - `detector_covered_ksis()` unions the registry's KSIs.
  - `GapAgentInput.detector_covered_ksis` defaults empty (backward compat).
  - `_build_user_message` marks covered KSIs and emits the rule block only
    when a covered KSI is in the batch; empty set → byte-identical output.

The agent-behavior confirmation (covered + zero evidence → not_implemented on
a real model) is an eval-harness dispatch, not a unit test — these lock the
inputs the agent reasons over.
"""

from __future__ import annotations

from efterlev.agents import GapAgentInput, detector_covered_ksis
from efterlev.agents.gap import _build_user_message
from efterlev.models import Indicator


def _ind(ksi_id: str) -> Indicator:
    return Indicator(
        id=ksi_id,
        theme=ksi_id.split("-")[1],
        name=f"name-{ksi_id}",
        statement="...",
        controls=["sc-28"],
    )


def test_detector_covered_ksis_unions_registry() -> None:
    """The covered set is non-empty, all KSI-shaped, and includes the two
    detectors the 2026-06-07 validation found mis-classified (SVC-RUD lifecycle,
    RPL-TRC restore-testing both have registered detectors)."""
    covered = detector_covered_ksis()
    assert isinstance(covered, frozenset)
    assert len(covered) >= 30  # 37 at v0.1.221; floor guards a gross registry break
    assert all(k.startswith("KSI-") for k in covered)
    assert "KSI-SVC-RUD" in covered
    assert "KSI-RPL-TRC" in covered
    # A purely-procedural KSI with no IaC detector must NOT be covered.
    assert "KSI-AFR-FSI" not in covered


def test_gap_agent_input_covered_set_defaults_empty() -> None:
    """Default-empty keeps direct/unit-test invocation backward compatible —
    no markers, no rule block, byte-identical prompt."""
    gi = GapAgentInput(indicators=[_ind("KSI-RPL-TRC")], evidence=[])
    assert gi.detector_covered_ksis == frozenset()


def test_build_user_message_marks_covered_ksi_and_emits_rule() -> None:
    """A covered KSI in the batch gets the marker AND the rule block."""
    covered = frozenset({"KSI-RPL-TRC"})
    msg = _build_user_message(
        [_ind("KSI-RPL-TRC"), _ind("KSI-AFR-FSI")],
        [],
        [],
        nonce="abcd1234",
        covered_ksis=covered,
    )
    assert "KSI-RPL-TRC [IaC-detector-covered]" in msg
    # The uncovered KSI is NOT marked.
    assert "KSI-AFR-FSI [IaC-detector-covered]" not in msg
    assert "KSI-AFR-FSI —" in msg
    # The rule block tells the model zero-evidence-covered → not_implemented.
    assert "Detector-coverage rule" in msg
    assert "not_implemented" in msg


def test_build_user_message_empty_covered_is_byte_identical() -> None:
    """Empty covered set → no marker, no rule block (backward compat)."""
    inds = [_ind("KSI-RPL-TRC")]
    with_empty = _build_user_message(inds, [], [], nonce="abcd1234")
    explicit_empty = _build_user_message(inds, [], [], nonce="abcd1234", covered_ksis=frozenset())
    assert with_empty == explicit_empty
    assert "[IaC-detector-covered]" not in with_empty
    assert "Detector-coverage rule" not in with_empty


def test_build_user_message_no_rule_block_when_batch_has_no_covered_ksi() -> None:
    """A non-empty covered set whose members aren't in THIS batch emits no rule
    block — keeps it out of all-procedural batches."""
    covered = frozenset({"KSI-RPL-TRC"})  # not in the batch below
    msg = _build_user_message(
        [_ind("KSI-AFR-FSI"), _ind("KSI-CED-DRP")],
        [],
        [],
        nonce="abcd1234",
        covered_ksis=covered,
    )
    assert "Detector-coverage rule" not in msg
    assert "[IaC-detector-covered]" not in msg
