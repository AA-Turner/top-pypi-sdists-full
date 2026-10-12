"""Test the DSN detector's handling of unusual delivery-status reports."""

from email import message_from_string
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from flufl.bounce import NoFailures
from flufl.bounce._detectors.dsn import DSN


_UNTYPED_FINAL_RECIPIENT = """\
Content-Type: multipart/report; report-type=delivery-status; boundary=BOUNDARY

--BOUNDARY
Content-Type: text/plain

Delivery failed.
--BOUNDARY
Content-Type: message/delivery-status

Reporting-MTA: dns; mx.example.com

Action: failed
Final-Recipient: anne@example.com
--BOUNDARY--
"""


def test_final_recipient_without_type_or_angle_brackets():
    # A recipient with neither an rfc822 type nor angle brackets can't be trusted to be an
    # address, so nothing is reported for it.
    msg = message_from_string(_UNTYPED_FINAL_RECIPIENT)
    assert DSN().process(msg) == NoFailures


def test_constructed_delivery_status_with_string_payload():
    # A message built in code can have a delivery-status part whose payload is a string rather
    # than a list of header blocks.  The detector skips that part instead of failing on it.
    msg = MIMEMultipart('report', report_type='delivery-status')
    status = MIMEBase('message', 'delivery-status')
    status.set_payload('Action: failed\nFinal-Recipient: rfc822; anne@example.com\n')
    msg.attach(status)
    assert not status.is_multipart()
    assert DSN().process(msg) == NoFailures
