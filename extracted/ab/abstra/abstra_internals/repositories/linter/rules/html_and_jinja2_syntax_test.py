from abstra_internals.repositories.linter.rules.html_and_jinja2_syntax import (
    HtmlAndJinja2Syntax,
)
from tests.fixtures import BaseTest


class HtmlAndJinja2SyntaxTest(BaseTest):
    def test_no_html_files(self):
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_full_page(self):
        (self.root / "page.html").write_text(
            "<html><head><title>Test</title></head>"
            "<body><div><p>Hello</p></div></body></html>"
        )
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_fragment(self):
        (self.root / "fragment.html").write_text("<div><p>Hello</p></div>")
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_with_doctype(self):
        (self.root / "doctype.html").write_text(
            "<!DOCTYPE html><html><head><title>T</title></head>"
            "<body><p>Hi</p></body></html>"
        )
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_invalid_unclosed_tag(self):
        (self.root / "bad.html").write_text("<div><p>unclosed<span></div>")
        rule = HtmlAndJinja2Syntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertIn("bad.html", issues[0].label)

    def test_empty_file(self):
        (self.root / "empty.html").touch()
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_multiple_files_mixed(self):
        (self.root / "good.html").write_text("<div><p>Hello</p></div>")
        (self.root / "bad.html").write_text("<div><p>unclosed<span></div>")
        rule = HtmlAndJinja2Syntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        issue_labels = [issue.label for issue in issues]
        self.assertTrue(any("bad.html" in label for label in issue_labels))
        self.assertFalse(any("good.html" in label for label in issue_labels))

    def test_non_utf8_file_is_skipped(self):
        (self.root / "binary.html").write_bytes(b"\x80\x81\x82\x83")
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_valid_jinja2_template(self):
        (self.root / "template.html").write_text(
            "<html><head><title>{{ title }}</title></head>"
            "<body>{% for item in items %}<li>{{ item }}</li>{% endfor %}"
            "{# a comment #}</body></html>"
        )
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)

    def test_invalid_jinja2_syntax(self):
        (self.root / "broken.html").write_text(
            "<html><body>{% if x %}<p>hi</p></body></html>"
        )
        rule = HtmlAndJinja2Syntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("Jinja2:" in issue.label for issue in issues))
        self.assertTrue(any("broken.html" in issue.label for issue in issues))

    def test_jinja2_template_with_bad_html(self):
        (self.root / "mixed.html").write_text("<div>{{ value }}<p>unclosed<span></div>")
        rule = HtmlAndJinja2Syntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("HTML:" in issue.label for issue in issues))
        self.assertTrue(any("mixed.html" in issue.label for issue in issues))

    def test_line_numbers_preserved_after_strip(self):
        (self.root / "multiline.html").write_text(
            "{% block content %}\n"
            "  {{ var }}\n"
            "{% endblock %}\n"
            "<div><p>unclosed<span></div>\n"
        )
        rule = HtmlAndJinja2Syntax()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        self.assertTrue(any("line 4" in issue.label for issue in issues))

    def test_jinja2_attribute_interpolation(self):
        (self.root / "attrs.html").write_text(
            '<a href="{{ url }}" class="{% if active %}on{% endif %}">x</a>'
        )
        rule = HtmlAndJinja2Syntax()
        self.assertEqual(len(rule.find_issues()), 0)
