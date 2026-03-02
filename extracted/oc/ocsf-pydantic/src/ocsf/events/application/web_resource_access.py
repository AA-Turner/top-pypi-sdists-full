from enum import Enum

from ocsf.objects.http_request import HTTPRequest
from ocsf.objects.http_response import HTTPResponse

from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.tls import TLS
from ocsf.objects.network_endpoint import NetworkProxy
from ocsf.objects.web_resource import WebResource

from .application import Application

class WebResourceAccessActivityActivityId(Enum):
    Grant: int = 1
    Deny: int = 2
    Revoke: int = 3
    Error: int = 4

class WebResourceAccessActivity(Application):
    """
    Web Resource Access Activity events describe successful/failed attempts to
    access a web resource over HTTP.
    """

    class_uid: int = 6004
    class_name: str = 'Web Resource Access Activity'

    http_request: HTTPRequest # Details about the underlying HTTP request.
    web_resources: list[WebResource] # Details about the resource that is the target of
                                     # the activity.

    # Recommended:
    src_endpoint: NetworkEndpoint | None = None # Details about the source endpoint of the request.

    # Optional:
    activity_id: WebResourceAccessActivityActivityId | None = None
    http_response: HTTPResponse | None = None # Details about the HTTP response, if available.
    proxy: NetworkProxy | None = None # Details about the proxy service, if available.
    tls: TLS | None = None # The Transport Layer Security (TLS) attributes, if available.
