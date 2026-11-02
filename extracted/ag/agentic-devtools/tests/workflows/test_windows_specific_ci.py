"""Contract tests for the focused native Windows CI workflow."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Literal

import pytest
import yaml

from agentic_devtools.cli.ci import windows_specific, windows_specific_cli
from agentic_devtools.cli.ci.windows_selector_policy import (
    V2_EXTENSION_EXPANSIONS,
    V2_EXTENSION_SELECTORS,
    validate_candidate_policy,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
WINDOWS_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "pr-windows-specific-tests.yml"
SMART_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "pr-smart-module-tests.yml"


def _load_workflow(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _steps(workflow: dict[str, Any], job_id: str) -> list[dict[str, Any]]:
    return workflow["jobs"][job_id]["steps"]


def _step(workflow: dict[str, Any], job_id: str, name: str) -> dict[str, Any]:
    return next(step for step in _steps(workflow, job_id) if step.get("name") == name)


def _trigger(workflow: Any) -> dict[str, Any]:
    return workflow.get("on", workflow.get(True, {}))


def _selection(*, groups: tuple[str, ...] = (), contract: bool = False) -> dict[str, object]:
    return {
        "ok": True,
        "product_groups": list(groups),
        "contract_required": contract,
        "windows_required": bool(groups),
        "bootstrap_allowed": False,
    }


def test_windows_workflow_is_a_least_privilege_stable_pull_request_check() -> None:
    workflow = _load_workflow(WINDOWS_WORKFLOW)
    trigger = _trigger(workflow)

    assert set(trigger) == {"pull_request"}
    assert trigger["pull_request"]["branches"] == ["main"]
    assert "paths" not in trigger["pull_request"]
    assert workflow["permissions"] == {"contents": "read", "pull-requests": "read"}
    assert set(workflow["jobs"]) == {"selection", "linux-contract", "windows-product", "gate"}
    assert workflow["jobs"]["gate"]["name"] == "Windows-Specific Tests"
    assert workflow["jobs"]["gate"]["if"] == "always()"
    assert set(workflow["jobs"]["gate"]["needs"]) == {"selection", "linux-contract", "windows-product"}
    assert "contract_required" in workflow["jobs"]["linux-contract"]["if"]
    assert "windows_required" in workflow["jobs"]["windows-product"]["if"]
    assert "pull_request_target" not in WINDOWS_WORKFLOW.read_text(encoding="utf-8")
    assert "secrets." not in WINDOWS_WORKFLOW.read_text(encoding="utf-8")
    assert "continue-on-error" not in WINDOWS_WORKFLOW.read_text(encoding="utf-8")


def test_windows_workflow_uses_python_314_and_only_installs_from_base() -> None:
    workflow = _load_workflow(WINDOWS_WORKFLOW)

    for job_id in ("selection", "linux-contract", "windows-product", "gate"):
        setup_python = next(
            step for step in _steps(workflow, job_id) if step.get("uses", "").startswith("actions/setup-python")
        )
        install = _step(workflow, job_id, "Install base package and development dependencies")
        assert setup_python["with"]["python-version"] == "3.14"
        assert install["working-directory"] == "policy"
        assert install["run"] == 'python -m pip install -e ".[dev]"'

    assert "pip install" not in WINDOWS_WORKFLOW.read_text(encoding="utf-8").replace(
        'python -m pip install -e ".[dev]"', ""
    )
    assert "PYTHONPATH:" not in WINDOWS_WORKFLOW.read_text(encoding="utf-8")
    assert "--bootstrap" not in WINDOWS_WORKFLOW.read_text(encoding="utf-8")


def test_windows_workflow_checks_out_exact_head_and_base_in_separate_roots() -> None:
    workflow = _load_workflow(WINDOWS_WORKFLOW)

    for job_id in ("selection", "linux-contract", "windows-product"):
        if job_id != "linux-contract":
            assert workflow["jobs"][job_id]["env"]["WINDOWS_CI_HEAD_ROOT"] == "${{ github.workspace }}/head"
        head = _step(workflow, job_id, "Checkout exact PR head")["with"]
        base = _step(workflow, job_id, "Checkout exact base policy")["with"]
        assert head["repository"] == "${{ github.event.pull_request.head.repo.full_name }}"
        assert head["ref"] == "${{ github.event.pull_request.head.sha }}"
        assert head["path"] == "head"
        assert head["persist-credentials"] is False
        assert base["ref"] == "${{ github.event.pull_request.base.sha }}"
        assert base["path"] == "policy"
        assert base["persist-credentials"] is False

    gate_base = _step(workflow, "gate", "Checkout exact base policy")["with"]
    assert gate_base["ref"] == "${{ github.event.pull_request.base.sha }}"
    assert gate_base["path"] == "policy"
    assert not any(step.get("name") == "Checkout exact PR head" for step in _steps(workflow, "gate"))


def test_selection_uses_json_changed_paths_and_preserves_errors_and_status(tmp_path: Path) -> None:
    workflow = _load_workflow(WINDOWS_WORKFLOW)
    selection_job = workflow["jobs"]["selection"]
    filter_step = _step(workflow, "selection", "Detect changed paths")
    filter_definition = yaml.safe_load(filter_step["with"]["filters"])
    select_step = _step(workflow, "selection", "Select applicable tests")
    run = select_step["run"]

    assert filter_step["uses"] == "dorny/paths-filter@v3"
    assert filter_step["with"]["list-files"] == "json"
    assert filter_definition == {"all": ["**"]}
    assert select_step["if"] == "always()"
    assert select_step["env"]["CHANGED_PATHS_JSON"] == "${{ steps.filter.outputs.all_files }}"
    assert select_step["env"]["FILTER_OUTCOME"] == "${{ steps.filter.outcome }}"
    assert "changed_paths_failed" in run
    assert '"--changed-paths-json",' in run
    assert '"--manifest",' in run
    assert '"--head-policy",' in run
    assert 'workspace / "head" / ".github" / "windows-specific-tests.json"' in run
    assert 'workspace / "head" / "agentic_devtools" / "cli" / "ci" / "windows_specific.py"' in run
    assert 'if not selection_json.endswith("\\n")' in run
    assert selection_job["outputs"]["selection_json"] == "${{ steps.select.outputs.selection_json }}"
    assert selection_job["outputs"]["select_status"] == "${{ steps.select.outputs.select_status }}"

    workspace = tmp_path
    (workspace / "head").symlink_to(REPO_ROOT, target_is_directory=True)
    policy = Path(os.environ.get("WINDOWS_CI_POLICY_ROOT", REPO_ROOT)).resolve()
    for outcome, changed_paths, expected_status in (("failure", "", 1), ("success", "[]", 0)):
        output = tmp_path / f"{outcome}.output"
        result = subprocess.run(
            ["bash", "-e", "-c", run],
            cwd=policy,
            env={
                **os.environ,
                "FILTER_OUTCOME": outcome,
                "CHANGED_PATHS_JSON": changed_paths,
                "GITHUB_WORKSPACE": str(workspace),
                "WINDOWS_CI_BASE_POLICY": str(policy / "agentic_devtools/cli/ci/windows_specific.py"),
                "WINDOWS_CI_POLICY_ROOT": str(policy),
                "GITHUB_OUTPUT": str(output),
            },
            capture_output=True,
            text=True,
            shell=False,
        )
        lines = output.read_text(encoding="utf-8").splitlines()
        delimiter = lines[0].partition("<<")[2]
        assert lines[0] == f"selection_json<<{delimiter}"
        assert lines[-2] == delimiter
        selection = json.loads("\n".join(lines[1:-2]))
        assert selection["ok"] is (expected_status == 0)
        if expected_status:
            assert selection == {"ok": False, "error_code": "changed_paths_failed"}
        assert result.returncode == expected_status
        assert lines[-1] == f"select_status={expected_status}"


def test_cli_invocations_verify_base_module_origin_and_use_policy_cwd() -> None:
    workflow = _load_workflow(WINDOWS_WORKFLOW)
    for job_id, step_names in (
        ("selection", ("Select applicable tests",)),
        ("windows-product", ("Verify benchmark fixture bytes", "Run focused Windows tests")),
        ("gate", ("Evaluate Windows-specific test gate",)),
    ):
        for name in step_names:
            run = _step(workflow, job_id, name)["run"]
            assert "agentic_devtools.cli.ci.windows_specific as selector" in run
            assert "agentic_devtools.cli.ci.windows_specific_cli as dispatcher" in run
            assert "module.__file__" in run
            assert "is_relative_to(policy)" in run
            assert 'env.pop("PYTHONPATH", None)' in run
            assert "cwd=policy" in run
            assert '"-m",' in run
            assert '"agentic_devtools.cli.ci.windows_specific",' in run

    for job_id in ("selection", "linux-contract", "windows-product", "gate"):
        assert (
            workflow["jobs"][job_id]["env"]["WINDOWS_CI_BASE_POLICY"]
            == "${{ github.workspace }}/policy/agentic_devtools/cli/ci/windows_specific.py"
        )

    linux_contract = _step(workflow, "linux-contract", "Run workflow contract tests")
    assert linux_contract["working-directory"] == "policy"
    assert "${{ github.workspace }}/head/tests/workflows/test_windows_specific_ci.py" in linux_contract["run"]
    assert "--import-mode=importlib" in linux_contract["run"]
    trusted_origin = _step(workflow, "linux-contract", "Verify trusted package origin")["run"]
    assert "windows_specific as selector" in trusted_origin
    assert "windows_specific_cli as dispatcher" in trusted_origin
    assert "module.__file__" in trusted_origin
    assert "is_relative_to(policy)" in trusted_origin


def test_workflow_contract_import_resolves_inside_trusted_policy() -> None:
    policy = Path(os.environ.get("WINDOWS_CI_POLICY_ROOT", REPO_ROOT)).resolve()

    assert Path(windows_specific.__file__).resolve().is_relative_to(policy)
    assert Path(windows_specific_cli.__file__).resolve().is_relative_to(policy)


def test_windows_job_orders_autocrlf_audit_and_test_execution() -> None:
    workflow = _load_workflow(WINDOWS_WORKFLOW)
    job = workflow["jobs"]["windows-product"]
    steps = job["steps"]
    names = [step.get("name") for step in steps]
    set_index = names.index("Set global autocrlf")
    head_index = names.index("Checkout exact PR head")
    autocrlf_index = names.index("Verify effective autocrlf")
    audit_index = names.index("Verify benchmark fixture bytes")
    run_index = names.index("Run focused Windows tests")
    audit = steps[audit_index]
    run = steps[run_index]["run"]

    assert job["runs-on"] == "windows-latest"
    assert job["timeout-minutes"] == 30
    assert set_index < head_index < autocrlf_index < audit_index < run_index < len(names) - 2
    assert names[-2].startswith("Run candidate-head") and names[-1].startswith("Measure candidate-head")
    assert steps[set_index]["run"] == "git config --global core.autocrlf true"
    assert steps[autocrlf_index]["shell"] == "bash"
    assert audit["shell"] == "bash"
    assert steps[run_index]["shell"] == "bash"
    assert "config --get core.autocrlf" in steps[autocrlf_index]["run"]
    assert "benchmark" in audit["if"]
    assert "verify-fixtures" in audit["run"]
    assert '"--root",' in audit["run"] or '"--root",' in run
    assert "WINDOWS_CI_HEAD_ROOT" in audit["run"]
    assert "WINDOWS_CI_HEAD_ROOT" in run
    assert "WINDOWS_CI_JUNIT" in run
    assert '"--commit",' in audit["run"]
    assert 'os.environ["HEAD_SHA"]' in audit["run"]
    assert 'os.environ["WINDOWS_CI_HEAD_ROOT"]' in audit["run"]
    assert '"--selection-json",' in run
    assert '"--manifest",' in run
    assert '"--head-policy",' in run
    assert '"--root",' in run
    assert 'os.environ["WINDOWS_CI_HEAD_ROOT"]' in run
    assert all(
        "runner." not in str(value)
        for job_data in workflow["jobs"].values()
        for value in job_data.get("env", {}).values()
    )
    assert "WINDOWS_CI_JUNIT" not in job["env"]
    assert "${{ runner.temp }}/windows-specific-junit.xml" == steps[run_index]["env"]["WINDOWS_CI_JUNIT"]
    assert all(step["working-directory"] == "head" and step["shell"] == "pwsh" for step in steps[-2:])
    assert "--cov=agentic_devtools.cli.ci.windows_process_tree" in steps[-1]["run"]
    assert "--cov-fail-under=100" in steps[-1]["run"]


def test_gate_passes_actual_same_workflow_dependency_results() -> None:
    workflow = _load_workflow(WINDOWS_WORKFLOW)
    gate = workflow["jobs"]["gate"]

    assert gate["env"]["SELECTION_JSON"] == "${{ needs.selection.outputs.selection_json }}"
    assert gate["env"]["LINUX_RESULT"] == "${{ needs.linux-contract.result }}"
    assert gate["env"]["WINDOWS_RESULT"] == "${{ needs.windows-product.result }}"
    run = _step(workflow, "gate", "Evaluate Windows-specific test gate")["run"]
    assert '"--selection-json",' in run
    assert '"--linux-result",' in run
    assert '"--windows-result",' in run


def test_smart_module_workflow_routes_windows_contract_and_unit_changes() -> None:
    workflow = _load_workflow(SMART_WORKFLOW)
    filters = yaml.safe_load(_step(workflow, "smart-module-tests", "Detect changed modules")["with"]["filters"])
    contract = set(filters["workflow_contract"])
    ci = set(filters["ci"])
    contract_step = _step(workflow, "smart-module-tests", "Validate CI workflow contract")

    assert {
        ".github/workflows/pr-windows-specific-tests.yml",
        ".github/windows-specific-tests.json",
        "tests/workflows/test_windows_specific_ci.py",
    } <= contract
    for module in ("windows_specific.py", "windows_specific_cli.py", "windows_fixture_bytes.py"):
        assert f"agentic_devtools/cli/ci/{module}" in contract
        assert f"agentic_devtools/cli/ci/{module}" in ci
    assert "tests/unit/cli/ci/windows_specific/**" in ci
    assert "tests/unit/cli/ci/windows_specific_cli/**" in ci
    assert "tests/unit/cli/ci/windows_fixture_bytes/**" in ci
    assert "tests/unit/cli/ci/windows_specific/**" in contract
    assert "tests/unit/cli/ci/windows_specific_cli/**" in contract
    assert "tests/unit/cli/ci/windows_fixture_bytes/**" in contract
    windows_contract_step = _step(workflow, "smart-module-tests", "Validate Windows-specific workflow contract")
    assert "tests/workflows/test_smart_module_ci_contract.py" in contract_step["run"]
    assert "tests/workflows/test_windows_specific_ci.py" in windows_contract_step["run"]
    assert _step(workflow, "smart-module-tests", "Run full test suite (config changed)")["if"]


def test_workflow_guide_documents_the_residual_trust_and_receipt_limits() -> None:
    guide = " ".join((REPO_ROOT / ".github" / "workflows" / "README.md").read_text(encoding="utf-8").split())

    for required_text in (
        "workflow YAML and setup steps remain",
        "PR-controlled and could deviate from the prescribed trust boundary",
        "plugins, `conftest.py`, process outcomes, and JUnit contents are also PR-controlled",
        "does not authenticate the workflow or",
        "does not expand the broader native-hold coverage or clear the separate `#4542` holds",
        "receipt tied to the refreshed exact PR-head SHA",
        "a missing receipt preserves the existing hold",
    ):
        assert required_text in guide


@pytest.mark.parametrize(
    ("paths", "groups", "contract_required"),
    [
        (["agentic_devtools/cli/setup/dependency_checker.py"], {"setup-check"}, False),
        (
            ["agentic_devtools/cli/audit/instruction_resolver.py"],
            {"portability"},
            False,
        ),
        ([".gitattributes"], {"benchmark"}, False),
        (["pyproject.toml"], {"setup-check", "portability", "benchmark"}, True),
        (
            [".github/workflows/pr-windows-specific-tests.yml", "tests/workflows/test_windows_specific_ci.py"],
            set(),
            True,
        ),
        (["docs/windows-ci.md"], set(), False),
        ([], set(), False),
    ],
)
def test_production_selector_routes_exact_paths(paths: list[str], groups: set[str], contract_required: bool) -> None:
    selected, requires_contract = windows_specific.select_groups(paths)

    assert selected == groups
    assert requires_contract is contract_required


def test_frozen_v1_and_registered_v2_cohorts_preserve_setup_cases() -> None:
    v1_selectors = getattr(windows_specific, "_FROZEN_V1_SELECTORS", windows_specific.EXPECTED_SELECTORS)
    v1_expansions = getattr(windows_specific, "_FROZEN_V1_EXPANSIONS", windows_specific.EXPECTED_EXPANSIONS)
    v1_policy = windows_specific.SelectorPolicy(v1_selectors, tuple(v1_expansions.items()))
    v1_expansion_map = dict(v1_policy.expansions)

    assert len(v1_policy.selectors) == 15
    assert sum(len(v1_expansion_map.get(selector, ("",))) for selector in v1_policy.selectors) == 21
    assert sum(len(v1_expansion_map.get(selector, ("",))) for selector in v1_policy.selectors[:2]) == 8

    source = (REPO_ROOT / "agentic_devtools" / "cli" / "ci" / "windows_specific.py").read_text(encoding="utf-8")
    manifest = (REPO_ROOT / ".github" / "windows-specific-tests.json").read_text(encoding="utf-8")
    v2_policy = validate_candidate_policy(source, manifest, v1_selectors, v1_expansions)

    assert v2_policy.selectors == (*v1_policy.selectors[:-1], *V2_EXTENSION_SELECTORS, v1_policy.selectors[-1])
    assert v2_policy.expansions == (*v1_policy.expansions, *V2_EXTENSION_EXPANSIONS)
    assert len(v2_policy.selectors) == 19
    assert len(v2_policy.selectors) - len(v2_policy.expansions) + sum(len(ids) for _, ids in v2_policy.expansions) == 26
    assert sum(len(dict(v2_policy.expansions).get(selector, ("",))) for selector in v2_policy.selectors[:2]) == 8


def test_production_selection_reports_changed_path_failures(capsys: pytest.CaptureFixture[str]) -> None:
    result = windows_specific.main(
        [
            "select",
            "--changed-paths-json",
            "{",
            "--manifest",
            str(REPO_ROOT / ".github" / "windows-specific-tests.json"),
            "--head-policy",
            str(REPO_ROOT / "agentic_devtools" / "cli" / "ci" / "windows_specific.py"),
        ]
    )

    assert result != 0
    assert json.loads(capsys.readouterr().out) == {"ok": False, "error_code": "changed_paths_failed"}


@pytest.mark.parametrize(
    ("selection", "linux", "windows", "expected"),
    [
        (_selection(), "skipped", "skipped", "not-applicable"),
        (_selection(contract=True), "success", "skipped", "not-applicable"),
        *[
            (_selection(contract=True), result, "skipped", "required_evidence_missing")
            for result in ("failure", "cancelled", "skipped", None)
        ],
        (_selection(groups=("setup-check",)), "skipped", "success", "native-evidence"),
        (_selection(groups=("setup-check",), contract=True), "success", "success", "native-evidence"),
        *[
            (_selection(groups=("setup-check",)), "success", result, "required_evidence_missing")
            for result in ("failure", "cancelled", "skipped", None)
        ],
        *[
            (_selection(groups=("setup-check",)), result, "success", "required_evidence_missing")
            for result in ("failure", "cancelled")
        ],
        ({"ok": False, "error_code": "changed_paths_failed"}, "skipped", "skipped", "changed_paths_failed"),
    ],
)
def test_production_gate_rejects_missing_failed_skipped_and_cancelled_evidence(
    selection: dict[str, object],
    linux: Literal["success", "failure", "cancelled", "skipped"] | None,
    windows: Literal["success", "failure", "cancelled", "skipped"] | None,
    expected: str,
) -> None:
    result = windows_specific.evaluate_gate(selection, linux, windows)

    if expected in {"native-evidence", "not-applicable"}:
        assert result == {"ok": True, "classification": expected}
    else:
        assert result == {"ok": False, "error_code": expected}


def test_product_pytest_subprocess_uses_head_as_cwd_and_import_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    head = tmp_path / "head"
    head.mkdir()
    junit = tmp_path / "windows-specific-junit.xml"
    policy = windows_specific.SelectorPolicy(
        windows_specific.EXPECTED_SELECTORS,
        tuple(windows_specific.EXPECTED_EXPANSIONS.items()),
    )
    expansion_map = dict(policy.expansions)
    selected_ids = [
        f"{selector}[{parameter}]" if selector in expansion_map else selector
        for selector in policy.selectors[:2]
        for parameter in expansion_map.get(selector, ("",))
    ]
    collection = "\n".join([*selected_ids, f"{len(selected_ids)} tests collected", ""])
    calls: list[tuple[list[str], dict[str, Any]]] = []

    def run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs))
        if len(calls) == 1:
            return subprocess.CompletedProcess(command, 0, stdout=collection, stderr="")
        raise RuntimeError("stop after checking both subprocess invocations")

    monkeypatch.delenv("PYTHONPATH", raising=False)
    monkeypatch.setattr(windows_specific.subprocess, "run", run)
    with pytest.raises(RuntimeError, match="stop after checking"):
        windows_specific.run_selected_tests(
            head,
            policy,
            {"setup-check"},
            junit_path=junit,
        )

    assert len(calls) == 2
    for command, kwargs in calls:
        assert command[:3] == [sys.executable, "-m", "pytest"]
        assert Path(kwargs["cwd"]) == head.resolve()
        assert kwargs["env"].get("PYTHONPATH") is None
    assert "--collect-only" in calls[0][0]
    assert f"--junitxml={junit}" in calls[1][0]
