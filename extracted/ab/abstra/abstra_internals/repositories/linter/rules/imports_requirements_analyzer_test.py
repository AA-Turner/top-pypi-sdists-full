"""
Tests for the unified ImportsRequirementsAnalyzer linter.

This linter follows a decision tree flow for analyzing imports and requirements:

1. Is import local? → Ignore
2. Can import be resolved (installed)?
   2.a Yes → Is it in requirements.txt?
       2.a.1 Yes → Ignore
       2.a.2 No → Error: missing package in requirements.txt
   2.b No → Go to step 3
3. Are all libs in requirements.txt installed?
   3.a No → Info: there are uninstalled libs in requirements.txt
   3.b Yes → Go to step 4
4. Does the import name exist on PyPI?
   4.a Yes → Error: missing package in requirements.txt
   4.b No → Error: invalid import (not found on PyPI)
"""

from unittest.mock import patch

from abstra_internals.repositories.linter.rules.imports_requirements_analyzer import (
    ImportsRequirementsAnalyzer,
    InvalidImport,
    MissingPackageInRequirements,
    UninstalledLibsInRequirements,
)
from abstra_internals.services.pypi_cache import PyPIVerificationCache
from tests.fixtures import BaseTest

# =============================================================================
# FLOW POINT 1: LOCAL IMPORT DETECTION
# =============================================================================


