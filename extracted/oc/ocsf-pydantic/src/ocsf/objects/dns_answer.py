
from enum import Enum
from ._dns import DNS

class DNSAnswerFlagIds(Enum):
    """
    The list of DNS answer header flag IDs.
    """
    Unknown: int = 0
    Authoritative_Answer: int = 1
    Truncated_Response: int = 2
    Recursion_Desired: int = 3
    Recursion_Available: int = 4
    Authentic_Data: int = 5
    Checking_Disabled: int = 6
    Other: int = 99 # The event DNS header flag is not mapped.

class DNSAnswer(DNS):
    """
    The DNS Answer object represents a specific response provided by the Domain Name
    System (DNS) when querying for information about a domain or performing a DNS
    operation. It encapsulates the relevant details and data returned by the DNS
    server in response to a query.
    """

    rdata: str

    # Recommended:
    class_: str | None = None # The class of DNS data contained in this resource record. See <a
                              # See RFC1035. For example: `IN`.
    flag_ids: DNSAnswerFlagIds | None = None # The list of DNS answer header flag IDs.
    ttl: int | None = None
    type: str | None = None # The type of data contained in this resource record
                            # For example: `CNAME`.

    # Optional:
    flags: list[str] | None = None # The list of DNS answer header flags.
