"""LLNL's custom Sendmail bounce message."""

import re

from email.iterators import body_line_iterator
from email.message import Message

from public import public

from flufl.bounce.interfaces import NoFailures, NoTemporaryFailures, Recipients


acre = re.compile(r',\s*(?P<addr>\S+@[^,]+),', re.IGNORECASE)


@public
class LLNL:
    """LLNL's custom Sendmail bounce message."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""

        for line in body_line_iterator(msg):
            if mo := acre.search(line):
                address = mo.group('addr').encode('us-ascii')
                return NoTemporaryFailures, frozenset([address])
        return NoFailures
