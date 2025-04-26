import agilicus
from ..context import get_apiclient_from_ctx
import operator
from agilicus.input_helpers import pop_item_if_none
from agilicus.input_helpers import update_attrs_if_not_none
from ..output.table import (
    spec_column,
    metadata_column,
    format_table,
    subtable,
)


def get_api(ctx):
    return get_apiclient_from_ctx(ctx).billing_api


def list_features(ctx, **kwargs):
    api = get_api(ctx)
    return api.list_features(**kwargs).features


def format_features(ctx, features):
    product_columns = [
        spec_column("name"),
        spec_column("label", optional=True),
        spec_column("description", optional=True),
    ]
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("key"),
        spec_column("value"),
        subtable(
            ctx,
            "products",
            columns=product_columns,
            subobject_name="status",
            table_getter=operator.itemgetter,
        ),
    ]
    return format_table(ctx, features, columns)


def add_feature(
    ctx,
    min=None,
    max=None,
    enabled=None,
    priority=None,
    **kwargs,
):
    api = get_api(ctx)
    pop_item_if_none(kwargs)
    spec = agilicus.FeatureSpec(**kwargs)
    val = agilicus.FeatureValue()
    spec.value = val
    if min:
        val.min = min

    if max:
        val.max = max

    if enabled is not None:
        val.enabled = enabled

    if priority is not None:
        spec.priority = priority
    return api.create_feature(agilicus.Feature(spec))


def delete_feature(ctx, **kwargs):
    api = get_api(ctx)
    return api.delete_feature(**kwargs)


def list_feature_subscriptions(ctx, **kwargs):
    api = get_api(ctx)
    return api.list_subscriptions_with_feature(**kwargs).billing_subscriptions


def update_feature(
    ctx,
    feature_id,
    **kwargs,
):
    api = get_api(ctx)

    feature = api.get_feature(feature_id)

    pop_item_if_none(kwargs)

    vals = {}
    for v in ["min", "max", "enabled"]:
        vals[v] = kwargs.pop(v, None)

    pop_item_if_none(vals)
    if not feature.spec.value:
        feature.spec.value = agilicus.FeatureValue()

    update_attrs_if_not_none(feature.spec, kwargs)
    update_attrs_if_not_none(feature.spec.value, vals)

    return api.replace_feature(feature_id, feature=feature)
