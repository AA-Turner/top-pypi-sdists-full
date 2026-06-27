from typing import Union

from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.project.project import (
    FormStage,
    LocalProjectRepository,
    PageStage,
    Project,
)
from abstra_internals.utils.file import generate_conflictless_path, is_path_in_conflict

StageWithPath = Union[FormStage, PageStage]


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


class ConflictingPathFound(LinterIssue):
    type = "error"
    fixes = []

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


class ConflictingPath(LinterRule):
    label = "Conflicting path"
    type = "error"

    def find_issues(self):
        project_repository = LocalProjectRepository()
        project = project_repository.load()

        issues = []
        for form in project.forms:
            if is_path_in_conflict(form.path):
                issues.append(ConflictingPathFound(form, project, project_repository))

        for page in project.pages:
            if is_path_in_conflict(page.path):
                issues.append(ConflictingPathFound(page, project, project_repository))

        return issues
