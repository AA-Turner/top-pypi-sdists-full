import ast
import unittest

from abstra_internals.repositories.linter.rules.internal_page_reference import (
    InternalPageReference,
)


class TestInternalPageReference(unittest.TestCase):
    def setUp(self):
        self.rule = InternalPageReference()

    def _refs(self, code: str):
        return list(self.rule._find_page_refs(ast.parse(code)))

    def test_detects_redirect_to_internal_page(self):
        code = 'redirect("/_page/other-page")'
        refs = self._refs(code)
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0][0], "/_page/other-page")

    def test_detects_inline_html_href(self):
        code = "html = '<a href=\"/_page/dashboard\">Go</a>'"
        refs = self._refs(code)
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0][0], "/_page/dashboard")

    def test_detects_pages_metadata_prefix(self):
        code = 'url = "/_pages/some-page"'
        self.assertEqual(len(self._refs(code)), 1)

    def test_detects_page_home_prefix(self):
        code = 'url = "/_page-home"'
        self.assertEqual(len(self._refs(code)), 1)

    def test_detects_fstring(self):
        code = 'name = "x"\nurl = f"/_page/{name}"'
        refs = self._refs(code)
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0][0], "/_page/")

    def test_detects_multiple_in_one_literal(self):
        code = 'html = \'<a href="/_page/a">A</a><a href="/_page/b">B</a>\''
        refs = self._refs(code)
        self.assertEqual(len(refs), 2)

    def test_reports_line_number(self):
        code = 'x = 1\ny = 2\nredirect("/_page/thanks")'
        refs = self._refs(code)
        self.assertEqual(refs[0][1], 3)

    def test_ignores_clean_public_path(self):
        code = 'redirect("/other-page")'
        self.assertEqual(self._refs(code), [])

    def test_ignores_path_without_underscore(self):
        code = 'url = "/pages/list"'
        self.assertEqual(self._refs(code), [])

    def test_ignores_unrelated_string(self):
        code = 'msg = "hello world"'
        self.assertEqual(self._refs(code), [])

    def test_ignores_empty_file(self):
        self.assertEqual(self._refs(""), [])
