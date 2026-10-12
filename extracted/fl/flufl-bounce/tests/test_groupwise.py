"""Test the GroupWise detector's handling of unusual bounces."""

from email import message_from_string

from flufl.bounce import NoFailures
from flufl.bounce._detectors.groupwise import GroupWise


def _bounce(first_part_headers, body):
    return message_from_string(
        'X-Mailer: Novell GroupWise Internet Agent 5.5.3.1\n'
        'Content-Type: multipart/mixed; boundary=BOUNDARY\n'
        '\n'
        f'--BOUNDARY\n{first_part_headers}\n{body}'
        '--BOUNDARY\n'
        'Content-Type: message/rfc822\n'
        '\n'
        'Subject: the original message\n'
        '\n'
        'Hello.\n'
        '--BOUNDARY--\n'
    )


_TEXT_PLAIN = 'Content-Type: text/plain\n'


def _report(recipient_line):
    return f'did not reach the following recipient(s):\n\n{recipient_line}\n    Unknown user\n\n'


def test_headerless_first_part():
    # A subpart with no headers defaults to text/plain but has len() == 0, so it is falsy even
    # though it exists.  The detector used to test it for truth and silently skipped it.
    msg = _bounce('', _report('anne@example.com on Fri, 20 Jul 2001 11:08:59 -0700'))
    assert len(msg.get_payload(0)) == 0
    temporary, permanent = GroupWise().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


_NO_TEXT_PLAIN = """\
X-Mailer: Novell GroupWise Internet Agent 5.5.3.1
Content-Type: multipart/mixed; boundary=BOUNDARY

--BOUNDARY
Content-Type: text/html

<p>Undeliverable to anne@example.com</p>
--BOUNDARY--
"""


def test_no_text_plain_part():
    # The search descends into every subpart, including a quoted original message, so this
    # bounce has no text/plain part anywhere.
    msg = message_from_string(_NO_TEXT_PLAIN)
    assert GroupWise().process(msg) == NoFailures


def test_angle_bracket_address():
    msg = _bounce(_TEXT_PLAIN, _report('<anne@example.com>'))
    temporary, permanent = GroupWise().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


def test_address_alone_on_a_line():
    # The whole line is the address.  It used to be reported with its line ending still attached.
    msg = _bounce(_TEXT_PLAIN, _report('anne@example.com'))
    temporary, permanent = GroupWise().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}


def test_invalid_address_alone_on_a_line():
    # A whole-line candidate must look like an address, just as a first-word candidate must.
    msg = _bounce(_TEXT_PLAIN, _report('anne@'))
    assert GroupWise().process(msg) == NoFailures


def test_constructed_message_with_string_part():
    # A message built in code can have a plain string where a subpart should be.  The search for
    # the text/plain part skips it instead of failing on it.
    msg = _bounce(_TEXT_PLAIN, _report('anne@example.com'))
    msg.get_payload().insert(0, 'not a message')
    temporary, permanent = GroupWise().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}
