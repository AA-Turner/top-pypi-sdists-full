"""
Errors for the DatabricksGenAI package.
"""
import logging
import re
from http import HTTPStatus
from typing import Any, Dict, List, Optional

import requests

DEFAULT_MESSAGE = 'Unknown Error'
ERROR_AUTH_KEY_MISSING = 'No API key or auth token was found. ' \
    'Please make sure you have your Databricks credentials set-up correctly.'

logger = logging.getLogger(__name__)


class DatabricksGenAIError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message: str = ''):
        self.message = message
        super().__init__(self.message)


class DatabricksModelTrainingRequestError(DatabricksGenAIError):
    """Exception raised for errors in the request.

    Attributes:
        message -- explanation of the error
    """


class DatabricksGenAIResponseError(DatabricksGenAIError):
    """Exception raised for errors in the response.

    Attributes:
        message -- explanation of the error
    """


class DatabricksGenAIConfigError(DatabricksGenAIError):
    """Exception raised for errors in the config.

    Attributes:
        message -- explanation of the error
    """


class MAPIException(DatabricksGenAIError):
    """Exceptions raised when a request to MAPI fails

    Args:
        status: The status code for the exception
        message: A brief description of the error
        description: An optional longer description of the error

    Details:
    MAPI responds to failures with the following status codes:
    - 400: The request was misconfigured or missing an argument. Double-check the API and try again
    - 401: User credentials were either missing or invalid. Be sure to set your API key before making a request
    - 403: User credentials were valid, but the requested action is not allowed
    - 404: Could not find the requested resource(s)
    - 409: Attempted to create an object with a name that already exists. Change the name and try again.
    - 500: Internal error in MAPI. Please report the issue
    - 503: MAPI or a subcomponent is currently offline. Please report the issue
    """
    status: HTTPStatus
    message: str
    description: Optional[str] = None

    def __init__(self, status: HTTPStatus, message: str = DEFAULT_MESSAGE, description: Optional[str] = None):
        super().__init__()
        self.status = status
        self.message = message
        self.description = description

    def __str__(self) -> str:
        error_message = f'Error {self.status}: {self.message}'

        if self.description:
            error_message = f'{error_message}. {self.description}'

        return error_message

    @classmethod
    def from_mapi_error_response(cls, error: Dict[str, Any]):
        """Initializes a new exception based on error dict from a MAPI response
        """
        extensions = error.get('extensions', {})
        code = extensions.get('code', HTTPStatus.INTERNAL_SERVER_ERROR)
        try:
            status = HTTPStatus(code)
        except ValueError:
            logger.debug(f'Unknown status code {code}. Setting to 500')
            status = HTTPStatus.INTERNAL_SERVER_ERROR

        message = error.get('message', DEFAULT_MESSAGE)

        # TODO: could potentially include extensions['stacktrace'] as description for 500s internally
        # From apollo docs, this could only be available in dev?

        # Optionally translate to a more specific error, if one matches
        if RunConfigException.match(message):
            return RunConfigException(status=status, message=message)

        return MAPIException(status=status, message=message)

    @classmethod
    def from_bad_response(cls, response: requests.Response):
        return MAPIException(
            status=HTTPStatus(response.status_code),
            message=response.reason,
        )

    @classmethod
    def from_requests_error(cls, error: requests.exceptions.RequestException):
        """Initializes a new exception based on a requests RequestException
        """
        msg = 'Unable to connect to MAPI'
        if error.args:
            con = error.args[0]
            try:
                # Try to get the destination we tried to connect to
                # if the app is fully not accessible
                source = f'http://{con.pool.host}:{con.pool.port}{con.url}'
            except AttributeError:
                pass
            else:
                msg = f'{msg} at {source}'
        return MAPIException(status=HTTPStatus.SERVICE_UNAVAILABLE, message=msg)


class MultiMAPIException(MAPIException):
    """Raises 1 or more MAPI Exceptions

    Graphql can technically return multiple errors in the response. This
    allows the user to see all of them at once rather than having to debug
    one by one
    """

    def __init__(self, errors: List[MAPIException]) -> None:
        self.errors = errors
        status = max(e.status for e in errors)
        super().__init__(status)

    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self.errors])


class RunConfigException(MAPIException):
    """Thrown when a run could not be created due to an incomplete FinalRunConfig
    """
    MATCH_MESSAGE = 'Bad run request'
    FIELD_PATTERN = re.compile('([A-Za-z]+) is a required field')

    def __init__(self, status: HTTPStatus, message: str = DEFAULT_MESSAGE, description: Optional[str] = None):
        super().__init__(status, message, description)
        fields = re.findall(self.FIELD_PATTERN, self.message)

        # Translate fields to make sense to the user
        fields_string = ', '.join(RunConfigException.translate_fields(fields))
        if fields:
            self.message = f'Run configuration is missing the following required values: {fields_string}'
        else:
            self.message = message

    @staticmethod
    def translate_fields(fields: List[str]) -> List[str]:
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli.models.run_config import FinalRunConfig

        # pylint: disable-next=protected-access
        return [FinalRunConfig._property_translations.get(f, f) for f in fields]

    @classmethod
    def match(cls, message: str) -> bool:
        """Returns True if the error message suggests a RunConfigException
        """
        return RunConfigException.MATCH_MESSAGE in message


class ValidationError(DatabricksGenAIError):
    """Base class for interactive validation errors
    """


MAPI_DESERIALIZATION_ERROR = MAPIException(
    status=HTTPStatus.INTERNAL_SERVER_ERROR,
    message='Unknown issue deserializing data',
)
