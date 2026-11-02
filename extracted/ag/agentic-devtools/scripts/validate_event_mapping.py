"""Validate that the workflow-event-mapping.md document covers all events and workflows.

Checks:
  (a) Every WorkflowEvent enum member appears in the mapping document.
  (b) Every workflow in WORKFLOW_REGISTRY appears in the mapping document.
  (c) Every (workflow, event, from_step, to_step) 4-tuple transition present in
      WORKFLOW_REGISTRY has a corresponding row in the mapping document.

Exit codes:
  0 — All checks pass.
  1 — One or more checks fail (details printed to stderr).
"""

import ast
import sys
from pathlib import Path

MANAGER_PATH = Path("agentic_devtools/cli/workflows/manager.py")
MAPPING_DOC_PATH = Path("docs/orchestration/workflow-event-mapping.md")


def _parse_workflow_event_members(source: str) -> set[str]:
    """Extract all WorkflowEvent enum member names via AST."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "WorkflowEvent":
            members = set()
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            members.add(target.id)
            return members
    return set()


def _parse_workflow_registry_names(source: str) -> set[str]:
    """Extract workflow names from WORKFLOW_REGISTRY dict literal via AST."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        # Handle annotated assignment: WORKFLOW_REGISTRY: dict[...] = {...}
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "WORKFLOW_REGISTRY":
                if isinstance(node.value, ast.Dict):
                    names = set()
                    for key in node.value.keys:
                        if isinstance(key, ast.Constant) and isinstance(key.value, str):
                            names.add(key.value)
                    return names
        # Handle regular assignment: WORKFLOW_REGISTRY = {...}
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "WORKFLOW_REGISTRY":
                    if isinstance(node.value, ast.Dict):
                        names = set()
                        for key in node.value.keys:
                            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                                names.add(key.value)
                        return names
    return set()


