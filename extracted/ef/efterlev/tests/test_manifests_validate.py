"""Tests for `efterlev manifests validate <path>`.

Offline schema validation for Evidence Manifests. Pre-commit / pre-PR
gate that catches the high-leverage authoring mistakes (typo'd field
names rejected by `extra="forbid"`, malformed dates, missing required
fields) before scan time.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from efterlev.cli.main import app

runner = CliRunner()


_VALID_MANIFEST = """
ksi: KSI-AFR-FSI
name: "Security inbox attestation"
evidence:
  - type: attestation
    statement: "Monitored security inbox at security@example.com with 15-min SLA."
    attested_by: "alice@example.com"
    attested_at: 2026-04-01
    next_review: 2026-10-01
"""


_INVALID_TYPO_FIELD = """
ksi: KSI-AFR-FSI
evidence:
  - type: attestation
    statement: "typo: attester instead of attested_by"
    attester: "alice"
    attested_at: 2026-04-01
"""


_INVALID_MISSING_KSI = """
name: "missing ksi field"
evidence: []
"""


_INVALID_NOT_A_MAPPING = """
- this is a list at the top
- not a mapping
"""


def test_validate_single_valid_file_exits_0(tmp_path: Path) -> None:
    """Valid manifest exits 0 with a per-file ✓ line + summary."""
    p = tmp_path / "valid.yml"
    p.write_text(_VALID_MANIFEST, encoding="utf-8")
    result = runner.invoke(app, ["manifests", "validate", str(p)])
    assert result.exit_code == 0
    assert "✓" in result.output
    assert "ksi=KSI-AFR-FSI" in result.output
    assert "attestations=1" in result.output
    assert "1/1 valid" in result.output


def test_validate_typo_field_exits_1_and_reports_path(tmp_path: Path) -> None:
    """A typo'd field name (`attester` vs `attested_by`) is rejected."""
    p = tmp_path / "typo.yml"
    p.write_text(_INVALID_TYPO_FIELD, encoding="utf-8")
    result = runner.invoke(app, ["manifests", "validate", str(p)])
    assert result.exit_code == 1
    assert "✗" in result.output
    assert "typo.yml" in result.output
    assert "extra_forbidden" in result.output or "not permitted" in result.output
    assert "0/1 valid" in result.output
    assert "1 failed" in result.output


def test_validate_missing_ksi_exits_1(tmp_path: Path) -> None:
    """Missing required `ksi:` field is rejected."""
    p = tmp_path / "no-ksi.yml"
    p.write_text(_INVALID_MISSING_KSI, encoding="utf-8")
    result = runner.invoke(app, ["manifests", "validate", str(p)])
    assert result.exit_code == 1
    assert "ksi" in result.output.lower()
    assert "1 failed" in result.output


def test_validate_top_level_not_a_mapping_exits_1(tmp_path: Path) -> None:
    """A list at the top level (not a mapping) is rejected with a clear error."""
    p = tmp_path / "list-top.yml"
    p.write_text(_INVALID_NOT_A_MAPPING, encoding="utf-8")
    result = runner.invoke(app, ["manifests", "validate", str(p)])
    assert result.exit_code == 1
    assert "mapping" in result.output.lower()


def test_validate_directory_walks_and_reports_each(tmp_path: Path) -> None:
    """A directory argument validates every *.yml + *.yaml found."""
    (tmp_path / "good1.yml").write_text(_VALID_MANIFEST, encoding="utf-8")
    (tmp_path / "good2.yaml").write_text(_VALID_MANIFEST, encoding="utf-8")
    (tmp_path / "bad.yml").write_text(_INVALID_TYPO_FIELD, encoding="utf-8")
    result = runner.invoke(app, ["manifests", "validate", str(tmp_path)])
    assert result.exit_code == 1
    assert result.output.count("✓") == 2
    assert result.output.count("✗") == 1
    assert "2/3 valid; 1 failed" in result.output


def test_validate_directory_skips_template_files(tmp_path: Path) -> None:
    """Files matching `*.template.yml` are skipped (consistent with
    the scan-time discovery glob)."""
    (tmp_path / "real.yml").write_text(_VALID_MANIFEST, encoding="utf-8")
    (tmp_path / "draft.template.yml").write_text(
        "ksi: KSI-AFR-FSI\nbroken: true\n", encoding="utf-8"
    )
    result = runner.invoke(app, ["manifests", "validate", str(tmp_path)])
    assert result.exit_code == 0
    assert result.output.count("✓") == 1
    assert "draft.template.yml" not in result.output
    assert "1/1 valid" in result.output


def test_validate_empty_directory_exits_2_with_helpful_message(tmp_path: Path) -> None:
    """No manifests found in the directory is a usage error, not pass."""
    result = runner.invoke(app, ["manifests", "validate", str(tmp_path)])
    assert result.exit_code == 2
    assert "no manifest files found" in result.output


def test_validate_nonexistent_path_exits_2(tmp_path: Path) -> None:
    """A path that doesn't exist is a clear usage error."""
    result = runner.invoke(app, ["manifests", "validate", str(tmp_path / "missing.yml")])
    assert result.exit_code == 2
    assert "does not exist" in result.output


@pytest.mark.parametrize("ksi_value", ["KSI-AFR-FSI", "KSI-NOT-IN-BASELINE", "totally-made-up-ksi"])
def test_validate_does_not_check_ksi_against_baseline(tmp_path: Path, ksi_value: str) -> None:
    """Per design: `validate` is offline-only; KSI value can be any string
    accepted by the schema. The cross-baseline check happens at scan time."""
    manifest = (
        f"ksi: {ksi_value}\n"
        "evidence:\n"
        "  - type: attestation\n"
        "    statement: 's'\n"
        "    attested_by: 'a'\n"
        "    attested_at: 2026-04-01\n"
    )
    p = tmp_path / "manifest.yml"
    p.write_text(manifest, encoding="utf-8")
    result = runner.invoke(app, ["manifests", "validate", str(p)])
    assert result.exit_code == 0
