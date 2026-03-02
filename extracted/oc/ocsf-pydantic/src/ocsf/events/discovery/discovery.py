from enum import Enum

from ocsf.events.base import BaseEvent, CategoryId

from ocsf.objects.query_info import QueryInformation


class DiscoveryActivityId(Enum):
    Log: int = 1 # The discovered information is via a log.
    Collect: int = 2 # The discovered information is via a collection process.

class DiscoveryResultActivityId(Enum):
    Query: int = 1 # The discovered results are via a query request.


class Discovery(BaseEvent):
    """
    The Discovery event is a generic event that defines a set of attributes
    available in Discovery category events. As a generic event, it could be used to
    log events that are not otherwise defined by the Discovery specific event
    classes.
    """

    category_uid: CategoryId = CategoryId.Discovery

    # Optional:
    activity_id: DiscoveryActivityId | None = None


class DiscoveryResult(BaseEvent):
    """
    Discovery Result events report the results of a discovery request.
    """

    category_uid: CategoryId = CategoryId.Discovery

    query_result_id: DiscoveryResultActivityId

    # Recommended:
    query_info: QueryInformation | None = None # The search details associated with the query request.
    query_result: str | None = None

    # Optional:
    activity_id: DiscoveryResultActivityId | None = None
