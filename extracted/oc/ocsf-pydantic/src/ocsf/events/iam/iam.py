from ocsf.events.base import BaseEvent, CategoryId

from ocsf.objects.http_request import HTTPRequest
from ocsf.objects.network_endpoint import NetworkEndpoint

class IAM(BaseEvent):
    """
    The Identity & Access Management event is a generic event that defines a set of
    attributes available in the access control events. As a generic event, it could
    be used to log events that are not otherwise defined by the IAM category.
    """
    category_uid: CategoryId = CategoryId.Identity_Access_Management

    # Recommended:
    src_endpoint: NetworkEndpoint | None = None # Details about the source of the IAM activity.

    # Optional:
    http_request: HTTPRequest | None = None # Details about the underlying HTTP request.
