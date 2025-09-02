"""State module for managing Elastic Load Balancer V2 target groups."""
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
    protocol: str = None,
    protocol_version: str = None,
    port: int = None,
    vpc_id: str = None,
    health_check_protocol: str = None,
    health_check_port: str = None,
    health_check_enabled: bool = None,
    health_check_path: str = None,
    health_check_interval_seconds: int = None,
    health_check_timeout_seconds: int = None,
    healthy_threshold_count: int = None,
    unhealthy_threshold_count: int = None,
    matcher: make_dataclass(
        """The IDs of the public subnets""" "SubnetMapping",
        [
            ("HttpCode", str, field(default=None)),
            ("GrpcCode", str, field(default=None)),
        ],
    ) = None,
    target_type: str = None,
    tags: Dict[str, str] = None,
    ip_address_type: str = None,
    attributes: make_dataclass(
        """Information about the target group attributes""" "Attribute",
        [
            ("Key", str, field(default=None)),
            ("Value", str, field(default=None)),
        ],
    ) = None,
    targets: List[
        make_dataclass(
            """The type of target""" "Target",
            [
                ("Id", str, field(default=None)),
                ("Port", int, field(default=None)),
                ("AvailabilityZone", str, field(default=None)),
            ],
        )
    ] = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Creates a target group.

    Args:
        name(str): An Idem name of the resource.
            This name must be unique per region per account, can have a maximum of 32 characters, must contain only
            alphanumeric characters or hyphens, and must not begin or end with a hyphen.
        protocol(str, Optional): The protocol to use for routing traffic to the targets.
            1. For Application Load Balancers, the supported protocols are HTTP and HTTPS.
            2. For Network Load Balancers, the supported protocols are TCP, TLS, UDP, or TCP_UDP.
            3. For Gateway Load Balancers, the supported protocol is GENEVE.
            4. A TCP_UDP listener must be associated with a TCP_UDP target group. If the target is a Lambda function,
            this parameter does not apply.
        protocol_version(str, Optional):  [HTTP/HTTPS protocol] The protocol version. Specify GRPC to send requests to
            targets using gRPC. Specify HTTP2 to send requests to targets using HTTP/2. The default is HTTP1 , which
            sends requests to targets using HTTP/1.1.
        port(int, Optional): The port on which the targets receive traffic. This port is used unless you specify a
            port override when registering the target. If the target is a Lambda function, this parameter does not
            apply. If the protocol is GENEVE, the supported port is 6081.
        vpc_id(str, Optional): The identifier of the virtual private cloud (VPC). If the target is a Lambda function,
            this parameter does not apply. Otherwise, this parameter is required.
        health_check_protocol(str, Optional): The protocol the load balancer uses when performing health checks on
            targets. For Application Load Balancers, the default is HTTP. For Network Load Balancers and Gateway
            Load Balancers, the default is TCP. The TCP protocol is not supported for health checks if the protocol of
            the target group is HTTP/HTTPS. GENEVE, TLS, UDP, and TCP_UDP protocols are not supported for health checks.
        health_check_port(str, Optional): The port the load balancer uses when performing health checks on targets.
            If the protocol is HTTP, HTTPS, TCP, TLS, UDP, or TCP_UDP, the default is traffic-port , which is the port
            on which each target receives traffic from the load balancer. If the protocol is GENEVE, default is port 80.
        health_check_enabled(bool, Optional): Indicates whether health checks are enabled. If the target type is
            lambda , health checks are disabled by default but can be enabled. If the target type is instance , ip ,
            or alb , health checks are always enabled and cannot be disabled.
        health_check_path(str, Optional):
            * [HTTP/HTTPS health checks] The destination for health checks on the targets.
            * [HTTP1 or HTTP2 protocol version] The ping path. The default is /.
            * [GRPC protocol version] The path of a custom health check method with the format /package.service/method. The default is /Amazon Web Services.ALB/healthcheck.
        health_check_interval_seconds(int, Optional): The approximate amount of time, in seconds, between health
            checks of an individual target. If the target group protocol is HTTP or HTTPS, the default is 30 seconds.
            If the target group protocol is TCP, TLS, UDP, or TCP_UDP, the supported values are 10 and 30 seconds and
            the default is 30 seconds. If the target group protocol is GENEVE, the default is 10 seconds. If the target
            type is lambda , the default is 35 seconds.
        health_check_timeout_seconds(int, Optional): The amount of time, in seconds, during which no response from a
            target means a failed health check. For target groups with a protocol of HTTP/HTTPS/GENEVE, the default is
            5 seconds. For target groups with a protocol of TCP or TLS, this value must be 6 seconds for HTTP health
            checks and 10 seconds for TCP & HTTPS health checks. If the target type is lambda, default is 30 seconds.
        healthy_threshold_count(int, Optional): The number of consecutive health checks successes required before
            considering an unhealthy target healthy. For target groups with a protocol of HTTP/HTTPS, the default is 5.
            For target groups with a protocol of TCP/TLS/GENEVE, default is 3. If the target type is lambda, default = 5.
        unhealthy_threshold_count(int, Optional): The number of consecutive health check failures required before
            considering a target unhealthy. If the target group protocol is HTTP or HTTPS, the default is 2. If the
            target group protocol is TCP or TLS, this value must be the same as the healthy threshold count. If the
            target group protocol is GENEVE, the default is 3. If the target type is lambda , the default is 2.
        matcher(dict[str, str]), Optional): [HTTP/HTTPS health checks] The HTTP or gRPC codes to use when checking for a successful response from a target.

            * HttpCode(str, Optional):
                For Application Load Balancers, you can specify values between 200 and 499, and the
                default value is 200. You can specify multiple values (for example, "200,202") or a range of values
                (for example, "200-299"). For Network Load Balancers and Gateway Load Balancers, this must be "200–399".
                Note that when using shorthand syntax, some values such as commas need to be escaped.

            * GrpcCode(str, Optional):
                You can specify values between 0 and 99. You can specify multiple values (for example, "0,1") or a range
                of values (for example, "0-5"). The default value is 12.

        target_type(str, Optional):
            The type of target that you must specify when registering targets with this
            target group. You can't specify targets for a target group using more than one target type.

            * instance: Register targets by instance ID. This is the default value.

            * ip: Register targets by IP address. You can specify IP addresses from the subnets of the virtual private
              cloud (VPC) for the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16),
              and the RFC 6598 range (100.64.0.0/10). You can't specify publicly routable IP addresses.

            * lambda: Register a single Lambda function as a target.

            * alb: Register a single Application Load Balancer as a target.
        tags(dict[str, str], Optional): A list of tags to assign to the load balancer. For more information about
            tagging your load balancer, see Tag Your Classic Load Balancer in the Classic Load Balancers Guide.
            Defaults to None.

            * Key (str): The key of the tag.

            * Value (str): The value of the tag.

        ip_address_type(str, Optional):

            The type of IP address used for this target group. The possible values are ipv4
            and ipv6. This is an Optional parameter. If not specified, the IP address type defaults to ipv4.

        attributes(dict[str, str], Optional):
            The load balancer attributes.

            Key (str): The name of the attribute.

            * The following attribute is supported by all load balancers:
                1. 'deregistration_delay.timeout_seconds' - The amount of time, in seconds, for Elastic Load Balancing
                to wait before changing the state of a deregistering target from draining to unused. The range is
                0-3600 seconds. The default value is 300 seconds. If the target is a Lambda function, this
                attribute is not supported.

            * The following attributes are supported by both Application LoadBalancers and Network Load Balancers:
                1. 'stickiness.enabled' - Indicates whether sticky sessions are enabled.
                The value is true or false. The default is false.

                2. 'stickiness.type' - The type of sticky sessions. The possible values are lb_cookie and app_cookie for
                Application Load Balancers or source_ip for Network Load Balancers.

            * The following attributes are supported only if the load balancer is an Application Load Balancer and the target is an instance or an IP address:
                1. 'load_balancing.algorithm.type' - The load balancing algorithm determines how the load balancer
                selects targets when routing requests. The value is round_robin or least_outstanding_requests.
                The default is round_robin.

                2. 'slow_start.duration_seconds' - The time period, in seconds, during which a newly registered target
                receives an increasing share of the traffic to the target group. After this time period ends, the
                target receives its full share of traffic. The range is 30-900 seconds (15 minutes).
                The default is 0 seconds (disabled).

                3. 'stickiness.app_cookie.cookie_name' - Indicates the name of the application-based cookie. Names that
                start with the following prefixes are not allowed: AWSALB , AWSALBAPP , and AWSALBTG ; they're
                reserved for use by the load balancer.

                4. 'stickiness.app_cookie.duration_seconds' - The time period, in seconds, during which requests from a
                client should be routed to the same target. After this time period expires, the application-based
                cookie is considered stale. The range is 1 second to 1 week (604800 seconds).
                The default value is 1 day (86400 seconds).

                5. 'stickiness.lb_cookie.duration_seconds' - The time period, in seconds, during which requests from a
                client should be routed to the same target. After this time period expires, the load
                balancer-generated cookie is considered stale. The range is 1 second to 1 week (604800 seconds).
                The default value is 1 day (86400 seconds).

            * The following attribute is supported only if the load balancer is an Application Load Balancer and the target is a Lambda function:
                1. 'lambda.multi_value_headers.enabled' - Indicates whether the request and response headers that are
                exchanged between the load balancer and the Lambda function include arrays of values or strings.
                The value is true or false. The default is false. If the value is false and the request contains
                a duplicate header field name or query parameter key, the load balancer uses the last value sent by
                the client.

            * The following attributes are supported only by Network Load Balancers:
                1. 'deregistration_delay.connection_termination.enabled' - Indicates whether the load balancer
                terminates connections at the end of the deregistration timeout.
                The value is true or false. The default is false.

                2. 'preserve_client_ip.enabled' - Indicates whether client IP preservation is enabled. The value is true or false. The default is
                disabled if the target group type is IP address and the target group
                protocol is TCP or TLS. Otherwise, the default is enabled. Client IP preservation cannot be
                disabled for UDP and TCP_UDP target groups.

                3. proxy_protocol_v2.enabled' - Indicates whether Proxy Protocol version 2 is enabled. The value is true or false. The default is false.

        targets(list[dict[str, Any]], Optional):
            The targets. If you specified a port override when you registered a
            target, you must specify both the target ID and the port when you de-register it.

            Information about a target.

            * Id(str):
                The ID of the target. If the target type of the target group is instance, specify an instance
                ID. If the target type is ip , specify an IP address. If the target type is lambda , specify the ARN of
                the Lambda function. If the target type is alb , specify the ARN of the Application Load Balancer target.

            * Port(int):
                The port on which the target is listening. If the target group protocol is GENEVE, the
                supported port is 6081. If the target type is alb , the targeted Application Load Balancer must have at
                least one listener whose port matches the target group port. Not used if the target is a Lambda function.

            * AvailabilityZone(str):
                An Availability Zone or all. This determines whether the target receives traffic
                from the load balancer nodes in the specified Availability Zone or from all enabled Availability Zones
                for the load balancer.

                1. This parameter is not supported if the target type of the target group is instance or alb.

                2. If the target type is ip and the IP address is in a subnet of the VPC for the target group, the availability Zone is automatically detected and this parameter is optional. If the IP address is outside the VPC, this parameter is required.

                3. With an Application Load Balancer, if the target type is ip and the IP address is outside the VPC for the target group, the only supported value is all.

                4. If the target type is lambda , this parameter is optional and the only supported value is all.

        resource_id:(str, Optional): The Amazon Resource Name (ARN) of the ElasticLoadBalancingv2 target group.

    Examples:

    .. code-block:: sls

        test_target-group_name:
          aws.elbv2.target_group.present:
            - name: my-target-group
            - protocol: HTTP
            - protocol_version: HTTP2
            - port: 80
            - vpc_id: vpc-3ac0fb5f
            - health_check_protocol: HTTP
            - health_check_port: traffic-port
            - health_check_enabled: True
            - health_check_path: /health-check
            - health_check_interval_seconds: 30
            - health_check_timeout_seconds: 60
            - healthy_threshold_count: 5
            - unhealthy_threshold_count: 2
            - matcher:
              - HttpCode: 200
            - target_type: instance
            - tags:
                name: target-group-name
            - ip_address_type: ipv4
            - targets:
              - Id: i-80c8dd94
                Port: 80
                AvailabilityZone: us-east-1a
            - resource_id: arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    plan_state = {}
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.elbv2.target_group.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        input_map = {
            "protocol": protocol,
            "port": port,
            "vpc_id": vpc_id,
            "health_check_protocol": health_check_protocol,
            "health_check_port": health_check_port,
            "health_check_enabled": health_check_enabled,
            "health_check_interval_seconds": health_check_interval_seconds,
            "health_check_timeout_seconds": health_check_timeout_seconds,
            "healthy_threshold_count": healthy_threshold_count,
            "unhealthy_threshold_count": unhealthy_threshold_count,
            "health_check_path": health_check_path,
            "matcher": matcher,
            "target_type": target_type,
            "protocol_version": protocol_version,
            "ip_address_type": ip_address_type,
            "tags": tags,
            "attributes": attributes,
            "targets": targets,
        }
        update_return = await hub.tool.aws.elbv2.target_group.update(
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
            if update_return["ret"] is not None:
                for updated_value in update_return["ret"]:
                    plan_state[updated_value.get("Key")] = updated_value.get("Value")
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.elbv2.target_group", name=name
                )

            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.elbv2.target_group", name=name
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
                    "protocol": protocol,
                    "protocol_version": protocol_version,
                    "port": port,
                    "vpc_id": vpc_id,
                    "health_check_protocol": health_check_protocol,
                    "health_check_port": health_check_port,
                    "health_check_enabled": health_check_enabled,
                    "health_check_path": health_check_path,
                    "health_check_interval_seconds": health_check_interval_seconds,
                    "health_check_timeout_seconds": health_check_timeout_seconds,
                    "healthy_threshold_count": healthy_threshold_count,
                    "unhealthy_threshold_count": unhealthy_threshold_count,
                    "matcher": matcher,
                    "target_type": target_type,
                    "tags": tags,
                    "targets": targets,
                    "attributes": attributes,
                    "ip_address_type": ip_address_type,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.elbv2.target_group", name=name
            )
            return result
        ret = await hub.exec.boto3.client.elbv2.create_target_group(
            ctx,
            Name=name,
            Protocol=protocol,
            ProtocolVersion=protocol_version,
            Port=port,
            VpcId=vpc_id,
            HealthCheckProtocol=health_check_protocol,
            HealthCheckPort=health_check_port,
            HealthCheckEnabled=health_check_enabled,
            HealthCheckPath=health_check_path,
            HealthCheckIntervalSeconds=health_check_interval_seconds,
            HealthCheckTimeoutSeconds=health_check_timeout_seconds,
            HealthyThresholdCount=healthy_threshold_count,
            UnhealthyThresholdCount=unhealthy_threshold_count,
            Matcher=matcher,
            TargetType=target_type,
            Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
            IpAddressType=ip_address_type,
        )
        if not ret["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        resource_id = (ret["ret"]["TargetGroups"][0]).get("TargetGroupArn")
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.elbv2.target_group", name=name
        )
        if targets:
            register_targets = await hub.exec.boto3.client.elbv2.register_targets(
                ctx,
                TargetGroupArn=resource_id,
                Targets=targets,
            )
            if not register_targets["result"]:
                result["comment"] += register_targets["comment"]
                result["result"] = False
                return result
            result["comment"] += ["Registered Targets."]
        if attributes:
            modify_attributes = (
                await hub.exec.boto3.client.elbv2.modify_target_group_attributes(
                    ctx,
                    TargetGroupArn=resource_id,
                    Attributes=attributes,
                )
            )
            if not modify_attributes["result"]:
                result["comment"] += modify_attributes["comment"]
                result["result"] = False
                return result
            result["comment"] += ["Added Attributes."]

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif not (before and before["result"]) or resource_updated:
        after = await hub.exec.aws.elbv2.target_group.get(
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

    Deletes the specified target group.

    You can delete a target group if it is not referenced by any actions. Deleting a target group also deletes any
    associated health checks. Deleting a target group does not affect its registered targets. For example, any EC2
    instances continue to run until you stop or terminate them.

    Args:
        name(str): Idem name of the load balancer.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of ElasticLoadBalancingv2 Target Group. If the
        target group does not exist or has already been deleted, the call still succeeds.

    Examples:
        .. code-block:: sls

            test_load-balancer_name:
                aws.elbv2.target_group.absent:
                  - name: my-load-balancer
                  - resource_id: arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.elbv2.target_group", name=name
        )
        return result
    before = await hub.exec.aws.elbv2.target_group.get(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.elbv2.target_group", name=name
        )
    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.elbv2.target_group", name=name
            )
            return result
        else:
            ret = await hub.exec.boto3.client.elbv2.delete_target_group(
                ctx, TargetGroupArn=resource_id
            )
            if not ret["result"]:
                result["comment"] = before["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.elbv2.target_group", name=name
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describes the resource in a way that can be recreated/managed with the corresponding "present" function
    By default, all target groups are described.

    Examples:

    .. code-block:: bash

        $ idem describe aws.elbv2.target_group
    """
    result = {}
    ret = await hub.exec.boto3.client.elbv2.describe_target_groups(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.elbv2.target_group: {ret['comment']}")
        return result
    if ret["ret"].get("TargetGroups"):
        for target_group in ret["ret"].get("TargetGroups"):
            tags_ret = await hub.exec.boto3.client.elbv2.describe_tags(
                ctx, ResourceArns=[target_group.get("TargetGroupArn")]
            )
            if not tags_ret["result"]:
                # Error fetching tags. If fetching tags itself fails, just skip this and continue. Since tags are
                # optional, they need not be associated with all load balancers. But API needs to succeed.
                hub.log.warning(
                    f"Failed listing tags for aws.elbv2.target_group '{target_group.get('TargetGroupArn')}'"
                    f"Describe will skip this aws.elbv2.target_group and continue."
                )
                continue

            tags = []
            if tags_ret.get("ret") and tags_ret.get("ret")["TagDescriptions"]:
                tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    tags_ret.get("ret").get("TagDescriptions")[0].get("Tags")
                )

            attributes_ret = (
                await hub.exec.boto3.client.elbv2.describe_target_group_attributes(
                    ctx, TargetGroupArn=target_group.get("TargetGroupArn")
                )
            )
            if not attributes_ret["result"]:
                # Error fetching attributes (Attributes are optional. Not every load_balancer needs to have them.)
                hub.log.warning(
                    f"Failed listing attributes for aws.elbv2.target_group '{target_group.get('TargetGroupArn')}'"
                    f"Describe will skip this aws.elbv2.target_group and continue. "
                )
                continue

            attributes = []
            if attributes_ret.get("ret") and attributes_ret.get("ret").get(
                "Attributes"
            ):
                attributes = attributes_ret["ret"].get("Attributes")

            targets_ret = await hub.exec.boto3.client.elbv2.describe_target_health(
                ctx, TargetGroupArn=target_group.get("TargetGroupArn")
            )
            if not targets_ret["result"]:
                # Error fetching attributes (Attributes are optional. Not every load_balancer needs to have them.)
                hub.log.warning(
                    f"Failed listing targets for aws.elbv2.target_group '{target_group.get('TargetGroupArn')}'"
                    f"Describe will skip this aws.elbv2.target_group and continue. "
                )
                continue

            targets = []
            if targets_ret.get("ret") and targets_ret.get("ret").get(
                "TargetHealthDescriptions"
            ):
                targets = targets_ret.get("ret").get("TargetHealthDescriptions")

            resource_converted = (
                hub.tool.aws.elbv2.conversion_utils.convert_raw_target_group_to_present(
                    raw_resource=target_group,
                    idem_resource_name=target_group.get("TargetGroupName"),
                    tags=tags,
                    attributes=attributes,
                    targets=targets,
                )
            )
            result[resource_converted["resource_id"]] = {
                "aws.elbv2.target_group.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_converted.items()
                ]
            }
    return result
