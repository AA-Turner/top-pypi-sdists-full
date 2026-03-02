from pydantic import BaseModel
from datetime import datetime

class HTTPCookie(BaseModel):
    """
    The HTTP Cookie object, also known as a web cookie or browser cookie, contains
    details and values pertaining to a small piece of data that a server sends to a
    user's web browser. This data is then stored by the browser and sent back to the
    server with subsequent requests, allowing the server to remember and track
    certain information about the user's browsing session or preferences.
    """

    name: str | None = None # The HTTP cookie name.
    value: str | None = None # The HTTP cookie value.

    # Optional:
    domain: str | None = None
    expiration_time: datetime | None = None # The expiration time of the HTTP cookie.
    http_only: bool | None = None
    is_http_only: bool | None = None
    is_secure: bool | None = None
    path: str | None = None # The path of the HTTP cookie.
    samesite: str | None = None
    secure: bool | None = None
