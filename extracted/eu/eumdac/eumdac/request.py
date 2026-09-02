"""This module contains the eumdac requests wrapper that includes automatic retries and management of throttling."""

import json
import random
import time
from datetime import datetime
from typing import Any, Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from eumdac.errors import EumdacError
from eumdac.logging import logger


class RequestError(EumdacError):
    """Error related to requests."""

    pass


class RetryAndLog(Retry):
    """Retry configuration that will log retry attempts.

    Extends urllib3.util.retry.Retry, decorating the 'increment' method.
    """

    def increment(  # type: ignore
        self,
        method: Any = None,
        url: Any = None,
        response: Any = None,
        error: Any = None,
        _pool: Any = None,
        _stacktrace: Any = None,
    ) -> Retry:
        """Decorated urllib3.util.retry.Retry::increment to include logging."""
        target_uri = ""
        if _pool:
            target_uri = f"{method} {_pool.scheme}://{_pool.host}:{_pool.port}{url}"
        elif error:
            target_uri = f"{error.conn.host}{url}"

        cause = ""
        if response and response.data:
            cause = f'server response {response.status} - "{response.data}" '
        if error:
            cause = f'{cause}error: "{error}"'

        logger.warning(f"Trying again for {target_uri} due to {cause}")
        return super().increment(method, url, response, error, _pool, _stacktrace)


def _get_adapter(max_retries: int, backoff_factor: float) -> HTTPAdapter:
    """Prepare an an HTTPAdapter that will retry failed requests up to 'max_retries' times.

    Only requests that return a 50X error code will be retried.

    Parameters
    ----------
    - `max_retries` : *int*
        Number of retries to perform.
    - `backoff_factor` : *float*
        Backoff factor to apply between attempts after the second try.

    Returns
    -------
    - `HTTPAdapter`
        Adapter prepared with the given 'max_retries' and 'backoff_factor'.
    """

    retry = RetryAndLog(
        total=max_retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "PATCH"],
        raise_on_status=False,
    )

    return HTTPAdapter(max_retries=retry)


def _should_retry(response: requests.Response, backoff: int = random.randint(1, 6) * 10) -> bool:
    """Decide whether the request should be retried considering the received response.

    Handles the throttling of requests done by the Data Store API.

    Parameters
    ---------
    - `response` : *requests.Response*
        Response received from the server.
    - `backoff` : *int, optional*
        Backoff, in seconds, to apply between attempts, defaults to a random value smaller than 1 minute.
    """
    if response.status_code == 429:
        rd = json.loads(response.text)
        # handle throttling
        message = rd["message"]["reason"]
        if "message" in rd and "retryAfter" in rd["message"]:
            # Traffic limits exceeded
            timestamp = int(rd["message"]["retryAfter"]) / 1000
            utc_endtime = datetime.utcfromtimestamp(timestamp)
            duration = utc_endtime - datetime.utcnow()
            if duration.total_seconds() > 0:
                logger.warning(f"{rd['message']}: operation will resume in {duration}")
                time.sleep(duration.total_seconds())
                return True
        elif "message" in rd and "reason" in rd["message"]:
            if rd["message"]["reason"] == "Maximum number of connections exceeded":
                # Maximum number of connections exceeded
                logger.warning(f"{message}: throttling for {backoff}s")
                time.sleep(backoff)
                return True
            elif rd["message"]["reason"] == "Maximum number of requests exceeded":
                # Maximum number of requests exceeded
                logger.warning(f"{message}: throttling for 1s")
                time.sleep(1)
                return True

    return False


