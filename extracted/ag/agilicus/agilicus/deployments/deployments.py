from .. import context
import yaml
import agilicus
from ..input_helpers import update_org_from_input_or_ctx, pop_item_if_none
from .. import create_or_update


def list_deployments(ctx, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.list_deployments(**kwargs).deployments


def get_deployment(ctx, deployment_id, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.get_deployment(deployment_id, **kwargs)


def delete_deployment(ctx, deployment_id, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.delete_deployment(deployment_id, **kwargs)


def add_deployment(ctx, schema=None, **kwargs):
    config_data = {}
    if schema:
        with open(schema, "r") as file:
            config_data = yaml.safe_load(file)
    pop_item_if_none(kwargs)
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)

    deployment = agilicus.Deployment(
        agilicus.DeploymentSpec(**kwargs, schema=config_data)
    )
    return apiclient.deployments_api.create_deployment(deployment)


def list_deployment_instances(ctx, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.list_deployment_instances(
        **kwargs
    ).deployment_instances


def get_deployment_instance(ctx, deployment_instance_id, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.get_deployment_instance(
        deployment_instance_id, **kwargs
    )


def add_deployment_instance(ctx, input, **kwargs):
    pop_item_if_none(kwargs)
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)

    inputs = []
    for _input in input:
        split_str = _input.split(",")
        name = split_str[0]
        value = split_str[1]
        inputs.append(agilicus.DeploymentInstanceInput(name=name, value_as_string=value))
    instance = agilicus.DeploymentInstance(
        agilicus.DeploymentInstanceSpec(inputs=inputs, **kwargs)
    )
    return apiclient.deployments_api.create_deployment_instance(instance)


def delete_deployment_instance(ctx, deployment_instance_id, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.delete_deployment_instance(
        deployment_instance_id, **kwargs
    )


def list_deployment_templates(ctx, **kwargs):
    pop_item_if_none(kwargs)
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.list_deployment_templates(
        **kwargs
    ).deployment_templates


def get_deployment_template(ctx, deployment_template_id, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.get_deployment_template(
        deployment_template_id, **kwargs
    )


def add_deployment_template(ctx, template, **kwargs):
    with open(template, "r") as file:
        config_data = yaml.safe_load(file)
        return add_deployment_template_from_dict(ctx, config_data, **kwargs)


def add_deployment_template_from_dict(ctx, template, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    kwargs["description"] = template.get("description")
    pop_item_if_none(kwargs)

    deployment_template = agilicus.DeploymentTemplate(
        agilicus.DeploymentTemplateSpec(**kwargs, template=template)
    )

    return create_or_update(
        deployment_template,
        apiclient.deployments_api.create_deployment_template,
        apiclient.deployments_api.update_deployment_template,
    )


def update_system_templates(ctx, templates, **kwargs):
    with open(templates, "r") as file:
        config_data = yaml.safe_load(file)
        for template_type, v in config_data.items():
            for name, template_dict in v.items():
                add_deployment_template_from_dict(
                    ctx,
                    name=name,
                    template=template_dict,
                    template_type=template_type,
                    **kwargs,
                )


def delete_deployment_template(ctx, deployment_template_id, **kwargs):
    token = context.get_token(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    apiclient = context.get_apiclient(ctx, token)
    return apiclient.deployments_api.delete_deployment_template(
        deployment_template_id, **kwargs
    )
