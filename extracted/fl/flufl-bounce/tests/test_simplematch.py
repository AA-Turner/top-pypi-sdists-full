"""Test the SimpleMatch detector's handling of unusual recipient lines."""

from email import message_from_string

from flufl.bounce._detectors.simplematch import SimpleMatch


_NULL_ADDRESS = """\
Content-Type: text/plain

Here is your list of failed recipients:

<>
<anne@example.com>
"""


def test_empty_address_is_skipped():
    # <> is the null address, so the pattern matches with nothing to capture.  That line is
    # skipped, and the scan carries on to the real recipient after it.
    msg = message_from_string(_NULL_ADDRESS)
    temporary, permanent = SimpleMatch().process(msg)
    assert temporary == frozenset()
    assert permanent == {b'anne@example.com'}
