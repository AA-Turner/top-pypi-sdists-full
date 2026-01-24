import importlib.abc
import importlib.machinery
import sys
from types import ModuleType


class StringSourceLoader(importlib.abc.SourceLoader):
    MOD_NAME = "__string_mod"

    def __init__(self, data):
        self.data = data.encode()

    def get_data(self, path):
        return self.data

    def get_filename(self, fullname):
        return "<string>"

    def create_module(self, spec):
        return ModuleType(spec.name)

    def exec_module(self, module):
        code = self.source_to_code(self.data, self.get_filename(module.__name__))
        exec(code, module.__dict__)  # noqa: S102

    def get_spec(self):
        return importlib.machinery.ModuleSpec(self.MOD_NAME, self, origin=self.get_filename(self.MOD_NAME))

    def register_module(self):
        sys.modules[self.MOD_NAME] = importlib._bootstrap._load(self.get_spec())

    def import_module(self):
        return importlib.import_module(self.MOD_NAME)

    def load_module(self):
        self.register_module()
        return self.import_module()

    def cleanup(self):
        del sys.modules[self.MOD_NAME]
        if self.MOD_NAME in globals():
            del globals()[self.MOD_NAME]
