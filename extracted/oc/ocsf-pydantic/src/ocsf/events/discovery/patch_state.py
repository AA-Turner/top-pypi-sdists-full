from ocsf.events.discovery import Discovery

from ocsf.objects.device import Device
from ocsf.objects.kb_article import KBArticle


class OperatingSystemPatchState(Discovery):
    """
    Operating System Patch State reports the installation of an OS patch to a device
    and any associated knowledgebase articles.
    """

    class_uid: int = 5004
    class_name: str = 'Operating System Patch State'

    device: Device

    # Recommended:
    kb_article_list: list[KBArticle] | None = None
