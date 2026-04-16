from abstra_internals.repositories.linter.rules.css_syntax import CssSyntax
from tests.fixtures import BaseTest


class CssSyntaxTest(BaseTest):
    def test_no_css_files(self):
        rule = CssSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_css(self):
        (self.root / "style.css").write_text("body { color: red; margin: 0; }")
        rule = CssSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_css_with_at_rules(self):
        (self.root / "style.css").write_text(
            "@media (max-width: 600px) { body { color: blue; } }"
        )
        rule = CssSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_invalid_declaration_missing_name(self):
        (self.root / "bad.css").write_text("body { : red; }")
        rule = CssSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertIn("bad.css", issues[0].label)

    def test_invalid_declaration_missing_colon(self):
        (self.root / "bad.css").write_text("body { color red; }")
        rule = CssSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertIn("bad.css", issues[0].label)

    def test_empty_file(self):
        (self.root / "empty.css").touch()
        rule = CssSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_multiple_files_mixed(self):
        (self.root / "good.css").write_text("body { color: red; }")
        (self.root / "bad.css").write_text("body { : red; }")
        rule = CssSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        issue_labels = [issue.label for issue in issues]
        self.assertTrue(any("bad.css" in label for label in issue_labels))
        self.assertFalse(any("good.css" in label for label in issue_labels))

    def test_multiple_errors_single_issue(self):
        (self.root / "bad.css").write_text("body { : red; color red; }")
        rule = CssSyntax()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 1)
        self.assertIn("bad.css", issues[0].label)
        self.assertGreater(issues[0].label.count("  - "), 1)

    def test_non_utf8_file_is_skipped(self):
        (self.root / "binary.css").write_bytes(b"\x80\x81\x82\x83")
        rule = CssSyntax()
        self.assertEqual(len(rule.find_issues()), 0)
