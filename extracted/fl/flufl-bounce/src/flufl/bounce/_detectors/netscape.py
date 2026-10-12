"""Netscape Messaging Server bounce formats.

I've seen at least one NMS server version 3.6 (envy.gmp.usyd.edu.au) bounce
messages of this format.  Bounces come in DSN MIME format, but don't include
any -Recipient: headers.  Gotta just parse the text :(

NMS 4.1 (dfw-smtpin1.email.verio.net) seems even worse, but we'll try to
decipher the format here too.

"""

import re

from email.message import Message
from io import BytesIO
from typing import cast

from public import public

from flufl.bounce._interfaces import NoFailures, NoTemporaryFailures, Recipients


pcre = re.compile(b'This Message was undeliverable due to the following reason:', re.IGNORECASE)

acre = re.compile(b'(?P<reply>please reply to)?.*<(?P<addr>[^>]*)>', re.IGNORECASE)


@public
class Netscape:
    """Netscape Messaging Server bounce formats."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        # Sigh.  Some NMS 3.6's show
        #     multipart/report; report-type=delivery-status
        # and some show
        #     multipart/mixed;
        if not msg.is_multipart():
            return NoFailures
        # We're looking for a text/plain subpart occurring before a message/delivery-status subpart,
        # so the last leaf can never be it.
        plainmsg = None
        leaves = [p for p in msg.walk() if not p.is_multipart()]
        for subpart in leaves[:-1]:
            if subpart.get_content_type() == 'text/plain':
                plainmsg = subpart
                break
        # A text/plain leaf with no headers is falsy (len() counts headers), so test for None rather
        # than truth.
        if plainmsg is None:
            return NoFailures
        # Total guesswork, based on captured examples...
        #
        # plainmsg is the selected text/plain leaf, so the decoded payload is bytes at runtime;
        # pyrefly sees the wider Message | bytes | Any union.
        body = BytesIO(cast(bytes, plainmsg.get_payload(decode=True)))
        addresses: set[bytes] = set()
        for line in body:
            if mo := pcre.search(line):
                # We found a bounce section, but I have no idea what the official format inside here
                # is.  :( We'll just search for <addr> strings.
                for line in body:
                    if (mo := acre.search(line)) and not mo.group('reply'):
                        addresses.add(mo.group('addr'))
        return NoTemporaryFailures, frozenset(addresses)
