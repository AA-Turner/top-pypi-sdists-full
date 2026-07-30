from importlib.metadata import distribution
from unittest.mock import patch

from abstra_internals.repositories.linter.repository import BULK_FIX_EXCLUDED_FIXES
from abstra_internals.repositories.linter.rules.requirements_analyzer import (
    AbstraNotInRequirementsFound,
    AbstraVersionInRequirementsIsAheadOfInstalled,
    AbstraVersionInRequirementsIsBehindInstalled,
    AbstraVersionNotDefined,
    DuplicatePackagesInRequirementsFound,
    InstallRequirements,
    LocalPackageInRequirementsFound,
    Psycopg2FoundWithoutBinary,
    RequirementsAnalyzer,
    UninstalledLibsInRequirements,
    UpdateAbstraToLatestVersion,
)
from abstra_internals.services.requirements import (
    Requirements,
    RequirementsRepository,
    requirement_to_dict,
)
from tests.fixtures import BaseTest

RUNNING_VERSION = "1.0.0"

RA_MOD = "abstra_internals.repositories.linter.rules.requirements_analyzer"

ABSTRA_PIN_ISSUE_TYPES = (
    AbstraNotInRequirementsFound,
    AbstraVersionNotDefined,
    AbstraVersionInRequirementsIsBehindInstalled,
    AbstraVersionInRequirementsIsAheadOfInstalled,
)


def _issues_of(issue_types):
    """The analyzer emits every requirements verdict at once, so each test
    filters down to the sub-check under test."""
    return [
        issue
        for issue in RequirementsAnalyzer().find_issues()
        if isinstance(issue, issue_types)
    ]


class SharedParseTest(BaseTest):
    def test_analyzer_loads_requirements_once(self):
        # The consolidation's contract: one parse shared by every sub-check.
        original = RequirementsRepository.load
        with patch.object(RequirementsRepository, "load", side_effect=original) as spy:
            RequirementsAnalyzer().find_issues()
        spy.assert_called_once()


