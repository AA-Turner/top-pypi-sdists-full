"""Cloud exceptions thrown"""
from __future__ import annotations

import functools
import logging
import re
from concurrent.futures import TimeoutError as FuturesTimeoutError
from enum import Enum, IntEnum
from http import HTTPStatus
from typing import Any, Dict, List, Optional

import requests
from websockets.exceptions import ConnectionClosedError, InvalidStatusCode

from mcli.utils.utils_logging import FAIL

logger = logging.getLogger(__name__)

DEFAULT_MESSAGE = 'Unknown Error'
ERROR_AUTH_KEY_MISSING = 'No API key or auth token was found. To create an API key, use `mcli set api-key`.'


class MCLIException(Exception):
    """Base custom exception that MCLI will raise

    All errors should inherit this base so that expected errors can be properly caught
    """


class InputDisabledError(MCLIException):
    """Error thrown when interactivity is requested but input has been disabled.
    """


class ValidationError(MCLIException):
    """Base class for interactive validation errors
    """


class MCLIConfigError(MCLIException):
    """Exception raised when local MCLI config cannot be loaded or is missing information
    """


class MCLIRunConfigValidationError(MCLIException):
    """Exception raised when RunConfig cannot be finalized
    """


class MCLIDeploymentConfigValidationError(MCLIException):
    """Exception raised when DeploymentConfig cannot be finalized
    """


class InferenceServerException(MCLIException):
    """Exception raised when inference deployment server requests fail
    """
    status: HTTPStatus
    message: str
    e: Exception
    description: Optional[str] = None

    def __init__(self, status: HTTPStatus, message: str = DEFAULT_MESSAGE, description: Optional[str] = None):
        super().__init__()
        self.status = status
        self.message = message
        self.description = description

    def __str__(self) -> str:
        error_message = f'Inference Deployment Server Error {self.status.value}: {self.message}'

        if self.description:
            error_message = f'{error_message}. {self.description}'

        return error_message

    @classmethod
    def from_server_error_response(cls, error: str, code: int) -> InferenceServerException:
        """Initializes a new exception based on error dict from a Infernece Server response
        """
        try:
            status = HTTPStatus(code)
        except ValueError:
            logger.debug(f'Unknown status code {code}. Setting to 500')
            status = HTTPStatus.INTERNAL_SERVER_ERROR

        message = error if error else DEFAULT_MESSAGE
        description = None
        if code == 503:
            description = (
                "Inference deployment could not be reached. It is likely "
                "either not yet ready or is currently failing. Check `mcli describe deployment "
                "<deployment>` and if the deployment is failing, try `mcli get deployment logs <deployment>` "
                "to see what\'s wrong")
        if code == 408:
            description = ("Request timed out. This could be due to generating a long output sequence. "
                           "Consider increasing the timeout in your predict request.")

        return InferenceServerException(status=status, message=message, description=description)

    @classmethod
    def from_bad_response(cls, response: requests.Response) -> InferenceServerException:
        return InferenceServerException(
            status=HTTPStatus(response.status_code),
            message=response.reason,
        )

    @classmethod
    def from_requests_error(cls, error: requests.exceptions.RequestException) -> InferenceServerException:
        """Initializes a new exception based on a requests RequestException
        """
        msg = 'Unable to connect'
        if error.args:
            con = error.args[0]
            try:
                # Try to get the destination we tried to connect to
                # if the app is fully not accessible
                source = f'http://{con.pool.host}{con.url}'
            except AttributeError:
                pass
            else:
                msg = f'{msg} to {source}'
        return InferenceServerException(status=HTTPStatus.SERVICE_UNAVAILABLE, message=msg)


class MAPIException(MCLIException):
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
        error_message = f'Error {self.status.value}: {self.message}'

        if self.description:
            error_message = f'{error_message}. {self.description}'

        return error_message

    @classmethod
    def from_mapi_error_response(cls, error: Dict[str, Any]) -> MAPIException:
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
    def from_bad_response(cls, response: requests.Response) -> MAPIException:
        return MAPIException(
            status=HTTPStatus(response.status_code),
            message=response.reason,
        )

    @classmethod
    def from_requests_error(cls, error: requests.exceptions.RequestException) -> MAPIException:
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


