import ast
import unittest

from abstra_internals.repositories.linter.rules.abstra_dir_reference import (
    AbstraDirReference,
)


class TestAbstraDirReference(unittest.TestCase):
    def setUp(self):
        self.rule = AbstraDirReference()

    def _refs(self, code: str):
        return list(self.rule._find_abstra_refs(ast.parse(code)))

    def test_detects_uploads_path(self):
        code = 'open(".abstra/uploads/data.csv")'
        refs = self._refs(code)
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0][0], ".abstra/uploads/data.csv")

    def test_detects_persistent_path(self):
        code = 'p = ".abstra/persistent/keys.json"'
        self.assertEqual(len(self._refs(code)), 1)

    def test_detects_any_abstra_segment(self):
        code = 'p = ".abstra/anything/file.txt"'
        self.assertEqual(len(self._refs(code)), 1)

    def test_detects_path_constructor(self):
        code = 'from pathlib import Path\nPath(".abstra/persistent")'
        self.assertEqual(len(self._refs(code)), 1)

    def test_detects_fstring(self):
        code = 'name = "x"\np = f".abstra/uploads/{name}.csv"'
        refs = self._refs(code)
        self.assertEqual(len(refs), 1)

    def test_detects_trailing_segment(self):
        code = 'd = ".abstra"'
        self.assertEqual(len(self._refs(code)), 1)

    def test_reports_line_number(self):
        code = 'x = 1\ny = 2\np = ".abstra/uploads/a.txt"'
        refs = self._refs(code)
        self.assertEqual(refs[0][1], 3)

    def test_ignores_helper_usage(self):
        code = (
            "from abstra.common import get_persistent_dir\n"
            'p = get_persistent_dir() / "uploads" / "a.csv"'
        )
        self.assertEqual(self._refs(code), [])

    def test_ignores_dotted_name_in_string(self):
        code = 'mod = "my.abstra.module"'
        self.assertEqual(self._refs(code), [])

    def test_ignores_empty_file(self):
        self.assertEqual(self._refs(""), [])

    def test_ignores_unrelated_string(self):
        code = 'msg = "hello world"'
        self.assertEqual(self._refs(code), [])