class AbstraPinTest(BaseTest):
    def setUp(self) -> None:
        # Patch before super().setUp() so the boot-time
        # RequirementsRepository.ensure("abstra") also pins the mocked running
        # version. Both the analyzer and the repository read the running
        # version as a module attribute, so patching the source module reaches
        # both.
        self.patcher = patch(
            "abstra_internals.utils.packages.RUNNING_ABSTRA_VERSION",
            RUNNING_VERSION,
        )
        self.patcher.start()
        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()
        self.patcher.stop()

    def _write_requirements(self, content: str) -> None:
        (self.root / "requirements.txt").write_text(content)

    def _pin_issues(self):
        return _issues_of(ABSTRA_PIN_ISSUE_TYPES)

    def test_no_issue_when_requirements_matches_running(self):
        self._write_requirements(f"abstra=={RUNNING_VERSION}")
        self.assertEqual(self._pin_issues(), [])

    def test_missing_abstra_is_the_only_pin_issue(self):
        self._write_requirements("")
        issues = self._pin_issues()
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], AbstraNotInRequirementsFound)

    def test_undefined_version_is_the_only_pin_issue(self):
        self._write_requirements("abstra")
        issues = self._pin_issues()
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], AbstraVersionNotDefined)

    def test_behind_running_is_the_only_pin_issue(self):
        self._write_requirements("abstra==0.0.1")
        issues = self._pin_issues()
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], AbstraVersionInRequirementsIsBehindInstalled)

    def test_ahead_of_running_is_the_only_pin_issue(self):
        self._write_requirements("abstra==2.0.0")
        issues = self._pin_issues()
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], AbstraVersionInRequirementsIsAheadOfInstalled)

    def test_ahead_fix_triggers_self_update(self):
        self._write_requirements("abstra==2.0.0")
        issues = self._pin_issues()
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0].fixes[0], UpdateAbstraToLatestVersion)
        # The fix updates the install (self-update + restart), NOT requirements.txt.
        with patch(
            "abstra_internals.controllers.editor_update.EditorUpdateController.trigger_update"
        ) as trigger_update:
            issues[0].fixes[0].fix()
            trigger_update.assert_called_once_with()

    def test_self_update_fix_is_excluded_from_bulk_fix(self):
        # It restarts the pod, so a "fix all" sweep must not trigger it.
        self.assertIn(UpdateAbstraToLatestVersion().name, BULK_FIX_EXCLUDED_FIXES)

    def test_install_requirements_fix_is_excluded_from_bulk_fix(self):
        # It calls restart_editor_and_workers on success, so a "fix all" sweep must not trigger it.
        self.assertIn(InstallRequirements().name, BULK_FIX_EXCLUDED_FIXES)

    def test_add_fix_pins_running_version(self):
        self._write_requirements("")
        issues = self._pin_issues()
        self.assertEqual(len(issues), 1)
        issues[0].fixes[0].fix()
        self.assertEqual(self._pin_issues(), [])
        content = (self.root / "requirements.txt").read_text()
        self.assertIn(f"abstra=={RUNNING_VERSION}", content)

    def test_dev_version_zero_is_a_real_running_version(self):
        # "0.0.0" is the dev/CI version of abstra, NOT a "not found" marker: the
        # check must still run (regression guard for the requirements/install
        # desync fix, where "0.0.0" was wrongly treated as a skip sentinel).
        with patch("abstra_internals.utils.packages.RUNNING_ABSTRA_VERSION", "0.0.0"):
            self._write_requirements("")
            self.assertEqual(len(self._pin_issues()), 1)

    def test_skips_when_running_version_unknown(self):
        # None means abstra's metadata couldn't be located at boot; without a
        # real running version the check can't reason, so it reports nothing.
        with patch("abstra_internals.utils.packages.RUNNING_ABSTRA_VERSION", None):
            self._write_requirements("")
            self.assertEqual(self._pin_issues(), [])


class DuplicatePackagesTest(BaseTest):
    def _dup_issues(self):
        return _issues_of(DuplicatePackagesInRequirementsFound)

    def _exact_abstra_version(self):
        requirements = RequirementsRepository.load()
        self.assertEqual(len(requirements.libraries), 1)
        self.assertEqual(requirements.libraries[0].name, "abstra")
        req_dict = requirement_to_dict(requirements.libraries[0])
        for spec in req_dict.get("specifiers", []):
            if spec["operator"] == "==":
                return spec["version"]
        return None

    def test_default_valid(self):
        self.assertEqual(len(self._dup_issues()), 0)

    def test_valid_with_no_requirements_file(self):
        (self.root / "requirements.txt").unlink()
        self.assertEqual(len(self._dup_issues()), 0)

    def test_valid_with_no_duplicates(self):
        (self.root / "requirements.txt").write_text("abstra==1.0.0\nflask==1.0.0")
        self.assertEqual(len(self._dup_issues()), 0)

    def test_invalid_with_equal_duplicates(self):
        (self.root / "requirements.txt").write_text("abstra==1.0.0\nabstra==1.0.0")
        issues = self._dup_issues()
        self.assertEqual(len(issues), 1)
        self.assertEqual(len(issues[0].fixes), 1)

        issues[0].fixes[0].fix()

        self.assertEqual(len(self._dup_issues()), 0)

    def test_invalid_with_distinct_versions_choose_first(self):
        (self.root / "requirements.txt").write_text("abstra==1.0.0\nabstra==2.0.0")
        issues = self._dup_issues()
        self.assertEqual(len(issues), 1)
        self.assertEqual(len(issues[0].fixes), 2)

        issues[0].fixes[0].fix()

        self.assertEqual(len(self._dup_issues()), 0)
        self.assertEqual(self._exact_abstra_version(), "1.0.0")

    def test_invalid_with_distinct_versions_choose_second(self):
        (self.root / "requirements.txt").write_text("abstra==1.0.0\nabstra==2.0.0")
        issues = self._dup_issues()
        self.assertEqual(len(issues), 1)
        self.assertEqual(len(issues[0].fixes), 2)

        issues[0].fixes[1].fix()

        self.assertEqual(len(self._dup_issues()), 0)
        self.assertEqual(self._exact_abstra_version(), "2.0.0")


