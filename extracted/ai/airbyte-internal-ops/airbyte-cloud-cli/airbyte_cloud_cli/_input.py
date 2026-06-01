# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Input helpers for `airbyte-cloud` commands."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Annotated

import yaml
from airbyte.exceptions import PyAirbyteInputError
from cyclopts import Parameter
from yaml import YAMLError

WorkspaceIdArg = Annotated[
    str | None,
    Parameter(
        name="--workspace-id",
        env_var=["AIRBYTE_WORKSPACE_ID", "AIRBYTE_CLOUD_WORKSPACE_ID"],
        help="The workspace ID.",
    ),
]
OrganizationIdArg = Annotated[
    str | None,
    Parameter(
        name="--organization-id",
        env_var=["AIRBYTE_ORGANIZATION_ID", "AIRBYTE_CLOUD_ORGANIZATION_ID"],
        help="The organization ID.",
    ),
]
ClientIdArg = Annotated[
    str | None,
    Parameter(
        env_var=["AIRBYTE_CLIENT_ID", "AIRBYTE_CLOUD_CLIENT_ID"],
        help="Airbyte client ID.",
    ),
]
ClientSecretArg = Annotated[
    str | None,
    Parameter(
        env_var=["AIRBYTE_CLIENT_SECRET", "AIRBYTE_CLOUD_CLIENT_SECRET"],
        help="Airbyte client secret.",
    ),
]
PublicApiRootArg = Annotated[
    str | None,
    Parameter(
        name="--public-api-root",
        env_var=["AIRBYTE_API_ROOT", "AIRBYTE_CLOUD_API_URL"],
        help="Airbyte public API root URL override.",
    ),
]
ConnectionIdArg = Annotated[
    str | None,
    Parameter(name="--connection-id", help="The connection ID."),
]
SourceIdArg = Annotated[
    str | None,
    Parameter(name="--source-id", help="The source ID."),
]
DestinationIdArg = Annotated[
    str | None,
    Parameter(name="--destination-id", help="The destination ID."),
]
JobIdArg = Annotated[
    int | None,
    Parameter(name="--job-id", help="The job ID."),
]
PositionalIdArg = Annotated[
    str,
    Parameter(show=False, consume_multiple=True),
]


def parse_config_options(
    *,
    config_json: str | None = None,
    config_file: Path | None = None,
) -> dict[str, object]:
    """Parse connector configuration from JSON text or a YAML/JSON file."""
    if bool(config_json) == bool(config_file):
        raise PyAirbyteInputError(
            message="Exactly one config input is required.",
            context={"options": "--config-json, --config-file"},
        )

    if config_json:
        try:
            parsed_json = json.loads(config_json)
        except JSONDecodeError as exc:
            raise PyAirbyteInputError(
                message="Config JSON must be valid JSON.",
                context={"option": "--config-json"},
            ) from exc
        if not isinstance(parsed_json, dict):
            raise PyAirbyteInputError(message="Config JSON must be an object.")
        return parsed_json

    if config_file is None:
        raise PyAirbyteInputError(message="Config file is required.")
    if not config_file.exists():
        raise PyAirbyteInputError(message="Config file does not exist.")

    try:
        parsed_file = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    except YAMLError as exc:
        raise PyAirbyteInputError(
            message="Config file must contain valid YAML or JSON.",
            context={"option": "--config-file"},
        ) from exc
    if not isinstance(parsed_file, dict):
        raise PyAirbyteInputError(message="Config file must contain an object.")
    return parsed_file


def parse_csv(value: str | None) -> list[str]:
    """Parse a comma-separated CLI option value."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def resolve_entity_id(
    args: tuple[str, ...],
    option_value: str | None,
    *,
    option_name: str,
) -> str:
    """Resolve an entity ID from one positional argument or named option."""
    if len(args) > 1:
        raise PyAirbyteInputError(message="Only one entity ID argument is allowed.")

    arg_value = args[0] if args else None
    if arg_value and option_value and arg_value != option_value:
        raise PyAirbyteInputError(message="Entity ID arguments must match.")

    entity_id = arg_value or option_value
    if not entity_id:
        raise PyAirbyteInputError(
            message="Entity ID is required.",
            context={"option": option_name},
        )

    return entity_id
