"""Migrates existing server-saved connection options into a local options file.

This module is self-contained by design: everything the stateless-CLI migration needs --
including its own REST calls -- lives here, so the whole feature can be removed in one place
once the migration window closes.
"""

import os
import sys
import time
from typing import Optional

import requests as rq
from tqdm import tqdm

from fivetran_connector_sdk_common import constants
from fivetran_connector_sdk_cli.connector_helper import NetworkingMethod, _auth_headers
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli.options_file import (
    is_options_file_supported, load_options_file, update_profile_fields, write_options_file)

_MIGRATION_CONNECTIONS_PATH = "/v1/connector-sdk/migration/connections"
_LIST_PAGE_LIMIT = 100
_LIST_TIMEOUT_SECONDS = 30
_RETRYABLE_STATUS_CODES = {429}


def _is_retryable(error: rq.exceptions.RequestException) -> bool:
    """Connection errors, timeouts, 429 and 5xx can succeed on a retry; other 4xx (invalid key,
    missing endpoint) can't.
    """
    if isinstance(error, rq.exceptions.HTTPError) and error.response is not None:
        status = error.response.status_code
        return status >= 500 or status in _RETRYABLE_STATUS_CODES
    return True


def _get_with_retries(url: str, headers: dict, params: Optional[dict] = None) -> rq.Response:
    """GETs a URL, retrying a transient failure with exponential backoff. Raises after
    MAX_RETRIES attempts, or at once for a failure that a retry can't fix.
    """
    for attempt in range(constants.MAX_RETRIES):
        try:
            resp = rq.get(url, headers=headers, params=params, timeout=_LIST_TIMEOUT_SECONDS)
            resp.raise_for_status()
            return resp
        except rq.exceptions.RequestException as e:
            if attempt == constants.MAX_RETRIES - 1 or not _is_retryable(e):
                raise
            retry_after = 2 ** attempt
            print_library_log(
                f"migration: request to Fivetran API failed, retrying in {retry_after}s "
                f"(attempt {attempt + 1}/{constants.MAX_RETRIES})",
                Logging.Level.WARNING)
            time.sleep(retry_after)


def _warn_migration_failed(error) -> None:
    print_library_log(
        f"migration failed: {error}. Your deployment will continue, and migration "
        f"will be retried on your next deployment. If this keeps happening, contact Fivetran Support. "
        f"For more information, see {constants.OPTIONS_FILE_MIGRATION_DOCS_URL}",
        Logging.Level.WARNING)


def _list_all_pages(path: str, deploy_key: str, on_page=None) -> Optional[list]:
    """Lists every item of a cursor-paginated endpoint. Returns None (never partial) on failure
    instead of exiting -- a migration failure is non-fatal. `on_page(count)` is called per page.
    """
    headers = _auth_headers(deploy_key)
    params = {"limit": _LIST_PAGE_LIMIT}
    items = []
    while True:
        try:
            resp = _get_with_retries(f"{constants.PRODUCTION_BASE_URL}{path}", headers, params)
        except rq.exceptions.RequestException as e:
            _warn_migration_failed(e)
            return None
        try:
            data = resp.json().get("data", {})
            page = data.get("items") or []
        except (ValueError, AttributeError) as e:
            _warn_migration_failed(f"unexpected response ({e})")
            return None
        items.extend(page)
        if on_page:
            on_page(len(page))
        cursor = data.get("next_cursor")
        if not cursor:
            return items
        if cursor == params.get("cursor"):
            _warn_migration_failed("the server returned the same page cursor twice")
            return None
        params = {"limit": _LIST_PAGE_LIMIT, "cursor": cursor}


def _list_connections_for_migration(deploy_key: str) -> Optional[list]:
    """Lists the deploy settings of every Connector SDK connection, via the migration endpoint."""
    with tqdm(desc="fetching connection details", bar_format="{desc}: {n_fmt} fetched [{elapsed}]", file=sys.stdout,
              leave=False) as progress:
        return _list_all_pages(_MIGRATION_CONNECTIONS_PATH, deploy_key, progress.update)


def _strip_naming_suffix(naming: Optional[str]) -> Optional[str]:
    if naming and naming.endswith(constants.UNDERSCORE_NAMING):
        return naming[: -len(constants.UNDERSCORE_NAMING)]
    return naming


def _non_empty(fields: dict) -> dict:
    """Drops empty values -- TOML has no null."""
    return {key: value for key, value in fields.items() if value}


