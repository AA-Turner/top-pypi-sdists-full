from enum import Enum
from ocsf.events.network import Network


class NTPActivityActivityId(Enum):
    Unknown: int = 0 # Not used in standard NTP implementations.
    Symmetric_Active_Exchange: int = 1 # Bidirectional time exchange between devices.
    Symmetric_Passive_Response: int = 2 # Device responds as a server to peers in symmetric active mode.
    Client_Synchronization: int = 3 # NTP client, syncs with servers.
    Server_Response: int = 4 # Dedicated NTP time server, responds to clients.
    Broadcast: int = 5 # Broadcast time info to network devices.
    Control: int = 6 # Monitoring and control messaging.
    Private_Use_Case: int = 7 # Reserved - Not defined in standard NTP specifications.
    Other: int = 99 # The event activity is not mapped.


class NTPActivity(Network):
    """
    The Network Time Protocol (NTP) Activity events report instances of remote
    clients synchronizing their clocks with an NTP server, as observed on the
    network.
    """

    class_uid: int = 4013
    class_name: str = 'NTP Activity'

    version: str # The version number of the NTP protocol.

    # Recommended:
    delay: int | None = None
    dispersion: int | None = None
    precision: int | None = None # The NTP precision quantifies a clock's accuracy and stability in
                                 # log2 seconds, as defined in RFC-5905.
    stratum: str | None = None
    stratum_id: int | None = None

    # Optional:
    activity_id: NTPActivityActivityId | None = None
