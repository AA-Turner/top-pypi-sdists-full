"""
State module for managing EC2 Internet Gateways.

hub.exec.boto3.client.ec2.attach_internet_gateway
hub.exec.boto3.client.ec2.create_internet_gateway
hub.exec.boto3.client.ec2.delete_internet_gateway
hub.exec.boto3.client.ec2.describe_internet_gateways
hub.exec.boto3.client.ec2.detach_internet_gateway
resource = await hub.tool.boto3.resource.create(ctx, "ec2", "InternetGateway", name)
hub.tool.boto3.resource.exec(resource, attach_to_vpc, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, create_tags, *args, **kwargs)
"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]
TREQ = {
    "absent": {
        "require": [
            "aws.ec2.elastic_ip.absent",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    vpc_id: List = None,
) -> Dict[str, Any]:
    """Creates an internet gateway for use with a VPC.

    After creating the internet gateway, you attach it to a VPC using AttachInternetGateway. For more information about
    your VPC and internet gateway, see the Amazon Virtual Private Cloud User Guide.

    Args:
        name(str):
            An Idem name to identify the internet gateway resource.

        resource_id(str, Optional):
            AWS Internet Gateway ID.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the internet gateway resource. Defaults to None.

            * (Key, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * (Value, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

        vpc_id(list, Optional):
            This list can contain only single element. This is ID of VPC to which internet gateway attaches.
            If vpc_id is not passed, then attach/detach operation is ignored.
            If user passes empty list, then attached vpc is detached.

    Request Syntax:
       .. code-block:: sls

          [internet_gateway-name]:
            aws.ec2.internet_gateway.present:
              - vpc_id:
                - 'string'
              - tags:
                - Key: 'string'
                  Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            test-igw:
              aws.ec2.internet_gateway.present:
                - vpc_id:
                - vpc-d04fbf46
                - tags:
                  - Key: Name
                    Value: test-igw
    """

    plan_state = {}
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    # Skip fetching resource if there is no change
    is_state_updated = True
    before = None
    if resource_id:
        before = await hub.exec.boto3.client.ec2.describe_internet_gateways(
            ctx=ctx, DryRun=False, InternetGatewayIds=[resource_id]
        )

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if before and before["result"]:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_internet_gateway_to_present(
            resource=before["ret"]["InternetGateways"][0], idem_resource_name=name
        )
        plan_state = copy.deepcopy(result["old_state"])
        result["comment"] += [f"'{name}' already exists"]
        try:
            if tags is not None and tags != result["old_state"].get("tags"):
                update_ret = await hub.tool.aws.ec2.tag.update_tags(
                    ctx=ctx,
                    resource_id=resource_id,
                    old_tags=result["old_state"].get("tags"),
                    new_tags=tags,
                )
                result["result"] = update_ret["result"]
                result["comment"] += update_ret["comment"]
                if ctx.get("test", False) and update_ret["result"]:
                    plan_state["tags"] = update_ret["ret"]
            ret = await hub.tool.aws.ec2.internet_gateway.update_attachments(
                ctx=ctx,
                internet_gateway_name=resource_id,
                vpc_id=vpc_id,
                before=result["old_state"],
            )
            result["result"] = ret["result"]
            result["comment"] += ret["comment"]
            if tags is None and vpc_id is None:
                is_state_updated = False
            if ctx.get("test", False) and ret["ret"].get("updated_vpc_id") is not None:
                plan_state["vpc_id"] = ret["ret"]["updated_vpc_id"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "vpc_id": vpc_id,
                    "tags": tags,
                    "resource_id": name,
                },
            )
            if vpc_id:
                result["comment"] += [
                    f"Would create aws.ec2.internet_gateway '{name}' and attach to vpc '{vpc_id[0]}'"
                ]
                return result

            result["comment"] += [f"Would create aws.ec2.internet_gateway '{name}'"]
            return result
        try:
            ret = await hub.exec.boto3.client.ec2.create_internet_gateway(
                ctx,
                TagSpecifications=[
                    {
                        "ResourceType": "internet-gateway",
                        "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                    }
                ]
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            resource_id = ret["ret"]["InternetGateway"]["InternetGatewayId"]
            result["comment"] += [f"Created '{name}'"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
        if vpc_id:
            try:
                ret = await hub.exec.boto3.client.ec2.attach_internet_gateway(
                    ctx, InternetGatewayId=resource_id, VpcId=vpc_id[0]
                )
                result["result"] = ret["result"]
                if not result["result"]:
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result
                result["comment"] += [
                    f"Created '{name}' and attached to vpc '{vpc_id[0]}'"
                ]
            except hub.tool.boto3.exception.ClientError as e:
                result["result"] = False
                result["comment"] += [
                    f"Created '{name}'. Attach to '{vpc_id[0]}' failed with error: {e}"
                ]
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif is_state_updated or not (before and before["result"]):
            after = await hub.exec.boto3.client.ec2.describe_internet_gateways(
                ctx, DryRun=False, InternetGatewayIds=[resource_id]
            )
            result[
                "new_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_internet_gateway_to_present(
                resource=after["ret"].get("InternetGateways")[0],
                idem_resource_name=name,
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the specified internet gateway.

    If resource is attached to VPC. then it is detached first and then deleted.

    Args:
        name(str):
            An Idem name to identify the internet gateway resource.

        resource_id(str, Optional):
            AWS Internet Gateway ID.

    Request Syntax:
       .. code-block:: sls

         [internet_gateway-name]:
           aws.ec2.internet_gateway.absent:
             - name: 'string'
             - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

           igw-test:
             aws.ec2.internet_gateway.absent:
               - name: igw-test
               - resource_id: '12345678'
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.internet_gateway", name=name
        )
        return result
    resource = await hub.tool.boto3.resource.create(
        ctx, "ec2", "InternetGateway", resource_id
    )
    before = await hub.tool.boto3.resource.describe(resource)
    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.internet_gateway", name=name
        )
    else:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_internet_gateway_to_present(
            resource=before, idem_resource_name=name
        )
        if ctx.get("test", False):
            result["comment"] += [f"Would delete aws.ec2.internet_gateway '{name}'"]
            return result
        else:
            try:
                gateway_resource = before
                if gateway_resource["Attachments"]:
                    resource.detach_from_vpc(
                        VpcId=gateway_resource["Attachments"][0]["VpcId"]
                    )
                ret = await hub.exec.boto3.client.ec2.delete_internet_gateway(
                    ctx, InternetGatewayId=resource_id
                )
                result["result"] = ret["result"]
                if not result["result"]:
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result
                result["comment"] += [f"Deleted '{name}'"]
            except hub.tool.boto3.exception.ClientError as e:
                result["result"] = False
                result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Describes one or more of your internet gateways.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.internet_gateway
    """

    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_internet_gateways(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe internet_gateway {ret['comment']}")
        return {}

    for internet_gateway in ret["ret"]["InternetGateways"]:
        resource_id = internet_gateway.get("InternetGatewayId")
        resource_converted = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_internet_gateway_to_present(
                resource=internet_gateway, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.ec2.internet_gateway.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_converted.items()
            ]
        }
    return result
