from ._dns import DNS

class DNSQuery(DNS):
    """
    The DNS query object represents a specific request made to the Domain Name
    System (DNS) to retrieve information about a domain or perform a DNS operation.
    This object encapsulates the necessary attributes and methods to construct and
    send DNS queries, specify the query type (e.g., A, AAAA, MX)
    """

    hostname: str # The hostname or domain being queried. For example:
                  # `www.example.com`

    # Recommended:
    opcode_id: int | None = None

    # Optional:
    opcode: str | None = None
