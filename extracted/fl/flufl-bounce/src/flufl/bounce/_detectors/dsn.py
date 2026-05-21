"""Parse RFC 3464 (i.e. DSN) bounce formats.

RFC 3464 obsoletes 1894 which was the old DSN standard.  This module has not
been audited for differences between the two.
"""

from email.iterators import typed_subpart_iterator
from email.utils import parseaddr
from email.message import Message

from public import public

from flufl.bounce.interfaces import Recipients


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
            # yields Message subparts, i.e. Iterator[Message].  For now, we'll
            # just ignore the erroneous type errors.
            #
            # https://github.com/python/typeshed/issues/15809
            #
            # pyrefly: ignore[missing-attribute]
            if not part.is_multipart():
                # Huh?
                continue
            # Each message/delivery-status contains a list of Message objects
            # which are the header blocks.  Iterate over those too.
            #
            # pyrefly: ignore[missing-attribute]
            for msgblock in part.get_payload():
                address_set = None
                # We try to dig out the Original-Recipient (which is optional)
                # and Final-Recipient (which is mandatory, but may not exactly
                # match an address on our list).  Some MTA's also use
                # X-Actual-Recipient as a synonym for Original-Recipient, but
                # some apparently use that for other purposes :(
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
                    # MAS: This is a kludge, but
                    # SMTP-GATEWAY01.intra.home.dk has a final-recipient
                    # with an angle-addr and no address-type parameter at
                    # all. Non-compliant, but ...
                    for param in params:
                        if param.startswith('<') and param.endswith('>'):
                            address_set.append(param[1:-1])
        # There may be Nones in the current set of failures, so filter those
        # out of both sets.  Also, for Python 3 compatibility, the API
        # requires byte addresses.
        return (
            # First, the delayed, or temporary failures.
            frozenset(
                parseaddr(address)[1].encode('us-ascii')
                for address in delayed_addresses
                if address is not None
            ),
            # And now the failed or permanent failures.
            frozenset(
                parseaddr(address)[1].encode('us-ascii')
                for address in failed_addresses
                if address is not None
            ),
        )
