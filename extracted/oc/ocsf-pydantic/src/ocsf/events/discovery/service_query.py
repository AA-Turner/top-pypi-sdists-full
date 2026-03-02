from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.service import Service


class ServiceQuery(DiscoveryResult):
    """
    Service Query events report information about running services.
    """

    class_uid: int = 5016
    class_name: str = 'Service Query'

    service: Service
