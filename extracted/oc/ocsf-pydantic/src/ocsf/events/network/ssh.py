from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.file import File
from ocsf.objects.hassh import HASSH


class SSHActivityAuthTypeId(Enum):
    """
    The normalized identifier of the SSH authentication type.
    """
    Other: int = 99
    Unknown: int = 0
    Certificate_Based: int = 1 # Authentication using digital certificates.
    Gssapi: int = 2 # GSSAPI for centralized authentication.
    Host_Based: int = 3 # Authentication based on the client host's identity.
    Keyboard_Interactive: int = 4 # Multi-step, interactive authentication.
    Password: int = 5 # Password Authentication.
    Public_Key: int = 6 # Paired public key authentication.


class SSHActivity(Network):
    """
    SSH Activity events report remote client connections to a server using the
    Secure Shell (SSH) Protocol.
    """

    class_uid: int = 4007
    class_name: str = 'SSH Activity'

    # Recommended:
    auth_type: str | None = None # The SSH authentication type, normalized to the caption of
                                 # 'auth_type_id'. In the case of 'Other', it is defined by the event
                                 # source.
    auth_type_id: SSHActivityAuthTypeId | None = None # The normalized identifier of the SSH
                                                      # authentication type.
    client_hassh: HASSH | None = None
    protocol_ver: str | None = None # The Secure Shell Protocol version.
    server_hassh: HASSH | None = None

    # Optional:
    file: File | None = None # The file that is the target of the SSH activity.
