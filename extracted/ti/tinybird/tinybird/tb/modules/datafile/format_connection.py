import json
from typing import Any, Dict, List, Optional

from tinybird.datafile.common import Datafile
from tinybird.datafile.parse_connection import parse_connection
from tinybird.tb.modules.datafile.format_common import (
    DATAFILE_INDENT,
    DATAFILE_NEW_LINE,
    format_description,
    format_include,
)

# Define the order of settings for each connection type
# Settings not in these lists will be appended at the end
KAFKA_SETTINGS_ORDER = [
    "kafka_bootstrap_servers",
    "kafka_security_protocol",
    "kafka_sasl_mechanism",
    "kafka_key",
    "kafka_secret",
    "kafka_schema_registry_url",
    "kafka_ssl_ca_pem",
    "kafka_sasl_oauthbearer_method",
    "kafka_sasl_oauthbearer_aws_region",
    "kafka_sasl_oauthbearer_aws_role_arn",
    "kafka_sasl_oauthbearer_aws_external_id",
    "kafka_key_avro_deserialization",
    "kafka_key_format",
]

S3_SETTINGS_ORDER = [
    "s3_arn",
    "s3_region",
    "s3_access_key",
    "s3_secret",
]

GCS_SETTINGS_ORDER = [
    "gcs_service_account_credentials_json",
    "gcs_hmac_access_id",
    "gcs_hmac_secret",
]

# Multiline settings that need special handling
MULTILINE_SETTINGS = {"kafka_ssl_ca_pem"}


def format_connection(
    filename: str,
    datafile: Optional[Datafile] = None,
    skip_eval: bool = False,
    content: Optional[str] = None,
    ignore_secrets: bool = False,
) -> str:
    """Format a .connection file.

    Args:
        filename: The path to the connection file.
        datafile: Optional pre-parsed datafile.
        skip_eval: Whether to skip template evaluation.
        content: Optional content string instead of reading from file.
        ignore_secrets: Whether to ignore secret resolution.

    Returns:
        The formatted connection file content as a string.
    """
    if datafile:
        doc = datafile
    else:
        doc = parse_connection(
            filename,
            skip_eval=skip_eval,
            content=content,
            ignore_secrets=ignore_secrets,
        ).datafile

    file_parts: List[str] = []

    # Format description if present
    format_description(file_parts, doc)

    # Get the node data (connection files have a single "default" node)
    if doc.nodes:
        node = doc.nodes[0]
        format_type(file_parts, node)
        format_connection_settings(file_parts, node)

    # Format includes if present
    format_include(file_parts, doc)

    result = "".join(file_parts)
    result = result.rstrip("\n") + "\n"
    return result


def format_type(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    """Format the TYPE setting."""
    connection_type = node.get("type")
    if connection_type:
        file_parts.append(f"TYPE {connection_type}")
        file_parts.append(DATAFILE_NEW_LINE)
    return file_parts


def format_connection_settings(file_parts: List[str], node: Dict[str, Any]) -> List[str]:
    """Format connection-specific settings based on connection type."""
    connection_type = node.get("type", "").lower()

    # Determine the order of settings based on connection type
    if connection_type == "kafka":
        settings_order = KAFKA_SETTINGS_ORDER
    elif connection_type in ("s3", "s3_iamrole"):
        settings_order = S3_SETTINGS_ORDER
    elif connection_type in ("gcs", "gcs_hmac"):
        settings_order = GCS_SETTINGS_ORDER
    else:
        # For unknown types, just output all settings
        settings_order = []

    # Keys to skip (already handled or not settings)
    skip_keys = {"type", "name", "schema", "columns", "engine", "description"}

    # First, format settings in the defined order
    formatted_keys = set()
    for setting in settings_order:
        if setting in node and node[setting] is not None:
            format_setting(file_parts, setting, node[setting])
            formatted_keys.add(setting)

    # Then, format any remaining settings that weren't in the order list
    for key, value in node.items():
        if key not in formatted_keys and key not in skip_keys and value is not None:
            format_setting(file_parts, key, value)

    return file_parts


def format_setting(file_parts: List[str], key: str, value: Any) -> None:
    """Format a single connection setting."""
    key_upper = key.upper()

    if key in MULTILINE_SETTINGS and value and "\n" in str(value):
        # Handle multiline settings
        file_parts.append(f"{key_upper} >")
        file_parts.append(DATAFILE_NEW_LINE)
        for line in str(value).split("\n"):
            if line.strip():
                file_parts.append(f"{DATAFILE_INDENT}{line.strip()}")
                file_parts.append(DATAFILE_NEW_LINE)
    else:
        # Handle single-line settings
        # Non-string values (dict, list, bool, int, float, None) came from JSON parsing
        # and need to be serialized back to valid JSON
        if isinstance(value, str):
            formatted_value = value
        else:
            formatted_value = json.dumps(value, separators=(",", ": "))
        file_parts.append(f"{key_upper} {formatted_value}")
        file_parts.append(DATAFILE_NEW_LINE)
