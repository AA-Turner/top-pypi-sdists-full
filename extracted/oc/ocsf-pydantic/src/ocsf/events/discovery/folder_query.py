from ocsf.objects.file import File

from ocsf.events.discovery import DiscoveryResult


class FolderQuery(DiscoveryResult):
    """
    Folder Query events report information about folders that are present on the
    system.
    """

    class_uid: int = 5008
    class_name: str = 'Folder Query'

    folder: File # The folder that is the target of the query.
