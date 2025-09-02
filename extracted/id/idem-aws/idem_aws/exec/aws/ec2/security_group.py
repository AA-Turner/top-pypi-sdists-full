"""Exec module for managing EC2 security groups."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """
    Get a SecurityGroup resource from AWS. Supply one of the inputs as the filter.

    Args:
        name (str):
            The name of the Idem state.

        resource_id (str, Optional):
            ID of the security group.

        filters (list[str, str], Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups

    Returns:
        Dict[str, Any]:
            Returns security group in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.security_group.get name="my_resource" filters=[{'name': 'name', 'values': ['resource-name']}]

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.security_group.get
                - kwargs:
                    name: my_resource
                    filters:
                        - name: 'name'
                          values: ['resource-name']
    """
    result = dict(comment=[], ret=None, result=True)
    boto3_filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )

    ret = await hub.exec.boto3.client.ec2.describe_security_groups(
        ctx=ctx,
        GroupIds=[resource_id] if resource_id else None,
        Filters=boto3_filters,
    )
    if not ret.get("result"):
        if "InvalidGroup.NotFound" in str(ret.get("comment", "")):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.security_group", name=name
                )
            )
            result["result"] = False
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret.get("comment", ""))
        result["result"] = False
        return result
    if not ret.get("ret", {}).get("SecurityGroups"):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.security_groups", name=name
            )
        )
        return result

    resource = ret["ret"]["SecurityGroups"][0]
    if len(ret["ret"]["SecurityGroups"]) > 1:
        result["comment"].append(
            f"More than one aws.ec2.security_group resource was found. Use resource {resource.get('GroupId')}"
        )

    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(
        resource
    )
    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """
    Get a list of SecurityGroup resources from AWS. Supply one of the inputs as the filter.

    Args:
        name (str, Optional):
            The name of the Idem state.

        filters (list[str, str], Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups

    Returns:
        Dict[str, Any]:
            Returns security group list in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.security_group.list name="my_resource" filters=[{'name': 'name', 'values': ['resource-name']}]

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.security_group.list
                - kwargs:
                    name: my_resource
                    filters:
                        - name: 'name'
                          values: ['resource-name']
    """
    result = dict(comment=[], ret=[], result=True)
    boto3_filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.ec2.describe_security_groups(
        ctx,
        Filters=boto3_filters,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["SecurityGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.security_group", name=name
            )
        )
        return result
    for security_group in ret["ret"]["SecurityGroups"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_sg_to_present(
                security_group=security_group
            )
        )
    return result
