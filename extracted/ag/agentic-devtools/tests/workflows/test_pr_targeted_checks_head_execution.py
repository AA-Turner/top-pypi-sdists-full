"""Contracts for separate merge-ref integration and explicit PR-head execution."""

import os
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "pr-targeted-checks.yml"
HEAD_JOB = "pr-head-targeted-checks"
HEAD_GATE = "pr-head-targeted-checks-gate"


@pytest.fixture
def workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _step(job: dict, name: str) -> dict:
    return next(step for step in job["steps"] if step.get("name") == name)


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True, shell=False)
    return result.stdout.strip()


@pytest.fixture
def history(tmp_path: Path) -> dict:
    """Model a fork head available through the base repository's object graph."""
    origin = tmp_path / "base-repository"
    origin.mkdir()
    _git(origin, "init", "-b", "main")
    _git(origin, "config", "user.name", "Workflow Test")
    _git(origin, "config", "user.email", "workflow@example.invalid")
    (origin / "base.txt").write_text("base\n", encoding="utf-8")
    _git(origin, "add", ".")
    _git(origin, "commit", "-m", "base")
    base = _git(origin, "rev-parse", "HEAD")
    _git(origin, "checkout", "-b", "fork-head")
    (origin / "changed.py").write_text("value = 1\n", encoding="utf-8")
    _git(origin, "add", ".")
    _git(origin, "commit", "-m", "head")
    head = _git(origin, "rev-parse", "HEAD")
    _git(origin, "checkout", "main")
    (origin / "moving-main.txt").write_text("later\n", encoding="utf-8")
    _git(origin, "add", ".")
    _git(origin, "commit", "-m", "moving main")
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    _git(checkout, "init")
    _git(checkout, "remote", "add", "origin", str(origin))
    _git(checkout, "fetch", "origin")
    _git(checkout, "checkout", "--detach", head)
    return {"checkout": checkout, "origin": origin, "base": base, "head": head}


def _preflight(workflow: dict, history: dict, tmp_path: Path, **overrides: str) -> tuple:
    step = _step(workflow["jobs"][HEAD_JOB], "Verify PR head and exact changed files")
    output = tmp_path / "outputs"
    summary = tmp_path / "summary"
    env = {
        **os.environ,
        "EXPECTED_HEAD_SHA": history["head"],
        "EXPECTED_BASE_SHA": history["base"],
        "GITHUB_OUTPUT": str(output),
        "GITHUB_STEP_SUMMARY": str(summary),
        "RUNNER_TEMP": str(tmp_path),
        **overrides,
    }
    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", step["run"]],
        cwd=history["checkout"],
        env=env,
        capture_output=True,
        text=True,
        shell=False,
    )
    return result, output.read_text() if output.exists() else "", summary.read_text() if summary.exists() else ""


def test_trigger_and_permissions_remain_unprivileged(workflow: dict) -> None:
    # PyYAML's YAML 1.1 loader interprets the Actions key "on" as True.
    assert workflow.get("on", workflow.get(True)) == {"pull_request": {"branches": ["main"]}}
    assert workflow["permissions"] == {"contents": "read"}
    text = WORKFLOW.read_text(encoding="utf-8")
    for forbidden in ("pull_request_target", "secrets.", "secrets[", "write-all", "rulesets", "branch-protection"):
        assert forbidden not in text
    assert set(workflow["jobs"]) == {"targeted-checks", "targeted-checks-gate", HEAD_JOB, HEAD_GATE}
    for job in workflow["jobs"].values():
        assert "permissions" not in job
        assert not job.get("continue-on-error")
        for step in job["steps"]:
            assert not step.get("continue-on-error")


