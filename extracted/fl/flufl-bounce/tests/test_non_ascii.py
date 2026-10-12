"""Test that a non-ASCII recipient address doesn't break detection.

Messages arrive as bytes, and by the time a detector sees a non-ASCII address the email package has
already replaced its non-ASCII bytes with U+FFFD.  Such an address can't be reported faithfully, so
detectors skip it instead of raising UnicodeEncodeError and aborting the whole scan.

See GL#3: https://gitlab.com/flufl/flufl.bounce/-/work_items/3
"""

from email import message_from_bytes

import pytest

from flufl.bounce import BounceDetector, NoFailures, scan_message
from flufl.bounce._detectors.caiwireless import Caiwireless
from flufl.bounce._detectors.dsn import DSN
from flufl.bounce._detectors.exchange import Exchange
from flufl.bounce._detectors.exim import Exim
from flufl.bounce._detectors.llnl import LLNL
from flufl.bounce._detectors.qmail import Qmail
from flufl.bounce._detectors.simplematch import SimpleMatch
from flufl.bounce._detectors.sina import Sina
from flufl.bounce._detectors.smtp32 import SMTP32
from flufl.bounce._detectors.yahoo import Yahoo


_DSN = """\
Content-Type: multipart/report; report-type=delivery-status; boundary=BOUNDARY

--BOUNDARY
Content-Type: text/plain

Delivery failed.
--BOUNDARY
Content-Type: message/delivery-status

Reporting-MTA: dns; mx.example.com

Action: failed
Final-Recipient: rfc822; jürgen@example.com

Action: failed
Final-Recipient: rfc822; anne@example.com
--BOUNDARY--
"""


_EXIM = """\
X-Failed-Recipients: jürgen@example.com, anne@example.com

Delivery failed.
"""


_EXCHANGE = """\
Content-Type: text/plain

Your message did not reach the following recipients:

    SMTP=jürgen@example.com; on Tue, 6 Oct 2026 10:00:00 -0400
    SMTP=anne@example.com; on Tue, 6 Oct 2026 10:00:00 -0400
"""


_LLNL = """\
Content-Type: text/plain

Recipients, jürgen@example.com, failed
Recipients, anne@example.com, failed
"""


_QMAIL = """\
Content-Type: text/plain

Hi. This is the qmail-send program at mx.example.com.

<jürgen@example.com>:
Sorry, no mailbox here by that name.

<anne@example.com>:
Sorry, no mailbox here by that name.

--- Below this line is a copy of the message.
"""


_SIMPLEMATCH = """\
Content-Type: text/plain

Here is your list of failed recipients:

<jürgen@example.com>
<anne@example.com>
"""


_SINA = """\
From: MAILER-DAEMON@sina.com
Content-Type: multipart/mixed; boundary=BOUNDARY

--BOUNDARY
Content-Type: text/plain

<jürgen@example.com>
<anne@example.com>
--BOUNDARY--
"""


_SMTP32 = """\
X-Mailer: <SMTP32 v8.15>
Content-Type: text/plain

User mailbox exceeds allowed size: jürgen@example.com
User mailbox exceeds allowed size: anne@example.com
"""


_YAHOO = """\
From: MAILER-DAEMON@yahoo.com
Content-Type: text/plain

Sorry, we were unable to deliver your message to the following address.

<jürgen@example.com>:
<anne@example.com>:
"""


# The only recipient in a Caiwireless bounce is the one on the line after the tag.
_CAIWIRELESS = """\
Content-Type: multipart/mixed; boundary=BOUNDARY

The following recipients did not receive this message:

<jürgen@example.com>
"""


_CASES: list[tuple[type[BounceDetector], str]] = [
    (DSN, _DSN),
    (Exim, _EXIM),
    (Exchange, _EXCHANGE),
    (LLNL, _LLNL),
    (Qmail, _QMAIL),
    (SimpleMatch, _SIMPLEMATCH),
    (Sina, _SINA),
    (SMTP32, _SMTP32),
    (Yahoo, _YAHOO),
]


@pytest.mark.parametrize(
    'detector, text', _CASES, ids=[detector.__name__ for detector, _ in _CASES]
)
def test_non_ascii_address_is_skipped(detector, text):
    # The non-ASCII address is dropped, and the ASCII one beside it is still reported.
    msg = message_from_bytes(text.encode('utf-8'))
    temporary, permanent = detector().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


def test_caiwireless_only_recipient_is_non_ascii():
    msg = message_from_bytes(_CAIWIRELESS.encode('utf-8'))
    assert Caiwireless().process(msg) == NoFailures


def test_gl3_dsn_no_longer_aborts_the_scan():
    # This is the shape of the bounce in GL#3: scan_message() used to raise UnicodeEncodeError.
    msg = message_from_bytes(_DSN.encode('utf-8'))
    assert scan_message(msg) == {b'anne@example.com'}
