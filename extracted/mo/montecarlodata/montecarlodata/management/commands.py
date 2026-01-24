import json

import click
from pycarlo.features.metadata.asset_filters_container import ASSET_TYPE_ATTRIBUTES

from montecarlodata.common import create_mc_client
from montecarlodata.management.service import ManagementService
from montecarlodata.tools import AdvancedOptions, convert_empty_str_callback


def _get_asset_types_help_text():
    """Generate help text listing supported resource types and their asset types."""
    lines = ["Supported asset types and attributes:"]
    for resource_type, asset_types in ASSET_TYPE_ATTRIBUTES.items():
        lines.append(f"  {resource_type}")
        for asset_type, attributes in asset_types.items():
            lines.append(f"    - {asset_type}: {', '.join(attributes)}")

    return "\n\n".join(lines)


@click.group(help="Manage account settings.")
def management():
    """
    Group for any management related subcommands
    """
    pass


@management.command(help="Get PII filtering preferences.")
@click.pass_obj
def get_pii_preferences(ctx):
    ManagementService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="management get_pii_preferences",
    ).get_pii_preferences()


@management.command(help="Configure PII filtering preferences for the account.")
@click.option(
    "--enable/--disable",
    "enabled",
    required=False,
    type=click.BOOL,
    default=None,
    help="Whether PII filtering should be active for the account.",
)
@click.option(
    "--fail-mode",
    required=False,
    type=click.Choice(["CLOSE", "OPEN"], case_sensitive=False),
    help="Whether PII filter failures will allow (OPEN) or prevent (CLOSE) data "
    "flow for this account.",
)
@click.pass_obj
def configure_pii_filtering(ctx, **kwargs):
    ManagementService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="management configure_pii_filtering",
    ).set_pii_filtering(**kwargs)


@management.command(help="List entities blocked from collection on this account.")
@click.option(
    "--resource-name",
    required=False,
    help="Name of a specific resource to filter by. Shows all resources by default.",
)
@click.pass_obj
def get_collection_block_list(ctx, **kwargs):
    ManagementService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="management get_collection_block_list",
    ).get_collection_block_list(**kwargs)


@management.command(help="Update entities for which collection is blocked on this account.")
@click.option(
    "--add/--remove",
    "adding",
    required=True,
    type=click.BOOL,
    default=None,
    help="Whether the entities being specified should be added or removed from the block list.",
)
@click.option(
    "--resource-name",
    "resource_name",
    help="Name of a specific resource to apply collection block to. "
    "Only warehouse names are supported for now.",
    cls=AdvancedOptions,
    mutually_exclusive_options=["filename"],
    required_with_options=["project"],
    at_least_one_set=["resource_name", "filename"],
)
@click.option(
    "--project",
    "project",
    help="Top-level object hierarchy e.g. database, catalog, etc.",
    cls=AdvancedOptions,
    mutually_exclusive_options=["filename"],
    required_with_options=["resource_name"],
)
@click.option(
    "--dataset",
    "dataset",
    default=None,
    callback=convert_empty_str_callback,
    required=False,
    help="Intermediate object hierarchy e.g. schema, database, etc.",
    cls=AdvancedOptions,
    mutually_exclusive_options=["filename"],
    required_with_options=["resource_name", "project"],
)
@click.option(
    "--collection-block-list-filename",
    "filename",
    help="Filename that contains collection block definitions. "
    "This file is expected to be in a CSV format with the headers resource_name, project, "
    "and dataset.",
    cls=AdvancedOptions,
    mutually_exclusive_options=["resource_name", "project", "dataset"],
)
@click.pass_obj
def update_collection_block_list(ctx, **kwargs):
    ManagementService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="management update_collection_block_list",
    ).update_collection_block_list(**kwargs)


@management.command(
    help=f"List asset collection preferences on this account. {_get_asset_types_help_text()}"
)
@click.option(
    "--resource-name",
    required=False,
    help="Name of a specific resource (warehouse or BI container) to filter by."
    "Shows all resources by default.",
)
@click.option(
    "--asset-type",
    required=False,
    help="Filter by specific asset type. Shows all asset types by default.",
)
@click.pass_obj
def get_asset_collection_preferences(ctx, **kwargs):
    ManagementService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="management get_asset_collection_preferences",
    ).get_asset_collection_preferences(**kwargs)


@management.command(
    help="Set asset collection preferences for a specific asset type on a resource."
    f" {_get_asset_types_help_text()}"
)
@click.option(
    "--resource-name",
    required=True,
    help="Name of the resource (warehouse or BI container) to configure.",
)
@click.option(
    "--asset-type",
    required=True,
    help="The type of asset to configure collection preferences for."
    " See command help for supported types.",
)
@click.option(
    "--default-effect",
    required=False,
    type=click.Choice(["allow", "block"], case_sensitive=False),
    help="Default action when no rules match: 'allow' to collect assets, 'block' to exclude them.",
)
@click.option(
    "--rules-json",
    required=False,
    help="Optional JSON array of rules to filter which assets are collected. "
    "Each rule has conditions and an effect. "
    'Example: [{"conditions": [{"attribute_name": "name", "value": "test_*", '
    '"comparison_type": "prefix"}], "effect": "block"}]. '
    "Valid comparison_type values: exact_match (default), prefix, suffix, substring, regexp. "
    "Valid effect values: allow, block.",
)
@click.pass_obj
def set_asset_collection_preferences(ctx, resource_name, asset_type, default_effect, rules_json):
    ManagementService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="management set_asset_collection_preferences",
    ).set_asset_collection_preferences(
        resource_name=resource_name,
        asset_type=asset_type,
        default_effect=default_effect,
        rules=json.loads(rules_json) if rules_json else None,
    )


@management.command(
    help="Delete asset collection preferences for a specific asset type on a resource."
    f" {_get_asset_types_help_text()}"
)
@click.option(
    "--resource-name",
    required=True,
    help="Name of the resource (warehouse or BI container) to remove preferences from.",
)
@click.option(
    "--asset-type",
    required=True,
    help="The type of asset to remove collection preferences for."
    " See command help for supported types.",
)
@click.pass_obj
def delete_asset_collection_preferences(ctx, resource_name, asset_type):
    ManagementService(
        config=ctx["config"],
        mc_client=create_mc_client(ctx),
        command_name="management delete_asset_collection_preferences",
    ).delete_asset_collection_preferences(
        resource_name=resource_name,
        asset_type=asset_type,
    )
