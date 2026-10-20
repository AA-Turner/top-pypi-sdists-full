"""Migrates existing server-saved connection options into a local options file.

This module is self-contained by design: everything the stateless-CLI migration needs --
including its own REST calls -- lives here, so the whole feature can be removed in one place
once the migration window closes (see the TDD's deployment/rollback phase 3, "migration path
removed").
"""

import os
import sys
import time
from typing import Optional

import requests as rq
from tqdm import tqdm

from fivetran_connector_sdk_common import constants
from fivetran_connector_sdk_common.connector_helper import NetworkingMethod, get_user_agent
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_common.options_file import write_options_file, update_profile_fields

_CONNECTOR_SDK_SERVICE = "connector_sdk"
_LIST_PAGE_LIMIT = 1000


def _migration_headers(deploy_key: str) -> dict:
    return {
        "Authorization": f"Basic {deploy_key}",
        "User-Agent": get_user_agent(),
    }


def _get_with_retries(url: str, headers: dict, params: Optional[dict] = None) -> rq.Response:
    """GETs a URL, retrying a transient failure with exponential backoff. Raises after
    MAX_RETRIES attempts.
    """
    for attempt in range(constants.MAX_RETRIES):
        try:
            resp = rq.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            return resp
        except rq.exceptions.RequestException:
            if attempt == constants.MAX_RETRIES - 1:
                raise
            retry_after = 2 ** attempt
            print_library_log(
                f"migration: request to Fivetran API failed, retrying in {retry_after}s "
                f"(attempt {attempt + 1}/{constants.MAX_RETRIES})",
                Logging.Level.WARNING)
            time.sleep(retry_after)


def _list_groups_for_migration(deploy_key: str) -> Optional[dict]:
    """Lists every destination as {group_id: group_name}. Returns None on failure instead of
    exiting -- a migration failure is non-fatal.
    """
    headers = _migration_headers(deploy_key)
    params = {"limit": _LIST_PAGE_LIMIT}
    group_id_to_name = {}
    while True:
        try:
            resp = _get_with_retries(f"{constants.PRODUCTION_BASE_URL}/v1/groups", headers, params)
        except rq.exceptions.RequestException:
            print_library_log(
                "migration: failed to list destinations; migration will be retried on the next deploy",
                Logging.Level.WARNING)
            return None
        data = resp.json().get("data", {})
        for group in data.get("items", []):
            group_id_to_name[group["id"]] = group["name"]
        cursor = data.get("next_cursor")
        if not cursor:
            return group_id_to_name
        params = {"limit": _LIST_PAGE_LIMIT, "cursor": cursor}


def _list_connections_for_migration(deploy_key: str) -> Optional[list]:
    """Lists every Connector SDK connection. Returns None (never partial) on failure."""
    headers = _migration_headers(deploy_key)
    params = {"limit": _LIST_PAGE_LIMIT}
    connections = []
    while True:
        try:
            resp = _get_with_retries(f"{constants.PRODUCTION_BASE_URL}/v1/connections", headers, params)
        except rq.exceptions.RequestException:
            print_library_log(
                "migration: failed to list existing connections; migration will be retried on the next deploy",
                Logging.Level.WARNING)
            return None
        data = resp.json().get("data", {})
        connections.extend(data.get("items", []))
        cursor = data.get("next_cursor")
        if not cursor:
            return [c for c in connections if c.get("service") == _CONNECTOR_SDK_SERVICE]
        params = {"limit": _LIST_PAGE_LIMIT, "cursor": cursor}


def _get_connection_detail_for_migration(connection_id: str, deploy_key: str) -> Optional[dict]:
    """Fetches one connection's full options. Returns None on failure."""
    try:
        resp = _get_with_retries(
            f"{constants.PRODUCTION_BASE_URL}/v1/connections/{connection_id}",
            _migration_headers(deploy_key))
    except rq.exceptions.RequestException:
        print_library_log(
            f"migration: failed to fetch options for connection '{connection_id}'",
            Logging.Level.WARNING)
        return None
    return resp.json().get("data")


def extract_managed_fields(connection_detail: dict, group_id_to_name: dict) -> dict:
    """Maps one connection's API detail onto the managed fields for its migrated profile.
    Empty values are omitted -- TOML has no null.
    """
    config = connection_detail.get("config") or {}
    naming = connection_detail.get("destination_schema_names")
    if naming and naming.endswith(constants.UNDERSCORE_NAMING):
        naming = naming[: -len(constants.UNDERSCORE_NAMING)]

    fields = {
        "destination": group_id_to_name.get(connection_detail.get("group_id")),
        "connection": connection_detail.get("schema"),
        "python_version": config.get("python_version"),
        "naming": naming,
        "hybrid_deployment_agent_id": connection_detail.get("hybrid_deployment_agent_id"),
        "proxy_host_config_key": config.get("proxy_host_config_key"),
        "package_id": config.get("package_id"),
    }
    if connection_detail.get("networking_method") == NetworkingMethod.PROXY_AGENT.value:
        fields["proxy_id"] = connection_detail.get("proxy_agent_id")

    return {key: value for key, value in fields.items() if value}


