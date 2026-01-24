import tempfile
from pathlib import Path
from unittest import TestCase

from .find_deps import find_deps


class TestFindDeps(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)

    def _create_file(self, name: str, content: str) -> Path:
        path = self.base_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_top_level_import(self):
        """Top-level imports should be detected"""
        self._create_file("foo.py", "")
        main = self._create_file("main.py", "import foo\n")

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, {Path("foo.py")})

    def test_top_level_import_from(self):
        """Top-level 'from X import Y' should be detected"""
        self._create_file("foo.py", "")
        main = self._create_file("main.py", "from foo import bar\n")

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, {Path("foo.py")})

    def test_import_inside_function_is_ignored(self):
        """Imports inside functions should be ignored (runtime/lazy imports)"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
def my_func():
    import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_import_from_inside_function_is_ignored(self):
        """'from X import Y' inside functions should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
def my_func():
    from foo import bar
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_import_inside_method_is_ignored(self):
        """Imports inside class methods should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
class MyClass:
    def my_method(self):
        import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_import_inside_async_function_is_ignored(self):
        """Imports inside async functions should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
async def my_async_func():
    import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_import_inside_type_checking_is_ignored(self):
        """Imports inside TYPE_CHECKING blocks should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_mixed_imports(self):
        """Only top-level imports should be detected, not runtime ones"""
        self._create_file("foo.py", "")
        self._create_file("bar.py", "")
        self._create_file("baz.py", "")
        main = self._create_file(
            "main.py",
            """
import foo

def my_func():
    import bar

class MyClass:
    def method(self):
        from baz import something
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, {Path("foo.py")})

    def test_nested_function_import_is_ignored(self):
        """Imports inside nested functions should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
def outer():
    def inner():
        import foo
    return inner
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_import_in_class_body_is_detected(self):
        """Imports at class body level (not in methods) should be detected"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
class MyClass:
    import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, {Path("foo.py")})

    def test_import_in_staticmethod_is_ignored(self):
        """Imports inside static methods should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
class MyClass:
    @staticmethod
    def my_static():
        import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_import_in_classmethod_is_ignored(self):
        """Imports inside class methods should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
class MyClass:
    @classmethod
    def my_classmethod(cls):
        import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_import_in_property_is_ignored(self):
        """Imports inside property getters should be ignored"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
class MyClass:
    @property
    def my_prop(self):
        import foo
        return foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_typing_type_checking_attribute_form(self):
        """Imports inside typing.TYPE_CHECKING blocks should be ignored (using from import)"""
        self._create_file("foo.py", "")
        main = self._create_file(
            "main.py",
            """
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_relative_import_inside_function_is_ignored(self):
        """Relative imports inside functions should be ignored"""
        self._create_file("pkg/__init__.py", "")
        self._create_file("pkg/foo.py", "")
        main = self._create_file(
            "pkg/main.py",
            """
def my_func():
    from . import foo
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, set())

    def test_relative_import_top_level_is_detected(self):
        """Relative imports at top level should be detected"""
        self._create_file("pkg/__init__.py", "")
        self._create_file("pkg/foo.py", "")
        main = self._create_file(
            "pkg/main.py",
            """
from .foo import something
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertIn(Path("pkg/foo.py"), deps)

    def test_import_in_if_else_top_level_is_detected(self):
        """Imports inside if/else at top level should be detected"""
        self._create_file("foo.py", "")
        self._create_file("bar.py", "")
        main = self._create_file(
            "main.py",
            """
import sys

if sys.version_info >= (3, 10):
    import foo
else:
    import bar
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, {Path("foo.py"), Path("bar.py")})

    def test_import_in_try_except_top_level_is_detected(self):
        """Imports inside try/except at top level should be detected"""
        self._create_file("foo.py", "")
        self._create_file("bar.py", "")
        main = self._create_file(
            "main.py",
            """
try:
    import foo
except ImportError:
    import bar
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, {Path("foo.py"), Path("bar.py")})

    def test_package_init_is_detected(self):
        """Imports of packages (with __init__.py) should be detected"""
        self._create_file("mypkg/__init__.py", "")
        main = self._create_file(
            "main.py",
            """
import mypkg
""",
        )

        deps = find_deps(self.base_path, main, [])
        self.assertEqual(deps, {Path("mypkg/__init__.py")})

    def test_excluded_patterns(self):
        """Imports matching excluded patterns should be ignored"""
        self._create_file("foo.py", "")
        self._create_file("bar.py", "")
        main = self._create_file(
            "main.py",
            """
import foo
import bar
""",
        )

        deps = find_deps(self.base_path, main, ["foo"])
        self.assertEqual(deps, {Path("bar.py")})
