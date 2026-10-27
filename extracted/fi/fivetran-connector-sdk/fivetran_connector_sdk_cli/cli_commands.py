import os
import sys
from http import HTTPStatus
from typing import Callable, Optional

from fivetran_connector_sdk_common import __version__, constants
from fivetran_connector_sdk_cli.initialisation_helper import init
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_common.constants import DEPRECATED_FORCE_FLAG_WARNING, DEFAULT_PYTHON_VERSION, PYPROJECT_TOML
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_cli.cli_helpers import (
    state_file_to_update,
    telemetry,
    reset_local_file_directory,
    find_connector_object,
    PromptMode,
    resolve_confirmation,
    _resolve_existing_project_path,
    enable_debugging_for_verbose_commands
)
from fivetran_connector_sdk_cli.cli_parser import create_argument_parser, intercept_unknown_command
from fivetran_connector_sdk_cli.connector_helper import (
    validate_requirements_file,
    validate_pyproject_file,
    package_project,
    create_package,
    update_connection,
    get_connection_details,
    create_connection,
    get_group_info,
    update_base_url_if_required,
    check_newer_version,
    get_api_key,
    get_state,
    get_naming,
    get_configuration,
    get_destination_settings,
    validate_proxy_configuration,
    handle_connection_response,
    validate_required_deploy_params,
    validate_configuration,
    get_update_prompt,
    get_rebind_prompt,
    validate_required_package_params,
    validate_package_dependencies,
    package_create,
    package_update,
    package_list,
    get_connection_package_id,
    is_package_shared,
    get_package,
    validate_connection_package_update,
    DeployOptions,
    safe_option_names_from_argv,
    attempted_command_for_telemetry
)
from fivetran_connector_sdk_common.configuration import check_dict
from fivetran_connector_sdk_cli.options_file import find_options_file, default_options_file_path, is_options_file_supported
from fivetran_connector_sdk_cli.migration import run_migration, write_resolved_profile
from fivetran_connector_sdk_cli.resolution import resolve_deploy_options

def package(
        project_path: str,
        prompt_mode: PromptMode = PromptMode.INTERACTIVE,
        configuration_form_method: Optional[Callable] = None):
    """Packages the connector project into a distributable zip file.

    Args:
        project_path (str): The path to the connector project directory.
        prompt_mode (PromptMode): Controls how prompts are answered. Defaults to INTERACTIVE.
        configuration_form_method: Optional callable returning a ConfigurationForm instance.
    """
    validate_package_dependencies(project_path, prompt_mode)
    package_path = create_package(project_path, configuration_form_method)
    print_library_log(f"package created at: {package_path}", log_icon=Logging.LogIcon.SUCCESS)
    sys.exit(0)


