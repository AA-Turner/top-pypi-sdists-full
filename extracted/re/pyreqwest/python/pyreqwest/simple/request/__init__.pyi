from pyreqwest.http import Url
from pyreqwest.request import OneOffRequestBuilder

def pyreqwest_request(method: str, url: Url | str) -> OneOffRequestBuilder:
    """Create a simple request with the given HTTP method and URL.

    Returns a request builder, which will allow setting headers and the request body before sending.

    NOTE: This is only recommended for simple scripting use-cases. Usually, the client should be reused for multiple
    requests to benefit from connection pooling and other optimizations (via ClientBuilder).
    """

def pyreqwest_get(url: Url | str) -> OneOffRequestBuilder:
    """Same as `pyreqwest_request("GET", url)`."""

def pyreqwest_post(url: Url | str) -> OneOffRequestBuilder:
    """Same as `pyreqwest_request("POST", url)`."""

def pyreqwest_put(url: Url | str) -> OneOffRequestBuilder:
    """Same as `pyreqwest_request("PUT", url)`."""

def pyreqwest_patch(url: Url | str) -> OneOffRequestBuilder:
    """Same as `pyreqwest_request("PATCH", url)`."""

def pyreqwest_delete(url: Url | str) -> OneOffRequestBuilder:
    """Same as `pyreqwest_request("DELETE", url)`."""

def pyreqwest_head(url: Url | str) -> OneOffRequestBuilder:
    """Same as `pyreqwest_request("HEAD", url)`."""
