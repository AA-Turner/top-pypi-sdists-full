"""Rule: issues must have a weight assigned."""

from ....common.glab.models import GitLabIssue
from ....common.references.gitlab_labels import BoardLabel
from ..diagnostic import RuleContext, Violation
from .base import Rule

BEYOND_REFINEMENT_LABELS: set[str] = {str(b) for b in BoardLabel if b is not BoardLabel.REFINEMENT}


class WeightRule(Rule):
    name = "weight"
    display_name = "Poids"
    color = "#fd7e14"

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations = []
        weight = issue.weight
        if weight is None:
            issue_labels = set(issue.labels)
            is_beyond_refinement = bool(issue_labels & BEYOND_REFINEMENT_LABELS)
            severity = "error" if is_beyond_refinement else "warning"
            violations.append(
                Violation(
                    check=self.name,
                    severity=severity,
                    message="Aucun poids assigné à l'issue",
                    method="beyond_refinement" if is_beyond_refinement else "backlog",
                )
            )
        return violations

    # No enrich/build_actions — weight is not auto-fixable
