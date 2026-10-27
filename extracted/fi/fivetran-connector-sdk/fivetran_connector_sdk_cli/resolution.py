"""Resolves managed deploy fields from CLI param -> env var -> options-file profile ->
SDK built-in default, and logs the resolved value/source for each. See the stateless CLI TDD's
"Field Resolution" and "End-to-End Deploy Flow" sections.

Does not resolve `pyproject.toml` package defaults (step 4 of the TDD's precedence list) -- no
such mechanism exists in the SDK today; left out of scope for this change.

Structure:
    `resolve_deploy_options` orchestrates one `_resolve_<field>` function per managed field,
    then reports missing fields, warns about server drift, and logs a summary.
"""

import sys
from typing import Optional, Tuple

from fivetran_connector_sdk_common import constants
from fivetran_connector_sdk_cli.connector_helper import (
    NetworkingMethod,
    get_connection_detail,
    get_connection_details,
    get_connection_name,
    get_destination_default_hd_agent_id,
    get_destination_group,
    get_group_info,
    get_hd_agent_id,
    get_naming,
    get_package_id,
    get_proxy_host_config_key,
    get_proxy_id,
    get_python_version,
    validate_naming,
)
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli.options_file import (
    find_options_file, is_options_file_supported, load_options_file, select_profile)

_OPTIONS_FILE_ENV = constants.FIVETRAN_OPTIONS_FILE_ENV
_SDK_DEFAULT_SOURCE = "SDK built-in default"
_OPTIONS_FILE_SOURCE_PREFIX = "options file"

# A resolved field's (value, source) pair; `source` is None only when `value` is also unresolved.
_ResolvedField = Tuple[Optional[str], Optional[str]]
# A (flag, env_var) pair describing how an unresolved required field could have been provided.
_MissingEntry = Tuple[str, str]


def _profile_source(profile_label: str) -> str:
    return f"{_OPTIONS_FILE_SOURCE_PREFIX}, profile [{profile_label}]"


def _group_id(destination: str, deploy_key: str, group_ids: dict) -> str:
    """The destination's group id, looked up once per run and memoised in `group_ids`."""
    if destination not in group_ids:
        group_ids[destination], _ = get_group_info(destination, deploy_key)
    return group_ids[destination]


def _candidate_profile_name(args, options_data: dict, deploy_key: str, group_ids: dict) -> Optional[str]:
    """Best-effort guess at the profile name matching the connection being deployed, confirmed
    to actually exist in `options_data`, built only from CLI/env-provided destination+
    connection identity (never from whichever profile was actually selected, since the point is
    suggesting a profile when the one actually selected is wrong or missing).

    Returns None when destination/connection aren't both available from CLI/env, no options file
    applies, or the candidate doesn't exist in it. A failed destination lookup exits.
    """
    destination = get_destination_group(args)
    connection = get_connection_name(args)
    if not destination or not connection or not options_data:
        return None
    group_id = _group_id(destination, deploy_key, group_ids)
    candidate = f"{group_id}-{connection}"
    return candidate if candidate in options_data else None


