import random
import string
import time

from collections.abc import Sequence
from typing import Any
from unittest.mock import MagicMock

import pytest

from snowflake.core._utils import check_version_gte
from snowflake.core.version import __version__ as VERSION


BASE_URL = "http://localhost:80/api/v2"


def is_gov_deployment(snowflake_region: str) -> bool:
    return "GOV" in snowflake_region


def is_preprod_deployment(snowflake_region: str) -> bool:
    return "PREPROD" in snowflake_region


def is_prod_deployment(version_str: str) -> bool:
    return version_str and all(character.isdigit() or character == "." for character in version_str)


def is_prod_or_preprod(version_str: str, snowflake_region: str) -> bool:
    # For prod, we check if version string is all digits or decimals, because non-prod versions contain
    # letters or other symbols.
    # For preprod, we check if "PREPROD" is in the regions name
    return is_prod_deployment(version_str) or is_preprod_deployment(snowflake_region)


def ensure_snowflake_version(current_version: str, requested_version: str) -> None:
    version_number = extract_version_number(current_version)
    if not check_version_gte(version_number, requested_version):
        pytest.skip(
            f"Skipping test because the current server version {version_number} "
            f"is older than the minimum version {requested_version}"
        )


def extract_version_number(version_str: str) -> str:
    # on non-prod deployments the CURRENT_VERSION result contains the version number and hash
    return version_str.split(" ")[0]


def random_string(
    length: int, prefix: str = "", suffix: str = "", choices: Sequence[str] = string.ascii_lowercase
) -> str:
    """Our convenience function to generate random string for object names.

    Args:
        length: How many random characters to choose from choices.
            length would be at least 6 for avoiding collision
        prefix: Prefix to add to random string generated.
        suffix: Suffix to add to random string generated.
        choices: A generator of things to choose from.
    """
    random_part = "".join([random.choice(choices) for _ in range(length)]) + str(time.time_ns())

    return "".join([prefix, random_part, suffix])


def unquote(name: str) -> str:
    if '""' in name:
        return name.replace('""', '"')
    if name.startswith('"') and name.endswith('"'):
        return name[1:-1]


def extra_params(**kwargs) -> dict[str, Any]:
    headers = {"Accept": "application/json", "User-Agent": "python_api/" + VERSION}
    if "body" in kwargs:
        headers["Content-Type"] = "application/json"
    return {
        "query_params": [],
        "headers": headers,
        "post_params": [],
        "body": None,
        "_preload_content": True,
        "_request_timeout": None,
    } | kwargs


def mock_http_response(data: str = "") -> MagicMock:
    m = MagicMock()
    m.data = data
    m.status = 200
    return m
