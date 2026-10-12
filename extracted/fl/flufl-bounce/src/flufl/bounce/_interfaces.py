"""Interfaces."""

from email.message import Message
from typing import Protocol, TypeAlias, runtime_checkable

from public import public


# Use `type` when our minimum Python version is 3.12.
Recipients: TypeAlias = frozenset[bytes]
public(Recipients=Recipients)


# Constants for improved readability in detector classes.  Use these like so:
#
# - to signal that no temporary or permanent failures were found:
#   `return NoFailures`
# - to signal that no temporary failures, but some permanent failures were
#   found:
#   `return NoTemporaryFailures, my_permanent_failures`
# - to signal that some temporary failures, but no permanent failures were
#   found:
#   `return my_temporary_failures, NoPermanentFailures`

NoTemporaryFailures: Recipients = frozenset()
NoPermanentFailures: Recipients = frozenset()
NoFailures: tuple[Recipients, Recipients] = (NoTemporaryFailures, NoPermanentFailures)

public(NoTemporaryFailures=NoTemporaryFailures)
public(NoPermanentFailures=NoPermanentFailures)
public(NoFailures=NoFailures)


@public
@runtime_checkable
class BounceDetector(Protocol):
    """Detect a bounce in an email message."""

    def process(self, msg: Message) -> tuple[Recipients, Recipients]:
        """Scan an email message looking for bounce addresses.

        :param msg: An email message.
        :type msg: `Message`
        :return: A 2-tuple of the detected temporary and permanent bouncing
            addresses.  Both elements of the tuple are frozensets of byte
            email addresses.  Not all detectors can tell the difference
            between temporary and permanent failures, in which case, the
            addresses will be considered to be permanently bouncing.
        """
