from ._resource import Resource
from .user import User
from .group import Group
from .agent import Agent

class ResourceDetails(Resource):
    """
    The Resource Details object describes details about resources that were affected
    by the activity/event.
    """

    # Recommended:
    owner: User | None = None # The identity of the service or user account that owns the resource.

    # Optional:
    agent_list: list[Agent] | None = None
    cloud_partition: str | None = None
    criticality: str | None = None # The criticality of the resource as defined by the event source.
    group: Group | None = None # The name of the related resource group.
    namespace: str | None = None # The namespace is useful when similar entities exist that you need to
                                 # keep separate.
    region: str | None = None # The cloud region of the resource.
    version: str | None = None # The version of the resource. For example `1.2.3`.
