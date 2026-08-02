"""Rule: titles must be in English, action-oriented, without prefixes."""

import re
from typing import Any

from ....common.glab.models import GitLabIssue
from ..classifiers import generate_title_with_claude
from ..diagnostic import IssueReport, RuleContext, Violation, ViolationFix, ViolationFixType
from .base import Rule


class TitleRule(Rule):
    name = "title"
    display_name = "Titre"
    color = "#20c997"
    fix_types = {
        "title:strip_prefix": "Suppression préfixe titre",
        "title:translate": "Traduction titre",
    }

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations = []
        title = issue.title

        prefix_match = re.match(r"^\s*(\[.*?\]|[\w-]+\s*:)\s*", title)
        if prefix_match:
            prefix = prefix_match.group(1).strip()
            violations.append(
                Violation(
                    check=self.name,
                    severity="error",
                    message=f"Préfixe interdit dans le titre : '{prefix}' (utiliser les labels)",
                    method="prefix",
                )
            )

        french_markers = [
            r"\bpour\b",
            r"\bdans\b",
            r"\bune?\b",
            r"\bavec\b",
            r"\bdes\b",
            r"\best\b",
            r"\bles?\b",
            r"\bsur\b",
            r"\bdu\b",
            r"\bau\b",
            r"\baux\b",
            r"\bqui\b",
            r"\bque\b",
            r"\bpar\b",
            r"\bson\b",
            r"\bsa\b",
            r"\bses\b",
            r"\bnous\b",
            r"\bvoir\b",
            r"\bfaire\b",
            r"\bajouter\b",
            r"\bcréer\b",
            r"\bmettre\b",
            r"\bsupprimer\b",
            r"\bmodifier\b",
            r"\bcorriger\b",
            r"\bpermettre\b",
            r"\bgérer\b",
            r"\bafficher\b",
            r"\benvoyer\b",
            r"\blorsque\b",
            r"\bquand\b",
            r"\bl['\u2019]",
            r"\bd['\u2019]",
        ]
        french_count = sum(1 for p in french_markers if re.search(p, title, re.IGNORECASE))
        if french_count >= 2:
            violations.append(
                Violation(
                    check=self.name,
                    severity="error",
                    message="Titre en français (doit être en anglais)",
                    method="french",
                )
            )

        return violations

    def enrich(self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext) -> None:
        if violation.method == "prefix":
            violation.fixable = True
            violation.fix = ViolationFix(ViolationFixType.STRIP_PREFIX, "Supprimer le préfixe")
        elif violation.method == "french":
            violation.fixable = True
            violation.fix = ViolationFix(ViolationFixType.TRANSLATE, "Reformuler le titre en anglais")
        else:
            violation.fixable = False

    def build_actions(
        self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext
    ) -> list[dict[str, Any]]:
        if violation.fix and violation.fix.type == ViolationFixType.STRIP_PREFIX:
            stripped = re.sub(r"^\s*(\[.*?\]|[\w-]+\s*:)\s*", "", report.title).strip()
            if stripped:
                stripped = stripped[0].upper() + stripped[1:]
            return [
                {
                    "type": "set_title",
                    "check": self.name,
                    "title": stripped,
                    "current_title": report.title,
                    "needs_claude": False,
                }
            ]

        elif violation.fix and violation.fix.type == ViolationFixType.TRANSLATE:
            desc = issue_data.description or ""
            new_title = generate_title_with_claude(report.title, desc, report.labels)
            if new_title:
                return [
                    {
                        "type": "set_title",
                        "check": self.name,
                        "title": new_title,
                        "current_title": report.title,
                        "needs_claude": False,
                    }
                ]

        return []
