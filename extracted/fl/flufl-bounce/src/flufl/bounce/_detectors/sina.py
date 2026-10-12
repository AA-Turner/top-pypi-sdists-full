"""sina.com bounces."""

import re

from contextlib import suppress
from email.iterators import body_line_iterator
from email.message import Message
from typing import cast

from public import public

from flufl.bounce._interfaces import NoFailures, NoTemporaryFailures, Recipients


acre = re.compile(r'<(?P<addr>[^>]*)>')


@public
class Sina:
    """sina.com bounces."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        if msg.get('from', '').lower() != 'mailer-daemon@sina.com':
            return NoFailures
        if not msg.is_multipart():
            return NoFailures
        # is_multipart() above guarantees a list of subparts at runtime, but pyrefly can't narrow
        # get_payload()'s Message | str | list | Any union.
        parts = cast(list[Message], msg.get_payload())
        if len(parts) == 0:
            # A multipart built with no subparts at all.
            return NoFailures
        # The interesting bits are in the first text/plain multipart.
        part = parts[0]
        addresses: set[bytes] = set()
        for line in body_line_iterator(part):
            if mo := acre.match(line):
                # By now the email package has replaced any non-ASCII bytes in the address with
                # U+FFFD, so it can't be reported faithfully; skip it.  See GL#3.
                with suppress(UnicodeEncodeError):
                    addresses.add(mo.group('addr').encode('us-ascii'))
        return NoTemporaryFailures, frozenset(addresses)
