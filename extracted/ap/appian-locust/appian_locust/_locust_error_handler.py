from locust.clients import ResponseContextManager
from requests.exceptions import HTTPError
from requests.models import Response


def _format_http_error(resp: Response, uri: str, username: str) -> str:
    """Taken from Response.raise_for_status. Formats the http error message,
     additionally adding the username

    Args:
        resp (Response): Response to generate an http error message from
        uri (str): URI accessed as part of the request
        username (str): Username of the calling user

    Returns:
        str: the http error message to use
    """
    http_error_msg = ''
    if isinstance(resp.reason, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = resp.reason.decode('utf-8')
        except UnicodeDecodeError:
            reason = resp.reason.decode('iso-8859-1')
    else:
        reason = resp.reason

    if 400 <= resp.status_code < 500:
        http_error_msg = u'%s Client Error: %s for uri: %s Username: %s' % (resp.status_code, reason, uri, username)

    elif 500 <= resp.status_code < 600:
        http_error_msg = u'%s Server Error: %s for uri: %s Username: %s' % (resp.status_code, reason, uri, username)

    return http_error_msg


def test_response_for_error(
    resp: ResponseContextManager,
    uri: str = 'No URI Specified',
    raise_error: bool = True,
    username: str = "",
    name: str = "",
) -> None:
    """
    Locust relies on errors to be logged to the global_stats attribute for error handling.
    This function is used to notify Locust that its instances are failing and that it should fail too.

    Args:
        resp (Response): a python response object from a client.get() or client.post() call in Locust tests.
        uri (Str): URI in the request that caused the above response.
        username (Str): identifies the current user when we use multiple different users for locust test)

    Returns:
        None

    Example (Returns a HTTP 500 error):

    .. code-block:: python

      username = 'admin'
      uri = 'https://httpbin.org/status/500'
      with self.client.get(uri) as resp:
        test_response_for_error(resp, uri, username)
    """
    if not resp or not resp.ok:
        http_error_msg = _format_http_error(resp, uri, username)
        error = HTTPError(http_error_msg)
        resp.failure(error)
        if raise_error:
            raise error