def _select_active_profile(args, deploy_key: str, group_ids: dict,
                           is_first_migration_deploy: bool = False) -> Tuple[dict, str, dict, Optional[str]]:
    """Locates the options file (if any) and selects the profile it applies for this deploy.

    On the first migration deploy, with no specific `--profile` requested (omitted, or
    explicitly "default"), selects the migrated profile that matches this connection (named
    "<group_id>-<connection>") instead of the absent [default], so the connection's
    just-migrated settings are used rather than new-connection defaults.

    When no options file exists at all and a named, non-default profile was explicitly
    requested, fails the same way a missing profile in an existing file would, instead of
    silently ignoring the request.

    Only computes the profile-mismatch hint (an extra API lookup) when the requested profile is
    actually missing -- never on the common, successful path -- since the hint is purely
    advisory and not worth its cost when nothing is wrong.

    Returns:
        Tuple[dict, str, dict, Optional[str]]: The selected profile's fields (empty dict if none
            applies), the profile label to use in log/error messages, every profile in the
            options file (empty dict if there is no file), and the options file's path (None if
            there is no file).
    """
    profile_name = getattr(args, "profile", None)
    options_path = find_options_file(args)
    if not options_path:
        if (profile_name and profile_name != constants.DEFAULT_PROFILE_NAME
                and is_options_file_supported()):
            select_profile({}, profile_name)
        return {}, profile_name or constants.DEFAULT_PROFILE_NAME, {}, None

    data = load_options_file(options_path)
    no_profile_requested = profile_name is None or profile_name == constants.DEFAULT_PROFILE_NAME
    if no_profile_requested and is_first_migration_deploy:
        migrated_profile = _candidate_profile_name(args, data, deploy_key, group_ids)
        if migrated_profile:
            profile_name = migrated_profile

    hint_profile = (_candidate_profile_name(args, data, deploy_key, group_ids)
                    if profile_name and profile_name not in data else None)
    profile, _applied = select_profile(data, profile_name, hint_profile, options_path)
    return profile, profile_name or constants.DEFAULT_PROFILE_NAME, data, options_path


def _lookup_connection_context(destination: str, connection: str, deploy_key: str, group_ids: dict):
    """Looks up the current server-side state for this connection (if any), to support the
    migration-period required-field rule and the resolved-value warnings below. A lookup
    failure (e.g. an invalid destination) propagates rather than being treated as "new
    connection" -- that classification must only follow a successful lookup that genuinely
    found no match.

    Returns:
        Tuple[bool, Optional[str], Optional[dict]]: (is_new_connection, group_id, the
            connection's full detail dict or None).
    """
    group_id = _group_id(destination, deploy_key, group_ids)
    details = get_connection_details(connection, destination, group_id, deploy_key)
    if details is None:
        return True, group_id, None
    connection_id, _ = details
    return False, group_id, get_connection_detail(connection_id, deploy_key)


def _current_server_values(current_detail: Optional[dict]) -> dict:
    """Extracts the current server-side values this module compares resolved values against.
    Omits `naming`: it can't be changed after connection creation (the server silently ignores
    it), so a mismatch there isn't something the deploy would actually update.

    Deliberately not shared with migration.py's extract_managed_fields -- migration.py is
    self-contained by design so it can be removed in one place once the migration window closes
    (see its module docstring); this comparison isn't part of that removal.
    """
    if not current_detail:
        return {}
    config = current_detail.get("config") or {}
    return {
        constants.FIELD_PYTHON_VERSION: config.get(constants.FIELD_PYTHON_VERSION),
        constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID: current_detail.get(constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID),
        constants.FIELD_PROXY_HOST_CONFIG_KEY: config.get(constants.FIELD_PROXY_HOST_CONFIG_KEY),
        constants.FIELD_PACKAGE_ID: config.get(constants.FIELD_PACKAGE_ID),
    }


def _resolve(field: str, cli_env_value, cli_env_source: Optional[str], profile: dict,
             profile_label: str) -> _ResolvedField:
    """Applies the CLI/env -> options-file precedence for a single field."""
    if cli_env_value:
        return cli_env_value, cli_env_source
    if profile.get(field):
        return profile[field], _profile_source(profile_label)
    return None, None


def _source_from_flag(args, attr: str, flag: str) -> Optional[str]:
    """`flag`, if it was explicitly passed on the CLI, else None. For fields with no env var."""
    return flag if getattr(args, attr, None) else None


def _source_from_flag_or_env(args, attr: str, flag: str, env_var: str, value) -> Optional[str]:
    """`flag` if it was explicitly passed on the CLI; else `env_var` if `value` is set (meaning
    it must have come from the env var, since the CLI flag wasn't used); else None.
    """
    if getattr(args, attr, None):
        return flag
    return env_var if value else None


