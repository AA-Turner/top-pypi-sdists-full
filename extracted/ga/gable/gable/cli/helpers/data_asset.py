import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, List, Optional, Tuple, TypedDict, cast

import click
import jsonref
from loguru import logger

from gable.api.client import GableAPIClient
from gable.cli.helpers.emoji import EMOJI
from gable.cli.helpers.npm import (
    prepare_npm_environment,
    run_sca_pyspark,
    run_sca_python,
    run_sca_typescript,
)
from gable.cli.helpers.repo_interactions import (
    get_git_repo_info,
    get_git_ssh_file_path,
    get_relative_file_path,
    strip_ssh_user,
)
from gable.cli.readers.dbapi import DbapiReader
from gable.cli.readers.file import read_file
from gable.common_types import DATABASE_SOURCE_TYPES
from gable.openapi import (
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetMissingAssetResponse,
    CheckDataAssetNoChangeResponse,
    CheckDataAssetNoContractResponse,
    CheckDataAssetResponse,
    EnforcementLevel,
    SourceType,
    StructuredDataAssetResourceName,
)


class EventAsset(TypedDict):
    eventName: str
    eventNamespace: str
    properties: dict[str, Any]


def validate_db_input_args(user: str, password: str, db: str) -> None:
    if user is None:
        raise ValueError("User (--proxy-user) is required for database connections")
    if password is None:
        raise ValueError(
            "Password (--proxy-password) is required for database connections"
        )
    if db is None:
        raise ValueError("Database (--proxy-db) is required for database connections")


def get_db_connection(
    source_type: SourceType, user: str, password: str, db: str, host: str, port: int
):
    if source_type == SourceType.postgres:
        try:
            from gable.cli.readers.postgres import create_postgres_connection

            return create_postgres_connection(user, password, db, host, port)
        except ImportError:
            raise ImportError(
                "The psycopg2 library is not installed. Run `pip install 'gable[postgres]'` to install it."
            )
    elif source_type == SourceType.mysql:
        try:
            from gable.cli.readers.mysql import create_mysql_connection

            return create_mysql_connection(user, password, db, host, port)
        except ImportError:
            raise ImportError(
                "The MySQLdb library is not installed. Run `pip install 'gable[mysql]'` to install it."
            )
    elif source_type == SourceType.mssql:
        try:
            from gable.cli.readers.mssql import create_mssql_connection

            return create_mssql_connection(user, password, db, host, port)
        except ImportError:
            raise ImportError(
                "The pymssql library is not installed. Run `pip install 'gable[mssql]'` to install it."
            )


def get_db_schema_contents(
    source_type: SourceType,
    connection: Any,
    schema: str,
    tables: Optional[list[str]] = None,
) -> list[dict[str, Any]]:
    reader = DbapiReader(connection=connection)
    return reader.get_information_schema(
        source_type=source_type, schema=schema, tables=tables
    )


def get_db_resource_name(
    source_type: SourceType, host: str, port: int, db: str, schema: str, table: str
) -> str:
    return f"{source_type.value}://{host}:{port}/{db}/{schema}/{table}"


def get_protobuf_resource_name(
    source_type: SourceType, namespace: str, message: str
) -> str:
    return f"{source_type.value}://{namespace}/{message}"


def get_avro_resource_name(source_type: SourceType, namespace: str, record: str) -> str:
    return f"{source_type.value}://{namespace}/{record}"


