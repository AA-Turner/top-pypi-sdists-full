from __future__ import annotations

import datetime as dt
from typing import Literal, Mapping, get_args

from chalk.features._encoding.http import HttpResponse
from chalk.features.underscore import Underscore, UnderscoreFunction

_HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "TRACE", "CONNECT"]
_HTTP_METHOD_LIST = get_args(_HttpMethod)


class UnderscoreHttpRequest(UnderscoreFunction):
    def __init__(
        self,
        url: Underscore | str,
        method: _HttpMethod,
        headers: Underscore | Mapping[str, str] | None = None,
        body: Underscore | str | bytes | None = None,
        *,
        allow_redirects: bool = False,
        timeout: dt.timedelta | float | None = None,
    ):
        if isinstance(url, str) and not url.startswith(("http://", "https://")):
            raise ValueError(f"F.http_request(): URL must start with http:// or https://, got {url}")
        if not isinstance(url, (str, Underscore)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"F.http_request(): URL must be a string or Expression, got {type(url)}")
        if (
            not isinstance(body, (str, bytes, Underscore)) and body is not None
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"F.http_request(): body must be a string, bytes, Expression, or None: got {type(body)}")
        if method not in _HTTP_METHOD_LIST:
            raise ValueError(f"F.http_request(): Unknown HTTP method {method}, Supported: {_HTTP_METHOD_LIST}")
        if headers is not None and not isinstance(headers, (dict, Underscore)):
            raise TypeError(f"F.http_request(): headers must be a dict or Underscore, got {type(headers)}")
        if isinstance(timeout, dt.timedelta):
            timeout = timeout.total_seconds()
        super().__init__(
            "http_request",
            url,
            method,
            headers,
            body,
            allow_redirects,
            int(timeout * 1000) if timeout is not None else None,
        )


def http_request(
    url: Underscore | str,
    method: _HttpMethod,
    headers: Underscore | Mapping[str, str] | None = None,
    body: Underscore | str | bytes | None = None,
    *,
    allow_redirects: bool = True,
    timeout: dt.timedelta | float | None = None,
):
    """
    Make an HTTP request. The return type of this function is a `HttpResponse`, and features that are the result of
    this function should be annotated as such.

    HttpResponse is considered to be a struct, and you may use struct accessing syntax to access fields, HttpResponse
    consists of

    - status_code: int
    - headers: map<string, string>
    - body: bytes or string
    - final_url: string

    Parameters
    ----------
    url
        The URL to send the request to. Must start with http:// or https://.
    method
        The HTTP method to use. Must be one of GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, TRACE, CONNECT.
    headers
        The headers to include in the request, if any. Should take the form of a map of strings to strings.
        The Content-Length header is automatically added to the headers, unless you explicitly set it in the request
        headers.
    body
        The body of the request, if any. Should be a string or bytes.
    allow_redirects
        Whether to follow redirects. Defaults to True.
    timeout
        The timeout for the request, in seconds. If None or 0, no timeout will be set.
        Timeout's precision is limited to milliseconds.
        Defaults to None.

    Examples
    --------
    >>> from chalk import _
    >>> import chalk.functions as F
    >>> import datetime as dt
    >>> from chalk.functions.http import HttpResponse
    >>> @features
    ... class User:
    ...    id: str
    ...    json_data: str
    ...    resp: HttpResponse[str] = F.http_request(
    ...        "https://example.com",
    ...        "POST",
    ...        headers={"Content-Type": "application/json", "X-Client-Id": "abc123", "X-Client-Secret": "xyz789"},
    ...        body=_.json_data,
    ...        allow_redirects=True,
    ...        timeout=dt.timedelta(seconds=5),
    ...    )
    ...    status_code: int = _.resp.status_code
    ...    resp_body: str = _.resp.body
    """

    return UnderscoreHttpRequest(
        url=url,
        method=method,
        headers=headers,
        body=body,
        allow_redirects=allow_redirects,
        timeout=timeout,
    )


def http_get(
    url: Underscore | str,
    headers: Underscore | Mapping[str, str] | None = None,
    body: Underscore | str | bytes | None = None,
    *,
    allow_redirects: bool = True,
    timeout: dt.timedelta | float | None = None,
):
    """
    HTTP GET request. See `http_request` for more details.
    """
    return http_request(
        url=url,
        method="GET",
        headers=headers,
        body=body,
        allow_redirects=allow_redirects,
        timeout=timeout,
    )


def http_post(
    url: Underscore | str,
    headers: Underscore | Mapping[str, str] | None = None,
    body: Underscore | str | bytes | None = None,
    *,
    allow_redirects: bool = True,
    timeout: dt.timedelta | float | None = None,
):
    """
    HTTP POST request. See `http_request` for more details.
    """
    return http_request(
        url=url,
        method="POST",
        headers=headers,
        body=body,
        allow_redirects=allow_redirects,
        timeout=timeout,
    )


def http_put(
    url: Underscore | str,
    headers: Underscore | Mapping[str, str] | None = None,
    body: Underscore | str | bytes | None = None,
    *,
    allow_redirects: bool = True,
    timeout: dt.timedelta | float | None = None,
):
    """
    HTTP PUT request. See `http_request` for more details.
    """
    return http_request(
        url=url,
        method="PUT",
        headers=headers,
        body=body,
        allow_redirects=allow_redirects,
        timeout=timeout,
    )


def http_delete(
    url: Underscore | str,
    headers: Underscore | Mapping[str, str] | None = None,
    body: Underscore | str | bytes | None = None,
    *,
    allow_redirects: bool = True,
    timeout: dt.timedelta | float | None = None,
):
    """
    HTTP PUT request. See `http_request` for more details.
    """
    return http_request(
        url=url,
        method="DELETE",
        headers=headers,
        body=body,
        allow_redirects=allow_redirects,
        timeout=timeout,
    )


__all__ = [
    "HttpResponse",
    "UnderscoreHttpRequest",
    "http_request",
    "http_get",
    "http_post",
    "http_put",
    "http_delete",
]
