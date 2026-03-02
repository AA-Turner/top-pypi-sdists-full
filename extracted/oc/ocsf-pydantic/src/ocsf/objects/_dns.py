from pydantic import BaseModel

class DNS(BaseModel):
    """
    The Domain Name System (DNS) object represents the shared information associated
    with the DNS query and answer objects.
    """

    # Recommended:
    class_: str | None = None # The class of resource records being queried. See <a target='_blank'
                             # href='https://www.rfc-editor.org/rfc/rfc1035.txt'>RFC1035</a>. For
                             # example: `IN`.
    packet_uid: int | None = None # The DNS packet identifier assigned by the program that generated
                                  # the query. The identifier is copied to the response.
    type: str | None = None # The type of resource records being queried. See <a target='_blank'
                            # href='https://www.rfc-editor.org/rfc/rfc1035.txt'>RFC1035</a>. For
                            # example: A, AAAA, CNAME, MX, and NS.
