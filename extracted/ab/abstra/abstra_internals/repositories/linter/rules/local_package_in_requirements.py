from typing import List

from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.services.requirements import (
    RequirementsRepository,
    is_local_module,
)
from abstra_internals.settings import Settings


class RemoveConflictingPackage(LinterFix):
    """Fix that removes a conflicting package from requirements.txt"""

    def __init__(self, pkg_name: str) -> None:
        super().__init__()
        self.pkg_name = pkg_name
        self.label = f'Remove "{pkg_name}" from requirements.txt'

    def fix(self):
        requirements = RequirementsRepository.load()
        requirements.delete(self.pkg_name)
        RequirementsRepository.save(requirements)

        # If it's a folder without __init__.py, add it
        pkg_dir = Settings.root_path / self.pkg_name
        if pkg_dir.is_dir():
            init_file = pkg_dir / "__init__.py"
            if not init_file.exists():
                init_file.touch()

    def __hash__(self) -> int:
        return hash(self.pkg_name)


class LocalPackageInRequirementsFound(LinterIssue):
    """Issue when a package in requirements.txt conflicts with a local module"""

    def __init__(self, pkg_name: str, is_file: bool) -> None:
        self.pkg_name = pkg_name
        if is_file:
            self.label = f'Package "{pkg_name}" in requirements.txt conflicts with local file "{pkg_name}.py"'
        else:
            self.label = f'Package "{pkg_name}" in requirements.txt conflicts with local folder "{pkg_name}/"'
        self.fixes: List[LinterFix] = [RemoveConflictingPackage(pkg_name)]


class LocalPackageInRequirements(LinterRule):
    """
    Detects when a package in requirements.txt has the same name as a local module.

    This can cause import conflicts where Python imports the external package
    instead of the local module, leading to ModuleNotFoundError for local submodules.

    Example:
        - Local folder: utils/jira_data_processor.py
        - requirements.txt: utils
        - Import: from utils.jira_data_processor import X
        - Result: ModuleNotFoundError because Python imports the PyPI 'utils' package
    """

    label = "Local module found in requirements.txt"
    type = "error"

    def find_issues(self) -> List[LinterIssue]:
        issues: List[LinterIssue] = []
        requirements = RequirementsRepository.load()
        root = Settings.root_path

        for lib in requirements.libraries:
            pkg_name = lib.name

            if not is_local_module(pkg_name):
                continue

            # Determine if it's a file or folder conflict
            is_file = (root / f"{pkg_name}.py").exists()

            issues.append(
                LocalPackageInRequirementsFound(
                    pkg_name=pkg_name,
                    is_file=is_file,
                )
            )

        return issues
