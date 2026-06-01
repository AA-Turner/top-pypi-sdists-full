"""Tests for the evals/cli.py report-reader helpers.

Locks the JSON shape contracts the readers depend on. The 2026-05-09
baseline run surfaced a real bug: `_read_doc_narratives` assumed
`attestations[].draft.ksi_id` (the in-memory model nesting) but the
serializer flattens to `attestations[].ksi_id`. Result: M4 was always
n/a (0/0). These tests pin the actual shape.

If the doc-report serializer ever changes, these tests fail before
the metrics silently regress.
"""

from __future__ import annotations

import json
from pathlib import Path

from evals.cli import (
    _read_doc_narratives,
    _read_gap_classifications,
    _read_gap_rationales,
    _read_poam_markdown,
)


def _write_report(workspace: Path, rel: str, body: str) -> Path:
    p = workspace / ".efterlev" / "reports" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_read_doc_narratives_handles_flattened_attestation_shape(tmp_path: Path) -> None:
    """The shipped serializer flattens KsiAttestation.draft.* to
    top-level keys on each attestation object. Lock the actual shape
    so PR beta's nesting bug stays fixed."""
    body = json.dumps(
        {
            "attestations": [
                {
                    "ksi_id": "KSI-AFR-FSI",
                    "narrative": "security@example.com is monitored 24/7",
                    "boundary_state": "in_boundary",
                    "citations": [],
                    "controls_evidenced": [],
                    "controls_mapped": [],
                    "mode": "narrative_drafted",
                    "claim_record_id": "sha256:abc",
                    "status": "partial",
                },
                {
                    "ksi_id": "KSI-INR-RIR",
                    "narrative": "PagerDuty rotation handles incidents",
                    "boundary_state": "in_boundary",
                    "citations": [],
                    "controls_evidenced": [],
                    "controls_mapped": [],
                    "mode": "narrative_drafted",
                    "claim_record_id": "sha256:def",
                    "status": "partial",
                },
            ],
            "skipped_ksi_ids": [],
        }
    )
    _write_report(tmp_path, "documentation-20260509-120000.json", body)

    narratives = _read_doc_narratives(tmp_path)
    assert "KSI-AFR-FSI" in narratives
    assert "security@example.com" in narratives["KSI-AFR-FSI"]
    assert "KSI-INR-RIR" in narratives
    assert "PagerDuty" in narratives["KSI-INR-RIR"]


def test_read_doc_narratives_skips_attestations_without_narrative(tmp_path: Path) -> None:
    """An attestation may have ksi_id but no narrative (e.g.,
    deterministic-template mode for evidence_layer_inapplicable
    KSIs sometimes ships with narrative=null). Skip those rather
    than emit an empty-string narrative that would confuse M4."""
    body = json.dumps(
        {
            "attestations": [
                {"ksi_id": "KSI-A", "narrative": "real narrative"},
                {"ksi_id": "KSI-B", "narrative": None},
                {"ksi_id": "KSI-C"},  # missing key entirely
            ]
        }
    )
    _write_report(tmp_path, "documentation-20260509-120000.json", body)

    narratives = _read_doc_narratives(tmp_path)
    assert narratives == {"KSI-A": "real narrative"}


def test_read_doc_narratives_returns_empty_when_no_report(tmp_path: Path) -> None:
    """No reports/ dir at all: empty dict, not exception."""
    assert _read_doc_narratives(tmp_path) == {}


def test_read_gap_classifications_picks_latest_report(tmp_path: Path) -> None:
    """Two gap reports — the lexically-greatest (latest by timestamp)
    wins. Sortable timestamps are the contract."""
    _write_report(
        tmp_path,
        "gap-20260509-100000.json",
        json.dumps({"ksi_classifications": [{"ksi_id": "KSI-A", "status": "implemented"}]}),
    )
    _write_report(
        tmp_path,
        "gap-20260509-120000.json",
        json.dumps({"ksi_classifications": [{"ksi_id": "KSI-A", "status": "partial"}]}),
    )

    classifications = _read_gap_classifications(tmp_path)
    assert classifications == {"KSI-A": "partial"}


def test_read_gap_rationales_extracts_rationale_text(tmp_path: Path) -> None:
    """M3 reads rationales from the gap report. Rationales live at
    `ksi_classifications[].rationale` per the gap-agent's serializer."""
    _write_report(
        tmp_path,
        "gap-20260509-120000.json",
        json.dumps(
            {
                "ksi_classifications": [
                    {
                        "ksi_id": "KSI-IAM-MFA",
                        "status": "partial",
                        "rationale": "admin_with_mfa enforces MFA; admin_no_mfa does not.",
                    },
                    {
                        "ksi_id": "KSI-SVC-VRI",
                        "status": "partial",
                        "rationale": "TLS 1.3 listener present; HTTP listener also present.",
                    },
                ]
            }
        ),
    )

    rationales = _read_gap_rationales(tmp_path)
    assert "admin_with_mfa" in rationales["KSI-IAM-MFA"]
    assert "TLS 1.3" in rationales["KSI-SVC-VRI"]


def test_read_poam_markdown_returns_empty_when_no_poam(tmp_path: Path) -> None:
    """Pipelines that didn't generate a POAM yield empty string,
    which M5 treats as 0 excluded count + no leak constraint
    violations (vacuous pass on Check A)."""
    assert _read_poam_markdown(tmp_path) == ""


def test_read_poam_markdown_returns_latest_md(tmp_path: Path) -> None:
    """POAM lives at .efterlev/reports/poam/poam-*.md (subdirectory,
    not flat under reports/). Lock the location."""
    poam_dir = tmp_path / ".efterlev" / "reports" / "poam"
    poam_dir.mkdir(parents=True)
    (poam_dir / "poam-20260509-100000.md").write_text("OLDER POAM body", encoding="utf-8")
    (poam_dir / "poam-20260509-120000.md").write_text(
        "NEWER POAM body\n- **Excluded as out-of-boundary:** 3 item(s)",
        encoding="utf-8",
    )

    body = _read_poam_markdown(tmp_path)
    assert "NEWER POAM body" in body
    assert "Excluded as out-of-boundary" in body
