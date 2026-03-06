from abstra_internals.repositories.linter.rules.missing_packages_in_requirements import (
    MissingPackagesInRequirements,
)
from tests.fixtures import BaseTest


class MissingPackagesInRequirementsTest(BaseTest):
    def test_missing_packages_in_requirements_valid_default(self):
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_missing_packages_in_requirements_valid_with_packages(self):
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()
        requirements_file.write_text("pandas==1.0.0")
        script = self.controller.create_tasklet("New script", "script.py")
        code = "import pandas"
        script.file_path.write_text(code)
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_missing_packages_in_requirements_valid_with_packages_using_from_syntax(
        self,
    ):
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()
        requirements_file.write_text("pandas==1.0.0")
        script = self.controller.create_tasklet("New script", "script.py")
        code = "from pandas import foo"
        script.file_path.write_text(code)
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_missing_packages_in_requirements_invalid_requirements_file(self):
        script = self.controller.create_tasklet("New script", "script.py")
        code = "import pandas"
        script.file_path.write_text(code)
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 1)

    def test_missing_packages_in_requirements_invalid_requirements_file_using_from_syntax(
        self,
    ):
        script = self.controller.create_tasklet("New script", "script.py")
        code = "from pandas import foo"
        script.file_path.write_text(code)
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 1)

    def test_missing_packages_in_requirements_invalid_missing_package(self):
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()
        script = self.controller.create_tasklet("New script", "script.py")
        code = "import pandas"
        script.file_path.write_text(code)
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 1)

    def test_missing_packages_with_submodule_import(self):
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()
        script = self.controller.create_tasklet("New script", "script.py")
        code = "import pandas.plotting"
        script.file_path.write_text(code)
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 1)

    def test_missing_package_with_submodule_using_from_syntax(self):
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()
        script = self.controller.create_tasklet("New script", "script.py")
        code = "from pandas.plotting import foo"
        script.file_path.write_text(code)
        rule = MissingPackagesInRequirements()
        self.assertEqual(len(rule.find_issues()), 1)

    def test_does_not_suggest_local_folder_as_package(self):
        """Should not suggest adding local folders to requirements.txt"""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a local folder with Python files
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "helper.py").write_text("def helper(): pass")

        # Create script that imports from local folder
        script = self.controller.create_tasklet("New script", "script.py")
        code = "from utils.helper import helper"
        script.file_path.write_text(code)

        rule = MissingPackagesInRequirements()
        issues = rule.find_issues()

        # Should not suggest 'utils' as a missing package
        issue_packages = [
            issue.label for issue in issues if "utils" in issue.label.lower()
        ]
        self.assertEqual(len(issue_packages), 0)

    def test_does_not_suggest_local_python_file_as_package(self):
        """Should not suggest adding local .py files to requirements.txt"""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a local Python file
        (self.root / "mymodule.py").write_text("def foo(): pass")

        # Create script that imports from local file
        script = self.controller.create_tasklet("New script", "script.py")
        code = "from mymodule import foo"
        script.file_path.write_text(code)

        rule = MissingPackagesInRequirements()
        issues = rule.find_issues()

        # Should not suggest 'mymodule' as a missing package
        issue_packages = [
            issue.label for issue in issues if "mymodule" in issue.label.lower()
        ]
        self.assertEqual(len(issue_packages), 0)

    def test_does_not_suggest_local_folder_with_init_py(self):
        """Should not suggest adding local packages (with __init__.py) to requirements.txt"""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        # Create a local package with __init__.py
        utils_dir = self.root / "utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("")
        (utils_dir / "helper.py").write_text("def helper(): pass")

        # Create script that imports from local package
        script = self.controller.create_tasklet("New script", "script.py")
        code = "from utils import helper"
        script.file_path.write_text(code)

        rule = MissingPackagesInRequirements()
        issues = rule.find_issues()

        # Should not suggest 'utils' as a missing package
        issue_packages = [
            issue.label for issue in issues if "utils" in issue.label.lower()
        ]
        self.assertEqual(len(issue_packages), 0)

    def test_fix_adds_package_without_version(self):
        """Fix should add package without version for pip compatibility"""
        requirements_file = self.root / "requirements.txt"
        requirements_file.touch()

        script = self.controller.create_tasklet("New script", "script.py")
        code = "import pandas"
        script.file_path.write_text(code)

        rule = MissingPackagesInRequirements()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)

        # Apply the fix
        issues[0].fixes[0].fix()

        # Verify package was added without version
        requirements_content = requirements_file.read_text()
        requirements_lines = requirements_content.strip().split("\n")
        pandas_lines = [
            line for line in requirements_lines if line.startswith("pandas")
        ]
        self.assertEqual(len(pandas_lines), 1)
        self.assertEqual(pandas_lines[0], "pandas")
