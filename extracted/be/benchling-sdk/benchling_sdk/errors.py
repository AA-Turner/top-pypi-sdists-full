"""Specialized Exception classes."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from json import JSONDecodeError
from typing import Any, Dict, Generic, Iterable, MutableMapping, Optional, Protocol, Type, TypeVar, Union

from benchling_api_client.v2.types import Response

from benchling_sdk.helpers.logging_helpers import default_logger
from benchling_sdk.helpers.serialization_helpers import unset_as_none
from benchling_sdk.models import (
    AsyncTask,
    AsyncTaskStatus,
    BadRequestError,
    BadRequestErrorBulk,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)

logger = default_logger()


@dataclass
class BenchlingError(Exception):
    """
    An error resulting from communicating with the Benchling API.

    This could be an error returned from the API intentionally (e.g., 400 Bad Request) or an
    unexpected transport error (e.g., 502 Bad Gateway)

    The json attribute is present if the API response provided a deserializable JSON body as part of the
    error description. It will be None if the response could not be parsed as JSON.

    The content attribute is any unparsed content returned as part of the response body.

    Instead of extending this class directly, prefer extending ExtendedBenchlingErrorBase.
    """

    status_code: int
    headers: MutableMapping[str, str]
    json: Optional[Dict[str, str]]
    content: Optional[bytes]
    parsed: Union[
        None,
        ForbiddenError,
        NotFoundError,
        BadRequestError,
        BadRequestErrorBulk,
        ConflictError,
    ]

    @classmethod
    def from_response(cls, response: Response) -> BenchlingError:
        """Create a BenchlingError from a generated Response."""
        json_body = _parse_error_body(response.content)
        return cls(
            status_code=response.status_code,
            headers=response.headers,
            json=json_body,
            content=response.content,
            parsed=response.parsed,
        )

    def __str__(self):
        message = self.json if self.json else self.content
        return f"{self.__class__.__name__}(status_code={self.status_code}, message={message})"

    def __hash__(self):
        return self._generate_hash()

    def __eq__(self, other):
        return self._generate_hash() == other._generate_hash()

    def _generate_hash(self):
        return hash(
            (
                self.status_code,
                json.dumps(self.headers, sort_keys=True),
                json.dumps(self.json, sort_keys=True),
                self.content,
                str(self.parsed),
            )
        )


@dataclass
class RegistrationError(Exception):
    """An error relating to Benchling registration."""

    message: Optional[str] = None
    errors: Optional[Dict[Any, Any]] = None
    task_status: Optional[AsyncTaskStatus] = None

    @classmethod
    def from_task(cls, task: AsyncTask) -> RegistrationError:
        """Create a RegistrationError from a failed AsyncTask."""
        task_errors = unset_as_none(lambda: task.errors)
        errors_dict: Dict[Any, Any] = task_errors.to_dict() if task_errors else dict()  # type: ignore
        return cls(
            message=unset_as_none(lambda: task.message), errors=errors_dict, task_status=task.status
        )

    def __str__(self):
        return repr(self)


@dataclass
class WaitForTaskExpiredError(Exception):
    """An error indicating an AsyncTask did not complete in the time allotted for polling."""

    message: str
    task: AsyncTask

    def __str__(self):
        return repr(self)


ExtendedError = TypeVar("ExtendedError", bound="ExtendedBenchlingErrorBase")


class ExtendedBenchlingErrorBase(ABC, BenchlingError):
    """
    Extended Benchling Error.

    Prefer using this class instead of extending BenchlingError directly.

    Forces subclasses to implement useful helpers.
    """

    @classmethod
    @abstractmethod
    def error_matcher(cls: Type[ExtendedError]) -> ResponseErrorMatcher[ExtendedError]:
        """Create an instance of ResponseErrorMatcher matching an exception extending BenchlingError."""
        pass


E = TypeVar("E", bound=BenchlingError)


class ResponseMatcher(Protocol):
    """Callable for checking if a Response matches specified conditions."""

    def __call__(self, response: Response) -> bool:
        """Return True if the provided response matches specified conditions."""
        pass


class ResponseErrorMatcher(Generic[E]):
    """
    Response Error Matcher.

    Raise a more specific Benchling Error if the HTTP response matches specific conditions.
    """

    _error_type: Type[E]
    _matcher: ResponseMatcher

    def __init__(self, error_type: Type[E], matcher: ResponseMatcher):
        """Init Response Error Matcher."""
        self._error_type = error_type
        self._matcher = matcher

    def raise_on_match(self, response: Response) -> None:
        """Raise error_type if the response matches some defined condition."""
        if self._matcher(response):
            raise self._error_type.from_response(response)


class AppSessionClosedError(ExtendedBenchlingErrorBase):
    """An error indicating a Benchling App session was already closed when attempting an API update."""

    _ERROR_TEXT: str = "Session has been closed and cannot be updated"

    @classmethod
    def error_matcher(cls) -> ResponseErrorMatcher[AppSessionClosedError]:
        """Create an instance of ResponseErrorMatcher matching AppSessionClosedError."""

        def _matcher(response: Response) -> bool:
            return _match_in_response_message(response, cls._ERROR_TEXT, status_code=400)

        return ResponseErrorMatcher(cls, _matcher)


@dataclass
class InvalidDataFrameError(Exception):
    """A general error related to Benchling DataFrames."""

    message: str

    def __str__(self):
        return repr(self)


@dataclass
class DataFrameInProgressError(Exception):
    """An error for Benchling data frames for unavailable data operations on a DataFrame in progress."""

    message: str

    def __str__(self):
        return repr(self)


def raise_for_status(
    response: Response, error_matchers: Optional[Iterable[ResponseErrorMatcher[E]]] = None
) -> Response:
    """
    Evaluate a Response for a successful HTTP status code or raise a BenchlingError.

    Custom error_matchers may be passed to raise more specific types of BenchlingError in a few specialized cases.

    If multiple matchers are specified, it's recommended that the caller provide an ordered Iterable
    such as List, with the more specific matchers first in the collection. Specifying a broader exception
    earlier in the collection, with a more narrow exception later, may cause the broader exception to be
    returned first.
    """
    logger.info("Status: %s", response.status_code)
    logger.debug(response)
    if response.status_code < 200 or response.status_code >= 300:
        # Check for specific error matches
        if error_matchers:
            for check_matcher in error_matchers:
                check_matcher.raise_on_match(response)
        # Raise a generalized error
        raise BenchlingError.from_response(response)
    return response


def _parse_error_body(content: bytes) -> Optional[Dict[str, str]]:
    if content:
        string_content = content.decode("utf-8")
        # In case the response is not a serialized JSON dict (e.g. a gateway error)
        try:
            return json.loads(string_content)
        except JSONDecodeError:
            # Some responses may not be JSON. Just catch the error
            return None
    return None


def _match_in_response_message(
    response: Response, match_string: str, status_code: Optional[int] = None
) -> bool:
    if status_code is not None and status_code != response.status_code:
        return False
    json_body = _parse_error_body(response.content)
    error_message = _error_message(json_body) if json_body is not None else None
    return error_message is not None and match_string in error_message


def _error_message(body: Dict[str, Any]) -> Optional[str]:
    error = body.get("error", {})
    # Needed for MyPy
    if isinstance(error, dict):
        return error.get("message")
    return None
