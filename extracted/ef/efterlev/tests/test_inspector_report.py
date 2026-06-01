"""Tests for `generate_inspector_report` — 3PAO single-page HTML assembly.

The primitive composes three inputs (FRMR catalog entries, optional
attestation artifact, RFC-0017 gate report) into a per-KSI HTML view.
Tests cover the assembly logic (does each row carry the right data),
HTML shape (does it parse, do failing rows render their failure block),
and graceful-degradation (does it work when the attestation is missing).
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from efterlev.models.attestation_artifact import (
    AttestationArtifact,
    AttestationArtifactIndicator,
    AttestationArtifactInfo,
    AttestationArtifactProvenance,
    AttestationArtifactTheme,
)
from efterlev.models.attestation_draft import AttestationCitation
from efterlev.primitives.generate.generate_inspector_report import (
    GenerateInspectorReportInput,
    generate_inspector_report,
)
from efterlev.primitives.readiness import compute_rfc_0017_gate


def _gate(
    workspace: Path,
    *,
    ksis: list[str],
    machine: str = "every PR",
    human: str = "quarterly",
):
    return compute_rfc_0017_gate(
        workspace,
        baseline_ksi_ids=ksis,
        machine_validation_cadence=machine,
        human_validation_cadence=human,
    )


def _catalog(
    ksi_id: str,
    *,
    theme: str = "CNA",
    statement: str = "test statement",
    controls: list[str] | None = None,
) -> dict[str, object]:
    return {
        "ksi_id": ksi_id,
        "theme": theme,
        "statement": statement,
        "controls_mapped": controls or [],
    }


def _attestation(indicators_by_theme: dict[str, dict[str, AttestationArtifactIndicator]]):
    return AttestationArtifact(
        info=AttestationArtifactInfo(
            tool_version="0.1.168-test",
            baseline="fedramp-20x-moderate",
            frmr_version="0.9.43-beta",
            frmr_last_updated="2026-04-19",
            generated_at=datetime.now(UTC),
        ),
        KSI={
            theme: AttestationArtifactTheme(indicators=indicators)
            for theme, indicators in indicators_by_theme.items()
        },
        provenance=AttestationArtifactProvenance(),
    )


# --- Assembly: row shape -----------------------------------------------


def test_row_carries_catalog_fields(tmp_path: Path) -> None:
    """Every catalog entry produces a row with statement + controls + theme."""
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[
                _catalog(
                    "KSI-CNA-RNT", statement="Resource not trusted", controls=["sc-7", "ac-4"]
                ),
            ],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-RNT"]),
        )
    )
    [row] = result.rows
    assert row.ksi_id == "KSI-CNA-RNT"
    assert row.theme == "CNA"
    assert row.statement == "Resource not trusted"
    assert row.controls_mapped == ["sc-7", "ac-4"]


def test_store_status_drives_pill_without_attestation(tmp_path: Path) -> None:
    """v0.1.173 fix: a KSI with a store claim but NO attestation (e.g. an
    inherited claim from `scope apply`, or `agent gap` without `document`)
    must show that status — not 'unclassified' — so the pill matches the
    gate dots in the same row."""
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-CNA-RVP")],
            attestation=None,
            store_statuses={"KSI-CNA-RVP": "implemented"},
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-RVP"]),
        )
    )
    [row] = result.rows
    assert row.status == "implemented"
    # And it surfaces in the rendered pill (not status-unclassified).
    assert "status-implemented" in result.rendered


def test_store_status_wins_over_attestation(tmp_path: Path) -> None:
    """When both exist, the store claim is authoritative (it's what the
    gate reads) — the attestation only enriches narrative/citations."""
    indicator = AttestationArtifactIndicator(
        mode="agent_drafted", status="partial", narrative="drafted earlier"
    )
    artifact = _attestation({"CNA": {"KSI-CNA-RVP": indicator}})
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-CNA-RVP")],
            attestation=artifact,
            store_statuses={"KSI-CNA-RVP": "implemented"},  # newer store claim
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-RVP"]),
        )
    )
    [row] = result.rows
    assert row.status == "implemented"  # store wins
    # Attestation narrative still surfaces (enrichment).
    assert "drafted earlier" in (row.narrative or "")


def test_row_without_attestation_has_no_narrative(tmp_path: Path) -> None:
    """Fresh workspace (no agent document run) — narrative + status are None."""
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-CNA-RNT")],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-RNT"]),
        )
    )
    [row] = result.rows
    assert row.has_attestation is False
    assert row.narrative is None
    assert row.status is None
    assert row.citations == []


def test_row_with_attestation_carries_narrative_and_citations(tmp_path: Path) -> None:
    indicator = AttestationArtifactIndicator(
        mode="agent_drafted",
        status="implemented",
        narrative="The system uses VPC endpoints to keep traffic private.",
        citations=[
            AttestationCitation(
                evidence_id="ev-1",
                detector_id="vpc_endpoint",
                source_file="infra/vpc.tf",
                source_lines="12-24",
            ),
        ],
        controls_mapped=["sc-7"],
        controls_evidenced=["sc-7"],
        machine_validation_cadence="every PR",
        non_machine_validation_cadence="quarterly",
    )
    artifact = _attestation({"CNA": {"KSI-CNA-RNT": indicator}})
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-CNA-RNT")],
            attestation=artifact,
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-RNT"]),
        )
    )
    [row] = result.rows
    assert row.has_attestation is True
    assert row.status == "implemented"
    assert "VPC endpoints" in (row.narrative or "")
    assert row.citations == ["infra/vpc.tf:12-24"]
    assert row.controls_evidenced == ["sc-7"]
    assert row.attestation_mode == "agent_drafted"


def test_citation_without_lines_renders_path_only(tmp_path: Path) -> None:
    indicator = AttestationArtifactIndicator(
        mode="scanner_only",
        status="implemented",
        citations=[
            AttestationCitation(
                evidence_id="ev-1",
                detector_id="whole_file_check",
                source_file="config.yaml",
                source_lines=None,
            ),
        ],
    )
    artifact = _attestation({"CNA": {"KSI-CNA-RNT": indicator}})
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-CNA-RNT")],
            attestation=artifact,
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-RNT"]),
        )
    )
    [row] = result.rows
    assert row.citations == ["config.yaml"]


# --- Gate integration --------------------------------------------------


def test_passing_count_matches_gate(tmp_path: Path) -> None:
    """Counts equal the gate's verdict; not re-derived."""
    # Empty workspace → no evidence, no classifications. Items 2 + 5 fail
    # for both KSIs; items 1/3/4 pass. So 0 passing, 2 failing.
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A"), _catalog("KSI-B")],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-A", "KSI-B"]),
        )
    )
    assert result.passing_count == 0
    assert result.failing_count == 2


