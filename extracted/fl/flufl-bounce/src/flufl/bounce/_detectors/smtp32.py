"""Something which claims to be SMTP32.

It identifies itself with X-Mailer: <SMTP32 vXXXXXX>

What the heck is this thing?  Here's a recent host:

% telnet 207.51.255.218 smtp
Trying 207.51.255.218...
Connected to 207.51.255.218.
Escape character is '^]'.
220 X1 NT-ESMTP Server 208.24.118.205 (IMail 6.00 45595-15)
"""

import re

from contextlib import suppress
from email.iterators import body_line_iterator
from email.message import Message

from public import public

from flufl.bounce._interfaces import NoFailures, NoTemporaryFailures, Recipients


ecre = re.compile('original message follows', re.IGNORECASE)
acre = re.compile(
    r"""
    (                                             # several different prefixes
    user\ mailbox[^:]*:                           # have been spotted in the
    |delivery\ failed[^:]*:                       # wild...
    |unknown\ user[^:]*:
    |undeliverable\ +to
    |delivery\ userid[^:]*:
    )
    \s*                                           # space separator
    (?P<addr>[^\s]+)                              # and finally, the address
    """,
    re.IGNORECASE | re.VERBOSE,
)


@public
class SMTP32:
    """Something which claims to be SMTP32.

    It identifies itself with X-Mailer: <SMTP32 vXXXXXX>
    """

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        mailer = msg.get('x-mailer', '')
        if not mailer.startswith('<SMTP32 v'):
            return NoFailures
        addresses: set[bytes] = set()
        for line in body_line_iterator(msg):
            if ecre.search(line):
                break
            if mo := acre.search(line):
                # By now the email package has replaced any non-ASCII bytes in the address with
                # U+FFFD, so it can't be reported faithfully; skip it.  See GL#3.
                with suppress(UnicodeEncodeError):
                    addresses.add(mo.group('addr').encode('us-ascii'))
        return NoTemporaryFailures, frozenset(addresses)
