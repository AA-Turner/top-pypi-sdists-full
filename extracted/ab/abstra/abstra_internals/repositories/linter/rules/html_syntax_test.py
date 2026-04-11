from abstra_internals.repositories.linter.rules.html_syntax import HtmlSyntax
from tests.fixtures import BaseTest


class HtmlSyntaxTest(BaseTest):
    def test_no_html_files(self):
        rule = HtmlSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_full_page(self):
        (self.root / "page.html").write_text(
            "<html><head><title>Test</title></head>"
            "<body><div><p>Hello</p></div></body></html>"
        )
        rule = HtmlSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_fragment(self):
        (self.root / "fragment.html").write_text("<div><p>Hello</p></div>")
        rule = HtmlSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_with_doctype(self):
        (self.root / "doctype.html").write_text(
            "<!DOCTYPE html><html><head><title>T</title></head>"
            "<body><p>Hi</p></body></html>"
        )
        rule = HtmlSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_invalid_unclosed_tag(self):
        (self.root / "bad.html").write_text("<div><p>unclosed<span></div>")
        rule = HtmlSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertIn("bad.html", issues[0].label)

    def test_empty_file(self):
        (self.root / "empty.html").touch()
        rule = HtmlSyntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_multiple_files_mixed(self):
        (self.root / "good.html").write_text("<div><p>Hello</p></div>")
        (self.root / "bad.html").write_text("<div><p>unclosed<span></div>")
        rule = HtmlSyntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        issue_labels = [issue.label for issue in issues]
        self.assertTrue(any("bad.html" in label for label in issue_labels))
        self.assertFalse(any("good.html" in label for label in issue_labels))

    def test_non_utf8_file_is_skipped(self):
        (self.root / "binary.html").write_bytes(b"\x80\x81\x82\x83")
        rule = HtmlSyntax()
        self.assertEqual(len(rule.find_issues()), 0)