def _resolve_required_field(args, attr: str, flag: str, env_var: str, getter, profile: dict,
                             profile_label: str) -> Tuple[Optional[str], Optional[str], Optional[_MissingEntry]]:
    """Resolves `destination` or `connection` via CLI/env/profile. Always required -- no
    default or fallback applies.
    """
    value = getter(args)
    source = _source_from_flag_or_env(args, attr, flag, env_var, value)
    value, source = _resolve(attr, value, source, profile, profile_label)
    missing_entry = None if value else (flag, env_var)
    return value, source, missing_entry


def _resolve_python_version(args, prompt_mode, profile: dict, profile_label: str,
                             treat_as_new: bool) -> Tuple[Optional[str], Optional[str], Optional[_MissingEntry]]:
    """Resolves python_version via CLI/env/profile. If unresolved, falls back to the SDK
    default for a new connection (or the first migration deploy); otherwise reported as missing.
    """
    value = get_python_version(args, prompt_mode)
    source = _source_from_flag_or_env(args, constants.FIELD_PYTHON_VERSION, "--python-version",
                                       constants.FIVETRAN_PYTHON_VERSION_ENV, value)
    value, source = _resolve(constants.FIELD_PYTHON_VERSION, value, source, profile, profile_label)
    missing_entry = None
    if not value:
        if treat_as_new:
            value, source = constants.DEFAULT_PYTHON_VERSION, _SDK_DEFAULT_SOURCE
        else:
            missing_entry = ("--python-version", constants.FIVETRAN_PYTHON_VERSION_ENV)
    return value, source, missing_entry


def _resolve_hd_agent_id(args, prompt_mode, profile: dict, profile_label: str, treat_as_new: bool,
                          group_id: Optional[str], current_detail: Optional[dict],
                          deploy_key: str) -> Tuple[Optional[str], Optional[str], Optional[_MissingEntry]]:
    """Resolves hybrid_deployment_agent_id via CLI/env/profile. If unresolved: required when an
    existing connection already relies on an agent; falls back to the destination's default
    agent for a new connection (or the first migration deploy); otherwise left unset.
    """
    value = get_hd_agent_id(args, prompt_mode)
    source = _source_from_flag_or_env(args, constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID, "--hybrid-deployment-agent-id",
                                       constants.FIVETRAN_HD_AGENT_ID, value)
    value, source = _resolve(constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID, value, source, profile, profile_label)
    missing_entry = None
    if not value:
        current_hd_agent_id = (current_detail or {}).get(constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID)
        if not treat_as_new and current_hd_agent_id:
            missing_entry = ("--hybrid-deployment-agent-id", constants.FIVETRAN_HD_AGENT_ID)
        elif treat_as_new and group_id:
            default_agent_id = get_destination_default_hd_agent_id(group_id, deploy_key)
            if default_agent_id:
                value, source = default_agent_id, "destination's default agent_id"
    return value, source, missing_entry


def _resolve_proxy_fields(args, profile: dict, profile_label: str,
                          current_detail: Optional[dict]) -> Tuple[_ResolvedField, _ResolvedField]:
    """Resolves proxy_id and proxy_host_config_key via CLI/profile (no env var; never
    required). Warns when proxy_id goes unresolved for a connection currently using a Proxy
    Agent, since it will revert to direct networking.
    """
    proxy_id_cli = get_proxy_id(args)
    proxy_id_source = _source_from_flag(args, constants.FIELD_PROXY_ID, "--proxy-id")
    proxy_id, proxy_id_source = _resolve(constants.FIELD_PROXY_ID, proxy_id_cli, proxy_id_source, profile, profile_label)
    if not proxy_id and current_detail and current_detail.get("networking_method") == NetworkingMethod.PROXY_AGENT.value:
        print_library_log(
            "proxy_id not resolved for a connection that currently uses a Proxy Agent; the "
            "connection will revert to direct networking",
            Logging.Level.WARNING)

    phck_cli = get_proxy_host_config_key(args)
    phck_source = _source_from_flag(args, constants.FIELD_PROXY_HOST_CONFIG_KEY, "--proxy-host-config-key")
    proxy_host_config_key, phck_source = _resolve(
        constants.FIELD_PROXY_HOST_CONFIG_KEY, phck_cli, phck_source, profile, profile_label)

    return (proxy_id, proxy_id_source), (proxy_host_config_key, phck_source)


