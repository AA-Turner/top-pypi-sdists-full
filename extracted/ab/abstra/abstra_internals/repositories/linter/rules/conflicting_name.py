from pathlib import Path
from pkgutil import iter_modules
from typing import List

from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.project.project import LocalProjectRepository
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings


class AddPreffix(LinterFix):
    label = "Fix conflicting name"
    preffix = "util_"

    def __init__(self, file: Path):
        self.file = file
        self.project_repository = LocalProjectRepository()

    def fix(self):
        new_file = self.file.parent / f"{self.preffix}{self.file.name}"

        self.file.rename(new_file)

        project = self.project_repository.load()

        for stage in project.get_stages_by_file_path(self.file):
            project.update_stage(stage, dict(file=str(new_file.name)))

        self.project_repository.save(project)


class ConflictingNameIssue(LinterIssue):
    type = "bug"
    fixes = []

    def __init__(self, file: Path):
        self.label = f"The name of the file {file.name} is in conflict with an internal reserved name. This can cause unexpected behavior. You can either change it manually in the Editor or use the 'Fix conflicting name' button."
        self.fixes = [AddPreffix(file)]


def reserved_names() -> List[str]:
    project_path = Path(Settings.root_path).resolve()
    return [
        m.name
        for m in iter_modules()
        if Path(getattr(m.module_finder, "path", "")).resolve() != project_path
    ]


class ConflictingName(LinterRule):
    label = "Conflicting path"
    type = "bug"

    def find_issues(self) -> List[LinterIssue]:
        root = Settings.root_path
        project_py_files = FileSystemService.list_files(root, allowed_suffixes=[".py"])

        _reserved_names = set((root / (name + ".py")) for name in reserved_names())

        return [
            ConflictingNameIssue(file)
            for file in _reserved_names.intersection(project_py_files)
        ]