class LocalPackageTest(BaseTest):
    def _local_issues(self):
        return _issues_of(LocalPackageInRequirementsFound)

    def test_no_issues_when_no_conflicts(self):
        (self.root / "requirements.txt").write_text("requests==2.28.0\nflask==2.0.0")
        self.assertEqual(len(self._local_issues()), 0)

    def test_no_issues_when_no_requirements_file(self):
        (self.root / "requirements.txt").unlink()
        self.assertEqual(len(self._local_issues()), 0)

    def test_no_issues_when_folder_has_no_python_files(self):
        (self.root / "requirements.txt").write_text("utils==1.0.0")
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "readme.md").write_text("# Utils")

        self.assertEqual(len(self._local_issues()), 0)

    def test_detects_conflict_with_local_folder(self):
        (self.root / "requirements.txt").write_text("utils==1.0.0")
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = self._local_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("utils", issues[0].label)
        self.assertIn("conflicts", issues[0].label.lower())

    def test_detects_conflict_even_with_init_py(self):
        (self.root / "requirements.txt").write_text("utils==1.0.0")
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("")
        (utils_dir / "helper.py").write_text("def helper(): pass")

        self.assertEqual(len(self._local_issues()), 1)

    def test_fix_removes_conflicting_package(self):
        (self.root / "requirements.txt").write_text("utils==1.0.0\nrequests==2.28.0")
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = self._local_issues()
        self.assertEqual(len(issues), 1)

        issues[0].fixes[0].fix()

        requirements = RequirementsRepository.load()
        package_names = [lib.name for lib in requirements.libraries]
        self.assertNotIn("utils", package_names)
        self.assertIn("requests", package_names)

    def test_fix_also_adds_init_py_when_missing(self):
        (self.root / "requirements.txt").write_text("utils==1.0.0")
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = self._local_issues()
        self.assertEqual(len(issues), 1)
        self.assertEqual(len(issues[0].fixes), 1)

        issues[0].fixes[0].fix()

        self.assertTrue((utils_dir / "__init__.py").exists())
        requirements = RequirementsRepository.load()
        package_names = [lib.name for lib in requirements.libraries]
        self.assertNotIn("utils", package_names)

    def test_fix_does_not_overwrite_existing_init_py(self):
        (self.root / "requirements.txt").write_text("utils==1.0.0")
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("# existing content")
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = self._local_issues()
        self.assertEqual(len(issues), 1)

        issues[0].fixes[0].fix()

        self.assertEqual((utils_dir / "__init__.py").read_text(), "# existing content")

    def test_detects_multiple_conflicts(self):
        (self.root / "requirements.txt").write_text(
            "utils==1.0.0\nhelpers==2.0.0\nrequests==2.28.0"
        )
        for folder_name in ["utils", "helpers"]:
            folder = self.root / folder_name
            folder.mkdir()
            (folder / "module.py").write_text("# module")

        issues = self._local_issues()
        self.assertEqual(len(issues), 2)

        labels = {issue.label for issue in issues}
        self.assertTrue(any("utils" in label for label in labels))
        self.assertTrue(any("helpers" in label for label in labels))

    def test_detects_conflict_with_local_file(self):
        (self.root / "requirements.txt").write_text("mymodule==1.0.0")
        (self.root / "mymodule.py").write_text("def foo(): pass")

        issues = self._local_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("mymodule", issues[0].label)
        self.assertIn("mymodule.py", issues[0].label)  # Should mention it's a file

    def test_only_remove_fix_for_file_conflict(self):
        (self.root / "requirements.txt").write_text("mymodule==1.0.0")
        (self.root / "mymodule.py").write_text("def foo(): pass")

        issues = self._local_issues()
        self.assertEqual(len(issues), 1)

        # Only the remove fix — no __init__.py fix for files
        self.assertEqual(len(issues[0].fixes), 1)
        self.assertIn("Remove", issues[0].fixes[0].label)


