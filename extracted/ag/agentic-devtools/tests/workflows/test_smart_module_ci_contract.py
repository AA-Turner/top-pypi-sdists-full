"""Contract tests for the smart-module and full-suite CI workflows."""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from agentic_devtools.cli.checks.smart_module_tests import _MODULE_SPECS

REPO_ROOT = Path(__file__).resolve().parents[2]
PR_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "pr-smart-module-tests.yml"
FULL_SUITE_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "post-merge-full-suite.yml"


def _load_workflow(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _step(workflow: dict[str, Any], job_id: str, name: str) -> dict[str, Any]:
    return next(step for step in workflow["jobs"][job_id]["steps"] if step.get("name") == name)


def test_pr_smart_module_workflow_preserves_job_names_and_event_gate() -> None:
    workflow = _load_workflow(PR_WORKFLOW)
    jobs = workflow["jobs"]

    assert {job_id: job["name"] for job_id, job in jobs.items()} == {
        "smart-module-tests": "Run Smart Module Tests",
        "upload-coverage-python": "Upload Python Coverage",
        "smart-module-tests-gate": "Smart Module Tests ✅",
    }
    event_gate = jobs["smart-module-tests"]["if"]
    assert "github.event.pull_request.base.ref == 'main'" in event_gate
    assert "github.event_name == 'pull_request'" in event_gate
    assert "github.event_name == 'pull_request_review'" in event_gate
    assert "github.event.review.state == 'approved'" in event_gate
    assert "copilot-pull-request-reviewer[bot]" in event_gate
    assert "AMARSNIK_swica" in event_gate
    assert jobs["smart-module-tests-gate"]["if"] == "always()"


def test_pr_smart_module_workflow_routes_matching_flags_to_the_runner() -> None:
    workflow = _load_workflow(PR_WORKFLOW)
    steps = workflow["jobs"]["smart-module-tests"]["steps"]
    filter_step = next(step for step in steps if step.get("id") == "filter")
    flags_step = _step(workflow, "smart-module-tests", "Run scoped tests with per-module coverage")
    workflow_filter = yaml.safe_load(filter_step["with"]["filters"])["workflow_contract"]

    flags = json.loads(flags_step["env"]["AGDT_SMART_MODULE_FLAGS"])
    path_filters = yaml.safe_load(filter_step["with"]["filters"])
    assert set(flags) == set(_MODULE_SPECS)
    assert set(flags) <= set(path_filters)
    assert {"config", "e2e_smoke", "skill_classification"} <= set(path_filters) - set(flags)
    assert {
        ".github/workflows/pr-smart-module-tests.yml",
        ".github/workflows/post-merge-full-suite.yml",
        "tests/workflows/test_smart_module_ci_contract.py",
        "tests/workflows/test_windows_specific_fixture_bytes.py",
    } <= set(workflow_filter)
    assert "steps.has-modules.outputs.result == 'true' && steps.filter.outputs.config != 'true'" in flags_step["if"]
    assert flags_step["run"].strip() == "python -m agentic_devtools.cli.checks.smart_module_tests"


def test_pr_smart_module_workflow_preserves_full_suite_and_skill_gates() -> None:
    workflow = _load_workflow(PR_WORKFLOW)
    config_step = _step(workflow, "smart-module-tests", "Run full test suite (config changed)")
    skill_step = _step(workflow, "smart-module-tests", "Run skill classification tests")

    assert "steps.filter.outputs.config == 'true'" in config_step["if"]
    assert "pytest -n auto --dist=worksteal" in config_step["run"]
    assert config_step["env"]["COVERAGE_CORE"] == "sysmon"

    assert (
        skill_step["if"]
        == "steps.filter.outputs.skill_classification == 'true' && steps.has-modules.outputs.result != 'true' "
        "&& steps.filter.outputs.config != 'true' && steps.python-changes.outputs.changed != 'true'"
    )
    assert skill_step["env"]["COVERAGE_CORE"] == "sysmon"
    assert "-n " not in skill_step["run"]
    assert "--dist=" not in skill_step["run"]


def test_pr_smart_module_workflow_preserves_other_gate_conditions_and_fork_safety() -> None:
    workflow = _load_workflow(PR_WORKFLOW)
    e2e_step = _step(workflow, "smart-module-tests", "Run E2E smoke tests")
    workflows_step = _step(workflow, "smart-module-tests", "Run workflow integration tests")
    contract_step = _step(workflow, "smart-module-tests", "Validate CI workflow contract")
    setup_python = _step(workflow, "smart-module-tests", "Set up Python")
    install_dependencies = _step(workflow, "smart-module-tests", "Install dependencies")
    coverage_check = _step(workflow, "smart-module-tests", "Check coverage report exists")
    artifact = _step(workflow, "smart-module-tests", "Upload coverage artifact")
    no_modules_step = _step(workflow, "smart-module-tests", "No modules changed")

    assert e2e_step["if"] == "steps.filter.outputs.e2e_smoke == 'true'"
    assert "steps.filter.outputs.workflows == 'true'" in workflows_step["if"]
    assert contract_step["if"] == "steps.filter.outputs.workflow_contract == 'true'"
    assert contract_step["run"].strip() == (
        'python -m pytest tests/workflows/test_smart_module_ci_contract.py -v --override-ini="addopts="'
    )
    assert "steps.filter.outputs.workflow_contract == 'true'" in setup_python["if"]
    assert "steps.filter.outputs.workflow_contract == 'true'" in install_dependencies["if"]
    assert "steps.filter.outputs.workflow_contract != 'true'" in no_modules_step["if"]
    assert coverage_check["if"] == "always()"
    assert (
        artifact["if"] == "steps.coverage_check.outputs.exists == 'true' && "
        "github.event.pull_request.head.repo.full_name == github.repository"
    )
    assert workflow["jobs"]["upload-coverage-python"]["if"] == (
        "${{ !cancelled() && github.event_name == 'pull_request' && "
        "needs.smart-module-tests.result == 'success' && "
        "needs.smart-module-tests.outputs.coverage_generated == 'true' && "
        "github.event.pull_request.head.repo.full_name == github.repository }}"
    )


def _condition_matches(step: dict[str, Any], outputs: dict[str, str]) -> bool:
    condition = re.sub(
        r"steps\.([\w-]+)\.outputs\.(\w+)",
        lambda match: f"'{outputs.get(f'{match[1]}.{match[2]}', 'false')}'",
        step["if"],
    )
    return subprocess.run(["bash", "-c", f"[[ {condition} ]]"], shell=False).returncode == 0


def _detect_python_changes(tmp_path: Path, paths: list[str]) -> dict[str, str]:
    workflow = _load_workflow(PR_WORKFLOW)
    step = _step(workflow, "smart-module-tests", "Detect changed Python files")
    assert step["env"]["BASE_SHA"] == "${{ github.event.pull_request.base.sha }}"
    assert step["env"]["HEAD_SHA"] == "${{ github.event.pull_request.head.sha }}"

    def git(*args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=tmp_path, text=True, shell=False).strip()

    git("init", "-q")
    git("config", "user.email", "test@example.invalid")
    git("config", "user.name", "Workflow contract test")
    git("commit", "--allow-empty", "-qm", "base")
    base = git("rev-parse", "HEAD")
    for name in paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# changed\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-qm", "changed paths")
    output = tmp_path / "github-output"
    result = subprocess.run(
        ["bash", "-e", "-c", step["run"]],
        cwd=tmp_path,
        env={**os.environ, "BASE_SHA": base, "HEAD_SHA": git("rev-parse", "HEAD"), "GITHUB_OUTPUT": str(output)},
        capture_output=True,
        text=True,
        shell=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return {
        f"{step['id']}.{key}": value for key, value in (line.split("=") for line in output.read_text().splitlines())
    }


@pytest.mark.parametrize(
    "package",
    [
        "adapters",
        "ai_providers",
        "context",
        "epic_tree",
        "mcp",
        "models",
        "prompts",
        "resources",
        "schemas",
        "segments",
        "cli",
        "cli/ci",
        "cli/analysis",
        "cli/audit",
        "cli/checks",
        "cli/config",
        "cli/observability",
        "cli/phase0_review",
        "cli/segments",
        "cli/setup",
        "cli/shared",
        "future_package",
    ],
)
@pytest.mark.parametrize("mapped_also_changed", [False, True], ids=["unmapped", "mixed-mapped-unmapped"])
def test_changed_python_audit_gaps_require_full_suite(tmp_path: Path, package: str, mapped_also_changed: bool) -> None:
    paths = [f"agentic_devtools/{package}/unmapped.py"]
    if mapped_also_changed:
        paths.append("agentic_devtools/cli/git/core.py")
    outputs = _detect_python_changes(tmp_path, paths)
    outputs["has-modules.result"] = str(mapped_also_changed).lower()
    workflow = _load_workflow(PR_WORKFLOW)
    assert _condition_matches(_step(workflow, "smart-module-tests", "Run full test suite (config changed)"), outputs)
    for name in ("Run scoped tests with per-module coverage", "No modules changed"):
        assert not _condition_matches(_step(workflow, "smart-module-tests", name), outputs)
    for name in ("Set up Python", "Install dependencies"):
        assert _condition_matches(_step(workflow, "smart-module-tests", name), outputs)


@pytest.mark.parametrize("path", ["tests/unmapped/test_future.py", "tests/workflows/test_future.py"])
def test_changed_python_zero_selected_tests_falls_back_to_full_suite(tmp_path: Path, path: str) -> None:
    outputs = _detect_python_changes(tmp_path, [path])
    workflow = _load_workflow(PR_WORKFLOW)
    for selected in ("false", "true"):
        outputs["has-modules.result"] = selected
        assert _condition_matches(
            _step(workflow, "smart-module-tests", "Run full test suite (config changed)"), outputs
        )
        assert not _condition_matches(_step(workflow, "smart-module-tests", "No modules changed"), outputs)
        assert not _condition_matches(
            _step(workflow, "smart-module-tests", "Run scoped tests with per-module coverage"), outputs
        )
        assert _condition_matches(_step(workflow, "smart-module-tests", "Run workflow integration tests"), outputs)


def test_skill_only_python_changes_preserve_full_suite_coverage(tmp_path: Path) -> None:
    outputs = _detect_python_changes(tmp_path, ["agentic_devtools/cli/checks/skill_classification.py"])
    outputs.update(
        {
            "filter.skill_classification": "true",
            "has-modules.result": "false",
            "filter.config": "false",
        }
    )
    workflow = _load_workflow(PR_WORKFLOW)
    full_suite = _step(workflow, "smart-module-tests", "Run full test suite (config changed)")
    skill_tests = _step(workflow, "smart-module-tests", "Run skill classification tests")

    assert _condition_matches(full_suite, outputs)
    assert not _condition_matches(skill_tests, outputs)
    assert "--cov-report=xml" in full_suite["run"]
    assert "--cov-report=xml" in skill_tests["run"]


def test_non_python_changes_keep_no_module_skip(tmp_path: Path) -> None:
    outputs = _detect_python_changes(tmp_path, ["docs/example.md"])
    workflow = _load_workflow(PR_WORKFLOW)
    assert _condition_matches(_step(workflow, "smart-module-tests", "No modules changed"), outputs)
    assert not _condition_matches(
        _step(workflow, "smart-module-tests", "Run full test suite (config changed)"), outputs
    )


@pytest.mark.parametrize(
    ("report", "succeeds"),
    [
        (None, False),
        ("not XML", False),
        ("<testsuites><testsuite tests='0'/></testsuites>", False),
        ("<testsuite><testcase><skipped/></testcase></testsuite>", False),
        ("<testsuite><testcase><error/></testcase></testsuite>", False),
        ("<testsuites><testsuite><testcase/></testsuite></testsuites>", True),
        ("<testsuite><testcase><skipped/></testcase><testcase/></testsuite>", True),
    ],
    ids=[
        "zero-selection-no-report",
        "invalid-report",
        "zero-executed-full-suite",
        "nonempty-selection-all-skipped",
        "collection-error",
        "executed",
        "executed-and-skipped",
    ],
)
def test_changed_python_requires_actual_full_suite_execution(
    tmp_path: Path, report: str | None, succeeds: bool
) -> None:
    workflow = _load_workflow(PR_WORKFLOW)
    full_suite = _step(workflow, "smart-module-tests", "Run full test suite (config changed)")
    guard = _step(workflow, "smart-module-tests", "Require executed tests for changed Python")
    assert guard["if"] == "always() && steps.python-changes.outputs.changed == 'true'"
    assert full_suite["env"]["TEST_RESULTS"] == guard["env"]["TEST_RESULTS"]
    assert '--junitxml="$TEST_RESULTS"' in full_suite["run"]
    report_path = tmp_path / "results.xml"
    if report is not None:
        report_path.write_text(report, encoding="utf-8")
    result = subprocess.run(
        ["bash", "-e", "-c", guard["run"]],
        env={**os.environ, "TEST_RESULTS": str(report_path)},
        capture_output=True,
        text=True,
        shell=False,
    )
    assert (result.returncode == 0) == succeeds, result.stdout + result.stderr
    if not succeeds:
        assert "::error::" in result.stdout + result.stderr
        assert "full suite" in result.stdout + result.stderr


def test_full_suite_workflow_keeps_coverage_scope_and_upload_gates() -> None:
    workflow = _load_workflow(FULL_SUITE_WORKFLOW)
    run_step = _step(workflow, "full-suite", "Run full pytest with coverage")
    run = run_step["run"]

    assert workflow["jobs"]["full-suite"]["name"] == "Full Test Suite"
    assert "pytest -n auto --dist=worksteal" in run
    assert run_step["env"]["COVERAGE_CORE"] == "sysmon"
    for preserved_argument in (
        "--cov=agentic_devtools",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-fail-under=100",
        "--ignore=tests/workflows",
    ):
        assert preserved_argument in run

    coverage_job = workflow["jobs"]["upload-coverage-python"]
    assert coverage_job["name"] == "Upload Python Coverage"
    assert coverage_job["if"] == "${{ !cancelled() && needs.full-suite.result == 'success' }}"
