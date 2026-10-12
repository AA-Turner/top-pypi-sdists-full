"""Test the Microsoft detector's handling of unusual message structures."""

from email import message_from_string
from email.mime.multipart import MIMEMultipart

from flufl.bounce import NoFailures, scan_message
from flufl.bounce._detectors.microsoft import Microsoft


_DECLARED_BUT_NO_PARTS = """\
Content-Type: multipart/mixed; boundary=BOUNDARY

--BOUNDARY--
"""


_NESTED_MULTIPART = """\
Content-Type: multipart/mixed; boundary=OUTER

--OUTER
Content-Type: multipart/alternative; boundary=INNER

--INNER
Content-Type: text/plain

transcript of session follows
anne@example.com
--INNER--
--OUTER--
"""


def test_declared_multipart_with_no_parts():
    # The parser finds no parts, so the payload is a string rather than a list.  This used to raise
    # TypeError out of get_payload(0) and abort the whole scan.
    msg = message_from_string(_DECLARED_BUT_NO_PARTS)
    assert not msg.is_multipart()
    assert Microsoft().process(msg) == NoFailures
    assert scan_message(msg) == frozenset()


def test_constructed_multipart_with_no_parts():
    # A message built in code can be a genuine multipart with an empty list of subparts.
    msg = MIMEMultipart('mixed')
    assert msg.get_payload() == []
    assert Microsoft().process(msg) == NoFailures


def test_nested_multipart_is_not_a_bounce():
    # Microsoft bounces have a plain first subpart; a multipart one doesn't match, even when it
    # contains text that otherwise would.
    msg = message_from_string(_NESTED_MULTIPART)
    assert msg.get_payload(0).is_multipart()
    assert Microsoft().process(msg) == NoFailures
