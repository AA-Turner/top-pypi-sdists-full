"""Test the Yale detector's handling of unusual messages."""

from email import message_from_string

from flufl.bounce import NoFailures
from flufl.bounce._detectors.yale import Yale


_BODY = """\

 --------Message not delivered to the following:

 userx    No matches to nameserver query
"""


def _bounce(from_header):
    headers = '' if from_header is None else f'From: {from_header}\n'
    return message_from_string(headers + _BODY)


def test_no_from_header():
    assert Yale().process(_bounce(None)) == NoFailures


def test_from_address_without_at():
    assert Yale().process(_bounce('mailer-daemon')) == NoFailures


def test_bare_edu_domain_is_not_yale():
    # Only yale.edu and its subdomains count.  The domain check used to stop at the shorter of the
    # domain and ('edu', 'yale'), so a one-part domain like this one slipped through.
    assert Yale().process(_bounce('MAILER-DAEMON@edu')) == NoFailures


def test_domain_is_case_insensitive():
    temporary, permanent = Yale().process(_bounce('MAILER-DAEMON@MR2.ITS.YALE.EDU'))
    assert temporary == frozenset()
    assert permanent == {b'userx@yale.edu', b'userx@cs.yale.edu'}


def test_no_end_marker():
    # Without an "Error Detail" line, the scan runs to the end of the body and still collects
    # every name it found.
    temporary, permanent = Yale().process(_bounce('MAILER-DAEMON@mr2.its.yale.edu'))
    assert temporary == frozenset()
    assert permanent == {b'userx@yale.edu', b'userx@cs.yale.edu'}
