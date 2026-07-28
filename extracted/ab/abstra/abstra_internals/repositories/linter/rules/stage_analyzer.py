import shutil
from pathlib import Path
from typing import List, Union

from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.project.project import (
    FormStage,
    HookStage,
    JobStage,
    LocalProjectRepository,
    PageStage,
    Project,
    ScriptStage,
    StageWithFile,
)
from abstra_internals.settings import Settings
from abstra_internals.templates import (
    new_form_code,
    new_hook_code,
    new_job_code,
    new_page_code,
    new_script_code,
)
from abstra_internals.utils.cron import cron_schedule_error
from abstra_internals.utils.file import generate_conflictless_path, is_path_in_conflict

StageWithPath = Union[FormStage, PageStage]


def is_path_inside_root(file_path: Path, root_path: Path) -> bool:
    try:
        resolved_file = file_path.resolve()
        resolved_root = root_path.resolve()
        resolved_file.relative_to(resolved_root)
        return True
    except ValueError:
        return False


class ConflictingPathFix(LinterFix):
    label = "Fix conflicting path"
    description = "Change the path of the stage to avoid conflicts"

    def __init__(
        self,
        stage: StageWithPath,
        project: Project,
        project_repository: LocalProjectRepository,
    ):
        self.stage = stage
        self.project = project
        self.project_repository = project_repository

    def fix(self):
        self.project.update_stage(
            self.stage, {"path": generate_conflictless_path(self.stage.path)}
        )
        self.project_repository.save(self.project)


class AddEntrypoint(LinterFix):
    label = "Add entrypoint"
    description = "Creates the .py file for the entrypoint"
    stage: StageWithFile

    def __init__(self, stage: StageWithFile) -> None:
        self.stage = stage

    def make_label(self):
        return f"Create {self.stage.file}"

    def fix(self):
        if isinstance(self.stage, FormStage):
            self.stage.file_path.write_text(new_form_code, "utf-8")
        elif isinstance(self.stage, HookStage):
            self.stage.file_path.write_text(new_hook_code, "utf-8")
        elif isinstance(self.stage, JobStage):
            self.stage.file_path.write_text(new_job_code, "utf-8")
        elif isinstance(self.stage, ScriptStage):
            self.stage.file_path.write_text(new_script_code, "utf-8")
        elif isinstance(self.stage, PageStage):
            self.stage.file_path.write_text(new_page_code, "utf-8")
        else:
            raise Exception(f"Unknown stage: {self.stage}")

    @property
    def name(self):
        return (
            f"{self.__class__.__name__}:{self.stage.__class__.__name__}:{self.stage.id}"
        )


class DeleteStage(LinterFix):
    label = "Delete stage"

    def __init__(self, stage: StageWithFile) -> None:
        self.stage = stage

    def make_label(self):
        return f"Delete {self.stage.type_name} '{self.stage.title}'"

    def fix(self):
        repo = LocalProjectRepository()
        with repo.atomic() as project:
            project.delete_stage(self.stage.id)

    @property
    def name(self):
        return (
            f"{self.__class__.__name__}:{self.stage.__class__.__name__}:{self.stage.id}"
        )


class MoveFileToProjectRoot(LinterFix):
    label = "Move file to project root"

    def __init__(
        self,
        stage: StageWithFile,
        project: Project,
        project_repository: LocalProjectRepository,
    ):
        self.stage = stage
        self.project = project
        self.project_repository = project_repository

    def make_label(self):
        file_name = Path(self.stage.file).name
        return f"Move {file_name} to project root"

    def fix(self):
        old_path = self.stage.file_path
        file_name = Path(self.stage.file).name
        new_path = Settings.root_path / file_name

        if old_path.exists() and not new_path.exists():
            shutil.move(str(old_path), str(new_path))

        self.stage.file = file_name
        self.project_repository.save(self.project)


class ConflictingPathFound(LinterIssue):
    title = "Conflicting path"
    type = "error"

    def __init__(
        self,
        stage: StageWithPath,
        project: Project,
        project_repository: LocalProjectRepository,
    ):
        self.label = (
            f"The path of the {stage.type_name} '{stage.title}' is in conflict "
            f"with an internal reserved path. This can cause unexpected behavior. "
            f"You can either change it manually in the Editor or use the "
            f"'Fix conflicting path' button."
        )
        self.fixes = [ConflictingPathFix(stage, project, project_repository)]


