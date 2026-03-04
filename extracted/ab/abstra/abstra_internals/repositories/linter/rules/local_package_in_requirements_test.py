from abstra_internals.repositories.linter.rules.local_package_in_requirements import (
    LocalPackageInRequirements,
)
from abstra_internals.services.requirements import RequirementsRepository
from tests.fixtures import BaseTest


class TestLocalPackageInRequirements(BaseTest):
    def test_no_issues_when_no_conflicts(self):
        """No issues when requirements.txt packages don't conflict with local folders"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("requests==2.28.0\nflask==2.0.0")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 0)

    def test_no_issues_when_no_requirements_file(self):
        """No issues when there's no requirements.txt"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.unlink()

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 0)

    def test_no_issues_when_folder_has_no_python_files(self):
        """No issues when local folder exists but has no Python files"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("utils==1.0.0")

        # Create folder without Python files
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "readme.md").write_text("# Utils")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 0)

    def test_detects_conflict_with_local_folder(self):
        """Detects when package in requirements.txt conflicts with local folder"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("utils==1.0.0")

        # Create local folder with Python file
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("utils", issues[0].label)
        self.assertIn("conflicts", issues[0].label.lower())

    def test_detects_conflict_even_with_init_py(self):
        """Detects conflict even when local folder has __init__.py"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("utils==1.0.0")

        # Create local folder with __init__.py
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("")
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 1)

    def test_fix_removes_conflicting_package(self):
        """Fix removes the conflicting package from requirements.txt"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("utils==1.0.0\nrequests==2.28.0")

        # Create local folder
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 1)

        # Apply the first fix (remove from requirements.txt)
        issues[0].fixes[0].fix()

        # Verify package was removed
        requirements = RequirementsRepository.load()
        package_names = [lib.name for lib in requirements.libraries]
        self.assertNotIn("utils", package_names)
        self.assertIn("requests", package_names)

    def test_fix_also_adds_init_py_when_missing(self):
        """Fix removes package and also adds __init__.py to folder when missing"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("utils==1.0.0")

        # Create local folder without __init__.py
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 1)

        # Should have 1 fix (remove package, which also adds __init__.py)
        self.assertEqual(len(issues[0].fixes), 1)

        # Apply the fix
        issues[0].fixes[0].fix()

        # Verify __init__.py was created
        self.assertTrue((utils_dir / "__init__.py").exists())

        # Verify package was removed
        requirements = RequirementsRepository.load()
        package_names = [lib.name for lib in requirements.libraries]
        self.assertNotIn("utils", package_names)

    def test_fix_does_not_overwrite_existing_init_py(self):
        """Fix does not overwrite existing __init__.py"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("utils==1.0.0")

        # Create local folder with __init__.py containing content
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("# existing content")
        (utils_dir / "helper.py").write_text("def helper(): pass")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 1)

        # Apply the fix
        issues[0].fixes[0].fix()

        # Verify __init__.py was not overwritten
        self.assertEqual((utils_dir / "__init__.py").read_text(), "# existing content")

    def test_detects_multiple_conflicts(self):
        """Detects multiple conflicting packages"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("utils==1.0.0\nhelpers==2.0.0\nrequests==2.28.0")

        # Create multiple local folders
        for folder_name in ["utils", "helpers"]:
            folder = self.root / folder_name
            folder.mkdir()
            (folder / "module.py").write_text("# module")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 2)

        # Check that both conflicts are detected by checking labels
        labels = {issue.label for issue in issues}
        self.assertTrue(any("utils" in label for label in labels))
        self.assertTrue(any("helpers" in label for label in labels))

    def test_detects_conflict_with_local_file(self):
        """Detects when package in requirements.txt conflicts with local .py file"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("mymodule==1.0.0")

        # Create local Python file (not a folder)
        (self.root / "mymodule.py").write_text("def foo(): pass")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("mymodule", issues[0].label)
        self.assertIn("mymodule.py", issues[0].label)  # Should mention it's a file

    def test_only_remove_fix_for_file_conflict(self):
        """Only offers remove fix when conflict is with a file (not folder)"""
        requirements_txt = self.root / "requirements.txt"
        requirements_txt.write_text("mymodule==1.0.0")

        # Create local Python file
        (self.root / "mymodule.py").write_text("def foo(): pass")

        issues = LocalPackageInRequirements().find_issues()
        self.assertEqual(len(issues), 1)

        # Should only have 1 fix (remove package) - no __init__.py fix for files
        self.assertEqual(len(issues[0].fixes), 1)
        self.assertIn("Remove", issues[0].fixes[0].label)
