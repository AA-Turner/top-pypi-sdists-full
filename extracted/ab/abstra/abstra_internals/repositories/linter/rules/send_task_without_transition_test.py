import unittest

from abstra_internals.repositories.linter.rules.send_task_without_transition import (
    SendTaskWithoutTransition,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
    ScriptStage,
    WorkflowTransition,
)
from tests.fixtures import clear_dir, init_dir


class SendTaskWithoutTransitionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = init_dir()
        self.project_repository = LocalProjectRepository()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def test_no_issues_when_no_stages(self):
        rule = SendTaskWithoutTransition()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_no_issues_when_stage_has_no_send_task(self):
        project = self.project_repository.load()
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[],
        )
        project.scripts.append(script)
        self.project_repository.save(project)

        # Create the script file without send_task
        (self.root / "script.py").write_text("print('hello')")

        rule = SendTaskWithoutTransition()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_no_issues_when_send_task_has_matching_transition(self):
        project = self.project_repository.load()
        target_script = ScriptStage(
            id="target_script",
            file="target.py",
            title="Target Script",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[
                WorkflowTransition(
                    id="1",
                    target_type="script",
                    target_id="target_script",
                    type="task",
                    task_type="my_task",
                )
            ],
        )
        project.scripts.append(script)
        project.scripts.append(target_script)
        self.project_repository.save(project)

        # Create script files
        (self.root / "script.py").write_text(
            'from abstra.tasks import send_task\nsend_task("my_task", {})'
        )
        (self.root / "target.py").write_text("print('target')")

        rule = SendTaskWithoutTransition()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_no_issues_when_transition_has_no_task_type(self):
        """Transitions with no task_type should accept any task type."""
        project = self.project_repository.load()
        target_script = ScriptStage(
            id="target_script",
            file="target.py",
            title="Target Script",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[
                WorkflowTransition(
                    id="1",
                    target_type="script",
                    target_id="target_script",
                    type="task",
                    task_type=None,  # Accepts any task type
                )
            ],
        )
        project.scripts.append(script)
        project.scripts.append(target_script)
        self.project_repository.save(project)

        # Create script files
        (self.root / "script.py").write_text(
            'from abstra.tasks import send_task\nsend_task("any_task_type", {})'
        )
        (self.root / "target.py").write_text("print('target')")

        rule = SendTaskWithoutTransition()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_issue_when_send_task_has_no_matching_transition(self):
        project = self.project_repository.load()
        target_script = ScriptStage(
            id="target_script",
            file="target.py",
            title="Target Script",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[
                WorkflowTransition(
                    id="1",
                    target_type="script",
                    target_id="target_script",
                    type="task",
                    task_type="different_task",  # Different task type
                )
            ],
        )
        project.scripts.append(script)
        project.scripts.append(target_script)
        self.project_repository.save(project)

        # Create script files
        (self.root / "script.py").write_text(
            'from abstra.tasks import send_task\nsend_task("my_task", {})'
        )
        (self.root / "target.py").write_text("print('target')")

        rule = SendTaskWithoutTransition()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("my_task", issues[0].label)
        self.assertIn("Script", issues[0].label)

    def test_issue_when_stage_has_no_transitions(self):
        project = self.project_repository.load()
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[],  # No transitions at all
        )
        project.scripts.append(script)
        self.project_repository.save(project)

        # Create the script file
        (self.root / "script.py").write_text(
            'from abstra.tasks import send_task\nsend_task("my_task", {})'
        )

        rule = SendTaskWithoutTransition()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("my_task", issues[0].label)

    def test_ignores_non_literal_task_type(self):
        """Should not report issues when task type is a variable (not a string literal)."""
        project = self.project_repository.load()
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[],
        )
        project.scripts.append(script)
        self.project_repository.save(project)

        # Create the script file with variable task type
        (self.root / "script.py").write_text(
            'from abstra.tasks import send_task\ntask_type = "my_task"\nsend_task(task_type, {})'
        )

        rule = SendTaskWithoutTransition()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_handles_import_alias(self):
        """Should detect send_task when imported with alias."""
        project = self.project_repository.load()
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[],
        )
        project.scripts.append(script)
        self.project_repository.save(project)

        # Create the script file with aliased import
        (self.root / "script.py").write_text(
            'from abstra.tasks import send_task as st\nst("my_task", {})'
        )

        rule = SendTaskWithoutTransition()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("my_task", issues[0].label)

    def test_handles_module_import(self):
        """Should detect send_task when using module import style."""
        project = self.project_repository.load()
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[],
        )
        project.scripts.append(script)
        self.project_repository.save(project)

        # Create the script file with module import
        (self.root / "script.py").write_text(
            'import abstra.tasks as at\nat.send_task("my_task", {})'
        )

        rule = SendTaskWithoutTransition()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("my_task", issues[0].label)

    def test_multiple_send_task_calls(self):
        """Should report issues for each send_task call without matching transition."""
        project = self.project_repository.load()
        target_script = ScriptStage(
            id="target_script",
            file="target.py",
            title="Target Script",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[
                WorkflowTransition(
                    id="1",
                    target_type="script",
                    target_id="target_script",
                    type="task",
                    task_type="success",
                )
            ],
        )
        project.scripts.append(script)
        project.scripts.append(target_script)
        self.project_repository.save(project)

        # Create script file with multiple send_task calls
        (self.root / "script.py").write_text(
            """from abstra.tasks import send_task
send_task("success", {})  # Has matching transition
send_task("error_a", {})  # No matching transition
send_task("error_b", {})  # No matching transition
"""
        )
        (self.root / "target.py").write_text("print('target')")

        rule = SendTaskWithoutTransition()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 2)

        task_types_in_issues = [i.label for i in issues]
        self.assertTrue(any("error_a" in label for label in task_types_in_issues))
        self.assertTrue(any("error_b" in label for label in task_types_in_issues))
        self.assertFalse(any("'success'" in label for label in task_types_in_issues))

    def test_issue_resolved_after_adding_transition(self):
        """
        This test simulates the user scenario:
        1. Create a stage with send_task but no transition -> linter reports issue
        2. Add a matching transition -> linter should NOT report issue anymore
        """
        # Step 1: Create a stage with send_task but no transition
        project = self.project_repository.load()
        target_script = ScriptStage(
            id="target_script",
            file="target.py",
            title="Target Script",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        script = ScriptStage(
            id="script",
            file="script.py",
            title="Script",
            workflow_position=(0, 0),
            workflow_transitions=[],  # No transitions initially
        )
        project.scripts.append(script)
        project.scripts.append(target_script)
        self.project_repository.save(project)

        # Create script files
        (self.root / "script.py").write_text(
            'from abstra.tasks import send_task\nsend_task("my_task", {})'
        )
        (self.root / "target.py").write_text("print('target')")

        # Verify linter reports the issue
        rule = SendTaskWithoutTransition()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("my_task", issues[0].label)

        # Step 2: Add a matching transition
        project = self.project_repository.load()
        source_stage = None
        for stage in project.scripts:
            if stage.id == "script":
                source_stage = stage
                break

        self.assertIsNotNone(source_stage)
        assert source_stage is not None  # for type narrowing
        source_stage.workflow_transitions.append(
            WorkflowTransition(
                id="1",
                target_type="script",
                target_id="target_script",
                type="task",
                task_type="my_task",
            )
        )
        self.project_repository.save(project)

        # Verify linter NO LONGER reports the issue
        rule = SendTaskWithoutTransition()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 0)
