from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.http_cookie import HTTPCookie
from ocsf.objects.http_response import HTTPResponse
from ocsf.objects.http_request import HTTPRequest
from ocsf.objects.file import File


class HTTPActivityActivityId(Enum):
    CONNECT: int = 1
    DELETE: int = 2
    GET: int = 3
    HEAD: int = 4
    OPTIONS: int = 5
    POST: int = 6
    PUT: int = 7
    TRACE: int = 8


class HTTPActivity(Network):
    """
    HTTP Activity events report HTTP connection and traffic information.
    """

    class_uid: int = 4002
    class_name: str = 'HTTP Activity'

    http_request: HTTPRequest
    http_response: HTTPResponse

    # Recommended:
    http_cookies: list[HTTPCookie] | None = None
    http_status: int | None = None

    # Optional:
    activity_id: HTTPActivityActivityId | None = None
    file: File | None = None # The file that is the target of the HTTP activity.
