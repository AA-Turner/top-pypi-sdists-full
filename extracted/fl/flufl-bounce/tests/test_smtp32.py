"""Test the SMTP32 detector's handling of unusual report bodies."""

from email import message_from_string

from flufl.bounce import NoFailures
from flufl.bounce._detectors.smtp32 import SMTP32


_NO_END_LINE = """\
X-Mailer: <SMTP32 v8.15>
Content-Type: text/plain

User mailbox exceeds allowed size: anne@example.com
"""


def test_no_end_line():
    # Without an "original message follows" line, the scan runs to the end of the body and still
    # collects every address it found.
    msg = message_from_string(_NO_END_LINE)
    temporary, permanent = SMTP32().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


_ADDRESS_ON_NEXT_LINE = """\
X-Mailer: <SMTP32 v8.15>
Content-Type: text/plain

Delivery failed:
anne@example.com
"""


def test_prefix_with_nothing_after_it():
    # The address pattern could match zero characters, so a prefix line with nothing after it
    # used to report an empty b'' address.  Now it reports nothing.
    msg = message_from_string(_ADDRESS_ON_NEXT_LINE)
    assert SMTP32().process(msg) == NoFailures
