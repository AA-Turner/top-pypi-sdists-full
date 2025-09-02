"""

hub.exec.boto3.client.ec2.associate_dhcp_options
"""
import copy
import re
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    *,
    name: str,
    vpc_id: str,
    dhcp_id: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Associates a set of DHCP options (that you've previously created) with the specified VPC, or associates no DHCP
    options with the VPC.

    After you associate the options with the VPC, any existing instances and all new instances that you launch in that
    VPC use the options. You don't need to restart or relaunch the instances. They automatically pick up the changes
    within a few hours, depending on how frequently the instance renews its DHCP lease. You can explicitly renew the
    lease using the operating system on the instance.

    Args:
        name(str):
            An Idem name to identify the dhcp option resource.

        vpc_id(str):
            The list of AWS VPC ID that needs to be associated with dhcp options set.

        dhcp_id(str):
            AWS DHCP Option Set ID.

        resource_id(str, Optional):
            Vpc ID and DHCP Options ID with a separator '-'. Format: [dhcp_id]-[vpc_id]

    Request Syntax:
        .. code-block:: sls

            [dhcp_option-name]:
              aws.ec2.dhcp_option_association.present:
                - resource_id: 'string'
                - vpc_id: 'string'
                - dhcp_id: 'string'
                - name: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            my-dhcp-option:
              aws.ec2.dhcp_option_association.present:
                - resource_id: dhcp-8dh27j-vpc-76db75b8
                - vpc_id: vpc-76db75b8
                - dhcp_id: dhcp-8dh27j
                - name: my-dhcp-option
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    match = re.match(r"^(\w+)-(vpc-\w+)$", str(resource_id))
    if match:
        if not dhcp_id:
            result["comment"] += ["Inferring dhcp_id from resource_id"]
            vpc_id = match.group(1)
        if not vpc_id:
            result["comment"] += ["Inferring vpc_id from resource_id"]
            vpc_id = match.group(2)

    resource = await hub.tool.boto3.resource.create(
        ctx,
        "ec2",
        "DhcpOptions",
        dhcp_id,
    )
    before = await hub.tool.boto3.resource.describe(resource)
    if before:
        ret = await hub.tool.aws.ec2.dhcp_option_association_utils.get_dhcp_vpc_association_details(
            ctx, dhcp_id=dhcp_id, vpc_id=vpc_id
        )
        if ret["result"]:
            result[
                "old_state"
            ] = hub.tool.aws.ec2.conversion_utils.convert_raw_dhcp_association_to_present(
                dhcp_id=dhcp_id,
                idem_resource_name=name,
                vpc_id=vpc_id,
            )
            result["comment"] += [
                f"aws.ec2.dhcp_option_association '{name}' for vpc_id '{vpc_id}' already exists"
            ]
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result

        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "vpc_id": vpc_id,
                    "dhcp_id": dhcp_id,
                    "resource_id": f"{dhcp_id}-{vpc_id}",
                },
            )
            result["comment"] += list(
                hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.ec2.dhcp_option_association", name=name
                )
            )
            return result
        ret = await hub.exec.boto3.client.ec2.associate_dhcp_options(
            ctx,
            DhcpOptionsId=dhcp_id,
            VpcId=vpc_id,
        )
        if not ret["result"]:
            result["result"] = False
            result["comment"] += [result["comment"], ret["comment"]]
            return result
        result["comment"] += result["comment"] + list(
            hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.ec2.dhcp_option_association", name=name
            )
        )
    else:
        result["result"] = False
        result["comment"] += [
            f"Incorrect aws.ec2.dhcp_option_association id: '{dhcp_id}'. Couldn't find DHCP Options with given id."
        ]
        return result
    try:
        convert_ret = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_dhcp_association_to_present(
                dhcp_id=dhcp_id,
                idem_resource_name=name,
                vpc_id=vpc_id,
            )
        )
        result["new_state"] = convert_ret
    except Exception as e:
        result["comment"] += [result["comment"], str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    *,
    name: str,
    vpc_id: str = None,
    dhcp_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Deletes/disassociates association of DHCP options with VPC.

    Args:
        name(str):
            An Idem name to identify the dhcp option resource.

        vpc_id (str, Optional):
            AWS VPC ID that needs to be associated with dhcp options set.

        dhcp_id (str, Optional):
            AWS DHCP Option Set ID.

        resource_id(str, Optional):
            Vpc ID and DHCP Options ID with a separator '-'. Format: [dhcp_id]-[vpc_id]

    Request Syntax:
        .. code-block:: sls

            [dhcp_option-name]:
              aws.ec2.dhcp_option_association.absent:
                - resource_id: 'string'
                - vpc_id: 'string'
                - dhcp_id: 'string'
                - name: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            my-dhcp-option:
              aws.ec2.dhcp_option_association.absent:
                - resource_id: dhcp-8dh27j-vpc-76db75b8
                - vpc_id: vpc-76db75b8
                - dhcp_id: dhcp-8dh27j
                - name: my-dhcp-option
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    match = re.match(r"^(\w+)-(vpc-\w+)$", str(resource_id))
    if match:
        if not dhcp_id:
            result["comment"] += ["Inferring dhcp_id from resource_id"]
            vpc_id = match.group(1)
        if not vpc_id:
            result["comment"] += ["Inferring vpc_id from resource_id"]
            vpc_id = match.group(2)

    if not dhcp_id or not vpc_id:
        result["comment"] += list(
            hub.tool.aws.comment_utils.missing_args_for_absent_comment(
                resource_type="aws.ec2.dhcp_option_association",
                name=name,
                args=["dhcp_id", "vpc_id"],
            )
        )
        result["result"] = False
        return result

    resource = await hub.tool.boto3.resource.create(ctx, "ec2", "DhcpOptions", dhcp_id)
    before = await hub.tool.boto3.resource.describe(resource)
    if not before:
        result["result"] = False
        result["comment"] += [
            f"Incorrect aws.ec2.dhcp_option_association id: '{dhcp_id}'. Couldn't find DHCP Options with given id."
        ]
        return result
    else:
        ret = await hub.tool.aws.ec2.dhcp_option_association_utils.get_dhcp_vpc_association_details(
            ctx, dhcp_id=dhcp_id, vpc_id=vpc_id
        )
        if not ret["result"]:
            result["comment"] += [
                f"aws.ec2.dhcp_option_association '{name}' for vpc_id '{vpc_id}' is already absent!"
            ]
            return result
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_dhcp_association_to_present(
            dhcp_id=dhcp_id,
            idem_resource_name=name,
            vpc_id=vpc_id,
        )
        if ctx.get("test", False):
            result["comment"] += list(
                hub.tool.aws.comment_utils.would_delete_comment(
                    resource_type="aws.ec2.dhcp_option_association", name=name
                )
            )
            return result
        update_ret = await hub.exec.boto3.client.ec2.associate_dhcp_options(
            ctx,
            DhcpOptionsId="default",
            VpcId=vpc_id,
        )
        result["result"] = update_ret["result"]
        result["comment"] += list(
            hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.ec2.dhcp_option_association", name=name
            )
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Lists out all DHCP Options to VPC associations.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.dhcp_option_association
    """

    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_dhcp_options(ctx)
    vpc_ret = await hub.exec.boto3.client.ec2.describe_vpcs(ctx)

    if not (ret["result"] and vpc_ret["result"]):
        hub.log.warning(f"Could not describe dhcp_options association {ret['comment']}")
        return result

    for resource in ret["ret"]["DhcpOptions"]:
        resource_id = resource.get("DhcpOptionsId")
        for vpc_dhcp in vpc_ret["ret"]["Vpcs"]:
            if vpc_dhcp["DhcpOptionsId"] == resource_id:
                resource_converted = hub.tool.aws.ec2.conversion_utils.convert_raw_dhcp_association_to_present(
                    dhcp_id=resource_id,
                    idem_resource_name=resource_id,
                    vpc_id=vpc_dhcp["VpcId"],
                )
                result[f"{resource_id}-{vpc_dhcp['VpcId']}"] = {
                    "aws.ec2.dhcp_option_association.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in resource_converted.items()
                    ]
                }
    return result
