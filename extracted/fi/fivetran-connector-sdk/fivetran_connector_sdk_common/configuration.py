import sys

from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging


def _validate_configuration_value(key, value, exempt_keys: set, allow_null_value: bool):
    """Validates a single configuration value, exiting the process with an error if invalid.
    Args:
        key: The configuration key being validated.
        value: The value for that key. Exempt keys must have a string or list of strings value
            (None is not allowed, since they hold host details required for proxy routing).
            All other keys must have a string value, unless allow_null_value is True, in which
            case None is also accepted.
        exempt_keys (set): Keys whose values may be a string or a list of strings instead of a
            plain string. Used for the proxy host key, which may hold a list of endpoints.
        allow_null_value (bool): Whether a None value is acceptable for non-exempt keys. This is
            required for updating secrets for a connection via configuration when deploying, but
            is not accepted when just running/debugging a connector locally.
    """
    if key in exempt_keys:
        if not isinstance(value, (str, list)):
            print_library_log(
                f"invalid configuration file; value for '{key}' must be a string or a list of strings\nreference: https://fivetran.com/docs/connector-sdk/connector-development-and-configuration/configuration-json#workingwithconfigurationjson", Logging.Level.SEVERE)
            sys.exit(1)
    elif value is None and allow_null_value:
        return
    elif not isinstance(value, str):
        expected = "strings or null" if allow_null_value else "strings"
        print_library_log(
            f"invalid configuration file; all values must be {expected}\nreference: https://fivetran.com/docs/connector-sdk/connector-development-and-configuration/configuration-json#workingwithconfigurationjson", Logging.Level.SEVERE)
        sys.exit(1)


def check_dict(incoming: dict, string_only: bool = False, exempt_keys: set = None, allow_null_value: bool = False) -> dict:
    """Validates the incoming dictionary.
    Args:
        incoming (dict): The dictionary to validate.
        string_only (bool): Whether to allow only string values.
        exempt_keys (set): Keys whose values are exempt from the string-only check and must be a
            string or a list of strings (None is not allowed). Used for the proxy host key, which
            may hold a list of endpoints instead of a plain string.
        allow_null_value (bool): Whether a None value is accepted for any non-exempt key,
            regardless of string_only. This is required for updating secrets for a connection via
            configuration when deploying, but should stay False when just running/debugging a
            connector locally.

    Returns:
        dict: The validated dictionary.
    """

    if not incoming:
        return {}

    if not isinstance(incoming, dict):
        raise ValueError(
            "invalid configuration file; must be a valid JSON object\nreference: https://fivetran.com/docs/connector-sdk/connector-development-and-configuration/configuration-json#workingwithconfigurationjson")

    if string_only:
        exempt_keys = exempt_keys or set()
        for key, value in incoming.items():
            _validate_configuration_value(key, value, exempt_keys, allow_null_value)

    return incoming