def _extract_workflow_transitions(workflow_name: str, value_node: ast.expr) -> list[tuple[str, str, str]]:
    """Extract ``(event_member, from_step, to_step)`` triples from a WorkflowDefinition AST node.

    Walks ``value_node`` (the right-hand side of a workflow variable assignment) and
    collects all ``WorkflowTransition(...)`` calls, returning one triple per
    ``(event, from_step, to_step)`` combination.
    """
    results: list[tuple[str, str, str]] = []
    for child in ast.walk(value_node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id == "WorkflowTransition":
            from_step: str | None = None
            to_step: str | None = None
            events: list[str] = []
            for kw in child.keywords:
                if kw.arg == "from_step" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    from_step = kw.value.value
                elif kw.arg == "to_step" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    to_step = kw.value.value
                elif kw.arg == "trigger_events" and isinstance(kw.value, ast.Set):
                    for elt in kw.value.elts:
                        if isinstance(elt, ast.Attribute):
                            events.append(elt.attr)
            if from_step and to_step:
                for event in events:
                    results.append((event, from_step, to_step))
    return results


def _parse_workflow_event_transitions(source: str) -> set[tuple[str, str, str, str]]:
    """Extract (workflow_name, event_member, from_step, to_step) tuples from WORKFLOW_REGISTRY transitions."""
    tree = ast.parse(source)
    tuples: set[tuple[str, str, str, str]] = set()

    # Build variable_name -> workflow_name mapping from WORKFLOW_REGISTRY
    workflow_vars: dict[str, str] = {}  # variable_name -> workflow_name

    for node in ast.walk(tree):
        # Handle annotated assignment: WORKFLOW_REGISTRY: dict[...] = {...}
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "WORKFLOW_REGISTRY":
                if isinstance(node.value, ast.Dict):
                    for key, value in zip(node.value.keys, node.value.values):
                        if isinstance(key, ast.Constant) and isinstance(key.value, str) and isinstance(value, ast.Name):
                            workflow_vars[value.id] = key.value
        # Handle regular assignment
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "WORKFLOW_REGISTRY":
                    if isinstance(node.value, ast.Dict):
                        for key, value in zip(node.value.keys, node.value.values):
                            if (
                                isinstance(key, ast.Constant)
                                and isinstance(key.value, str)
                                and isinstance(value, ast.Name)
                            ):
                                workflow_vars[value.id] = key.value

    # For each workflow variable assignment, delegate WorkflowTransition extraction to
    # the helper so that multiple transitions sharing the same event (e.g. MANUAL_ADVANCE
    # across several steps) each produce a distinct 4-tuple.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in workflow_vars:
                    workflow_name = workflow_vars[target.id]
                    for event, from_step, to_step in _extract_workflow_transitions(workflow_name, node.value):
                        tuples.add((workflow_name, event, from_step, to_step))
    return tuples


def _parse_mapping_doc(doc_text: str) -> tuple[set[str], set[str], set[tuple[str, str, str, str]]]:
    """Parse the mapping document and return (events_found, workflows_found, transitions_found).

    ``transitions_found`` contains ``(workflow, event, legacy_from_step, legacy_to_step)``
    4-tuples.  Rows where ``legacy_from_step`` or ``legacy_to_step`` are placeholder strings
    (e.g. ``"N/A — not yet implemented"``) are excluded from the transition set because they
    don't correspond to real transitions in the registry.
    """
    events_found: set[str] = set()
    workflows_found: set[str] = set()
    transitions_found: set[tuple[str, str, str, str]] = set()

    _SKIP_MARKERS = {"N/A — not yet implemented", "N/A"}

    for line in doc_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 6:
            continue
        workflow = cells[1]
        event = cells[2]
        legacy_from = cells[3]
        legacy_to = cells[4]

        # Skip header rows
        if workflow in ("Workflow", "---", "--------", ""):
            continue
        if event.startswith("---"):
            continue

        workflows_found.add(workflow)
        if event and event not in _SKIP_MARKERS:
            events_found.add(event)
            if legacy_from not in _SKIP_MARKERS and legacy_to not in _SKIP_MARKERS:
                transitions_found.add((workflow, event, legacy_from, legacy_to))

    return events_found, workflows_found, transitions_found


def main() -> int:
    """Run all validation checks."""
    if not MANAGER_PATH.exists():
        print(f"ERROR: {MANAGER_PATH} not found", file=sys.stderr)
        return 1
    if not MAPPING_DOC_PATH.exists():
        print(f"ERROR: {MAPPING_DOC_PATH} not found", file=sys.stderr)
        return 1

    source = MANAGER_PATH.read_text()
    doc_text = MAPPING_DOC_PATH.read_text()

    enum_members = _parse_workflow_event_members(source)
    registry_workflows = _parse_workflow_registry_names(source)
    registry_transitions = _parse_workflow_event_transitions(source)

    doc_events, doc_workflows, doc_transitions = _parse_mapping_doc(doc_text)

    errors: list[str] = []

    if not enum_members:
        errors.append("Could not parse WorkflowEvent enum members from manager.py")
    if not registry_workflows:
        errors.append("Could not parse WORKFLOW_REGISTRY workflow names from manager.py")
    if not registry_transitions:
        errors.append("Could not parse trigger_events transitions from manager.py")

    # (a) Every enum member must appear in the doc
    for member in sorted(enum_members):
        if member not in doc_events:
            errors.append(f"Missing enum member in mapping doc: {member}")

    # (b) Every workflow in registry must appear in the doc
    for workflow in sorted(registry_workflows):
        if workflow not in doc_workflows:
            errors.append(f"Missing workflow in mapping doc: {workflow}")

    # (c) Every (workflow, event, from_step, to_step) transition from the registry must
    #     have a corresponding row in the mapping doc.  Validating the full 4-tuple
    #     (rather than just (workflow, event)) catches cases where the same event (e.g.
    #     MANUAL_ADVANCE) triggers multiple distinct transitions within a workflow.
    for workflow, event, from_step, to_step in sorted(registry_transitions):
        if (workflow, event, from_step, to_step) not in doc_transitions:
            errors.append(
                f"Missing (workflow, event, from_step, to_step) row: ({workflow}, {event}, {from_step}, {to_step})"
            )

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1

    print(
        f"OK: All {len(enum_members)} enum members, {len(registry_workflows)} workflows, "
        f"and {len(registry_transitions)} (workflow, event, from_step, to_step) transitions are documented."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
