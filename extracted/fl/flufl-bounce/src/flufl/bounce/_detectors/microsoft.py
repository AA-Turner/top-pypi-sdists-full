"""Microsoft's `SMTPSVC' nears I kin tell."""

import re

from email.message import Message
from enum import Enum
from io import BytesIO
from typing import cast

from public import public

from flufl.bounce._detectors.simplematch import VALID
from flufl.bounce.interfaces import NoFailures, NoTemporaryFailures, Recipients


scre = re.compile(rb'transcript of session follows', re.IGNORECASE)


class ParseState(Enum):
    start = 0
    tag_seen = 1


@public
class Microsoft:
    """Microsoft's `SMTPSVC' nears I kin tell."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        if msg.get_content_type() != 'multipart/mixed':
            return NoFailures
        # Find the first subpart, which has no MIME type.  msg was validated
        # multipart/mixed above, so get_payload(0) returns a Message subpart
        # at runtime; pyrefly sees the wider Message | str | Any union.
        try:
            subpart = cast(Message, msg.get_payload(0))
        except IndexError:
            # The message *looked* like a multipart but wasn't.
            return NoFailures
        data = subpart.get_payload(decode=True)
        if isinstance(data, list):
            # The message is a multi-multipart, so not a matching bounce.
            return NoFailures
        # `subpart` is a Message and not multi-multipart (handled above), so
        # the decoded payload is bytes at runtime.
        body = BytesIO(cast(bytes, data))
        state = ParseState.start
        addresses: set[bytes] = set()
        for line in body:
            if state is ParseState.start:
                if scre.search(line):
                    state = ParseState.tag_seen
            elif state is ParseState.tag_seen and VALID.match(line.strip()):
                addresses.add(line.strip())
        return NoTemporaryFailures, frozenset(addresses)
