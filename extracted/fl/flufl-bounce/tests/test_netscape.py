"""Test the Netscape detector's choice of the text/plain part."""

from email import message_from_string

from flufl.bounce import NoFailures
from flufl.bounce._detectors.netscape import Netscape


_HEADERLESS_FIRST_PART = """\
Content-Type: multipart/report; report-type=delivery-status; boundary=BOUNDARY

--BOUNDARY

This Message was undeliverable due to the following reason:

<anne@example.com>
--BOUNDARY
Content-Type: message/delivery-status

Action: failed
--BOUNDARY--
"""


_TEXT_PLAIN_ONLY_LAST = """\
Content-Type: multipart/mixed; boundary=BOUNDARY

--BOUNDARY
Content-Type: text/html

<p>Undeliverable</p>
--BOUNDARY
Content-Type: text/plain

This Message was undeliverable due to the following reason:

<anne@example.com>
--BOUNDARY--
"""


def test_headerless_first_part():
    # A subpart with no headers defaults to text/plain but has len() == 0, so it is falsy even
    # though it exists.  The detector used to test it for truth and silently skipped it.
    msg = message_from_string(_HEADERLESS_FIRST_PART)
    assert len(msg.get_payload(0)) == 0
    temporary, permanent = Netscape().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


def test_text_plain_only_as_last_part():
    # The text/plain part has to come before the delivery status, so a text/plain part in last
    # place doesn't count, and neither does any other kind of part before it.
    msg = message_from_string(_TEXT_PLAIN_ONLY_LAST)
    assert Netscape().process(msg) == NoFailures
