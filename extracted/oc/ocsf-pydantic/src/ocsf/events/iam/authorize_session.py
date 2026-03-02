
from enum import Enum

from ocsf.events.iam import IAM

from ocsf.objects.group import Group
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.session import Session
from ocsf.objects.user import User


class AuthorizeSessionActivityId(Enum):
    Assign_Privileges: int = 1 # Assign special privileges to a new logon.
    Assign_Groups: int = 2 # Assign special groups to a new logon.

class AuthorizeSession(IAM):
    """
    Authorize Session events report privileges or groups assigned to a new user
    session, usually at login time.
    """

    class_uid = 3003
    class_name = 'Authorize Session'

    user: User # The user to which new privileges were assigned.

    # Recommended:
    group: Group | None = None # Group that was assigned to the new user session.
    privileges: list[str] | None = None # The list of sensitive privileges, assigned to the new user
                                        # session.
    session: Session | None = None # The user session with the assigned privileges.

    # Optional:
    activity_id: AuthorizeSessionActivityId | None = None
    dst_endpoint: NetworkEndpoint | None = None # The Endpoint for which the user session was targeted.
