from ocsf.events.network import Network

from ocsf.objects.url import URL


class NetworkActivity(Network):
    """
    Network Activity events report network connection and traffic activity.
    """

    class_uid: int = 4001
    class_name: str = 'Network Activity'

    # Recommended:
    url: URL | None = None # The URL details relevant to the network traffic.
