
from ._entity import Entity


class Group(Entity):
    """
    The Group object represents a collection or association of entities, such as
    users, policies, or devices. It serves as a logical grouping mechanism to
    organize and manage entities with similar characteristics or permissions within
    a system or organization.
    """

    # Optional:
    desc: str | None = None # The group description.
    domain: str | None = None # The domain where the group is defined. For example: the LDAP or Active
                              # Directory domain.
    name: str | None = None # The group name.
    privileges: list[str] | None = None # The group privileges.
    type: str | None = None # The type of the group or account.
    uid: str | None = None # The unique identifier of the group. For example, for Windows events this
                           # is the security identifier (SID) of the group.
