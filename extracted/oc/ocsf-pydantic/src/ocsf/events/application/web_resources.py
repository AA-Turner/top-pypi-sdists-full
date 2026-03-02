from enum import Enum

from ocsf.objects.tls import TLS
from ocsf.objects.http_request import HTTPRequest
from ocsf.objects.http_response import HTTPResponse
from ocsf.events.base import BaseEvent
from ocsf.objects.web_resource import WebResource
from ocsf.objects.network_endpoint import NetworkEndpoint



class WebResourcesActivityActivityId(Enum):
    Create: int = 1
    Read: int = 2
    Update: int = 3
    Delete: int = 4
    Search: int = 5
    Import: int = 6
    Export: int = 7
    Share: int = 8

class WebResourcesActivity(BaseEvent):
    """
    Web Resources Activity events describe actions executed on a set of Web
    Resources.
    """
    
    class_uid: int = 6001
    class_name: str = 'Web Resources Activity'

    web_resources: list[WebResource]

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None # Details about server providing the web resources.
    http_request: HTTPRequest | None = None # Details about the underlying HTTP request.
    src_endpoint: NetworkEndpoint | None = None # Details about the endpoint from which the request
                                                # originated.
    web_resources_result: list[WebResource] | None = None

    # Optional:
    activity_id: WebResourcesActivityActivityId | None = None
    http_response: HTTPResponse | None = None # Details about the HTTP response, if available.
    tls: TLS | None = None # The Transport Layer Security (TLS) attributes, if available.
