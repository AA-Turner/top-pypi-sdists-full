"""Recognizes a class of messages from AOL that report only Screen Name."""

import re

from email.message import Message
from email.utils import parseaddr
from typing import cast

from public import public

from flufl.bounce.interfaces import NoFailures, NoTemporaryFailures, Recipients


scre = re.compile(b'mail to the following recipients could not be delivered')


@public
class AOL:
    """Recognizes a class of messages from AOL that report only Screen Name."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        if msg.get_content_type() != 'text/plain':
            return NoFailures
        if not parseaddr(msg.get('from', ''))[1].lower().endswith('@aol.com'):
            return NoFailures
        addresses: set[bytes] = set()
        found = False
        # The content-type was validated as text/plain above, so the decoded
        # payload is bytes at runtime; pyrefly can't follow the precondition
        # through Message.get_payload()'s wider union return type.
        for line in cast(bytes, msg.get_payload(decode=True)).splitlines():
            if scre.search(line):
                found = True
                continue
            if found:
                local = line.strip()
                if local:
                    if re.search(b'\\s', local):
                        break
                    if b'@' in local:
                        addresses.add(local)
                    else:
                        addresses.add(local + b'@aol.com')
        return NoTemporaryFailures, frozenset(addresses)
