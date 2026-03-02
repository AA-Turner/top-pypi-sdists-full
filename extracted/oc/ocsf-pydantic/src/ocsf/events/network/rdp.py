from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.display import Display
from ocsf.objects.device import Device
from ocsf.objects.file import File
from ocsf.objects.response import ResponseElements
from ocsf.objects.request import RequestElements


class RDPActivityActivityId(Enum):
    Initial_Request: int = 1 # The initial RDP request.
    Initial_Response: int = 2 # The initial RDP response.
    Connect_Request: int = 3 # An RDP connection request.
    Connect_Response: int = 4 # An RDP connection response.
    Tls_Handshake: int = 5 # The TLS handshake.
    Traffic: int = 6 # Network traffic report.


class RDPActivity(Network):
    """
    Remote Desktop Protocol (RDP) Activity events report remote client connections
    to a server as seen on the network.
    """

    class_uid: int = 4005
    class_name: str = 'RDP Activity'

    # Recommended:
    certificate_chain: list[str] | None = None # The list of observed certificates in an RDP TLS
                                               # connection.
    protocol_ver: str | None = None # The Remote Desktop Protocol version.
    request: RequestElements | None = None # The client request in an RDP network connection.
    response: ResponseElements | None = None # The server response in an RDP network connection.

    # Optional:
    activity_id: RDPActivityActivityId | None = None
    capabilities: list[str] | None = None
    device: Device | None = None # The device instigating the RDP connection.
    file: File | None = None # The file that is the target of the RDP activity.
    identifier_cookie: str | None = None
    remote_display: Display | None = None
