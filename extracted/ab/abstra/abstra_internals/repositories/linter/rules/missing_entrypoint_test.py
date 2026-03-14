from abstra_internals.repositories.linter.rules.missing_entrypoint import (
    AddEntrypoint,
    DeleteStage,
    MissingEntrypoint,
)
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
    ScriptStage,
    WorkflowTransition,
)
from tests.fixtures import BaseTest


class MissingEntrypointTest(BaseTest):
    def test_missing_entrypoint_valid_default(self):
        rule = MissingEntrypoint()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_missing_entrypoint_valid_with_entrypoint(self):
        self.controller.create_tasklet("New script", "script.py")
        self.controller.create_form("New form", "form.py")
        self.controller.create_hook("New hook", "hook.py")
        self.controller.create_job("New job", "job.py")
        rule = MissingEntrypoint()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_missing_entrypoint_invalid_without_entrypoint(self):
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.unlink()
        rule = MissingEntrypoint()
        self.assertEqual(len(rule.find_issues()), 1)

        self.assertEqual(rule.find_issues()[0].fixes[0], AddEntrypoint(script))

        rule.find_issues()[0].fixes[0].fix()

        self.assertEqual(len(rule.find_issues()), 0)

    def test_missing_entrypoint_has_delete_stage_fix(self):
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.unlink()
        rule = MissingEntrypoint()
        issues = rule.find_issues()

        self.assertEqual(len(issues), 1)
        self.assertEqual(len(issues[0].fixes), 2)
        self.assertEqual(issues[0].fixes[1], DeleteStage(script))

    def test_delete_stage_fix_removes_stage(self):
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.unlink()
        rule = MissingEntrypoint()
        issues = rule.find_issues()

        delete_fix = issues[0].fixes[1]
        delete_fix.fix()

        project = LocalProjectRepository().load()
        self.assertIsNone(project.get_stage(script.id))
        self.assertEqual(len(rule.find_issues()), 0)

    def test_delete_stage_fix_removes_transitions_to_stage(self):
        project_repository = LocalProjectRepository()
        project = project_repository.load()

        script1 = ScriptStage(
            id="script1",
            file="script1.py",
            title="Script 1",
            workflow_position=(0, 0),
            workflow_transitions=[
                WorkflowTransition(
                    id="transition1",
                    target_type="scripts",
                    target_id="script2",
                    type="task",
                    task_type=None,
                )
            ],
        )
        script2 = ScriptStage(
            id="script2",
            file="script2.py",
            title="Script 2",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        project.scripts.append(script1)
        project.scripts.append(script2)
        project_repository.save(project)

        (self.root / "script1.py").write_text("print('hello')")

        rule = MissingEntrypoint()
        issues = rule.find_issues()

        self.assertEqual(len(issues), 1)
        delete_fix = issues[0].fixes[1]
        delete_fix.fix()

        project = project_repository.load()
        self.assertIsNone(project.get_stage("script2"))
        script1_reloaded = project.get_stage("script1")
        self.assertIsNotNone(script1_reloaded)
        assert script1_reloaded is not None  # for type checker
        self.assertEqual(len(script1_reloaded.workflow_transitions), 0)
