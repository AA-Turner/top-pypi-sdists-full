"""Rule: issues in workflow must be assigned."""

from ....common.glab.models import GitLabIssue
from ..diagnostic import RuleContext, Violation
from .base import Rule

WORKFLOW_LABELS = {
    "workflow::To Do",
    "workflow::In progress",
    "workflow::Under review",
    "workflow::To deploy",
}


class AssigneeRule(Rule):
    name = "assignee"
    display_name = "Assignation"
    color = "#d63384"

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations: list[Violation] = []
        issue_labels = set(issue.labels)

        if not (issue_labels & WORKFLOW_LABELS):
            return violations

        assignees = issue.assignees
        if not assignees:
            workflow_label = sorted(issue_labels & WORKFLOW_LABELS)[0]
            violations.append(
                Violation(
                    check=self.name,
                    severity="error",
                    message=f"Issue en '{workflow_label}' non assignée",
                    method=workflow_label,
                )
            )

        return violations

    # No enrich/build_actions — assignee is not auto-fixable
