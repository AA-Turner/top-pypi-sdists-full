import unittest

from abstra_internals.repositories.linter.rules.stage_analyzer import (
    AddEntrypoint,
    ConflictingPathFound,
    DeleteStage,
    FileOutsideProject,
    InvalidJobScheduleFound,
    MoveFileToProjectRoot,
    NoEntrypointFound,
    StageAnalyzer,
    is_path_inside_root,
)
from abstra_internals.repositories.project.project import (
    FormStage,
    HookStage,
    JobStage,
    LocalProjectRepository,
    ScriptStage,
    WorkflowTransition,
)
from abstra_internals.settings import Settings
from tests.fixtures import BaseTest, clear_dir, init_dir


def _issues_of(issue_type):
    """The analyzer emits every stage verdict at once (a fixture stage whose
    file doesn't exist also trips the missing-entrypoint sub-check), so each
    test filters down to the sub-check under test."""
    return [i for i in StageAnalyzer().find_issues() if isinstance(i, issue_type)]


class ConflictingPathTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = init_dir()
        self.project_repository = LocalProjectRepository()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def test_conflicting_path_valid_default(self):
        self.assertEqual(len(_issues_of(ConflictingPathFound)), 0)

    def test_conflicting_path_without_conflict(self):
        project = self.project_repository.load()
        form = FormStage.create(
            id="test",
            title="test",
            file="test.py",
        )
        form.path = "not_conflicting_path"
        project.add_stage(form)
        self.project_repository.save(project)

        self.assertEqual(len(_issues_of(ConflictingPathFound)), 0)

    def test_conflicting_path_with_conflict(self):
        project = self.project_repository.load()
        form = FormStage.create(
            id="login",
            title="login",
            file="login.py",
        )
        form.path = "login"
        project.add_stage(form)
        self.project_repository.save(project)

        issues = _issues_of(ConflictingPathFound)
        self.assertEqual(len(issues), 1)

        issue = issues[0]
        self.assertEqual(len(issue.fixes), 1)

        issue.fixes[0].fix()
        self.assertEqual(len(_issues_of(ConflictingPathFound)), 0)


class MissingEntrypointTest(BaseTest):
    def _entrypoint_issues(self):
        return _issues_of(NoEntrypointFound)

    def test_missing_entrypoint_valid_default(self):
        self.assertEqual(len(self._entrypoint_issues()), 0)

    def test_missing_entrypoint_valid_with_entrypoint(self):
        self.controller.create_stage("tasklet", "New script", "script.py")
        self.controller.create_stage("form", "New form", "form.py")
        self.controller.create_stage("hook", "New hook", "hook.py")
        self.controller.create_stage("job", "New job", "job.py")
        self.assertEqual(len(self._entrypoint_issues()), 0)

    def test_missing_entrypoint_invalid_without_entrypoint(self):
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        script.file_path.unlink()
        issues = self._entrypoint_issues()
        self.assertEqual(len(issues), 1)

        self.assertEqual(issues[0].fixes[0], AddEntrypoint(script))

        issues[0].fixes[0].fix()

        self.assertEqual(len(self._entrypoint_issues()), 0)

    def test_missing_entrypoint_has_delete_stage_fix(self):
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        script.file_path.unlink()
        issues = self._entrypoint_issues()

        self.assertEqual(len(issues), 1)
        self.assertEqual(len(issues[0].fixes), 2)
        self.assertEqual(issues[0].fixes[1], DeleteStage(script))

    def test_delete_stage_fix_removes_stage(self):
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        script.file_path.unlink()
        issues = self._entrypoint_issues()

        delete_fix = issues[0].fixes[1]
        delete_fix.fix()

        project = LocalProjectRepository().load()
        self.assertIsNone(project.get_stage(script.id))
        self.assertEqual(len(self._entrypoint_issues()), 0)

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

        issues = self._entrypoint_issues()

        self.assertEqual(len(issues), 1)
        delete_fix = issues[0].fixes[1]
        delete_fix.fix()

        project = project_repository.load()
        self.assertIsNone(project.get_stage("script2"))
        script1_reloaded = project.get_stage("script1")
        self.assertIsNotNone(script1_reloaded)
        assert script1_reloaded is not None  # for type checker
        self.assertEqual(len(script1_reloaded.workflow_transitions), 0)


class FileOutsideProjectTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = init_dir()
        self.project_repository = LocalProjectRepository()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def _outside_issues(self):
        return _issues_of(FileOutsideProject)

    def _add_stage(self, stage):
        project = self.project_repository.load()
        project.add_stage(stage)
        self.project_repository.save(project)

    def test_no_issues_with_empty_project(self):
        self.assertEqual(len(self._outside_issues()), 0)

    def test_no_issues_with_valid_form(self):
        self._add_stage(
            FormStage.create(id="test-form", title="Test Form", file="form.py")
        )
        self.assertEqual(len(self._outside_issues()), 0)

    def test_no_issues_with_valid_hook(self):
        self._add_stage(
            HookStage.create(id="test-hook", title="Test Hook", file="hook.py")
        )
        self.assertEqual(len(self._outside_issues()), 0)

    def test_no_issues_with_valid_job(self):
        self._add_stage(JobStage.create(id="test-job", title="Test Job", file="job.py"))
        self.assertEqual(len(self._outside_issues()), 0)

    def test_no_issues_with_valid_script(self):
        self._add_stage(
            ScriptStage.create(id="test-script", title="Test Script", file="script.py")
        )
        self.assertEqual(len(self._outside_issues()), 0)

    def test_no_issues_with_nested_valid_path(self):
        self._add_stage(
            FormStage.create(
                id="test-form", title="Test Form", file="subdir/nested/form.py"
            )
        )
        self.assertEqual(len(self._outside_issues()), 0)

    def test_issue_with_parent_directory_traversal_form(self):
        self._add_stage(
            FormStage.create(
                id="test-form", title="Test Form", file="../outside_project.py"
            )
        )
        issues = self._outside_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("outside the project directory", issues[0].label)
        self.assertIn("Test Form", issues[0].label)
        self.assertEqual(len(issues[0].fixes), 1)
        self.assertIsInstance(issues[0].fixes[0], MoveFileToProjectRoot)

    def test_issue_with_parent_directory_traversal_hook(self):
        self._add_stage(
            HookStage.create(
                id="test-hook", title="Test Hook", file="../outside_hook.py"
            )
        )
        issues = self._outside_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("Test Hook", issues[0].label)

    def test_issue_with_parent_directory_traversal_job(self):
        self._add_stage(
            JobStage.create(id="test-job", title="Test Job", file="../outside_job.py")
        )
        issues = self._outside_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("Test Job", issues[0].label)

    def test_issue_with_parent_directory_traversal_script(self):
        self._add_stage(
            ScriptStage.create(
                id="test-script", title="Test Script", file="../outside_script.py"
            )
        )
        issues = self._outside_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("Test Script", issues[0].label)

    def test_issue_with_deeply_nested_parent_traversal(self):
        self._add_stage(
            FormStage.create(
                id="test-form", title="Test Form", file="../../deeply/outside.py"
            )
        )
        self.assertEqual(len(self._outside_issues()), 1)

    def test_multiple_issues_with_multiple_invalid_stages(self):
        project = self.project_repository.load()
        project.add_stage(
            FormStage.create(id="test-form", title="Bad Form", file="../bad_form.py")
        )
        project.add_stage(
            HookStage.create(id="test-hook", title="Bad Hook", file="../bad_hook.py")
        )
        # Valid stage should not create an issue
        project.add_stage(
            JobStage.create(id="test-job", title="Good Job", file="good_job.py")
        )
        self.project_repository.save(project)

        self.assertEqual(len(self._outside_issues()), 2)

    def test_no_issue_with_normalized_path_staying_inside(self):
        # A path like "subdir/../form.py" should resolve to "form.py" which is inside
        self._add_stage(
            FormStage.create(
                id="test-form", title="Test Form", file="subdir/../form.py"
            )
        )
        self.assertEqual(len(self._outside_issues()), 0)


class MoveFileFixTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = init_dir()
        self.project_repository = LocalProjectRepository()
        # Create parent directory for outside files
        self.parent_dir = self.root.parent

    def tearDown(self) -> None:
        # Clean up any files created in parent directory
        outside_file = self.parent_dir / "outside_form.py"
        if outside_file.exists():
            outside_file.unlink()
        clear_dir(self.root)

    def _add_form(self, file):
        project = self.project_repository.load()
        project.add_stage(
            FormStage.create(id="test-form", title="Test Form", file=file)
        )
        self.project_repository.save(project)

    def test_fix_moves_file_and_updates_project(self):
        # Create a file outside the project
        outside_file = self.parent_dir / "outside_form.py"
        outside_file.write_text("# test content")

        self._add_form("../outside_form.py")

        issues = _issues_of(FileOutsideProject)
        self.assertEqual(len(issues), 1)

        # Apply the fix
        fix = issues[0].fixes[0]
        self.assertEqual(fix.make_label(), "Move outside_form.py to project root")
        fix.fix()

        # Verify the file was moved
        new_file = Settings.root_path / "outside_form.py"
        self.assertTrue(new_file.exists())
        self.assertFalse(outside_file.exists())
        self.assertEqual(new_file.read_text(), "# test content")

        # Verify the project was updated
        self.assertEqual(len(_issues_of(FileOutsideProject)), 0)

        # Verify the stage file attribute was updated
        updated_project = self.project_repository.load()
        updated_form = updated_project.get_form("test-form")
        assert updated_form is not None
        self.assertEqual(updated_form.file, "outside_form.py")

    def test_fix_updates_project_even_if_file_does_not_exist(self):
        # Create a stage pointing to a non-existent file outside
        self._add_form("../nonexistent.py")

        issues = _issues_of(FileOutsideProject)
        self.assertEqual(len(issues), 1)

        issues[0].fixes[0].fix()

        # Verify the project was updated even though the file didn't exist
        self.assertEqual(len(_issues_of(FileOutsideProject)), 0)

        # Verify the stage file attribute was updated
        updated_project = self.project_repository.load()
        updated_form = updated_project.get_form("test-form")
        assert updated_form is not None
        self.assertEqual(updated_form.file, "nonexistent.py")

    def test_fix_extracts_filename_from_nested_path(self):
        # Create a file outside the project with nested path
        outside_file = self.parent_dir / "outside_form.py"
        outside_file.write_text("# nested content")

        self._add_form("../../some/path/outside_form.py")

        issues = _issues_of(FileOutsideProject)
        self.assertEqual(len(issues), 1)

        # Check the fix label extracts just the filename
        fix = issues[0].fixes[0]
        self.assertEqual(fix.make_label(), "Move outside_form.py to project root")

    def test_fix_preserves_existing_file_in_root_and_updates_reference(self):
        # File already exists in project root with correct content
        existing_file = Settings.root_path / "form.py"
        existing_file.write_text("# correct content in root")

        # abstra.json wrongly references a file outside the project
        self._add_form("../form.py")

        issues = _issues_of(FileOutsideProject)
        self.assertEqual(len(issues), 1)

        issues[0].fixes[0].fix()

        # Verify the existing file in root was NOT overwritten
        self.assertTrue(existing_file.exists())
        self.assertEqual(existing_file.read_text(), "# correct content in root")

        # Verify the project reference was updated
        self.assertEqual(len(_issues_of(FileOutsideProject)), 0)

        # Verify the stage file attribute was updated
        updated_project = self.project_repository.load()
        updated_form = updated_project.get_form("test-form")
        assert updated_form is not None
        self.assertEqual(updated_form.file, "form.py")


class IsPathInsideRootTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = init_dir()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def test_simple_file_inside(self):
        file_path = self.root / "file.py"
        self.assertTrue(is_path_inside_root(file_path, self.root))

    def test_nested_file_inside(self):
        file_path = self.root / "subdir" / "nested" / "file.py"
        self.assertTrue(is_path_inside_root(file_path, self.root))

    def test_parent_traversal_outside(self):
        file_path = self.root / ".." / "outside.py"
        self.assertFalse(is_path_inside_root(file_path, self.root))

    def test_double_parent_traversal_outside(self):
        file_path = self.root / ".." / ".." / "outside.py"
        self.assertFalse(is_path_inside_root(file_path, self.root))

    def test_traversal_that_stays_inside(self):
        file_path = self.root / "subdir" / ".." / "file.py"
        self.assertTrue(is_path_inside_root(file_path, self.root))

    def test_root_path_itself(self):
        self.assertTrue(is_path_inside_root(self.root, self.root))


class JobScheduleValidityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = init_dir()
        self.project_repository = LocalProjectRepository()

    def tearDown(self) -> None:
        clear_dir(self.root)

    def _add_job(self, *, id: str, title: str, file: str, schedule: str) -> None:
        project = self.project_repository.load()
        job = JobStage.create(id=id, title=title, file=file)
        job.schedule = schedule
        project.add_stage(job)
        self.project_repository.save(project)

    def _schedule_issues(self):
        return _issues_of(InvalidJobScheduleFound)

    def test_empty_project_has_no_issues(self):
        self.assertEqual(len(self._schedule_issues()), 0)

    def test_valid_schedule_passes(self):
        self._add_job(id="daily", title="Daily", file="daily.py", schedule="0 0 * * *")
        self.assertEqual(len(self._schedule_issues()), 0)

    def test_impossible_schedule_is_flagged(self):
        self._add_job(
            id="feb31", title="Feb 31 job", file="feb31.py", schedule="0 0 31 2 *"
        )
        issues = self._schedule_issues()
        self.assertEqual(len(issues), 1)
        # The job title surfaces in the message so the user knows which job to fix.
        self.assertIn("Feb 31 job", issues[0].label)

    def test_reports_one_issue_per_invalid_job_and_skips_valid_ones(self):
        self._add_job(
            id="feb31", title="Feb 31 job", file="feb31.py", schedule="0 0 31 2 *"
        )
        self._add_job(
            id="apr31", title="Apr 31 job", file="apr31.py", schedule="0 0 31 4 *"
        )
        self._add_job(id="ok", title="OK job", file="ok.py", schedule="0 0 * * *")
        self.assertEqual(len(self._schedule_issues()), 2)