def get_schema_contents(
    source_type: SourceType,
    dbuser: str,
    dbpassword: str,
    db: str,
    dbhost: str,
    dbport: int,
    schema: str,
    tables: Optional[list[str]],
    files: list[str],
) -> list[str]:
    # Validate the source type arguments and get schema contents
    if source_type in ["postgres", "mysql", "mssql"]:
        validate_db_input_args(dbuser, dbpassword, db)
        connection = get_db_connection(
            source_type, dbuser, dbpassword, db, dbhost, dbport
        )
        return [
            json.dumps(
                get_db_schema_contents(source_type, connection, schema, tables=tables)
            )
        ]
    elif source_type in ["avro", "protobuf", "json_schema"]:
        schema_contents: list[str] = []
        for file in files:
            if source_type == "json_schema":
                file_path = Path(file).absolute()

                try:
                    # Resolve any local JSON references before sending the schema
                    with file_path.open() as file_contents:
                        result = jsonref.load(
                            file_contents,
                            base_uri=file_path.as_uri(),
                            jsonschema=True,
                            proxies=False,
                        )
                        schema_contents.append(jsonref.dumps(result))
                except Exception as exc:
                    # Log full stack trace with --debug flag
                    logger.opt(exception=exc).debug(
                        f"{file}: Error parsing JSON Schema file, or resolving local references: {exc}"
                    )
                    raise click.ClickException(
                        f"{file}: Error parsing JSON Schema file, or resolving local references: {exc}"
                    ) from exc
            else:
                schema_contents.append(read_file(file))
    else:
        raise NotImplementedError(f"Unknown source type: {source_type}")
    return schema_contents


def get_source_names(
    ctx: click.Context,
    source_type: SourceType,
    dbhost: str,
    dbport: int,
    files: list[str],
) -> list[str]:
    # Validate the source type arguments and get schema contents
    if source_type in ["postgres", "mysql", "mssql"]:
        return [f"{dbhost}:{dbport}"]
    elif source_type in ["avro", "protobuf", "json_schema"]:
        source_names = []
        for file in files:
            source_names.append(get_git_ssh_file_path(get_git_repo_info(file), file))
        return source_names
    else:
        raise NotImplementedError(f"Unknown source type: {source_type}")


def is_empty_schema_contents(
    source_type: SourceType,
    schema_contents: list[str],
) -> bool:
    if len(schema_contents) == 0 or (
        # If we're registering a database table the schema_contents array will contain
        # a stringified empty array, so we need to check for that
        source_type in DATABASE_SOURCE_TYPES
        and len(schema_contents) == 1
        and schema_contents[0] == "[]"  # type: ignore
    ):
        return True
    return False


def determine_should_block(
    check_data_assets_results: list[CheckDataAssetResponse],
) -> bool:
    """For detailed response from the /data-assets/check endpoint, determine if any of the contracts
    have violations and have their enforcement level set to BLOCK.
    """

    for result in check_data_assets_results:
        result = result.root
        if isinstance(result, CheckDataAssetDetailedResponse):
            if result.violations is not None and len(result.violations) > 0:
                if result.enforcementLevel == EnforcementLevel.BLOCK:
                    return True
        if isinstance(result, CheckDataAssetMissingAssetResponse):
            if result.contract.enforcementLevel == EnforcementLevel.BLOCK:
                return True
    return False


def format_check_data_assets_text_output(
    check_data_assets_results: list[CheckDataAssetResponse],
) -> str:
    """Format the console output for the gable data-asset check command with the '--output text' flag.
    Returns the full command output string.
    """
    results_strings = []
    contract_violations_found = False
    for result in check_data_assets_results:
        result = result.root
        if isinstance(result, CheckDataAssetDetailedResponse):
            # If there were violations, print them
            if result.violations is not None and len(result.violations) > 0:
                contract_violations_found = True
                violations_string = "\n\t".join(
                    [
                        f"{violation.field}: {violation.message}\n\tExpected: {violation.expected}\n\tActual: {violation.actual}"
                        for violation in result.violations
                    ]
                )
                results_strings.append(
                    f"{EMOJI.RED_X.value} {result.dataAssetPath}:{violations_string}"
                )
            else:
                # For valid contracts, just print the check mark and name
                results_strings.append(
                    f"{EMOJI.GREEN_CHECK.value} {result.dataAssetPath}: No contract violations found"
                )
        elif isinstance(result, CheckDataAssetMissingAssetResponse):
            contract_violations_found = True
            results_strings.append(
                f"{EMOJI.RED_X.value} Data asset {result.dataAssetPath} has a contract but seems to be missing!"
            )
        elif isinstance(result, CheckDataAssetErrorResponse):
            # If there was an error, print the error message
            results_strings.append(
                f"{EMOJI.RED_X.value} {result.dataAssetPath}:\n\t{result.message}"
            )
        elif isinstance(result, CheckDataAssetNoContractResponse):
            # For missing contracts print a warning
            results_strings.append(
                f"{EMOJI.YELLOW_WARNING.value} {result.dataAssetPath}: No contract found"
            )
        elif isinstance(result, CheckDataAssetNoChangeResponse):
            results_strings.append(
                f"{EMOJI.GREEN_CHECK.value} {result.dataAssetPath}: No changes in asset, skipping check"
            )
    return (
        "\n".join(results_strings)
        + "\n\n"
        + (
            "Contract violation(s) found"
            if contract_violations_found
            else "No contract violations found"
        )
    )