class MockDistribution:
    def __init__(self, name, version):
        self.name = name
        self.version = version


def mock_distribution(name):
    if name == "abstra":
        return MockDistribution("abstra", "1.0.0")
    else:
        return distribution(name)


class Psycopg2Test(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.patcher = patch(
            "abstra_internals.utils.packages.distribution",
            side_effect=mock_distribution,
        )
        self.patcher.start()

    def tearDown(self) -> None:
        self.patcher.stop()
        super().tearDown()

    def test_psycopg2_valid(self):
        (self.root / "requirements.txt").write_text("psycopg2-binary")
        self.assertEqual(len(_issues_of(Psycopg2FoundWithoutBinary)), 0)

    def test_psycopg2_invalid(self):
        (self.root / "requirements.txt").write_text("psycopg2")
        issues = _issues_of(Psycopg2FoundWithoutBinary)
        self.assertEqual(len(issues), 1)
        self.assertIsInstance(issues[0], Psycopg2FoundWithoutBinary)


class UninstalledLibsTest(BaseTest):
    """Moved from ImportsAnalyzer: the verdict reads requirements.txt
    vs installed packages, not code, so it re-runs on requirements changes
    (which the imports analyzer's trigger groups never covered)."""

    def _uninstalled_issues(self):
        return _issues_of(UninstalledLibsInRequirements)

    def test_no_issue_with_empty_requirements(self):
        (self.root / "requirements.txt").write_text("")
        self.assertEqual(self._uninstalled_issues(), [])

    def test_reports_all_uninstalled_libs_in_one_issue(self):
        (self.root / "requirements.txt").write_text(
            "nonexistent-lib-one==1.0.0\n"
            "nonexistent-lib-two==2.0.0\n"
            "nonexistent-lib-three==3.0.0\n"
        )
        issues = self._uninstalled_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("nonexistent-lib-one", issues[0].label)
        self.assertIn("nonexistent-lib-two", issues[0].label)
        self.assertIn("nonexistent-lib-three", issues[0].label)
        self.assertIn("pip install", issues[0].label.lower())
        self.assertIsInstance(issues[0].fixes[0], InstallRequirements)


class InstallRequirementsFixTest(BaseTest):
    """A pip install lands files on disk that the long-lived editor/worker
    processes can't see. On a successful install (and only then) the fix calls
    restart_or_defer_after_install, which restarts now (desktop) or defers via
    "Restart editor" (web); otherwise the linter would keep reporting the issue."""

    def test_applies_when_install_succeeds(self):
        (self.root / "requirements.txt").write_text("pandas\n")
        with (
            patch.object(Requirements, "install_succeeded", return_value=True),
            patch(f"{RA_MOD}.restart_or_defer_after_install") as apply,
        ):
            InstallRequirements().fix()
        apply.assert_called_once_with()

    def test_does_not_apply_when_install_fails(self):
        (self.root / "requirements.txt").write_text("pandas\n")
        with (
            patch.object(Requirements, "install_succeeded", return_value=False),
            patch(f"{RA_MOD}.restart_or_defer_after_install") as apply,
        ):
            InstallRequirements().fix()
        apply.assert_not_called()

    def test_noop_without_requirements_file(self):
        req = self.root / "requirements.txt"
        if req.exists():
            req.unlink()
        with (
            patch.object(Requirements, "install_succeeded") as install,
            patch(f"{RA_MOD}.restart_or_defer_after_install") as apply,
        ):
            InstallRequirements().fix()
        install.assert_not_called()
        apply.assert_not_called()
