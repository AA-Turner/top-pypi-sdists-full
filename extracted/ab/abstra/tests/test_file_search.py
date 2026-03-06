import unittest
from pathlib import Path
from tempfile import mkdtemp

from abstra_internals.utils.file_search import (
    find_files_by_glob,
    grep_files,
    list_directory_entries,
)
from tests.fixtures import rm_tree


def _make_tree(root: Path, spec: dict) -> None:
    """Recursively create files and directories described by *spec*.

    *spec* is a dict where:
    - a key whose value is a dict creates a subdirectory
    - a key whose value is a str creates a file with that content
    """
    for name, content in spec.items():
        path = root / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            _make_tree(path, content)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")


class TestListDirectoryEntries(unittest.TestCase):
    def setUp(self):
        self.root = Path(mkdtemp())
        _make_tree(
            self.root,
            {
                "alpha.py": "x = 1",
                "beta.txt": "hello",
                "subdir": {
                    "nested.py": "y = 2",
                },
                "gamma.json": "{}",
            },
        )

    def tearDown(self):
        rm_tree(self.root)

    def test_returns_immediate_children_only(self):
        entries = list_directory_entries(self.root)
        names = {e["name"] for e in entries}
        # immediate children
        self.assertIn("alpha.py", names)
        self.assertIn("beta.txt", names)
        self.assertIn("subdir", names)
        self.assertIn("gamma.json", names)
        # nested file must NOT appear
        self.assertNotIn("nested.py", names)

    def test_dirs_come_before_files(self):
        entries = list_directory_entries(self.root)
        types = [e["type"] for e in entries]
        # Find the last "dir" and first "file" index
        last_dir = max((i for i, t in enumerate(types) if t == "dir"), default=-1)
        first_file = min((i for i, t in enumerate(types) if t == "file"), default=999)
        self.assertLess(last_dir, first_file)

    def test_file_entries_have_correct_metadata(self):
        entries = {e["name"]: e for e in list_directory_entries(self.root)}

        py_entry = entries["alpha.py"]
        self.assertEqual(py_entry["type"], "file")
        self.assertEqual(py_entry["extension"], ".py")
        self.assertGreater(py_entry["size_bytes"], 0)

        dir_entry = entries["subdir"]
        self.assertEqual(dir_entry["type"], "dir")
        self.assertEqual(dir_entry["extension"], "")
        self.assertEqual(dir_entry["size_bytes"], 0)

    def test_returns_empty_list_for_nonexistent_directory(self):
        result = list_directory_entries(self.root / "does_not_exist")
        self.assertEqual(result, [])

    def test_returns_empty_list_for_file_path(self):
        result = list_directory_entries(self.root / "alpha.py")
        self.assertEqual(result, [])

    def test_is_ignored_fn_filters_entries(self):
        # Ignore anything named "subdir"
        ignored = list_directory_entries(
            self.root, is_ignored_fn=lambda p: p.name == "subdir"
        )
        names = {e["name"] for e in ignored}
        self.assertNotIn("subdir", names)
        self.assertIn("alpha.py", names)

    def test_empty_directory(self):
        empty = self.root / "empty_dir"
        empty.mkdir()
        self.assertEqual(list_directory_entries(empty), [])

    def test_extension_is_lowercase(self):
        mixed = self.root / "Data.CSV"
        mixed.write_text("a,b,c")
        entries = {e["name"]: e for e in list_directory_entries(self.root)}
        self.assertEqual(entries["Data.CSV"]["extension"], ".csv")


class TestFindFilesByGlob(unittest.TestCase):
    def setUp(self):
        self.root = Path(mkdtemp())
        _make_tree(
            self.root,
            {
                "main.py": "import os",
                "utils.py": "pass",
                "README.md": "# readme",
                "src": {
                    "api.py": "x = 1",
                    "helpers.py": "y = 2",
                    "deep": {
                        "core.py": "z = 3",
                        "data.json": "{}",
                    },
                },
                "tests": {
                    "test_main.py": "import unittest",
                    "test_api.py": "import unittest",
                },
            },
        )

    def tearDown(self):
        rm_tree(self.root)

    def test_recursive_glob_all_python_files(self):
        results = find_files_by_glob(self.root, "**/*.py")
        self.assertIn("main.py", results)
        self.assertIn("utils.py", results)
        self.assertIn("src/api.py", results)
        self.assertIn("src/helpers.py", results)
        self.assertIn("src/deep/core.py", results)
        self.assertIn("tests/test_main.py", results)
        self.assertIn("tests/test_api.py", results)
        # Non-.py files must not appear
        self.assertNotIn("README.md", results)
        self.assertNotIn("src/deep/data.json", results)

    def test_scoped_glob(self):
        results = find_files_by_glob(self.root, "src/**/*.py")
        self.assertIn("src/api.py", results)
        self.assertIn("src/deep/core.py", results)
        self.assertNotIn("main.py", results)
        self.assertNotIn("tests/test_main.py", results)

    def test_bare_word_expansion(self):
        # "utils" should expand to "**/utils*" and find utils.py
        results = find_files_by_glob(self.root, "utils")
        self.assertIn("utils.py", results)

    def test_bare_word_finds_in_nested_directory(self):
        # "core" should find src/deep/core.py
        results = find_files_by_glob(self.root, "core")
        self.assertIn("src/deep/core.py", results)

    def test_max_results_limits_output(self):
        results = find_files_by_glob(self.root, "**/*.py", max_results=3)
        self.assertLessEqual(len(results), 3)

    def test_no_matches_returns_empty_list(self):
        results = find_files_by_glob(self.root, "**/*.nonexistent")
        self.assertEqual(results, [])

    def test_results_are_sorted(self):
        results = find_files_by_glob(self.root, "**/*.py")
        self.assertEqual(results, sorted(results))

    def test_nonexistent_root_returns_empty(self):
        results = find_files_by_glob(self.root / "ghost", "**/*.py")
        self.assertEqual(results, [])

    def test_directories_are_excluded(self):
        results = find_files_by_glob(self.root, "**/*")
        for path in results:
            self.assertTrue((self.root / path).is_file(), f"{path!r} is not a file")

    def test_is_ignored_fn_excludes_files(self):
        # Exclude the entire "tests" directory
        results = find_files_by_glob(
            self.root,
            "**/*.py",
            is_ignored_fn=lambda p: "tests" in p.parts,
        )
        for r in results:
            self.assertNotIn("tests", r)
        self.assertIn("main.py", results)


