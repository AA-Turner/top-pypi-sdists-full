"""Rule: every issue must have exactly one board column label."""

import re
from typing import Any

from ....common.glab.models import GitLabIssue
from ....common.references.gitlab_labels import (
    BOARD_LABEL_ORDER,
    DEFAULT_BOARD_LABEL,
    BoardLabel,
)
from ..diagnostic import IssueReport, RuleContext, Violation, ViolationFix, ViolationFixType
from .base import Rule

BOARD_LABELS: set[str] = set(BoardLabel)


def _is_description_ready(description: str) -> bool:
    """Check if ALL sections in the description have non-trivial content."""
    if not description:
        return False
    sections = re.split(r"^#{2,3}\s+", description, flags=re.MULTILINE)
    if len(sections) <= 1:
        return False
    for section in sections[1:]:
        lines = []
        for line in section.splitlines()[1:]:
            stripped = line.strip()
            if not stripped or stripped.startswith(">") or stripped.startswith("---") or stripped.startswith("- [ ]"):
                continue
            lines.append(stripped)
        if not lines:
            return False
    return True


class BoardRule(Rule):
    name = "board"
    display_name = "Placement board"
    color = "#0d6efd"
    fix_types = {
        "board:add_board": "Ajout label board",
        "board:keep_board": "Nettoyage labels board",
    }

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations = []
        issue_labels = set(issue.labels)
        board_labels_present = issue_labels & BOARD_LABELS

        if len(board_labels_present) == 0:
            violations.append(
                Violation(
                    check=self.name,
                    severity="error",
                    message="Aucun label de colonne board (invisible sur le board)",
                    method="missing",
                )
            )
        elif len(board_labels_present) > 1:
            labels_str = ", ".join(sorted(board_labels_present))
            violations.append(
                Violation(
                    check=self.name,
                    severity="error",
                    message=f"Plusieurs labels board : {labels_str}",
                    method="duplicate",
                )
            )

        return violations

    def enrich(self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext) -> None:
        if violation.method == "duplicate":
            present = set(report.labels) & BOARD_LABELS
            best = max(
                present, key=lambda lbl: BOARD_LABEL_ORDER.index(BoardLabel(lbl)) if lbl in BOARD_LABEL_ORDER else -1
            )
            to_remove = sorted(present - {best})
            violation.fixable = True
            violation.fix = ViolationFix(
                ViolationFixType.KEEP_BOARD, f"Conserver '{best}', supprimer {', '.join(to_remove)}"
            )
        elif violation.method == "missing":
            desc = issue_data.description or ""
            board_label = BoardLabel.READY if _is_description_ready(desc) else DEFAULT_BOARD_LABEL
            violation.fixable = True
            violation.fix = ViolationFix(ViolationFixType.ADD_BOARD, f"Ajouter '{board_label}'")
        else:
            violation.fixable = False

    def build_actions(
        self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext
    ) -> list[dict[str, Any]]:
        if violation.fix and violation.fix.type == ViolationFixType.KEEP_BOARD:
            present = set(report.labels) & BOARD_LABELS
            best = max(
                present, key=lambda lbl: BOARD_LABEL_ORDER.index(BoardLabel(lbl)) if lbl in BOARD_LABEL_ORDER else -1
            )
            to_remove = sorted(present - {best})
            return [{"type": "set_board_label", "check": self.name, "label": best, "remove": to_remove}]
        elif violation.fix and violation.fix.type == ViolationFixType.ADD_BOARD:
            board_label = violation.fix.label.split("'")[1]
            return [{"type": "add_label", "check": self.name, "label": board_label}]
        return []
