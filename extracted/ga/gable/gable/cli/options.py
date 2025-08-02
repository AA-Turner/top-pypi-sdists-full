import functools
import re
import sys
import traceback
from typing import List, Literal, Optional

import click
from click_option_group import OptionGroup, optgroup
from gable.cli.client import GableCliClient
from gable.cli.helpers.logging import configure_debug_logger, configure_trace_logger
from gable.cli.helpers.multi_option import MultiOption
from gable.cli.option_defaults import (
    DEFAULT_NUM_RECENT_FILES_TO_SAMPLE,
    DEFAULT_NUM_ROWS_TO_SAMPLE,
)
from gable.common_types import DATABASE_SOURCE_TYPES, FILE_SOURCE_TYPES
from gable.openapi import SourceType
from loguru import logger

TypescriptLibrary = Literal["brandviews", "segment", "amplitude", "udf"]
ALL_TYPESCRIPT_LIBRARY_VALUES: List[TypescriptLibrary] = [
    "brandviews",
    "segment",
    "amplitude",
    "udf",
]


class Context:
    def __init__(self):
        self.client: Optional[GableCliClient] = None


def help_option(func):
    """Re-adds the help option, which fixes the eagerness issue with required parameters... Without this, if a parameter
    is marked as required, <command> --help will fail because the required parameters are not provided.
    """

    @click.help_option(is_eager=True)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def endpoint_options(func, global_option_group: OptionGroup):
    """Decorator that adds global endpoint options to a command. This decorator is added by the below global_options
    decorator, so it should not be used directly"""

    @global_option_group.option(
        "--endpoint",
        help="Customer API endpoint for Gable, in the format https://api.company.gable.ai/. Can also be set with the GABLE_API_ENDPOINT environment variable.",
    )
    @global_option_group.option(
        "--api-key",
        help="API Key for Gable. Can also be set with the GABLE_API_KEY environment variable.",
    )
    @functools.wraps(func)
    @click.pass_context
    def wrapper(ctx: click.Context, endpoint=None, api_key=None, *args, **kwargs):
        if ctx.obj is None:
            ctx.obj = Context()
        if ctx.obj.client is None:
            ctx.obj.client = GableCliClient()

        # allow users to do something like `gable --endpoint abc data-asset list --api-key 123`
        if not ctx.obj.client.api_key and api_key:
            ctx.obj.client.api_key = api_key
        if not ctx.obj.client.endpoint and endpoint:
            ctx.obj.client.endpoint = endpoint
        if ctx.invoked_subcommand is None:
            # if there are no more subcommands, the client must be valid by now
            try:
                ctx.obj.client.validate_api_key()
                ctx.obj.client.validate_endpoint()
                ctx.obj.client.get_ping()
                logger.debug(
                    f"Created Gable client with endpoint {ctx.obj.client.endpoint}"
                )
            except Exception as e:
                raise click.ClickException(f"Failed to connect to Gable API: {e}")

        return func(*args, **kwargs)

    return wrapper


