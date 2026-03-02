from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.module import Module
from ocsf.objects.process import Process


class ModuleQuery(DiscoveryResult):
    """
    Module Query events report information about loaded modules.
    """

    class_uid: int = 5011
    class_name: str = 'Module Query'

    module: Module
    process: Process # The process that loaded the module.
