"""Exceptions for the foundation model api
"""
import logging
from http import HTTPStatus
from typing import Union

import httpx
import requests

logger = logging.getLogger(__name__)

DEFAULT_MESSAGE = 'Unknown Error'
DEFAULT_URL = None


class FoundationModelAPIException(Exception):
    """Exception raised when foundation model api requests fail

    Attributes:
        status (HTTPStatus): HTTP status code of the response
        message (str): Error message returned by the API
        url (str): URL of the API endpoint that was called
    """

    def __init__(self,
                 status: HTTPStatus = None,
                 message: str = DEFAULT_MESSAGE,
                 url: str = DEFAULT_URL,
                 response: Union[requests.Response, httpx.Response] = None):
        self.status = status
        self.message = message
        self.url = url
        if response is not None:
            try:
                self.status = HTTPStatus(
                    response.status_code) if response.status_code != HTTPStatus.OK else HTTPStatus.INTERNAL_SERVER_ERROR
            except ValueError:
                logger.debug(f'Unknown status code {response.status_code}. Setting to 500')
                self.status = HTTPStatus.INTERNAL_SERVER_ERROR
            error = response.content.decode().strip()
            self.message = error if error else self.message

    def __str__(self) -> str:
        error_string = (f'\ncode: {self.status.value}' if self.status else '') + (
            f'\nreason: {self.message}' if self.message else '') + (f'\nurl: {self.url}' if self.url else '')
        return error_string
