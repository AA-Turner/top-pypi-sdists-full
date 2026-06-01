"""Tests for `efterlev detectors show <id>`.

Read/inspect counterpart to `detectors list` (registry summary) and
`detectors new` (write/scaffold). Surfaces the mapping.yaml notes,
evidence.yaml shape, README excerpt, and fixture file counts that
`detectors list` elides.
"""

from __future__ import annotations

from typer.testing import CliRunner

from efterlev.cli.main import app

runner = CliRunner()


def test_show_known_detector_includes_id_version_source() -> None:
    """Header line carries id@version + source label."""
    result = runner.invoke(app, ["detectors", "show", "github.branch_protection"])
    assert result.exit_code == 0
    assert "github.branch_protection@" in result.output
    assert "source=terraform" in result.output


def test_show_includes_ksis_and_controls() -> None:
    """KSI list + control list visible on the header."""
    result = runner.invoke(app, ["detectors", "show", "github.branch_protection"])
    assert result.exit_code == 0
    assert "KSIs:" in result.output
    assert "KSI-PIY-RSD" in result.output
    assert "Controls:" in result.output
    assert "SA-15" in result.output
    assert "CM-2" in result.output


def test_show_supplementary_800_53_only_tag() -> None:
    """Supplementary detectors (no KSI) get the visible `[800-53 only]` tag."""
    result = runner.invoke(app, ["detectors", "show", "aws.iam_password_policy"])
    assert result.exit_code == 0
    assert "[800-53 only]" in result.output
    assert "KSIs:" in result.output
    # The em-dash is the no-KSI placeholder.
    assert "—" in result.output


def test_show_includes_mapping_notes_when_yaml_present() -> None:
    """When mapping.yaml is present, KSI + control coverage notes render."""
    result = runner.invoke(app, ["detectors", "show", "github.branch_protection"])
    assert result.exit_code == 0
    assert "Mapping notes:" in result.output
    # Coverage label is included next to each entry.
    assert "(partial)" in result.output
    # The notes paragraph from mapping.yaml is included verbatim (wrapped).
    assert "merge-time gate" in result.output


def test_show_includes_evidence_shape_when_yaml_present() -> None:
    """When evidence.yaml is present, the per-record content keys render."""
    result = runner.invoke(app, ["detectors", "show", "github.branch_protection"])
    assert result.exit_code == 0
    assert "Evidence shape" in result.output
    assert "rule_state:" in result.output
    assert "has_required_status_checks: bool" in result.output


def test_show_includes_readme_excerpt() -> None:
    """README's lead paragraph (after the H1, before the first H2) renders."""
    result = runner.invoke(app, ["detectors", "show", "github.branch_protection"])
    assert result.exit_code == 0
    assert "README:" in result.output
    # The lead paragraph mentions branch_protection's core claim.
    assert "branch_protection" in result.output.lower()


def test_show_includes_fixture_summary() -> None:
    """Fixture file counts + names render under the Fixtures section."""
    result = runner.invoke(app, ["detectors", "show", "github.branch_protection"])
    assert result.exit_code == 0
    assert "Fixtures:" in result.output
    assert "should_match:" in result.output
    assert "should_not_match:" in result.output
    assert "branch_protection_enforced.tf" in result.output
    assert "branch_protection_empty.tf" in result.output


def test_show_unknown_id_exits_1_with_suggestions() -> None:
    """Unknown detector id exits 1 and suggests near-matches."""
    result = runner.invoke(app, ["detectors", "show", "aws.foo_bar"])
    assert result.exit_code == 1
    assert "is not registered" in result.output
    # The cloud-prefix fallback should suggest aws.* detectors.
    assert "did you mean:" in result.output
    assert "aws." in result.output


def test_show_unknown_id_no_cloud_prefix_falls_back_to_list_hint() -> None:
    """A nonsense id with no overlap points the user at `detectors list`."""
    result = runner.invoke(app, ["detectors", "show", "totally_made_up_id"])
    assert result.exit_code == 1
    assert "is not registered" in result.output
    assert "detectors list" in result.output


def test_show_substring_match_suggests_overlapping_id() -> None:
    """A near-miss substring suggests the overlapping registered id."""
    # `branch_protection` is a substring of `github.branch_protection`.
    result = runner.invoke(app, ["detectors", "show", "branch_protection"])
    assert result.exit_code == 1
    assert "is not registered" in result.output
    assert "github.branch_protection" in result.output
