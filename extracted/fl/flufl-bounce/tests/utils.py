"""Common test utilities."""

from email import message_from_binary_file
from importlib.resources import files

DATA = files('tests.data')


def _parse(filename):
    with (DATA / filename).open('rb') as fp:
        return message_from_binary_file(fp)
