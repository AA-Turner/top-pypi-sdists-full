import os
import sys

from importlib import import_module
try:
    # Python < 3.12
    from importlib_resources import files
except ImportError:
    from importlib.resources import files

from contextlib import ExitStack, contextmanager
from doctest import ELLIPSIS, REPORT_NDIFF, NORMALIZE_WHITESPACE
from sybil import Sybil
from sybil.parsers.codeblock import PythonCodeBlockParser
from sybil.parsers.doctest import DocTestParser
from tempfile import TemporaryDirectory
from types import ModuleType

import pytest

DOCTEST_FLAGS = ELLIPSIS | NORMALIZE_WHITESPACE | REPORT_NDIFF


@contextmanager
def syspath(directory):
    try:
        sys.path.insert(0, directory)
        yield
    finally:
        assert sys.path[0] == directory
        del sys.path[0]


@contextmanager
def sysmodules():
    modules = sys.modules.copy()
    try:
        yield
    finally:
        sys.modules = modules


class ExampleModule:
    def __init__(self, path):
        self.path = path

    def __call__(self, contents):
        with open(self.path, 'w', encoding='utf-8') as fp:
            fp.write(contents)


@pytest.fixture
def example():
    with ExitStack() as resources:
        tmpdir = resources.enter_context(TemporaryDirectory())
        resources.enter_context(sysmodules())
        resources.enter_context(syspath(tmpdir))
        path = os.path.join(tmpdir, 'example.py')
        yield ExampleModule(path)


def import_example(filename):
    # This assumes the file is relative to the docs/ directory.
    path = files() / 'docs' / filename
    with path.open(encoding='utf-8') as fp:
        contents = fp.read()

    with ExitStack() as resources:
        tmpdir = resources.enter_context(TemporaryDirectory())
        resources.enter_context(sysmodules())
        resources.enter_context(syspath(tmpdir))
        path = os.path.join(tmpdir, 'example.py')
        with open(path, 'w', encoding='utf-8') as fp:
            fp.write(contents)

        return import_module('example')


class DoctestNamespace:
    def setup(self, namespace):
        # The doctests in .rst files require that they mimic being executed in
        # a particular module.  The stdlib doctest functionality creates its
        # own globals namespace, unattached to any specific module object.
        # This causes coordination problems between the apparent globals that
        # the doctest sees, and public()'s implementation.
        #
        # We can't make them the same namespace because doing so violates
        # other assumptions in the public() function's code, but we can set
        # things up to be close enough for the doctest to pass.
        #
        # We use two techniques to make this work.  First, we create a test
        # module and ensure that its string name is assigned to the
        # namespace's __name__ attribute.  We also ensure that the module by
        # that name is in the sys.modules cache (and cleaned up in the
        # teardown).
        #
        # The second thing we need to do is to ensure that the module and the
        # namespace the doctest is executed in, share the same list object in
        # their __all__ attribute.  Now, generally public() will create
        # __all__ if it doesn't exist, but we can test that in the unittests,
        # so it's good enough to just initialize both name bindings to the
        # same list object here.
        #
        # There is some further discussion in this Sybil ticket:
        # https://github.com/cjw296/sybil/issues/21
        self._testmod = ModuleType('testmod')
        namespace['__name__'] = self._testmod.__name__
        sys.modules[self._testmod.__name__] = self._testmod

        # Used in the doctests to provide a clean __all__.
        def reset():
            self._testmod.__all__ = namespace['__all__'] = []

        reset()
        namespace['reset'] = reset
        namespace['import_example'] = import_example

    def teardown(self, namespace):
        del sys.modules[self._testmod.__name__]


namespace = DoctestNamespace()


pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=DOCTEST_FLAGS),
        PythonCodeBlockParser(),
    ],
    pattern='*.rst',
    setup=namespace.setup,
).pytest()
