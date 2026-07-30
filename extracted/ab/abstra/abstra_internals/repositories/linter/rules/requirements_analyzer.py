import enum
from typing import List, Optional

from abstra_internals.repositories.linter.models import (
    LinterFix,
    LinterIssue,
    LinterRule,
)
from abstra_internals.repositories.linter.process_actions import (
    RESTART_NOTICE,
    restart_or_defer_after_install,
)
from abstra_internals.services.requirements import (
    Requirements,
    RequirementsRepository,
    get_uninstalled_requirements,
    is_local_module,
    requirement_to_dict,
)
from abstra_internals.settings import Settings
from abstra_internals.utils import packages as pkg_utils


class _AbstraRequirementStatus(enum.Enum):
    # Running version couldn't be determined (abstra not located at boot).
    UNKNOWN = enum.auto()
    # requirements.txt pins abstra at exactly the running version.
    OK = enum.auto()
    # abstra is absent from requirements.txt.
    MISSING = enum.auto()
    # abstra is present but without a pinned (==) version.
    VERSION_UNDEFINED = enum.auto()
    # requirements.txt pins an older abstra than the one running.
    BEHIND_RUNNING = enum.auto()
    # requirements.txt pins a newer abstra than the one running.
    AHEAD_OF_RUNNING = enum.auto()


def _abstra_requirement_status(requirements: Requirements) -> _AbstraRequirementStatus:
    """Classify how requirements.txt relates to the abstra version running.

    Single classification for the abstra-pin issues so their case splits can't
    drift apart. The comparison is against the version actually running this
    process, not importlib.metadata's on-disk view (see
    RequirementsRepository._resolve_pinned_version): right after an upgrade
    whose install hasn't taken effect, disk reports the new version while the
    old code still runs.
    """
    # None means abstra couldn't be located at boot — we can't reason about the
    # requirement without a real running version. ("0.0.0" is a real dev/CI
    # version, not a not-found marker.)
    running = pkg_utils.RUNNING_ABSTRA_VERSION
    if running is None:
        return _AbstraRequirementStatus.UNKNOWN

    running_version = pkg_utils.parse_version(running)

    if not requirements.has("abstra"):
        return _AbstraRequirementStatus.MISSING

    if requirements.has("abstra", str(running_version)):
        return _AbstraRequirementStatus.OK

    requirements_version = requirements.get("abstra")
    if requirements_version is None:
        return _AbstraRequirementStatus.VERSION_UNDEFINED

    if pkg_utils.parse_version(requirements_version) > running_version:
        return _AbstraRequirementStatus.AHEAD_OF_RUNNING

    return _AbstraRequirementStatus.BEHIND_RUNNING


class AddAbstraToRequirements(LinterFix):
    label = "Add abstra to requirements.txt"

    def fix(self):
        requirements = RequirementsRepository.load()
        # Pin the version actually running this process (captured at boot), not
        # importlib.metadata's on-disk view — see
        # RequirementsRepository._resolve_pinned_version.
        requirements.ensure("abstra", pkg_utils.RUNNING_ABSTRA_VERSION)
        RequirementsRepository.save(requirements)


class SetAbstraVersionInRequirements(LinterFix):
    label = "Set abstra version in requirements.txt"

    def fix(self):
        requirements = RequirementsRepository.load()
        # See AddAbstraToRequirements: pin the running version, not the disk one.
        requirements.ensure("abstra", pkg_utils.RUNNING_ABSTRA_VERSION)
        RequirementsRepository.save(requirements)


class UpdateAbstraToLatestVersion(LinterFix):
    label = "Update abstra to the latest version"

    def fix(self):
        # When requirements.txt is ahead of the running version, the install is
        # what lags behind — so the reconciliation is to bring the install up,
        # not to edit requirements.txt down. Delegate to the self-update
        # controller (staged slot flip on web, in-place upgrade elsewhere, then
        # a restart); boot's RequirementsRepository.ensure re-syncs
        # requirements.txt to the newly installed version afterwards. Lazy
        # import avoids an import cycle at linter package load.
        from abstra_internals.controllers.editor_update import EditorUpdateController

        EditorUpdateController.trigger_update()


