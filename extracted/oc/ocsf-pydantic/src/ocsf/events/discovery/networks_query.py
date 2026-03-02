
from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.network_interface import NetworkInterface

class NetworksQuery(DiscoveryResult):
    """
    Networks Query events report information about network adapters.
    """

    class_uid: int = 5013
    class_name: str = 'Networks Query'

    network_interfaces: list[NetworkInterface]