def test_row_gate_items_reflect_gate_output(tmp_path: Path) -> None:
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A")],
            attestation=None,
            # Empty workspace + empty cadence → items 2+3+4+5 fail; only item 1 passes.
            gate_report=_gate(tmp_path, ksis=["KSI-A"], machine="", human=""),
        )
    )
    [row] = result.rows
    assert row.gate_passed is False
    assert "implementation_goal" in row.gate_passed_items
    assert "automated_validation_cadence" in row.gate_failed_items
    assert "human_validation_cadence" in row.gate_failed_items


def test_catalog_ksi_missing_from_gate_marks_failing(tmp_path: Path) -> None:
    """Defensive: catalog has KSI-X but gate doesn't — render as failing."""
    # Gate over KSI-A only; catalog includes KSI-B.
    gate = _gate(tmp_path, ksis=["KSI-A"])
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A"), _catalog("KSI-B")],
            attestation=None,
            gate_report=gate,
        )
    )
    rows_by_id = {r.ksi_id: r for r in result.rows}
    assert rows_by_id["KSI-B"].gate_passed is False
    # All 5 items reported as failing for the unmatched KSI.
    assert len(rows_by_id["KSI-B"].gate_failed_items) == 5


# --- HTML shape --------------------------------------------------------


def test_html_includes_verdict_banner(tmp_path: Path) -> None:
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A")],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-A"]),
        )
    )
    # Empty workspace → gate fails; banner should be FAIL.
    assert "verdict-banner verdict-fail" in result.rendered
    assert "FAIL" in result.rendered


def test_html_includes_per_ksi_row_with_status_pill(tmp_path: Path) -> None:
    indicator = AttestationArtifactIndicator(
        mode="agent_drafted",
        status="implemented",
        narrative="all good",
    )
    artifact = _attestation({"CNA": {"KSI-CNA-RNT": indicator}})
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-CNA-RNT")],
            attestation=artifact,
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-RNT"]),
        )
    )
    # KSI id in summary, status pill rendered.
    assert "KSI-CNA-RNT" in result.rendered
    assert "status-implemented" in result.rendered


def test_html_groups_rows_by_theme(tmp_path: Path) -> None:
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[
                _catalog("KSI-CNA-A", theme="CNA"),
                _catalog("KSI-IAM-A", theme="IAM"),
                _catalog("KSI-CNA-B", theme="CNA"),
            ],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-CNA-A", "KSI-IAM-A", "KSI-CNA-B"]),
        )
    )
    # Each theme rendered as an h3 with count.
    assert ">CNA <" in result.rendered
    assert "(2 KSIs)" in result.rendered
    assert ">IAM <" in result.rendered
    assert "(1 KSIs)" in result.rendered


def test_html_failing_row_renders_failure_block(tmp_path: Path) -> None:
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A")],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-A"], machine="", human=""),
        )
    )
    # Failure detail block surfaces when row fails.
    assert "RFC-0017 gate failure:" in result.rendered