class MergeDuplicatePackages(LinterFix):
    pkg_version: Optional[str]
    pkg_name: str

    def __init__(self, pkg_name: str, pkg_version: Optional[str]) -> None:
        super().__init__()
        self.pkg_version = pkg_version
        self.pkg_name = pkg_name
        version_name = pkg_version if pkg_version is not None else "latest"
        self.label = f"Choose {version_name}"

    def fix(self):
        requirements = RequirementsRepository.load()
        requirements.ensure(self.pkg_name, self.pkg_version)
        requirements.delete_duplicates(self.pkg_name, self.pkg_version)
        RequirementsRepository.save(requirements)

    def __hash__(self) -> int:
        return hash((self.pkg_name, self.pkg_version))


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


class ReplacePsycopg2WithBinary(LinterFix):
    def __init__(self):
        self.label = "Replace psycopg2 with psycopg2-binary"

    def fix(self):
        requirements = RequirementsRepository.load()
        requirements.delete("psycopg2")
        requirements.ensure("psycopg2-binary")
        RequirementsRepository.save(requirements)


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
            # Just-installed packages become visible only after a restart. On the
            # web editor this is deferred (via "Restart editor"); elsewhere it
            # restarts now (see restart_or_defer_after_install).
            restart_or_defer_after_install()


class AbstraNotInRequirementsFound(LinterIssue):
    title = "Abstra should be in your requirements.txt"
    type = "error"

    def __init__(self) -> None:
        self.label = "Abstra is not in your requirements.txt file."
        self.fixes = [AddAbstraToRequirements()]


class AbstraVersionNotDefined(LinterIssue):
    title = "Abstra version in requirements.txt must match the running version"
    type = "error"

    def __init__(self) -> None:
        self.label = (
            "You have abstra in requirements.txt, but the version is not defined."
        )
        self.fixes = [SetAbstraVersionInRequirements()]


class AbstraVersionInRequirementsIsBehindInstalled(LinterIssue):
    title = "Abstra version in requirements.txt must match the running version"
    type = "error"

    def __init__(self) -> None:
        self.label = (
            "The version of abstra in your requirements.txt is behind the version "
            "currently running. Update your requirements.txt to fix this."
        )
        self.fixes = [SetAbstraVersionInRequirements()]


class AbstraVersionInRequirementsIsAheadOfInstalled(LinterIssue):
    title = "Abstra in requirements.txt is ahead of the running version"
    type = "error"

    def __init__(self) -> None:
        self.label = (
            "The version of abstra in your requirements.txt is ahead of the "
            "running version."
        )
        self.fixes = [UpdateAbstraToLatestVersion()]


class DuplicatePackagesInRequirementsFound(LinterIssue):
    title = "Duplicate package in requirements.txt"
    type = "error"

    def __init__(self, name: str, versions: List[Optional[str]]) -> None:
        self.label = f"Duplicate {name} found in requirements.txt"
        fixes = [
            MergeDuplicatePackages(pkg_name=name, pkg_version=version)
            for version in versions
        ]
        self.fixes = list(
            dict.fromkeys(fixes).keys()
        )  # remove duplicates keeping order


class LocalPackageInRequirementsFound(LinterIssue):
    """Issue when a package in requirements.txt conflicts with a local module"""

    title = "Local module found in requirements.txt"
    type = "error"

    def __init__(self, pkg_name: str, is_file: bool) -> None:
        self.pkg_name = pkg_name
        if is_file:
            self.label = f'Package "{pkg_name}" in requirements.txt conflicts with local file "{pkg_name}.py"'
        else:
            self.label = f'Package "{pkg_name}" in requirements.txt conflicts with local folder "{pkg_name}/"'
        self.fixes: List[LinterFix] = [RemoveConflictingPackage(pkg_name)]


class Psycopg2FoundWithoutBinary(LinterIssue):
    title = "The dependency psycopg2 must be in its binary form"
    type = "error"

    def __init__(self):
        self.label = "The dependency psycopg2 must be replaced with psycopg2-binary"
        self.fixes = [ReplacePsycopg2WithBinary()]