class TestFlowPoint1_LocalImportDetection(BaseTest):
    """
    Flow point 1: Check if import refers to a local module.
    If it's a local import, it should be ignored.
    """

    def test_ignores_local_folder_import(self):
        """Should ignore imports from local folders containing Python files."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a local folder with Python files
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        # Create script that imports from local folder
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("from utils.helper import helper")

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        # Should not have any issue about 'utils'
        utils_issues = [i for i in issues if "utils" in i.label.lower()]
        self.assertEqual(len(utils_issues), 0)

    def test_ignores_local_file_import(self):
        """Should ignore imports from local .py files."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a local Python file
        (self.root / "mymodule.py").write_text("def foo(): pass")

        # Create script that imports from local file
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("from mymodule import foo")

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        mymodule_issues = [i for i in issues if "mymodule" in i.label.lower()]
        self.assertEqual(len(mymodule_issues), 0)

    def test_ignores_local_package_with_init_py(self):
        """Should ignore imports from local packages with __init__.py."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a local package with __init__.py
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("")
        (utils_dir / "helper.py").write_text("def helper(): pass")

        # Create script that imports from local package
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("from utils import helper")

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        utils_issues = [i for i in issues if "utils" in i.label.lower()]
        self.assertEqual(len(utils_issues), 0)

    def test_ignores_relative_import(self):
        """Should ignore relative imports (from . import X, from ..module import Y)."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a package with relative imports
        classes_dir = self.root / "src" / "classes"
        classes_dir.mkdir(parents=True)
        (classes_dir / "__init__.py").write_text("")
        (classes_dir / "another_class.py").write_text("OTHER_VALUE = 42")
        (classes_dir / "some_class.py").write_text(
            "from .another_class import OTHER_VALUE\n"
        )
        (self.root / "src" / "__init__.py").write_text("")

        # Create an entrypoint script
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("from src.classes.some_class import OTHER_VALUE\n")

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        # Should not report relative imports as missing packages
        self.assertEqual(len(issues), 0)

    def test_ignores_namespace_package_without_init_py(self):
        """
        Should ignore namespace packages (PEP 420) without __init__.py.

        Python 3.3+ supports namespace packages, which are directories containing
        Python files but without __init__.py.
        """
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a namespace package structure (no __init__.py files)
        entities_dir = self.root / "src" / "entities"
        entities_dir.mkdir(parents=True)
        (entities_dir / "square.py").write_text("class Square: pass")

        # Create a script at root that imports from the namespace package
        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("from src.entities.square import Square\n")

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        src_issues = [i for i in issues if "src" in i.label.lower()]
        self.assertEqual(len(src_issues), 0)

    def test_ignores_builtin_modules(self):
        """Should ignore built-in Python modules (os, sys, json, etc.)."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text(
            "import os\n"
            "import sys\n"
            "import json\n"
            "from collections import defaultdict\n"
            "from typing import List\n"
        )

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        self.assertEqual(len(issues), 0)


# =============================================================================
# FLOW POINT 2: RESOLVED IMPORTS VS REQUIREMENTS
# =============================================================================


class TestFlowPoint2_ResolvedImportsVsRequirements(BaseTest):
    """
    Flow point 2: Check if import can be resolved (installed package).
    2.a If resolved and in requirements.txt → Ignore
    2.a.2 If resolved but NOT in requirements.txt → Error: missing package
    """

    def test_no_issue_when_installed_package_is_in_requirements(self):
        """Should not report issue when installed package is in requirements.txt."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("pandas==1.0.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import pandas")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            pandas_issues = [i for i in issues if "pandas" in i.label.lower()]
            self.assertEqual(len(pandas_issues), 0)

    def test_issue_when_installed_package_not_in_requirements(self):
        """Should report error when installed package is not in requirements.txt."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()  # Empty requirements

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import pandas")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            self.assertEqual(len(issues), 1)
            self.assertIsInstance(issues[0], MissingPackageInRequirements)
            self.assertIn("pandas", issues[0].label.lower())

    def test_handles_package_name_mapping_dateutil(self):
        """
        Should handle cases where import name differs from PyPI package name.
        Example: 'import dateutil' → package is 'python-dateutil' on PyPI.
        """
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("python-dateutil==2.8.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import dateutil")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"dateutil": ["python-dateutil"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should NOT report issue because python-dateutil is in requirements
            dateutil_issues = [i for i in issues if "dateutil" in i.label.lower()]
            self.assertEqual(len(dateutil_issues), 0)

    def test_handles_package_name_mapping_pil(self):
        """Should handle PIL → Pillow mapping."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("Pillow==9.0.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("from PIL import Image")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"PIL": ["Pillow"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            pil_issues = [i for i in issues if "pil" in i.label.lower()]
            self.assertEqual(len(pil_issues), 0)

    def test_handles_submodule_imports(self):
        """Should correctly handle submodule imports like 'from pandas.plotting import X'."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("pandas==1.0.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("from pandas.plotting import scatter_matrix")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            pandas_issues = [i for i in issues if "pandas" in i.label.lower()]
            self.assertEqual(len(pandas_issues), 0)

    def test_handles_import_alias(self):
        """Should correctly handle import aliases like 'import numpy as np'."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("numpy==1.0.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import numpy as np")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"numpy": ["numpy"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            numpy_issues = [i for i in issues if "numpy" in i.label.lower()]
            self.assertEqual(len(numpy_issues), 0)

    def test_handles_multiple_imports_same_package(self):
        """Should only report one issue per package even with multiple imports."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text(
            "import pandas\n"
            "from pandas import DataFrame\n"
            "from pandas.plotting import scatter_matrix\n"
        )

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should only have ONE issue for pandas, not three
            pandas_issues = [i for i in issues if "pandas" in i.label.lower()]
            self.assertEqual(len(pandas_issues), 1)


# =============================================================================
# FLOW POINT 3: UNINSTALLED LIBS IN REQUIREMENTS
# =============================================================================


class TestFlowPoint3_UninstalledLibsDetection(BaseTest):
    """
    Flow point 3: Check if all libs in requirements.txt are installed.
    3.a If there are uninstalled libs → Info: there are libs not installed
    3.b If all installed → Go to step 4 (PyPI check)
    """

    def test_info_when_requirements_has_uninstalled_libs(self):
        """Should show info when requirements.txt has libs that are not installed."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("pandas==1.0.0\nsome-uninstalled-package==1.0.0\n")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import unknown_module")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="unknown",
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=["some-uninstalled-package"],
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should find info issue about uninstalled libs
            uninstalled_issues = [
                i for i in issues if isinstance(i, UninstalledLibsInRequirements)
            ]
            self.assertEqual(len(uninstalled_issues), 1)
            self.assertIn("some-uninstalled-package", uninstalled_issues[0].label)

    def test_skips_pypi_check_when_libs_not_installed(self):
        """
        Should NOT check PyPI when there are uninstalled libs in requirements.txt.

        This is important because the unresolved import might be from a lib
        that is in requirements.txt but with a different import name
        (like dateutil → python-dateutil).
        """
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("python-dateutil==2.8.0\n")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import dateutil")

        pypi_called = False

        def mock_pypi_check(package_name):
            nonlocal pypi_called
            pypi_called = True
            return True

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="unknown",
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=["python-dateutil"],
            ),
            patch.object(
                PyPIVerificationCache,
                "verify_package_exists",
                side_effect=mock_pypi_check,
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # PyPI should NOT have been called
            self.assertFalse(pypi_called)

            # Should show "libs not installed" info instead
            uninstalled_issues = [
                i for i in issues if isinstance(i, UninstalledLibsInRequirements)
            ]
            self.assertEqual(len(uninstalled_issues), 1)

    def test_detects_multiple_uninstalled_libs(self):
        """Should report all uninstalled libs in a single issue."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text(
            "nonexistent-lib-one==1.0.0\n"
            "nonexistent-lib-two==2.0.0\n"
            "nonexistent-lib-three==3.0.0\n"
        )

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("print('hello')")

        with patch(
            "abstra_internals.services.requirements.get_uninstalled_requirements",
            return_value=[
                "nonexistent-lib-one",
                "nonexistent-lib-two",
                "nonexistent-lib-three",
            ],
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should report info about all uninstalled libs in one issue
            uninstalled_issues = [
                i for i in issues if isinstance(i, UninstalledLibsInRequirements)
            ]
            self.assertEqual(len(uninstalled_issues), 1)
            self.assertIn("nonexistent-lib-one", uninstalled_issues[0].label)
            self.assertIn("nonexistent-lib-two", uninstalled_issues[0].label)
            self.assertIn("nonexistent-lib-three", uninstalled_issues[0].label)


# =============================================================================
# FLOW POINT 4: PYPI VERIFICATION
# =============================================================================


class TestFlowPoint4_PyPIVerification(BaseTest):
    """
    Flow point 4: Check if import name exists on PyPI.
    Only runs when:
    - Import cannot be resolved (not installed)
    - All libs in requirements.txt ARE installed

    4.a If exists on PyPI → Error: missing package in requirements.txt
    4.b If not on PyPI → Error: invalid import
    """

    def setUp(self):
        super().setUp()
        PyPIVerificationCache.clear_cache()

    def test_issue_when_import_exists_on_pypi_but_not_installed(self):
        """Should report 'missing package' when import exists on PyPI."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import requests")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="unknown",
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=[],
            ),
            patch.object(
                PyPIVerificationCache, "verify_package_exists", return_value=True
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should find bug issue: "requests" missing from requirements.txt
            missing_issues = [
                i for i in issues if isinstance(i, MissingPackageInRequirements)
            ]
            self.assertEqual(len(missing_issues), 1)
            self.assertIn("requests", missing_issues[0].label.lower())

    def test_issue_when_import_not_found_on_pypi(self):
        """Should report 'invalid import' when import doesn't exist on PyPI."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import nonexistent_xyz_package_12345")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="unknown",
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=[],
            ),
            patch.object(
                PyPIVerificationCache, "verify_package_exists", return_value=False
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should find bug issue: invalid import
            invalid_issues = [i for i in issues if isinstance(i, InvalidImport)]
            self.assertEqual(len(invalid_issues), 1)
            self.assertIn("nonexistent_xyz_package_12345", invalid_issues[0].label)

    def test_uses_pypi_cache(self):
        """Should use PyPI cache to avoid duplicate network calls."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import some_package")

        query_count = 0

        def mock_query(package_name):
            nonlocal query_count
            query_count += 1
            return True

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="unknown",
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=[],
            ),
            patch.object(PyPIVerificationCache, "_query_pypi", side_effect=mock_query),
        ):
            rule = ImportsRequirementsAnalyzer()

            # First call
            rule.find_issues()
            first_count = query_count

            # Second call should use cache
            rule.find_issues()

            # Should only have queried once (cached)
            self.assertEqual(query_count, first_count)


