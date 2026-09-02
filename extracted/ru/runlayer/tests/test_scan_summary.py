from pathlib import Path

from runlayer_cli.models_api import SkillScanFileScore, SkillScanResponse
from runlayer_cli.skills.models import DiscoveredSkill, SkillFile
from runlayer_cli.skills.scan_summary import (
    FailOn,
    build_scan_summary,
    exit_code,
    render_scan_summary_markdown,
    render_scan_summary_text,
)


def _scan(
    *,
    name: str = "dangerous-skill",
    risk_level: str = "High",
    classification: str = "UNKNOWN_SKILL",
    skill_score: float = 0.95,
    files: list[SkillScanFileScore] | None = None,
) -> tuple[DiscoveredSkill, SkillScanResponse]:
    return (
        DiscoveredSkill(path=name, name=name),
        SkillScanResponse(
            skill_score=skill_score,
            skill_risk_level=risk_level,
            classification=classification,
            files=files or [],
        ),
    )


def test_unprefixed_reason_is_neutral_and_markdown_safe() -> None:
    scanned_skill = _scan(
        files=[
            SkillScanFileScore(
                name="SKILL.md",
                score=0.95,
                risk_level="High",
                reasons=["Investigate [docs](https://attacker.example)"],
            )
        ]
    )

    summary = build_scan_summary([scanned_skill], "scan-123", FailOn.BLOCK)
    text = render_scan_summary_text(summary)
    markdown = render_scan_summary_markdown(summary)

    assert "[Finding] Investigate [docs](https://attacker.example)" in text
    assert "Review this finding in Audit Logs" in text
    assert "**Finding:** `Investigate [docs](https://attacker.example)`" in markdown
    assert "**Finding:** Investigate [docs](https://attacker.example)" not in markdown


def test_markdown_reason_suppresses_bare_url_autolinks() -> None:
    scanned_skill = _scan(
        files=[
            SkillScanFileScore(
                name="SKILL.md",
                score=0.95,
                risk_level="High",
                reasons=["external-url: https://evil.example/install.sh"],
            )
        ]
    )

    summary = build_scan_summary([scanned_skill], "scan-123", FailOn.BLOCK)
    markdown = render_scan_summary_markdown(summary)

    assert "`external-url: https://evil.example/install.sh`" in markdown


def test_model_level_finding_includes_skill_metadata_and_next_step() -> None:
    scanned_skill = _scan(
        classification="MALICIOUS",
        skill_score=0.9500000000000001,
        files=[
            SkillScanFileScore(
                name="SKILL.md",
                score=0.0,
                risk_level="Minimal",
                reasons=[],
            )
        ],
    )

    summary = build_scan_summary([scanned_skill], "scan-123", FailOn.BLOCK)
    text = render_scan_summary_text(summary)

    assert "dangerous-skill (High; MALICIOUS; score 0.95)" in text
    assert (
        "Model-level detection; findings are not attributed to individual files" in text
    )
    assert "Open the Audit Logs entry for this scan ID" in text


def test_summary_caps_nested_rows_and_reports_omissions() -> None:
    reasons = [f"[BLOCK] reason-{index}" for index in range(4)]
    files = [
        SkillScanFileScore(
            name=f"file-{index}.md",
            score=0.95,
            risk_level="High",
            reasons=reasons,
        )
        for index in range(6)
    ]
    scanned_skills = [_scan(name=f"skill-{index}", files=files) for index in range(21)]

    summary = build_scan_summary(scanned_skills, "scan-123", FailOn.BLOCK)
    text = render_scan_summary_text(summary)

    assert "...and 11 more skills (see Audit Logs)" in text
    assert "...and 1 more file (see Audit Logs)" in text
    assert "...and 1 more reason (see Audit Logs)" in text
    assert "skill-10" not in text
    assert "file-5.md" not in text
    assert "reason-3" not in text


def test_file_count_matches_scored_files_not_discovered_files() -> None:
    """The backend drops empty/whitespace-only files before scoring, so the
    scanned-file total must come from the scan response (matching the per-file
    risk counts and the audit log's file_count), not from discovery."""
    discovered = DiscoveredSkill(
        path="skill",
        name="skill",
        files=[
            SkillFile(title="SKILL.md", path=Path("SKILL.md"), content="content"),
            SkillFile(title="notes.md", path=Path("notes.md"), content="notes"),
            SkillFile(title="empty.md", path=Path("empty.md"), content="   \n"),
        ],
    )
    result = SkillScanResponse(
        skill_score=0.95,
        skill_risk_level="High",
        classification="UNKNOWN_SKILL",
        files=[
            SkillScanFileScore(
                name="SKILL.md", score=0.95, risk_level="High", reasons=[]
            ),
            SkillScanFileScore(
                name="notes.md", score=0.0, risk_level="Minimal", reasons=[]
            ),
        ],
    )

    summary = build_scan_summary([(discovered, result)], "scan-123", FailOn.BLOCK)

    assert summary["file_count"] == 2
    assert sum(summary["file_counts"].values()) == summary["file_count"]


def test_exit_explanation_uses_actual_failing_risk_level_and_shared_code() -> None:
    summary = build_scan_summary(
        [_scan(risk_level="Critical")],
        "scan-123",
        FailOn.BLOCK,
    )

    assert exit_code(FailOn.BLOCK) == 3
    assert summary["exit_explanation"] == (
        "exiting 3: 1 skill(s) failed --fail-on=block (risk levels: Critical 1)"
    )
