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
    RESTART_NOTICE,
    restart_or_defer_after_install,
)
from abstra_internals.services.requirements import (
    Requirements,
    RequirementsRepository,
    analyze_project_imports,
    create_requirement,
    get_installed_version,
)


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
            # and worker processes. On the web editor this defers a restart (the
            # user applies it via "Restart editor"); elsewhere it restarts now so
            # the linter re-checks against it. A failed install leaves things as-is.
            restart_or_defer_after_install()


class MissingPackageInRequirements(LinterIssue):
    """Issue when an installed/available package is not in requirements.txt."""

    title = "Package missing in requirements.txt"
    type = "error"

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
            label = f"{label}. {RESTART_NOTICE}"
        self.label = label
        self.fixes = [AddPackageToRequirements(package_name)]


class InvalidImport(LinterIssue):
    """Issue when an import cannot be resolved and doesn't exist on PyPI."""

    title = "Import not found on PyPI"
    type = "error"
    fix_with_ai = True

    def __init__(self, import_name: str, file_path: str, line: int):
        self.import_name = import_name
        self.file_path = file_path
        self.line = line
        self.label = (
            f"Import '{import_name}' in {file_path}:{line} was not found on PyPI. "
            f"Please check if the package name is correct."
        )
        self.fixes = []


class ImportsAnalyzer(PathScopedLinterRule):
    """
    Analyzes project imports against requirements.txt and PyPI.

    Uses the shared analyze_project_imports() function from services.requirements
    to ensure consistent behavior across the codebase.
    """

    label = "Imports analysis"

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
            # The uninstalled-libs verdict itself belongs to RequirementsAnalyzer
            # (it reads requirements.txt, not code); the analysis still computes
            # it internally to gate the PyPI checks below.
            results, _ = analyze_project_imports(skip_pypi_check=False)

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
