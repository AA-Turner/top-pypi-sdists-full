from enum import Enum

from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.http_request import HTTPRequest
from ocsf.objects.actor import Actor
from ocsf.objects.resource_details import ResourceDetails
from ocsf.objects.api import API

from ocsf.events.application import Application


class APIActivityId(Enum):
    Unknown: int = 0
    Create: int = 1
    Read: int = 2
    Update: int = 3
    Delete: int = 4
    Other: int = 99

class APIActivity(Application):
    """
    API events describe general CRUD (Create, Read, Update, Delete) API activities,
    e.g. (AWS Cloudtrail)
    """

    class_uid: int = 6003
    class_name: str = 'API Activity'

    api: API
    actor: Actor
    src_endpoint: NetworkEndpoint # Details about the source of the activity.

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None
    http_request: HTTPRequest | None = None # Details about the underlying http request.
    resources: list[ResourceDetails] | None = None # Details about resources that were affected by the
                                                   # activity/event.

    # Optional:
    activity_id: APIActivityId = APIActivityId.Unknown
