from enum import Enum

from pydantic import BaseModel

from .session import Session


class IPVerId(Enum):
    """
    The Internet Protocol version identifier.
    """
    Unknown: int = 0
    IPv4: int = 4
    IPv6: int = 6
    Other: int = 99

class NetworkConnectionInformation(BaseModel):
    """
    The Network Connection Information object describes characteristics of a network
    connection. Defined by D3FEND <a target='_blank' href='https://d3fend.mitre.org/
    dao/artifact/d3f:NetworkSession/'>d3f:NetworkSession</a>.
    """

    direction_id: int

    # Recommended:
    boundary_id: int | None = None
    protocol_name: str | None = None
    protocol_num: int | None = None
    protocol_ver_id: IPVerId | None = None # The Internet Protocol version identifier.
    uid: str | None = None # The unique identifier of the connection.

    # Optional:
    boundary: str | None = None
    direction: str | None = None
    protocol_ver: str | None = None # The Internet Protocol version.
    session: Session | None = None
    tcp_flags: int | None = None