def _resolve_package_id(args, profile: dict, profile_label: str) -> _ResolvedField:
    """Resolves package_id via CLI/profile (no env var; never required)."""
    cli_value = get_package_id(args)
    source = _source_from_flag(args, constants.FIELD_PACKAGE_ID, "--package-id")
    return _resolve(constants.FIELD_PACKAGE_ID, cli_value, source, profile, profile_label)


def _resolve_naming(args, profile: dict, profile_label: str, is_new_connection: bool) -> _ResolvedField:
    """Resolves naming via CLI/env, then (for a new connection only) a validated/suffixed profile
    value, then the default. An existing connection with no explicit value is left unresolved,
    since the server ignores naming on updates and resolving it from the profile or a default
    would trigger a warning on every redeploy.
    """
    value = get_naming(args)
    source = _source_from_flag_or_env(args, constants.FIELD_NAMING, "--naming", constants.FIVETRAN_NAMING_ENV, value)
    if not value and is_new_connection:
        validated = validate_naming(profile.get(constants.FIELD_NAMING))
        if validated:
            value = validated + constants.UNDERSCORE_NAMING
            source = _profile_source(profile_label)
    if not value and is_new_connection:
        value = constants.FIVETRAN_NAMING_VALUE + constants.UNDERSCORE_NAMING
        source = _SDK_DEFAULT_SOURCE
    return value, source


def _report_missing_and_exit(missing: list, profile_label: str, args, options_data: dict, deploy_key: str,
                             group_ids: dict) -> None:
    """Logs all unresolved required fields together, hints at a matching profile name if none
    was explicitly selected, and exits.
    """
    for flag, env in missing:
        if is_options_file_supported():
            sources = f"the {flag} flag, the {env} environment variable, or the options file (profile [{profile_label}])"
        else:
            sources = f"the {flag} flag or the {env} environment variable"
        reason = " when deploying to an existing connection" if flag == "--python-version" else ""
        print_library_log(f"{flag} is required{reason}; provide it via {sources}", Logging.Level.SEVERE)
    print_library_log(
        f"For more information, see {constants.FIELD_RESOLUTION_ORDER_DOCS_URL}", Logging.Level.SEVERE)
    if getattr(args, "profile", None) in (None, constants.DEFAULT_PROFILE_NAME):
        hint_profile = _candidate_profile_name(args, options_data, deploy_key, group_ids)
        if hint_profile:
            print_library_log(
                f"a profile named '{hint_profile}' exists in the options file that may "
                f"match this connection; did you mean '--profile {hint_profile}'?",
                Logging.Level.WARNING)
    sys.exit(1)


def _warn_on_server_drift(resolved: dict, current_detail: Optional[dict]) -> None:
    """Warns for each field whose resolved value differs from the connection's current server
    value -- the deploy will overwrite it.
    """
    server_values = _current_server_values(current_detail)
    for field, (value, _source) in resolved.items():
        server_value = server_values.get(field)
        if value and server_value and str(value) != str(server_value):
            print_library_log(
                f"resolved {field} ('{value}') differs from the connection's current server "
                f"value ('{server_value}'); the server value will be updated",
                Logging.Level.WARNING)


