import subprocess
import sys
from typing import List, Optional

from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.services.requirements import (
    RequirementsRepository,
    analyze_project_imports,
)
from abstra_internals.settings import Settings


class AddPackageToRequirements(LinterFix):
    """Fix that adds a missing package to requirements.txt."""

    def __init__(self, package_name: str, version: Optional[str] = None):
        self.package_name = package_name
        self.version = version
        self.label = f"Add {package_name} to requirements.txt"

    @property
    def name(self):
        return f"AddPackageToRequirements:{self.package_name}"

    def fix(self):
        requirements = RequirementsRepository.load()
        requirements.add(self.package_name, self.version)
        RequirementsRepository.save(requirements)


class InstallRequirements(LinterFix):
    """Fix that installs missing packages from requirements.txt."""

    def __init__(self):
        self.label = "Install missing packages"

    def fix(self):
        requirements_path = Settings.root_path / "requirements.txt"
        if not requirements_path.exists():
            return

        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
            check=False,
        )


class MissingPackageInRequirements(LinterIssue):
    """Issue when an installed/available package is not in requirements.txt."""

    def __init__(self, package_name: str, import_name: str, file_path: str, line: int):
        self.package_name = package_name
        self.import_name = import_name
        self.file_path = file_path
        self.line = line

        if import_name != package_name:
            self.label = (
                f"Package '{package_name}' (imported as '{import_name}') "
                f"in {file_path}:{line} is not in requirements.txt"
            )
        else:
            self.label = (
                f"Package '{package_name}' imported in {file_path}:{line} "
                f"is not in requirements.txt"
            )
        self.fixes = [AddPackageToRequirements(package_name)]


class UninstalledLibsInRequirements(LinterIssue):
    """Issue when requirements.txt has libs that are not installed."""

    def __init__(self, uninstalled_libs: List[str]):
        self.uninstalled_libs = uninstalled_libs
        libs_str = ", ".join(uninstalled_libs)
        self.label = (
            f"The following packages in requirements.txt are not installed: {libs_str}. "
            f"Run 'pip install -r requirements.txt' to install them."
        )
        self.fixes = [InstallRequirements()]


class InvalidImport(LinterIssue):
    """Issue when an import cannot be resolved and doesn't exist on PyPI."""

    def __init__(self, import_name: str, file_path: str, line: int):
        self.import_name = import_name
        self.file_path = file_path
        self.line = line
        self.label = (
            f"Import '{import_name}' in {file_path}:{line} was not found on PyPI. "
            f"Please check if the package name is correct."
        )
        self.fixes = []


class ImportsRequirementsAnalyzer(LinterRule):
    """
    Unified analyzer for imports and requirements.txt.

    Uses the shared analyze_project_imports() function from services.requirements
    to ensure consistent behavior across the codebase.
    """

    label = "Import and requirements analysis"
    type = "bug"

    def find_issues(self) -> List[LinterIssue]:
        issues: List[LinterIssue] = []

        # Use the shared analysis function
        results, uninstalled_libs = analyze_project_imports(skip_pypi_check=False)

        # Report uninstalled libs first
        if uninstalled_libs:
            issues.append(UninstalledLibsInRequirements(uninstalled_libs))

        # Convert analysis results to linter issues
        for result in results:
            file_path = str(result.file_path) if result.file_path else ""

            if result.status == "missing_in_requirements":
                issues.append(
                    MissingPackageInRequirements(
                        package_name=result.package_name,
                        import_name=result.import_name,
                        file_path=file_path,
                        line=result.line,
                    )
                )
            elif result.status == "invalid_import":
                issues.append(
                    InvalidImport(
                        import_name=result.import_name,
                        file_path=file_path,
                        line=result.line,
                    )
                )
            # "unknown" status is skipped (can't determine due to uninstalled libs)
            # "ok" status is also skipped (no issue)

        return issues
