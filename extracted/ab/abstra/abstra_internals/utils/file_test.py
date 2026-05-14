import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from abstra_internals.utils.file import (
    _is_sdk_module,
    clear_local_modules,
    generate_conflictless_path,
    module2path,
    path2module,
    safe_write_file,
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

    def test_does_not_clear_sdk_modules(self):
        # Create a fake abstra_internals module structure under project root
        sdk_dir = self.root / "abstra_internals" / "controllers" / "sdk"
        sdk_dir.mkdir(parents=True)
        (self.root / "abstra_internals" / "__init__.py").write_text("")
        (self.root / "abstra_internals" / "controllers" / "__init__.py").write_text("")
        (
            self.root / "abstra_internals" / "controllers" / "sdk" / "__init__.py"
        ).write_text("")
        (sdk_dir / "sdk_context.py").write_text("class SDKContextStore: pass")

        # Create entrypoint that imports it
        main_file = self.root / "test_main_sdk.py"
        main_file.write_text(
            "from abstra_internals.controllers.sdk.sdk_context import SDKContextStore"
        )

        # Simulate these modules being in sys.modules
        sdk_module = type(sys)("abstra_internals.controllers.sdk.sdk_context")
        sys.modules["abstra_internals.controllers.sdk.sdk_context"] = sdk_module
        sys.modules["abstra_internals.controllers.sdk"] = type(sys)(
            "abstra_internals.controllers.sdk"
        )

        try:
            cleared = clear_local_modules(main_file, self.root)

            # SDK modules must NOT be cleared
            self.assertNotIn("abstra_internals.controllers.sdk.sdk_context", cleared)
            self.assertNotIn("abstra_internals.controllers.sdk", cleared)
            self.assertNotIn("abstra_internals.controllers", cleared)
            self.assertNotIn("abstra_internals", cleared)

            # SDK modules must still be in sys.modules
            self.assertIn("abstra_internals.controllers.sdk.sdk_context", sys.modules)
            self.assertIs(
                sys.modules["abstra_internals.controllers.sdk.sdk_context"], sdk_module
            )
        finally:
            # Clean up SDK modules we added
            for key in list(sys.modules.keys()):
                if key.startswith("abstra_internals.controllers.sdk"):
                    del sys.modules[key]


class SafeWriteFileTest(unittest.TestCase):
    """
    Regression tests for the CRLF blank-line doubling bug.

    On Windows, the Monaco editor model uses "\\r\\n" line endings by default.
    Python's ``Path.write_text`` with the default ``newline=None`` translates
    every "\\n" it sees into ``os.linesep`` ("\\r\\n"), so an editor save of
    ``"foo\\r\\n"`` becomes ``"foo\\r\\r\\n"`` on disk. The next universal-
    newline read interprets ``\\r\\r\\n`` as TWO line breaks, doubling every
    blank line on every save/read cycle (1 -> 3 -> 7 -> ...).

    ``safe_write_file`` must always disable newline translation.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fp = Path(self.temp_dir) / "regression.py"

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_does_not_use_write_text(self):
        # White-box guard: on Linux CI the byte-level tests below are trivially
        # green because os.linesep is "\\n", so we explicitly assert that the
        # call site never uses write_text. write_text with the default
        # newline=None translates "\\n" -> os.linesep on Windows and is the
        # exact root cause of the doubling bug. write_bytes is the safe choice
        # and works on every supported Python version (3.9+).
        with (
            mock.patch.object(Path, "write_text") as mt,
            mock.patch.object(Path, "write_bytes", return_value=None) as mb,
        ):
            self.assertTrue(safe_write_file(self.fp, "anything"))
            mt.assert_not_called()
            mb.assert_called_once()

    def test_lf_input_is_written_verbatim(self):
        content = "a\nb\nc\n"
        self.assertTrue(safe_write_file(self.fp, content))
        self.assertEqual(self.fp.read_bytes(), content.encode("utf-8"))

    def test_crlf_input_is_written_verbatim(self):
        # The exact input shape produced by Monaco-on-Windows.
        content = "a\r\nb\r\nc\r\n"
        self.assertTrue(safe_write_file(self.fp, content))
        on_disk = self.fp.read_bytes()
        self.assertEqual(on_disk, content.encode("utf-8"))
        self.assertNotIn(
            b"\r\r\n",
            on_disk,
            "safe_write_file must never produce \\r\\r\\n on disk; that is the "
            "byte sequence that gets read back as a doubled blank line.",
        )

    def test_crlf_save_read_round_trip_does_not_amplify_blank_lines(self):
        # End-to-end property: simulate the editor save / backend read loop and
        # confirm the number of newlines stays constant. Without the fix this
        # grows exponentially on Windows.
        content = "a\r\nb\r\nc\r\n"
        for _ in range(5):
            self.assertTrue(safe_write_file(self.fp, content))
            # read_text uses universal newlines (matches the backend's
            # read_file_with_pagination), normalizing whatever is on disk.
            content = self.fp.read_text(encoding="utf-8")

        self.assertEqual(content, "a\nb\nc\n")
        self.assertNotIn("\n\n", content)


class IsSdkModuleTest(unittest.TestCase):
    def test_abstra_top_level(self):
        self.assertTrue(_is_sdk_module("abstra"))

    def test_abstra_submodule(self):
        self.assertTrue(_is_sdk_module("abstra.ai"))

    def test_abstra_internals_top_level(self):
        self.assertTrue(_is_sdk_module("abstra_internals"))

    def test_abstra_internals_deep(self):
        self.assertTrue(_is_sdk_module("abstra_internals.controllers.sdk.sdk_context"))

    def test_abstra_statics(self):
        self.assertTrue(_is_sdk_module("abstra_statics"))

    def test_user_module(self):
        self.assertFalse(_is_sdk_module("my_module"))

    def test_user_module_similar_name(self):
        self.assertFalse(_is_sdk_module("abstractions.utils"))
