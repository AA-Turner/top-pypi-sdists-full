"""Tests for `generate_inventory` (v0.1.164 / #369).

RFC-0017 names "consolidated resource inventory being validated" as
one of the 5 required items per KSI. Pin the shape so when RFC-0017
finalizes (likely Q3 2026) the diff is intentional.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from efterlev.primitives.generate import (
    INVENTORY_SCHEMA_VERSION,
    GenerateInventoryInput,
    generate_inventory,
)


def _ev(
    resource_type: str,
    resource_name: str,
    *,
    detector_id: str = "aws.encryption_s3_at_rest",
    ksis: list[str] | None = None,
    controls: list[str] | None = None,
    boundary_state: str = "boundary_undeclared",
    source_file: str = "main.tf",
    line_start: int = 10,
    line_end: int = 15,
    import_source: str | None = None,
    extra_content: dict | None = None,
) -> dict:
    """Build a payload matching what `store.iter_evidence()` returns."""
    content = {
        "resource_type": resource_type,
        "resource_name": resource_name,
    }
    if import_source is not None:
        content["import_source"] = import_source
    if extra_content:
        content.update(extra_content)
    return {
        "detector_id": detector_id,
        "evidence_id": "sha256:" + "a" * 64,
        "ksis_evidenced": ksis or [],
        "controls_evidenced": controls or [],
        "boundary_state": boundary_state,
        "source_ref": {
            "file": source_file,
            "line_start": line_start,
            "line_end": line_end,
            "commit": None,
        },
        "content": content,
    }


def _inp(payloads: list[dict], *, output_format: str = "json") -> GenerateInventoryInput:
    return GenerateInventoryInput(
        evidence_payloads=payloads,
        output_format=output_format,  # type: ignore[arg-type]
        generated_at=datetime(2026, 5, 19, 12, 0, 0, tzinfo=UTC),
    )


# --- Aggregation ---------------------------------------------------------


def test_one_evidence_record_produces_one_entry() -> None:
    result = generate_inventory(_inp([_ev("aws_s3_bucket", "audit")]))
    assert result.entry_count == 1
    e = result.entries[0]
    assert e.resource_id == "aws_s3_bucket:audit"
    assert e.resource_type == "aws_s3_bucket"
    assert e.resource_name == "audit"
    assert e.evidence_count == 1


def test_multiple_evidence_for_same_resource_collapses_into_one_entry() -> None:
    """A bucket might be evidenced by 3 detectors (encryption, public-
    access-block, versioning). One inventory entry; evidence_count = 3."""
    result = generate_inventory(
        _inp(
            [
                _ev(
                    "aws_s3_bucket",
                    "audit",
                    detector_id="aws.encryption_s3_at_rest",
                    ksis=["KSI-SVC-VRI"],
                    controls=["sc-28"],
                ),
                _ev(
                    "aws_s3_bucket",
                    "audit",
                    detector_id="aws.s3_public_access_block",
                    ksis=["KSI-CNA-EIS"],
                    controls=["ac-3"],
                    line_start=20,
                    line_end=25,
                ),
                _ev(
                    "aws_s3_bucket",
                    "audit",
                    detector_id="aws.backup_s3_versioning",
                    ksis=["KSI-RPL-ABO"],
                    controls=["cp-9"],
                    line_start=30,
                    line_end=35,
                ),
            ]
        )
    )
    assert result.entry_count == 1
    e = result.entries[0]
    assert e.evidence_count == 3
    # KSI + control coverage aggregates across detectors.
    assert e.ksi_coverage == ["KSI-CNA-EIS", "KSI-RPL-ABO", "KSI-SVC-VRI"]
    assert e.controls_coverage == ["ac-3", "cp-9", "sc-28"]
    # Source files aggregated, stable order.
    assert len(e.source_files) == 3


def test_distinct_resources_produce_distinct_entries() -> None:
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit"),
                _ev("aws_s3_bucket", "user_uploads"),
                _ev("aws_kms_key", "app"),
            ]
        )
    )
    assert result.entry_count == 3
    ids = {e.resource_id for e in result.entries}
    assert ids == {
        "aws_s3_bucket:audit",
        "aws_s3_bucket:user_uploads",
        "aws_kms_key:app",
    }


# --- Determinism + ordering ----------------------------------------------


def test_entries_sorted_alphabetically_by_resource_id() -> None:
    """Deterministic output requires stable order."""
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "user_uploads"),
                _ev("aws_kms_key", "app"),
                _ev("aws_s3_bucket", "audit"),
            ]
        )
    )
    assert [e.resource_id for e in result.entries] == [
        "aws_kms_key:app",
        "aws_s3_bucket:audit",
        "aws_s3_bucket:user_uploads",
    ]


def test_same_input_produces_byte_identical_json() -> None:
    inp = _inp([_ev("aws_s3_bucket", "audit"), _ev("aws_kms_key", "app")])
    a = generate_inventory(inp)
    b = generate_inventory(inp)
    assert a.rendered == b.rendered


def test_same_input_produces_byte_identical_html() -> None:
    inp = _inp(
        [_ev("aws_s3_bucket", "audit"), _ev("aws_kms_key", "app")],
        output_format="html",
    )
    a = generate_inventory(inp)
    b = generate_inventory(inp)
    assert a.rendered == b.rendered


# --- Boundary precedence -------------------------------------------------


def test_boundary_precedence_in_boundary_wins() -> None:
    """If ANY evidence record marks the resource in_boundary, the entry
    shows in_boundary. (A real scenario: detector A is boundary-aware,
    detector B isn't — boundary-aware verdict wins.)"""
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit", boundary_state="boundary_undeclared"),
                _ev("aws_s3_bucket", "audit", boundary_state="in_boundary"),
                _ev("aws_s3_bucket", "audit", boundary_state="out_of_boundary"),
            ]
        )
    )
    assert result.entries[0].boundary_state == "in_boundary"


