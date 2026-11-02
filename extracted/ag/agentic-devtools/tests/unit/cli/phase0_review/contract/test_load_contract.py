"""Tests for contract.load_contract."""

from agentic_devtools.cli.phase0_review.config import MAX_PAYLOAD_BYTES
from agentic_devtools.cli.phase0_review.contract import load_contract


def test_load_contract_reports_missing_invalid_duplicate_and_oversized(tmp_path):
    missing = load_contract(tmp_path / "missing.json")
    assert "Missing input" in missing.findings[0].text

    invalid = tmp_path / "invalid.json"
    invalid.write_bytes(b"\xff")
    assert "Malformed input" in load_contract(invalid).findings[0].text

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"source":{"x":1,"x":2,"x":3,"x.y":4,"x.y":5},"template":{"x":4,"x":5}}')
    loaded = load_contract(duplicate)
    assert loaded.data == {"source": {"x": 3, "x.y": 5}, "template": {"x": 5}}
    duplicate_text = "\n".join(item.text for item in loaded.findings)
    assert duplicate_text.count("duplicate member $.source.x") == 2
    assert 'duplicate member $.source[\\"x.y\\"]' in duplicate_text
    assert "duplicate member $.template.x" in duplicate_text

    oversized = tmp_path / "oversized.json"
    oversized.write_bytes(b" " * (MAX_PAYLOAD_BYTES + 1))
    assert str(MAX_PAYLOAD_BYTES) in load_contract(oversized).findings[0].text


def test_load_contract_rejects_non_object_depth_and_constants(tmp_path):
    non_object = tmp_path / "list.json"
    non_object.write_text("[]")
    assert load_contract(non_object).data is None

    deep = tmp_path / "deep.json"
    deep.write_text('{"a":[[[[[[[[[[[]]]]]]]]]]]}')
    assert any("nesting depth" in item.text for item in load_contract(deep).findings)

    constant = tmp_path / "constant.json"
    constant.write_text('{"x":NaN}')
    assert load_contract(constant).data is None


def test_load_contract_uses_caller_label_for_missing_and_malformed_input(tmp_path):
    missing = load_contract(tmp_path / "missing.json", label="integrity metadata")
    assert missing.findings[0].text.startswith('Missing input: "integrity metadata": "unreadable:')

    invalid = tmp_path / "invalid.json"
    invalid.write_bytes(b"\xff")
    assert (
        load_contract(invalid, label="integrity metadata")
        .findings[0]
        .text.startswith('Malformed input: "integrity metadata is valid UTF-8 JSON":')
    )
