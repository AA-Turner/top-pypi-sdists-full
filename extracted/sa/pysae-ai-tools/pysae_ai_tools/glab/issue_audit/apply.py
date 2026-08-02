"""Apply fixes — execute fix actions via glab API.

Contains both:
- Legacy per-report apply functions (used by --fix)
- Plan-based apply (used by --apply / web UI)
"""

import json
import re
import sys
from typing import Any

from ...common.glab.fetch_issues import run_glab
from ...common.references.gitlab_labels import (
    BOARD_LABEL_ORDER,
    DEFAULT_BOARD_LABEL,
    BoardLabel,
)
from .checks import (
    extract_description_sections,
    fetch_template_sections,
    find_best_group_match,
    normalize_section_title,
)
from .classifiers import generate_title_with_claude
from .constants import BOARD_LABELS, TYPE_TO_TEMPLATE
from .diagnostic import IssueReport

# ---------------------------------------------------------------------------
# Per-report apply functions (legacy --fix mode)
# ---------------------------------------------------------------------------


def apply_label_fixes(report: IssueReport, group_labels: set[str]) -> list[str]:
    """Fix label violations for an issue."""
    actions = []
    for v in report.violations:
        if v.check != "labels" or not v.fixable:
            continue

        label = v.message.split("'")[1]
        group_match = find_best_group_match(label, group_labels)
        if group_match:
            run_glab(
                "api",
                "-X",
                "PUT",
                f"projects/{report.project_id}/issues/{report.iid}",
                "-f",
                f"remove_labels={label}",
                "-f",
                f"add_labels={group_match}",
                allow_fail=True,
            )
            actions.append(f"#{report.iid} ({report.project_path}): '{label}' → '{group_match}'")
        else:
            run_glab(
                "api",
                "-X",
                "PUT",
                f"projects/{report.project_id}/issues/{report.iid}",
                "-f",
                f"remove_labels={label}",
                allow_fail=True,
            )
            actions.append(f"#{report.iid} ({report.project_path}): '{label}' supprimé (aucun équivalent groupe)")

    return actions


def apply_board_fixes(report: IssueReport) -> list[str]:
    """Fix board violations for an issue."""
    actions = []
    for v in report.violations:
        if v.check != "board" or not v.fixable:
            continue

        if "Plusieurs labels board" in v.message:
            present = set(report.labels) & BOARD_LABELS
            best = max(
                present, key=lambda lbl: BOARD_LABEL_ORDER.index(BoardLabel(lbl)) if lbl in BOARD_LABEL_ORDER else -1
            )
            to_remove = present - {best}
            for label in to_remove:
                run_glab(
                    "api",
                    "-X",
                    "PUT",
                    f"projects/{report.project_id}/issues/{report.iid}",
                    "-f",
                    f"remove_labels={label}",
                    allow_fail=True,
                )
            actions.append(
                f"#{report.iid} ({report.project_path}): conservé '{best}', supprimé {', '.join(sorted(to_remove))}"
            )
        else:
            run_glab(
                "api",
                "-X",
                "PUT",
                f"projects/{report.project_id}/issues/{report.iid}",
                "-f",
                f"add_labels={DEFAULT_BOARD_LABEL}",
                allow_fail=True,
            )
            actions.append(f"#{report.iid} ({report.project_path}): label '{DEFAULT_BOARD_LABEL}' ajouté")

    return actions


def apply_title_fixes(report: IssueReport, issue: dict[str, Any]) -> list[str]:
    """Fix title violations: generate a proper English title via Claude."""
    actions: list[str] = []
    has_title_violation = any(v.check == "title" and v.fixable for v in report.violations)
    if not has_title_violation:
        return actions

    old_title = issue.get("title", "")
    description = issue.get("description") or ""
    labels = issue.get("labels", [])

    new_title = generate_title_with_claude(old_title, description, labels)
    if not new_title or new_title == old_title:
        return actions

    run_glab(
        "api",
        "-X",
        "PUT",
        f"projects/{report.project_id}/issues/{report.iid}",
        "-f",
        f"title={new_title}",
        allow_fail=True,
    )
    actions.append(f"#{report.iid} ({report.project_path}): '{old_title}' → '{new_title}'")

    return actions