class TestGrepFiles(unittest.TestCase):
    def setUp(self):
        self.root = Path(mkdtemp())
        _make_tree(
            self.root,
            {
                "alpha.py": "def foo():\n    return 42\n\n# TODO: fix this\n",
                "beta.py": "import os\nFoo = foo()\n",
                "gamma.txt": "This is a TODO item\nAnother line\n",
                "delta.py": (
                    "class MyClass:\n    def my_method(self):\n        pass\n"
                ),
                "sub": {
                    "epsilon.py": "# nothing special\n",
                    "zeta.py": "def foo():\n    pass\n",
                },
            },
        )

    def tearDown(self):
        rm_tree(self.root)

    def test_basic_substring_search(self):
        results = grep_files(self.root, "def foo")
        files = {r["file"] for r in results}
        self.assertIn("alpha.py", files)
        self.assertIn("sub/zeta.py", files)
        self.assertNotIn("beta.py", files)

    def test_case_insensitive_search(self):
        results = grep_files(
            self.root, "todo", file_pattern="**/*", case_sensitive=False
        )
        files = {r["file"] for r in results}
        # Both alpha.py ("# TODO") and gamma.txt ("TODO") should match
        self.assertIn("alpha.py", files)
        self.assertIn("gamma.txt", files)

    def test_case_sensitive_search_excludes_lowercase(self):
        results = grep_files(
            self.root, "TODO", file_pattern="**/*", case_sensitive=True
        )
        for r in results:
            self.assertIn("TODO", r["line"])

    def test_file_pattern_scopes_search(self):
        results = grep_files(self.root, "foo", file_pattern="**/*.py")
        files = {r["file"] for r in results}
        # gamma.txt does not contain "foo" but even if it did it would be excluded
        self.assertNotIn("gamma.txt", files)

    def test_result_has_correct_structure(self):
        results = grep_files(self.root, "def foo")
        self.assertTrue(len(results) > 0)
        for r in results:
            self.assertIn("file", r)
            self.assertIn("line_number", r)
            self.assertIn("line", r)
            self.assertIsInstance(r["line_number"], int)
            self.assertGreater(r["line_number"], 0)

    def test_line_number_is_correct(self):
        # "def foo" is the first line in alpha.py
        results = grep_files(self.root, "def foo", file_pattern="alpha.py")
        match = next(r for r in results if r["file"] == "alpha.py")
        self.assertEqual(match["line_number"], 1)

    def test_max_results_limits_total_across_files(self):
        # alpha.py and sub/zeta.py both have "def foo"
        results = grep_files(self.root, "def foo", max_results=1)
        self.assertEqual(len(results), 1)

    def test_no_matches_returns_empty_list(self):
        results = grep_files(self.root, "XYZZY_IMPOSSIBLE_STRING")
        self.assertEqual(results, [])

    def test_regex_pattern(self):
        results = grep_files(self.root, r"def \w+\(", file_pattern="**/*.py")
        # Should match "def foo():" and "def my_method(self):"
        files = {r["file"] for r in results}
        self.assertIn("alpha.py", files)
        self.assertIn("delta.py", files)

    def test_invalid_regex_falls_back_to_literal(self):
        # "[unclosed" is an invalid regex; should not raise, treats as literal
        results = grep_files(self.root, "[unclosed")
        # There's no literal "[unclosed" in any file, so result is empty
        self.assertEqual(results, [])

    def test_is_ignored_fn_excludes_files(self):
        results = grep_files(
            self.root,
            "def foo",
            file_pattern="**/*.py",
            is_ignored_fn=lambda p: p.name == "zeta.py",
        )
        files = {r["file"] for r in results}
        self.assertNotIn("sub/zeta.py", files)
        self.assertIn("alpha.py", files)

    def test_trailing_newlines_stripped_from_lines(self):
        results = grep_files(self.root, "def foo")
        for r in results:
            self.assertFalse(
                r["line"].endswith("\n"),
                f"Line should not end with newline: {r['line']!r}",
            )

    def test_nonexistent_root_returns_empty(self):
        results = grep_files(self.root / "ghost", "foo")
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
