import click

from agilicus.command_helpers import Command
from ..input_helpers import page_sort_order_values
from . import metrics

cmd = Command()


@cmd.command(name="get-usage-metrics")
@click.argument("org-id", default=None, required=False)
@click.option("--org-id", "opt_org_id", default=None, help="Organisation UUID")
@click.option(
    "--org-ids",
    multiple=True,
    default=None,
    help="Multiple organisation UUIDs (for multi-tenant queries)",
)
@click.option(
    "--all-orgs",
    "--fleet",
    is_flag=True,
    default=False,
    help=(
        "Query across all organisations (fleet-wide). Requires a token with "
        "the multiorg scope (urn:agilicus:token_payload:multiorg:true)."
    ),
)
@click.option(
    "--dt-from",
    default=None,
    help="Start time (ISO 8601 or natural language, e.g. 'now-30d', '6 months ago')",
)
@click.option(
    "--dt-to",
    default=None,
    help="End time (ISO 8601 or natural language, e.g. 'now', '1 month ago')",
)
@click.option(
    "--bucket-size",
    default=None,
    help="Time bucket granularity (e.g. PT15M, PT1H, P1D, P1W, P1M, or aliases)",
)
@click.option(
    "--breakdown-by",
    multiple=True,
    default=None,
    help="Dimensions to break down by: user_id, resource_id, resource_type, org_id",
)
@click.option(
    "--resource-type",
    default=None,
    help="Filter by resource type (e.g. ssh, web, rdp)",
)
@click.option("--resource-id", default=None, help="Filter by resource UUID")
@click.option("--user-id", default=None, help="Filter by user UUID")
@click.option(
    "--sort-by",
    type=click.Choice(["time", "access_count", "unique_users", "unique_resources"]),
    default=None,
    help="Field to sort buckets by",
)
@click.option(
    "--sort-order",
    type=click.Choice(["asc", "desc", "ascending", "descending"]),
    default=None,
    help="Sort direction (asc or desc)",
)
@click.option(
    "--limit",
    default=None,
    type=int,
    help=(
        "Maximum total records returned (default 500). Values above the "
        "server page size are fetched over multiple pages."
    ),
)
@click.option(
    "--get-all", default=False, is_flag=True, help="Fetch all pages of results"
)
@click.option(
    "--page-on",
    multiple=True,
    default=None,
    help="Dimensions/fields to page on: time, user_id, resource_id, etc.",
)
@click.option(
    "--page-at-key",
    multiple=True,
    type=str,
    default=None,
    help="Keyset pagination starting point",
)
@click.option(
    "--page-sort",
    multiple=True,
    type=click.Choice(page_sort_order_values),
    default=None,
    help="Keyset pagination sort direction (asc or desc)",
)
@click.option(
    "--preset",
    type=click.Choice(
        [
            "user-usage",
            "resource-usage",
            "adoption",
            "velocity",
            "resource-types",
            "unique-users",
            "fleet-comparison",
        ]
    ),
    default=None,
    help="Run a standard usage/adoption preset query",
)
@click.pass_context
def cli_command_get_usage_metrics(ctx, org_id, opt_org_id, **kwargs):
    """View aggregated usage, adoption, and access metrics over intervals."""
    kwargs["org_id"] = org_id or opt_org_id
    result = metrics.query_usage(ctx, **kwargs)
    print(metrics.format_usage_metrics(ctx, result))


# Alias list-usage-metrics to get-usage-metrics so options stay synchronized
cmd.commands.append(
    click.Command(
        name="list-usage-metrics",
        callback=cli_command_get_usage_metrics.callback,
        params=cli_command_get_usage_metrics.params,
        help=cli_command_get_usage_metrics.help,
    )
)


@cmd.command(name="get-user-usage")
@click.argument("org-id", default=None, required=False)
@click.option("--org-id", "opt_org_id", default=None, help="Organisation UUID")
@click.option("--dt-from", default=None, help="Start time")
@click.option("--dt-to", default=None, help="End time")
@click.option("--bucket-size", default=None, help="Time bucket granularity")
@click.option("--resource-type", default=None, help="Filter by resource type")
@click.option("--resource-id", default=None, help="Filter by resource UUID")
@click.option("--limit", default=None, type=int, help="Maximum records returned")
@click.option(
    "--get-all", default=False, is_flag=True, help="Fetch all pages of results"
)
@click.option(
    "--page-on",
    multiple=True,
    default=None,
    help="Dimensions/fields to page on",
)
@click.option(
    "--page-at-key",
    multiple=True,
    type=str,
    default=None,
    help="Keyset pagination starting point",
)
@click.option(
    "--page-sort",
    multiple=True,
    type=click.Choice(page_sort_order_values),
    default=None,
    help="Keyset pagination sort direction",
)
@click.pass_context
def cli_command_get_user_usage(ctx, org_id, opt_org_id, **kwargs):
    """Query user usage and frequency: who is using the system, and how often."""
    kwargs["org_id"] = org_id or opt_org_id
    result = metrics.query_user_usage(ctx, **kwargs)
    print(metrics.format_usage_metrics(ctx, result))


