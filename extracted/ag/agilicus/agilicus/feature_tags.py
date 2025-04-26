from . import context

import agilicus

from .input_helpers import strip_none

from .output.table import (
    spec_column,
    format_table,
    metadata_column,
)


def list_feature_tags(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.features_api.list_feature_tags(**strip_none(kwargs)).feature_tags


def add_feature_tag(ctx, name, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    tag_spec = agilicus.FeatureTagSpec(name=agilicus.FeatureTagName(name))
    tag = agilicus.FeatureTag(spec=tag_spec)
    return apiclient.features_api.add_feature_tag(tag)


def show_feature_tag(ctx, name):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.features_api.get_feature_tag(feature_tag_name=name)


def delete_feature_tag(ctx, name):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.features_api.delete_feature_tag(feature_tag_name=name)


def format_feature_tags_as_text(ctx, tags):
    columns = [
        spec_column("name"),
        metadata_column("created"),
    ]

    return format_table(ctx, tags, columns)
