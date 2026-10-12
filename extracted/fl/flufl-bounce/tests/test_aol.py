"""Test the AOL detector's handling of recipient lists."""

from email import message_from_string

from flufl.bounce._detectors.aol import AOL


def _bounce(body):
    return message_from_string(
        'From: Mail Delivery Subsystem <MAILER-DAEMON@aol.com>\n'
        'Content-Type: text/plain\n'
        '\n'
        'The mail you sent could not be delivered:\n'
        '\n'
        'mail to the following recipients could not be delivered\n' + body
    )


def test_full_address_kept_as_is():
    # A bare screen name gets @aol.com appended, but a line that already has an @ is a complete
    # address and is reported unchanged.
    temporary, permanent = AOL().process(_bounce('screenname\nanne@example.com\n'))
    assert temporary == frozenset()
    assert permanent == {b'screenname@aol.com', b'anne@example.com'}


def test_prose_line_ends_recipient_list():
    # A line with internal whitespace isn't a recipient, so it ends the list; nothing after it is
    # collected, even a line that looks like a screen name.
    body = 'screenname\n\nPlease check the address and try again.\notherscreenname\n'
    temporary, permanent = AOL().process(_bounce(body))
    assert temporary == frozenset()
    assert permanent == {b'screenname@aol.com'}
