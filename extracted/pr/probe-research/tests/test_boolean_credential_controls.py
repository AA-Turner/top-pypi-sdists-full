"""Credential-shaped status keys must not turn typed booleans into findings."""

import json

import pytest

from probe.sdk.redaction import default_scrub
from probe.sdk.secret_gate import inspect_bytes, redact_bytes


@pytest.mark.parametrize("key", ["synthetic_credentials_absent", "password", "api_key"])
@pytest.mark.parametrize("value", [True, False])
def test_typed_boolean_status_preserved(key, value):
    payload = {"nested": {key: value}}
    assert default_scrub(payload) == payload


@pytest.mark.parametrize("value", [True, False])
def test_serialized_boolean_report_is_unchanged_and_uploadable(value):
    raw = json.dumps({"nested": {"synthetic_credentials_absent": value}}, indent=2)
    assert default_scrub(raw) == raw
    inspect_bytes(raw.encode())


@pytest.mark.parametrize("value", ["true", "false", "synthetic-credential", 123456, 12.34])
def test_sensitive_strings_and_numbers_still_redact_and_record(value):
    payload = {"synthetic_credentials_absent": value}
    assert default_scrub(payload) == {"synthetic_credentials_absent": "<redacted>"}
    # Recorded, not refused: the key-name tier is a judgement about a FIELD
    # NAME, so it never rewrites a researcher's bytes -- but it is still seen.
    assert inspect_bytes(json.dumps(payload).encode()).has_findings


def test_untyped_boolean_assignment_is_not_exempt():
    assert default_scrub("password=true") != "password=true"
    assert inspect_bytes(b"password=true").has_findings


def test_vendor_credential_in_dictionary_key_is_still_removed():
    key = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
    scrubbed = default_scrub({key: True})
    assert key not in json.dumps(scrubbed)
    assert list(scrubbed.values()) == [True]
    # A vendor shape is certain, so this one is REWRITTEN, not merely recorded.
    clean, result = redact_bytes(json.dumps({key: True}).encode())
    assert "github-token" in result.rules
    assert key.encode() not in clean
