"""State module for managing Amazon Elastic Load Balancing V2."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    subnets: List[str] = None,
    subnet_mappings: List[
        make_dataclass(
            """The IDs of the public subnets.""" "SubnetMapping",
            [
                ("SubnetId", str, field(default=None)),
                ("AllocationId", str, field(default=None)),
                ("PrivateIPv4Address", str, field(default=None)),
                ("IPv6Address", str, field(default=None)),
            ],
        )
    ] = None,
    security_groups: List[str] = None,
    scheme: str = None,
    tags: Dict[str, str] = None,
    lb_type: str = None,
    ip_address_type: str = None,
    customer_owned_ipv4_pool: str = None,
    attributes: List[
        make_dataclass(
            """Describes the attributes for the specified Application Load Balancer, Network Load Balancer, or Gateway Load Balancer."""
            "Attribute",
            [
                ("Key", str, field(default=None)),
                ("Value", str, field(default=None)),
            ],
        )
    ] = None,
) -> Dict[str, Any]:
    """
    Creates an Application Load Balancer, Network Load Balancer, or Gateway Load Balancer in AWS.

    Args:
        name(str): An Idem name to identify load balancer. This name must be unique per region per account, can have a
            maximum of 32 characters, must contain only alphanumeric characters or hyphens, must not begin or end with
            a hyphen, and must not begin with "internal-"
        subnets(list, Optional): The IDs of the public subnets. You can specify only one subnet per Availability Zone.
            You must specify either subnets or subnet mappings, but not both. To specify an Elastic IP address, specify
            subnet mappings instead of subnets.

            * [Application Load Balancers]
                You must specify subnets from at least two Availability Zones.
            * [Application Load Balancers on Outposts]
                You must specify one Outpost subnet.
            * [Application Load Balancers on Local Zones]
                You can specify subnets from one or more Local Zones.
            * [Network Load Balancers]
                You can specify subnets from one or more Availability Zones.
            * [Gateway Load Balancers]
                You can specify subnets from one or more Availability Zones.
        subnet_mappings([list[dict[str, Any]]): The IDs of the public subnets. You can specify only one subnet per
            Availability Zone. You must specify either subnets or subnet mappings, but not both.

            * [Application Load Balancers]
                You must specify subnets from at least two Availability Zones. You cannot specify Elastic IP addresses for your subnets.
            * [Application Load Balancers on Outposts]
                You must specify one Outpost subnet.
            * [Application Load Balancers on Local Zones]
                You can specify subnets from one or more Local Zones.
            * [Network Load Balancers]
                You can specify subnets from one or more Availability Zones. You can specify one
                Elastic IP address per subnet if you need static IP addresses for your internet-facing load balancer.
                For internal load balancers, you can specify one private IP address per subnet from the IPv4 range of the subnet.
                For internet-facing load balancer, you can specify one IPv6 address per subnet.
            * [Gateway Load Balancers]
                You can specify subnets from one or more Availability Zones. You cannot specify
                Elastic IP addresses for your subnets.

                * SubnetId (str, Optional): The ID of the subnet.
                * AllocationId (str, Optional):
                    [Network Load Balancers] The allocation ID of the Elastic IP address  for an internet-facing load balancer.
                * PrivateIPv4Address (str, Optional):
                    [Network Load Balancers] The private IPv4 address for an internal load balancer.
                * IPv6Address (str, Optional):
                    [Network Load Balancers] The IPv6 address.
        security_groups(list): [Application Load Balancers] The IDs of the security groups for the load balancer.
        scheme(str, Optional): The nodes of an Internet-facing load balancer have public IP addresses. The DNS name of
            an Internet-facing load balancer is publicly resolvable to the public IP addresses of the nodes. Therefore,
            Internet-facing load balancers can route requests from clients over the internet.

            The nodes of an internal load balancer have only private IP addresses. The DNS name of an internal load
            balancer is publicly resolvable to the private IP addresses of the nodes. Therefore, internal load balancers
            can route requests only from clients with access to the VPC for the load balancer.

            The default is an Internet-facing load balancer. You cannot specify a scheme for a Gateway Load Balancer.
        tags([dict[str, str], Optional): The tags to assign to the load balancer. Defaults to None.

            * Key (str): The key of the tag.
            * Value (str, Optional): The value of the tag.
        lb_type(str, Optional): The type of load balancer. The default is application.
        ip_address_type(str, Optional): The type of IP addresses used by the subnets for your load balancer. The
            possible values are ipv4 (for IPv4 addresses) and dualstack (for IPv4 and IPv6 addresses).
        customer_owned_ipv4_pool(str, Optional): [Application Load Balancers on Outposts] The ID of the customer-owned
            address pool (CoIP pool).
        attributes(dict):
            The load balancer attributes.
                * Key (str):
                    The name of the attribute.
                        * Attributes supported by all load balancers.
                            1. 'deletion_protection.enabled' - Indicates whether deletion protection is enabled. The value is true or false. The default is false.

                        * The following attributes are supported by both Application Load Balancers and Network Load Balancers:
                            1. 'access_logs.s3.enabled' - Indicates whether access logs are enabled. The value is true or false.
                               The default is false .
                            2. 'access_logs.s3.bucket' - The name of the S3 bucket for the access logs. This attribute is required
                               if access logs are enabled. The bucket must exist in the same region as the load balancer and have a
                               bucket policy that grants Elastic Load Balancing permissions to write to the bucket.
                            3. 'access_logs.s3.prefix' - The prefix for the location in the S3 bucket for the access logs.
                            4. 'ipv6.deny_all_igw_traffic' - Blocks internet gateway (IGW) access to the load balancer. It is set
                               to false for internet-facing load balancers and true for internal load balancers, preventing
                               unintended access to your internal load balancer through an internet gateway.

                        * The following attributes are supported by only Application Load Balancers:
                            1. 'idle_timeout.timeout_seconds' - The idle timeout value, in seconds. The valid range is 1-4000
                               seconds. The default is 60 seconds.
                            2. 'routing.http.desync_mitigation_mode' - Determines how the load balancer handles requests that might
                               pose a security risk to your application. The possible values are monitor, defensive, and strictest.
                               The default is defensive .
                            3. 'routing.http.drop_invalid_header_fields.enabled' - Indicates whether HTTP headers with invalid
                               header fields are removed by load balancer(true) or routed to target(s) (false). Default is false.
                            4. 'routing.http.preserve_host_header.enabled' - Indicates whether the Application Load Balancer should
                               preserve the Host header in the HTTP request and send it to the target without any change. The
                               possible values are true and false. The default is false.
                            5. 'routing.http.x_amzn_tls_version_and_cipher_suite.enabled' - Indicates whether the two headers
                               (x-amzn-tls-version and x-amzn-tls-cipher-suite ), which contain information about the negotiated TLS
                               version and cipher suite, are added to the client request before sending it to the target. The
                               x-amzn-tls-version header has information about the TLS protocol version negotiated with the client,
                               and the x-amzn-tls-cipher-suite header has information about the cipher suite negotiated with the
                               client. Both headers are in OpenSSL format. The possible values for the attribute are true and false.
                               The default is false.
                            6. 'routing.http.xff_client_port.enabled' - Indicates whether the X-Forwarded-For header should preserve
                               the source port that the client used to connect to the load balancer. The possible values are true
                               and false . The default is false .
                            7. 'routing.http.xff_header_processing.mode' - Enables you to modify, preserve, or remove the
                               X-Forwarded-For header in the HTTP request before the Application Load Balancer sends the request to
                               the target. The possible values: append, preserve, and remove. The default is 'append'.

                               If the value is 'append', the Application Load Balancer adds the client IP address (of the last hop)
                               to the X-Forwarded-For header in the HTTP request before it sends it to targets.

                               If the value is 'preserve' the Application Load Balancer preserves the X-Forwarded-For header in the
                               HTTP request, and sends it to targets without any change.

                               If the value is 'remove', Application Load Balancer removes the X-Forwarded-For header in the HTTP
                               request before it sends it to targets.
                            8. 'routing.http2.enabled' - Indicates whether HTTP/2 is enabled. The possible values are true & false.
                               The default is true . Elastic Load Balancing requires that message header names contain only
                               alphanumeric characters and hyphens.
                            9. 'waf.fail_open.enabled' - Indicates whether to allow a WAF-enabled load balancer to route requests to
                               target(s) if it is unable to forward the request to Amazon Web Services WAF. The possible values are
                               true and false. The default is false.

                        * The following attribute is supported by Network Load Balancers and Gateway Load Balancers:
                            1. 'load_balancing.cross_zone.enabled' - Indicates whether cross-zone load balancing is enabled. The
                               possible values are true and false. The default is false.
                * Value (str): The value of the attribute.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the load balancer.


    Examples:

    Using in a state:

    .. code-block:: yaml

        test_load-balancer_name:
            aws.elbv2.load_balancer.present:
                - name: my-load-balancer
                - resource_id: arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188
                - tags:
                    name: load-balancer-name
                - availability_zones:
                  - us-west-2a
                - subnets:
                  - subnet-15aaab61
                - security_groups:
                  - sg-a61988c3
                - scheme: internal

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    plan_state = {}
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.elbv2.load_balancer.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        update = {
            "LoadBalancerName": name,
            "Subnets": subnets,
            "SubnetMappings": subnet_mappings,
            "SecurityGroups": security_groups,
            "Scheme": scheme,
            "Tags": tags,
            "Type": lb_type,
            "IpAddressType": ip_address_type,
            "CustomerOwnedIpv4Pool": customer_owned_ipv4_pool,
            "Attributes": attributes,
        }
        update_return = await hub.tool.aws.elbv2.load_balancer.update(
            ctx=ctx,
            current_state=before["ret"],
            input_map=update,
            plan_state=plan_state,
            resource_id=resource_id,
        )
        result["comment"] = update_return["comment"]
        if not update_return["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_return["ret"])
        if resource_updated:
            if update_return["ret"] is not None:
                for updated_value in update_return["ret"]:
                    plan_state[updated_value.get("Key")] = updated_value.get("Value")
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.elbv2.load_balancer", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.elbv2.load_balancer", name=name
                )

        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_tags = await hub.tool.aws.elbv2.tag.update(
                ctx=ctx,
                resource_id=resource_id,
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_tags["comment"]
            result["result"] = update_tags["result"]
            resource_updated = resource_updated or bool(update_tags["ret"])
            if ctx.get("test", False) and update_tags["ret"]:
                plan_state["tags"] = update_tags["ret"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "subnets": subnets,
                    "subnet_mappings": subnet_mappings,
                    "security_groups": security_groups,
                    "scheme": scheme,
                    "tags": tags,
                    "lb_type": lb_type,
                    "ip_address_type": ip_address_type,
                    "customer_owned_ipv4_pool": customer_owned_ipv4_pool,
                    "attributes": attributes,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.elbv2.load_balancer", name=name
            )
            return result
        ret = await hub.exec.boto3.client.elbv2.create_load_balancer(
            ctx,
            Name=name,
            Subnets=subnets,
            SubnetMappings=subnet_mappings,
            SecurityGroups=security_groups,
            Scheme=scheme,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
            Type=lb_type,
            IpAddressType=ip_address_type,
            CustomerOwnedIpv4Pool=customer_owned_ipv4_pool,
        )
        if not ret["result"] and not ret["ret"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        resource_id = (ret["ret"]["LoadBalancers"][0]).get("LoadBalancerArn")
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.elbv2.load_balancer", name=name
        )
        if attributes:
            attributes_update = (
                await hub.exec.boto3.client.elbv2.modify_load_balancer_attributes(
                    ctx,
                    LoadBalancerArn=resource_id,
                    Attributes=attributes,
                )
            )
            if not attributes_update["result"]:
                result["comment"] += attributes_update["comment"]
                result["result"] = False
                return result
            result["comment"] += ["Modified Attributes."]

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif not (before and before["result"]) or resource_updated:
        after = await hub.exec.aws.elbv2.load_balancer.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not after["result"] or not after["ret"]:
            result["result"] = False
            result["comment"] += after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    1. Deletes the specified Application Load Balancer, Network Load Balancer, or Gateway Load Balancer. Deleting a
       load balancer also deletes its listeners.
    2. You can't delete a load balancer if deletion protection is enabled. If the load balancer does not exist or has
       already been deleted, the call succeeds.
    3. Deleting a load balancer does not affect its registered targets. For example, your EC2 instances continue to run
       and are still registered to their target groups. If you no longer need these EC2 instances, you can stop or
       terminate them.

    Args:
        name(str): Idem name of the load balancer.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the load balancer. Idem automatically considers this resource being absent if this field is not specified.

    Examples:

    Using in a state:

    .. code-block:: sls

        test_load-balancer_name:
            aws.elbv2.load_balancer.absent:
              - name: my-load-balancer
              - resource_id: arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.elbv2.load_balancer", name=name
        )
        return result
    before = await hub.exec.aws.elbv2.load_balancer.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.elbv2.load_balancer", name=name
        )
    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.elbv2.load_balancer", name=name
            )
            return result
        else:
            ret = await hub.exec.boto3.client.elbv2.delete_load_balancer(
                ctx, LoadBalancerArn=resource_id
            )
            if not ret["result"]:
                result["comment"] += ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.elbv2.load_balancer", name=name
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function
    Lists out all load balancers.

    Examples:

    Using in command line:

    .. code-block:: bash

        $ idem describe aws.elbv2.load_balancer
    """
    result = {}
    ret = await hub.exec.boto3.client.elbv2.describe_load_balancers(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.elbv2.load_balancer: {ret['comment']}")
        return result
    if ret["ret"].get("LoadBalancers"):
        for load_balancer in ret["ret"].get("LoadBalancers"):
            tags_ret = await hub.exec.boto3.client.elbv2.describe_tags(
                ctx, ResourceArns=[load_balancer.get("LoadBalancerArn")]
            )
            if not tags_ret["result"]:
                # Error fetching tags. If fetching tags itself fails, just skip this and continue. Since tags are
                # Optional, they need not be associated with all load balancers. But API needs to succeed.
                hub.log.warning(
                    f"Failed listing tags for aws.elbv2.load_balancer '{load_balancer.get('LoadBalancerArn')}'"
                    f"Describe will skip this aws.elbv2.load_balancer and continue. "
                )
                continue

            tags = []
            if tags_ret.get("ret") and tags_ret.get("ret")["TagDescriptions"]:
                tags = (tags_ret.get("ret").get("TagDescriptions")[0]).get("Tags")

            attributes_ret = (
                await hub.exec.boto3.client.elbv2.describe_load_balancer_attributes(
                    ctx, LoadBalancerArn=load_balancer.get("LoadBalancerArn")
                )
            )
            if not attributes_ret["result"]:
                # Error fetching attributes (Attributes are Optional. Not every load_balancer needs to have them.)
                hub.log.warning(
                    f"Failed listing attributes for aws.elbv2.load_balancer '{load_balancer.get('LoadBalancerArn')}'"
                    f"Describe will skip this aws.elbv2.load_balancer and continue. "
                )
                continue

            attributes = []
            if attributes_ret.get("ret") and attributes_ret.get("ret").get(
                "Attributes"
            ):
                attributes = attributes_ret["ret"].get("Attributes")

            resource_converted = hub.tool.aws.elbv2.conversion_utils.convert_raw_load_balancer_to_present(
                raw_resource=load_balancer,
                idem_resource_name=load_balancer.get("LoadBalancerName"),
                tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
                attributes=attributes,
            )
            result[resource_converted["resource_id"]] = {
                "aws.elbv2.load_balancer.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_converted.items()
                ]
            }
    return result
