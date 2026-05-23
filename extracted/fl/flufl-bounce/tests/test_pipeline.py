"""Test the full pipeline."""

import pytest

from flufl.bounce import scan_message

from .utils import _parse


@pytest.mark.parametrize(
    'filename,expected_permanent',
    [
        ('microsoft_01.txt', {b'userx@example.COM'}),
        ('microsoft_04.txt', {b'userx@example.COM'}),
    ])
def test_scan(filename, expected_permanent):
    msg = _parse(filename)
    recipients = scan_message(msg)
    assert recipients == expected_permanent
