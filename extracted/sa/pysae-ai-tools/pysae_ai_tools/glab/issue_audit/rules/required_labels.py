"""Rule: mandatory domain and type labels must be present."""

from typing import Any

from ....common.glab.models import GitLabIssue
from ....common.project_config import domain_labels
from ..classifiers import VALID_TYPE_LABELS, guess_domain_label, guess_type_label
from ..constants import METHOD_DISPLAY
from ..diagnostic import IssueReport, RuleContext, Violation, ViolationFix, ViolationFixType
from .base import Rule

TYPE_LABEL_PREFIX = "type::"


class RequiredLabelsRule(Rule):
    name = "required_labels"
    display_name = "Labels obligatoires"
    color = "#9c27b0"
    fix_types = {
        "required_labels:add_label": "Ajout label requis",
        "required_labels:add_label:project": "Ajout label requis (via projet)",
        "required_labels:add_label:keywords": "Ajout label requis (via mots-clés)",
        "required_labels:add_label:claude": "Ajout label requis (via Claude)",
    }

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations = []
        issue_labels = issue.labels

        # Domain label check — vocabulary is the union of repo configs' primary domain labels.
        # An empty vocabulary means "can't validate" (glab unreachable, or no config declares a
        # domain): skip the check rather than flagging every issue as missing a domain.
        vocabulary = domain_labels()
        has_domain = any(label in vocabulary for label in issue_labels)
        if vocabulary and not has_domain:
            guessed_domain = guess_domain_label(issue)
            if guessed_domain:
                violations.append(
                    Violation(
                        check=self.name,
                        severity="error",
                        message=f"Label domaine manquant — suggestion : '{guessed_domain}'",
                    )
                )
            else:
                violations.append(
                    Violation(
                        check=self.name,
                        severity="error",
                        message=f"Label domaine manquant (attendu : {', '.join(vocabulary)})",
                    )
                )

        # Type label check
        type_labels = [label for label in issue_labels if label.startswith(TYPE_LABEL_PREFIX)]
        if not type_labels:
            violations.append(
                Violation(
                    check=self.name,
                    severity="error",
                    message="Label type:: manquant",
                )
            )
        elif len(type_labels) > 1:
            violations.append(
                Violation(
                    check=self.name,
                    severity="error",
                    message=f"Plusieurs labels type:: : {', '.join(type_labels)} (un seul attendu)",
                )
            )
        else:
            unofficial = [label for label in type_labels if label not in VALID_TYPE_LABELS]
            if unofficial:
                official = ", ".join(sorted(VALID_TYPE_LABELS))
                violations.append(
                    Violation(
                        check=self.name,
                        severity="error",
                        message=f"Label type:: non-officiel : '{unofficial[0]}' (valeurs autorisées : {official})",
                    )
                )

        return violations

    def enrich(self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext) -> None:
        if "type:: manquant" in violation.message:
            guessed_type, guess_method = guess_type_label(issue_data)
            if guessed_type:
                method_label = METHOD_DISPLAY.get(guess_method, guess_method)
                violation.fixable = True
                violation.fix = ViolationFix(ViolationFixType.ADD_LABEL, f"Ajouter '{guessed_type}'")
                violation.method = guess_method
                violation.message = f"Label type:: manquant — suggestion : '{guessed_type}' (via {method_label})"
            else:
                violation.fixable = False

        elif "domaine manquant" in violation.message and "suggestion" in violation.message:
            label_to_add = violation.message.split("'")[1]
            violation.fixable = True
            violation.fix = ViolationFix(ViolationFixType.ADD_LABEL, f"Ajouter '{label_to_add}'")

        else:
            violation.fixable = False

    def build_actions(
        self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext
    ) -> list[dict[str, Any]]:
        if violation.fix and violation.fix.type == ViolationFixType.ADD_LABEL:
            label_to_add = violation.fix.label.split("'")[1]
            return [{"type": "add_label", "check": self.name, "label": label_to_add}]
        return []
