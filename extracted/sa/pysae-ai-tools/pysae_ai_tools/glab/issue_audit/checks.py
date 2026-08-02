"""Diagnostic checks — detect issues without resolving them.

All check functions return list[Violation] with fixable=False.
Resolution (setting fixable=True and fix objects) is done in fix_plan.py.
"""

import re
import urllib.parse
from typing import Any

from ...common.glab.fetch_issues import (
    glab_api_paginated,
    run_glab,
)
from ...common.glab.models import GitLabIssue
from ...common.group import resolve_group_id
from ...common.project_config import domain_labels
from ...common.references.gitlab_labels import BoardLabel
from .classifiers import guess_domain_label
from .constants import BOARD_LABELS, TEMPLATES_PROJECT, TYPE_TO_TEMPLATE
from .diagnostic import DetectionMethod, Violation

# ---------------------------------------------------------------------------
# Label resolution helpers
# ---------------------------------------------------------------------------

TYPE_LABEL_PREFIX = "type::"


def fetch_group_labels() -> tuple[set[str], dict[str, str]]:
    """Fetch all labels defined at the pysae group level.

    Returns (label_names, label_colors) where label_colors maps name -> hex color.
    """
    data = glab_api_paginated(f"groups/{resolve_group_id()}/labels")
    names = {label["name"] for label in data}
    colors = {label["name"]: label.get("color", "#6c757d") for label in data}
    return names, colors


def fetch_project_labels(project_id: int) -> set[str]:
    """Fetch labels defined at the project level (excluding inherited group labels)."""
    data = glab_api_paginated(f"projects/{project_id}/labels?include_ancestor_groups=false")
    return {label["name"] for label in data}


def fetch_group_projects() -> list[dict[str, Any]]:
    """Fetch all projects in the pysae group."""
    return glab_api_paginated(f"groups/{resolve_group_id()}/projects?archived=false")


# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------

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
    sections = []
    for line in description.splitlines():
        match = re.match(r"^(#{2,3})\s+(.+)$", line.strip())
        if match:
            sections.append(match.group(2).strip())
    return sections


def strip_emojis(text: str) -> str:
    """Remove emoji characters from a string."""
    return re.sub(
        r"[\U0001f300-\U0001f9ff\U00002600-\U000027bf\U0000fe00-\U0000fe0f"
        r"\U0000200d\U00002702-\U000027b0\U0001fa00-\U0001fa6f"
        r"\U0001fa70-\U0001faff\U00002500-\U00002bef]+",
        "",
        text,
    ).strip()


def normalize_section_title(title: str) -> str:
    """Normalize a section title for fuzzy comparison."""
    return re.sub(r"\s+", " ", strip_emojis(title)).lower().strip()


def find_best_group_match(label: str, group_labels: set[str]) -> str | None:
    """Find the best matching group label for a project label (case-insensitive)."""
    label_lower = label.lower().strip()
    for gl in group_labels:
        if gl.lower().strip() == label_lower:
            return gl
    return None


# ---------------------------------------------------------------------------
# Check functions (diagnostic only — no resolution)
# ---------------------------------------------------------------------------

WORKFLOW_LABELS = {
    "workflow::To Do",
    "workflow::In progress",
    "workflow::Under review",
    "workflow::To deploy",
}

BEYOND_REFINEMENT_LABELS: set[str] = {str(b) for b in BoardLabel if b is not BoardLabel.REFINEMENT}


def check_labels(
    issue: dict[str, Any],
    group_labels: set[str],
    project_labels_cache: dict[int, set[str]],
) -> list[Violation]:
    """Check that all issue labels are group-level (not project-level)."""
    violations: list[Violation] = []
    issue_labels = issue.get("labels", [])
    project_id = issue["project_id"]

    cache_hit = project_id in project_labels_cache
    if not cache_hit:
        project_labels_cache[project_id] = fetch_project_labels(project_id)

    proj_labels = project_labels_cache[project_id]
    method = DetectionMethod.CACHE if cache_hit else DetectionMethod.API

    for label in issue_labels:
        if label in proj_labels and label not in group_labels:
            violations.append(
                Violation(
                    check="labels",
                    severity="error",
                    message=f"Label projet interdit : '{label}'",
                    method=method,
                )
            )

    return violations


def check_required_labels(issue: dict[str, Any]) -> list[Violation]:
    """Check that mandatory labels are present: at least one domain label and exactly one type:: label."""
    violations: list[Violation] = []
    issue_labels = issue.get("labels", [])

    # Domain label check — vocabulary is the union of repo configs' primary domain labels.
    # An empty vocabulary means "can't validate" (glab unreachable, or no config declares a
    # domain): skip the check rather than flagging every issue as missing a domain.
    vocabulary = domain_labels()
    has_domain = any(label in vocabulary for label in issue_labels)
    if vocabulary and not has_domain:
        guessed_domain = guess_domain_label(GitLabIssue.from_api(issue))
        if guessed_domain:
            violations.append(
                Violation(
                    check="required_labels",
                    severity="error",
                    message=f"Label domaine manquant — suggestion : '{guessed_domain}'",
                )
            )
        else:
            violations.append(
                Violation(
                    check="required_labels",
                    severity="error",
                    message=f"Label domaine manquant (attendu : {', '.join(vocabulary)})",
                )
            )

    # Type label check
    type_labels = [label for label in issue_labels if label.startswith(TYPE_LABEL_PREFIX)]
    if not type_labels:
        violations.append(
            Violation(
                check="required_labels",
                severity="error",
                message="Label type:: manquant",
            )
        )
    elif len(type_labels) > 1:
        violations.append(
            Violation(
                check="required_labels",
                severity="error",
                message=f"Plusieurs labels type:: : {', '.join(type_labels)} (un seul attendu)",
            )
        )

    return violations


