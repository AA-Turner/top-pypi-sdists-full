
from pydantic import BaseModel, AnyUrl

class URL(BaseModel):
    """
    The Uniform Resource Locator(URL) object describes the characteristics of a URL.
    Defined in RFC 1738
    """

    # Recommended:
    category_ids: list[int] | None = None
    hostname: str | None = None # The URL host as extracted from the URL. For example:
                                # `www.example.com` from
                                # `www.example.com/download/trouble`.
    path: str | None = None # The URL path as extracted from the URL. For example:
                            # `/download/trouble` from
                            # `www.example.com/download/trouble`.
    port: int | None = None # The URL port. For example: `80`.
    query_string: str | None = None
    scheme: str | None = None
    url_string: AnyUrl | None = None # The URL string. See RFC 1738. For example:
                                     # `http://www.example.com/download/trouble.exe`. Note:
                                     # The URL path should not populate the URL string.

    # Optional:
    categories: list[str] | None = None
    resource_type: str | None = None # The context in which a resource was retrieved in a web request.
    subdomain: str | None = None
