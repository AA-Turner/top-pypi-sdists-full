"""Canonical review encoding and exact envelope size limits."""

from dataclasses import asdict, replace

import pytest

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import (
    ReconciliationValidationError,
    decode_reconciliation_review_body,
    encode_reconciliation_review_body,
)


def test_deterministic_exact_encoding(attestation, envelope):
    body = encode_reconciliation_review_body(attestation)
    assert body == envelope(asdict(attestation))
    assert body == encode_reconciliation_review_body(attestation)
    assert decode_reconciliation_review_body(body) == attestation
    assert len(body.splitlines()) == 3
    assert "=" not in body.splitlines()[1]


def test_escaped_unicode_roundtrip(attestation):
    record = replace(attestation.file_verdicts[0], behavior="Retains café ☃\nbehavior")
    value = replace(attestation, file_verdicts=(record, attestation.file_verdicts[1]))
    assert decode_reconciliation_review_body(encode_reconciliation_review_body(value)) == value


@pytest.mark.parametrize("length", [58000, 58001])
def test_exact_body_size(attestation, envelope, length):
    # Vary only one ASCII behavior; Base64 encodings can reach both adjacent sizes.
    for count in range(41000, 44000):
        record = replace(attestation.file_verdicts[0], behavior="x" * count)
        candidate = replace(attestation, file_verdicts=(record, attestation.file_verdicts[1]))
        body = envelope(asdict(candidate))
        if len(body) == length:
            break
    else:
        pytest.fail("Could not construct the exact envelope length")
    assert len(body) == length
    if length == 58000:
        assert encode_reconciliation_review_body(candidate) == body
        assert decode_reconciliation_review_body(body) == candidate
    else:
        # Size takes precedence even over a different invalid field or metadata.
        for value in (candidate, replace(candidate, schema_version=2)):
            with pytest.raises(ReconciliationValidationError) as error:
                encode_reconciliation_review_body(value)
            assert error.value.reason == "review_body_too_large"
        for value in (body, "!" * length):
            with pytest.raises(ReconciliationValidationError) as error:
                decode_reconciliation_review_body(value)
            assert error.value.reason == "review_body_too_large"


def test_encode_validates(attestation):
    with pytest.raises(ReconciliationValidationError) as error:
        encode_reconciliation_review_body(replace(attestation, repair_writer_login=""))
    assert error.value.reason == "invalid_login"


@pytest.mark.parametrize("value", [{}, None])
def test_encode_wrong_record(value):
    with pytest.raises(ReconciliationValidationError) as error:
        encode_reconciliation_review_body(value)
    assert error.value.reason == "invalid_record_type"


def test_encode_non_json_value_is_controlled(attestation):
    with pytest.raises(ReconciliationValidationError) as error:
        encode_reconciliation_review_body(replace(attestation, changed_files={"a.py"}))
    assert error.value.reason == "invalid_collection_type"


def test_serializer_failure_is_not_success(attestation, monkeypatch):
    from agentic_devtools.cli.ci.pipeline import conflict_reconciliation

    def fail_serialization(_value):
        raise TypeError("Cannot serialize")

    monkeypatch.setattr(conflict_reconciliation, "_canonical_json", fail_serialization)
    with pytest.raises(ReconciliationValidationError) as error:
        encode_reconciliation_review_body(attestation)
    assert error.value.reason == "invalid_record_type"
