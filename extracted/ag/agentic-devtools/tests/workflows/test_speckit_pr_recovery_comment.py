"""Behavioral checks for the created-PR failure recovery entrypoint."""

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "render-pr-recovery.js"


def _render(**overrides: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        GITHUB_REPOSITORY="swai-factory/agentic-devtools",
        GITHUB_RUN_ID="12345",
        NEXT_PHASE="2",
        NEXT_PHASE_NAME="clarify",
        HIERARCHY_LEVEL="feature",
        CREATED_PR_NUMBER="42",
        CREATED_PR_URL="https://github.com/swai-factory/agentic-devtools/pull/42",
        LABEL_SETUP_STATUS="failed",
        ARTIFACT_GATE_RESULT="pass",
    )
    env.update(overrides)
    return subprocess.run(["node", str(SCRIPT)], env=env, capture_output=True, text=True, check=False)


@pytest.mark.parametrize("phase", ["1", "2", "3"])
@pytest.mark.parametrize("level", ["epic", "feature", "task", "unknown"])
@pytest.mark.parametrize("label_status", ["failed", ""])
@pytest.mark.parametrize("artifact_result", ["fail", "pass", ""])
def test_recovery_covers_phase_hierarchy_and_failure_combinations(
    phase: str, level: str, label_status: str, artifact_result: str
) -> None:
    result = _render(
        NEXT_PHASE=phase,
        HIERARCHY_LEVEL=level,
        LABEL_SETUP_STATUS=label_status,
        ARTIFACT_GATE_RESULT=artifact_result,
    )

    assert result.returncode == 0, result.stderr
    body = result.stdout
    assert f'--raw-field "labels[]=speckit:phase-{phase}"' in body
    if level == "unknown":
        assert "labels[]=speckit:level-" not in body
    else:
        assert f'--raw-field "labels[]=speckit:level-{level}"' in body
    assert ("PR Created, Routing Labels Failed" in body) == (label_status == "failed")
    assert ("PR Created, Workflow Incomplete" in body) == (label_status != "failed")
    if phase == "3":
        assert "Phase 4 is not a valid dispatch phase" in body
    else:
        assert f"manually dispatch Phase {int(phase) + 1}" in body
    assert "then merge" not in body
    assert "before marking the PR ready or merging" in body
    assert "complete any skipped artifact repair" in body
    assert ("artifact gate reported violations" in body) == (artifact_result == "fail")
    assert "--paginate --jq '.[].name'" in body
    assert "actions/runs/12345" in body


def test_url_only_recovery_does_not_invent_a_pr_number() -> None:
    result = _render(CREATED_PR_NUMBER="")

    assert result.returncode == 0, result.stderr
    assert "Use the PR URL to determine its number" in result.stdout
    assert "issues/<PR_NUMBER>/labels" in result.stdout
    assert "pull/42" in result.stdout


@pytest.mark.parametrize(
    "overrides",
    [
        {"GITHUB_REPOSITORY": "not-a-repository"},
        {"NEXT_PHASE": "4"},
        {"NEXT_PHASE": "0"},
        {"NEXT_PHASE": "not-a-phase"},
        {"GITHUB_RUN_ID": "invalid"},
        {"CREATED_PR_NUMBER": "invalid"},
        {"CREATED_PR_NUMBER": "", "CREATED_PR_URL": ""},
    ],
)
def test_invalid_recovery_inputs_fail_explicitly(overrides: dict[str, str]) -> None:
    result = _render(**overrides)

    assert result.returncode != 0
    assert result.stdout == ""
    assert "Could not render SpecKit PR recovery:" in result.stderr
