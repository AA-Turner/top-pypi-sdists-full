"""Contracts for the SpecKit normalizer and read-only Copilot completion route."""

import json
import subprocess
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "speckit-agent-pr-normalizer.yml"
HELPER = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "assess-copilot-completion.js"
ASSESSMENT_TEST = REPO_ROOT / ".github" / "scripts" / "speckit-trigger" / "tests" / "test_assess_copilot_completion.js"

EXPECTED_RESULTS = {
    ("verified_empty", "verified_no_delivery"),
    ("unknown", "assessment_adapter_unavailable"),
    ("unknown", "delivery_evidence_unknown"),
    ("unknown", "delivery_evidence_incomplete"),
    ("unknown", "delivery_evidence_malformed"),
    ("unknown", "delivery_not_admitted"),
    ("not_admitted", "workflow_not_success"),
    ("not_admitted", "pr_missing"),
    ("not_admitted", "pr_ambiguous"),
    ("not_admitted", "cross_repository"),
    ("not_admitted", "stale_head"),
    ("not_admitted", "pr_lookup_unavailable"),
}


def _load_workflow() -> dict:
    return yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def _load_assessment_result_pairs() -> set[tuple[str, str]]:
    result = subprocess.run(  # noqa: S603
        [
            "node",
            "-e",
            "const helper = require(process.argv[1]); process.stdout.write(JSON.stringify(helper.ASSESSMENT_RESULTS));",
            str(HELPER),
        ],
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )
    return {tuple(pair) for pair in json.loads(result.stdout)}


def test_completion_assessment_behavioral_suite() -> None:
    result = subprocess.run(  # noqa: S603
        ["node", str(ASSESSMENT_TEST)],
        check=True,
        capture_output=True,
        text=True,
        shell=False,
    )

    assert "All Copilot completion assessment tests passed." in result.stdout


def test_completion_trigger_is_separate_and_exactly_filtered() -> None:
    workflow = _load_workflow()
    events = workflow["on"]

    assert events["pull_request"]["types"] == ["opened", "synchronize", "ready_for_review", "edited", "labeled"]
    assert events["workflow_run"] == {
        "workflows": ["Copilot cloud agent"],
        "types": ["completed"],
    }
    jobs = workflow["jobs"]
    assert "normalize" in jobs
    assert "assess-copilot-completion" in jobs
    assert "completion-summary" in jobs
    assert "github.event_name == 'workflow_run'" in jobs["assess-copilot-completion"]["if"]
    assert "github.event.workflow_run.name == 'Running Copilot cloud agent'" in jobs["assess-copilot-completion"]["if"]
    assert (
        "github.event.workflow_run.path == 'dynamic/copilot-swe-agent/copilot'"
        in jobs["assess-copilot-completion"]["if"]
    )


def test_assessment_job_checks_out_only_trusted_default_branch_with_read_permissions() -> None:
    workflow = _load_workflow()
    job = workflow["jobs"]["assess-copilot-completion"]
    assert job["permissions"] == {"contents": "read", "pull-requests": "read"}

    checkout = next(step for step in job["steps"] if step.get("uses") == "actions/checkout@v4")
    assert checkout["with"]["ref"] == "${{ github.event.repository.default_branch }}"
    assert checkout["with"]["persist-credentials"] == "false"
    assert all("workflow_run.head_sha" not in str(step.get("with", {}).get("ref", "")) for step in job["steps"])
    assert all("pull_request.head" not in str(step) for step in job["steps"])
    assert all("download-artifact" not in str(step.get("uses", "")) for step in job["steps"])
    assert [step["run"] for step in job["steps"] if "run" in step] == ["python -m pip install ."]
    setup = next(step for step in job["steps"] if step.get("uses") == "actions/setup-python@v5")
    assert setup["with"] == {"python-version": "3.14"}
    assessment_step = next(step for step in job["steps"] if step.get("id") == "assessment")
    assert assessment_step["env"] == {"GH_TOKEN": "${{ github.token }}"}
    assert all("env" not in step for step in job["steps"] if step != assessment_step)
    assert job["steps"].index(checkout) < job["steps"].index(setup) < job["steps"].index(assessment_step)
    install = next(step for step in job["steps"] if "run" in step)
    assert job["steps"].index(setup) < job["steps"].index(install) < job["steps"].index(assessment_step)
    script = "\n".join(str(step.get("with", {}).get("script", "")) for step in job["steps"])
    assert "assess-copilot-completion.js" in script
    assert "context.payload.workflow_run" in script
    assert "createPythonDeliveryAdapter" in script
    assert "assessDelivery: createPythonDeliveryAdapter({" in script
    assert "execFile: require('child_process').execFile" in script
    assert "env: process.env" in script
    assert "timeoutMs: 120000" in script
    assert "maxBuffer: 65536" in script
    assert "cwd: process.env.GITHUB_WORKSPACE" in script
    assert "secrets." not in json.dumps(job)
    assert len(job["steps"]) == 4
    assert set(workflow["jobs"]) == {"normalize", "assess-copilot-completion", "completion-summary"}

    summary = workflow["jobs"]["completion-summary"]
    assert summary["permissions"] == {"contents": "read"}
    assert summary["needs"] == ["assess-copilot-completion"]