def apply_template_fixes(report: IssueReport, issue: dict[str, Any]) -> list[str]:
    """Fix template violations: rename fuzzy-matching headings or append missing sections."""
    actions = []
    for v in report.violations:
        if v.check != "template" or not v.fixable:
            continue

        description = issue.get("description") or ""
        issue_labels = set(issue.get("labels", []))

        template_name = None
        for type_label, tpl in TYPE_TO_TEMPLATE.items():
            if type_label in issue_labels:
                template_name = tpl
                break
        if not template_name:
            continue

        expected_sections = fetch_template_sections(template_name)
        actual_sections = extract_description_sections(description)

        missing = [s for s in expected_sections if s not in actual_sections]
        if not missing:
            continue

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

        if renamed or appended:
            run_glab(
                "api",
                "-X",
                "PUT",
                f"projects/{report.project_id}/issues/{report.iid}",
                "-f",
                f"description={new_description}",
                allow_fail=True,
            )
            parts = []
            if renamed:
                parts.append(f"renommé {', '.join(renamed)}")
            if appended:
                parts.append(f"ajouté {', '.join(appended)}")
            actions.append(f"#{report.iid} ({report.project_path}): {'; '.join(parts)}")

    return actions


# ---------------------------------------------------------------------------
# Plan-based apply (--apply / web UI)
# ---------------------------------------------------------------------------


def save_plan(plan: dict[str, Any], plan_path: str) -> None:
    """Save a plan dict to a JSON file."""
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    total_actions = sum(len(p["actions"]) for p in plan["issues"])
    print(f"\nPlan: {plan_path} ({len(plan['issues'])} issues, {total_actions} actions)", file=sys.stderr)


def apply_plan(plan_path: str) -> None:
    """Apply fixes from a plan file."""
    with open(plan_path) as f:
        plan = json.load(f)

    issues = plan.get("issues", [plan]) if "issues" in plan else [plan]

    for issue_plan in issues:
        project_id = issue_plan["project_id"]
        iid = issue_plan["iid"]
        project_path = issue_plan.get("project_path", str(project_id))
        actions = issue_plan.get("actions", [])

        print(f"Applying plan for #{iid} ({project_path}): {len(actions)} action(s)")

        for action in actions:
            action_type = action["type"]
            try:
                if action_type == "remove_label":
                    run_glab(
                        "api",
                        "-X",
                        "PUT",
                        f"projects/{project_id}/issues/{iid}",
                        "-f",
                        f"remove_labels={action['label']}",
                    )
                    print(f"  ✓ Removed label '{action['label']}'")
                elif action_type == "add_label":
                    run_glab(
                        "api", "-X", "PUT", f"projects/{project_id}/issues/{iid}", "-f", f"add_labels={action['label']}"
                    )
                    print(f"  ✓ Added label '{action['label']}'")
                elif action_type == "set_board_label":
                    for label in action.get("remove", []):
                        run_glab(
                            "api", "-X", "PUT", f"projects/{project_id}/issues/{iid}", "-f", f"remove_labels={label}"
                        )
                    run_glab(
                        "api", "-X", "PUT", f"projects/{project_id}/issues/{iid}", "-f", f"add_labels={action['label']}"
                    )
                    print(f"  ✓ Board: kept '{action['label']}', removed {action.get('remove', [])}")
                elif action_type == "set_title":
                    run_glab(
                        "api", "-X", "PUT", f"projects/{project_id}/issues/{iid}", "-f", f"title={action['title']}"
                    )
                    print("  ✓ Title updated")
                elif action_type == "set_description":
                    run_glab(
                        "api",
                        "-X",
                        "PUT",
                        f"projects/{project_id}/issues/{iid}",
                        "-f",
                        f"description={action['description']}",
                    )
                    print("  ✓ Description updated")
                else:
                    print(f"  ? Unknown action type: {action_type}")
            except Exception as e:
                print(f"  ✗ Failed: {action_type} — {e}")

        print(f"Done: {len(actions)} action(s) applied for #{iid}")