# =============================================================================
# EDGE CASES AND ADDITIONAL SCENARIOS
# =============================================================================


class TestEdgeCases(BaseTest):
    """Edge cases that should be handled correctly."""

    def test_no_issues_when_no_imports(self):
        """Should not report any issues when file has no imports."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("print('hello world')")

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        self.assertEqual(len(issues), 0)

    def test_no_issues_when_no_python_files(self):
        """Should not report any issues when there are no Python files."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("pandas==1.0.0")

        # Don't create any scripts/Python files

        rule = ImportsRequirementsAnalyzer()
        issues = rule.find_issues()

        # May have uninstalled libs issue, but no import issues
        import_issues = [
            i
            for i in issues
            if isinstance(i, (MissingPackageInRequirements, InvalidImport))
        ]
        self.assertEqual(len(import_issues), 0)

    def test_handles_syntax_error_in_python_file(self):
        """Should not crash when a Python file has syntax errors."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("def foo(\n  # syntax error - unclosed paren")

        # Should not raise exception
        rule = ImportsRequirementsAnalyzer()
        try:
            rule.find_issues()
        except SyntaxError:
            self.fail("Linter should not raise SyntaxError for invalid Python files")

    def test_handles_empty_requirements_file(self):
        """Should handle empty requirements.txt gracefully."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import pandas")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should report pandas as missing
            pandas_issues = [i for i in issues if "pandas" in i.label.lower()]
            self.assertEqual(len(pandas_issues), 1)

    def test_handles_no_requirements_file(self):
        """Should handle missing requirements.txt gracefully."""
        requirements_file = self.root / "requirements.txt"
        if requirements_file.exists():
            requirements_file.unlink()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import pandas")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            # Should not raise exception
            try:
                rule.find_issues()
            except FileNotFoundError:
                self.fail("Linter should handle missing requirements.txt gracefully")

    def test_handles_packages_with_urls(self):
        """Should not check PyPI for packages installed from URLs."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("mypackage @ https://example.com/mypackage.tar.gz")

        with patch(
            "abstra_internals.services.requirements.get_uninstalled_requirements",
            return_value=[],
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # URL packages should be considered valid
            url_issues = [i for i in issues if "mypackage" in i.label.lower()]
            self.assertEqual(len(url_issues), 0)

    def test_handles_packages_with_extras(self):
        """Should correctly identify packages with extras like 'package[extra]'."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("requests[security]==2.28.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import requests")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"requests": ["requests"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should recognize that 'requests' is in requirements.txt
            requests_issues = [i for i in issues if "requests" in i.label.lower()]
            self.assertEqual(len(requests_issues), 0)

    def test_handles_version_specifiers(self):
        """Should correctly identify packages with various version specifiers."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text(
            "abstra==1.0.0\npandas>=1.0.0\nnumpy~=1.20\nscipy!=1.5.0\nmatplotlib<4.0\n"
        )

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text(
            "import pandas\nimport numpy\nimport scipy\nimport matplotlib\n"
        )

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={
                    "pandas": ["pandas"],
                    "numpy": ["numpy"],
                    "scipy": ["scipy"],
                    "matplotlib": ["matplotlib"],
                },
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=[],
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # All packages are in requirements, should have no issues
            self.assertEqual(len(issues), 0)

    def test_handles_commented_lines_in_requirements(self):
        """Should ignore commented lines in requirements.txt."""
        requirements_file = self.root / "requirements.txt"
        # Use 'requests' in requirements and 'flask' commented out
        # Note: flask is NOT a transitive dependency of requests
        requirements_file.write_text(
            "# This is a comment\nrequests==2.0.0\n# flask==2.0.0  # disabled\n"
        )

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import flask")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements._PackagesDistributionsCache.get",
                return_value={"flask": ["flask"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should report flask as missing (it's commented out and not a transitive dep)
            flask_issues = [
                i
                for i in issues
                if "flask" in i.label.lower()
                and isinstance(i, MissingPackageInRequirements)
            ]
            self.assertEqual(len(flask_issues), 1)

    def test_handles_multiple_files_with_same_import(self):
        """Should only report each missing package once even if imported in multiple files."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script1 = self.controller.create_tasklet("Script 1", "script1.py")
        script1.file_path.write_text("import pandas")

        script2 = self.controller.create_tasklet("Script 2", "script2.py")
        script2.file_path.write_text("import pandas")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should have only ONE issue for pandas
            pandas_issues = [
                i
                for i in issues
                if "pandas" in i.label.lower()
                and isinstance(i, MissingPackageInRequirements)
            ]
            self.assertEqual(len(pandas_issues), 1)