def _request(
    method: str,
    url: str,
    max_retries: int = 3,
    backoff_factor: float = 0.3,
    **kwargs: Any,
) -> requests.Response:
    """Perform a request with the given `method`, `url` and parameters with automatic retries and throttling management.

    Parameters
    ----------
    - `method`: *{'get', 'post', 'patch', 'put', 'delete'}*
        HTTP request method to use in the request.
    - `url`: *str*
        URL to make the request to.
    - `max_retries`: *int, optional*
        Max number of retries to perform if the request fails, default: 3.
    - `backoff_factor`: *float, optional*
        Backoff factor to apply between attempts, default 0.3.
    - `**kwargs`: *dict, optional*
        Extra arguments to pass to the request, refer to the requests library documentation for a list of possible arguments.

    Returns
    -------
    - `requests.Response`:
        Response received from the server.
    """

    adapter = _get_adapter(max_retries, backoff_factor)
    session = requests.Session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = requests.Response()
    try:
        while True:
            if hasattr(session, method):
                logger.debug(_pretty_print(method, url, kwargs))
                response = getattr(session, method.lower())(url, **kwargs)
                if _should_retry(response):
                    continue
            else:
                raise RequestError(f"Operation not supported: {method}")
            break
    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"Received unexpected response: {e}")
    except requests.exceptions.RetryError as e:
        raise RequestError(
            f"Maximum retries ({max_retries}) reached for {method.capitalize()} {url}"
        )

    return response


def get(url: str, **kwargs: Any) -> requests.Response:
    """Perform a GET HTTP request to the given `url` with the given parameters.

    Retries and throttling will be managed in a transparent way when making the request.

    Arguments
    ---------
    - `url`: *str*
        URL to make the request to.
    - `**kwargs`: *dict, optional*
        Extra arguments to pass to the request, refer to the requests library documentation for a list of possible arguments.

    Returns
    -------
    - `request.Response`:
        Response received from the server.
    """

    return _request("get", url, **kwargs)


def post(url: str, **kwargs: Any) -> requests.Response:
    """Perform a POST HTTP request to the given `url` with the given parameters.

    Retries and throttling will be managed in a transparent way when making the request.

    Arguments
    ---------
    - `url`: *str*
        URL to make the request to.
    - `**kwargs`: *dict, optional*
        Extra arguments to pass to the request, refer to the requests library documentation for a list of possible arguments.

    Returns
    -------
    - `request.Response`:
        Response received from the server.
    """
    return _request("post", url, **kwargs)


def patch(url: str, **kwargs: Any) -> requests.Response:
    """Perform a PATCH HTTP request to the given `url` with the given parameters.

    Retries and throttling will be managed in a transparent way when making the request.

    Arguments
    ---------
    - `url`: *str*
        URL to make the request to.
    - `**kwargs`: *dict, optional*
        Extra arguments to pass to the request, refer to the requests library documentation for a list of possible arguments.

    Returns
    -------
    - `request.Response`:
        Response received from the server.
    """
    return _request("patch", url, **kwargs)


def put(url: str, **kwargs: Any) -> requests.Response:
    """Perform a PUT HTTP request to the given `url` with the given parameters.

    Retries and throttling will be managed in a transparent way when making the request.

    Arguments
    ---------
    - `url`: *str*
        URL to make the request to.
    - `**kwargs`: *dict, optional*
        Extra arguments to pass to the request, refer to the requests library documentation for a list of possible arguments.

    Returns
    -------
    - `request.Response`:
        Response received from the server.
    """
    return _request("put", url, **kwargs)


def delete(url: str, **kwargs: Any) -> requests.Response:
    """Perform a DELETE HTTP request to the given `url` with the given parameters.

    Retries and throttling will be managed in a transparent way when making the request.

    Arguments
    ---------
    - `url`: *str*
        URL to make the request to.
    - `**kwargs`: *dict, optional*
        Extra arguments to pass to the request, refer to the requests library documentation for a list of possible arguments.

    Returns
    -------
    - `request.Response`:
        Response received from the server.
    """

    return _request("delete", url, **kwargs)


def _pretty_print(method: str, url: str, kwargs: Dict[str, Any]) -> str:
    """Returns a readable str of the given request."""
    pargs = {}
    for key in kwargs.keys():
        if key == "headers":
            headers = {}
            for header in kwargs[key]:
                if header not in ["referer", "User-Agent"]:
                    headers[header] = kwargs[key][header]
            if len(headers) > 0:
                pargs[key] = headers
        elif key == "auth":
            if hasattr(kwargs[key], "token"):
                pargs[key] = f"Bearer {str(kwargs[key].token)}"  # type: ignore
            else:
                pargs[key] = f"{type(kwargs[key]).__name__}"  # type: ignore
        else:
            pargs[key] = kwargs[key]
    return f"Request: {method.upper()} {url}, payload: {pargs}"
