import os
import sys

from sybil import Sybil
from doctest import ELLIPSIS, REPORT_NDIFF, NORMALIZE_WHITESPACE
from contextlib import ExitStack
from sybil.parsers.doctest import DocTestParser
from sybil.parsers.codeblock import PythonCodeBlockParser

# For the message catalog used in the doctests.
from tests.data import messages


DOCTEST_FLAGS = ELLIPSIS | NORMALIZE_WHITESPACE | REPORT_NDIFF


class DoctestNamespace:
    def __init__(self):
        self._resources = ExitStack()

    def setup(self, namespace):
        sys.modules['messages'] = messages
        namespace['cleanups'] = self._resources
        # Ensure that environment variables affecting translation are
        # neutralized.
        for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
            if envar in os.environ:
                del os.environ[envar]

    def teardown(self, namespace):
        del sys.modules['messages']
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
