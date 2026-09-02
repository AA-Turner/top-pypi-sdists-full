"""
This module defines errors and error handling functions for eumdac.
"""

import json
from typing import *
from urllib.parse import urlparse

import requests


def eumdac_raise_for_status(
    msg: str, response: requests.Response, exc_cls: Type[Exception]
) -> None:
    """Raises an EumdacError with the given message wrapping an HTTPError, if one occurred.

    Raises
    ------
    - `EumdacError`
        If the provided response raises an HTTPError
    """

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        url = urlparse(response.url)
        response_text = response.text
        if not response_text and response.raw:
            response_text = response.raw.data
        try:
            extra_info = json.loads(response_text)
        except json.decoder.JSONDecodeError:
            extra_info = {"text": response_text}
        extra_info.update({"url": url, "status": response.status_code})
        if response.status_code == 401:
            msg += " - Authentication error (401)"
        elif response.status_code == 403:
            msg += " - Unauthorised (403)"
        elif response.status_code == 404:
            msg += " - Not found (404)"
        if response.status_code > 500:
            msg += f" (due to a server-side error ({response.status_code})"
        exception = exc_cls(msg, extra_info)
        raise exception from exc


class EumdacError(Exception):
    """Common base class for eumdac errors

    Attributes
    ----------
    - `msg` : *str*
        exception text
    - `extra_info` : *Optional[Dict[str, Any]]*
        Dictionary containing additional information
        The title and description entries are embedded into the msg attribute, if present
    """

    def __init__(self, msg: str, extra_info: Optional[Dict[str, Any]] = None):
        """Init the error, putting common extra_info members into the message."""
        self.extra_info = extra_info
        if extra_info:
            if "title" in extra_info:
                msg = f"{msg} - {extra_info['title']}"
            if "description" in extra_info:
                msg = f"{msg}. {extra_info['description']}"
        super().__init__(msg)
