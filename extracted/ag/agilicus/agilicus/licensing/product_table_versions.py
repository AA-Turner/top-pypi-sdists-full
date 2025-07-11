from operator import attrgetter
from ..input_helpers import (
    model_from_dict,
    strip_none,
)

from .. import context

from agilicus import (
    create_or_update,
    ProductTableVersion,
)

from ..output.table import (
    format_table,
    spec_column,
    metadata_column,
    constant_if_exists,
    subtable,
    column,
    list_map,
    summarize,
)

from .formatters import constraint_columns


def list_product_table_versions(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    result = apiclient.licensing_api.list_product_table_versions(
        **strip_none(kwargs),
    )
    return result.product_table_versions


def format_product_table_versions(ctx, templates):
    num_subtable_rows = 10
    feature_columns = [
        column("name"),
        *constraint_columns(num_subtable_rows),
    ]
    product_columns = [
        column("name"),
        *constraint_columns(num_subtable_rows),
        column("included_features", "features"),
    ]
    columns = [
        metadata_column("id"),
        spec_column("version"),
        constant_if_exists(spec_column("published"), "✓", default=""),
        subtable(ctx, "spec.product_table.features", feature_columns, "features"),
        subtable(ctx, "spec.product_table.products", product_columns, "products"),
        summarize(
            list_map(
                spec_column("product_table.global_constraints", "constraints"),
                attrgetter("name"),
            ),
            num_subtable_rows,
        ),
    ]

    return format_table(ctx, templates, columns)


def apply_product_table_version(ctx, input_file, **kwargs):
    version = model_from_dict(ProductTableVersion, input_file)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    resp, _ = create_or_update(
        version,
        lambda obj: apiclient.licensing_api.create_product_table_version(obj),
        lambda guid, obj: apiclient.licensing_api.replace_product_table_version(
            guid, product_table_version=obj
        ),
        to_dict=False,
    )
    return resp


def delete_product_table_version(ctx, product_table_version_id):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    apiclient.licensing_api.delete_product_table_version(product_table_version_id)


def show_product_table_version(ctx, product_table_version_id, version, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    if not version and not product_table_version_id:
        raise ValueError("version or product_table_version must be provided")
    if version:
        result = apiclient.licensing_api.list_product_table_versions(
            version=version, limit=1
        )
        if not result.product_table_versions:
            raise ValueError(f"version {version} not found")
        return result.product_table_versions[0]

    return apiclient.licensing_api.get_product_table_version(product_table_version_id)