def collect_migration_profiles(deploy_key: str) -> Optional[dict]:
    """Builds one profile per existing connection, keyed by "<group_id>-<connection_schema>".
    All-or-nothing: any API failure returns None rather than a partial result.
    """
    connections = _list_connections_for_migration(deploy_key)
    if connections is None:
        return None

    profiles = {}
    if not connections:
        return profiles

    group_id_to_name = _list_groups_for_migration(deploy_key)
    if group_id_to_name is None:
        return None

    for connection in tqdm(connections, desc="fetching connection options", unit="connection",
                           file=sys.stdout, leave=False):
        detail = _get_connection_detail_for_migration(connection["id"], deploy_key)
        if detail is None:
            print_library_log(
                "migration failed while fetching existing connection options; contact "
                "Fivetran Support if this persists. Continuing deploy without a local "
                "options file; migration will be retried on the next deploy.",
                Logging.Level.WARNING)
            return None
        profile_name = f"{detail.get('group_id')}-{detail.get('schema')}"
        profiles[profile_name] = extract_managed_fields(detail, group_id_to_name)

    return profiles


_COMMENTED_DEFAULT_PROFILE = (
    "# [default]\n"
    f'# python_version = "{constants.DEFAULT_PYTHON_VERSION}"\n'
    f'# naming = "{constants.FIVETRAN_NAMING_VALUE}"\n'
)


def run_migration(deploy_key: str, options_file_path: str) -> Optional[str]:
    """Migrates existing server-saved connection options into a new local options file.
    Skips if already migrated, in CI, or on Python < 3.11. Not safe against two deploys
    racing to migrate at once -- last write wins, an accepted tradeoff.

    Returns:
        Optional[str]: The path written, or None if migration didn't run or failed.
    """
    if (os.getenv("CI") or "").lower() == "true":
        print_library_log("migration skipped: CI=true", log_icon=Logging.LogIcon.INFO)
        return None

    if sys.version_info < (3, 11):
        print_library_log(constants.OPTIONS_FILE_SKIP_MIN_PYTHON_MESSAGE)
        return None

    if os.path.isfile(options_file_path):
        return None

    print_library_log(
        f"no local options file found; migrating existing connection settings into "
        f"{options_file_path} (one-time step, won't run again once the file exists)",
        log_icon=Logging.LogIcon.STEP)

    profiles = collect_migration_profiles(deploy_key)
    if profiles is None:
        return None

    try:
        write_options_file(options_file_path, profiles, extra_header=_COMMENTED_DEFAULT_PROFILE + "\n")
    except OSError as e:
        print_library_log(
            f"migration failed: could not write options file {options_file_path}: {e}; "
            f"will retry on the next deploy",
            Logging.Level.WARNING)
        return None

    print_library_log(
        f"migration complete: wrote {len(profiles)} profile(s) to {options_file_path}; "
        f"edit it anytime, the CLI won't touch it again automatically",
        log_icon=Logging.LogIcon.SUCCESS)
    return options_file_path


def write_resolved_profile(options_file_path: str, group_id: str, connection: str, resolved: dict,
                           package_id: Optional[str]) -> None:
    """Persists this deploy's final resolved values into the connection's profile, overwriting
    whatever migration wrote (or adding it, if new). Only called when migration ran this deploy.
    """
    naming = resolved.get("naming")
    if naming and naming.endswith(constants.UNDERSCORE_NAMING):
        naming = naming[: -len(constants.UNDERSCORE_NAMING)]

    fields = {
        "destination": resolved.get("destination"),
        "connection": connection,
        "python_version": resolved.get("python_version"),
        "naming": naming,
        "hybrid_deployment_agent_id": resolved.get("hybrid_deployment_agent_id"),
        "proxy_id": resolved.get("proxy_id"),
        "proxy_host_config_key": resolved.get("proxy_host_config_key"),
        "package_id": package_id,
    }
    fields = {key: value for key, value in fields.items() if value}
    update_profile_fields(options_file_path, f"{group_id}-{connection}", fields,
                          extra_header=_COMMENTED_DEFAULT_PROFILE + "\n")