def test_assessment_outputs_are_bounded_and_summary_only_consumer() -> None:
    workflow = _load_workflow()
    jobs = workflow["jobs"]
    assessment = jobs["assess-copilot-completion"]
    summary = jobs["completion-summary"]
    assert set(assessment["outputs"]) == {"assessment_status", "assessment_reason"}
    assert assessment["outputs"]["assessment_status"] == "${{ steps.assessment.outputs.assessment_status }}"
    assert assessment["outputs"]["assessment_reason"] == "${{ steps.assessment.outputs.assessment_reason }}"
    assert all(
        "pull-requests: write" not in str(job.get("permissions", {}))
        and "contents: write" not in str(job.get("permissions", {}))
        for name, job in jobs.items()
        if name != "normalize"
    )

    output_references = [
        name for name, job in jobs.items() if "needs.assess-copilot-completion.outputs.assessment_" in json.dumps(job)
    ]
    assert output_references == ["completion-summary"]
    summary_script = "\n".join(str(step.get("with", {}).get("script", "")) for step in summary["steps"])
    summary_env = summary["steps"][0]["env"]
    assert "core.summary" in summary_script
    assert "process.env.ASSESSMENT_STATUS" in summary_script
    assert "process.env.ASSESSMENT_REASON" in summary_script
    assert "ASSESSMENT_STATUS" in summary_env
    assert "ASSESSMENT_REASON" in summary_env
    assert all(step.get("uses") == "actions/github-script@v7" for step in summary["steps"])

    assessment_script = next(step for step in assessment["steps"] if step.get("id") == "assessment")["with"]["script"]
    assert "await assessCompletion({" in assessment_script
    assert "core," in assessment_script
    assert "None retained" not in json.dumps(workflow), "sentinel handling stays inside the correlated helper"
    assert "deliveryEvidence" not in json.dumps(workflow), "internal evidence is not transported"
    assert "assess-copilot-completion.js" not in summary_script
    assert "github.rest" not in summary_script, "the separate summary must not correlate or mutate PRs"


def test_helper_keeps_correlation_fail_closed_and_reason_mapping_exact() -> None:
    workflow = _load_workflow()
    normalizer_if = workflow["jobs"]["normalize"]["if"]
    assert "github.event.pull_request.user.login == 'copilot-swe-agent[bot]'" in normalizer_if
    assert "github.event.workflow_run" not in normalizer_if
    assert normalizer_if.count("||") == 7
    assert all(
        value in normalizer_if
        for value in (
            "contains(github.event.pull_request.labels.*.name, 'speckit:spec')",
            "contains(github.event.pull_request.body || '', "
            "'speckit:agent-assigned schema_version=1 engine=cloud-agent')",
            "contains(github.event.pull_request.labels.*.name, 'speckit:phase-1')",
            "contains(github.event.pull_request.labels.*.name, 'speckit:phase-2')",
            "contains(github.event.pull_request.labels.*.name, 'speckit:phase-3')",
            "contains(github.event.pull_request.labels.*.name, 'speckit:phase-4')",
            "contains(github.event.pull_request.labels.*.name, 'speckit:phase-5')",
        )
    )

    assert _load_assessment_result_pairs() == EXPECTED_RESULTS
    helper = HELPER.read_text(encoding="utf-8")
    assert "github.rest.repos.listPullRequestsAssociatedWithCommit" in helper
    assert "github.rest.pulls.get" in helper
    assert "MAX_ASSOCIATED_PR_PAGES" in helper
    assert "headSha" in helper and "stale_head" in helper
    assert "pr_ambiguous" in helper and "cross_repository" in helper
    assert "github.rest.pulls.update" not in helper
    assert "github.rest.issues.createComment" not in helper
