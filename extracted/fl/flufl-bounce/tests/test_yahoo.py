"""Test the Yahoo detector's scan of the error response."""

from email import message_from_string

from flufl.bounce._detectors.yahoo import Yahoo


_PREAMBLE_NO_END_MARKER = """\
From: MAILER-DAEMON@yahoo.com
Content-Type: text/plain

Hello, this is the mail delivery program.
Sorry, we were unable to deliver your message to the following address.

<anne@example.com>:
Remote host said: 550 mailbox unavailable
"""


_ADDRESS_AFTER_END_MARKER = """\
From: MAILER-DAEMON@yahoo.com
Content-Type: text/plain

Sorry, we were unable to deliver your message to the following address.

<anne@example.com>:
Remote host said: 550 mailbox unavailable

--- Below this line is a copy of the message.

<bart@example.com>:
"""


def test_preamble_and_no_end_marker():
    # Lines before the tag are skipped, and without an end marker the scan runs to the end of the
    # body and still collects every address it found.
    msg = message_from_string(_PREAMBLE_NO_END_MARKER)
    temporary, permanent = Yahoo().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


def test_end_marker_stops_the_scan():
    # Anything after the end marker belongs to the quoted original message, so an address-like
    # line there isn't collected.
    msg = message_from_string(_ADDRESS_AFTER_END_MARKER)
    temporary, permanent = Yahoo().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}
