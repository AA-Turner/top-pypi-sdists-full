"""Test the Sina detector's handling of unusual message structures."""

from email import message_from_string
from email.mime.multipart import MIMEMultipart

from flufl.bounce import NoFailures
from flufl.bounce._detectors.sina import Sina


_NOT_MULTIPART = """\
From: MAILER-DAEMON@sina.com
Content-Type: text/plain

<anne@example.com>
"""


_HEADERLESS_FIRST_PART = """\
From: MAILER-DAEMON@sina.com
Content-Type: multipart/mixed; boundary=BOUNDARY

--BOUNDARY

<anne@example.com>
<bart@example.com>
--BOUNDARY--
"""


def test_not_multipart():
    msg = message_from_string(_NOT_MULTIPART)
    assert Sina().process(msg) == NoFailures


def test_constructed_multipart_with_no_parts():
    # A message built in code can be a genuine multipart with an empty list of subparts.
    msg = MIMEMultipart('mixed')
    msg['From'] = 'MAILER-DAEMON@sina.com'
    assert msg.get_payload() == []
    assert Sina().process(msg) == NoFailures


def test_headerless_first_part():
    # A subpart with no headers has len() == 0, so it is falsy even though it exists.  The detector
    # used to test it for truth and silently skipped bounces shaped like this.
    msg = message_from_string(_HEADERLESS_FIRST_PART)
    assert len(msg.get_payload(0)) == 0
    temporary, permanent = Sina().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com', b'bart@example.com'}
