from enum import Enum

from ocsf.events.iam import IAM

from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.user import User


class UserAccessManagementActivityId(Enum):
    Assign_Privileges: int = 1
    Revoke_Privileges: int = 2

class UserAccessManagement(IAM):
    """
    User Access Management events report management updates to a user's privileges.
    """

    class_uid = 3005
    class_name = 'User Access Management'

    privileges: list[str]  # List of privileges assigned to a user.
    user: User  # User to which privileges were assigned.

    # Recommended:
    resource: ResourceDetails | None = None # Resource that the privileges give access to.

    # Optional:
    activity_id: UserAccessManagementActivityId | None = None