def test_html_passing_row_omits_failure_block(tmp_path: Path) -> None:
    indicator = AttestationArtifactIndicator(
        mode="agent_drafted",
        status="implemented",
        narrative="ok",
        citations=[
            AttestationCitation(
                evidence_id="ev-1",
                detector_id="d",
                source_file="x.tf",
                source_lines="1",
            ),
        ],
    )
    artifact = _attestation({"CNA": {"KSI-A": indicator}})
    # Seed evidence so gate item 2 passes; classify so item 5 passes.
    import json
    import sqlite3

    efterlev = tmp_path / ".efterlev"
    efterlev.mkdir(parents=True, exist_ok=True)
    (efterlev / "manifests").mkdir(exist_ok=True)
    blob_dir = efterlev / "store"
    blob_dir.mkdir(exist_ok=True)
    conn = sqlite3.connect(efterlev / "store.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS provenance_records ("
        "record_id TEXT PRIMARY KEY, record_type TEXT, content_ref TEXT, "
        "derived_from TEXT, primitive TEXT, agent TEXT, model TEXT, "
        "prompt_hash TEXT, timestamp TEXT, metadata TEXT)"
    )
    (blob_dir / "ev0.json").write_text(json.dumps({"ksis_evidenced": ["KSI-A"]}), encoding="utf-8")
    conn.execute(
        "INSERT INTO provenance_records "
        "(record_id, record_type, content_ref, derived_from, primitive, timestamp, metadata) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("ev0", "evidence", "ev0.json", "[]", "scan@1", "2026-05-19T00:00:00Z", "{}"),
    )
    (blob_dir / "cl0.json").write_text(
        json.dumps({"content": {"ksi_id": "KSI-A", "status": "implemented"}}),
        encoding="utf-8",
    )
    conn.execute(
        "INSERT INTO provenance_records "
        "(record_id, record_type, content_ref, derived_from, primitive, timestamp, metadata) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            "cl0",
            "claim",
            "cl0.json",
            "[]",
            "gap@1",
            "2026-05-19T00:00:00Z",
            json.dumps({"ksi_id": "KSI-A", "kind": "ksi_classification"}),
        ),
    )
    conn.commit()
    conn.close()

    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A")],
            attestation=artifact,
            gate_report=_gate(tmp_path, ksis=["KSI-A"]),
        )
    )
    assert result.passing_count == 1
    assert "RFC-0017 gate failure:" not in result.rendered
    # Pass-row's narrative block + cadence still render.
    assert "DRAFT narrative" in result.rendered


def test_html_renders_workspace_and_profile_in_meta(tmp_path: Path) -> None:
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A")],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-A"]),
            workspace_label="acme-saas",
            profile_label="prod",
        )
    )
    assert "acme-saas" in result.rendered
    assert "prod" in result.rendered


def test_html_escapes_workspace_label(tmp_path: Path) -> None:
    """Defensive: workspace label is escaped (could be attacker-controlled path)."""
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A")],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-A"]),
            workspace_label="<script>alert(1)</script>",
        )
    )
    assert "<script>alert(1)</script>" not in result.rendered
    assert "&lt;script&gt;" in result.rendered


# --- Per-item summary --------------------------------------------------


def test_per_item_summary_counts_failures(tmp_path: Path) -> None:
    """Per-item rollup shows which item drives most failures."""
    # 3 KSIs, all unclassified, no evidence — items 2 + 5 fail for each.
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[
                _catalog("KSI-A"),
                _catalog("KSI-B"),
                _catalog("KSI-C"),
            ],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=["KSI-A", "KSI-B", "KSI-C"]),
        )
    )
    # The item-grid block should report 3 failing for inventory + status.
    assert "Consolidated resource inventory" in result.rendered
    assert "Current status" in result.rendered
    # Counts of 3 surface in two places (inventory + status).
    assert result.rendered.count("3 failing") >= 2


# --- Empty / edge cases ------------------------------------------------


def test_empty_baseline_renders_pass_verdict(tmp_path: Path) -> None:
    """No KSIs in baseline → vacuously passing gate."""
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[],
            attestation=None,
            gate_report=_gate(tmp_path, ksis=[]),
        )
    )
    assert result.rows == []
    assert result.passing_count == 0
    assert result.failing_count == 0


def test_attestation_with_extra_ksis_ignored(tmp_path: Path) -> None:
    """Attestation includes a KSI not in catalog — silently dropped."""
    indicator = AttestationArtifactIndicator(
        mode="agent_drafted",
        status="implemented",
        narrative="extra",
    )
    # KSI-EXTRA is in attestation but not catalog.
    artifact = _attestation({"CNA": {"KSI-EXTRA": indicator}})
    result = generate_inspector_report(
        GenerateInspectorReportInput(
            catalog_entries=[_catalog("KSI-A")],
            attestation=artifact,
            gate_report=_gate(tmp_path, ksis=["KSI-A"]),
        )
    )
    # Only KSI-A renders; KSI-EXTRA is silently ignored.
    assert len(result.rows) == 1
    assert result.rows[0].ksi_id == "KSI-A"
    assert result.rows[0].narrative is None
