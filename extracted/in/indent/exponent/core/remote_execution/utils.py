import json
import logging
import stat
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import (
    Any,
    NoReturn,
    TypeVar,
)

import websockets
import websockets.exceptions
from anyio import Path as AsyncPath
from bs4 import UnicodeDammit
from httpx import Response
from pydantic import BaseModel
from sentry_sdk.serializer import serialize
from sentry_sdk.utils import (
    event_from_exception,
    exc_info_from_error,
)

from exponent.core.remote_execution.cli_rpc_types import FileMetadata
from exponent.core.remote_execution.types import (
    CLIErrorLog,
    FilePath,
)
from exponent.utils.version import get_installed_version

logger = logging.getLogger(__name__)


TModel = TypeVar("TModel", bound=BaseModel)


async def deserialize_api_response(
    response: Response,
    data_model: type[TModel],
) -> TModel:
    if response.is_error:
        logging.error(response.text)
        try:
            error_message = response.json()["detail"]
        except Exception:
            error_message = response.text
        raise ValueError(f"{error_message} ({response.status_code})")

    response_json = response.json()
    return data_model.model_validate(response_json)


def assert_unreachable(x: NoReturn) -> NoReturn:
    assert False, f"Unhandled type: {type(x).__name__}"


### Truncation

DEFAULT_CHARACTER_LIMIT = 20_000
MAX_LINES = 10_000


def truncate_output(
    output: str, character_limit: int = DEFAULT_CHARACTER_LIMIT
) -> tuple[str, bool]:
    output_length = len(output)
    lines = output.split("\n")

    if output_length <= character_limit and len(lines) <= MAX_LINES:
        return output, False

    while output_length > character_limit:
        last_line = lines.pop()
        output_length -= len(last_line) + 1

    if not lines:
        output = output[:character_limit]
    else:
        lines = lines[:MAX_LINES]
        output = "\n".join(lines)

    return output, True


### Error Handling


def format_attachment_data(
    attachment_lines: list[str] | None = None,
) -> str | None:
    if not attachment_lines:
        return None
    log_attachment_str = "\n".join(attachment_lines)
    return log_attachment_str


def format_error_log(
    exc: Exception,
    chat_uuid: str | None = None,
    attachment_lines: list[str] | None = None,
) -> CLIErrorLog | None:
    exc_info = exc_info_from_error(exc)
    event, _ = event_from_exception(exc_info)
    attachment_data = format_attachment_data(attachment_lines)
    version = get_installed_version()

    try:
        event_data = json.dumps(serialize(event))
    except json.JSONDecodeError:
        return None

    return CLIErrorLog(
        event_data=event_data,
        attachment_data=attachment_data,
        version=version,
        chat_uuid=chat_uuid,
    )


### Websockets


ws_logger = logging.getLogger("WebsocketUtils")


def ws_retry(
    connection_name: str,
    max_retries: int = 5,
) -> Callable[[Callable[..., Awaitable[None]]], Callable[..., Awaitable[None]]]:
    connection_name = connection_name.capitalize()
    reconnect_msg = f"{connection_name} reconnecting."
    disconnect_msg = f"{connection_name} connection closed."
    max_disconnect_msg = (
        f"{connection_name} connection closed {max_retries} times, exiting."
    )

    def decorator(
        f: Callable[..., Awaitable[None]],
    ) -> Callable[..., Awaitable[None]]:
        @wraps(f)
        async def wrapped(*args: Any, **kwargs: Any) -> None:
            i = 0

            while True:
                try:
                    return await f(*args, **kwargs)
                except (websockets.exceptions.ConnectionClosed, TimeoutError) as e:
                    # Warn on disconnect
                    ws_logger.warning(disconnect_msg)

                    if i >= max_retries:
                        # We've reached the max number of retries,
                        # log an error and reraise
                        ws_logger.warning(max_disconnect_msg)
                        raise e

                    # Increment the retry count
                    i += 1
                    # Notify the user that we're reconnecting
                    ws_logger.warning(reconnect_msg)
                    continue

        return wrapped

    return decorator


async def safe_read_file(path: FilePath) -> str:
    path = AsyncPath(path)

    try:
        return await path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Potentially a wacky encoding or mixture of encodings,
        # attempt to correct it.
        fbytes = await path.read_bytes()
        # Handles mixed encodings with utf-8 and cp1252 (windows)
        fbytes = UnicodeDammit.detwingle(fbytes)

        decode_result = smart_decode(fbytes)

        if decode_result:
            # First item in tuple is the decoded str
            return decode_result[0]

        raise


async def safe_get_file_metadata(path: FilePath) -> FileMetadata | None:
    path = AsyncPath(path)
    try:
        stats = await path.stat()
    except Exception as e:
        logger.error(f"Error getting file metadata: {e!s}")
        return None

    return FileMetadata(
        modified_timestamp=stats.st_mtime,
        file_mode=stat.filemode(stats.st_mode),
    )


async def safe_write_file(path: FilePath, content: str) -> None:
    await AsyncPath(path).write_text(content, encoding="utf-8")


def smart_decode(b: bytes) -> tuple[str, str] | None:
    # This function attempts to decode by detecting the actual source
    # encoding, returning (decoded_str, detected_encoding) if successful.
    # We also attempt to fix cases of mixed encodings of cp1252 + utf-8
    # using the detwingle helper provided by bs4. This can happen on
    # windows, particularly when a user edits a utf-8 file by pasting in
    # the special windows smart quotes.
    b = UnicodeDammit.detwingle(b)

    encoding = UnicodeDammit(
        b, known_definite_encodings=["utf-8", "cp1252"]
    ).original_encoding

    if not encoding:
        return None

    return (b.decode(encoding=encoding), encoding)
