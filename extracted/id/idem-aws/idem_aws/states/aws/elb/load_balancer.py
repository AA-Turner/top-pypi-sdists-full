"""State module for managing Amazon Elastic Load Balancing."""
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
    listeners: List[
        make_dataclass(
            """Information about a listener.""" "Listener",
            [
                ("Protocol", str),
                ("LoadBalancerPort", int),
                ("InstancePort", int),
                ("InstanceProtocol", str, field(default=None)),
                ("SSLCertificateId", str, field(default=None)),
            ],
        )
    ],
    availability_zones: List[str] = None,
    subnets: List[str] = None,
    security_groups: List[str] = None,
    scheme: str = None,
    instances: List[
        make_dataclass(
            """The ID of an EC2 instance.""" "Instance",
            [
                ("InstanceId", str, field(default=None)),
            ],
        )
    ] = None,
    load_balancer_attributes: make_dataclass(
        "LoadBalancerAttributes",
        [
            (
                "CrossZoneLoadBalancing",
                make_dataclass(
                    "CrossZoneLoadBalancing",
                    [("Enabled", bool, field(default=False))],
                ),
            ),
            (
                "AccessLog",
                make_dataclass(
                    "AccessLog",
                    [
                        ("Enabled", bool, field(default=False)),
                        ("S3BucketName", str, field(default=None)),
                        ("EmitInterval", int, field(default=60)),
                        ("S3BucketPrefix", str, field(default=None)),
                    ],
                ),
            ),
            (
                "ConnectionDraining",
                make_dataclass(
                    "ConnectionDraining",
                    [
                        ("Timeout", int),
                        ("Enabled", bool, field(default=False)),
                    ],
                ),
            ),
            (
                "ConnectionSettings",
                make_dataclass(
                    "ConnectionSettings",
                    [
                        ("IdleTimeout", int),
                    ],
                ),
            ),
            (
                "AdditionalAttributes",
                List[
                    make_dataclass(
                        "AdditionalAttributes",
                        [
                            ("Key", str, field(default=None)),
                            ("Value", str, field(default=None)),
                        ],
                    )
                ],
            ),
        ],
    ) = None,
    tags: Dict[str, str] = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Create an Elastic Load Balancer in AWS.

    Creates a Classic Load Balancer. You can add listeners, security groups, subnets, and tags when you create your
    load balancer, or you can add them later using this present function with a resource_id.

    You can create up to 20 load balancers per region per account.

    Args:
        name(str): The name of the load balancer. This name must be unique within your set of load balancers for the
            region, must have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and
            cannot begin or end with a hyphen.

        listeners(list[dict[str, Any]]): Information about a listener.

            * Protocol (str):
                The load balancer transport protocol to use for routing: HTTP, HTTPS, TCP, or SSL.
            * LoadBalancerPort (int):
                The port on which the load balancer is listening. On EC2-VPC, you can specify any port from the
                range 1-65535. On EC2-Classic, you can specify any port from the following list: 25, 80, 443, 465,
                587, 1024-65535.
            * InstanceProtocol (str, Optional):
                1. The protocol to use for routing traffic to instance: HTTP, HTTPS, TCP, or SSL. If the front-end
                protocol is TCP or SSL, the back-end protocol must be TCP or SSL. If the front-end protocol is HTTP
                or HTTPS, the back-end protocol must be HTTP or HTTPS.

                2. If there is another listener with the same InstancePort whose InstanceProtocol is secure,
                (HTTPS or SSL), the listener's InstanceProtocol must also be secure.

                3. If there is another listener with the same InstancePort whose InstanceProtocol is HTTP or TCP,
                the listener's InstanceProtocol must be HTTP or TCP.
            * InstancePort (int):
                The port on which the instance is listening.
            * SSLCertificateId (str, Optional):
                The Amazon Resource Name (ARN) of the server certificate.

        availability_zones(list, Optional):
            One or more Availability Zones from the same region as the load balancer. You must specify at least one
            Availability Zone. You can add more Availability Zones after you create the load balancer using
            EnableAvailabilityZonesForLoadBalancer.

        subnets(list, Optional):
            The IDs of the subnets in your VPC to attach to the load balancer. Specify one subnet per Availability Zone
            specified in AvailabilityZones.

        security_groups(list, Optional): The IDs of the security groups to assign to the load balancer.

        scheme(str, Optional): Given load balance type. Valid only for load balancers in a VPC.

        instances(list, Optional):
            The IDs of the instances.
                * (dict): The ID of an EC2 instance.

        load_balancer_attributes(dict, Optional):
            The attributes for the load balancer.
                * CrossZoneLoadBalancing(dict): If enabled, the load balancer routes the request traffic evenly across all instances regardless of the Availability Zones. Enabled (bool): Specifies whether cross-zone load balancing is enabled for the load balancer.
                * AccessLog(dict, Optional): If enabled, the load balancer captures detailed information of all requests and delivers the information to the Amazon S3 bucket that you specify.
                    * Enabled(bool): Specifies whether access logs are enabled for the load balancer.
                    * S3BucketName(str, Optional): The name of the Amazon S3 bucket where the access logs are stored.
                    * EmitInterval(int, Optional): The interval for publishing the access logs. You can specify an interval of either 5 minutes or 60 minutes. Default: 60 minutes
                    * S3BucketPrefix(str, Optional): The logical hierarchy you created for your Amazon S3 bucket, for example my-bucket-prefix/prod . If the prefix is not provided, the log is placed at the root level of the bucket.
                * ConnectionDraining(dict[int, bool], Optional): If enabled, the load balancer allows existing requests to complete before the load balancer shifts traffic away from a deregistered or unhealthy instance.
                    * Enabled(bool): Specifies whether connection draining is enabled for the load balancer.
                    * Timeout(int, Optional): The maximum time, in seconds, to keep the existing connections open before unregistering the instances.
                    * ConnectionSettings(dict): If enabled, the load balancer allows the connections to remain idle (no data is sent over the connection) for the specified duration.
                    * IdleTimeout(int): The time, in seconds, that the connection is allowed to be idle (no data has been sent over the connection) before it is closed by the load balancer.
                * AdditionalAttributes (list[dict[str, Any]], Optional): Any additional attributes.
                    Information about additional load balancer attributes.
                        * Key (str): The name of the attribute. The following attribute is supported.
                            elb.http.desyncmitigationmode - Determines how the load balancer handles requests that might
                            pose a security risk to your application. The possible values are monitor, defensive,
                            and strictest . The default is defensive.
                        * Value (str, Optional): This value of the attribute.

        tags(dict[str, str], Optional):
            The tags to assign to the load balancer.
                * Key (str): The key of the tag.
                * Value (str, Optional): The value of the tag.

        resource_id(str, Optional): AWS ELB load balancer name.

    Examples:

    Using in a state:

    .. code-block:: sls

        test_load-balancer_name:
            aws.elb.load_balancer.present
            - name: my-load-balancer
            - resource_id: my-load-balancer
            - listeners:
              - InstancePort: 80
              - InstanceProtocol: HTTP
              - LoadBalancerPort: 80
              - Protocol: HTTP
            - tags:
                name: my-load-balancer
            - availability_zones:
              - us-west-2a
            - subnets:
              - subnet-15aaab61
            - security_groups:
              - sg-a61988c378fgtyu
            - scheme: internal
            - instances:
              - i-d6f6f34tyu78ae3
              - i-207d9vbty56u717
              - i-afefvbu90ipb49b
            - load_balancer_attributes:
                CrossZoneLoadBalancing:
                    - Enabled: True

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    plan_state = {}
    before = None
    resource_updated = False
    input_map = {
        "LoadBalancerName": name,
        "Listeners": listeners,
        "Subnets": subnets,
        "AvailabilityZones": availability_zones,
        "LoadBalancerAttributes": load_balancer_attributes,
        "SecurityGroups": security_groups,
        "Scheme": scheme,
        "Tags": tags,
        "Instances": instances,
    }
    if resource_id:
        before = await hub.exec.aws.elb.load_balancer.get(
            ctx=ctx, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        update_return = await hub.tool.aws.elb.load_balancer.update(
            ctx=ctx,
            name=name,
            current_state=before["ret"],
            input_map=input_map,
            plan_state=plan_state,
            resource_id=resource_id,
        )
        result["comment"] = update_return["comment"]
        if not update_return["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_return["ret"])
        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += list(
                    hub.tool.aws.comment_utils.would_update_comment(
                        resource_type="aws.elb.load_balancer", name=name
                    )
                )
            else:
                result["comment"] += list(
                    hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.elb.load_balancer", name=name
                    )
                )

        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_tags = await hub.tool.aws.elb.tag.update(
                ctx=ctx,
                resource_id=resource_id,
                old_tags=result["old_state"]["tags"],
                new_tags=tags,
            )
            result["comment"] += list(update_tags["comment"])
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
                    "listeners": listeners,
                    "availability_zones": availability_zones,
                    "subnets": subnets,
                    "security_groups": security_groups,
                    "scheme": scheme,
                    "instances": instances,
                    "load_balancer_attributes": load_balancer_attributes,
                    "tags": tags,
                    "resource_id": name,
                },
            )
            result["comment"] = list(
                hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.elb.load_balancer", name=name
                )
            )
            return result
        ret = await hub.tool.aws.elb.load_balancer.create(
            ctx=ctx,
            input_map=input_map,
        )
        if not ret["result"] and not ret["ret"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = list(
            hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.elb.load_balancer", name=name
            )
        )
        resource_id = name
        result["comment"] += ret["comment"]

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.elb.load_balancer.get(
            ctx=ctx, resource_id=resource_id
        )
        if not after["result"] or not after["ret"]:
            result["result"] = False
            result["comment"] += list(after["comment"])
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
    Deletes the specified load balancer.

    If the load balancer does not exist or has already been deleted, the call still succeeds.

    Args:
        name(str): Idem name of the load balancer.
        resource_id(str, Optional): AWS ELB load balancer name. Idem automatically considers this resource being absent if this field is not specified.


    Examples:

    Using in a state:

    .. code-block:: sls

        test_load-balancer_name:
            aws.elb.load_balancer.absent:
                - name: my-load-balancer
                - resource_id: my-load-balancer

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.elb.load_balancer", name=name
            )
        )
        return result
    before = await hub.exec.aws.elb.load_balancer.get(ctx=ctx, resource_id=resource_id)
    if not before["result"]:
        result["comment"] = list(before["comment"])
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.elb.load_balancer", name=name
            )
        )
    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = list(
                hub.tool.aws.comment_utils.would_delete_comment(
                    resource_type="aws.elb.load_balancer", name=name
                )
            )
            return result
        else:
            ret = await hub.exec.boto3.client.elb.delete_load_balancer(
                ctx, LoadBalancerName=resource_id
            )
            if not ret["result"]:
                result["comment"] = list(ret["comment"])
                result["result"] = False
                return result
            result["comment"] = list(
                hub.tool.aws.comment_utils.delete_comment(
                    resource_type="aws.elb.load_balancer", name=name
                )
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.
    This call describes all of your load balancers.

    Examples:

    .. code-block:: bash

        $ idem describe aws.elb.load_balancer
    """
    result = {}
    ret = await hub.exec.boto3.client.elb.describe_load_balancers(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.elb.load_balancer: {ret['comment']}")
        return result
    if ret["ret"].get("LoadBalancerDescriptions"):
        for load_balancer in ret["ret"]["LoadBalancerDescriptions"]:
            tags_ret = await hub.exec.boto3.client.elb.describe_tags(
                ctx, LoadBalancerNames=[load_balancer["LoadBalancerName"]]
            )
            if not tags_ret["result"]:
                # Error fetching tags. If fetching tags itself fails, just skip this and continue. Since tags are
                # Optional, they need not be associated with all load balancers. But API needs to succeed.
                hub.log.warning(
                    f"Failed listing tags for aws.elb.load_balancer '{load_balancer['LoadBalancerName']}' "
                    f"with error: {tags_ret['comment']}"
                    f"Describe will skip this aws.elb.load_balancer resource and continue."
                )
                continue

            tags = []
            if tags_ret.get("ret") and tags_ret.get("ret")["TagDescriptions"]:
                tags = (tags_ret["ret"]["TagDescriptions"][0]).get("Tags")

            attributes_ret = (
                await hub.exec.boto3.client.elb.describe_load_balancer_attributes(
                    ctx, LoadBalancerName=load_balancer["LoadBalancerName"]
                )
            )
            if not attributes_ret["result"]:
                # Error fetching attributes (Attributes are Optional. Not every load_balancer needs to have them.)
                hub.log.warning(
                    f"Failed listing attributes for aws.elb.load_balancer '{load_balancer.get('LoadBalancerName')}' "
                    f"with error: {attributes_ret['comment']}"
                    f"Describe will skip this aws.elb.load_balancer resource and continue."
                )
                continue

            attributes = []
            if attributes_ret.get("ret") and attributes_ret.get("ret").get(
                "LoadBalancerAttributes"
            ):
                attributes = attributes_ret["ret"]["LoadBalancerAttributes"]

            resource_converted = (
                hub.tool.aws.elb.conversion_utils.convert_raw_load_balancer_to_present(
                    raw_resource=load_balancer,
                    idem_resource_name=load_balancer["LoadBalancerName"],
                    tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
                    attributes=attributes,
                )
            )
            result[resource_converted["resource_id"]] = {
                "aws.elb.load_balancer.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_converted.items()
                ]
            }
    return result
