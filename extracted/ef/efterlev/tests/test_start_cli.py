"""Tests for `efterlev start` — the Stage 0 pre-scan walkthrough.

The core is `render_start_report` (pure, deterministic). Tests assert
the report adapts to architecture / partition / posture / impact level,
that it only cites shipped commands, and that the CLI wiring works
non-interactively (the path CI + scripts take).
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from typer.testing import CliRunner

from efterlev.cli.main import app
from efterlev.cli.start_cli import (
    StartAnswers,
    render_start_report,
    run_start,
)

runner = CliRunner()

_FIXED = datetime(2026, 5, 20, tzinfo=UTC)


def _report(**kwargs: str) -> str:
    return render_start_report(StartAnswers(**kwargs), generated_at=_FIXED)  # type: ignore[arg-type]


# --- determinism + situation block -------------------------------------


def test_report_is_deterministic() -> None:
    a = StartAnswers(architecture="serverless")
    assert render_start_report(a, generated_at=_FIXED) == render_start_report(
        a, generated_at=_FIXED
    )


def test_report_echoes_inputs() -> None:
    """The report must surface the inputs it used so assumed defaults are visible."""
    report = _report(
        cloud="aws",
        partition="govcloud",
        impact_level="high",
        architecture="vms",
        posture="soc2",
    )
    assert "AWS (GovCloud)" in report
    assert "FedRAMP 20x High" in report
    assert "Virtual machines" in report
    assert "SOC 2" in report


def test_default_answers_produce_serverless_moderate_report() -> None:
    report = render_start_report(StartAnswers(), generated_at=_FIXED)
    assert "AWS (Commercial)" in report
    assert "FedRAMP 20x Moderate" in report
    assert "Serverless" in report


# --- architecture-specific guidance ------------------------------------


def test_serverless_marks_host_hardening_not_applicable() -> None:
    report = _report(architecture="serverless")
    assert "Host / OS hardening — there are no servers you patch" in report
    assert "IAM (least privilege" in report


def test_vms_does_not_mark_host_hardening_na() -> None:
    """VM architectures exercise host KSIs — host hardening is a FOCUS, not n/a."""
    report = _report(architecture="vms")
    assert "Host / OS hardening + a documented patching cadence" in report
    # The serverless "no servers you patch" line must NOT appear.
    assert "there are no servers you patch" not in report


def test_containers_mentions_image_scanning() -> None:
    report = _report(architecture="containers")
    assert "Container image scanning" in report


def test_hybrid_notes_most_families_apply() -> None:
    report = _report(architecture="hybrid")
    assert "Most KSI families apply" in report


# --- recommended-path branching ----------------------------------------


def test_govcloud_adds_bedrock_note_and_init_flags() -> None:
    report = _report(cloud="aws", partition="govcloud")
    assert "GovCloud note:" in report
    assert "--llm-backend bedrock --llm-region us-gov-west-1" in report


def test_commercial_init_command_has_no_bedrock_flags() -> None:
    report = _report(cloud="aws", partition="commercial")
    assert "--llm-backend bedrock" not in report
    assert "efterlev init --baseline fedramp-20x-moderate" in report


def test_non_aws_cloud_adds_coverage_heads_up() -> None:
    report = _report(cloud="gcp")
    assert "deepest evidence coverage today is for" in report


def test_rev5_posture_frames_20x_as_distinct() -> None:
    report = _report(posture="fedramp-rev5")
    assert "distinct, KSI-based path" in report


def test_high_impact_adds_caution() -> None:
    report = _report(impact_level="high")
    assert "High baseline:" in report
    # init command should target the high baseline.
    assert "fedramp-20x-high" in report


def test_moderate_impact_no_high_caution() -> None:
    report = _report(impact_level="moderate")
    assert "High baseline:" not in report


# --- shipped-commands-only discipline ----------------------------------


def test_report_cites_only_shipped_commands() -> None:
    """The actionable next-steps must not reference unshipped commands.
    `efterlev scope` and `poam delta` are planned — they must NOT appear
    in the report's command guidance."""
    report = _report(architecture="serverless")
    assert "efterlev scope" not in report
    assert "poam delta" not in report
    # Shipped commands it SHOULD cite:
    assert "efterlev init" in report
    assert "efterlev report run" in report
    assert "efterlev agent gap" in report
    assert "efterlev readiness --strict" in report
    assert "efterlev report inspector" in report


def test_report_always_carries_draft_caveat() -> None:
    report = _report()
    assert "not an authorization" in report
    assert "not a 3PAO" in report


# --- journey table -----------------------------------------------------


def test_journey_table_lists_all_seven_stages() -> None:
    report = _report()
    for stage in (
        "0. Strategic",
        "1. Engineering",
        "2. 3PAO",
        "3. Submission",
        "4. Authorization",
        "5. ConMon",
        "6. Incident",
    ):
        assert stage in report
    assert "You are at Stage 0" in report


# --- CLI wiring (non-interactive path) ---------------------------------


def test_cli_runs_non_interactively_with_flags() -> None:
    result = runner.invoke(
        app,
        [
            "start",
            "--cloud",
            "aws",
            "--partition",
            "govcloud",
            "--architecture",
            "serverless",
            "--impact-level",
            "moderate",
            "--posture",
            "none",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "Your FedRAMP 20x path" in result.output
    assert "GovCloud" in result.output


def test_cli_rejects_invalid_flag_value() -> None:
    result = runner.invoke(app, ["start", "--architecture", "mainframe"])
    assert result.exit_code == 2
    assert "must be one of" in result.output


def test_cli_writes_out_file(tmp_path: Path) -> None:
    out = tmp_path / "path.md"
    result = runner.invoke(app, ["start", "--architecture", "serverless", "--out", str(out)])
    assert result.exit_code == 0, result.output
    assert out.is_file()
    content = out.read_text(encoding="utf-8")
    assert "Your FedRAMP 20x path" in content
    # Confirmation line printed to stdout.
    assert "Wrote your FedRAMP 20x path to:" in result.output


def test_run_start_returns_zero_with_defaults() -> None:
    # Non-interactive (no TTY in test) + no flags → defaults, exit 0.
    assert run_start() == 0
