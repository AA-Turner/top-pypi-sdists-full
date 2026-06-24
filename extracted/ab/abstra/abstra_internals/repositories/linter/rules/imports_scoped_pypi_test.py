"""A scoped (per-save) import analysis MUST still verify on PyPI that a newly
imported, not-installed package actually exists — otherwise a typo'd import would
only be caught on a full pass. It stays cheap via the long-lived
PyPIVerificationCache (7-day, on-disk): only a package name never seen before
hits the network; everything else is a cache hit.
"""

from unittest.mock import Mock, patch

from abstra_internals.repositories.linter.rules.imports_requirements_analyzer import (
    ImportsRequirementsAnalyzer,
    InvalidImport,
    MissingPackageInRequirements,
)
from abstra_internals.services.pypi_cache import PyPIVerificationCache
from tests.fixtures import BaseTest

_CHECK_PACKAGE = "abstra_internals.services.requirements.check_package"
_UNINSTALLED = "abstra_internals.services.requirements.get_uninstalled_requirements"


def _has(issues, cls):
    return any(isinstance(i, cls) for i in issues)


class TestScopedVerifiesPyPI(BaseTest):
    """The save path drives the analysis to the PyPI-verification branch (import
    unresolved + all requirements installed) and must flag accordingly."""

    def setUp(self):
        super().setUp()
        PyPIVerificationCache.clear_cache()
        (self.root / "requirements.txt").touch()
        self.script = self.controller.create_stage("tasklet", "S", "script.py")

    def test_scoped_flags_invalid_import_when_not_on_pypi(self):
        self.script.file_path.write_text("import nonexistent_xyz_pkg")
        with (
            patch(_CHECK_PACKAGE, return_value="unknown"),
            patch(_UNINSTALLED, return_value=[]),
            patch.object(
                PyPIVerificationCache, "verify_package_exists", return_value=False
            ),
        ):
            issues = ImportsRequirementsAnalyzer().find_issues(
                path=self.script.file_path
            )
        self.assertTrue(_has(issues, InvalidImport))

    def test_scoped_flags_missing_when_on_pypi(self):
        self.script.file_path.write_text("import some_real_pkg")
        with (
            patch(_CHECK_PACKAGE, return_value="unknown"),
            patch(_UNINSTALLED, return_value=[]),
            patch.object(
                PyPIVerificationCache, "verify_package_exists", return_value=True
            ),
        ):
            issues = ImportsRequirementsAnalyzer().find_issues(
                path=self.script.file_path
            )
        self.assertTrue(_has(issues, MissingPackageInRequirements))

    def test_scoped_verifies_new_name_once_then_uses_cache(self):
        # New name → network once on the save; same name again → cache hit, no
        # second network call. Proves "long cache, only new packages".
        self.script.file_path.write_text("import nonexistent_xyz_pkg")
        with (
            patch(_CHECK_PACKAGE, return_value="unknown"),
            patch(_UNINSTALLED, return_value=[]),
            patch.object(
                PyPIVerificationCache, "_query_pypi", Mock(return_value=False)
            ) as query,
        ):
            cold = ImportsRequirementsAnalyzer().find_issues(path=self.script.file_path)
            after_cold = query.call_count
            warm = ImportsRequirementsAnalyzer().find_issues(path=self.script.file_path)
            after_warm = query.call_count
        self.assertEqual(after_cold, 1)
        self.assertEqual(after_warm, 1)
        self.assertTrue(_has(cold, InvalidImport))
        self.assertTrue(_has(warm, InvalidImport))

    def test_full_run_also_flags_invalid_import(self):
        self.script.file_path.write_text("import nonexistent_xyz_pkg")
        with (
            patch(_CHECK_PACKAGE, return_value="unknown"),
            patch(_UNINSTALLED, return_value=[]),
            patch.object(
                PyPIVerificationCache, "verify_package_exists", return_value=False
            ),
        ):
            issues = ImportsRequirementsAnalyzer().find_issues()
        self.assertTrue(_has(issues, InvalidImport))

    def test_scoped_still_flags_installed_missing_from_requirements(self):
        self.script.file_path.write_text("import pandas")
        with (
            patch(_CHECK_PACKAGE, return_value="installed"),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            issues = ImportsRequirementsAnalyzer().find_issues(
                path=self.script.file_path
            )
        self.assertTrue(_has(issues, MissingPackageInRequirements))
