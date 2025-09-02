import base64
import copy
from typing import Any
from typing import Dict
from typing import List


async def search_raw_launch_template_version(
    hub, ctx, name=None, resource_id: str = None
) -> Dict:
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.ec2.describe_launch_template_versions(
        ctx,
        LaunchTemplateId=resource_id if resource_id else None,
        LaunchTemplateName=name if resource_id is None else None,
        Versions=["$Latest"],
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def search_raw(
    hub, ctx, name, filters: List = None, resource_id: str = None
) -> Dict:
    """Fetch one or more launch templates from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        name(str):
            The name of the Idem state.
        resource_id(str, Optional):
            AWS launch template id to identify the resource.
        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_launch_templates

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}

    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["result"] = False
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.ec2.describe_launch_templates(
        ctx,
        Filters=boto3_filter,
        LaunchTemplateIds=[resource_id] if resource_id else None,
    )

    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update_launch_template_version(
    hub,
    ctx,
    launch_template_id: str,
    new_launch_template_data: Dict[str, Any],
):
    """Update launch template version"""
    result = dict(comment=[], result=True, ret={})

    ret = await hub.exec.boto3.client.ec2.create_launch_template_version(
        ctx=ctx,
        LaunchTemplateId=launch_template_id,
        LaunchTemplateData=pre_process_launch_template_data(
            hub, chunk=new_launch_template_data
        ),
    )
    result["result"] = ret["result"]
    result["comment"] += [f"Update launch_template_version"]
    result["ret"] = ret["ret"]["LaunchTemplateVersion"]
    await hub.exec.boto3.client.ec2.modify_launch_template(
        ctx=ctx,
        DefaultVersion=str(result["ret"]["VersionNumber"]),
        LaunchTemplateId=launch_template_id,
    )
    return result


def pre_process_launch_template_data(hub, chunk):
    """Base64 encode launch template user data"""
    desired_state = copy.deepcopy(chunk)
    if desired_state.get("UserData"):
        user_data = desired_state["UserData"]
        desired_state["UserData"] = base64.b64encode(user_data.encode()).decode()

    return desired_state
