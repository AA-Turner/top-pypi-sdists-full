import unittest
import os.path

here = os.path.dirname(os.path.abspath(__file__))


class ImportModuleTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from magicalimport import import_module

        return import_module(*args, **kwargs)

    def test_target_file_is_notfound(self):
        import random

        path = os.path.join(here, "missing{}.py".format(random.random()))
        with self.assertRaises(ModuleNotFoundError):
            self._callFUT(path)

    def test_target_module_is_notfound(self):
        import random

        path = os.path.join(here, "missing{}".format(random.random()))
        with self.assertRaises(ModuleNotFoundError):
            self._callFUT(path)


class ImportSymbolTests(unittest.TestCase):
    def _callFUT(self, *args, **kwargs):
        from magicalimport import import_symbol

        kwargs["silent"] = True
        return import_symbol(*args, **kwargs)

    def test_target_file_is_notfound(self):
        import random

        path = os.path.join(here, "missing{}.py:foo".format(random.random()))
        with self.assertRaises(ModuleNotFoundError):
            self._callFUT(path)

    def test_target_module_is_notfound(self):
        import random

        path = os.path.join(here, "missing{}:foo".format(random.random()))
        with self.assertRaises(ModuleNotFoundError):
            self._callFUT(path)

    def test_target_module_has_not_member(self):
        with self.assertRaises(ImportError) as c:
            self._callFUT("collections:foo")

    def test_target_file_has_not_member(self):
        import os.path

        path = os.path.join(here, "../../examples/a/b/c/foo.py")
        self.assertTrue(os.path.exists(path))

        with self.assertRaises(ImportError):
            self._callFUT("{}:foo".format(path))
