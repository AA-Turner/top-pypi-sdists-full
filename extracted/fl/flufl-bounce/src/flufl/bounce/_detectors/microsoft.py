"""Microsoft's `SMTPSVC' nears I kin tell."""

import re

from email.message import Message
from enum import Enum
from io import BytesIO
from typing import cast

from public import public

from flufl.bounce._detectors.simplematch import VALID
from flufl.bounce._interfaces import NoFailures, NoTemporaryFailures, Recipients


scre = re.compile(rb'transcript of session follows', re.IGNORECASE)


class ParseState(Enum):
    start = 0
    tag_seen = 1


@public
class Microsoft:
    """Microsoft's `SMTPSVC' nears I kin tell."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        # A message can declare multipart/mixed without the parser finding any parts in it, in which
        # case its payload is a string and get_payload(0) would raise TypeError.  is_multipart()
        # checks what was actually parsed.
        if msg.get_content_type() != 'multipart/mixed' or not msg.is_multipart():
            return NoFailures
        # is_multipart() above guarantees a list of subparts at runtime, but pyrefly can't narrow
        # get_payload()'s Message | str | list | Any union.
        parts = cast(list[Message], msg.get_payload())
        if len(parts) == 0:
            # A multipart built with no subparts at all.
            return NoFailures
        # Find the first subpart, which has no MIME type.
        subpart = parts[0]
        if subpart.is_multipart():
            # The message is a multi-multipart, so not a matching bounce.
            return NoFailures
        # `subpart` is not a multipart (handled above), so the decoded payload is bytes at runtime;
        # pyrefly sees the wider union.
        body = BytesIO(cast(bytes, subpart.get_payload(decode=True)))
        state = ParseState.start
        addresses: set[bytes] = set()
        for line in body:
            if state is ParseState.start:
                if scre.search(line):
                    state = ParseState.tag_seen
            elif state is ParseState.tag_seen and VALID.match(line.strip()):
                addresses.add(line.strip())
        return NoTemporaryFailures, frozenset(addresses)