class MintException(MCLIException):
    """Exception raised when connection to MINT fails or is broken
    """

    message: str

    def __init__(self, message: str = DEFAULT_MESSAGE):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        error_message = f'Error: {self.message}'
        return error_message


class MintServerException(MintException):
    """Exception type for MINT server errors
    """


class MintRequestException(MintException):
    """Exception type for bad requests to MINT
    """


class MintConnectionException(MintException):
    """Exception type for bad connections to MINT
    """


class RunConfigException(MAPIException):
    """Thrown when a run could not be created due to an incomplete FinalRunConfig
    """
    MATCH_MESSAGE = 'Bad run request'
    FIELD_PATTERN = re.compile('([A-Za-z]+) is a required field')

    def __init__(self, status: HTTPStatus, message: str = DEFAULT_MESSAGE, description: Optional[str] = None):
        super().__init__(status, message, description)
        fields = re.findall(self.FIELD_PATTERN, self.message)

        # Translate fields to make sense to the user
        fields_string = ", ".join(RunConfigException.translate_fields(fields))
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


MAPI_DESERIALIZATION_ERROR = MAPIException(
    status=HTTPStatus.INTERNAL_SERVER_ERROR,
    message='Unknown issue deserializing data',
)


class MultiMAPIException(MAPIException):
    """Raises 1 or more MAPI Exceptions

    Graphql can technically return multiple errors in the response. This
    allows the user to see all of them at once rather than having to debug
    one by one
    """

    def __init__(self, errors: list[MAPIException]) -> None:
        self.errors = errors
        status = max(e.status for e in errors)
        super().__init__(status)

    def __str__(self) -> str:
        return "\n".join([str(x) for x in self.errors])


class MAPIErrorMessages(Enum):

    NOT_FOUND_CLUSTER = 'No clusters found. Please contact your organization administrator to set one up'


def cli_error_handler(command: Optional[str] = None):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)
            except InputDisabledError as e:
                help_msg = ''
                if command:
                    help_msg = ('\n\nRun a help command for more information on required arguments:'
                                f'\n\n[bold]{command} --help[/]')
                logger.error(f'{FAIL} {e}{help_msg}')
                return 1
            except MCLIException as e:
                logger.error(f'{FAIL} {e}')
                return 1
            except RuntimeError as e:
                # TODO: Create custom MCLIRuntimeError
                logger.error(f'{FAIL} {e}')
                return 1
            except (TimeoutError, FuturesTimeoutError) as e:
                logger.error(f'{FAIL} Request has timed out. Please check your internet '
                             'connection or extend the timeout using [bold]MCLI_TIMEOUT[/]')
                return 1

        return wrapper

    return decorator


class MintError(IntEnum):
    """Enum of known websocket errors from MINT
    """
    OK = 1000
    COMPLETED = 1001
    BAD_REQUEST = 1002


def handle_mint_errors(func):
    """Decorator to handle errors from the MINT API"""

    @functools.wraps(func)
    async def decorated(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ConnectionClosedError as e:
            mint_handle_connection_closed(e)
        except OSError as e:
            if "Errno 61" in str(e):  # https://bugs.python.org/issue29980
                e = MintConnectionException('Could not reach MosaicML platform')
            raise e
        except InvalidStatusCode as e:
            # This is _probably_ auth related
            raise MintException(f'Connection to run failed with code: {e.status_code}') from e

    return decorated


def mint_handle_connection_closed(e: ConnectionClosedError):
    """Convert connection closed errors to MintExceptions, if needed

    Args:
        e (ConnectionClosedError): A websocket connection closed error

    Raises:
        MintRequestException: Raised when the user submitted a bad request
        MintServerException: Raised when the server encountered an error
    """
    if e.code == MintError.OK:
        # 1000: ConnectionClosedOK
        # Connection closed normally
        pass
    elif e.code == MintError.COMPLETED:
        # 1000: Going away
        # Connection closed gracefully
        logger.info(f'Connection to run closed: {e.reason}')
    elif e.code == MintError.BAD_REQUEST:
        # 1002: Protocol error
        raise MintRequestException(f'Unable to connect to run. {e.reason}') from e
    else:
        raise MintServerException(f'Unexpected error connecting to run. {e.reason}\n'
                                  'Please try again later.') from e
