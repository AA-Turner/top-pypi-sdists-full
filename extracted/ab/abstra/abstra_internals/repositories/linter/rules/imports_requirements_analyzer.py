from pathlib import Path
from typing import List, Optional

from abstra_internals.repositories.linter.context import (
    LintContext,
    current_lint_context,
)
from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.repositories.linter.process_actions import (
    restart_editor_and_workers,
)
from abstra_internals.services.requirements import (
    Requirements,
    RequirementsRepository,
    analyze_project_imports,
    create_requirement,
    get_installed_version,
)
from abstra_internals.settings import Settings

_RESTART_NOTICE = "Installing will restart the editor and may take up to 2 minutes."


class AddPackageToRequirements(LinterFix):
    """Fix that adds a missing package to requirements.txt, installing it
    if it isn't already present in the current environment."""

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

        if get_installed_version(self.package_name) is not None:
            # Already importable by freshly-spawned processes; nothing to do.
            return

        req = create_requirement(self.package_name, self.version)
        if Requirements([req]).install_succeeded():
            # The package is now on disk but invisible to the long-lived editor
            # and worker processes — restart both so the linter re-checks
            # against it, otherwise this issue would never clear (only a manual
            # editor restart would). A failed install leaves things as-is.
            restart_editor_and_workers("[InstallPackage]")


class InstallRequirements(LinterFix):
    """Fix that installs missing packages from requirements.txt."""

    def __init__(self):
        self.label = "Install missing packages"

    def fix(self):
        requirements_path = Settings.root_path / "requirements.txt"
        if not requirements_path.exists():
            return

        requirements = RequirementsRepository.load()
        if requirements.install_succeeded():
            # Restart so the just-installed packages become visible to the
            # editor/linter and worker processes (see restart_editor_and_workers).
            restart_editor_and_workers("[InstallPackage]")


class MissingPackageInRequirements(LinterIssue):
    """Issue when an installed/available package is not in requirements.txt."""

    def __init__(self, package_name: str, import_name: str, file_path: str, line: int):
        self.package_name = package_name
        self.import_name = import_name
        self.file_path = file_path
        self.line = line

        if import_name != package_name:
            label = (
                f"Package '{package_name}' (imported as '{import_name}') "
                f"in {file_path}:{line} is not in requirements.txt"
            )
        else:
            label = (
                f"Package '{package_name}' imported in {file_path}:{line} "
                f"is not in requirements.txt"
            )
        # This issue covers both an already-installed package missing from
        # requirements.txt (the fix just edits the file) and a not-yet-installed
        # one (the fix pip-installs it, which restarts the editor). Mirror the
        # fix's own gate so we only warn about the restart when it will happen.
        if get_installed_version(package_name) is None:
            label = f"{label}. {_RESTART_NOTICE}"
        self.label = label
        self.fixes = [AddPackageToRequirements(package_name)]


class UninstalledLibsInRequirements(LinterIssue):
    """Issue when requirements.txt has libs that are not installed."""

    def __init__(self, uninstalled_libs: List[str]):
        self.uninstalled_libs = uninstalled_libs
        libs_str = ", ".join(uninstalled_libs)
        self.label = (
            f"The following packages in requirements.txt are not installed: {libs_str}. "
            f"Run 'pip install -r requirements.txt' to install them. {_RESTART_NOTICE}"
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


class ImportsRequirementsAnalyzer(PathScopedLinterRule):
    """
    Unified analyzer for imports and requirements.txt.

    Uses the shared analyze_project_imports() function from services.requirements
    to ensure consistent behavior across the codebase.
    """

    label = "Import and requirements analysis"
    type = "bug"

    def find_issues(self, path: Optional[Path] = None) -> List[LinterIssue]:
        issues: List[LinterIssue] = []

        if path is not None:
            ctx = current_lint_context() or LintContext()
            key = linter_path_key(path)
            if key not in ctx.project_file_keys:
                return []
            # Verify on PyPI too (skip_pypi_check=False): a newly typed import
            # that isn't installed and doesn't exist on PyPI must be flagged on
            # the save, not only on a full pass. This stays cheap via the
            # long-lived PyPIVerificationCache (7-day, on-disk) — only a package
            # name never seen before hits the network; the rest are cache hits.
            results, _ = analyze_project_imports(skip_pypi_check=False, paths=[path])
        else:
            results, uninstalled_libs = analyze_project_imports(skip_pypi_check=False)

            # Report uninstalled libs first. Project-global issue (path=None):
            # owned by full runs and the requirements/package-install triggers.
            if uninstalled_libs:
                issues.append(UninstalledLibsInRequirements(uninstalled_libs))

        # Convert analysis results to linter issues
        for result in results:
            file_path = str(result.file_path) if result.file_path else ""
            issue_path = linter_path_key(result.file_path) if result.file_path else None

            if result.status == "missing_in_requirements":
                issue = MissingPackageInRequirements(
                    package_name=result.package_name,
                    import_name=result.import_name,
                    file_path=file_path,
                    line=result.line,
                )
            elif result.status == "invalid_import":
                issue = InvalidImport(
                    import_name=result.import_name,
                    file_path=file_path,
                    line=result.line,
                )
            else:
                # "unknown" status is skipped (can't determine due to uninstalled libs)
                # "ok" status is also skipped (no issue)
                continue

            issue.path = issue_path
            issues.append(issue)

        return issues
