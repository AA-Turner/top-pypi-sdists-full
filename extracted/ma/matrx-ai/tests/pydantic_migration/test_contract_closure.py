"""The contract closure is a measurement, so it has to be falsifiable.

agent-engine-extraction Phase 1b.2. The plan carried "149 sibling dataclasses"
as an estimate. The closure walk says the real number is 33 — the transitive set
of dataclasses reachable from UnifiedConfig / UnifiedMessage / UnifiedResponse.
Only those cross the language boundary, so only those need pydantic twins
(D2/D8: model_json_schema() is what generates the TypeScript).

A number that shrinks the work by ~78% is exactly the kind of number that must be provably
wrong when it IS wrong, which is what the self-test is for.

🚨 IT WAS WRONG ONCE ALREADY. The first published figure was 26. The annotation walk
trusts annotations, and `UnifiedContent` omitted seven of the fourteen classes in
STRUCTURED_INPUT_TYPE_MAP — so `reconstruct_content` returned types outside its own
declared return type and the walk never reached them. A wrong union does not look like a
blind spot; it looks like a complete annotation. That is why `registry_escapees` exists as
a SECOND, independent layer.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import contract_closure  # noqa: E402


def test_the_walk_can_detect_a_planted_contract_type():
    """The falsifiability rule. A closure tool that has never been shown to fail
    is not evidence — see PRINCIPLES.md and the fallback law's --self-test."""
    assert contract_closure.self_test() == 0


def test_every_annotation_in_the_contract_resolves():
    """An unwalkable edge is a HOLE, and a closure with unreported holes reads as
    'we measured it' when we did not."""
    _, unresolved, _ = contract_closure.walk()
    assert unresolved == [], f"the closure is incomplete: {unresolved}"


def test_the_closure_is_the_number_the_plan_rests_on():
    closure, _, _ = contract_closure.walk()
    dataclasses_in_contract = [
        c for c in closure if contract_closure.classify(c) == "DATACLASS — needs a twin"
    ]
    # Not a golden-file assertion for its own sake: this number is what PLAN.md
    # and the phase estimate rest on. If it moves, the plan moves with it —
    # a new contract dataclass is a new twin nobody scheduled.
    assert len(dataclasses_in_contract) == 33, (
        "the contract closure changed; update PLAN.md in the same commit. Now: "
        + ", ".join(sorted(f"{c.__module__}.{c.__name__}" for c in dataclasses_in_contract))
    )


def test_the_three_roots_are_in_their_own_closure():
    closure, _, _ = contract_closure.walk()
    names = {c.__name__ for c in closure}
    assert {"UnifiedConfig", "UnifiedResponse", "UnifiedMessage"} <= names


def test_erased_edges_are_reported_rather_than_silently_narrowing_the_count():
    """Any-typed fields are edges the walk cannot see through, so 26 is a LOWER
    bound. The tool must say so; a count that hides its own blind spot is the
    'validator that cannot fail' antipattern."""
    _, _, erased = contract_closure.walk()
    assert erased, "the tool stopped reporting erased edges — it now overstates its certainty"
    # Each one is also an `any` in the generated TypeScript.
    assert any("ToolCallContent.arguments" in e for e in erased)


def test_the_registry_layer_catches_what_the_annotation_walk_cannot():
    """The second layer, and proof it can fail.

    Layer one follows annotations. When an annotation is WRONG rather than
    absent — the UnifiedContent union omitting seven structured-input classes —
    layer one reports a complete closure and is simply wrong. Layer two sweeps
    registries instead, so it catches exactly that case.
    """
    from matrx_ai.config.structured_input_config import WorkbookInputContent

    closure, _, _ = contract_closure.walk()
    assert contract_closure.registry_escapees(closure) == [], (
        "a registry can produce a dataclass no annotation reaches — the closure is an undercount"
    )

    # Falsification: recreate the pre-fix world and require the layer to fire.
    crippled = {k: v for k, v in closure.items() if k is not WorkbookInputContent}
    found = contract_closure.registry_escapees(crippled)
    assert found, "the registry layer cannot fail, so its silence means nothing"
    assert all("WorkbookInputContent" in f for f in found)
