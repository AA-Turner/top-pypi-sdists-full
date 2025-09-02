import contextlib
import logging
import sys

import pytest

from jaraco.net import importer


@contextlib.contextmanager
def logging_context(**kwargs):
    """
    Creating a logging context using logging.basicConfig.
    """
    orig_handlers = logging.root.handlers
    logging.root.handlers[:] = []
    try:
        logging.basicConfig(**kwargs)
        yield
    finally:
        logging.root.handlers[:] = orig_handlers


@pytest.mark.xfail(reason="Dropbox public folder taken away")
def test_importer():
    with logging_context(level=logging.DEBUG):
        importer.URLImporter.install()
        sys.path.append('http://dl.dropbox.com/u/54081/modules/')
        try:
            import tester  # type: ignore[import-not-found] # Online module

            assert tester.echo(True, x=3) == ((True,), dict(x=3))
        finally:
            importer.URLImporter.remove()
