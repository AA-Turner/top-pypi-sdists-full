from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.process import Process


class ProcessQuery(DiscoveryResult):
    """
    Process Query events report information about running processes.
    """

    class_uid: int = 5015
    class_name: str = 'Process Query'

    process: Process
