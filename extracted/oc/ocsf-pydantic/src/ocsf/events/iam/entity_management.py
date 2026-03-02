from enum import Enum

from ocsf.events.iam import IAM

from ocsf.objects.actor import Actor
from ocsf.objects.managed_entity import ManagedEntity


class EntityManagementActivityId(Enum):
    Create: int = 1
    Read: int = 2
    Update: int = 3
    Delete: int = 4

class EntityManagement(IAM):
    """
    Entity Management events report activity by a managed client, a micro service,
    or a user at a management console. The activity can be a create, read, update,
    and delete operation on a managed entity.
    """

    class_uid = 3004
    class_name = 'Entity Management'

    entity: ManagedEntity

    # Recommended:
    comment: str | None = None # The user provided comment about why the entity was changed.
    entity_result: ManagedEntity | None = None

    # Optional:
    activity_id: EntityManagementActivityId | None = None
    actor: Actor | None = None # Use for when the entity acting upon another entity is a process or
                               # user.