def test_boundary_precedence_out_of_boundary_over_undeclared() -> None:
    """When no record says in_boundary but at least one says out_of_boundary,
    that's the safer reading — surface the explicit exclusion."""
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit", boundary_state="boundary_undeclared"),
                _ev("aws_s3_bucket", "audit", boundary_state="out_of_boundary"),
            ]
        )
    )
    assert result.entries[0].boundary_state == "out_of_boundary"


# --- Skipped records -----------------------------------------------------


def test_evidence_without_resource_type_skipped_with_counter() -> None:
    """Primitive-wrapper records (`{"input":..., "output":...}`) don't
    have resource_type — skip them, count the skip so callers detect
    detector-evidence-shape drift."""
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit"),
                # No resource_type in content:
                {"detector_id": "x", "content": {"input": "y"}, "source_ref": {"file": "x"}},
            ]
        )
    )
    assert result.entry_count == 1
    assert result.skipped_no_resource == 1


def test_evidence_with_missing_content_skipped() -> None:
    result = generate_inventory(_inp([{"detector_id": "x"}]))
    assert result.entry_count == 0
    assert result.skipped_no_resource == 1


def test_manifest_evidence_skipped_as_manifest_not_drift() -> None:
    """v0.1.176 / #383: manifest-sourced evidence (detector_id='manifest')
    legitimately has no resource_type — it's a procedural attestation, not a
    cloud resource. It must count toward `skipped_manifest` (expected), NOT
    `skipped_no_resource` (the detector-shape-drift signal that the CLI
    flags). Before the fix, manifests inflated the drift counter and the CLI
    falsely warned 'detector evidence shape drift?'."""
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit"),
                {
                    "detector_id": "manifest",
                    "evidence_id": "sha256:" + "b" * 64,
                    "ksis_evidenced": ["KSI-AFR-FSI"],
                    "content": {"attestation": "secure inbox operated"},
                    "source_ref": {"file": ".efterlev/manifests/afr-fsi.yml"},
                },
            ]
        )
    )
    assert result.entry_count == 1  # only the real resource
    assert result.skipped_manifest == 1
    assert result.skipped_no_resource == 0  # NOT counted as drift


# --- Import-source surfacing ---------------------------------------------


def test_import_source_surfaces_for_runtime_evidence() -> None:
    """Security Hub / Prowler imports carry `import_source` in content;
    surface so the inventory shows which records came from runtime
    feeds vs IaC scans."""
    result = generate_inventory(
        _inp(
            [
                _ev(
                    "aws_iam_user",
                    "admin",
                    import_source="aws.security_hub.asff",
                )
            ]
        )
    )
    assert result.entries[0].import_source == "aws.security_hub.asff"


