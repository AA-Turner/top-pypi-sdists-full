"""Parse RFC 3464 (i.e. DSN) bounce formats.

RFC 3464 obsoletes 1894 which was the old DSN standard.  This module has not
been audited for differences between the two.
"""

from contextlib import suppress
from email.iterators import typed_subpart_iterator
from email.message import Message
from email.utils import parseaddr

from public import public

from flufl.bounce._interfaces import Recipients


def _encode_all(addresses: list[str]) -> Recipients:
    """Return the addresses as bytes, skipping any that aren't ASCII."""
    encoded: set[bytes] = set()
    for address in addresses:
        # By now the email package has replaced any non-ASCII bytes in the address with U+FFFD, so
        # it can't be reported faithfully; skip it.  See GL#3.
        with suppress(UnicodeEncodeError):
            encoded.add(parseaddr(address)[1].encode('us-ascii'))
    return frozenset(encoded)


@public
class DSN:
    """Parse RFC 3464 (i.e. DSN) bounce formats."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """See `BounceDetector`."""
        # Iterate over each message/delivery-status subpart.
        failed_addresses: list[str] = []
        delayed_addresses: list[str] = []
        for part in typed_subpart_iterator(msg, 'message', 'delivery-status'):
            # typeshed mis-types typed_subpart_iterator's return as Iterator[str]; it actually
            # yields Message subparts, i.e. Iterator[Message].  For now, we'll just ignore the
            # erroneous type errors.
            #
            # https://github.com/python/typeshed/issues/15809
            #
            # pyrefly: ignore[missing-attribute]
            if not part.is_multipart():
                # A delivery-status part built in code can carry a string payload instead of header
                # blocks.
                continue
            # Each message/delivery-status contains a list of Message objects which are the header
            # blocks.  Iterate over those too.
            #
            # pyrefly: ignore[missing-attribute]
            for msgblock in part.get_payload():
                address_set = None
                # We try to dig out the Original-Recipient (which is optional) and Final-Recipient
                # (which is mandatory, but may not exactly match an address on our list).  Some
                # MTA's also use X-Actual-Recipient as a synonym for Original-Recipient, but some
                # apparently use that for other purposes :(
                #
                # Also grok out Action so we can do something with that too.
                action = msgblock.get('action', '').lower()
                # Some MTAs have been observed that put comments on the action.
                if action.startswith('delayed'):
                    address_set = delayed_addresses
                # opensmtpd uses non-compliant Action: error
                elif action.startswith(('fail', 'error')):
                    address_set = failed_addresses
                else:
                    # Some non-permanent failure, so ignore this block.
                    continue
                params: list[str] = []
                foundp = False
                for header in ('original-recipient', 'final-recipient'):
                    for k, _v in msgblock.get_params([], header):
                        if k.lower() == 'rfc822':
                            foundp = True
                        else:
                            params.append(k)
                    if foundp:
                        # Note that params should already be unquoted.
                        address_set.extend(params)
                        break
                    # MAS: This is a kludge, but SMTP-GATEWAY01.intra.home.dk has a final-recipient
                    # with an angle-addr and no address-type parameter at all.  Non-compliant,
                    # but ...
                    for param in params:
                        if param.startswith('<') and param.endswith('>'):
                            address_set.append(param[1:-1])
        # The delayed addresses are temporary failures, and the failed ones are permanent.
        return _encode_all(delayed_addresses), _encode_all(failed_addresses)
