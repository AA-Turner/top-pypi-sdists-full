"""Test the Exchange detector's handling of unusual report bodies."""

from email import message_from_string

from flufl.bounce._detectors.exchange import Exchange


_NO_END_LINE = """\
Content-Type: text/plain

Your message did not reach the following recipients:

    SMTP=anne@example.com; on Tue, 6 Oct 2026 10:00:00 -0400
"""


def test_no_end_line():
    # Without an MSEXCH: line, the scan runs to the end of the body and still collects every
    # address it found.
    msg = message_from_string(_NO_END_LINE)
    temporary, permanent = Exchange().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


_PROSE_AFTER_RECIPIENT = """\
Content-Type: text/plain

Your message did not reach the following recipients:

anne@example.com on Tue, 6 Oct 2026 10:00:00 -0400
Delivery was attempted on Monday and again on Tuesday.
"""


def test_prose_is_not_an_address():
    # The fallback pattern used to take any word followed by " on " as an address, so this
    # sentence reported "attempted".  Only a word containing an @ counts now.
    msg = message_from_string(_PROSE_AFTER_RECIPIENT)
    temporary, permanent = Exchange().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}
