"""Test the Caiwireless detector's handling of unexpected report bodies."""

from email import message_from_string

from flufl.bounce import NoFailures
from flufl.bounce._detectors.caiwireless import Caiwireless


_NO_ADDRESS_AFTER_TAG = """\
Content-Type: multipart/mixed; boundary=BOUNDARY

The following recipients did not receive this message:

Delivery failed for an unspecified reason.
<anne@example.com>
"""


def test_tag_not_followed_by_address():
    # Only the first non-blank line after the tag can name the recipient.  When it doesn't, the
    # detector gives up instead of picking up an address further down.
    msg = message_from_string(_NO_ADDRESS_AFTER_TAG)
    assert Caiwireless().process(msg) == NoFailures
