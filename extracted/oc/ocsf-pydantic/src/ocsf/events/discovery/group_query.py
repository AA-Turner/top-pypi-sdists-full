
from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.group import Group
from ocsf.objects.user import User

class AdminGroupQuery(DiscoveryResult):
    """
    Admin Group Query events report information about administrative groups.
    """

    class_uid: int = 5009
    class_name: str = 'Admin Group Query'

    group: Group # The administrative group.

    # Recommended:
    users: list[User] | None = None # The users that belong to the administrative group.