def logging_options(func, global_option_group: OptionGroup):
    """Decorator that adds global logging options to a command. This decorator is added by the below global_options
    decorator, so it should not be used directly"""

    @global_option_group.option(
        "--debug",
        help="Enable debug logging",
        is_flag=True,
        default=False,
        # Make eager so we can configure logging before the other options are parsed
        is_eager=True,
        # Unintuitive, but we need to set this to true even though we don't actually want to pass this value to the
        # subcommand functions. We need this in the below function wrapper to determine if we should log detailed
        # exception information. This will be stripped out of the kwargs before they are passed to the subcommand
        expose_value=True,
        callback=configure_debug_logger,
    )
    @global_option_group.option(
        "--trace",
        help="Enable trace logging. This is the most verbose logging level and should only be used for debugging.",
        is_flag=True,
        default=False,
        # Make eager so we can configure logging before the other options are parsed
        is_eager=True,
        # Unintuitive, but we need to set this to true even though we don't actually want to pass this value to the
        # subcommand functions. We need this in the below function wrapper to determine if we should log detailed
        # exception information. This will be stripped out of the kwargs before they are passed to the subcommand
        expose_value=True,
        callback=configure_trace_logger,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if debug logging is enabled
        debug_logging_enabled = "debug" in kwargs and kwargs["debug"]
        trace_logging_enabled = "trace" in kwargs and kwargs["trace"]
        # We need to remove the debug/trace flags from the kwargs before passing them to the subcommand functions
        # because they don't expect it
        if "debug" in kwargs:
            del kwargs["debug"]
        if "trace" in kwargs:
            del kwargs["trace"]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if debug_logging_enabled or trace_logging_enabled:
                # If trace logging is enabled, log the full exception information
                if trace_logging_enabled:
                    logger.exception(traceback.format_exc())
                # Otherwise, just log the exception message
                else:
                    logger.exception(str(e))
                # Then immediately exit to prevent the default click exception handler from printing the exception
                # again. If this is a ClickException, grab the exit code and use that, otherwise use 1
                exit_code = e.exit_code if isinstance(e, click.ClickException) else 1
                # The context should always be available here, but just in case it isn't use sys.exit() instead
                context = click.get_current_context(silent=True)
                if context:
                    context.exit(exit_code)
                sys.exit(exit_code)
            # If debug logging is not enabled, just raise the exception and let the default click exception handler
            # print it
            raise e

    return wrapper


def global_options(add_endpoint_options=True):
    """Decorator that adds global options to a command. This decorator should be applied to all commands to add the
    --debug/--trace options, and conditionally (though almost always) add the --endpoint/--api-key options.
    """

    def decorate(func):
        func = help_option(func)
        global_option_group = OptionGroup("Global Options")
        func = logging_options(func, global_option_group)
        if add_endpoint_options:
            # Return the function unchanged, not decorated.
            func = endpoint_options(func, global_option_group)

        return func

    return decorate


def required_option_callback(ctx, param, value):
    """This callback is used to enforce required options when the option needs to be eager, which can cause problems
    with the --help flag"""
    if not value or str(value).strip() == "":
        raise click.MissingParameter(ctx=ctx, param=param)
    return value


def check_for_empty_string_callback(ctx, param, value):
    """This callback is used to check for optional options that were specified, but might be an empty string"""
    if value != None and str(value).strip() == "":
        raise click.BadParameter("Cannot be an empty string", ctx=ctx, param=param)
    return value


def source_type_dependent_required_option_callback(ctx, param, value):
    """
    This callback is used to conditionally enforce option requirements based on the source type.
    It also checks if the correct number of include patterns is provided when the source type requires historical data comparison.

    Args:
        ctx: Click context, which holds all the parameters and their values.
        param: The parameter currently being processed.
        value: The value of the parameter.

    Raises:
        click.MissingParameter: If a required parameter is missing.
        click.BadParameter: If an unexpected value is processed.
        ValueError: If incorrect number of include patterns are provided for historical analysis.

    Returns:
        The value if no errors are raised.
    """
    source_type: SourceType = SourceType(ctx.params.get("source_type"))

    if source_type in DATABASE_SOURCE_TYPES:
        # Only require the options for the database source type
        if param.group.name == "Database Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type in FILE_SOURCE_TYPES:
        # Only require the options for the file source type
        if param.group.name == "Protobuf & Avro options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type == SourceType.python:
        if param.group.name == "Python Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
        python_event_name_key_validator(param, value)
    elif source_type == SourceType.pyspark:
        if param.group.name == "Pyspark Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type == SourceType.typescript:
        if param.group.name == "Typescript Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
    elif source_type == SourceType.s3:
        if param.group.name == "S3 Project Options" and not value:
            raise click.MissingParameter(ctx=ctx, param=param)
        if param.name == "include" and (not value or len(value) != 2):
            raise click.BadParameter(
                "Exactly two include patterns are required for historical data asset detection.",
                ctx=ctx,
                param=param,
            )
    else:
        # Should never happen, but just in case
        raise click.BadParameter("", ctx=ctx, param=param)
    return value


PYTHON_EVENT_NAME_KEY_REGEX = (
    r"^(\w+|\*|\[\*\]|\[-?[0-9]+\])(\.(\w+|\[\*\]|\[-?[0-9]+\]))*\w+$"
)


def python_event_name_key_validator(param: click.Parameter, value: str) -> None:
    # Event name key must be a valid access path:
    # 1. The string can start with a word (letters, digits, underscores), *, [*], or [<index>].
    # 2. If there is a dot separator, it should be followed by a word, [*], or [<index>]. This process can repeat (zero or more times).
    # 3. The string must end with a word.
    if param.opts[0] == "--event-name-key" and not re.match(
        PYTHON_EVENT_NAME_KEY_REGEX, value
    ):
        raise click.BadParameter(value + " must be valid event name access path")


@logger.catch()
def python_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds Python project related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Python Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--project-root",
            help="This should be the directory location of the Python project that will be analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--emitter-function",
            help="Name of the emitter function",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--emitter-payload-parameter",
            help="Name of the parameter representing the event payload",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--event-name-key",
            help="Input must be a \".\" delimited list of field property access directives or array indexes to the event name key field. The field property access directive is a valid dictionary key, or the wildcard character *. The array index is square brackets[] with either a digit in it (targeting a specific element of the array), or * (targeting all elements in the array).\n\nExample: \"fieldName.[0].eventName\" describes the access pay to the event name in: {'fieldName': [{'eventName': 'event_one'}]}.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--emitter-file-path",
            help="Relative path from the root of the project to the file that contains the emitter function",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--exclude",
            help="Comma separated list of paths to be excluded from the analysis, with support for glob patterns. Gable automatically excludes '**/node_modules, **/__pycache__, **/.*'. Example: '**/tests,docs/*'",
            type=str,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def pyspark_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds Pyspark project related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):

        @optgroup.group(
            "Pyspark Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--project-root",
            help="This should be the directory location of the project containing the Pyspark job that will analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--spark-job-entrypoint",
            help='Entrypoint to execute spark job, starting with python file and including any arguments. Example: "main.py --arg1 value1 --arg2 value2"',
            type=str,
            default=None,
        )
        @optgroup.option(
            "--connection-string",
            help="Connection string to Hive cluster used to pull schemas of input tables",
            type=str,
            default=None,
        )
        @optgroup.option(
            "--metastore-connection-string",
            help="Connection string to the Hive metastore used to pull S3 to table mappings",
            type=str,
            default=None,
        )
        @optgroup.option(
            "--csv-schema-file",
            help="Path to the CSV schema file",
            type=str,
            default=None,
        )
        @optgroup.option(
            "--csv-path-to-table-file",
            help="Path to a CSV schema file containing a mapping of Delta table paths to table names",
            type=str,
            default=None,
        )
        @optgroup.option(
            "--config-file",
            help="Path to YAML configuration file containing the necessary configurations for the Pyspark job.",
            type=click.File(),
            default=None,
        )
        @optgroup.option(
            "--config-entrypoint-path",
            help="The path to the property of the YAML config file containing the spark job entrypoint, which is the main Python script for the job. For example: 'spec.mainApplicationFile'",
            type=str,
            default=None,
        )
        @optgroup.option(
            "--config-args-path",
            help="The path to the property of the YAML config file containing the spark job arguments. For example: 'spec.arguments'",
            type=str,
            default=None,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def file_source_type_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds file source type (protobuf, avro, etc) related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Protobuf & Avro options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--files",
            help=f"Space delimited path(s) to the assets to {action}, with support for glob patterns.",
            type=tuple,
            callback=source_type_dependent_required_option_callback,
            cls=MultiOption,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def typescript_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds Typescript project related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):

        @optgroup.group(
            "Typescript Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--project-root",
            help="This should be the directory location of the Typescript project that will be analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--library",
            help="This should indicate the library emitting the events you want detected as data assets.",
            type=click.Choice(ALL_TYPESCRIPT_LIBRARY_VALUES),
        )
        @optgroup.option(
            "--node-modules-include",
            help="Comma delimited list of filenames or patterns of node modules to include in the analysis.",
            type=str,
        )
        @optgroup.option(
                "--emitter-file-path",
                help="DEPRECATED: Use --emitter-location instead.",
                type=str,
            )
        @optgroup.option(
            "--emitter-location",
            help="NPM package name, or relative path from the root of the project to the file that contains the emitter function",
            type=str,
        )
        @optgroup.option(
            "--emitter-function",
            help="Name of the emitter function. This can be a standalone function like 'trackEvent' or a class method like 'AnalyticsClient.track'",
            type=str,
        )
        @optgroup.option(
            "--emitter-payload-parameter",
            help="Name of the parameter representing the event payload",
            type=str,
        )
        @optgroup.option(
            "--emitter-name-parameter",
            help="Name of the emitter function parameter that contains the event name. Either this option, or the --event-name-key option must be provided when using --emitter-function.",
            type=str,
        )
        @optgroup.option(
            "--event-name-key",
            help="Name of the event property that contains the event name. Either this option, or the --emitter-name-parameter option must be provided when using --emitter-function.",
            type=str,
        )
        @optgroup.option(
                "--exclude",
                help="Comma delimited list of filenames or extended globbing patterns of node modules to include in the analysis. Defaults toexclude common test patterns like *.test.js, *.spec.js, etc.",
                type=str,
                # TODO: Removed the default value until the new SCA tool will be released that supports this option.
                #default="**/*.@(test|spec).@(js|jsx|ts|tsx|mjs|mts|cjs|cts),**/@(test|tests|spec)/**",
                #show_default=True,
                default=None,
            )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def proxy_database_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds database + proxy database related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):
        @optgroup.group(
            "Database Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--host",
            "-h",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help="""The host name of the production database, for example 'service-one.xxxxxxxxxxxx.us-east-1.rds.amazonaws.com'.
            Despite not needing to connect to the production database, the host is still needed to generate the unique resource
            name for the real database tables (data assets).
            """,
        )
        @optgroup.option(
            "--port",
            "-p",
            type=int,
            callback=source_type_dependent_required_option_callback,
            help="""The port of the production database. Despite not needing to connect to the production database, the port is
            still needed to generate the unique resource name for the real database tables (data assets).
            """,
        )
        @optgroup.option(
            "--db",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help="""The name of the production database. Despite not needing to connect to the production database, the database
            name is still needed to generate the unique resource name for the real database tables (data assets).

            Database naming convention frequently includes the environment (production/development/test/staging) in the
            database name, so this value may not match the name of the database in the proxy database instance. If this is
            the case, you can set the --proxy-db value to the name of the database in the proxy instance, but we'll use the
            value of --db to generate the unique resource name for the data asset.

            For example, if your production database is 'prod_service_one', but your test database is 'test_service_one',
            you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.""",
        )
        @optgroup.option(
            "--schema",
            "-s",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help=f"""The schema of the production database containing the table(s) to {action}. Despite not needing to connect to
            the production database, the schema is still needed to generate the unique resource name for the real database tables
            (data assets).

            Database naming convention frequently includes the environment (production/development/test/staging) in the
            schema name, so this value may not match the name of the schema in the proxy database instance. If this is
            the case, you can set the --proxy-schema value to the name of the schema in the proxy instance, but we'll use the
            value of --schema to generate the unique resource name for the data asset.

            For example, if your production schema is 'production', but your test database is 'test',
            you would set --schema to 'production' and --proxy-schema to 'test'.""",
        )
        @optgroup.option(
            "--table",
            "--tables",
            "-t",
            type=str,
            callback=check_for_empty_string_callback,
            default=None,
            help=f"""A comma delimited list of the table(s) to {action}. If no table(s) are specified, all tables within the provided schema will be {action}ed.

            Table names in the proxy database instance must match the table names in the production database instance, even if
            the database or schema names are different.""",
        )
        @optgroup.option(
            "--proxy-host",
            "-ph",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help=f"""The host string of the database instance that serves as the proxy for the production database. This is the
            database that Gable will connect to when {action}ing tables in the CI/CD workflow.
            """,
        )
        @optgroup.option(
            "--proxy-port",
            "-pp",
            type=int,
            callback=source_type_dependent_required_option_callback,
            help=f"""The port of the database instance that serves as the proxy for the production database. This is the
            database that Gable will connect to when {action}ing tables in the CI/CD workflow.
            """,
        )
        @optgroup.option(
            "--proxy-db",
            "-pdb",
            type=str,
            callback=check_for_empty_string_callback,
            default=None,
            help="""Only needed if the name of the database in the proxy instance is different than the name of the
            production database. If not specified, the value of --db will be used to generate the unique resource name for
            the data asset.

            For example, if your production database is 'prod_service_one', but your test database is 'test_service_one',
            you would set --db to 'prod_service_one' and --proxy-db to 'test_service_one'.
            """,
        )
        @optgroup.option(
            "--proxy-schema",
            "-ps",
            type=str,
            callback=check_for_empty_string_callback,
            default=None,
            help="""Only needed if the name of the schema in the proxy instance is different than the name of the schema in the
            production database. If not specified, the value of --schema will be used to generate the unique resource name for
            the data asset.

            For example, if your production schema is 'production', but your test database is 'test', you would set --schema to
            'production' and --proxy-schema to 'test'.
            """,
        )
        @optgroup.option(
            "--proxy-user",
            "-pu",
            type=str,
            callback=source_type_dependent_required_option_callback,
            help=f"""The user that will be used to connect to the proxy database instance that serves as the proxy for the production
            database. This is the database that Gable will connect to when {action}ing tables in the CI/CD workflow.
            """,
        )
        @optgroup.option(
            "--proxy-password",
            "-ppw",
            type=str,
            default=None,
            help=f"""If specified, the password that will be used to connect to the proxy database instance that serves as the proxy for
            the production database. This is the database that Gable will connect to when {action}ing tables in the CI/CD workflow.
            """,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@logger.catch()
def s3_project_options(
    option_group_help_text: str, action: Literal["register", "check"]
):
    """Decorator that adds S3 related options to a command like 'data-asset register'.

    The 'action' option is used to tweak the help text depending on the command being run. If a new value is
    added, make sure it works as {action}ed and {action}ing (e.g. registered and registering, checked and checking)
    """

    def decorator(func):

        @optgroup.group(
            "S3 Project Options",
            help=option_group_help_text,
        )
        @optgroup.option(
            "--bucket",
            help="This should indicate the S3 bucket containing the files to be analyzed.",
            callback=source_type_dependent_required_option_callback,
            type=str,
        )
        @optgroup.option(
            "--include-prefix",
            help="This optional parameter allows you to specify what to include in your S3 bucket. If not specified, all files in the bucket will be analyzed.",
            multiple=True,
        )
        @optgroup.option(
            "--exclude-prefix",
            help="This optional parameter allows you to specify what to exclude in your S3 bucket. If --include-prefix is specified, this parameter must be a subset of include to be considered.",
            multiple=True,
        )
        @optgroup.option(
            "--lookback-days",
            type=int,
            default=2,
            help="""Number of days to look back from the latest day in the list of paths, defaults to 2.
            For example if the latest path is 2024/01/02, and lookback_days is 3, then the paths return
            will have 2024/01/02, 2024/01/01, and 2023/12/31
            """,
        )
        @optgroup.option(
            "--history",
            help="This optional parameter allows you to do a historical analysis between 2 dates.",
            type=bool,
            is_flag=True,
            default=False,
        )
        @optgroup.option(
            "--skip-profiling",
            help="This optional parameter allows you to turn off data profiling.",
            type=bool,
            is_flag=True,
            default=False,
        )
        @optgroup.option(
            "--row-sample-count",
            type=int,
            default=DEFAULT_NUM_ROWS_TO_SAMPLE,
            help=f"""Number of rows of data per file to sample for schema detection and data profiling. Default is {DEFAULT_NUM_ROWS_TO_SAMPLE}.
            Accuracy increases with larger sample size, but processing time and AWS costs also increases.
            """,
        )
        @optgroup.option(
            "--recent-file-count",
            type=click.IntRange(min=1),
            default=DEFAULT_NUM_RECENT_FILES_TO_SAMPLE,
            help=f"""Specifies the number of most recent files whose schema will be used for inference per data asset.
            Default is {DEFAULT_NUM_RECENT_FILES_TO_SAMPLE}. For example, if the latest file is 2024/01/10 and `--recent-file-count` is 2,
            then only files 2024/01/10 and 2024/01/09 will be used for schema inference, even if --lookback-days is greater than 2.
            Increase this value to improve schema accuracy over more schema history, at the cost of increased runtime. Must be at least 1.
            """,
        )
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if action == "register":
            wrapped = optgroup.option(
                "--use-inventory",
                is_flag=True,
                default=False,
                help="Enable S3 Inventory-based discovery instead of listing files live from S3.",
            )(wrapper)

            wrapped = optgroup.option(
                "--inventory-dir",
                type=str,
                help="Local directory or S3 URI where inventory .csv.gz files are stored. Used when --use-inventory is enabled.",
            )(wrapped)

        return functools.wraps(func)(wrapper)

    return decorator
