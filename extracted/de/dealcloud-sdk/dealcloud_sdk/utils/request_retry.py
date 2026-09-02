import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from json import dumps
from json.decoder import JSONDecodeError
from typing import Callable, Collection, Optional, Union

from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from requests_futures.sessions import FuturesSession
from urllib3.util.retry import Retry

from dealcloud_sdk.constants.request import (
    BACKOFF_FACTOR,
    MAX_RETRIES,
    STATUS_FORCE_LIST,
)


def create_retry_handler(
    status_force_list: Collection[int], max_retries: int = MAX_RETRIES
) -> Retry:
    """
    Create a retry handler with defaults
    Args:
        status_force_list(Collection[int]): list of status codes that will trigger a retry
        max_retries(int): the number of times the request will be retried before failure

    Returns:
        Retry: the retry handler
    """
    return Retry(
        total=max_retries,
        read=max_retries,
        connect=max_retries,
        backoff_factor=BACKOFF_FACTOR,
        respect_retry_after_header=True,
        status_forcelist=status_force_list,
    )


def request_with_retry(
    method: str,
    url: str,
    auth: Union[str, Callable],
    data: Optional[Union[list, dict, str]] = None,
    status_force_list: list[int] = STATUS_FORCE_LIST,
    auth_type: str = "Bearer",
    max_retries: int = MAX_RETRIES,
    content_type: str = "application/json",
) -> Response:
    """
    A wrapper around the requests/retry libraries to capture 400/429 errors.

    Parameters:
        method(str): GET, PUT, POST, PATCH, DELETE
        url(str): The request URL
        auth (str): The authentication bearer token
        data(dict): The request body
        status_force_list(list[int]): the list of status codes that will trigger a retry
        auth_type(str): authentication type, defaults to "Bearer"
        max_retries(int): the number of times the request will be retried before failure
        content_type(str): pass the content_type header, defaults to "application/json"

    Returns:
        (Response): The API Response
    """
    session = Session()
    retry = create_retry_handler(status_force_list, max_retries)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    if not isinstance(auth, str):
        auth = auth()

    headers = {
        "Authorization": f"{auth_type} {auth}",
        "Content-Type": content_type,
    }
    if data and content_type == "application/json":
        data = dumps(data)
    response = session.request(method, url, data=data, headers=headers)
    return response


def multi_threaded_request_with_retry(
    method: str,
    urls: Union[list[str], str],
    auth: Callable,
    data: Optional[Union[dict, str, list]] = None,
    status_force_list: list[int] = STATUS_FORCE_LIST,
    auth_type: str = "Bearer",
    content_type: str = "application/json",
    iterate_urls_over_data: bool = True,
    max_workers: int = 3,
) -> list:
    """
    A wrapper around the requests/retry libraries to capture 400/429 errors.

    Parameters:
        method(str): GET, PUT, POST, PATCH, DELETE
        urls(list[str]): The request URLs
        auth (str): The authentication bearer token
        data(dict): The request body
        status_force_list(list[int]): the list of status codes that will trigger a retry
        auth_type(str): authentication type, defaults to "Bearer"
        content_type(str): pass the content_type header, defaults to "application/json"
        iterate_urls_over_data(bool): to iterate over urls or payloads,
            true to send multiple urls, false to send multiple payloads.
        max_workers(int): the number of threads to use in the process

    Returns:
        (Response): The API Response
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        session = FuturesSession(executor=executor)
        retry = create_retry_handler(status_force_list)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)

        responses = []
        if data and content_type == "application/json":
            if iterate_urls_over_data:
                data = dumps(data)
            else:
                data = list([dumps(d) for d in data])
        if iterate_urls_over_data:
            futures = [
                session.request(
                    method,
                    url,
                    data=data,
                    headers={
                        "Authorization": f"{auth_type} {auth()}",
                        "Content-Type": content_type,
                    },
                )
                for url in urls
            ]
        else:
            if not data:
                raise KeyError("data must be defined when not iterating over urls")
            futures = [
                session.request(
                    method,
                    urls,
                    data=d,
                    headers={
                        "Authorization": f"{auth_type} {auth()}",
                        "Content-Type": content_type,
                    },
                )
                for d in data
            ]
        completed = 0
        for future in as_completed(futures):
            resp = future.result()
            if resp.status_code != 200:
                raise HTTPError(f"Request failed with {resp.status_code}: {resp.text}")

            try:
                resp_json = resp.json()
                responses.append(resp_json)
            except JSONDecodeError:
                raise JSONDecodeError("Could not decode response", f"{resp.text}", 0)
            completed += 1
            if iterate_urls_over_data:
                logging.debug(f"processed: {completed}/{len(urls)}")
            else:
                if not data:
                    raise KeyError('argument: "data" not defined.')

                logging.debug(f"processed: {completed}/{len(data)}")

    return responses