class NoEntrypointFound(LinterIssue):
    title = "Pointed files should exist"
    type = "error"

    def __init__(self, stage: StageWithFile) -> None:
        self.label = f"The {stage.type_name} entitled {stage.title} points to a non-existent file: {stage.file}"
        self.fixes = [AddEntrypoint(stage), DeleteStage(stage)]


class FileOutsideProject(LinterIssue):
    title = "Stage files must be inside the project directory"
    type = "error"

    def __init__(
        self,
        stage: StageWithFile,
        project: Project,
        project_repository: LocalProjectRepository,
    ) -> None:
        self.label = f"The {stage.type_name} '{stage.title}' references a file outside the project directory: {stage.file_path}"
        self.fixes = [MoveFileToProjectRoot(stage, project, project_repository)]


class InvalidJobScheduleFound(LinterIssue):
    title = "Job schedules must be valid cron expressions"
    type = "error"
    fix_with_ai = True

    def __init__(self, job_title: str, schedule: str, reason: str) -> None:
        self.label = f'The job entitled {job_title} has an invalid schedule "{schedule}" because {reason}'
        self.fixes = []


def _conflicting_path_issues(
    project: Project, project_repository: LocalProjectRepository
) -> List[LinterIssue]:
    issues: List[LinterIssue] = []
    for form in project.forms:
        if is_path_in_conflict(form.path):
            issues.append(ConflictingPathFound(form, project, project_repository))

    for page in project.pages:
        if is_path_in_conflict(page.path):
            issues.append(ConflictingPathFound(page, project, project_repository))

    return issues


def _missing_entrypoint_issues(project: Project) -> List[LinterIssue]:
    issues: List[LinterIssue] = []
    for form in project.forms:
        if not form.file_path.exists():
            issues.append(NoEntrypointFound(form))

    for hook in project.hooks:
        if not hook.file_path.exists():
            issues.append(NoEntrypointFound(hook))

    for job in project.jobs:
        if not job.file_path.exists():
            issues.append(NoEntrypointFound(job))

    for script in project.scripts:
        if not script.file_path.exists():
            issues.append(NoEntrypointFound(script))

    for page in project.pages:
        if not page.file_path.exists():
            issues.append(NoEntrypointFound(page))

    return issues


def _file_outside_project_issues(
    project: Project, project_repository: LocalProjectRepository
) -> List[LinterIssue]:
    root_path = Settings.root_path
    issues: List[LinterIssue] = []

    for form in project.forms:
        if not is_path_inside_root(form.file_path, root_path):
            issues.append(FileOutsideProject(form, project, project_repository))

    for hook in project.hooks:
        if not is_path_inside_root(hook.file_path, root_path):
            issues.append(FileOutsideProject(hook, project, project_repository))

    for job in project.jobs:
        if not is_path_inside_root(job.file_path, root_path):
            issues.append(FileOutsideProject(job, project, project_repository))

    for script in project.scripts:
        if not is_path_inside_root(script.file_path, root_path):
            issues.append(FileOutsideProject(script, project, project_repository))

    return issues


def _invalid_job_schedule_issues(project: Project) -> List[LinterIssue]:
    issues: List[LinterIssue] = []
    for job in project.jobs:
        reason = cron_schedule_error(job.schedule)
        if reason is not None:
            issues.append(
                InvalidJobScheduleFound(
                    job_title=job.title,
                    schedule=job.schedule,
                    reason=reason,
                )
            )
    return issues


class StageAnalyzer(LinterRule):
    """Every project-stage verdict in one pass: conflicting routes, missing
    entrypoint files, files outside the project root, invalid job schedules.

    One shared project (the pass's LintContext) instead of per-rule loads —
    two of the merged rules bypassed the context and re-loaded the project on
    every pass. The fixes that persist changes also share one project
    instance, so applying several fixes in a row can't lose an earlier fix's
    mutation to a stale copy."""

    label = "Stage analysis"

    def find_issues(self) -> List[LinterIssue]:
        project = (current_lint_context() or LintContext()).project
        project_repository = LocalProjectRepository()
        return [
            *_conflicting_path_issues(project, project_repository),
            *_missing_entrypoint_issues(project),
            *_file_outside_project_issues(project, project_repository),
            *_invalid_job_schedule_issues(project),
        ]
