from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.session import Session


class UserSessionQuery(DiscoveryResult):
    """
    User Session Query events report information about existing user sessions.
    """

    class_uid: int = 5017
    class_name: str = 'User Session Query'

    session: Session
