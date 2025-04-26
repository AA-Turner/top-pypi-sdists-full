import click

from montecarlodata.data_exports.data_exports import DataExportService
from montecarlodata.data_exports.fields import (
    ALERTS_DATA_EXPORT_NAME,
    ASSETS_DATA_EXPORT_NAME,
    EVENTS_DATA_EXPORT_NAME,
    FILE_SCHEME,
    MONITORS_DATA_EXPORT_NAME,
    S3_SCHEME,
    SCHEME_DELIM,
)
from montecarlodata.tools import add_common_options

# Shared command verbiage
GET_VERBIAGE = f"""
\b\n
DESTINATION is the path where the data will be written to.

Supported schemes:\n
    '{FILE_SCHEME}{SCHEME_DELIM}' - save Data Export locally.\n
    '{S3_SCHEME}{SCHEME_DELIM}' - save Data Export to S3.

Notice - Will overwrite a file if it exists in the path and create any missing directories or prefixes.
"""  # noqa: E501

# Options shared across commands
MINIMAL_GET_OPTIONS = [
    click.option(
        "--aws-profile",
        required=False,
        help="AWS profile to be used when uploading to S3.",
    ),
    click.option(
        "--dry",
        required=False,
        is_flag=True,
        help="Echo temporary presigned URL for the Data Export and quit.",
    ),
]

GET_OPTIONS = [click.argument("destination", required=True), *MINIMAL_GET_OPTIONS]


@click.group(help="Export your data.")
def export():
    """
    Group for any Data Export related subcommands
    """
    pass


@export.command(help="List Data Export details and availability.", name="list")
@click.pass_obj
def list_data_exports(ctx):
    DataExportService(
        config=ctx["config"],
        command_name="export list_data_exports",
    ).echo_data_exports()


@export.command(help=f"Export monitors data. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_monitors(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_monitors",
    ).get_data_export(data_export=MONITORS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Export assets data. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_assets(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_assets",
    ).get_data_export(data_export=ASSETS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Export alerts data. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_alerts(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_alerts",
    ).get_data_export(data_export=ALERTS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Export events data. {GET_VERBIAGE}")
@add_common_options(GET_OPTIONS)
@click.pass_obj
def get_events(ctx, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get_events",
    ).get_data_export(data_export=EVENTS_DATA_EXPORT_NAME, **kwargs)


@export.command(help=f"Export Monte Carlo objects. {GET_VERBIAGE}")
@add_common_options(MINIMAL_GET_OPTIONS)
@click.option(
    "--name",
    help="Type of objects to export. Names can be found "
    'via the list command (e.g. `MONITORS` from "Monitors (MONITORS)")',
    required=True,
)
@click.option(
    "--destination",
    help="Destination location to save the data.",
    required=True,
)
@click.pass_obj
def get(ctx, name, **kwargs):
    DataExportService(
        config=ctx["config"],
        command_name="export get",
    ).get_data_export(data_export=name, **kwargs)
