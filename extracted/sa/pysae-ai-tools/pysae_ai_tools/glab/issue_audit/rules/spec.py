"""Rule: issues beyond Refinement must have filled description sections."""

import re

from ....common.glab.models import GitLabIssue
from ....common.references.gitlab_labels import BoardLabel
from ..diagnostic import RuleContext, Violation
from .base import Rule

BEYOND_REFINEMENT_LABELS: set[str] = {str(b) for b in BoardLabel if b is not BoardLabel.REFINEMENT}


class SpecRule(Rule):
    name = "spec"
    display_name = "Spécification"
    color = "#6610f2"

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations: list[Violation] = []
        issue_labels = set(issue.labels)

        if not (issue_labels & BEYOND_REFINEMENT_LABELS):
            return violations

        description = issue.description or ""
        board_label = sorted(issue_labels & BEYOND_REFINEMENT_LABELS)[0]

        sections = re.split(r"^#{2,3}\s+", description, flags=re.MULTILINE)
        total_sections = len(sections) - 1
        if total_sections <= 0:
            violations.append(
                Violation(
                    check=self.name,
                    severity="warning",
                    message=f"Issue en '{board_label}' sans sections structurées",
                    method="no_sections",
                )
            )
            return violations

        empty_sections = []
        for section in sections[1:]:
            heading = section.splitlines()[0].strip() if section.splitlines() else ""
            content = "\n".join(section.splitlines()[1:]) if len(section.splitlines()) > 1 else ""
            lines = []
            for line in content.splitlines():
                stripped = line.strip()
                if (
                    not stripped
                    or stripped.startswith(">")
                    or stripped.startswith("---")
                    or stripped.startswith("- [ ]")
                ):
                    continue
                lines.append(stripped)
            if not lines:
                empty_sections.append(heading)

        if empty_sections and total_sections > 0 and len(empty_sections) / total_sections >= 0.5:
            sections_str = ", ".join(f"'{s}'" for s in empty_sections)
            violations.append(
                Violation(
                    check=self.name,
                    severity="warning",
                    message=f"Issue en '{board_label}' avec sections vides : {sections_str}",
                    method=f"{len(empty_sections)}/{total_sections} vides",
                )
            )

        return violations

    # No enrich/build_actions — spec is not auto-fixable
