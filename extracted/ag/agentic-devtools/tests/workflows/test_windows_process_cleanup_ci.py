from pathlib import Path

import yaml


def test_native_candidate_head_checks_include_process_cleanup_module() -> None:
    workflow_path = Path(__file__).parents[2] / ".github" / "workflows" / "pr-windows-specific-tests.yml"
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    steps = workflow["jobs"]["windows-product"]["steps"]
    test_step, coverage_step = steps[-2:]

    assert "tests/unit/cli/ci/windows_process_cleanup" in test_step["run"]
    assert "tests/unit/cli/ci/windows_process_cleanup" in coverage_step["run"]
    assert "--cov=agentic_devtools.cli.ci.windows_process_cleanup" in coverage_step["run"]
    assert "--cov-branch" in coverage_step["run"]
