"""Tests for decoding dispatch-state payloads."""

import json
from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.dispatch_state import DispatchIdentity, DispatchRecord
from agentic_devtools.cli.ci.dispatch_state_codec import decode_dispatch_state_payload

HEAD_SHA = "a" * 40
WORK_DIGEST = "b" * 64


def _legacy_record() -> tuple[str, dict[str, Any]]:
    record = DispatchRecord.new(DispatchIdentity("repo", 7, HEAD_SHA, 1))
    return record.identity.key, record.to_dict()


def _canonical_record(**overrides: object) -> tuple[str, dict[str, Any]]:
    record: dict[str, Any] = {
        "repo": "owner/repo",
        "pull_request_id": 7,
        "head_sha": HEAD_SHA,
        "review_id": 23,
        "work_digest": WORK_DIGEST,
        "ordinal": 4,
        "opaque": {"items": [1, {"flag": True}]},
    }
    record.update(overrides)
    key = (
        f"{record['repo']}:{record['pull_request_id']}:{record['head_sha']}:"
        f"{record['review_id']}:{record['work_digest']}:{record['ordinal']}"
    )
    return key, record


def test_decodes_flat_and_v1_payloads_as_legacy_only() -> None:
    key, record = _legacy_record()
    flat = decode_dispatch_state_payload(json.dumps({key: record}))
    v1 = decode_dispatch_state_payload(json.dumps({"version": 1, "records": {key: record}}))

    assert flat.version is None
    assert flat.records[key]["repo"] == "repo"
    assert flat.canonical_records == {}
    assert v1.version == 1
    assert v1.records == flat.records
    assert v1.canonical_records == {}


def test_decodes_v2_without_mixing_namespaces() -> None:
    legacy_key, legacy_record = _legacy_record()
    canonical_key, canonical_record = _canonical_record()

    envelope = decode_dispatch_state_payload(
        json.dumps(
            {
                "version": 2,
                "records": {legacy_key: legacy_record},
                "canonical_records": {canonical_key: canonical_record},
            }
        )
    )

    assert envelope.version == 2
    assert list(envelope.records) == [legacy_key]
    assert list(envelope.canonical_records) == [canonical_key]
    assert envelope.to_dict()["canonical_records"][canonical_key]["opaque"] == canonical_record["opaque"]


@pytest.mark.parametrize("version", [None, 1, 2])
def test_preserves_legacy_record_extension_metadata(version: int | None) -> None:
    legacy_key, legacy_record = _legacy_record()
    legacy_record["metadata"] = {"audit_reference": "preserve-me"}
    payload: dict[str, Any] = {"records": {legacy_key: legacy_record}}
    if version is not None:
        payload["version"] = version
    if version == 2:
        payload["canonical_records"] = {}
    if version is None:
        payload = {legacy_key: legacy_record}

    envelope = decode_dispatch_state_payload(json.dumps(payload))

    serialized = envelope.to_dict()
    serialized_records = serialized["records"] if version is not None else serialized
    assert serialized_records == {legacy_key: legacy_record}


def test_rejects_non_text_and_nonstandard_json_constants() -> None:
    with pytest.raises(ValueError, match="text"):
        decode_dispatch_state_payload(cast(Any, None))
    with pytest.raises(ValueError, match="blank"):
        decode_dispatch_state_payload(" \n ")
    with pytest.raises(ValueError, match="invalid JSON constant"):
        decode_dispatch_state_payload('{"version": 2, "records": {}, "canonical_records": {"bad": NaN}}')


@pytest.mark.parametrize(
    "content",
    [
        "",
        "{",
        "[]",
        '{"version": true, "records": {}, "canonical_records": {}}',
        '{"version": 3, "records": {}, "canonical_records": {}}',
        '{"version": 2, "records": {}}',
        '{"version": 2, "records": {}, "canonical_records": {}, "extra": 1}',
        '{"version": 2, "records": [], "canonical_records": {}}',
        '{"version": 2, "records": {}, "canonical_records": []}',
        '{"version": 1, "records": {}, "canonical_records": {}}',
        '{"version": 1}',
        '{"records": {}}',
    ],
)
def test_rejects_invalid_envelopes(content: str) -> None:
    with pytest.raises(ValueError):
        decode_dispatch_state_payload(content)


def test_rejects_invalid_legacy_or_canonical_record_without_partial_result() -> None:
    legacy_key, legacy_record = _legacy_record()
    canonical_key, canonical_record = _canonical_record()
    invalid_canonical = {**canonical_record, "head_sha": "not-a-sha"}
    content = json.dumps(
        {
            "version": 2,
            "records": {legacy_key: legacy_record},
            "canonical_records": {canonical_key: canonical_record, "invalid": invalid_canonical},
        }
    )

    with pytest.raises(ValueError, match="canonical"):
        decode_dispatch_state_payload(content)

    invalid_legacy = {**legacy_record, "ordinal": 4}
    with pytest.raises(ValueError):
        decode_dispatch_state_payload(
            json.dumps(
                {
                    "version": 2,
                    "records": {legacy_key: invalid_legacy},
                    "canonical_records": {canonical_key: canonical_record},
                }
            )
        )


def test_rejects_identity_key_mismatches_in_both_namespaces() -> None:
    _, legacy_record = _legacy_record()
    canonical_key, canonical_record = _canonical_record()

    with pytest.raises(ValueError, match="key"):
        decode_dispatch_state_payload(json.dumps({"wrong": legacy_record}))

    with pytest.raises(ValueError, match="key"):
        decode_dispatch_state_payload(
            json.dumps(
                {
                    "version": 2,
                    "records": {},
                    "canonical_records": {"wrong": canonical_record, canonical_key: canonical_record},
                }
            )
        )


def test_rejects_non_object_canonical_records() -> None:
    with pytest.raises(ValueError, match="invalid canonical record"):
        decode_dispatch_state_payload(
            json.dumps({"version": 2, "records": {}, "canonical_records": {"bad": "not an object"}})
        )
