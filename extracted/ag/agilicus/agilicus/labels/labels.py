from .. import context
from ..input_helpers import (
    get_org_from_input_or_ctx,
    strip_none,
    build_updated_model_validate,
    update_if_not_none,
)
import agilicus
from ..output.table import (
    spec_column,
    status_column,
    format_table,
    metadata_column,
    column,
    subtable,
)

from .. import resource_helpers


def add_label(ctx, name, navigation_enabled=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    spec = agilicus.LabelSpec(name=agilicus.LabelName(name), **kwargs)
    if navigation_enabled is not None:
        spec.navigation = agilicus.LabelNavigation(enabled=navigation_enabled)

    label = agilicus.Label(spec=spec)
    return apiclient.labels_api.create_object_label(label).to_dict()


def list_labels(ctx, name, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    if name is not None:
        kwargs["label_name"] = agilicus.LabelName(name)

    return apiclient.labels_api.list_object_labels(**kwargs).labels


def _get_label(ctx, apiclient, label_id, **kwargs):
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.labels_api.get_object_label(label_id, **kwargs)


def get_label(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return _get_label(ctx, apiclient, **kwargs)


def delete_label(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    apiclient.labels_api.delete_object_label(**kwargs)


def replace_label(ctx, label_id, org_id, navigation_enabled=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)

    label = apiclient.labels_api.get_object_label(label_id=label_id, org_id=org_id)
    kwargs["org_id"] = org_id

    label.spec = build_updated_model_validate(
        agilicus.LabelSpec,
        label.spec,
        kwargs,
        True,
    )

    if navigation_enabled is not None:
        label.spec.navigation.enabled = navigation_enabled

    return apiclient.labels_api.replace_object_label(label_id, label=label)


def format_labels(ctx, labels):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("description"),
        spec_column("navigation.enabled", "navigation"),
    ]

    return format_table(ctx, labels, columns)


def add_labelled_object(ctx, label, object_type, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    if object_type is not None:
        kwargs["object_type"] = agilicus.ObjectType(object_type)

    labels = _label_associations_to_list(label, kwargs["org_id"])
    obj = agilicus.LabelledObject(labels=labels, **kwargs)

    return apiclient.labels_api.create_labelled_object(obj).to_dict()


def list_labelled_objects(
    ctx, includes_any_label, excludes_any_label, object_type, **kwargs
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)
    if includes_any_label is not None:
        kwargs["includes_any_label"] = _labels_to_list(includes_any_label)
    if excludes_any_label is not None:
        kwargs["excludes_any_label"] = _labels_to_list(excludes_any_label)
    if object_type is not None:
        kwargs["object_type"] = agilicus.ObjectType(object_type)

    return apiclient.labels_api.list_labelled_objects(**kwargs).labelled_objects


def _label_associations_to_list(labels, org_id):
    return [
        agilicus.LabelAssociation(
            label_name=agilicus.LabelName(label),
            org_id=org_id,
        )
        for label in labels
    ]


def _labels_to_list(labels):
    return [agilicus.LabelName(label) for label in labels]


def get_labelled_object(ctx, object_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.labels_api.get_labelled_object(
        labelled_object_id=object_id, **kwargs
    )


def delete_labelled_object(ctx, object_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    apiclient.labels_api.delete_labelled_object(labelled_object_id=object_id, **kwargs)


def replace_labelled_object(ctx, label, object_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    obj = apiclient.labels_api.get_labelled_object(
        labelled_object_id=object_id, **kwargs
    )
    if not label:
        return obj

    obj.labels = _label_associations_to_list(label, kwargs["org_id"])
    return apiclient.labels_api.replace_labelled_object(
        obj.object_id, labelled_object=obj
    )


def format_labelled_objects(ctx, objs):
    labels = [
        column("label_name"),
        status_column("navigation.enabled", "navigation"),
    ]

    columns = [
        column("org_id"),
        column("object_id"),
        column("object_type"),
        subtable(ctx, "labels", labels),
    ]

    return format_table(ctx, objs, columns)


def add_labelled_object_label(ctx, label, object_id, org_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    assoc = agilicus.LabelAssociation(
        label_name=agilicus.LabelName(label), org_id=org_id
    )

    return apiclient.labels_api.create_labelled_object_label(object_id, assoc, **kwargs)


def delete_labelled_object_label(ctx, label, object_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.labels_api.delete_labelled_object_label(
        labelled_object_id=object_id, label_name=label, **kwargs
    )


def add_labels_to_resources(
    ctx, resource_type, exclude_resource_type, resource_name, label, **kwargs
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    resources_params = {"org_id": org_id}
    update_if_not_none(
        resources_params,
        {
            "resource_type": resource_type,
            "exclude_resource_type": exclude_resource_type,
            "name": resource_name,
        },
    )

    resources = apiclient.resources_api.list_resources(**resources_params).resources
    for resource in resources:
        _try_add_resource(apiclient, resource, org_id)
        for label_name in label:
            _try_add_label(apiclient, resource.metadata.id, label_name, org_id)


def _try_add_resource(apiclient, resource, org_id):
    obj = agilicus.LabelledObject(
        object_id=resource.metadata.id,
        object_type=agilicus.ObjectType(str(resource.spec.resource_type)),
        org_id=org_id,
        labels=[],
    )

    # We don't care about the result
    agilicus.create_or_update(
        obj, lambda obj: apiclient.labels_api.create_labelled_object(obj), to_dict=False
    )


def _try_add_label(apiclient, resource_id, label_name, org_id):
    assoc = agilicus.LabelAssociation(
        label_name=agilicus.LabelName(label_name), org_id=org_id
    )

    # We don't care about the result
    agilicus.create_or_update(
        assoc,
        lambda obj: apiclient.labels_api.create_labelled_object_label(resource_id, obj),
        to_dict=False,
    )


def add_display_info_icon(ctx, label_id, uri, purpose, height_px, width_px, org_id):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    label = _get_label(ctx, apiclient, label_id, org_id=org_id)

    resource_helpers.add_display_info_icon(label.spec, uri, purpose, height_px, width_px)

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.labels_api.replace_object_label(label_id, label=label)


def delete_display_info_icon(ctx, label_id, uri, org_id):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    label = _get_label(ctx, apiclient, label_id, org_id=org_id)

    if not resource_helpers.delete_display_info_icon(label.spec, uri):
        return label

    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.labels_api.replace_object_label(label_id, label=label)
