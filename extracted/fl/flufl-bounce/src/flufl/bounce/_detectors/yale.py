"""Yale's mail server is pretty dumb.

Its reports include the end user's name, but not the full domain.  I think we
can usually guess it right anyway.  This is completely based on examination of
the corpse, and is subject to failure whenever Yale even slightly changes
their MTA. :(
"""

import re

from email.message import Message
from email.utils import getaddresses
from enum import Enum
from io import BytesIO
from typing import cast

from public import public

from flufl.bounce.interfaces import NoFailures, NoTemporaryFailures, Recipients


scre = re.compile(b'Message not delivered to the following', re.IGNORECASE)
ecre = re.compile(b'Error Detail', re.IGNORECASE)
acre = re.compile(b'\\s+(?P<addr>\\S+)\\s+')


class ParseState(Enum):
    start = 0
    intro_found = 1


@public
class Yale:
    """Parse Yale's bounces (or what used to be)."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        if msg.is_multipart():
            return NoFailures
        try:
            whofrom = getaddresses([msg.get('from', '')])[0][1]
            if not whofrom:
                return NoFailures
            username, domain = whofrom.split('@', 1)
        except (IndexError, ValueError):
            return NoFailures
        if username.lower() != 'mailer-daemon':
            return NoFailures
        parts = domain.split('.')
        parts.reverse()
        for part1, part2 in zip(parts, ('edu', 'yale'), strict=False):
            if part1 != part2:
                return NoFailures
        # Okay, we've established that the bounce came from the mailer-daemon
        # at yale.edu.  Let's look for a name, and then guess the relevant
        # domains.
        names: set[bytes] = set()
        # msg was validated non-multipart above, so the decoded payload is
        # bytes at runtime; pyrefly sees the wider Message | bytes | Any union.
        body = BytesIO(cast(bytes, msg.get_payload(decode=True)))
        state = ParseState.start
        for line in body:
            if state is ParseState.start and scre.search(line):
                state = ParseState.intro_found
            elif state is ParseState.intro_found and ecre.search(line):
                break
            elif state is ParseState.intro_found:
                if mo := acre.search(line):
                    names.add(mo.group('addr'))
        # Now we have a bunch of names, these are either @yale.edu or
        # @cs.yale.edu.  Add them both.
        addresses: set[bytes] = set()
        for name in names:
            addresses.add(name + b'@yale.edu')
            addresses.add(name + b'@cs.yale.edu')
        return NoTemporaryFailures, frozenset(addresses)
