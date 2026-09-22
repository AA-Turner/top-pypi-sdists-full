import os
import sys

from importlib import import_module, invalidate_caches
try:
    # Python < 3.12
    from importlib_resources import files
except ImportError:
    from importlib.resources import files

from contextlib import ExitStack, contextmanager
from doctest import ELLIPSIS, REPORT_NDIFF, NORMALIZE_WHITESPACE
from pathlib import Path
from sybil import Sybil
from sybil.parsers.codeblock import PythonCodeBlockParser
from sybil.parsers.doctest import DocTestParser
from tempfile import TemporaryDirectory

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
        # Restore the cache in place instead of rebinding sys.modules to the copy.
        #
        # There are really two module caches.  The interpreter keeps its own, and
        # sys.modules is a name that starts out pointing at it.  Assigning to sys.modules
        # moves that name without moving the interpreter's cache, so from then on the two
        # disagree about what has been imported.
        #
        # That disagreement is what breaks the next test.  Anything imported during this
        # one is left behind in the interpreter's cache, so re-importing it later is
        # satisfied from there and never reaches sys.modules.  Code that reads sys.modules
        # directly, such as inspect.getmodule(), is then told the module was never
        # imported at all.
        for stale in set(sys.modules) - set(modules):
            del sys.modules[stale]
        sys.modules.update(modules)


def write_module(directory, name, source=''):
    # A dotted name creates the intermediate packages, so 'pkg.sub' gets you both a
    # pkg/__init__.py and a pkg/sub.py.
    package, _, tail = name.rpartition('.')
    parent = directory
    if package:
        parts = package.split('.')
        parent = directory.joinpath(*parts)
        parent.mkdir(parents=True, exist_ok=True)
        # mkdir() makes all the intermediate directories, but every level of the package
        # needs its own __init__.py, not just the deepest one.
        for depth in range(1, len(parts) + 1):
            directory.joinpath(*parts[:depth], '__init__.py').touch()
    (parent / f'{tail}.py').write_text(source, encoding='utf-8')
    # The path finder may have already cached this directory's contents.
    invalidate_caches()


class ExampleModule:
    def __init__(self, tmpdir):
        self.tmpdir = Path(tmpdir)
        self.path = self.tmpdir / 'example.py'

    def __call__(self, contents):
        # Call `example(contents)` to write to the example.py module.
        self.path.write_text(contents, encoding='utf-8')

    def module(self, name, contents=''):
        # There are tests which require importing from a second module in example.py.  This method
        # gives a convenient API for those tests that need to create a second module.
        write_module(Path(self.tmpdir), name, contents)


@pytest.fixture
def example():
    with ExitStack() as resources:
        tmpdir = resources.enter_context(TemporaryDirectory())
        resources.enter_context(sysmodules())
        resources.enter_context(syspath(tmpdir))
        yield ExampleModule(tmpdir)


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
        # A doctest runs in a namespace that doctest makes up, not in a real module.  Since
        # public() and private() read the globals of the frame that called them, that namespace
        # is what they operate on, and it only has to look enough like a module for them to work:
        # a __name__, so that anything defined in the doctest gets a sensible __module__, and an
        # __all__ to append to.
        #
        # This used to be much more elaborate.  A real ModuleType was created, registered in
        # sys.modules, and given an __all__ that was the same list object as the namespace's, all
        # so the two would stay in agreement.  None of that is needed now that both functions
        # resolve names against the calling frame rather than looking the module up in
        # sys.modules.  See https://github.com/simplistix/sybil/issues/21 for the original
        # problem.
        namespace['__name__'] = 'testmod'

        # Used in the doctests to provide a clean __all__.
        def reset():
            namespace['__all__'] = []

        reset()
        namespace['reset'] = reset
        namespace['import_example'] = import_example

        # The doctests for the single argument call form need something to import *from*, since the
        # whole point is that the name lands in the calling module and not in the module where the
        # object was defined.  Give them a temporary directory on sys.path to write throwaway
        # modules into.
        self._resources = ExitStack()
        tmpdir = self._resources.enter_context(TemporaryDirectory())
        self._resources.enter_context(syspath(tmpdir))
        self._made = []

        def make_module(name, source=''):
            write_module(Path(tmpdir), name, source)
            self._made.append(name.split('.')[0])

        namespace['make_module'] = make_module

    def teardown(self, namespace):
        # Remove the throwaway modules that make_module() created, so that a later
        # document, or a test in another file, doesn't import a stale one.  Importing
        # 'pkg.sub' caches both 'pkg' and 'pkg.sub', so a package's submodules have to go
        # along with the package itself.
        tops = set(self._made)
        prefixes = tuple(f'{top}.' for top in tops)
        # The names are gathered before anything is deleted, because a dictionary cannot
        # be mutated while it is being iterated over.
        stale = [
            name for name in sys.modules if name in tops or name.startswith(prefixes)
        ]
        for name in stale:
            del sys.modules[name]
        self._resources.close()


namespace = DoctestNamespace()


pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=DOCTEST_FLAGS),
        PythonCodeBlockParser(),
    ],
    pattern='*.rst',
    setup=namespace.setup,
    teardown=namespace.teardown,
).pytest()
