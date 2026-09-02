"""Tests for scripts/validate_event_mapping.py."""

from __future__ import annotations

import importlib.util
import textwrap
from pathlib import Path
from unittest.mock import patch


def _load_module():
    """Load scripts/validate_event_mapping.py as a module."""
    repo_root = Path(__file__).resolve().parents[1]
    script_path = repo_root / "scripts" / "validate_event_mapping.py"
    spec = importlib.util.spec_from_file_location("validate_event_mapping", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load validate_event_mapping.py from {script_path!s}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = _load_module()


# ---------------------------------------------------------------------------
# _parse_workflow_event_members
# ---------------------------------------------------------------------------


class TestParseWorkflowEventMembers:
    """Tests for _parse_workflow_event_members()."""

    def test_returns_enum_member_names(self):
        src = textwrap.dedent("""\
            class WorkflowEvent:
                PLAN_POSTED = "plan_posted"
                CHECKLIST_COMPLETE = "checklist_complete"
        """)
        result = validator._parse_workflow_event_members(src)
        assert result == {"PLAN_POSTED", "CHECKLIST_COMPLETE"}

    def test_returns_empty_when_class_missing(self):
        src = "x = 1"
        assert validator._parse_workflow_event_members(src) == set()

    def test_returns_empty_for_empty_class(self):
        src = textwrap.dedent("""\
            class WorkflowEvent:
                pass
        """)
        assert validator._parse_workflow_event_members(src) == set()

    def test_ignores_other_classes(self):
        src = textwrap.dedent("""\
            class OtherClass:
                MEMBER = "value"
            class WorkflowEvent:
                REAL = "real"
        """)
        result = validator._parse_workflow_event_members(src)
        assert result == {"REAL"}

    def test_single_member(self):
        src = textwrap.dedent("""\
            class WorkflowEvent:
                MANUAL_ADVANCE = "manual_advance"
        """)
        assert validator._parse_workflow_event_members(src) == {"MANUAL_ADVANCE"}


# ---------------------------------------------------------------------------
# _parse_workflow_registry_names
# ---------------------------------------------------------------------------


class TestParseWorkflowRegistryNames:
    """Tests for _parse_workflow_registry_names()."""

    def test_annotated_assignment(self):
        src = textwrap.dedent("""\
            WORKFLOW_REGISTRY: dict[str, WorkflowDefinition] = {
                "work-on-jira-issue": work_on_jira_issue,
                "pull-request-review": pull_request_review,
            }
        """)
        result = validator._parse_workflow_registry_names(src)
        assert result == {"work-on-jira-issue", "pull-request-review"}

    def test_regular_assignment(self):
        src = textwrap.dedent("""\
            WORKFLOW_REGISTRY = {
                "my-workflow": my_workflow_def,
            }
        """)
        result = validator._parse_workflow_registry_names(src)
        assert result == {"my-workflow"}

    def test_returns_empty_when_registry_missing(self):
        src = "x = 1"
        assert validator._parse_workflow_registry_names(src) == set()

    def test_single_workflow(self):
        src = textwrap.dedent("""\
            WORKFLOW_REGISTRY: dict[str, object] = {
                "solo-workflow": solo_def,
            }
        """)
        assert validator._parse_workflow_registry_names(src) == {"solo-workflow"}


# ---------------------------------------------------------------------------
# _parse_workflow_event_transitions
# ---------------------------------------------------------------------------


class TestParseWorkflowEventTransitions:
    """Tests for _parse_workflow_event_transitions()."""

    def test_extracts_4_tuple(self):
        src = textwrap.dedent("""\
            my_workflow = WorkflowDefinition(
                transitions=[
                    WorkflowTransition(
                        trigger_events={WorkflowEvent.PLAN_POSTED},
                        from_step="planning",
                        to_step="checklist_creation",
                    ),
                ]
            )
            WORKFLOW_REGISTRY: dict[str, object] = {
                "work-on-jira-issue": my_workflow,
            }
        """)
        result = validator._parse_workflow_event_transitions(src)
        assert ("work-on-jira-issue", "PLAN_POSTED", "planning", "checklist_creation") in result

    def test_multiple_events_same_transition(self):
        src = textwrap.dedent("""\
            my_workflow = WorkflowDefinition(
                transitions=[
                    WorkflowTransition(
                        trigger_events={WorkflowEvent.EVENT_A, WorkflowEvent.EVENT_B},
                        from_step="step_a",
                        to_step="step_b",
                    ),
                ]
            )
            WORKFLOW_REGISTRY = {"wf": my_workflow}
        """)
        result = validator._parse_workflow_event_transitions(src)
        assert ("wf", "EVENT_A", "step_a", "step_b") in result
        assert ("wf", "EVENT_B", "step_a", "step_b") in result

    def test_returns_empty_when_no_registry(self):
        src = "x = 1"
        assert validator._parse_workflow_event_transitions(src) == set()

    def test_multiple_transitions(self):
        src = textwrap.dedent("""\
            wf = WorkflowDefinition(
                transitions=[
                    WorkflowTransition(
                        trigger_events={WorkflowEvent.EV1},
                        from_step="s1",
                        to_step="s2",
                    ),
                    WorkflowTransition(
                        trigger_events={WorkflowEvent.EV2},
                        from_step="s2",
                        to_step="s3",
                    ),
                ]
            )
            WORKFLOW_REGISTRY = {"my-wf": wf}
        """)
        result = validator._parse_workflow_event_transitions(src)
        assert ("my-wf", "EV1", "s1", "s2") in result
        assert ("my-wf", "EV2", "s2", "s3") in result
        assert len(result) == 2


# ---------------------------------------------------------------------------
# _parse_mapping_doc
# ---------------------------------------------------------------------------


class TestParseMappingDoc:
    """Tests for _parse_mapping_doc()."""

    def test_parses_basic_row(self):
        doc = textwrap.dedent("""\
            | Workflow | Event | From Step | To Step | LangGraph |
            | --- | --- | --- | --- | --- |
            | work-on-jira-issue | PLAN_POSTED | planning | checklist_creation | route_after_plan |
        """)
        events, workflows, transitions = validator._parse_mapping_doc(doc)
        assert "PLAN_POSTED" in events
        assert "work-on-jira-issue" in workflows
        assert ("work-on-jira-issue", "PLAN_POSTED", "planning", "checklist_creation") in transitions

    def test_skips_header_rows(self):
        doc = textwrap.dedent("""\
            | Workflow | Event | From Step | To Step | LangGraph |
            | -------- | ----- | --------- | ------- | --------- |
            | work-on-jira-issue | EV | step1 | step2 | fn |
        """)
        _, workflows, _ = validator._parse_mapping_doc(doc)
        assert "Workflow" not in workflows
        assert "work-on-jira-issue" in workflows

    def test_skips_na_from_step(self):
        doc = "| my-wf | MY_EVENT | N/A — not yet implemented | step2 | fn |\n"
        _, _, transitions = validator._parse_mapping_doc(doc)
        assert len(transitions) == 0

    def test_skips_na_to_step(self):
        doc = "| my-wf | MY_EVENT | step1 | N/A | fn |\n"
        _, _, transitions = validator._parse_mapping_doc(doc)
        assert len(transitions) == 0

    def test_multiple_rows(self):
        doc = textwrap.dedent("""\
            | wf1 | EV1 | s1 | s2 | fn1 |
            | wf2 | EV2 | s3 | s4 | fn2 |
        """)
        events, workflows, transitions = validator._parse_mapping_doc(doc)
        assert events == {"EV1", "EV2"}
        assert workflows == {"wf1", "wf2"}
        assert len(transitions) == 2

    def test_ignores_non_table_lines(self):
        doc = textwrap.dedent("""\
            # Heading
            Some prose text.
            | wf | EV | from | to | fn |
        """)
        _, workflows, _ = validator._parse_mapping_doc(doc)
        assert "wf" in workflows

    def test_skips_rows_with_too_few_cells(self):
        doc = "| only | two |\n"
        events, workflows, transitions = validator._parse_mapping_doc(doc)
        assert len(transitions) == 0


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


class TestMain:
    """Tests for main() exit codes."""

    def test_returns_1_when_manager_missing(self, tmp_path):
        with (
            patch.object(validator, "MANAGER_PATH", tmp_path / "nonexistent.py"),
            patch.object(validator, "MAPPING_DOC_PATH", tmp_path / "doc.md"),
        ):
            assert validator.main() == 1

    def test_returns_1_when_mapping_doc_missing(self, tmp_path):
        manager = tmp_path / "manager.py"
        manager.write_text("")
        with (
            patch.object(validator, "MANAGER_PATH", manager),
            patch.object(validator, "MAPPING_DOC_PATH", tmp_path / "nonexistent.md"),
        ):
            assert validator.main() == 1

    def test_returns_1_when_enum_member_missing_from_doc(self, tmp_path):
        manager = tmp_path / "manager.py"
        manager.write_text(
            textwrap.dedent("""\
            class WorkflowEvent:
                PLAN_POSTED = "plan_posted"
            wf = WorkflowDefinition(transitions=[
                WorkflowTransition(
                    trigger_events={WorkflowEvent.PLAN_POSTED},
                    from_step="planning",
                    to_step="checklist_creation",
                ),
            ])
            WORKFLOW_REGISTRY: dict[str, object] = {"work-on-jira-issue": wf}
        """)
        )
        # Doc is missing PLAN_POSTED entirely
        doc = tmp_path / "doc.md"
        doc.write_text("| work-on-jira-issue | OTHER_EVENT | planning | checklist_creation | fn |\n")
        with (
            patch.object(validator, "MANAGER_PATH", manager),
            patch.object(validator, "MAPPING_DOC_PATH", doc),
        ):
            assert validator.main() == 1

    def test_returns_1_when_transition_4tuple_missing_from_doc(self, tmp_path):
        manager = tmp_path / "manager.py"
        manager.write_text(
            textwrap.dedent("""\
            class WorkflowEvent:
                PLAN_POSTED = "plan_posted"
            wf = WorkflowDefinition(transitions=[
                WorkflowTransition(
                    trigger_events={WorkflowEvent.PLAN_POSTED},
                    from_step="planning",
                    to_step="checklist_creation",
                ),
            ])
            WORKFLOW_REGISTRY: dict[str, object] = {"work-on-jira-issue": wf}
        """)
        )
        # Doc has the event and workflow but wrong from_step/to_step
        doc = tmp_path / "doc.md"
        doc.write_text("| work-on-jira-issue | PLAN_POSTED | wrong_step | checklist_creation | fn |\n")
        with (
            patch.object(validator, "MANAGER_PATH", manager),
            patch.object(validator, "MAPPING_DOC_PATH", doc),
        ):
            assert validator.main() == 1

    def test_returns_0_when_all_checks_pass(self, tmp_path):
        manager = tmp_path / "manager.py"
        manager.write_text(
            textwrap.dedent("""\
            class WorkflowEvent:
                PLAN_POSTED = "plan_posted"
            wf = WorkflowDefinition(transitions=[
                WorkflowTransition(
                    trigger_events={WorkflowEvent.PLAN_POSTED},
                    from_step="planning",
                    to_step="checklist_creation",
                ),
            ])
            WORKFLOW_REGISTRY: dict[str, object] = {"work-on-jira-issue": wf}
        """)
        )
        doc = tmp_path / "doc.md"
        doc.write_text("| work-on-jira-issue | PLAN_POSTED | planning | checklist_creation | fn |\n")
        with (
            patch.object(validator, "MANAGER_PATH", manager),
            patch.object(validator, "MAPPING_DOC_PATH", doc),
        ):
            assert validator.main() == 0
