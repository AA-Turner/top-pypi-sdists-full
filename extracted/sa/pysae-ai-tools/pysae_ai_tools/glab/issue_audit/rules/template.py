"""Rule: issue description must follow the type-specific template."""

import re
import urllib.parse
from typing import Any

from ....common.glab.fetch_issues import run_glab
from ....common.glab.models import GitLabIssue
from ....common.glab.templates import extract_sections as _extract_sections_full
from ....common.glab.templates import strip_heading_emojis as strip_emojis
from ..constants import TEMPLATES_PROJECT, TYPE_TO_TEMPLATE
from ..diagnostic import IssueReport, RuleContext, Violation, ViolationFix, ViolationFixType
from .base import Rule

_template_cache: dict[str, list[str]] = {}


def fetch_template_sections(template_name: str) -> list[str]:
    """Fetch an issue template and extract its section headings (## and ###)."""
    if template_name in _template_cache:
        return _template_cache[template_name]

    encoded = urllib.parse.quote(f".gitlab/issue_templates/{template_name}.md", safe="")
    project_encoded = urllib.parse.quote(TEMPLATES_PROJECT, safe="")
    raw = run_glab(
        "api",
        f"projects/{project_encoded}/repository/files/{encoded}/raw?ref=main",
        allow_fail=True,
    )
    if not raw:
        _template_cache[template_name] = []
        return []

    sections = []
    for line in raw.splitlines():
        match = re.match(r"^(#{2,3})\s+(.+)$", line.strip())
        if match:
            sections.append(match.group(2).strip())

    _template_cache[template_name] = sections
    return sections


def extract_description_sections(description: str) -> list[str]:
    """Extract section headings from an issue description."""
    return [s.heading for s in _extract_sections_full(description)]


def normalize_section_title(title: str) -> str:
    return re.sub(r"\s+", " ", strip_emojis(title)).lower().strip()


class TemplateRule(Rule):
    name = "template"
    display_name = "Template"
    color = "#e83e8c"
    fix_types = {
        "template:fix_template": "Correction template",
    }

    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        violations = []
        issue_labels = set(issue.labels)
        description = issue.description or ""

        template_name = None
        for type_label, tpl in TYPE_TO_TEMPLATE.items():
            if type_label in issue_labels:
                template_name = tpl
                break

        if template_name is None:
            violations.append(
                Violation(
                    check=self.name,
                    severity="warning",
                    message="Pas de label type:: — impossible de vérifier le template",
                )
            )
            return violations

        expected_sections = fetch_template_sections(template_name)
        if not expected_sections:
            return violations

        actual_sections = extract_description_sections(description)
        missing = [s for s in expected_sections if s not in actual_sections]

        if missing:
            missing_str = ", ".join(f"'{s}'" for s in missing)
            violations.append(
                Violation(
                    check=self.name,
                    severity="warning",
                    message=f"Sections manquantes du template '{template_name}' : {missing_str}",
                    method=template_name,
                )
            )

        return violations

    def enrich(self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext) -> None:
        if "Sections manquantes" in violation.message:
            violation.fixable = True
            violation.fix = ViolationFix(
                ViolationFixType.FIX_TEMPLATE, "Renommer les titres proches ou ajouter les sections manquantes"
            )
        else:
            violation.fixable = False

    def build_actions(
        self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext
    ) -> list[dict[str, Any]]:
        if not (violation.fix and violation.fix.type == ViolationFixType.FIX_TEMPLATE):
            return []

        description = issue_data.description or ""
        issue_labels = set(issue_data.labels)

        template_name = None
        for type_label, tpl in TYPE_TO_TEMPLATE.items():
            if type_label in issue_labels:
                template_name = tpl
                break
        if not template_name:
            return []

        expected_sections = fetch_template_sections(template_name)
        actual_sections = extract_description_sections(description)
        missing = [s for s in expected_sections if s not in actual_sections]
        if not missing:
            return []

        actual_by_normalized: dict[str, str] = {}
        for s in actual_sections:
            actual_by_normalized[normalize_section_title(s)] = s

        renamed = []
        appended = []
        new_description = description

        for section in missing:
            norm = normalize_section_title(section)
            if norm in actual_by_normalized:
                old_title = actual_by_normalized[norm]
                new_description = re.sub(
                    rf"^(#{2, 3})\s+{re.escape(old_title)}\s*$",
                    rf"\1 {section}",
                    new_description,
                    count=1,
                    flags=re.MULTILINE,
                )
                renamed.append(f"'{old_title}' → '{section}'")
            else:
                new_description = new_description.rstrip() + f"\n\n### {section}\n\n"
                appended.append(f"'{section}'")

        if not renamed and not appended:
            return []

        summary_parts = []
        if renamed:
            summary_parts.append(f"Sections renommées : {', '.join(renamed)}")
        if appended:
            summary_parts.append(f"Sections ajoutées : {', '.join(appended)}")

        return [
            {
                "type": "set_description",
                "check": self.name,
                "description": new_description,
                "summary": "; ".join(summary_parts),
                "needs_claude": False,
            }
        ]
