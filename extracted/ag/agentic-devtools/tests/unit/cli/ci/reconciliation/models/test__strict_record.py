"""Strict nested decoding rejects coercion, omitted fields and duplicate lineage."""

from dataclasses import asdict

import pytest

from agentic_devtools.cli.ci.reconciliation.models import Evidence, RepairAttempt, _strict_record


def test_round_trip_preserves_enums_optional_and_tuples(foundation):
    f = foundation()
    attempt = f.state.attempts["attempt-0"]
    raw = asdict(attempt)
    raw["status"] = attempt.status.value
    raw["kind"] = attempt.kind.value
    assert _strict_record(RepairAttempt, raw) == attempt
    proof = f.proof(related_id="related")
    raw = asdict(proof)
    raw["inventory"] = list(proof.inventory)
    raw["observed_at"] = proof.observed_at.isoformat()
    raw["valid_until"] = proof.valid_until.isoformat()
    assert _strict_record(Evidence, raw) == proof


@pytest.mark.parametrize(
    "field,value",
    [
        ("inventory", "not-a-list"),
        ("inventory", ["duplicate", "duplicate"]),
        ("pr_number", True),
        ("complete", 1),
        ("observed_at", None),
    ],
)
def test_invalid_field_types(foundation, field, value):
    raw = asdict(foundation().proof())
    raw[field] = value
    with pytest.raises(ValueError):
        _strict_record(Evidence, raw)


def test_requires_complete_fields_and_string_enum(foundation):
    f = foundation()
    with pytest.raises(ValueError, match="exactly"):
        _strict_record(Evidence, {})
    raw = asdict(f.state.attempts["attempt-0"])
    raw["status"] = 1
    with pytest.raises(ValueError, match="enum string"):
        _strict_record(RepairAttempt, raw)
