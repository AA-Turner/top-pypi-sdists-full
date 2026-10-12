"""LLNL's custom Sendmail bounce message."""

import re

from contextlib import suppress
from email.iterators import body_line_iterator
from email.message import Message

from public import public

from flufl.bounce._interfaces import NoFailures, NoTemporaryFailures, Recipients


acre = re.compile(r',\s*(?P<addr>\S+@[^,]+),', re.IGNORECASE)


@public
class LLNL:
    """LLNL's custom Sendmail bounce message."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        for line in body_line_iterator(msg):
            if mo := acre.search(line):
                # By now the email package has replaced any non-ASCII bytes in the address with
                # U+FFFD, so it can't be reported faithfully; skip it.  See GL#3.
                address = None
                with suppress(UnicodeEncodeError):
                    address = mo.group('addr').encode('us-ascii')
                if address is not None:
                    return NoTemporaryFailures, frozenset([address])
        return NoFailures
