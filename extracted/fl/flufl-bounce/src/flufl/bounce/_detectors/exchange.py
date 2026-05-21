"""Recognizes (some) Microsoft Exchange formats."""

import re

from email.iterators import body_line_iterator
from email.message import Message

from public import public

from flufl.bounce.interfaces import NoFailures, NoTemporaryFailures, Recipients


scre = re.compile('did not reach the following recipient')
ecre = re.compile('MSEXCH:')
a1cre = re.compile('SMTP=(?P<addr>[^;]+); on ')
a2cre = re.compile('(?P<addr>[^ ]+) on ')


@public
class Exchange:
    """Recognizes (some) Microsoft Exchange formats."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        addresses: set[bytes] = set()
        it = body_line_iterator(msg)
        # Find the start line.
        for line in it:
            if scre.search(line):
                break
        else:
            return NoFailures
        # Search each line until we hit the end line.
        for line in it:
            if ecre.search(line):
                break
            if mo := a1cre.search(line) or a2cre.search(line):
                # For Python 3 compatibility, the API requires bytes
                addresses.add(mo.group('addr').encode('us-ascii'))
        return NoTemporaryFailures, frozenset(addresses)
