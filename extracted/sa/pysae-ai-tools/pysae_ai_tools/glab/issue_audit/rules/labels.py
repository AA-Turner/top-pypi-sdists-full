"""Rule: project-level labels must be replaced by group-level labels."""

from typing import Any

from ....common.glab.fetch_issues import glab_api_paginated
from ....common.glab.models import GitLabIssue
from ..diagnostic import DetectionMethod, IssueReport, RuleContext, Violation, ViolationFix, ViolationFixType
from .base import Rule


def fetch_project_labels(project_id: int) -> set[str]:
    """Fetch labels defined at the project level (excluding inherited group labels)."""
    data = glab_api_paginated(f"projects/{project_id}/labels?include_ancestor_groups=false")
    return {label["name"] for label in data}


def find_best_group_match(label: str, group_labels: set[str]) -> str | None:
    """Find the best matching group label for a project label (case-insensitive)."""
    label_lower = label.lower().strip()
    for gl in group_labels:
        if gl.lower().strip() == label_lower:
            return gl
    return None


class LabelsRule(Rule):
    name = "labels"
    display_name = "Labels projet"
    color = "#6f42c1"
    fix_types = {
        "labels:replace_label": "Remplacement label",
        "labels:remove_label": "Suppression label",
    }

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations = []

        cache_hit = issue.project_id in ctx.project_labels_cache
        if not cache_hit:
            ctx.project_labels_cache[issue.project_id] = fetch_project_labels(issue.project_id)

        proj_labels = ctx.project_labels_cache[issue.project_id]
        method = DetectionMethod.CACHE if cache_hit else DetectionMethod.API

        for label in issue.labels:
            if label in proj_labels and label not in ctx.group_labels:
                violations.append(
                    Violation(
                        check=self.name,
                        severity="error",
                        message=f"Label projet interdit : '{label}'",
                        method=method,
                    )
                )

        return violations

    def enrich(self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext) -> None:
        label = violation.message.split("'")[1]
        group_match = find_best_group_match(label, ctx.group_labels)
        if group_match:
            violation.fixable = True
            violation.fix = ViolationFix(ViolationFixType.REPLACE_LABEL, f"Remplacer '{label}' par '{group_match}'")
        else:
            violation.fixable = True
            violation.fix = ViolationFix(
                ViolationFixType.REMOVE_LABEL, f"Supprimer '{label}' (aucun équivalent groupe)"
            )

    def build_actions(
        self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext
    ) -> list[dict[str, Any]]:
        label = violation.message.split("'")[1]
        actions = [{"type": "remove_label", "check": self.name, "label": label}]
        if violation.fix and violation.fix.type == ViolationFixType.REPLACE_LABEL:
            group_match = find_best_group_match(label, ctx.group_labels)
            if group_match:
                actions.append({"type": "add_label", "check": self.name, "label": group_match})
        return actions
