from abstra_internals.repositories.linter.rules.js_syntax import JsSyntax
from tests.fixtures import BaseTest


class JsSyntaxTest(BaseTest):
    def test_no_js_files(self):
        rule = JsSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_js(self):
        (self.root / "app.js").write_text("function foo() { return 1; }")
        rule = JsSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_es6(self):
        (self.root / "app.js").write_text("const x = () => 42; let y = `hello ${x()}`;")
        rule = JsSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_module(self):
        (self.root / "app.js").write_text(
            'import { foo } from "bar"; export default 42;'
        )
        rule = JsSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_es2022(self):
        (self.root / "app.js").write_text(
            'const x = obj?.foo ?? "default"; class Foo { #bar = 1; }'
        )
        rule = JsSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_invalid_syntax(self):
        (self.root / "bad.js").write_text("function foo( { return 1; }")
        rule = JsSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertIn("bad.js", issues[0].label)

    def test_invalid_unclosed_string(self):
        (self.root / "bad.js").write_text('var x = "hello;')
        rule = JsSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertIn("bad.js", issues[0].label)

    def test_invalid_unclosed_brace(self):
        (self.root / "bad.js").write_text("if (true) { console.log(1);")
        rule = JsSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)

    def test_invalid_unexpected_token(self):
        (self.root / "bad.js").write_text("const x = ;")
        rule = JsSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)

    def test_invalid_double_comma(self):
        (self.root / "bad.js").write_text("var arr = [1,,2];")
        rule = JsSyntax()
        # Double comma creates a hole (elision) — valid JS, not an error
        # tree-sitter handles this correctly
        issues = rule.find_issues()
        self.assertEqual(len(issues), 0)

    def test_empty_file(self):
        (self.root / "empty.js").touch()
        rule = JsSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_multiple_files_mixed(self):
        (self.root / "good.js").write_text("var x = 1;")
        (self.root / "bad.js").write_text("var x = {;")
        rule = JsSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        issue_labels = [issue.label for issue in issues]
        self.assertTrue(any("bad.js" in label for label in issue_labels))
        self.assertFalse(any("good.js" in label for label in issue_labels))

    def test_unreadable_file_is_skipped(self):
        (self.root / "bad.js").write_text("var x = 1;")
        # Make the file unreadable
        (self.root / "bad.js").chmod(0o000)
        rule = JsSyntax()
        issues = rule.find_issues()
        self.assertEqual(len(issues), 0)
        # Restore permissions for cleanup
        (self.root / "bad.js").chmod(0o644)
