import sys
import tempfile
import unittest
from pathlib import Path

from abstra_internals.utils.file import (
    clear_local_modules,
    generate_conflictless_path,
    module2path,
    path2module,
)


class Module2PathTest(unittest.TestCase):
    def test_module2path_module(self):
        module = "a.b.c"
        path = module2path(module, False)
        self.assertEqual(path, Path("a", "b", "c.py"))

    def test_module2path_package(self):
        module = "a.b.c"
        path = module2path(module, True)
        self.assertEqual(path, Path("a", "b", "c", "__init__.py"))


class Path2ModuleTest(unittest.TestCase):
    def test_path2module_module(self):
        path = Path("a", "b", "c.py")
        module = path2module(path)
        self.assertEqual(module, "a.b.c")

    def test_path2module_package(self):
        path = Path("a", "b", "c", "__init__.py")
        module = path2module(path)
        self.assertEqual(module, "a.b.c")


class CreatePathTest(unittest.TestCase):
    def test_without_conflict(self):
        self.assertEqual(generate_conflictless_path("file"), "file")

    def test_conflict_with_static_path(self):
        path = "login"
        generated_path = generate_conflictless_path(path)

        self.assertNotEqual(generated_path, path)
        self.assertIn(path + "-", generated_path)

    def test_conflict_with_dynamic_path(self):
        path = "error/some-error"
        generated_path = generate_conflictless_path(path)

        self.assertNotEqual(generated_path, path)
        self.assertIn(path + "-", generated_path)


class ClearLocalModulesTest(unittest.TestCase):
    def setUp(self):
        import os

        self.temp_dir = tempfile.mkdtemp()
        self.root = Path(self.temp_dir)
        self.original_cwd = os.getcwd()
        # Change to temp dir so traverse_code can find files
        os.chdir(self.temp_dir)

    def tearDown(self):
        import os
        import shutil

        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        # Clean up any modules we added during tests (all test modules start with "test_")
        for key in list(sys.modules.keys()):
            if key.startswith("test_"):
                del sys.modules[key]

    def test_clears_simple_import_from_sys_modules(self):
        # Create a simple module
        helper_file = self.root / "test_helper_simple.py"
        helper_file.write_text("VALUE = 42")

        # Create entrypoint that imports it
        main_file = self.root / "test_main_simple.py"
        main_file.write_text("import test_helper_simple")

        # Simulate the module being in sys.modules (as if previously imported)
        sys.modules["test_helper_simple"] = type(sys)("test_helper_simple")

        # Clear modules
        cleared = clear_local_modules(main_file, self.root)

        # Verify it was cleared
        self.assertIn("test_helper_simple", cleared)
        self.assertNotIn("test_helper_simple", sys.modules)

    def test_clears_dotted_import_from_sys_modules(self):
        # Create a package structure
        utils_dir = self.root / "test_utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("")
        (utils_dir / "test_helper_dotted.py").write_text("VALUE = 42")

        # Create entrypoint that imports it
        main_file = self.root / "test_main_dotted.py"
        main_file.write_text("from test_utils.test_helper_dotted import VALUE")

        # Simulate the module being in sys.modules
        sys.modules["test_utils.test_helper_dotted"] = type(sys)(
            "test_utils.test_helper_dotted"
        )

        # Clear modules
        cleared = clear_local_modules(main_file, self.root)

        # Verify dotted name was cleared
        self.assertIn("test_utils.test_helper_dotted", cleared)
        self.assertNotIn("test_utils.test_helper_dotted", sys.modules)

    def test_does_not_crash_on_syntax_error(self):
        # Create a file with syntax error
        bad_file = self.root / "test_bad_syntax.py"
        bad_file.write_text("def broken(")

        # Should not raise, just return empty set
        cleared = clear_local_modules(bad_file, self.root)
        self.assertEqual(cleared, set())

    def test_does_not_crash_on_missing_file(self):
        missing_file = self.root / "test_nonexistent.py"

        # Should not raise
        cleared = clear_local_modules(missing_file, self.root)
        self.assertEqual(cleared, set())

    def test_clears_parent_package_modules(self):
        # Create a package structure
        utils_dir = self.root / "test_utils"
        utils_dir.mkdir()
        (utils_dir / "__init__.py").write_text("")
        (utils_dir / "test_helper_dotted.py").write_text("VALUE = 42")

        # Create entrypoint that imports it
        main_file = self.root / "test_main_parent.py"
        main_file.write_text("from test_utils.test_helper_dotted import VALUE")

        # Simulate both the child module and parent package being in sys.modules
        sys.modules["test_utils.test_helper_dotted"] = type(sys)(
            "test_utils.test_helper_dotted"
        )
        sys.modules["test_utils"] = type(sys)("test_utils")

        # Clear modules
        cleared = clear_local_modules(main_file, self.root)

        # Verify both child and parent were cleared
        self.assertIn("test_utils.test_helper_dotted", cleared)
        self.assertIn("test_utils", cleared)
        self.assertNotIn("test_utils.test_helper_dotted", sys.modules)
        self.assertNotIn("test_utils", sys.modules)

    def test_clears_entrypoint_file_from_sys_modules(self):
        # Create entrypoint file
        main_file = self.root / "test_entrypoint.py"
        main_file.write_text("VALUE = 42")

        # Simulate the entrypoint being in sys.modules (as if previously imported)
        sys.modules["test_entrypoint"] = type(sys)("test_entrypoint")

        # Clear modules
        cleared = clear_local_modules(main_file, self.root)

        # Verify the entrypoint itself was cleared
        self.assertIn("test_entrypoint", cleared)
        self.assertNotIn("test_entrypoint", sys.modules)
