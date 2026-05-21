"""sina.com bounces"""

import re

from contextlib import suppress
from email.iterators import body_line_iterator
from email.message import Message

from public import public

from flufl.bounce.interfaces import NoFailures, NoTemporaryFailures, Recipients


acre = re.compile(r'<(?P<addr>[^>]*)>')


@public
class Sina:
    """sina.com bounces"""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        if msg.get('from', '').lower() != 'mailer-daemon@sina.com':
            return NoFailures
        if not msg.is_multipart():
            return NoFailures
        # The interesting bits are in the first text/plain multipart.
        part = None
        with suppress(IndexError):
            part = msg.get_payload(0)
        if not part:
            return NoFailures
        addresses: set[bytes] = set()
        # `part` is a Message subpart at runtime (msg was validated multipart
        # above), but Message.get_payload(int)'s typeshed signature returns a
        # wider union than reality.
        #
        # pyrefly: ignore[bad-argument-type]
        for line in body_line_iterator(part):
            if mo := acre.match(line):
                addresses.add(mo.group('addr').encode('us-ascii'))
        return NoTemporaryFailures, frozenset(addresses)
