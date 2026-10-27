import json
import os
from datetime import datetime
from typing import Optional

from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_common import constants
from fivetran_connector_sdk_common.constants import ROOT_LOCATION, SDK_LOGGING_PREFIX


def config_root_dir() -> str:
    """The directory for the SDK's local state (the encryption key, the update check): `~/.fivetran/connector_sdk`."""
    return os.path.join(os.path.expanduser("~"), ROOT_LOCATION)


def _validate_table_name(table: str) -> None:
    if not isinstance(table, str):
        raise TypeError(f"Table name must be a string, got {type(table).__name__}")
    if not table.strip():
        raise ValueError("Table name must be a non-empty string")


def _validate_schema(schema: Optional[str]) -> None:
    """Validates the raw, optional `schema` a connector author passed in (the 'schema' key on a schema()
    entry, or the `schema` keyword argument on an op.* call). `None` means omitted and is always valid.
    """
    if schema is None:
        return
    if not isinstance(schema, str):
        raise TypeError(f"'schema' must be a string, got {type(schema).__name__}")
    if not schema.strip():
        raise ValueError("'schema' must be a non-empty string")


def _validate_message(message: str) -> None:
    if not isinstance(message, str):
        raise TypeError(f"Message must be a string, got {type(message).__name__}")
    if not message.strip():
        raise ValueError("Message must be a non-empty string")


def _validate_trace(trace) -> None:
    # trace is optional -- None means no trace was provided, which is valid.
    if trace is not None and not isinstance(trace, str):
        raise TypeError(f"Trace must be a string, got {type(trace).__name__}")


def print_library_log(message: str, level: Logging.Level = Logging.Level.INFO, dev_log: bool = False, log_icon: Logging.LogIcon = Logging.LogIcon.NONE, indent: bool = False):
    """Logs a library message with the specified logging level.
    Args:
        level (Logging.Level): The logging level.
        message (str): The message to log.
        dev_log (bool): Boolean value to check if it is dev log and shouldn't be visible to customer
        log_icon (Logging.LogIcon): The type of log icon to add.
        indent (bool): Whether to indent the message.
    """
    message = add_icon_to_log_message(message, log_icon)
    if indent:
        message = f"  {message}"
    if constants.DEBUGGING:
        # Debug mode: verbose format with timestamp
        if dev_log:
            return
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.") + f"{now.microsecond // 1000:03d}"
        log_origin = Logging.get_aligned_log_origin(SDK_LOGGING_PREFIX.strip())
        prefix = f"{current_time} {Logging.get_aligned_level_name(level)} {log_origin} "
        
        if "\n" in message:
            lines = message.split('\n')
            continuation_indent = Logging.get_display_width(prefix)
            message = f"\n{' ' * continuation_indent}".join(lines)
        
        print(Logging.colorize(f"{prefix}{message}", level))
    elif constants.EXECUTED_VIA_CLI:
        # Other CLI commands (deploy, init, etc.): concise format with icons and colors
        if dev_log:
            return
        print(Logging.colorize(message, level))
    else:
        message_origin = "library_dev" if dev_log else "library"
        escaped_message = json.dumps(SDK_LOGGING_PREFIX + message)
        log_message = f'{{"level":"{level.name}", "message": {escaped_message}, "message_origin": "{message_origin}"}}'
        print(log_message)


def add_icon_to_log_message(message: str, log_icon: Logging.LogIcon):
    """Adds an icon to the log message based on the specified log icon type.
    Args:
        message (str): The message to log.
        log_icon (Logging.LogIcon): The type of log icon to add.
    Returns:
        str: The log message with the added icon.
    """
    match log_icon:
        case Logging.LogIcon.INFO:
            return f"ℹ️ {message}"
        case Logging.LogIcon.SUCCESS:
            return f"✓ {message}"
        case Logging.LogIcon.FAILURE:
            return f"✗ {message}"
        case Logging.LogIcon.STEP:
            return f"› {message}"
        case Logging.LogIcon.LIGHTNING:
            return f"⚡ {message}"
        case _:
            return message