def _deploy_connector(project_path: Optional[str], deploy_key: str, group: str, connection: str,
                      hd_agent_id: str, options: DeployOptions = None,
                      configuration_form_method: Optional[Callable] = None):
    """Implements `Connector.deploy()`; also called directly by the CLI for `--package-id`,
    which needs neither a local project nor a Connector instance since packaging is skipped.

    project_path and configuration_form_method are only used on the local-packaging path
    (no target_package_id), so both may be None when target_package_id is set.
    """
    options = options or DeployOptions()
    (configuration, config_path, python_version, prompt_mode, naming, proxy_id, proxy_host_config_key,
     target_package_id) = (options.configuration, options.config_path, options.python_version, options.prompt_mode,
                            options.naming, options.proxy_id, options.proxy_host_config_key, options.target_package_id)
    constants.EXECUTED_VIA_CLI = True
    print_library_log("executing deploy:")
    deploy_cmd = f"fivetran deploy --destination {group} --connection {connection} --api-key {deploy_key[0:8]}******** "
    if config_path:
        deploy_cmd += f"--configuration {config_path} "
    if python_version:
        deploy_cmd += f"--python-version {python_version} "
    if hd_agent_id:
        deploy_cmd += f"--hybrid-deployment-agent-id {hd_agent_id} "
    if proxy_id:
        deploy_cmd += f"--proxy-id {proxy_id} "
    if proxy_host_config_key:
        deploy_cmd += f"--proxy-host-config-key {proxy_host_config_key} "
    if naming:
        deploy_cmd += f"--naming {naming} "
    if target_package_id:
        deploy_cmd += f"--package-id {target_package_id} "
    if prompt_mode.value:
        deploy_cmd += prompt_mode.value
    print_library_log(deploy_cmd)

    check_newer_version(__version__)

    resolved_proxy_host_config_key = validate_proxy_configuration(
        configuration or {}, proxy_id, proxy_host_config_key, hd_agent_id)
    check_dict(configuration, True, {resolved_proxy_host_config_key} if resolved_proxy_host_config_key else None, allow_null_value=True)

    secrets_list = []
    if configuration:
        for k, v in configuration.items():
            secrets_list.append({"key": k, "value": v})

    connection_config = {
        "schema": connection,
        "secrets_list": secrets_list,
    }

    if python_version:
        connection_config["python_version"] = python_version
    if resolved_proxy_host_config_key:
        connection_config["proxy_host_config_key"] = resolved_proxy_host_config_key

    if not target_package_id:
        if prompt_mode != PromptMode.FORCE:
            pyproject_path = os.path.join(project_path, PYPROJECT_TOML)
            if os.path.exists(pyproject_path):
                validate_pyproject_file(project_path, True, prompt_mode)
            else:
                validate_requirements_file(project_path, True, __version__, prompt_mode)
        else:
            print_library_log(f"skipping dependency validation; {prompt_mode.value} is set")
    else:
        print_library_log(f"package-id '{target_package_id}' will be reused")

    group_id, group_name = get_group_info(group, deploy_key)
    connection_id, service = get_connection_details(connection, group, group_id, deploy_key) or (None, None)

    if target_package_id:
        print_library_log(f"validating package {target_package_id}", log_icon=Logging.LogIcon.STEP)
        if get_package(target_package_id, deploy_key) is None:
            print_library_log(f"package-id not found: {target_package_id}", level=Logging.Level.SEVERE,
                              log_icon=Logging.LogIcon.FAILURE)
            sys.exit(1)
        print_library_log("package found", log_icon=Logging.LogIcon.SUCCESS)

    if connection_id:
        if naming:
            print_library_log("ignored --naming flag; naming strategy cannot be changed after connection creation", Logging.Level.WARNING)
        if service != 'connector_sdk':
            print_library_log(
                f"cannot update connection '{connection}'; not a Connector SDK connection", level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
            sys.exit(1)

        current_package_id = get_connection_package_id(connection_id, deploy_key)
        validate_connection_package_update(connection, current_package_id, target_package_id, deploy_key)
        left_shared_package_group = False
        if target_package_id and current_package_id:
            left_shared_package_group = is_package_shared(current_package_id, deploy_key)

        if target_package_id:
            rebind_prompt = get_rebind_prompt(connection, group, target_package_id, configuration, config_path)
            should_update = resolve_confirmation(rebind_prompt, False, prompt_mode)
        else:
            update_prompt = get_update_prompt(connection, group, configuration, config_path)
            should_update = resolve_confirmation(update_prompt, False, prompt_mode)

        if should_update:
            if target_package_id:
                print_library_log(f"updating connection {connection} in group {group_name} to use package {target_package_id}", log_icon=Logging.LogIcon.STEP)
            else:
                print_library_log(f"updating connection {connection} in group {group_name}", log_icon=Logging.LogIcon.STEP)
            package_id = target_package_id or package_project(project_path, deploy_key, configuration_form_method)
            response = update_connection(connection_id, connection, group_name, connection_config, package_id, deploy_key, hd_agent_id, proxy_id)
            handle_connection_response(response, package_id, deploy_key, HTTPStatus.OK.value, is_new_connection=False,
                                       connection_id=connection_id, cleanup_package_on_failure=not bool(target_package_id))
            if target_package_id and left_shared_package_group:
                print_library_log(
                    f"connection '{connection}' left previous package group '{current_package_id}'",
                    log_icon=Logging.LogIcon.INFO)
        else:
            print_library_log("update cancelled", log_icon=Logging.LogIcon.FAILURE)
            sys.exit(1)
    else:
        validate_configuration(configuration)
        if not python_version:
            print_library_log(
                f"python version not specified; connection will use the default python version ({DEFAULT_PYTHON_VERSION})")
            print_library_log(
                "set --python-version <version> in the deploy command or update it in your Fivetran dashboard")
        package_id = target_package_id or package_project(project_path, deploy_key, configuration_form_method)
        response = create_connection(deploy_key, group_id, connection_config, hd_agent_id, package_id, naming, proxy_id)
        handle_connection_response(response, package_id, deploy_key, HTTPStatus.CREATED.value, is_new_connection=True,
                                   cleanup_package_on_failure=not bool(target_package_id))

def print_version():
    print_library_log("fivetran_connector_sdk " + __version__)
    sys.exit(0)


def _run_deploy_command(args, prompt_mode: PromptMode) -> None:
    """Handles the `fivetran deploy` command. With a resolved package_id (from --package-id, an
    env var, or an options-file profile), reuses an existing package and skips local
    packaging/upload, so (unlike a standard deploy) it needs no local connector.py; the project
    path is still resolved, only to look up a configuration.json fallback.
    """
    ft_deploy_key = get_api_key(args)
    validate_required_package_params(ft_deploy_key)

    try:
        args.project_path = _resolve_existing_project_path(args.project_path)
    except ValueError as e:
        print_library_log(str(e), level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
        sys.exit(1)

    if not is_options_file_supported():
        print_library_log(constants.OPTIONS_FILE_SKIP_MIN_PYTHON_MESSAGE)

    migrated_options_path = None
    if not find_options_file(args):
        migrated_options_path = run_migration(ft_deploy_key, default_options_file_path())

    group_ids: dict = {}
    resolved = resolve_deploy_options(args, prompt_mode, ft_deploy_key,
                                      is_first_migration_deploy=bool(migrated_options_path),
                                      group_ids=group_ids)
    ft_group = resolved["destination"]
    ft_connection = resolved["connection"]
    validate_required_deploy_params(ft_group=ft_group, ft_connection=ft_connection, ft_deploy_key=ft_deploy_key)
    python_version = resolved["python_version"]
    hd_agent_id = resolved["hybrid_deployment_agent_id"]
    proxy_id = resolved["proxy_id"]
    proxy_host_config_key = resolved["proxy_host_config_key"]
    configuration, config_path = get_configuration(args)
    get_state(args)
    naming = resolved["naming"]
    target_package_id = resolved["package_id"]

    connector_object = None
    if not target_package_id:
        connector_object = find_connector_object(args.project_path)
        if not connector_object:
            sys.exit(1)

    if migrated_options_path:
        # Only when migration itself ran this deploy: persists the final resolved values
        # (including any CLI/env override) for this one connection.
        group_id = group_ids.get(ft_group) or get_group_info(ft_group, ft_deploy_key)[0]
        write_resolved_profile(migrated_options_path, group_id, ft_connection, resolved)

    options = DeployOptions(
        configuration=configuration, config_path=config_path, python_version=python_version,
        prompt_mode=prompt_mode, naming=naming, proxy_id=proxy_id, proxy_host_config_key=proxy_host_config_key,
        target_package_id=target_package_id)

    try:
        if target_package_id:
            _deploy_connector(None, ft_deploy_key, ft_group, ft_connection, hd_agent_id, options)
        else:
            _deploy_connector(args.project_path, ft_deploy_key, ft_group, ft_connection, hd_agent_id, options,
                              configuration_form_method=connector_object.configuration_form_method)
    except Exception as e:
        print_library_log(f"deploy run failed with error: {str(e)}", level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
        sys.exit(1)

def _run_package_command(args, prompt_mode: PromptMode) -> None:
    """Handles all `fivetran package ...` subcommands. Resolves project_path and looks up
    connector.py only for subcommands that need local code (local package, create, update);
    `list` is an account-level operation and needs neither.
    """
    subcommand = args.subcommand

    if subcommand == "list":
        api_key = get_api_key(args)
        validate_required_package_params(api_key)
        package_list(api_key, args.limit)
        return

    try:
        args.project_path = _resolve_existing_project_path(args.project_path)
    except ValueError as e:
        print_library_log(str(e), level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
        sys.exit(1)

    connector_object = find_connector_object(args.project_path)
    if not connector_object:
        sys.exit(1)
    configuration_form_method = connector_object.configuration_form_method

    if subcommand is None:
        package(args.project_path, prompt_mode, configuration_form_method)
    elif subcommand == "create":
        api_key = get_api_key(args)
        validate_required_package_params(api_key)
        package_create(args.project_path, api_key, prompt_mode, configuration_form_method)
    elif subcommand == "update":
        api_key = get_api_key(args)
        validate_required_package_params(api_key)
        package_update(args.project_path, args.package_id, api_key, prompt_mode, configuration_form_method)

def _telemetry_command(args) -> str:
    if args.version:
        return "version"
    if not args.command:
        return "unknown"
    command = args.command.lower()
    return f"{command} {args.subcommand}" if command == "package" and args.subcommand else command


def _run_command(args, parser, prompt_mode: PromptMode) -> None:
    """Runs the parsed command. Always exits via sys.exit, so the caller's telemetry scope
    reports the exit code of every outcome, including early validation failures.
    """
    update_base_url_if_required()

    if args.command.lower() == "version":
        print_version()
    elif args.command.lower() == "init":
        check_newer_version(__version__)
        init(args.project_path, args.template, prompt_mode)
    elif args.command.lower() == "help":
        parser.print_help()
        sys.exit(0)
    elif args.command.lower() == "package":
        _run_package_command(args, prompt_mode)
        sys.exit(0)
    elif args.command.lower() == "deploy":
        _run_deploy_command(args, prompt_mode)
        sys.exit(0)

    try:
        args.project_path = _resolve_existing_project_path(args.project_path)
    except ValueError as e:
        print_library_log(str(e), level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
        sys.exit(1)

    if args.command.lower() == "reset":
        reset_local_file_directory(args, prompt_mode)
        sys.exit(0)

    connector_object = find_connector_object(args.project_path)

    if not connector_object:
        sys.exit(1)

    if args.command.lower() in ("debug", "run"):
        configuration, _ = get_configuration(args)
        state = get_state(args)
        state_path = state_file_to_update(args)
        naming = get_naming(args)
        writes_to_iceberg = args.command.lower() == "run"  # to the Iceberg catalog destination.json describes, not to a local DuckDB file
        destination_settings = get_destination_settings(args.project_path, args.destination_file) if writes_to_iceberg else None
        debug_environment = {
            "FIVETRAN_CONNECTION_ID": "test_connection_id",
            "FIVETRAN_DEPLOYMENT_MODEL": "local_debug",
            "FIVETRAN_GROUP_ID": "test_group_id",
            "FIVETRAN_CONNECTION_NAME": "test_connection_name",
        }
        try:
            os.environ.update(debug_environment)
            if writes_to_iceberg:
                connector_object.run(destination_settings, args.project_path, configuration, state, naming, state_path=state_path)
            else:
                connector_object.debug(args.project_path, configuration, state, naming, state_path=state_path)
        except Exception as e:
            what = "run" if writes_to_iceberg else "debug run"
            print_library_log(f"{what} failed error: {str(e)}", level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
            sys.exit(1)
        finally:
            for name in debug_environment:
                os.environ.pop(name, None)

    elif args.command.lower() == "configuration":
        try:
            connector_object.generate_configuration(args.project_path, run_tests=args.test,
                                                   disable_encryption=args.disable_encryption,
                                                   prompt_mode=prompt_mode)
        except Exception as e:
            print_library_log(f"configuration command failed error: {str(e)}", level=Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
            sys.exit(1)


def main():
    """The main entry point for the script.
    Parses command line arguments and passes them to connector object methods.
    """
    constants.EXECUTED_VIA_CLI = True
    # Show the one-time telemetry notice before any other output; no event is sent on this run.
    telemetry.is_telemetry_enabled()
    intercept_unknown_command()
    parser = create_argument_parser()
    try:
        args = parser.parse_args()
    except SystemExit as e:
        exit_code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        telemetry.send_cli_usage(attempted_command_for_telemetry(sys.argv[1:]),
                                 safe_option_names_from_argv(parser, sys.argv[1:]), exit_code, __version__)
        raise

    # One telemetry event per invocation, covering setup and validation as well as the command itself.
    with telemetry.track_cli_usage(_telemetry_command(args), safe_option_names_from_argv(parser, sys.argv[1:]),
                                   __version__, track_duration=True):
        enable_debugging_for_verbose_commands(args.command)
        try:
            prompt_mode = PromptMode.from_args(args.non_interactive, args.force, args.yes)
        except ValueError as e:
            print_library_log(str(e), Logging.Level.SEVERE, log_icon=Logging.LogIcon.FAILURE)
            sys.exit(1)
        if args.force:
            print_library_log(DEPRECATED_FORCE_FLAG_WARNING, Logging.Level.WARNING)

        if args.version:
            print_version()

        if not args.command:
            parser.print_help()
            sys.exit(1)

        _run_command(args, parser, prompt_mode)