class UninstalledLibsInRequirements(LinterIssue):
    """Issue when requirements.txt has libs that are not installed."""

    title = "Packages in requirements.txt are not installed"
    type = "error"

    def __init__(self, uninstalled_libs: List[str]):
        self.uninstalled_libs = uninstalled_libs
        libs_str = ", ".join(uninstalled_libs)
        self.label = (
            f"The following packages in requirements.txt are not installed: {libs_str}. "
            f"Run 'pip install -r requirements.txt' to install them. {RESTART_NOTICE}"
        )
        self.fixes = [InstallRequirements()]


def _abstra_pin_issues(requirements: Requirements) -> List[LinterIssue]:
    status = _abstra_requirement_status(requirements)
    if status == _AbstraRequirementStatus.MISSING:
        return [AbstraNotInRequirementsFound()]
    if status == _AbstraRequirementStatus.VERSION_UNDEFINED:
        return [AbstraVersionNotDefined()]
    if status == _AbstraRequirementStatus.BEHIND_RUNNING:
        return [AbstraVersionInRequirementsIsBehindInstalled()]
    if status == _AbstraRequirementStatus.AHEAD_OF_RUNNING:
        return [AbstraVersionInRequirementsIsAheadOfInstalled()]
    return []


def _duplicate_package_issues(requirements: Requirements) -> List[LinterIssue]:
    issues: List[LinterIssue] = []
    for name, versions in requirements.get_duplicates().items():
        # Extract exact versions from specifiers
        version_list = []
        for r in versions:
            req_dict = requirement_to_dict(r)
            exact_version = None
            for spec in req_dict.get("specifiers", []):
                if spec["operator"] == "==":
                    exact_version = spec["version"]
                    break
            version_list.append(exact_version)

        issues.append(
            DuplicatePackagesInRequirementsFound(name=name, versions=version_list)
        )
    return issues


def _local_package_issues(requirements: Requirements) -> List[LinterIssue]:
    """Packages in requirements.txt shadowed by a local module.

    Python imports the external package instead of the local module, so local
    submodules raise ModuleNotFoundError (e.g. requirements.txt has "utils"
    while the project has utils/jira_data_processor.py).
    """
    issues: List[LinterIssue] = []
    root = Settings.root_path

    for lib in requirements.libraries:
        pkg_name = lib.name

        if not is_local_module(pkg_name):
            continue

        is_file = (root / f"{pkg_name}.py").exists()

        issues.append(
            LocalPackageInRequirementsFound(
                pkg_name=pkg_name,
                is_file=is_file,
            )
        )

    return issues


def _psycopg2_issues(requirements: Requirements) -> List[LinterIssue]:
    if requirements.has("psycopg2"):
        return [Psycopg2FoundWithoutBinary()]
    return []


def _uninstalled_libs_issues(requirements: Requirements) -> List[LinterIssue]:
    # Same helper analyze_project_imports uses internally to gate its PyPI
    # checks, so the two analyzers can't disagree on what counts as installed.
    uninstalled = get_uninstalled_requirements(requirements)
    if uninstalled:
        return [UninstalledLibsInRequirements(uninstalled)]
    return []


class RequirementsAnalyzer(LinterRule):
    """Every requirements.txt verdict in one pass.

    The sub-checks are case splits over a single input, so requirements.txt is
    parsed once and shared (previously six rules re-loaded it independently).
    PyPI-dependent checks stay out (see InvalidPackageInRequirements): a
    network failure would fail every requirements verdict at once, and a
    failed check blocks deploys.
    """

    label = "Requirements analysis"

    def find_issues(self) -> List[LinterIssue]:
        requirements = RequirementsRepository.load()
        return [
            *_abstra_pin_issues(requirements),
            *_duplicate_package_issues(requirements),
            *_local_package_issues(requirements),
            *_psycopg2_issues(requirements),
            *_uninstalled_libs_issues(requirements),
        ]
