"""Tests for contract.validate_integrity."""

import json

from agentic_devtools.cli.phase0_review.contract import validate_integrity


def test_validate_integrity_accepts_valid_metadata(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    artifacts = {
        "template.selected_path": (tmp_path / "template.md").read_bytes(),
        "template.structure_snapshot_path": (tmp_path / "structure_snapshot.md").read_bytes(),
    }
    assert validate_integrity(integrity, payload.read_bytes(), artifacts) == []


def test_validate_integrity_reports_missing_invalid_schema_and_mismatches(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    artifacts = {
        "template.selected_path": b"wrong",
        "template.structure_snapshot_path": b"wrong",
    }
    metadata = json.loads(integrity.read_text())
    metadata["payload_sha256"] = "A" * 64
    del metadata["snapshot_sha256"]
    metadata["unknown"] = "x"
    integrity.write_text(json.dumps(metadata))
    findings = validate_integrity(integrity, payload.read_bytes(), artifacts)
    text = "\n".join(item.text for item in findings)
    assert "lowercase 64-hex" in text
    assert "member is missing" in text
    assert "unknown integrity member" in text

    integrity.write_text("{")
    malformed = validate_integrity(integrity, b"", [])[0].text
    assert malformed.startswith('Malformed input: "integrity metadata is valid UTF-8 JSON":')
    assert 'Malformed input: "integrity metadata": "Malformed input:' not in malformed
    assert "Missing input" in validate_integrity(tmp_path / "missing.json", b"", [])[0].text


def test_validate_integrity_reports_duplicate_members_and_each_digest_mismatch(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    metadata = json.loads(integrity.read_text())
    duplicate = (
        '{"payload_sha256":"'
        + metadata["payload_sha256"]
        + '","payload_sha256":"'
        + metadata["payload_sha256"]
        + '","selected_template_sha256":"'
        + metadata["selected_template_sha256"]
        + '","snapshot_sha256":"'
        + metadata["snapshot_sha256"]
        + '"}'
    )
    integrity.write_text(duplicate)
    artifacts = {
        "template.selected_path": b"wrong",
        "template.structure_snapshot_path": b"wrong",
    }
    findings = validate_integrity(integrity, b"wrong", artifacts)
    text = "\n".join(item.text for item in findings)
    assert 'Malformed input: "integrity metadata has unique JSON member names"' in text
    assert text.count("matches raw bytes") == 3