def format_check_data_assets_json_output(
    check_data_assets_results: list[CheckDataAssetResponse],
) -> str:
    """Format the console output for the gable data-asset check command with the '--output json' flag.
    Returns the full command output string.
    """
    # Convert the results to dicts by calling Pydantic's json() on each result to deal with enums, which
    # aren't serializable by default
    results_dict = [
        json.loads(result.root.json()) for result in check_data_assets_results
    ]
    return json.dumps(results_dict, indent=4, sort_keys=True)


def gather_pyspark_asset_data(
    project_root: str,
    spark_job_entrypoint: str,
    csv_schema_file: Optional[str],
    csv_path_to_table_file: Optional[str],
    connection_string: Optional[str],
    metastore_connection_string: Optional[str],
    client: GableAPIClient,
) -> Tuple[str, dict[str, dict[str, Any]]]:
    python_path = subprocess.run(["which", "python3"], capture_output=True, text=True)
    prepare_npm_environment(client)
    # Run SCA, get back the results
    sca_results = run_sca_pyspark(
        project_root=project_root,
        python_executable_path=os.path.abspath(
            python_path.stdout.strip()
        ),  # Get the absolute path if the python executable is from a virtual environment
        spark_job_entrypoint=spark_job_entrypoint,
        csv_schema_file=csv_schema_file,
        csv_path_to_table_file=csv_path_to_table_file,
        connection_string=connection_string,
        metastore_connection_string=metastore_connection_string,
    )
    return get_git_repo(project_root), get_event_schemas_from_sca_results(sca_results)


def gather_python_asset_data(
    project_root: str,
    emitter_file_path: str,
    emitter_function: str,
    emitter_payload_parameter: str,
    event_name_key: str,
    exclude_paths: Optional[str],
    client: GableAPIClient,
) -> Tuple[List[str], List[str]]:
    """Gathers the schema_contents and source_name for a Python-based data asset."""
    prepare_npm_environment(client)
    # Run SCA, get back the results
    sca_results = run_sca_python(
        project_root=project_root,
        emitter_file_path=emitter_file_path,
        emitter_function=emitter_function,
        emitter_payload_parameter=emitter_payload_parameter,
        event_name_key=event_name_key,
        exclude_paths=exclude_paths,
    )
    sca_results_dict = cast(
        dict[str, list[tuple[str, EventAsset, None]]], json.loads(sca_results)
    )
    # Assume only one key in the outer dict for now. The key is the emitter file path and function name
    _, sca_result_list = list(sca_results_dict.items())[0]
    # Filter out any undefined events, or events that are a string, which will happen
    # when the SCA returns "Unknown" for the event type
    sca_result_list = cast(
        list[EventAsset],
        [x for x in sca_result_list if x is not None and not isinstance(x, str)],
    )
    project_repo = get_git_repo_info(project_root + "/" + emitter_file_path)

    source_names = [f"{project_repo['gitSSHRepo']}" for x in sca_result_list]
    schema_contents = [json.dumps(x) for x in sca_result_list]
    return source_names, schema_contents


