"""Build and post recovery guidance for failed SpecKit phase progressions."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def build_failure_comment(
    *,
    phase: str,
    phase_name: str,
    repo: str,
    run_id: str,
    gate_result: str,
    critical_findings: str,
    artifact_gate_result: str,
    artifact_gate_violations: str,
    created_pr_number: str,
    created_pr_url: str,
    label_setup_status: str,
    hierarchy_level: str,
    task_restart_guard_failed: bool = False,
    hierarchy_reason: str = "",
) -> str:
    """Render the issue comment describing the failure and safe recovery path."""
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"
    phase_number = int(phase or 0)
    critical_gate_failed = gate_result == "fail"
    artifact_gate_failed = artifact_gate_result == "fail"

    if task_restart_guard_failed and phase_number > 1:
        downgrade_description = (
            f" ({hierarchy_reason})" if hierarchy_reason else (" (verified as having no in-repository parent)")
        )
        return "\n".join(
            [
                f"## ❌ SpecKit: Phase {phase_number} Requires a Fresh Phase 1 Dispatch",
                "",
                (
                    f"The Task is verified as a standalone Feature{downgrade_description}. "
                    "This later-phase request requires a fresh Phase 1 dispatch to establish its own specification."
                ),
                "",
                "Start a fresh Phase 1 dispatch for this issue; do not retry the current later phase.",
                "",
                f"**Workflow Run**: [View logs]({run_url})",
                "",
                "---",
                "",
                f"_This comment was posted by the [SpecKit GitHub Action]({run_url})._",
            ]
        )

    def render_critical_findings() -> str:
        try:
            findings: Any = json.loads(critical_findings)
        except (json.JSONDecodeError, TypeError) as _exc:
            return f"_Could not parse findings: {critical_findings}_"
        if not isinstance(findings, list):
            return f"_Could not parse findings: {critical_findings}_"
        if not findings:
            return ""

        rows = ["| ID | Summary | Recommendation |", "|---|---|---|"]
        for finding in findings:
            values = finding if isinstance(finding, dict) else {}
            cells = [
                str(values.get("id", "")).replace("\r", " ").replace("\n", " ").replace("|", "\\|"),
                str(values.get("summary", "")).replace("\r", " ").replace("\n", " ").replace("|", "\\|"),
                str(values.get("recommendation", "")).replace("\r", " ").replace("\n", " ").replace("|", "\\|"),
            ]
            rows.append(f"| {' | '.join(cells)} |")
        return "\n".join(rows)

    gate_findings: list[str] = []
    if critical_gate_failed:
        findings_table = render_critical_findings()
        gate_findings.extend(
            [
                "### CRITICAL Gate Findings",
                "",
                findings_table or "_The CRITICAL gate failed; review the workflow logs for the findings._",
            ]
        )
    if artifact_gate_failed:
        gate_findings.extend(
            [
                "### Artifact Gate Violations",
                "",
                artifact_gate_violations
                or "_The artifact verification gate failed; review the workflow logs for details._",
            ]
        )

    if critical_gate_failed and critical_findings != "[]" and not created_pr_number and not created_pr_url:
        findings_table = render_critical_findings()
        return "\n".join(
            [
                "## ❌ SpecKit: CRITICAL Gate Failed",
                "",
                f"**Phase {phase_number}** analysis detected unresolved CRITICAL findings that block PR creation.",
                "",
                "### CRITICAL Findings",
                "",
                findings_table,
                "",
                "### What to Do",
                "",
                "1. Review the CRITICAL findings above and address them in the specification artifacts",
                (
                    "2. Re-trigger the pipeline by removing the `speckit:failed` label and re-adding the "
                    "`speckit` label, or use the **workflow_dispatch** trigger on the [SpecKit Phase "
                    f"Progression workflow](https://github.com/{repo}/actions/workflows/"
                    "speckit-phase-progression.yml)"
                ),
                "",
                f"**Workflow Run**: [View logs]({run_url})",
                "",
                "---",
                "",
                f"_This comment was posted by the [SpecKit CRITICAL Analysis Gate]({run_url})._",
            ]
        )

    if created_pr_number or created_pr_url:
        required_labels = [f"speckit:phase-{phase_number}"]
        if hierarchy_level in {"epic", "feature", "task"}:
            required_labels.append(f"speckit:level-{hierarchy_level}")
        if created_pr_number:
            label_command = (
                f'gh api --method POST "repos/{repo}/issues/{created_pr_number}/labels" \\'
                + "\n"
                + " \\\n".join(f'  --field "labels[]={label}"' for label in required_labels)
            )
        else:
            label_command = (
                "Use the PR URL to determine its number, then apply the required labels with the REST labels API."
            )

        merge_blockers = []
        if label_setup_status == "failed":
            merge_blockers.append("the required routing labels are present")
        if critical_gate_failed:
            merge_blockers.append("the CRITICAL findings are resolved and the analysis gate passes")
        if artifact_gate_failed:
            merge_blockers.append("the artifact violations are resolved and the artifact gate passes")

        recovery = [
            (
                f"## ⚠️ SpecKit: Phase {phase_number} ({phase_name}) PR Created, Routing Labels Failed"
                if label_setup_status == "failed"
                else f"## ⚠️ SpecKit: Phase {phase_number} ({phase_name}) PR Created, Workflow Incomplete"
            ),
            "",
            (
                f"The PR{f' #{created_pr_number}' if created_pr_number else ''}"
                f"{f' ({created_pr_url})' if created_pr_url else ''} already exists, "
                "but the workflow did not complete successfully."
            ),
            (
                f"Do not merge until {', and '.join(merge_blockers)}"
                f": {', '.join(f'`{label}`' for label in required_labels)}."
                if merge_blockers and label_setup_status == "failed"
                else (
                    f"Do not merge until {', and '.join(merge_blockers)}."
                    if merge_blockers
                    else (
                        "Check the workflow logs before merging; the PR workflow did not reach a verified "
                        "completion state."
                    )
                )
            ),
            *(["", *gate_findings] if gate_findings else []),
            "",
            "### Recovery",
            "",
            "1. Use the workflow logs to create any missing required labels.",
            "2. Apply the required labels with the REST API:",
            "",
            "```bash",
            label_command,
            "```",
            "",
            (
                f"3. Verify the labels with `gh api --paginate "
                f'"repos/{repo}/issues/{created_pr_number or "<PR_NUMBER>"}/labels"`.'
            ),
            (
                "4. Resolve the gate findings above, rerun the applicable checks, and merge only after all blockers "
                "are cleared."
                if merge_blockers
                else "4. Merge the PR after confirming the workflow completed successfully."
            ),
            (
                (
                    "If the PR was already merged, resolve the gate findings and re-run their checks before manually "
                    f"dispatching Phase {phase_number + 1} from the SpecKit Phase Progression workflow."
                )
                if phase_number < 3 and gate_findings
                else (
                    f"If the PR was already merged, manually dispatch Phase {phase_number + 1} from the SpecKit "
                    "Phase Progression workflow."
                    if phase_number < 3
                    else "If the PR was already merged, follow the workflow logs to recover the post-Phase-3 action; "
                    "Phase 4 is not a valid dispatch phase."
                )
            ),
            "",
            f"**Workflow Run**: [View logs]({run_url})",
            "",
            "---",
            "",
            f"_This comment was posted by the [SpecKit GitHub Action]({run_url})._",
        ]
        return "\n".join(recovery)

    return "\n".join(
        [
            f"## ❌ SpecKit: Phase {phase_number} ({phase_name}) Failed",
            "",
            f"An error occurred while generating Phase {phase_number} artifacts.",
            "",
            f"**Workflow Run**: [View logs]({run_url})",
            "",
            "### Troubleshooting",
            "",
            "1. Check the workflow logs for detailed error messages",
            "2. Verify that the COPILOT_GITHUB_TOKEN secret is configured with repo permissions",
            (
                "3. You can re-trigger this phase manually via the **workflow_dispatch** trigger on the "
                f"[SpecKit Phase Progression workflow](https://github.com/{repo}/actions/workflows/"
                "speckit-phase-progression.yml) — provide the issue number and phase to retry"
            ),
            "",
            "---",
            "",
            f"_This comment was posted by the [SpecKit GitHub Action]({run_url})._",
        ]
    )


def progression_failure_comment_command() -> None:
    """Build and optionally post the failed progression issue comment."""
    issue_number = os.environ.get("ISSUE_NUMBER", "").strip()
    if not issue_number or issue_number == "0":
        return
    if os.environ.get("COMMENT_ON_ISSUE", "").lower() != "true":
        return

    body = build_failure_comment(
        phase=os.environ.get("NEXT_PHASE", "0"),
        phase_name=os.environ.get("NEXT_PHASE_NAME", "unknown"),
        repo=os.environ.get("GITHUB_REPOSITORY", ""),
        run_id=os.environ.get("GITHUB_RUN_ID", ""),
        gate_result=os.environ.get("GATE_RESULT", ""),
        critical_findings=os.environ.get("CRITICAL_FINDINGS", "[]"),
        artifact_gate_result=os.environ.get("ARTIFACT_GATE_RESULT", ""),
        artifact_gate_violations=os.environ.get("ARTIFACT_GATE_VIOLATIONS", ""),
        created_pr_number=os.environ.get("CREATED_PR_NUMBER", ""),
        created_pr_url=os.environ.get("CREATED_PR_URL", ""),
        label_setup_status=os.environ.get("LABEL_SETUP_STATUS", ""),
        hierarchy_level=os.environ.get("HIERARCHY_LEVEL", "unknown"),
        task_restart_guard_failed=os.environ.get("TASK_RESTART_GUARD_FAILED", "").lower() == "true",
        hierarchy_reason=os.environ.get("HIERARCHY_REASON", ""),
    )

    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(body)
        body_file = handle.name
    try:
        completed = subprocess.run(
            [
                "gh",
                "issue",
                "comment",
                issue_number,
                "--repo",
                os.environ.get("GITHUB_REPOSITORY", ""),
                "--body-file",
                body_file,
            ],
            capture_output=True,
            text=True,
            shell=False,
        )
    finally:
        Path(body_file).unlink(missing_ok=True)

    if completed.returncode != 0:
        print(
            f"Error: failed to post the SpecKit progression failure comment (gh exit {completed.returncode}).",
            file=sys.stderr,
        )
        if completed.stderr:
            print(completed.stderr.strip(), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    progression_failure_comment_command()