def _log_resolved_summary(resolved: dict, options_path: Optional[str]) -> None:
    """Logs the final value and source of every resolved field, and which options file was read
    if any value came from it.
    """
    if options_path and any(source and source.startswith(_OPTIONS_FILE_SOURCE_PREFIX)
                            for _value, source in resolved.values()):
        print_library_log(f"reading options from {options_path}", Logging.Level.INFO,
                          log_icon=Logging.LogIcon.INFO)
    print_library_log("resolved options:", Logging.Level.INFO, log_icon=Logging.LogIcon.INFO)
    for field, (value, source) in resolved.items():
        if value:
            phrase = f"using {source}" if source == _SDK_DEFAULT_SOURCE else f"provided via {source}"
            print_library_log(f"  {field} = {value} ({phrase})", Logging.Level.INFO)


def resolve_deploy_options(args, prompt_mode, deploy_key: str, is_first_migration_deploy: bool = False,
                           group_ids: Optional[dict] = None) -> dict:
    """Resolves every managed deploy field for this run and logs the resolved values/sources.
    Each field's precedence and default rules are documented on its `_resolve_<field>` function.

    `is_first_migration_deploy` is set only for the one-time deploy that just created the
    options file, so an existing connection isn't immediately failed on a field it never had a
    chance to add; the SDK default used then is written back into its profile afterwards (see
    `migration.write_resolved_profile`), so later deploys read an explicit value.

    `group_ids` is an optional {destination name: group id} cache that the resolver fills as it
    looks groups up, so the caller can reuse the ids instead of repeating the API call.

    Returns:
        dict: Resolved values keyed by field name (`hybrid_deployment_agent_id`, `proxy_id`,
            `proxy_host_config_key` may be None).
    """
    group_ids = {} if group_ids is None else group_ids
    profile, profile_label, options_data, options_path = _select_active_profile(
        args, deploy_key, group_ids, is_first_migration_deploy)
    resolved = {}
    missing: list = []

    def _record(field: str, value, source, missing_entry=None) -> None:
        resolved[field] = (value, source)
        if missing_entry:
            missing.append(missing_entry)

    _record(constants.FIELD_DESTINATION, *_resolve_required_field(
        args, constants.FIELD_DESTINATION, "--destination", constants.FIVETRAN_DESTINATION_NAME_ENV,
        get_destination_group, profile, profile_label))
    _record(constants.FIELD_CONNECTION, *_resolve_required_field(
        args, constants.FIELD_CONNECTION, "--connection", constants.FIVETRAN_CONNECTION_NAME_ENV,
        get_connection_name, profile, profile_label))

    is_new_connection, group_id, current_detail = True, None, None
    if resolved[constants.FIELD_DESTINATION][0] and resolved[constants.FIELD_CONNECTION][0]:
        is_new_connection, group_id, current_detail = _lookup_connection_context(
            resolved[constants.FIELD_DESTINATION][0], resolved[constants.FIELD_CONNECTION][0], deploy_key, group_ids)
    # The migration-period required-field rule treats an existing connection like a new one for
    # the one-time deploy that just created the options file -- see the docstring above.
    treat_as_new = is_new_connection or is_first_migration_deploy

    _record(constants.FIELD_PYTHON_VERSION, *_resolve_python_version(args, prompt_mode, profile, profile_label, treat_as_new))
    _record(constants.FIELD_HYBRID_DEPLOYMENT_AGENT_ID, *_resolve_hd_agent_id(
        args, prompt_mode, profile, profile_label, treat_as_new, group_id, current_detail, deploy_key))

    resolved[constants.FIELD_PROXY_ID], resolved[constants.FIELD_PROXY_HOST_CONFIG_KEY] = _resolve_proxy_fields(
        args, profile, profile_label, current_detail)
    resolved[constants.FIELD_PACKAGE_ID] = _resolve_package_id(args, profile, profile_label)
    resolved[constants.FIELD_NAMING] = _resolve_naming(args, profile, profile_label, is_new_connection)

    if missing:
        _report_missing_and_exit(missing, profile_label, args, options_data, deploy_key, group_ids)

    _log_resolved_summary(resolved, options_path)
    _warn_on_server_drift(resolved, current_detail)

    return {field: value for field, (value, source) in resolved.items()}
