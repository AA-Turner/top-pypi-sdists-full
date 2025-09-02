"""Exec module for managing launch template."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """Get a Launch template resource from AWS. Supply one of the inputs as the filter.

    Args:
        name(str):
            The name of the Idem state.
        resource_id(string, Optional):
            AWS Launch template id to identify the resource.
        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_launch_templates

    Returns:
        Dict[str, Any]:
            Returns launch_template in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.launch_template.get  name=my_resource filters=[{'name': 'tag:Name', 'values': ['value']}]

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python

            async def state_function(hub, ctx, name, service_namespace, scaling_resource_id, scalable_dimension):
                await hub.exec.aws.ec2.launch_template.get(
                    ctx=ctx,
                    name=name,
                    resource_id=resource_id,
                    filters=filters
                )

        Using in a state:

        .. code-block:: yaml

           my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.launch_template.get
                - kwargs:
                    name: my_resource
                    filters:
                      - name: 'launch-template-name'
                        values: [ "template-name" ]
                      - name: 'tag:Key'
                        values: [ "value" ]
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.ec2.launch_template.search_raw(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        filters=filters,
    )
    if not ret["result"]:
        if "InvalidLaunchTemplateId.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.launch_template", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"]["LaunchTemplates"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.launch_template", name=name
            )
        )
        return result

    resource = ret["ret"]["LaunchTemplates"][0]
    if len(ret["ret"]["LaunchTemplates"]) > 1:
        result["comment"].append(
            f"More than one aws.ec2.launch_template resource was found. Use resource {resource.get('LaunchTemplateId')}"
        )
    ret_version = (
        await hub.tool.aws.ec2.launch_template.search_raw_launch_template_version(
            ctx=ctx,
            resource_id=resource["LaunchTemplateId"],
        )
    )

    if not ret_version["result"]:
        result["result"] = False
        result["comment"] += list(ret["comment"])
        return result

    result[
        "ret"
    ] = hub.tool.aws.ec2.conversion_utils.convert_raw_lauchtemplate_to_present(
        raw_resource=resource,
        raw_version=ret_version["ret"]["LaunchTemplateVersions"][0],
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    name: str = None,
    filters: List = None,
) -> Dict:
    """Get Launch templates from AWS. Supply one of the inputs as the filter.

    Args:
        name(str, Optional):
            The name of the Idem state.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_launch_templates

    Returns:
        Dict[str, Any]:
            Returns launch_templates in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.launch_template.list name="my_resources" filters=[{'name': 'launch-template-name', 'values': ['template-name']}]

        Calling this exec module function from within a state module in pure python.

        .. code-block:: python

            async def state_function(hub, ctx, name, service_namespace, scaling_resource_id, scalable_dimension):
                await hub.exec.aws.ec2.launch_template.list(
                    ctx=ctx,
                    name=name,
                    filters=filters
                )

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.launch_template.list
                - kwargs:
                    name: my_resources
                    filters:
                        - name: 'launch-template-name'
                          values: ["template-name"]
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.ec2.launch_template.search_raw(
        ctx=ctx,
        name=name,
        filters=filters,
    )
    if not ret["result"]:
        if "InvalidLaunchTemplateId.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.launch_template", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"]["LaunchTemplates"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.launch_template", name=name
            )
        )
        return result
    result["ret"] = []
    for launch_template in ret["ret"]["LaunchTemplates"]:
        launch_template_id = launch_template.get("LaunchTemplateId")

        ret_version = (
            await hub.tool.aws.ec2.launch_template.search_raw_launch_template_version(
                ctx=ctx,
                resource_id=launch_template_id,
            )
        )
        if not ret_version["result"]:
            continue

        if not ret_version["ret"]["LaunchTemplateVersions"]:
            continue

        result_ret = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_lauchtemplate_to_present(
                raw_resource=launch_template,
                raw_version=ret_version["ret"]["LaunchTemplateVersions"][0],
                idem_resource_name=launch_template.get("LaunchTemplateName"),
            )
        )
        result["ret"].append(result_ret)
    return result
