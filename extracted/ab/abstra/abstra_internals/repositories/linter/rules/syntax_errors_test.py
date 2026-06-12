from pathlib import Path

from abstra_internals.repositories.linter.rules.syntax_errors import SyntaxErrors
from tests.fixtures import BaseTest


class SyntaxErrorsTest(BaseTest):
    def test_syntax_errors_valid_default(self):
        rule = SyntaxErrors()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_syntax_errors_valid_empty_file(self):
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        script.file_path.touch()
        rule = SyntaxErrors()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_syntax_errors_valid_with_content(self):
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        script.file_path.write_text("print('hello world')")
        rule = SyntaxErrors()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_syntax_errors_invalid_with_syntax_error(self):
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        script.file_path.write_text("print('hello world'")
        rule = SyntaxErrors()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn(Path(script.file).name, issues[0].label)
        self.assertEqual(issues[0].path, "script.py")

    def test_syntax_errors_reports_every_broken_file(self):
        a = self.controller.create_stage("tasklet", "A", "broken_a.py")
        a.file_path.write_text("print('a'")
        b = self.controller.create_stage("tasklet", "B", "broken_b.py")
        b.file_path.write_text("def x(:")
        rule = SyntaxErrors()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 2)
        self.assertEqual(
            {issue.path for issue in issues}, {"broken_a.py", "broken_b.py"}
        )

    def test_syntax_errors_scoped_returns_only_that_file(self):
        a = self.controller.create_stage("tasklet", "A", "broken_a.py")
        a.file_path.write_text("print('a'")
        b = self.controller.create_stage("tasklet", "B", "broken_b.py")
        b.file_path.write_text("def x(:")
        rule = SyntaxErrors()
        issues = rule.find_issues(path=a.file_path)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].path, "broken_a.py")

    def test_syntax_errors_scoped_skips_non_project_file(self):
        script = self.controller.create_stage("tasklet", "New script", "script.py")
        script.file_path.write_text("print('ok')")
        scratch = script.file_path.parent / "scratch.py"
        scratch.write_text("def x(:")
        rule = SyntaxErrors()
        # scratch.py is not an entrypoint nor imported by one → out of domain
        self.assertEqual(len(rule.find_issues(path=scratch)), 0)