@cmd.command(name="get-resource-usage")
@click.argument("org-id", default=None, required=False)
@click.option("--org-id", "opt_org_id", default=None, help="Organisation UUID")
@click.option("--dt-from", default=None, help="Start time")
@click.option("--dt-to", default=None, help="End time")
@click.option("--bucket-size", default=None, help="Time bucket granularity")
@click.option("--resource-type", default=None, help="Filter by resource type")
@click.option("--limit", default=None, type=int, help="Maximum records returned")
@click.option(
    "--get-all", default=False, is_flag=True, help="Fetch all pages of results"
)
@click.option(
    "--page-on",
    multiple=True,
    default=None,
    help="Dimensions/fields to page on",
)
@click.option(
    "--page-at-key",
    multiple=True,
    type=str,
    default=None,
    help="Keyset pagination starting point",
)
@click.option(
    "--page-sort",
    multiple=True,
    type=click.Choice(page_sort_order_values),
    default=None,
    help="Keyset pagination sort direction",
)
@click.pass_context
def cli_command_get_resource_usage(ctx, org_id, opt_org_id, **kwargs):
    """Query resource usage: which resources are active vs least used."""
    kwargs["org_id"] = org_id or opt_org_id
    result = metrics.query_resource_usage(ctx, **kwargs)
    print(metrics.format_usage_metrics(ctx, result))


@cmd.command(name="get-adoption-metrics")
@click.argument("org-id", default=None, required=False)
@click.option("--org-id", "opt_org_id", default=None, help="Organisation UUID")
@click.option("--dt-from", default=None, help="Start time (default: now-30d)")
@click.option("--dt-to", default=None, help="End time (default: now)")
@click.option(
    "--bucket-size", default=None, help="Time bucket granularity (default: P1D)"
)
@click.option("--resource-type", default=None, help="Filter by resource type")
@click.option("--limit", default=None, type=int, help="Maximum records returned")
@click.option(
    "--get-all", default=False, is_flag=True, help="Fetch all pages of results"
)
@click.option(
    "--page-on",
    multiple=True,
    default=None,
    help="Dimensions/fields to page on",
)
@click.option(
    "--page-at-key",
    multiple=True,
    type=str,
    default=None,
    help="Keyset pagination starting point",
)
@click.option(
    "--page-sort",
    multiple=True,
    type=click.Choice(page_sort_order_values),
    default=None,
    help="Keyset pagination sort direction",
)
@click.pass_context
def cli_command_get_adoption_metrics(ctx, org_id, opt_org_id, **kwargs):
    """Query user adoption progression over time."""
    kwargs["org_id"] = org_id or opt_org_id
    result = metrics.query_adoption(ctx, **kwargs)
    print(metrics.format_usage_metrics(ctx, result))


@cmd.command(name="get-fleet-usage")
@click.option(
    "--org-ids",
    multiple=True,
    default=None,
    help="Multiple organisation UUIDs to compare",
)
@click.option("--dt-from", default=None, help="Start time")
@click.option("--dt-to", default=None, help="End time")
@click.option(
    "--bucket-size", default=None, help="Time bucket granularity (default: P1M)"
)
@click.option("--limit", default=None, type=int, help="Maximum records returned")
@click.option(
    "--get-all", default=False, is_flag=True, help="Fetch all pages of results"
)
@click.option(
    "--page-on",
    multiple=True,
    default=None,
    help="Dimensions/fields to page on",
)
@click.option(
    "--page-at-key",
    multiple=True,
    type=str,
    default=None,
    help="Keyset pagination starting point",
)
@click.option(
    "--page-sort",
    multiple=True,
    type=click.Choice(page_sort_order_values),
    default=None,
    help="Keyset pagination sort direction",
)
@click.pass_context
def cli_command_get_fleet_usage(ctx, **kwargs):
    """Fleet-wide usage comparison across customer organisations."""
    result = metrics.query_fleet_usage(ctx, **kwargs)
    print(metrics.format_usage_metrics(ctx, result))


def add_commands(cli):
    cmd.add_to_cli(cli)