def test_import_source_defaults_to_iac_detector() -> None:
    result = generate_inventory(_inp([_ev("aws_s3_bucket", "audit")]))
    assert result.entries[0].import_source == "iac_detector"


# --- JSON output shape ---------------------------------------------------


def test_json_output_includes_schema_version_and_rfc_reference() -> None:
    result = generate_inventory(_inp([_ev("aws_s3_bucket", "audit")]))
    doc = json.loads(result.rendered)
    assert doc["inventory_schema_version"] == INVENTORY_SCHEMA_VERSION
    assert "RFC-0017" in doc["rfc_reference"]
    assert doc["entry_count"] == 1
    assert doc["baseline_id"] == "fedramp-20x-moderate"


def test_json_output_round_trips_through_inventory_entry_model() -> None:
    """Output is a stable JSON shape that downstream callers can
    re-deserialize without surprise."""
    result = generate_inventory(
        _inp([_ev("aws_s3_bucket", "audit", ksis=["KSI-SVC-VRI"], controls=["sc-28"])])
    )
    doc = json.loads(result.rendered)
    e = doc["entries"][0]
    assert e["resource_id"] == "aws_s3_bucket:audit"
    assert e["ksi_coverage"] == ["KSI-SVC-VRI"]
    assert e["controls_coverage"] == ["sc-28"]
    assert len(e["source_files"]) == 1
    assert e["source_files"][0]["file"] == "main.tf"


# --- HTML output shape ---------------------------------------------------


def test_html_output_groups_by_resource_type() -> None:
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit"),
                _ev("aws_s3_bucket", "user_uploads"),
                _ev("aws_kms_key", "app"),
            ],
            output_format="html",
        )
    )
    html = result.rendered
    assert "aws_kms_key" in html
    assert "aws_s3_bucket" in html
    # Header + meta.
    assert "Consolidated Resource Inventory" in html
    assert INVENTORY_SCHEMA_VERSION in html
    # KSI coverage column present.
    assert "KSI coverage" in html


def test_html_output_empty_workspace_still_renders() -> None:
    """An empty inventory shouldn't crash — show header + zero count."""
    result = generate_inventory(_inp([], output_format="html"))
    assert result.entry_count == 0
    assert "0 resource(s)" in result.rendered
    assert "Consolidated Resource Inventory" in result.rendered


def test_html_escapes_resource_names() -> None:
    """Resource names trace back to Terraform / CFN / CDK identifiers;
    escape defensively to keep a malicious-upstream attack surface
    closed."""
    result = generate_inventory(
        _inp(
            [_ev("aws_s3_bucket", '<script>alert("xss")</script>')],
            output_format="html",
        )
    )
    assert "<script>" not in result.rendered
    assert "&lt;script&gt;" in result.rendered


# --- Format selection ----------------------------------------------------


def test_output_format_json_is_parseable_json() -> None:
    result = generate_inventory(_inp([_ev("aws_s3_bucket", "audit")]))
    assert result.output_format == "json"
    json.loads(result.rendered)


def test_output_format_html_is_not_json() -> None:
    result = generate_inventory(_inp([_ev("aws_s3_bucket", "audit")], output_format="html"))
    assert result.output_format == "html"
    with pytest.raises(json.JSONDecodeError):
        json.loads(result.rendered)


# --- Source-file aggregation -------------------------------------------


def test_source_files_deduplicated_across_repeated_evidence() -> None:
    """Same file:line range reported twice by two different detectors —
    one entry in source_files, not two."""
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit", detector_id="d1", line_start=10, line_end=15),
                _ev("aws_s3_bucket", "audit", detector_id="d2", line_start=10, line_end=15),
            ]
        )
    )
    assert len(result.entries[0].source_files) == 1


def test_source_files_sorted_by_file_then_line() -> None:
    """Stable order for diffing across runs."""
    result = generate_inventory(
        _inp(
            [
                _ev("aws_s3_bucket", "audit", source_file="z.tf", line_start=10),
                _ev("aws_s3_bucket", "audit", source_file="a.tf", line_start=50),
                _ev("aws_s3_bucket", "audit", source_file="a.tf", line_start=20),
            ]
        )
    )
    files = [(s.file, s.line_start) for s in result.entries[0].source_files]
    assert files == [("a.tf", 20), ("a.tf", 50), ("z.tf", 10)]