def gather_typescript_asset_data(
    library: Optional[str],
    node_modules_include: Optional[str],
    project_root: str,
    emitter_file_path: Optional[str],
    emitter_function: Optional[str],
    emitter_payload_parameter: Optional[str],
    emitter_name_parameter: Optional[str],
    event_name_key: Optional[str],
    client: GableAPIClient,
) -> Tuple[str, dict[str, dict[str, Any]]]:
    prepare_npm_environment(client)
    # Run SCA, get back the results
    (sca_results, sca_prime_results) = run_sca_typescript(
        library,
        node_modules_include,
        project_root,
        emitter_file_path,
        emitter_function,
        emitter_payload_parameter,
        event_name_key,
        emitter_name_parameter,
        None,  # No exclude paths for now
        client,
    )
    return get_git_repo(project_root), {
        **get_event_schemas_from_sca_results(sca_results),
        **sca_prime_results,
    }


def get_event_schemas_from_sca_results(sca_results: str) -> dict[str, dict[str, Any]]:
    try:
        # sca_results is a json string which should be an obj mapping event name to schema
        return json.loads(sca_results)

    except json.JSONDecodeError as exc:
        logger.opt(exception=exc).info(f"Error analyzing source code: {sca_results}")
        raise click.ClickException(
            f"Error analyzing source code: {sca_results}: {exc}"
        ) from exc


def get_git_repo(project_root: str) -> str:
    project_repo = get_git_repo_info(project_root)
    return f"{strip_ssh_user(project_repo['gitSSHRepo'])}"


def get_abs_project_root_path(project_root: str) -> str:
    absolute_path = os.path.abspath(project_root)
    if os.path.exists(absolute_path):
        return absolute_path
    else:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Project root is not valid directory."
        )


def get_relative_project_path(project_root: str) -> Tuple[str, str]:
    """Returns the name of the project directory, and the relative path of the project root in the git repository."""
    git_repo_info = get_git_repo_info(project_root)
    repo_root = os.path.abspath(git_repo_info["localRepoRootDir"])
    relative_project_root = get_relative_file_path(git_repo_info, project_root)
    project_name = os.path.basename(relative_project_root)
    return project_name, re.sub(
        r"^" + re.escape(repo_root), "", relative_project_root
    ).strip("/")


def darn_to_string(darn: StructuredDataAssetResourceName) -> str:
    return f"{darn.source_type.value}://{darn.data_source}:{darn.path}"


RECAP_TYPE_REGISTRY = None


def recap_type_to_dict(recap_type) -> dict[str, Any]:
    """
    Converts a RecapType to a dictionary

    Despite being called 'to_dict', this function can return a dictionary, a list or a
    string. This is a wrapper function to convert the output of to_dict() to a
    dictionary.

    This should take a RecapType, but we can't annotate the function because we want to only import that inside the function
    """
    from recap.types import RecapType, RecapTypeRegistry, alias_dict, to_dict

    recap_type_asserted: RecapType = recap_type

    global RECAP_TYPE_REGISTRY
    # Initialize this inside the function so we don't have to import the constructor at the top of the file
    RECAP_TYPE_REGISTRY = RECAP_TYPE_REGISTRY or RecapTypeRegistry()

    # Run alias_dict() separately so we can use a shared RecapTypeRegistry, otherwise
    # a new instance of the class is created for each call which kills performance
    recap_type_to_dict_output = to_dict(recap_type_asserted, True, False)
    if isinstance(recap_type_to_dict_output, list):
        type_dict = {"type": "union", "types": recap_type_to_dict_output}
    elif isinstance(recap_type_to_dict_output, str):
        type_dict = {"type": recap_type_to_dict_output}
    else:
        if recap_type_to_dict_output.get("type", None) is None:
            recap_type_to_dict_output["type"] = "unknown"
        type_dict = recap_type_to_dict_output
    type_dict = alias_dict(type_dict, RECAP_TYPE_REGISTRY)
    return type_dict
