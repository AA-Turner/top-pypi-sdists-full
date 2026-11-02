"""Contract tests for the Phase 2 skill's verified hierarchy handoff."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLARIFY_SKILL = REPO_ROOT / ".agents" / "skills" / "speckit-clarify" / "SKILL.md"
SPECIFY_SKILL = REPO_ROOT / ".agents" / "skills" / "speckit-specify" / "SKILL.md"


def test_phase_two_revalidates_hierarchy_and_parent_context() -> None:
    clarify = CLARIFY_SKILL.read_text(encoding="utf-8")
    phase_two = clarify.split("### 1. Validate the assignment", 1)[1].split("### 2.", 1)[0]

    assert "agdt-speckit-resolve-hierarchy" in phase_two
    assert "agdt-detect-parent" not in phase_two
    assert "RESOLVED_HIERARCHY" in phase_two
    assert "RESOLVED_PARENT_NUMBER" in phase_two
    assert "RESOLVED_REASON" in phase_two
    assert 'RESOLVED_REASON" == "task-cross-repo-parent"' in phase_two
    assert "matches `HIERARCHY_LEVEL`" in phase_two
    assert "parent issue metadata used when formatting the commit" in phase_two
    commit = " ".join(clarify.split("### 7. Commit and open the Phase 2 pull request", 1)[1].split())
    assert "Use the validated `RESOLVED_PARENT_NUMBER`" in commit
    assert "When it is non-empty" in commit
    assert "When it is empty" in commit


def test_phase_one_passes_verified_parent_decision_to_scaffolding() -> None:
    specify = SPECIFY_SKILL.read_text(encoding="utf-8")

    assert "RESOLVED_PARENT_NUMBER" in specify
    assert '--verified-parent-number "$RESOLVED_PARENT_NUMBER"' in specify
