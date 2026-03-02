from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.kernel import KernelResource


class KernelObjectQuery(DiscoveryResult):
    """
    Kernel Object Query events report information about discovered kernel resources.
    """

    class_uid: int = 5006
    class_name: str = 'Kernel Object Query'

    kernel: KernelResource # The kernel object that pertains to the event.
