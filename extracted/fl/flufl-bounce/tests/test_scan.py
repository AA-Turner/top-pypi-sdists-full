"""Test the detector pipeline in flufl.bounce._scan."""

import logging

from email import message_from_string

import pytest

from flufl.bounce import all_failures, scan_message


class ExplodingDetector:
    """A detector that fails on every message."""

    def process(self, msg):
        """See `BounceDetector`."""
        raise RuntimeError('boom')


@pytest.mark.parametrize('scanner', [scan_message, all_failures])
def test_detector_exception_is_logged_and_reraised(scanner, monkeypatch, caplog):
    # A detector that raises must not be silently skipped: both entry points log which detector
    # failed and then propagate the original exception to the caller.
    monkeypatch.setattr('flufl.bounce._scan._DETECTORS', [ExplodingDetector])
    msg = message_from_string('Subject: anything\n\nbody\n')

    with (
        caplog.at_level(logging.ERROR, logger='flufl.bounce'),
        pytest.raises(RuntimeError, match='boom'),
    ):
        scanner(msg)

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.ERROR
    assert 'ExplodingDetector' in record.getMessage()
    assert record.exc_info[0] is RuntimeError