def extract_managed_fields(connection: dict) -> dict:
    """Maps one connection from the migration endpoint onto the managed fields for its migrated
    profile. Empty values are omitted -- TOML has no null. package_id is kept only for a shared
    package, so a connection with its own package still packages and deploys local code by default.
    """
    fields = {
        constants.FIELD_DESTINATION: connection.get("group_name"),
        constants.FIELD_CONNECTION: connection.get("schema"),
        constants.FIELD_PYTHON_VERSION: connection.get(constants.FIELD_PYTHON_VERSION),
        constants.FIELD_NAMING: _strip_naming_suffix(connection.get("destination_schema_names")),
        constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID: connection.get(constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID),
        constants.FIELD_PROXY_HOST_CONFIG_KEY: connection.get(constants.FIELD_PROXY_HOST_CONFIG_KEY),
        constants.FIELD_PACKAGE_ID: connection.get(constants.FIELD_PACKAGE_ID) if connection.get("package_shared") else None,
    }
    if connection.get("networking_method") == NetworkingMethod.PROXY_AGENT.value:
        fields[constants.FIELD_PROXY_ID] = connection.get("proxy_agent_id")

    return _non_empty(fields)


def collect_migration_profiles(deploy_key: str) -> Optional[dict]:
    """Builds one profile per existing connection, keyed by "<group_id>-<connection_schema>".
    All-or-nothing: any API failure returns None rather than a partial result.
    """
    connections = _list_connections_for_migration(deploy_key)
    if connections is None:
        return None

    return {f"{connection.get('group_id')}-{connection.get('schema')}": extract_managed_fields(connection)
            for connection in connections}


_COMMENTED_DEFAULT_PROFILE = (
    '# ["default"]\n'
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

    if not is_options_file_supported():
        return None

    if os.path.isfile(options_file_path):
        return None

    print_library_log(
        f"no local options file found; migrating existing connection settings into "
        f"{options_file_path} (one-time step, will not run again once the file exists). "
        f"For more information, see {constants.OPTIONS_FILE_MIGRATION_DOCS_URL}",
        log_icon=Logging.LogIcon.STEP)

    profiles = collect_migration_profiles(deploy_key)
    if profiles is None:
        return None

    try:
        write_options_file(options_file_path, profiles, extra_header=_COMMENTED_DEFAULT_PROFILE + "\n")
    except OSError as e:
        print_library_log(
            f"migration failed: could not write options file {options_file_path}: {e}; "
            f"will retry on the next deployment. For more information, see {constants.OPTIONS_FILE_MIGRATION_DOCS_URL}",
            Logging.Level.WARNING)
        return None

    print_library_log(
        f"migration complete: saved the settings of {len(profiles)} existing connection(s) to {options_file_path}. "
        f"You can edit this file to change your deployment settings.",
        log_icon=Logging.LogIcon.SUCCESS)
    return options_file_path


def write_resolved_profile(options_file_path: str, group_id: str, connection: str, resolved: dict) -> None:
    """Persists this deploy's final resolved values into the connection's profile, overwriting
    whatever migration wrote (or adding it, if new). Only called when migration ran this deploy.
    package_id isn't taken from this deploy: it stays only if migration stored it (a shared package).
    """
    profile_name = f"{group_id}-{connection}"
    # An existing connection's naming isn't resolved (the server ignores it on update), so keep
    # the one migration stored instead of dropping it.
    stored_profiles = load_options_file(options_file_path) if os.path.isfile(options_file_path) else {}
    stored_profile = stored_profiles.get(profile_name, {})
    stored_naming = stored_profile.get(constants.FIELD_NAMING)
    fields = _non_empty({
        constants.FIELD_DESTINATION: resolved.get(constants.FIELD_DESTINATION),
        constants.FIELD_CONNECTION: connection,
        constants.FIELD_PYTHON_VERSION: resolved.get(constants.FIELD_PYTHON_VERSION),
        constants.FIELD_NAMING: _strip_naming_suffix(resolved.get(constants.FIELD_NAMING)) or stored_naming,
        constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID: resolved.get(constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID),
        constants.FIELD_PROXY_ID: resolved.get(constants.FIELD_PROXY_ID),
        constants.FIELD_PROXY_HOST_CONFIG_KEY: resolved.get(constants.FIELD_PROXY_HOST_CONFIG_KEY),
        constants.FIELD_PACKAGE_ID: stored_profile.get(constants.FIELD_PACKAGE_ID),
    })
    update_profile_fields(options_file_path, profile_name, fields,
                          extra_header=_COMMENTED_DEFAULT_PROFILE + "\n")
