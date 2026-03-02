from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.user import User


class UserQuery(DiscoveryResult):
    """
    User Query events report user data that have been discovered, queried, polled or
    searched. This event differs from User Inventory as it describes the result of a
    targeted search by filtering a subset of user attributes.
    """

    class_uid: int = 5018
    class_name: str = 'User Query'

    user: User