def test_merge_ref_integration_behavior_is_preserved(workflow: dict) -> None:
    job = workflow["jobs"]["targeted-checks"]
    assert job["name"] == "Run Targeted Checks"
    assert job["runs-on"] == "ubuntu-latest"
    checkout = _step(job, "Checkout code")
    assert checkout == {"name": "Checkout code", "uses": "actions/checkout@v4", "with": {"fetch-depth": 0}}
    assert _step(job, "Compute changed files") == {
        "name": "Compute changed files",
        "id": "changed",
        "run": (
            "git fetch origin main\n"
            "git diff --name-only origin/main...HEAD > /tmp/changed-files.txt\n"
            'echo "count=$(wc -l < /tmp/changed-files.txt | tr -d \' \')" >> "$GITHUB_OUTPUT"\n'
            "cat /tmp/changed-files.txt\n"
        ),
    }
    for name in ("Set up Go", "Install actionlint", "Run targeted checks"):
        assert _step(job, name)["if"] == "steps.changed.outputs.count != '0'"
    assert _step(job, "Run targeted checks")["run"].strip() == "python -m agentic_devtools.cli.checks"
    assert _step(job, "No changes detected")["if"] == "steps.changed.outputs.count == '0'"
    assert _step(job, "Install dependencies")["run"] == (
        'python -m pip install --upgrade pip\npip install -e ".[dev]"\n'
    )
    assert _step(job, "Set up Python")["with"] == {"python-version": "3.14", "cache": "pip"}
    assert _step(job, "Install actionlint")["run"] == "bash scripts/install-actionlint.sh"
    assert _step(job, "Install markdownlint-cli2")["run"] == "npm install -g markdownlint-cli2@0.17.2"
    gate = workflow["jobs"]["targeted-checks-gate"]
    assert gate["name"] == "Targeted Checks ✅"
    assert gate["needs"] == ["targeted-checks"]
    assert gate["if"] == "always()"
    assert gate["steps"] == [
        {
            "name": "Check result",
            "run": (
                'if [[ "${{ needs.targeted-checks.result }}" == "failure" ]]; then\n'
                '  echo "Targeted checks failed"\n'
                "  exit 1\n"
                "fi\n"
                'echo "Targeted checks passed"\n'
            ),
        }
    ]


def test_head_checkout_and_preflight_precede_all_execution(workflow: dict) -> None:
    job = workflow["jobs"][HEAD_JOB]
    assert "if" not in job
    checkout, verify = job["steps"][:2]
    assert checkout["uses"] == "actions/checkout@v4"
    assert checkout["with"] == {
        "repository": "${{ github.repository }}",
        "ref": "${{ github.event.pull_request.head.sha }}",
        "fetch-depth": 0,
    }
    assert "if" not in checkout
    assert verify["name"] == "Verify PR head and exact changed files"
    assert verify["id"] == "verified"
    assert verify["shell"] == "bash"
    assert "if" not in verify
    assert verify["env"] == {
        "EXPECTED_HEAD_SHA": "${{ github.event.pull_request.head.sha }}",
        "EXPECTED_BASE_SHA": "${{ github.event.pull_request.base.sha }}",
    }
    script = verify["run"]
    assert "set -euo pipefail" in script
    assert "git rev-parse --verify HEAD" in script
    assert "^[0-9a-fA-F]{40}$" in script
    assert 'git fetch --no-tags origin "$EXPECTED_BASE_SHA"' in script
    assert 'git update-ref refs/remotes/origin/main "$EXPECTED_BASE_SHA"' in script
    assert "git rev-parse --verify refs/remotes/origin/main" in script
    assert "git diff --name-only --diff-filter=d origin/main...HEAD --" in script
    for forbidden in ("|| true", "|| echo", "HEAD~", "diff-tree", "git fetch origin main", "${{"):
        assert forbidden not in script
    assert job["outputs"]["head_sha"] == "${{ steps.verified.outputs.head_sha }}"
    checks = _step(job, "Run targeted checks")
    assert checks["run"].strip() == "python -m agentic_devtools.cli.checks"
    assert checks["if"] == "steps.verified.outputs.count != '0'"
    assert _step(job, "No changes detected")["if"] == "steps.verified.outputs.count == '0'"
    # Preserve the same tools as integration checks, without fetching a moving base.
    merge = workflow["jobs"]["targeted-checks"]
    for name in (
        "Set up Python",
        "Install dependencies",
        "Set up Node.js (for markdownlint)",
        "Install markdownlint-cli2",
    ):
        assert _step(job, name) == _step(merge, name)
    for name in ("Set up Go", "Install actionlint"):
        assert _step(job, name)["if"] == "steps.verified.outputs.count != '0'"
        assert {k: v for k, v in _step(job, name).items() if k != "if"} == {
            k: v for k, v in _step(merge, name).items() if k != "if"
        }


