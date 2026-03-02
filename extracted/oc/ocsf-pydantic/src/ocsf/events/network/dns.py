from datetime import datetime
from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.dns_query import DNSQuery
from ocsf.objects.dns_answer import DNSAnswer
from ocsf.objects.network_connection_info import NetworkConnectionInformation
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.network_traffic import NetworkTraffic


class DNSActivityActivityId(Enum):
    Query: int = 1 # The DNS query request.
    Response: int = 2 # The DNS query response.
    Traffic: int = 6 # Bidirectional DNS request and response traffic.
class DNSActivityRcodeId(Enum):
    """
    The normalized identifier of the DNS server response code. See <a
    target='_blank'
    href='https://datatracker.ietf.org/doc/html/rfc6895'>RFC-6895</a>.
    """
    NoError: int = 0 # No Error.
    FormErr: int = 1 # Format Error.
    ServFail: int = 2 # Server Failure.
    NXDomain: int = 3 # Non-Existent Domain.
    NotImp: int = 4 # Not Implemented.
    Refused: int = 5 # Query Refused.
    YXDomain: int = 6 # Name Exists when it should not.
    YXRRset: int = 7 # RR Set Exists when it should not.
    NXRRset: int = 8 # RR Set that should exist does not.
    NotAuth: int = 9 # Not Authorized or Server Not Authoritative for zone.
    NotZone: int = 10 # Name not contained in zone.
    DSOTYPENI: int = 11 # DSO-TYPE Not Implemented.
    BADSIG_VERS: int = 16 # TSIG Signature Failure or Bad OPT Version.
    BADKEY: int = 17 # Key not recognized.
    BADTIME: int = 18 # Signature out of time window.
    BADMODE: int = 19 # Bad TKEY Mode.
    BADNAME: int = 20 # Duplicate key name.
    BADALG: int = 21 # Algorithm not supported.
    BADTRUNC: int = 22 # Bad Truncation.
    BADCOOKIE: int = 23 # Bad/missing Server Cookie.
    Unassigned: int = 24 # The codes deemed to be unassigned by the RFC (unassigned codes: 12-15, 24-3840, 4096-65534).
    Reserved: int = 25 # The codes deemed to be reserved by the RFC (codes: 3841-4095, 65535).
    Other: int = 99 # The dns response code is not defined by the RFC.


class DNSActivity(Network):
    """
    DNS Activity events report DNS queries and answers as seen on the network.
    """

    class_uid: int = 4003
    class_name: str = 'DNS Activity'

    # Recommended:
    answers: list[DNSAnswer] | None = None
    dst_endpoint: NetworkEndpoint | None = None
    query: DNSQuery | None = None
    query_time: datetime | None = None
    rcode: str | None = None # The DNS server response code, normalized to the caption of the rcode_id
                             # value. In the case of 'Other', it is defined by the event source.
    rcode_id: DNSActivityRcodeId | None = None # The normalized identifier of the DNS server response
                                               # code. See RFC-6895
    response_time: datetime | None = None

    # Optional:
    activity_id: DNSActivityActivityId | None = None
    connection_info: NetworkConnectionInformation | None = None
    traffic: NetworkTraffic | None = None
