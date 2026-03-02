from enum import Enum

from ocsf.events.iam import IAM

from ocsf.objects.group import Group
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.user import User


class GroupManagementActivityId(Enum):
    Assign_Privileges: int = 1 # Assign privileges to a group.
    Revoke_Privileges: int = 2 # Revoke privileges from a group.
    Add_User: int = 3 # Add user to a group.
    Remove_User: int = 4 # Remove user from a group.
    Delete: int = 5 # A group was deleted.
    Create: int = 6 # A group was created.

class GroupManagement(IAM):
    """
    Group Management events report management updates to a group, including updates
    to membership and permissions.
    """

    class_uid = 3006
    class_name = 'Group Management'

    group: Group # Group that was the target of the event.

    # Recommended:
    privileges: list[str] | None = None # A list of privileges assigned to the group.
    resource: ResourceDetails | None = None # Resource that the privileges give access to.
    user: User | None = None # A user that was added to or removed from the group.

    # Optional:
    activity_id: GroupManagementActivityId | None = None
