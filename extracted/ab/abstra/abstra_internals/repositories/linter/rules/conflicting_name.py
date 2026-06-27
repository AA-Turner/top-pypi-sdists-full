import threading
from pathlib import Path
from pkgutil import iter_modules
from typing import List, Optional

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
    type = "error"
    fixes = []

    def __init__(self, file: Path):
        self.label = f"The name of the file {file.name} is in conflict with an internal reserved name. This can cause unexpected behavior. You can either change it manually in the Editor or use the 'Fix conflicting name' button."
        self.fixes = [AddPreffix(file)]


def _compute_reserved_names(project_path: Path) -> List[str]:
    return [
        m.name
        for m in iter_modules()
        if Path(getattr(m.module_finder, "path", "")).resolve() != project_path
    ]


class _ReservedNamesCache:
    """iter_modules() scans the whole sys.path (with a resolve() per module) on
    every pass. The reserved set only changes when packages are installed/
    uninstalled, so cache it. Keyed by the resolved project path (root_path is
    excluded from the set, and the web editor / tests reuse the process across
    projects). The sidecar child refreshes it on the package-install pass
    (LocalLinterRepository._run_rules) so a package install is reflected."""

    _cache: Optional[List[str]] = None
    _project_path: Optional[str] = None
    _lock = threading.Lock()

    @classmethod
    def get(cls) -> List[str]:
        project_path = Path(Settings.root_path).resolve()
        key = str(project_path)
        with cls._lock:
            if cls._cache is not None and cls._project_path == key:
                return cls._cache
            cls._cache = _compute_reserved_names(project_path)
            cls._project_path = key
            return cls._cache

    @classmethod
    def invalidate(cls) -> None:
        with cls._lock:
            cls._cache = None
            cls._project_path = None


def reserved_names() -> List[str]:
    return _ReservedNamesCache.get()


class ConflictingName(LinterRule):
    label = "Conflicting path"
    type = "error"

    def find_issues(self) -> List[LinterIssue]:
        root = Settings.root_path
        project_py_files = FileSystemService.list_files(root, allowed_suffixes=[".py"])

        _reserved_names = set((root / (name + ".py")) for name in reserved_names())

        return [
            ConflictingNameIssue(file)
            for file in _reserved_names.intersection(project_py_files)
        ]
