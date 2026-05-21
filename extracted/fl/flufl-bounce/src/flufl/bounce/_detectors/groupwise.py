"""This appears to be the format for Novell GroupWise and NTMail

X-Mailer: Novell GroupWise Internet Agent 5.5.3.1
X-Mailer: NTMail v4.30.0012
X-Mailer: Internet Mail Service (5.5.2653.19)
"""

import re

from email.message import Message
from io import BytesIO
from typing import cast

from public import public

from flufl.bounce.interfaces import NoFailures, NoTemporaryFailures, Recipients


acre = re.compile(b'<(?P<addr>[^>]*)>')


def find_textplain(msg: Message) -> Message | None:
    if msg.get_content_type() == 'text/plain':
        return msg
    if msg.is_multipart():
        for part in msg.get_payload():
            if not isinstance(part, Message):
                continue
            if ret := find_textplain(part):
                return ret
    return None


@public
class GroupWise:
    """Parse Novell GroupWise and NTMail bounces."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        if msg.get_content_type() != 'multipart/mixed' or not msg['x-mailer']:
            return NoFailures
        if msg['x-mailer'][:3].lower() not in ('nov', 'ntm', 'int'):
            return NoFailures
        addresses: set[bytes] = set()
        # Find the first text/plain part in the message.
        text_plain = find_textplain(msg)
        if text_plain is None:
            return NoFailures
        # text_plain is a text/plain leaf Message at runtime, so the decoded
        # payload is bytes; pyrefly sees the wider Message | bytes | Any union.
        body = BytesIO(cast(bytes, text_plain.get_payload(decode=True)))
        for line in body:
            if mo := acre.search(line):
                addresses.add(mo.group('addr'))
            elif b'@' in line:
                i = line.find(b' ')
                if i == 0:
                    continue
                if i < 0:
                    # TODO: `line` here still has its trailing newline (BytesIO
                    # preserves line terminators), so this fallback would add
                    # addresses with `\n`/`\r\n` attached.  No test exercises
                    # this path; revisit when a real-world sample surfaces.
                    addresses.add(line)
                else:
                    addresses.add(line[:i])
        return NoTemporaryFailures, frozenset(addresses)
