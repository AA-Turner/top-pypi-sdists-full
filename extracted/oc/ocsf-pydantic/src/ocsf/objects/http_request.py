from enum import Enum
from pydantic import BaseModel

from pydantic.networks import IPvAnyAddress, AnyUrl

class HttpMethod(Enum):
    CONNECT = 'CONNECT'
    DELETE = 'DELETE'
    GET = 'GET'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    POST = 'POST'
    PUT = 'PUT'
    TRACE = 'TRACE'

class HTTPRequest(BaseModel):
    """
    The HTTP Request object represents the attributes of a request made to a web
    server. It encapsulates the details and metadata associated with an HTTP
    request, including the request method, headers, URL, query parameters, body
    content, and other relevant information.
    """

    # Recommended:
    http_headers: list[dict] | None = None
    http_method: HttpMethod | None = None # The HTTP request method indicates the desired
                                          # action to be performed for a given resource.
    url: AnyUrl | None = None # The URL object that pertains to the request.
    user_agent: str | None = None
    version: str | None = None # The Hypertext Transfer Protocol (HTTP) version.

    # Optional:
    args: str | None = None
    length: int | None = None # The HTTP request length, in number of bytes.
    referrer: str | None = None
    uid: str | None = None # The unique identifier of the http request.
    x_forwarded_for: list[IPvAnyAddress] | None = None
