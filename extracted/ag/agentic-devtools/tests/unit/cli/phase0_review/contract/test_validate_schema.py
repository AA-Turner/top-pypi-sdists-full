"""Tests for contract.validate_schema."""

import json

from agentic_devtools.cli.phase0_review.contract import load_contract, validate_schema


def test_validate_schema_accepts_valid_contract(make_review_case):
    payload_path, _ = make_review_case()
    data = load_contract(payload_path).data
    assert data is not None
    assert validate_schema(data) == []


def test_validate_schema_accepts_offsetless_iso8601_timestamp(make_review_case):
    """FR-009a: an offset-less extended-format ISO 8601 timestamp is valid."""
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    data["source"]["created_at"] = "2026-08-21T10:00:00"
    data["source"]["updated_at"] = "2026-08-21T10:00:00.5"
    findings = validate_schema(data)
    text = "\n".join(item.text for item in findings)
    assert "created_at" not in text
    assert "updated_at" not in text


def test_validate_schema_reports_exhaustive_shape_and_value_errors(make_review_case):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    source = data["source"]
    data["unknown"] = True
    data["schema_version"] = "wrong"
    source["provider"] = ""
    source["title"] = "x" * 1025
    source["body"] = "é" * 60000
    source["url"] = "relative"
    source["created_at"] = "not-a-date"
    source["updated_at"] = "2026-99-99T00:00:00Z"
    source["type"] = "Feature Name"
    source["labels"] = ["", 1]
    source["constraints"] = ["x" * 501]
    source["truncated"] = True
    source["original_size"] = 2
    source["properties"] = {
        "title": "collision",
        "x" * 129: ["", None, {}, [], float("inf")],
        "too_long": "x" * 1025,
    }
    data["issue_md"]["extra"] = 1
    data["issue_md"]["path"] = "wrong.md"
    data["template"]["extra"] = 1
    findings = validate_schema(data)
    text = "\n".join(item.text for item in findings)
    assert "unknown top-level member" in text
    assert "schema_version" in text
    assert "non-empty" in text
    assert "normalized slug" in text
    assert "name collision" in text
    assert "source.original_size" in text
    assert len(findings) >= 20


def test_validate_schema_handles_wrong_container_types_and_markdown_url(make_review_case):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    data["source"] = []
    data["issue_md"] = None
    data["template"] = "bad"
    assert len(validate_schema(data)) >= 3

    data = json.loads(payload_path.read_text())
    data["source"]["provider"] = "markdown"
    data["source"]["url"] = "https://example.test/x"
    assert any("repository-relative" in item.text for item in validate_schema(data))


def test_validate_schema_covers_collection_and_optional_bounds(make_review_case):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    source = data["source"]
    source.update(
        {
            "priority": None,
            "milestone": 1,
            "assignees": "wrong",
            "labels": ["x"] * 51,
            "truncated": "yes",
            "original_size": True,
            "properties": "wrong",
        }
    )
    text = "\n".join(item.text for item in validate_schema(data))
    assert "source.priority is a string" in text
    assert "source.assignees is an array" in text
    assert "total collection item count is at most 50" in text
    assert "source.truncated is a boolean" in text
    assert "source.properties is an object" in text


def test_validate_schema_covers_property_array_limits_and_timestamp_calendar(make_review_case):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    source = data["source"]
    source["created_at"] = "2026-02-31T10:00:00Z"
    source["unknown_source_member"] = "x"
    source["properties"] = {f"k{i}": i for i in range(51)}
    source["properties"]["array"] = ["x" * 501] * 49 + [1.5, int("9" * 501)]
    source["properties"]["unsupported"] = ("tuple",)
    source["properties"]["infinite"] = float("inf")
    findings = validate_schema(data)
    text = "\n".join(item.text for item in findings)
    assert "at most 50 entries" in text
    assert "has at most 50 members" in text
    assert "at most 500 characters" in text
    assert "supported scalar" in text
    assert "finite number" in text
    assert "valid timestamp" in text
    assert "unknown source member" in text


def test_validate_schema_covers_missing_members_and_path_types(make_review_case):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    del data["schema_version"]
    data["issue_md"]["path"] = None
    del data["template"]["selected_path"]
    data["template"]["structure_snapshot_path"] = None
    text = "\n".join(item.text for item in validate_schema(data))
    assert "required member 'schema_version'" in text
    assert "issue_md.path is a string" in text
    assert "required member template.selected_path" in text
    assert "template.structure_snapshot_path is a string" in text

    data = json.loads(payload_path.read_text())
    del data["issue_md"]["path"]
    assert any("required member issue_md.path" in item.text for item in validate_schema(data))


def test_validate_schema_accepts_markdown_relative_url_and_absent_properties(make_review_case):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    source = data["source"]
    source["provider"] = "markdown"
    source["url"] = "sources/42.md"
    del source["properties"]
    assert validate_schema(data) == []


def test_validate_schema_covers_each_truncation_consistency_branch(make_review_case):
    payload_path, _ = make_review_case()
    data = json.loads(payload_path.read_text())
    data["source"]["original_size"] = 5
    assert any("equals source.body" in item.text for item in validate_schema(data))

    data["source"]["truncated"] = True
    data["source"]["original_size"] = 102401
    assert validate_schema(data) == []
