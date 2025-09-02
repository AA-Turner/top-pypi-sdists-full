"""Exec module for managing EC2 security groups."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
) -> Dict:
    """
    Get a SecurityGroup resource from AWS. Supply one of the inputs as the filter.

    Args:
        resource_id (str):
            ID of the security group.

    Returns:
        Dict[str, Any]:
            Returns security group in present format

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.ec2.security_group.get resource_id="my_resource"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.security_group.get
                - kwargs:
                    resource_id: my_resource
    """
    result = {
        "comment": ["SecurityGroupRules"],
        "ret": None,
        "result": True,
    }

    ret = await hub.exec.boto3.client.ec2.describe_security_group_rules(
        ctx=ctx,
        SecurityGroupRuleIds=[resource_id],
    )
    if not ret.get("result"):
        if "InvalidGroup.NotFound" in str(ret.get("comment", "")):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.security_group_rule", name=resource_id
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret.get("comment", ""))
        return result
    if not ret.get("ret", {}).get("SecurityGroupRules"):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.security_group_rules", name=resource_id
            )
        )
        return result

    resource = ret["ret"]["SecurityGroupRules"][0]
    if len(ret["ret"]["SecurityGroupRules"]) > 1:
        result["comment"].append(
            f"More than one aws.ec2.security_group_rule resource was found. Use resource {resource.get('GroupId')}"
        )

    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_rule_to_present(
        resource
    )
    result["ret"]["name"] = result["ret"]["tags"].get("Name")
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

            idem exec aws.ec2.security_group.list filters=[{'name': 'name', 'values': ['resource-name']}]

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.security_group.list
                - kwargs:
                    filters:
                        - name: 'name'
                          values: ['resource-name']
    """
    result = {
        "comment": ["SecurityGroupRules"],
        "ret": None,
        "result": True,
    }
    boto3_filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.ec2.describe_security_group_rules(
        ctx,
        Filters=boto3_filters,
    )
    result["ret"] = []
    for security_group_rule in ret["ret"]["SecurityGroupRules"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_sg_rule_to_present(
                raw_resource=security_group_rule
            )
        )
    return result
