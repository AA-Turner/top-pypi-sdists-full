"""Yahoo! has its own weird format for bounces."""

import re

from contextlib import suppress
from email.iterators import body_line_iterator
from email.message import Message
from email.utils import parseaddr
from enum import Enum

from public import public

from flufl.bounce._interfaces import NoFailures, NoTemporaryFailures, Recipients


tcre = (
    re.compile(r'message\s+from\s+yahoo\.\S+', re.IGNORECASE),
    re.compile(
        r'Sorry, we were unable to deliver your message to '
        r'the following address(\(es\))?\.',
        re.IGNORECASE,
    ),
)
acre = re.compile(r'<(?P<addr>[^>]*)>:')
ecre = (
    re.compile(r'--- Original message follows'),
    re.compile(r'--- Below this line is a copy of the message'),
    re.compile(r'---------- Forwarded message ----------'),
)


class _ParseState(Enum):
    start = 0
    tag_seen = 1


@public
class Yahoo:
    """Yahoo! bounce detection."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        # Yahoo! bounces seem to have a known subject value and something called an x-uidl: header,
        # the value of which seems unimportant.
        sender = parseaddr(msg.get('from', '').lower())[1] or ''
        if not sender.startswith('mailer-daemon@yahoo'):
            return NoFailures
        addresses: set[bytes] = set()
        state = _ParseState.start
        for line in body_line_iterator(msg):
            line = line.strip()
            if state is _ParseState.start:
                if any(cre.match(line) for cre in tcre):
                    state = _ParseState.tag_seen
            elif mo := acre.match(line):
                # By now the email package has replaced any non-ASCII bytes in the address with
                # U+FFFD, so it can't be reported faithfully; skip it.  See GL#3.
                with suppress(UnicodeEncodeError):
                    addresses.add(mo.group('addr').encode('us-ascii'))
            elif any(cre.match(line) for cre in ecre):
                # We're at the end of the error response.
                break
        return NoTemporaryFailures, frozenset(addresses)