def check_weight(issue: dict[str, Any]) -> list[Violation]:
    """Check that the issue has a weight assigned."""
    violations: list[Violation] = []
    weight = issue.get("weight")
    if weight is None:
        issue_labels = set(issue.get("labels", []))
        is_beyond_refinement = bool(issue_labels & BEYOND_REFINEMENT_LABELS)
        severity = "error" if is_beyond_refinement else "warning"
        violations.append(
            Violation(
                check="weight",
                severity=severity,
                message="Aucun poids assigné à l'issue",
                method="beyond_refinement" if is_beyond_refinement else "backlog",
            )
        )
    return violations


def check_board(issue: dict[str, Any]) -> list[Violation]:
    """Check that the issue has exactly one board column label."""
    violations: list[Violation] = []
    issue_labels = set(issue.get("labels", []))
    board_labels_present = issue_labels & BOARD_LABELS

    if len(board_labels_present) == 0:
        violations.append(
            Violation(
                check="board",
                severity="error",
                message="Aucun label de colonne board (invisible sur le board)",
                method="missing",
            )
        )
    elif len(board_labels_present) > 1:
        labels_str = ", ".join(sorted(board_labels_present))
        violations.append(
            Violation(
                check="board",
                severity="error",
                message=f"Plusieurs labels board : {labels_str}",
                method="duplicate",
            )
        )

    return violations


def check_assignee(issue: dict[str, Any]) -> list[Violation]:
    """Check that issues with a workflow label are assigned to at least one person."""
    violations: list[Violation] = []
    issue_labels = set(issue.get("labels", []))

    if not (issue_labels & WORKFLOW_LABELS):
        return violations

    assignees = issue.get("assignees", [])
    if not assignees:
        workflow_label = sorted(issue_labels & WORKFLOW_LABELS)[0]
        violations.append(
            Violation(
                check="assignee",
                severity="error",
                message=f"Issue en '{workflow_label}' non assignée",
                method=workflow_label,
            )
        )

    return violations


def check_spec(issue: dict[str, Any]) -> list[Violation]:
    """Check that issues beyond Refinement have all description sections filled."""
    violations: list[Violation] = []
    issue_labels = set(issue.get("labels", []))

    if not (issue_labels & BEYOND_REFINEMENT_LABELS):
        return violations

    description = issue.get("description") or ""
    board_label = sorted(issue_labels & BEYOND_REFINEMENT_LABELS)[0]

    # Extract sections from description
    sections = re.split(r"^#{2,3}\s+", description, flags=re.MULTILINE)
    total_sections = len(sections) - 1  # skip text before first heading
    if total_sections <= 0:
        violations.append(
            Violation(
                check="spec",
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
            if not stripped or stripped.startswith(">") or stripped.startswith("---") or stripped.startswith("- [ ]"):
                continue
            lines.append(stripped)
        if not lines:
            empty_sections.append(heading)

    if empty_sections and total_sections > 0 and len(empty_sections) / total_sections >= 0.5:
        sections_str = ", ".join(f"'{s}'" for s in empty_sections)
        violations.append(
            Violation(
                check="spec",
                severity="warning",
                message=f"Issue en '{board_label}' avec sections vides : {sections_str}",
                method=f"{len(empty_sections)}/{total_sections} vides",
            )
        )

    return violations


def check_template(issue: dict[str, Any]) -> list[Violation]:
    """Check that the issue description follows the expected template."""
    violations: list[Violation] = []
    issue_labels = set(issue.get("labels", []))
    description = issue.get("description") or ""

    template_name = None
    for type_label, tpl in TYPE_TO_TEMPLATE.items():
        if type_label in issue_labels:
            template_name = tpl
            break

    if template_name is None:
        violations.append(
            Violation(
                check="template",
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
                check="template",
                severity="warning",
                message=f"Sections manquantes du template '{template_name}' : {missing_str}",
                method=template_name,
            )
        )

    return violations


def check_title(issue: dict[str, Any]) -> list[Violation]:
    """Check that the issue title is in English, action-oriented, and has no scope/type prefix."""
    violations: list[Violation] = []
    title = issue.get("title", "")

    prefix_match = re.match(
        r"^\s*(\[.*?\]|[\w-]+\s*:)\s*",
        title,
    )
    if prefix_match:
        prefix = prefix_match.group(1).strip()
        violations.append(
            Violation(
                check="title",
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
    french_count = sum(1 for pattern in french_markers if re.search(pattern, title, re.IGNORECASE))
    if french_count >= 2:
        violations.append(
            Violation(
                check="title",
                severity="error",
                message="Titre en français (doit être en anglais)",
                method="french",
            )
        )

    return violations
