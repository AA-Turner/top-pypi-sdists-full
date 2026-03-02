from ocsf.objects.file import File

from ocsf.events.discovery import DiscoveryResult


class FileQuery(DiscoveryResult):
    """
    File Query events report information about files that are present on the system.
    """

    class_uid: int = 5007
    class_name: str = 'File Query'

    file: File # The file that is the target of the query.
