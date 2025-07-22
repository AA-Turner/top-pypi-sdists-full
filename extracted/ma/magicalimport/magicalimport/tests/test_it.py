import unittest
import os.path

here = os.path.dirname(os.path.abspath(__file__))


class Tests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from magicalimport import import_from_physical_path

        return import_from_physical_path(*args, **kwargs)

    def test_impot_from_physical_path(self):
        path = os.path.join(here, "../../examples/a/b/c/foo.py")
        foo = self._callFUT(path, as_="foo2")
        self.assertEqual(foo.name, "foo")

        from foo2 import name

        self.assertEqual(name, "foo")

    def test_impot_from_physical_path__with_here_option(self):
        foo = self._callFUT("../../examples/a/b/c/foo.py", as_="foo3", here=here)
        self.assertEqual(foo.name, "foo")

        from foo2 import name

        self.assertEqual(name, "foo")

    def test_expose_all_members(self):
        from magicalimport import expose_all_members

        path = os.path.join(here, "../../examples/a/b/c/foo.py")
        foo = self._callFUT(path, as_="foo3")

        expose_all_members(foo)

        self.assertEqual(name, "foo")  # NOQA
        with self.assertRaises(NameError):
            self.assertEqual(_age, "*secret*")  # NOQA

    def test_expose_members(self):
        from magicalimport import expose_members

        path = os.path.join(here, "../../examples/a/b/c/foo.py")
        foo = self._callFUT(path, as_="foo4")

        expose_members(foo, ["_age"])

        self.assertEqual(_age, "*secret*")  # NOQA
