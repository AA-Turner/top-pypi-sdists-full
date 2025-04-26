import click
from . import products
from ..output.table import output_entry
from ..input_helpers import get_org_from_input_or_ctx
from ..orgs import get_raw


@click.command(name="list-products")
@click.option("--limit", default=500)
@click.option("--get-subscription-data", default=True)
@click.pass_context
def cli_command_list_products(ctx, **kwargs):
    results = products.list_products(ctx, **kwargs)
    table = products.format_products(ctx, results)
    print(table)


@click.command(name="add-product")
@click.argument("name")
@click.option("--product-price-id", default=None, multiple=True)
@click.option("--dev-mode", is_flag=True, default=None)
@click.option("--label", default=None)
@click.option("--description", default=None)
@click.option("--trial_period", type=int, default=None)
@click.pass_context
def cli_command_add_product(ctx, product_price_id, **kwargs):
    result = products.add_product(
        ctx, product_price_ids=list(product_price_id), **kwargs
    )
    output_entry(ctx, result.to_dict())


@click.command(name="delete-product")
@click.argument("product-id")
@click.pass_context
def cli_command_delete_product(ctx, **kwargs):
    products.delete_product(ctx, **kwargs)


@click.command(name="show-product")
@click.argument("product_id")
@click.pass_context
def cli_command_show_product(ctx, **kwargs):
    result = products.get_product(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="show-default-product")
@click.option("--org_id", default=None)
@click.pass_context
def cli_command_show_default_product(ctx, org_id, **kwargs):
    org = get_raw(ctx, get_org_from_input_or_ctx(ctx, org_id))

    print(f"new suborg product-id decision priority for root org: {org.organisation}")
    print("NOTE: priority 0 is highest\n")
    print("priority 0-product_label_override property organisation create")
    feature_override = "not_set"
    for feature_flag in org.feature_flags:
        if feature_flag.feature == "product_label_override_default":
            feature_override = feature_flag.feature

    print(f"priority 1-product_label_override_default={feature_override}")
    print("priority 2-GEO IP for currency product label")


@click.command(name="update-product")
@click.argument("product_id")
@click.option("--dev-mode", is_flag=True, default=None)
@click.option("--name", default=None)
@click.option("--label", default=None)
@click.option("--trial_period", type=int, default=None)
@click.option("--description", default=None)
@click.option("--product-price-id", default=None, multiple=True)
@click.option("--remove-product-price-id", default=None, multiple=True)
@click.option("--feature-id", default=None, multiple=True)
@click.option("--remove-feature-id", default=None, multiple=True)
@click.pass_context
def cli_command_update_product(
    ctx,
    product_price_id,
    remove_product_price_id,
    feature_id,
    remove_feature_id,
    **kwargs,
):
    result = products.update_product(
        ctx,
        remove_product_price_ids=list(remove_product_price_id),
        product_price_ids=list(product_price_id),
        remove_feature_ids=list(remove_feature_id),
        feature_ids=list(feature_id),
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
