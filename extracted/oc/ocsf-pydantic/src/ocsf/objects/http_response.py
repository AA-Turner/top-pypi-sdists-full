
from pydantic import BaseModel

class HTTPResponse(BaseModel):
    """
    The HTTP Response object contains detailed information about the response sent
    from a web server to the requester. It encompasses attributes and metadata that
    describe the response status, headers, body content, and other relevant
    information.
    """

    code: int # The Hypertext Transfer Protocol (HTTP) status code returned from the web
              # server to the client. For example, 200.

    # Recommended:
    http_headers: list[dict] | None = None

    # Optional:
    content_type: str | None = None
    latency: int | None = None
    length: int | None = None
    message: str | None = None
    status: str | None = None # The response status. For example: A successful HTTP status of 'OK'
                              # which corresponds to a code of 200.