def test_preflight_pins_event_base_and_records_actual_head(workflow: dict, history: dict, tmp_path: Path) -> None:
    result, output, summary = _preflight(workflow, history, tmp_path)
    assert result.returncode == 0, result.stderr
    assert _git(history["checkout"], "rev-parse", "origin/main") == history["base"]
    assert _git(history["checkout"], "rev-parse", "HEAD") == history["head"]
    assert f"head_sha={history['head']}\n" in output
    assert "count=1\n" in output
    assert history["head"] in summary
    assert "changed.py" in result.stdout
    assert "moving-main.txt" not in result.stdout


@pytest.mark.parametrize("expected", ["", "abc", "g" * 40, "a" * 39, "a" * 41, "a" * 40, "a" * 40 + "\n"])
def test_invalid_or_mismatched_head_fails_before_diff(
    workflow: dict, history: dict, tmp_path: Path, expected: str
) -> None:
    before = _git(history["checkout"], "rev-parse", "origin/main")
    result, output, _ = _preflight(workflow, history, tmp_path, EXPECTED_HEAD_SHA=expected)
    assert result.returncode != 0
    assert "count=" not in output
    assert "head_sha=" not in output
    assert _git(history["checkout"], "rev-parse", "origin/main") == before


@pytest.mark.parametrize("base", ["", "invalid", "f" * 40])
def test_unavailable_base_never_becomes_empty_success(workflow: dict, history: dict, tmp_path: Path, base: str) -> None:
    result, output, _ = _preflight(workflow, history, tmp_path, EXPECTED_BASE_SHA=base)
    assert result.returncode != 0
    assert "count=" not in output


def test_missing_head_fails_closed(workflow: dict, history: dict, tmp_path: Path) -> None:
    _git(history["checkout"], "symbolic-ref", "HEAD", "refs/heads/missing")
    result, output, _ = _preflight(workflow, history, tmp_path)
    assert result.returncode != 0
    assert output == ""


def test_missing_merge_base_fails_closed(workflow: dict, history: dict, tmp_path: Path) -> None:
    origin = history["origin"]
    _git(origin, "checkout", "--orphan", "unrelated")
    _git(origin, "commit", "-m", "unrelated root")
    base = _git(origin, "rev-parse", "HEAD")
    result, output, _ = _preflight(workflow, history, tmp_path, EXPECTED_BASE_SHA=base)
    assert result.returncode != 0
    assert "count=" not in output


def test_no_change_success_requires_verified_refs(workflow: dict, history: dict, tmp_path: Path) -> None:
    result, output, summary = _preflight(workflow, history, tmp_path, EXPECTED_BASE_SHA=history["head"])
    assert result.returncode == 0, result.stderr
    assert "count=0\n" in output
    assert f"head_sha={history['head']}\n" in output
    assert history["head"] in summary


@pytest.mark.parametrize("result", ["success", "failure", "cancelled", "skipped", "", "unknown"])
def test_head_gate_accepts_only_success(workflow: dict, result: str) -> None:
    gate = workflow["jobs"][HEAD_GATE]
    assert gate["name"] == "PR Head Targeted Checks ✅"
    assert gate["needs"] == [HEAD_JOB]
    assert gate["if"] == "always()"
    step = gate["steps"][0]
    assert "if" not in step
    assert step["env"] == {"HEAD_RESULT": "${{ needs.pr-head-targeted-checks.result }}"}
    completed = subprocess.run(
        ["bash", "-e", "-o", "pipefail", "-c", step["run"]],
        env={**os.environ, "HEAD_RESULT": result},
        capture_output=True,
        text=True,
        shell=False,
    )
    assert (completed.returncode == 0) == (result == "success")