# =============================================================================
# FIX TESTS
# =============================================================================


class TestFixes(BaseTest):
    """Tests for the fix actions provided by the linter."""

    def test_fix_second_issue_adds_correct_package(self):
        """
        Bug regression test: When multiple packages are missing, clicking
        the fix for the SECOND issue should add that package, not the first one.

        This is a positional bug - the fix was always adding the first package
        regardless of which fix was clicked.
        """
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("abstra==1.0.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import package_one\nimport package_two")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={
                    "package_one": ["package-one"],
                    "package_two": ["package-two"],
                },
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=[],
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            # Should have 2 missing package issues
            missing_issues = [
                i for i in issues if isinstance(i, MissingPackageInRequirements)
            ]
            self.assertEqual(len(missing_issues), 2)

            # Get the SECOND issue and apply its fix
            second_issue = missing_issues[1]
            second_package_name = second_issue.package_name
            second_issue.fixes[0].fix()

            # Verify the SECOND package was added, not the first
            requirements_content = requirements_file.read_text()
            self.assertIn(second_package_name, requirements_content)

            # The first package should NOT be in requirements
            first_issue = missing_issues[0]
            first_package_name = first_issue.package_name
            self.assertNotIn(first_package_name, requirements_content)

    def test_fix_by_name_adds_correct_package(self):
        """
        Bug regression test: When using fix.name to find and execute a fix
        (as done by fix_issue_in_codebase), the correct package should be added.

        The bug was that all AddPackageToRequirements fixes had the same name
        (the class name), so the first one was always executed.
        """
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("abstra==1.0.0")

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import package_one\nimport package_two")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={
                    "package_one": ["package-one"],
                    "package_two": ["package-two"],
                },
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=[],
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            missing_issues = [
                i for i in issues if isinstance(i, MissingPackageInRequirements)
            ]
            self.assertEqual(len(missing_issues), 2)

            # Get fixes from both issues
            first_fix = missing_issues[0].fixes[0]
            second_fix = missing_issues[1].fixes[0]

            # The fix names should be DIFFERENT so they can be distinguished
            self.assertNotEqual(
                first_fix.name,
                second_fix.name,
                "Fix names should be unique to identify which package to add",
            )

    def test_fix_adds_missing_package_to_requirements(self):
        """Fix should add missing package to requirements.txt."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import pandas")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            self.assertEqual(len(issues), 1)

            # Apply the fix
            issues[0].fixes[0].fix()

            # Verify pandas is added to requirements.txt
            requirements_content = requirements_file.read_text()
            self.assertIn("pandas", requirements_content)

    def test_fix_adds_correct_pypi_name_not_import_name(self):
        """
        Fix should add the PyPI package name, not the import name.
        Example: 'import dateutil' should add 'python-dateutil', not 'dateutil'.
        """
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import dateutil")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"dateutil": ["python-dateutil"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            self.assertEqual(len(issues), 1)

            # Apply the fix
            issues[0].fixes[0].fix()

            # Verify 'python-dateutil' is added (not 'dateutil')
            requirements_content = requirements_file.read_text()
            self.assertIn("python-dateutil", requirements_content)
            # Should not have 'dateutil' alone (without 'python-' prefix)
            lines = [
                line.strip()
                for line in requirements_content.split("\n")
                if line.strip()
            ]
            dateutil_only_lines = [line for line in lines if line == "dateutil"]
            self.assertEqual(len(dateutil_only_lines), 0)


# =============================================================================
# MESSAGE QUALITY TESTS
# =============================================================================


class TestMessageQuality(BaseTest):
    """Tests to ensure error messages are clear and actionable."""

    def test_message_for_missing_installed_package(self):
        """Error message should clearly state the package is installed but not in requirements."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import pandas")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="installed",
            ),
            patch(
                "abstra_internals.services.requirements.packages_distributions",
                return_value={"pandas": ["pandas"]},
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            self.assertEqual(len(issues), 1)
            # Message should mention: package name, requirements.txt
            self.assertIn("pandas", issues[0].label.lower())
            self.assertIn("requirements.txt", issues[0].label.lower())

    def test_message_for_uninstalled_libs(self):
        """Info message should list which libs are not installed."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.write_text("nonexistent-package==1.0.0")

        with patch(
            "abstra_internals.services.requirements.get_uninstalled_requirements",
            return_value=["nonexistent-package"],
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            uninstalled_issues = [
                i for i in issues if isinstance(i, UninstalledLibsInRequirements)
            ]
            self.assertEqual(len(uninstalled_issues), 1)
            self.assertIn("nonexistent-package", uninstalled_issues[0].label)
            self.assertIn("pip install", uninstalled_issues[0].label.lower())

    def test_message_for_invalid_import(self):
        """Error message should suggest checking the import name."""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        script.file_path.write_text("import nonexistent_xyz_12345")

        with (
            patch(
                "abstra_internals.services.requirements.check_package",
                return_value="unknown",
            ),
            patch(
                "abstra_internals.services.requirements.get_uninstalled_requirements",
                return_value=[],
            ),
            patch.object(
                PyPIVerificationCache, "verify_package_exists", return_value=False
            ),
        ):
            rule = ImportsRequirementsAnalyzer()
            issues = rule.find_issues()

            invalid_issues = [i for i in issues if isinstance(i, InvalidImport)]
            self.assertEqual(len(invalid_issues), 1)
            # Message should suggest checking the package name
            self.assertIn("not found", invalid_issues[0].label.lower())
            self.assertIn("check", invalid_issues[0].label.lower())
