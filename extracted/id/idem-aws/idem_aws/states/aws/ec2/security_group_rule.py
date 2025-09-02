"""State module for managing EC2 Security Group Rules"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.ec2.security_group.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    group_id: str,
    ip_protocol: str,
    from_port: int,
    to_port: int,
    is_egress: bool,
    resource_id: str = None,
    cidr_ipv4: str = None,
    cidr_ipv6: str = None,
    prefix_list_id: str = None,
    referenced_group_info: Dict = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    description: str = None,
) -> Dict[str, Any]:
    """Creates a security group rule.

    Adds the specified inbound (ingress) or outbound (egress) rules to a security group:
        * An inbound rule permits instances to receive traffic from the specified IPv4 or IPv6 CIDR address range, or from the
          instances that are associated with the specified destination security groups.You specify a protocol for each rule
          (for example, TCP). For TCP and UDP, you must also specify the destination port or port range. For ICMP/ICMPv6,
          you must also specify the ICMP/ICMPv6 type and code. You can use -1 to mean all types or all codes. Rule changes
          are propagated to instances within the security group as quickly as possible. However, a small delay might occur.

        * An outbound rule permits instances to send traffic to the specified IPv4 or IPv6 CIDR address ranges, or to the
          instances that are associated with the specified source security groups. You specify a protocol for each rule
          (for example, TCP). For the TCP and UDP protocols, you must also specify the destination port or port range.
          For the ICMP protocol, you must also specify the ICMP type and code. You can use -1 for the type or code to mean
          all types or all codes. Rule changes are propagated to affected instances as quickly as possible. However, a small
          delay might occur.

    Args:

        name(str):
            An Idem name to identify the security group rule resource.

        group_id(str):
            The ID of the security group

        is_egress(bool):
            To find the type of rule, whether it is a ingress or egress.

        ip_protocol(str):
            The IP protocol name (tcp , udp , icmp , icmpv6 ) or number (see Protocol Numbers ). [VPC only] Use -1 to specify all protocols.
            When authorizing security group rules, specifying -1 or a protocol number other than tcp , udp , icmp , or icmpv6 allows traffic
            on all ports, regardless of any port range you specify. For tcp , udp , and icmp , you must specify a port range. For icmpv6 ,
            the port range is optional; if you omit the port range, traffic for all types and codes is allowed.

        from_port(int):
            The start of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 type number. A value of -1 indicates all ICMP/ICMPv6 types.
            If you specify all ICMP/ICMPv6 types, you must specify all codes.

        to_port(int):
            The end of port range for the TCP and UDP protocols, or an ICMP/ICMPv6 code. A value of -1 indicates all ICMP/ICMPv6 codes.
            If you specify all ICMP/ICMPv6 types, you must specify all codes.

        cidr_ipv4(str, Optional):
            The IPv4 CIDR range. You can either specify a CIDR range or a source security group, not both.
            To specify a single IPv4 address, use the /32 prefix length.

        resource_id(str, Optional):
            AWS Security group rule ID.

        cidr_ipv6(str, Optional):
            The IPv6 CIDR range. You can either specify a CIDR range or a source security group, not both.
            To specify a single IPv6 address, use the /128 prefix length.

        prefix_list_id(str, Optional):
            The ID of the prefix.

        referenced_group_info(dict, Optional):
            The security group and Amazon Web Services account ID pairs.

        description(str, Optional):
            The description of the security group rule.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the security group rule.
            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional):
                The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode
                characters. May not begin with aws:.

            * Value (str, Optional):
                The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256
                Unicode characters.

    Request Syntax:
        .. code-block:: sls

            [security_group_rule_name]:
              aws.ec2.security_group_rule.present:
                - group_id: 'string'
                - is_egress: 'bool'
                - ip_protocol: 'string'
                - from_port: 'int'
                - to_port: 'int'
                - cidr_ipv4: 'string'
                - cidr_ipv6: 'string'
                - prefix_list_id: 'string'
                - referenced_group_info: 'dict'
                - tags:
                    - Key: 'string'
                      Value: 'string'
                - description: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            my-sg-rule:
              aws.ec2.security_group_rule.present:
                - group_id: sg-0dd442ba9f89c5d59
                - is_egress: false
                - ip_protocol: tcp
                - from_port: 60
                - to_port: 60
                - cidr_ipv4: 0.0.0.0/0
                - tags:
                    - Key: test_name5
                      Value: test-rule5
                - description: 'Security group desc'
    """

    result = {
        "comment": [],
        "old_state": None,
        "new_state": None,
        "name": name,
        "result": True,
    }
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.ec2.security_group_rule.get(
            ctx,
            resource_id=resource_id,
        )
    if before and before["result"] and before["ret"]:
        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])
        input_params = {
            "cidr_ipv4": cidr_ipv4,
            "cidr_ipv6": cidr_ipv6,
            "description": description,
            "from_port": from_port,
            "to_port": to_port,
            "group_id": group_id,
            "ip_protocol": ip_protocol,
            "prefix_list_id": prefix_list_id,
            "referenced_group_info": referenced_group_info,
        }

        update_ret = (
            await hub.tool.aws.ec2.security_group_rule.update_security_group_rule(
                ctx,
                before=before["ret"],
                input_params=input_params,
                resource_id=resource_id,
            )
        )

        result["comment"] += update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            for key, value in update_ret["ret"].items():
                plan_state[key] = value
        if not resource_updated:
            result["comment"] += [f"aws.ec2.security_group_rule {name} already exists"]
    else:
        if isinstance(tags, List):
            tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "group_id": group_id,
                    "ip_protocol": ip_protocol,
                    "from_port": from_port,
                    "to_port": to_port,
                    "is_egress": is_egress,
                    "cidr_ipv4": cidr_ipv4,
                    "tags": tags,
                    "description": description,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.security_group_rule", name=name
            )
            return result
        try:
            ip_permissions = []
            ip_perm = {}
            if ip_protocol:
                ip_perm["IpProtocol"] = ip_protocol
            ip_perm["FromPort"] = from_port
            ip_perm["ToPort"] = to_port
            if cidr_ipv4:
                IpRanges = {}
                if description:
                    IpRanges["Description"] = description
                if cidr_ipv4:
                    IpRanges["CidrIp"] = cidr_ipv4
                ip_perm["IpRanges"] = [IpRanges]
            if cidr_ipv6:
                Ipv6Ranges = {}
                if description:
                    Ipv6Ranges["Description"] = description
                if cidr_ipv6:
                    Ipv6Ranges["CidrIpv6"] = cidr_ipv6
                ip_perm["Ipv6Ranges"] = [Ipv6Ranges]
            if prefix_list_id:
                prefix_list = {}
                if description:
                    prefix_list["Description"] = description
                if prefix_list_id:
                    prefix_list["PrefixListId"] = prefix_list_id
                ip_perm["PrefixListIds"] = [prefix_list]
            if referenced_group_info:
                if description:
                    referenced_group_info["Description"] = description
                ip_perm["UserIdGroupPairs"] = [referenced_group_info]
            ip_permissions.append(ip_perm)
            if not is_egress:
                ret = await hub.exec.boto3.client.ec2.authorize_security_group_ingress(
                    ctx,
                    GroupId=group_id,
                    IpPermissions=ip_permissions,
                    TagSpecifications=[
                        {
                            "ResourceType": "security-group-rule",
                            "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                                tags
                            ),
                        }
                    ]
                    if tags
                    else None,
                )
                result["result"] = ret["result"]
                if not ret["result"]:
                    result["comment"] = ret["comment"]
                    return result
                result["comment"] = hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.ec2.security_group_rule", name=name
                )
            else:
                ret = await hub.exec.boto3.client.ec2.authorize_security_group_egress(
                    ctx,
                    GroupId=group_id,
                    IpPermissions=ip_permissions,
                    TagSpecifications=[
                        {
                            "ResourceType": "security-group-rule",
                            "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                                tags
                            ),
                        }
                    ]
                    if tags
                    else None,
                )
                result["result"] = ret["result"]
                if not ret["result"]:
                    result["comment"] = ret["comment"]
                    return result
                result["comment"] = hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.ec2.security_group_rule", name=name
                )
            resource_id = ret["ret"]["SecurityGroupRules"][0]["SecurityGroupRuleId"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.ec2.security_group_rule.get(
                ctx,
                resource_id=resource_id,
            )
            result["new_state"] = after["ret"]
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
    group_id: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Deletes a security group rule.

    Args:

        name(str):
            An Idem name to identify the security group rule resource.

        group_id(str, Optional):
            AWS Security Group ID. Idem automatically considers this resource being absent if this field is not specified.

        resource_id(str, Optional):
            AWS Security Group rule ID. Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [security_group_rule-resource-id]:
              aws.ec2.security_group_rule.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.security_group_rule.absent:
                - name: value
                - group_id: "sg-0008bd25b7867b5cf"
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if (not resource_id) or (not group_id):
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.security_group_rule", name=name
        )
        return result
    resource = await hub.tool.boto3.resource.create(
        ctx, "ec2", "SecurityGroup", group_id
    )
    before = await hub.exec.boto3.client.ec2.describe_security_group_rules(
        ctx, SecurityGroupRuleIds=[resource_id]
    )
    if not before and not before["result"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.security_group_rule", name=name
        )
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.ec2.conversion_utils.convert_raw_sg_rule_to_present(
            raw_resource=before["ret"]["SecurityGroupRules"][0], idem_resource_name=name
        )
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.ec2.security_group_rule", name=name
            )
            return result
        try:
            # checks for egress or ingress using before's output and revoke function needed sg resource
            if not before["ret"]["SecurityGroupRules"][0]["IsEgress"]:
                ret = resource.revoke_ingress(SecurityGroupRuleIds=[resource_id])
                result["result"] = ret["Return"]
                if not result["result"]:
                    result["comment"] += [
                        f"aws.ec2.security_group_rule '{name}' is already in deleted state."
                    ]
                    return result
                result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                    resource_type="aws.ec2.security_group_rule", name=name
                )
            else:
                ret = resource.revoke_egress(SecurityGroupRuleIds=[resource_id])
                result["result"] = ret["Return"]
                if not result["result"]:
                    result["comment"] += [
                        f"aws.ec2.security_group_rule '{name}' is already in deleted state."
                    ]
                    return result
                result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                    resource_type="aws.ec2.security_group_rule", name=name
                )
        except hub.tool.boto3.exception.ClientError as e:
            result["result"] = False
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.security_group_rule
    """
    result = {}

    ret = await hub.exec.boto3.client.ec2.describe_security_group_rules(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe security_group rule {ret['comment']}")
        result["comment"] = ret["comment"]
        result["result"] = False
        return result

    for resource in ret["ret"]["SecurityGroupRules"]:
        resource_id = resource.get("SecurityGroupRuleId")
        resource_translated = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_sg_rule_to_present(
                raw_resource=resource, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.ec2.security_group_rule.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
