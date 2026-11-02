"""Strict decoder rejects malformed envelopes and ambiguous JSON."""

import base64
import json

import pytest

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import (
    ReconciliationValidationError,
    decode_reconciliation_review_body,
)


@pytest.mark.parametrize(
    "transform",
    [
        lambda body: "",
        lambda body: body + "\n",
        lambda body: "\n" + body,
        lambda body: body + body,
        lambda body: body.replace("\n", "\r\n"),
        lambda body: body.replace(":v1 ", ":v2 "),
        lambda body: body.replace("sha256=", "sha256=Z"),
        lambda body: body[:-1],
        lambda body: body.splitlines()[1],
    ],
)
def test_malformed_metadata(payload, envelope, transform):
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(transform(envelope(payload)))
    assert error.value.reason == "malformed_metadata"


@pytest.mark.parametrize("encoded", ["", "a", "abc=", "ab+c", "ab/c", "abc ", "é", "ab"])
def test_invalid_base64url(payload, envelope, encoded):
    lines = envelope(payload).splitlines()
    lines[1] = encoded
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body("\n".join(lines))
    assert error.value.reason == "invalid_base64url"


def test_digest_mismatch(payload, envelope):
    lines = envelope(payload).splitlines()
    lines[0] = "<!-- agdt-reconciliation:v1 sha256=" + "0" * 64 + " -->"
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body("\n".join(lines))
    assert error.value.reason == "payload_digest_mismatch"


@pytest.mark.parametrize("raw", [b"{", b"\xff", b'{"a":1,"a":2}', b'{"a":{"b":1,"b":2}}', b"NaN", b"Infinity"])
def test_invalid_json(envelope, raw):
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(envelope(None, raw=raw))
    assert error.value.reason == "invalid_json"


@pytest.mark.parametrize(
    "raw",
    [
        b'{"z":1, "a":2}',
        b'{"z":1,"a":2}',
        b'{"a": 2}',
        b'{"a":"\\u0061"}',
        '{"a":"é"}'.encode(),
        b'{"a":2}\n',
    ],
)
def test_noncanonical_json(envelope, raw):
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(envelope(None, raw=raw))
    assert error.value.reason == "noncanonical_payload"


@pytest.mark.parametrize("target", ["attestation", "file", "criterion"])
@pytest.mark.parametrize("operation", ["missing", "unknown"])
def test_json_record_keys(payload, envelope, target, operation):
    record = {
        "attestation": payload,
        "file": payload["file_verdicts"][0],
        "criterion": payload["criterion_verdicts"][0],
    }[target]
    if operation == "missing":
        record.pop(next(iter(record)))
    else:
        record["unexpected"] = True
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(envelope(payload))
    assert error.value.reason == ("missing_field" if operation == "missing" else "unknown_field")


@pytest.mark.parametrize("value", [[], None, 1, "text"])
def test_wrong_json_top_record(envelope, value):
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(envelope(value))
    assert error.value.reason == "invalid_record_type"


@pytest.mark.parametrize("field", ["changed_files", "file_verdicts", "criterion_verdicts"])
@pytest.mark.parametrize("value", [None, {}, "abc"])
def test_wrong_json_collection(payload, envelope, field, value):
    payload[field] = value
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(envelope(payload))
    assert error.value.reason == "invalid_collection_type"


@pytest.mark.parametrize("field", ["file_verdicts", "criterion_verdicts"])
def test_wrong_json_nested_record(payload, envelope, field):
    payload[field] = [1]
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(envelope(payload))
    assert error.value.reason == "invalid_record_type"


def test_decoded_values_are_validated(payload, envelope):
    payload["schema_version"] = False
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(envelope(payload))
    assert error.value.reason == "unsupported_schema_version"


def test_decode_wrong_body_type():
    with pytest.raises(ReconciliationValidationError) as error:
        decode_reconciliation_review_body(None)
    assert error.value.reason == "malformed_metadata"


def test_envelope_digest_is_over_exact_json_bytes(payload, envelope):
    body = envelope(payload)
    decoded = base64.urlsafe_b64decode(body.splitlines()[1] + "==")
    assert json.loads(decoded) == payload
    assert decode_reconciliation_review_body(body).repository == payload["repository"]
