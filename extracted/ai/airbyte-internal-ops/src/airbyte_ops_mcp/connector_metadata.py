# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Utilities for reading and extracting connector metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast, overload

import dpath
import yaml

from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    CONNECTOR_PATH_PREFIX,
    METADATA_FILE_NAME,
)
from airbyte_ops_mcp.github_api import get_file_contents_at_ref

CONNECTOR_VERSION_DPATH = "data/dockerImageTag"
RawConnectorMetadata = dict[str, Any]


class ConnectorMetadataDpathNotFoundError(ValueError):
    """Raised when a dpath expression is not found in connector metadata."""


class ConnectorMetadataDpathError(ValueError):
    """Raised when a dpath expression cannot be evaluated."""


@overload
def load_raw_connector_metadata_from_local(
    repo_path: Path,
    connector_name: str,
    *,
    dpath_expression: None = None,
) -> RawConnectorMetadata: ...


@overload
def load_raw_connector_metadata_from_local(
    repo_path: Path,
    connector_name: str,
    *,
    dpath_expression: str,
) -> Any: ...


def load_raw_connector_metadata_from_local(
    repo_path: Path,
    connector_name: str,
    *,
    dpath_expression: str | None = None,
) -> RawConnectorMetadata | Any:
    """Load a local connector `metadata.yaml` file as raw metadata."""
    metadata_file = (
        repo_path / CONNECTOR_PATH_PREFIX / connector_name / METADATA_FILE_NAME
    )
    if not metadata_file.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
    return load_raw_connector_metadata_yaml(
        metadata_file.read_text(),
        dpath_expression=dpath_expression,
    )


@overload
def load_raw_connector_metadata_from_github(
    connector_name: str,
    *,
    owner: str,
    repo: str,
    ref: str,
    gh_token: str | None = None,
    dpath_expression: None = None,
) -> RawConnectorMetadata: ...


@overload
def load_raw_connector_metadata_from_github(
    connector_name: str,
    *,
    owner: str,
    repo: str,
    ref: str,
    gh_token: str | None = None,
    dpath_expression: str,
) -> Any: ...


def load_raw_connector_metadata_from_github(
    connector_name: str,
    *,
    owner: str,
    repo: str,
    ref: str,
    gh_token: str | None = None,
    dpath_expression: str | None = None,
) -> RawConnectorMetadata | Any:
    """Load connector `metadata.yaml` from GitHub as raw metadata."""
    path = f"{CONNECTOR_PATH_PREFIX}/{connector_name}/{METADATA_FILE_NAME}"
    content = get_file_contents_at_ref(owner, repo, path, ref, token=gh_token)
    if content is None:
        raise FileNotFoundError(
            f"Metadata file not found at {owner}/{repo}:{ref}:{path}"
        )
    return load_raw_connector_metadata_yaml(content, dpath_expression=dpath_expression)


@overload
def load_raw_connector_metadata_yaml(
    content: str,
    *,
    dpath_expression: None = None,
) -> RawConnectorMetadata: ...


@overload
def load_raw_connector_metadata_yaml(
    content: str,
    *,
    dpath_expression: str,
) -> Any: ...


def load_raw_connector_metadata_yaml(
    content: str,
    *,
    dpath_expression: str | None = None,
) -> RawConnectorMetadata | Any:
    """Parse connector metadata YAML content as raw metadata."""
    metadata = _parse_raw_connector_metadata_yaml(content)
    if dpath_expression is None:
        return metadata
    return get_raw_metadata_dpath_value(metadata, dpath_expression)


def _parse_raw_connector_metadata_yaml(content: str) -> RawConnectorMetadata:
    try:
        metadata = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError("Connector metadata YAML could not be parsed.") from e
    if not isinstance(metadata, dict):
        raise ValueError("Connector metadata YAML must contain a mapping.")
    return cast(RawConnectorMetadata, metadata)


def get_raw_metadata_dpath_value(
    metadata: RawConnectorMetadata,
    dpath_expression: str,
) -> Any:
    """Evaluate a dpath expression against parsed connector metadata."""
    try:
        return dpath.get(metadata, dpath_expression)
    except KeyError as e:
        raise ConnectorMetadataDpathNotFoundError(
            f"DPath expression not found in metadata: {dpath_expression}"
        ) from e
    except ValueError as e:
        raise ConnectorMetadataDpathError(
            f"DPath expression did not resolve to one value: {dpath_expression}"
        ) from e


def get_connector_version_from_metadata(metadata: RawConnectorMetadata) -> str:
    """Get `data/dockerImageTag` from parsed connector metadata."""
    value = get_raw_metadata_dpath_value(metadata, CONNECTOR_VERSION_DPATH)
    if not isinstance(value, str):
        raise ConnectorMetadataDpathError(
            f"DPath expression did not resolve to a string: {CONNECTOR_VERSION_DPATH}"
        )
    return value


def load_local_connector_metadata(
    repo_path: Path,
    connector_name: str,
) -> RawConnectorMetadata:
    """Load a local connector `metadata.yaml` file as raw metadata."""
    return load_raw_connector_metadata_from_local(repo_path, connector_name)


def load_connector_metadata_yaml(content: str) -> RawConnectorMetadata:
    """Parse connector metadata YAML content as raw metadata."""
    return load_raw_connector_metadata_yaml(content)


def get_metadata_dpath_value(
    metadata: RawConnectorMetadata,
    dpath_expression: str,
) -> Any:
    """Evaluate a dpath expression against parsed connector metadata."""
    return get_raw_metadata_dpath_value(metadata, dpath_expression)


def format_metadata_dpath_value(value: Any) -> str:
    """Format a dpath value for CLI output."""
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, default=str)
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
