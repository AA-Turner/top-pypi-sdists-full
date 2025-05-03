import io
from .. import context
from ..input_helpers import (
    get_user_id_from_input_or_ctx,
    get_org_from_input_or_ctx,
    strip_none,
    update_attrs_if_not_none,
)
import agilicus
from ..output.table import (
    spec_column,
    format_table,
    metadata_column,
    column,
    subtable,
    summarize,
)

from ..files import upload
from ..users import get_user


def _args_from_list(arg_list):
    return [
        agilicus.FileTemplateArgument(
            name=agilicus.FileTemplateParameterName(name), value=value
        )
        for name, value in arg_list or []
    ]


def add_file_template(
    ctx,
    content_type,
    parameters,
    default_arguments,
    rendered_file_name,
    file_to_upload=None,
    associated_objects=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    file_id = None
    if file_to_upload is not None:
        result = upload(ctx, file_to_upload, org_id=org_id, name=rendered_file_name)
        file_id = result["id"]
        kwargs["template_file"] = file_id

    spec = agilicus.FileTemplateSpec(
        template_content_type=content_type,
        org_id=org_id,
        rendered_file_name=rendered_file_name,
        template_parameters=[
            agilicus.FileTemplateParameter(
                name=agilicus.FileTemplateParameterName(param)
            )
            for param in parameters or []
        ],
        default_arguments=_args_from_list(default_arguments),
        associated_objects=[
            agilicus.FileTemplateAssociation(
                object_id=obj_id,
                object_type=agilicus.ObjectType(obj_type),
                descriptive_text=desc,
            )
            for obj_id, obj_type, desc in associated_objects or []
        ],
        **kwargs,
    )

    obj = agilicus.FileTemplate(spec=spec)
    return apiclient.files_api.create_file_template(obj).to_dict()


def replace_file_template(
    ctx,
    file_template_id,
    content_type,
    parameters,
    default_arguments,
    rendered_file_name,
    associated_objects=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    existing = apiclient.files_api.get_file_template(file_template_id, org_id=org_id)
    spec = existing.spec
    if content_type:
        spec.template_content_type = content_type
    if parameters:
        spec.template_parameters = [
            agilicus.FileTemplateParameter(
                name=agilicus.FileTemplateParameterName(param)
            )
            for param in parameters or []
        ]
    if default_arguments:
        spec.default_arguments = (_args_from_list(default_arguments),)
    if rendered_file_name:
        spec.rendered_file_name = rendered_file_name
    if associated_objects:
        spec.associated_objects.extend(
            [
                agilicus.FileTemplateParameter(
                    name=agilicus.FileTemplateParameterName(param)
                )
                for param in parameters or []
            ]
        )
    update_attrs_if_not_none(spec, kwargs)

    return apiclient.files_api.replace_file_template(
        file_template_id, file_template=existing
    ).to_dict()


def list_file_templates(ctx, org_id=None, object_types=None, object_ids=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, org_id=org_id)
    kwargs = strip_none(kwargs)

    if object_types:
        kwargs["object_types"] = [agilicus.ObjectType(t) for t in object_types]
    if object_ids:
        kwargs["object_ids"] = object_ids

    return apiclient.files_api.list_file_templates(**kwargs).file_templates


def get_file_template(ctx, file_template_id, org_id=None):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    return apiclient.files_api.get_file_template(file_template_id, org_id=org_id)


def delete_file_template(ctx, file_template_id, org_id=None):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    return apiclient.files_api.delete_file_template(file_template_id, org_id=org_id)


def render_file_template(
    ctx,
    file_template_id,
    template_arguments=[],
    include_user=False,
    resource_id=None,
    as_attachment=False,
    org_id=None,
    user_id=None,
) -> io.BufferedReader:
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    request = agilicus.FileTemplateRenderRequest(
        template_arguments=_args_from_list(template_arguments),
        org_id=org_id,
        as_attachment=as_attachment,
    )
    if include_user:
        user_id = get_user_id_from_input_or_ctx(ctx, user_id)
        user = get_user(ctx, user_id, org_id=org_id)
        request._check_type = False
        request.user_information = user
        request._check_type = True
    if resource_id is not None:
        svc = apiclient.app_services_api.get_application_service(
            resource_id, org_id=org_id
        )
        request.resource_information = resource_info_from_app_svc(svc)

    return apiclient.files_api.render_file_template(file_template_id, request)


def resource_info_from_app_svc(svc):
    result = agilicus.FileTemplateResourceInfo(
        org_id=svc.org_id,
        name=svc.name,
        resource_type=_map_proto(svc.service_protocol_type),
        resource_id=svc.id,
    )

    if not svc.status:
        return result
    routing_info = svc.status.routing_info
    if not routing_info:
        return result
    if not routing_info.exposed_as_hostname:
        return result
    # TODO: make this a property of the core resource somehow
    result.uri = f"https://{routing_info.exposed_as_hostname}"
    return result


def _map_proto(proto):
    if proto == "ip":
        return "application_service"
    return proto


def format_file_templates(ctx, labels):
    args_columns = [
        column("name"),
        column("value"),
    ]
    params_columns = [
        column("name"),
    ]
    associated_columns = [
        column("object_id"),
        column("object_type"),
        summarize(column("descriptive_text"), 10),
    ]
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("purpose"),
        spec_column("descriptive_text"),
        spec_column("template_file"),
        subtable(ctx, "default_arguments", args_columns, subobject_name="spec"),
        subtable(
            ctx,
            "template_parameters",
            params_columns,
            out_name="parameters",
            subobject_name="spec",
        ),
        subtable(
            ctx,
            "associated_objects",
            associated_columns,
            out_name="objects",
            subobject_name="spec",
        ),
    ]

    return format_table(ctx, labels, columns)
