"""
Functions for interacting with an instance based on its ID
"""
import copy
import itertools
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


DEFAULT_SSH_PORT = 22
DEFAULT_TUNNEL_PLUGIN = "asyncssh"


def __init__(hub):
    hub.pop.sub.add(dyne_name="heist")


async def bootstrap(
    hub,
    ctx,
    instance_id,
    *,
    username: str = None,
    host: str = None,
    port: int = DEFAULT_SSH_PORT,
    ssh_public_key: str = None,
    ssh_private_key: str = None,
    availability_zone: str = None,
    heist_manager: str,
    artifact_version: str = None,
    tunnel_plugin: str = DEFAULT_TUNNEL_PLUGIN,
    auto_configure: bool = False,
    verify: bool = True,
    **kwargs,
):
    """Connect to the instance with an ssh keypair and call heist to bootstrap it.

    If an ssh keypair is not provided one will be created.

    Args:
        instance_id:
            An AWS EC2 Instance ID.

        username(str, Optional):
            The instance OS username to use in the connection, Defaults to ec2-user.

        host(str, Optional):
            The public ip address or dns name of the instance.  Defaults to autodetect.

        port(int, Optional):
            The port to connect to on the host.  Defaults to 22.

        ssh_public_key(str, Optional):
            A public ssh key or path to send to the instance.

        ssh_private_key(str, Optional):
            A private ssh key or path to send to the instance.

        availability_zone(str, Optional):
            The Availability Zone in which the EC2 instance was launched.

        heist_manager(str, Required):
            The heist manager to use to bootstrap the instance (I.E. salt.minion).

        artifact_version(str, Optional):
            The version of the heist_manager's artifact to upload to the instance, Defaults to latest.

        tunnel_plugin(str, Optional):
            The heist tunnel plugin to use to ssh into the instance. Defaults to asyncssh.

        auto_configure(bool, Optional):
            automatically apply internet_gateway/subnet/vpc/route_table changes needed to SSH into an instance.

        verify(bool, Optional):
            If set to True, then verify that the instance is prepared for ssh connections.

        kwargs:
            All extra kwargs are used in asyncssh.SSHClientConnectionOptions.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    Examples:
        .. code-block:: bash

            idem exec aws.ec2.instance.bootstrap <instance_id> heist_manager="salt.minion"
    """
    result = dict(comment=[], result=True, ret=None)

    if verify or auto_configure:
        verify_ssh_ret = await hub.exec.aws.ec2.instance.verify_ssh(
            ctx, instance_id=instance_id, auto_configure=auto_configure
        )
        result["result"] &= verify_ssh_ret.result
        result["comment"] += verify_ssh_ret.comment
        if not result["result"]:
            return result

    with hub.tool.aws.ec2.instance.key_pair.verify(
        ssh_public_key=ssh_public_key,
        ssh_private_key=ssh_private_key,
        auto_configure=auto_configure,
    ) as key_pair:
        verified_public_key, private_key_file = key_pair

        connection_ret = await hub.exec.aws.ec2.instance.connect(
            ctx,
            instance_id=instance_id,
            username=username,
            host=host,
            port=port,
            tunnel_plugin=tunnel_plugin,
            ssh_public_key=verified_public_key,
            private_key_file=private_key_file,
            availability_zone=availability_zone,
            **kwargs,
        )
        result["result"] &= connection_ret.result
        result["comment"] += connection_ret.comment
        if not result["result"]:
            return result

        # Bootstrap the instance
        await hub.heist[heist_manager].run(
            remotes={instance_id: connection_ret.ret}, artifact_version=artifact_version
        )
        # TODO Check for a successful bootstrapping

    result["comment"] += [
        f"Successfully bootstrapped instance '{instance_id}' with '{heist_manager}'",
    ]

    return result


async def verify_ssh(hub, ctx, instance_id: str, auto_configure: bool = False):
    """Verify that an instance meets all the requirements for SSH connection

    Args:
        instance_id(str):
            An AWS EC2 Instance ID.

        auto_configure(bool, Optional):
            Automatically apply internet_gateway/subnet/vpc/route_table changes needed to SSH into an instance.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    Examples:

        .. code-block:: bash

            $ idem exec aws.ec2.instance.verify_ssh <instance_id> auto_configure=True
    """
    result = dict(result=True, comment=[], ret=None)

    # Create an instance resource object to use for defaults
    instance = await hub.tool.boto3.resource.create(ctx, "ec2", "Instance", instance_id)

    # Verify that the instance is in a state with all the right permissions
    if not instance.state["Name"] == "running":
        if auto_configure:
            # start the instance
            ret = await hub.exec.aws.ec2.instance.start(ctx, instance_id=instance.id)
            result["result"] &= ret
            if ret.comment:
                result["comment"].append(ret.comment)
        else:
            result["result"] = False
            result["comment"] += [
                "Instance is not running, run the following command to start the instance"
            ]
            result["comment"] += [
                f"$ idem exec aws.ec2.instance.start instance_id={instance.id}"
            ]
            return result

    if not instance.vpc.vpc_id:
        # Instances must have a vpc, this is a sanity check
        result["comment"] += [f"No vpc attached to instance"]
        result["result"] = False
        return result

    if not instance.subnet.subnet_id:
        # Instances must have a subnet, this is a sanity check
        result["comment"] += [f"No subnet attached to instance"]
        result["result"] = False
        return result

    # Verify that an internet gateway is attached to the instance's vpc
    internet_gateway_ret = await hub.exec.boto3.client.ec2.describe_internet_gateways(
        ctx,
        Filters=[
            {"Name": "attachment.vpc-id", "Values": [instance.vpc.vpc_id]},
        ],
    )

    if not internet_gateway_ret.result and internet_gateway_ret.ret["InternetGateways"]:
        if auto_configure:
            # Create a new internet gateway
            igw_ret = await hub.exec.boto3.client.ec2.create_internet_gateway(ctx)
            result["result"] &= igw_ret.result
            if igw_ret.comment:
                result["comment"] += [igw_ret.comment]
            if not result["result"]:
                return result

            internet_gateway_id = igw_ret.ret["InternetGatewayId"]
            result["comment"] += [f"Created internet gateway: {internet_gateway_id}"]

            # attach the internet gateway to the instance's vpc
            attach_ret = await hub.exec.boto3.client.ec2.attach_internet_gateway(
                ctx, InternetGatewayId=internet_gateway_id, VpcId=instance.vpc.vpc_id
            )
            result["result"] &= attach_ret.result
            if attach_ret.comment:
                result["comment"] += [attach_ret.comment]
            if not result["result"]:
                return result

            result["comment"] += [
                f"Attached internet gateway '{internet_gateway_id}' to {instance.vpc.vpc_id}"
            ]
            internet_gateway_ids = [internet_gateway_id]
        else:
            result["comment"] += [
                f"No internet gateway attached to instance's vpc: {instance.vpc.vpc_id}",
                "Run the following command to attach an internet gateway to the instance's vpc",
                f"$ idem exec boto3.client.ec2.create_internet_gateway --output=json > igw.json",
                "$ IGW_ID=\"${jq -r '.ret.InternetGatewayId' igw.json}\"",
                f"$ idem exec boto3.client.ec2.attach_internet_gateway InternetGatewayId=$IGW_ID VpcId={instance.vpc.vpc_id}",
            ]
            result["result"] = False
            return result
    else:
        internet_gateway_ids = [
            igw["InternetGatewayId"]
            for igw in internet_gateway_ret.ret["InternetGateways"]
        ]

    # Verify that there is a route with 0.0.0.0/0 as the destination and the internet gateway for your VPC as the target
    ipv4_route_table_ret = await hub.exec.boto3.client.ec2.describe_route_tables(
        ctx,
        Filters=[
            {"Name": "vpc-id", "Values": [instance.vpc.vpc_id]},
            {"Name": "route.destination-cidr-block", "Values": ["0.0.0.0/0"]},
            {"Name": "route.gateway-id", "Values": internet_gateway_ids},
        ],
    )
    has_route_table = False
    if not (ipv4_route_table_ret and ipv4_route_table_ret.ret["RouteTables"]):
        result["comment"] += [
            f"No route from vpc's internet gateway {internet_gateway_ids} to '0.0.0.0/0'"
        ]
    else:
        has_route_table = True

    if not has_route_table:
        # Verify that there is a route with ::/0 as the destination and the internet gateway for your VPC as the target
        ipv6_route_table_ret = await hub.exec.boto3.client.ec2.describe_route_tables(
            ctx,
            Filters=[
                {"Name": "vpc-id", "Values": [instance.vpc.vpc_id]},
                {"Name": "route.destination-ipv6-cidr-block", "Values": ["::/0"]},
                {"Name": "route.gateway-id", "Values": internet_gateway_ids},
            ],
        )
        if not (ipv6_route_table_ret and ipv6_route_table_ret.ret["RouteTables"]):
            result["comment"] += [
                f"No route from vpc's internet gateway {internet_gateway_ids} to '::/0'"
            ]
        else:
            has_route_table = True

    # If there is still no route table then add a command to the comments that would enable it
    if not has_route_table:
        if auto_configure:
            # TODO configure route table
            ...
        else:
            # At least one ipv4 or ipv6 route table must be configured for SSH
            result["result"] = False

        # Get the first internet gateway to use in an example
        igw_id = next(iter(internet_gateway_ids))
        # Get the id of the main route table attached to the vpc
        try_route_table = await hub.exec.boto3.client.ec2.describe_route_tables(
            ctx,
            Filters=[
                {"Name": "vpc-id", "Values": [instance.vpc.vpc_id]},
                {"Name": "route.gateway-id", "Values": [igw_id]},
            ],
        )
        if try_route_table and try_route_table.ret:
            result["comment"] += [
                "Use the following command to create a valid SSH route for the instance"
            ]
            # Get the id of the main route table
            rt_id = next(iter(try_route_table.ret["RouteTables"]))["RouteTableId"]
            result["comment"] += [
                f"$ idem exec boto3.client.ec2.create_route RouteTableID={rt_id} VpcEndpointId={instance.vpc.vpc_id} DestinationCidrBlock='0.0.0.0/0' GatewayId={igw_id}"
            ]

    # Verify that the ACL for the subnet allows inbound traffic
    network_acl_ret = await hub.exec.boto3.client.ec2.describe_network_acls(
        ctx,
        Filters=[
            {"Name": "association.subnet-id", "Values": [instance.subnet.subnet_id]},
            {"Name": "entry.rule-action", "Values": ["allow"]},
            {"Name": "vpc-id", "Values": [instance.vpc.vpc_id]},
        ],
    )
    if not (network_acl_ret and network_acl_ret.ret["NetworkAcls"]):
        result["comment"] += [f"No valid ACL"]
        if auto_configure:
            # TODO configure network acl
            ...
        else:
            result["result"] = False

    return result


async def connect(
    hub,
    ctx,
    instance_id: str,
    *,
    username: str = None,
    host: str = None,
    port: int = DEFAULT_SSH_PORT,
    tunnel_plugin: str = DEFAULT_TUNNEL_PLUGIN,
    ssh_public_key: str,
    private_key_file: str,
    availability_zone: str = None,
    **kwargs,
):
    """Attempt connection with SSH to the instance with the given parameters.

    If no host or username is specified, then make reasonable guesses and return the target configuration that was successful

    Args:
        instance_id(str):
            An AWS EC2 Instance ID.

        username(str, Optional):
            The instance OS username to use in the connection, Defaults to ec2-user.

        host(str, Optional):
            The public ip address or dns name of the instance.  Defaults to autodetect.

        port(int, Optional):
            The port to connect to on the host.  Defaults to 22.

        ssh_public_key(str, Optional):
            A public ssh key or path to send to the instance.

        private_key_file(str, Optional):
            The path to a private ssh key file.

        availability_zone(str, Optional):
            The Availability Zone in which the EC2 instance was launched.

        tunnel_plugin(str, Optional):
            The heist tunnel plugin to use to ssh into the instance. Defaults to asyncssh.

        kwargs:
            All extra kwargs are used in asyncssh.SSHClientConnectionOptions.

    Returns:
        {"result": True|False, "comment": A message Tuple, "ret": Dict}

    Examples:
        .. code-block:: bash

            idem exec aws.ec2.instance.connect <instance_id>
    """
    result = dict(result=True, comment=[], ret={})

    # Create an instance resource object to use for defaults
    instance = await hub.tool.boto3.resource.create(ctx, "ec2", "Instance", instance_id)

    # Use the availability zone defined in the instance if none was provided
    if availability_zone is None:
        availability_zone = instance.placement["AvailabilityZone"]

    # If no host was provided then try all the instance's dns names and ip addresses
    if host:
        hosts_to_try = (host,)
    else:
        hosts_to_try = (
            instance.public_dns_name,
            instance.private_dns_name,
            instance.private_ip_address,
            instance.ipv6_address,
            instance.public_ip_address,
        )

    # If no username was provided then try all common known usernames for ec2 images
    if username:
        # Only use the given username
        user_names_to_try = (username,)
    else:
        user_names_to_try = (
            "ec2-user",
            "root",
            "admin",
            "ubuntu",
            "bitnami",
            "fedora",
            "centos",
        )

    # If no username or host was specified, then try multiple combinations until one works
    for try_user, try_host in itertools.product(user_names_to_try, hosts_to_try):
        if not try_host:
            # the ipv6_address or other attempted host name might not be set
            continue
        target = dict(
            host=try_host,
            port=port,
            bootstrap=True,
            username=try_user,
            client_keys=[private_key_file],
            IdentitiesOnly="yes",
            **kwargs,
        )

        # Connect to the ec2 instance with the public key, connection will be available for 60 seconds
        connection_ret = await hub.exec.boto3.client[
            "ec2-instance-connect"
        ].send_ssh_public_key(
            ctx,
            InstanceId=instance_id,
            InstanceOSUser=try_user,
            SSHPublicKey=ssh_public_key,
            AvailabilityZone=availability_zone,
        )
        if connection_ret.comment:
            hub.log.debug(
                f"Sending public key to {instance_id}: {connection_ret.comment}"
            )

        if not connection_ret.result:
            hub.log.debug(f"Connection error sending public key to {instance_id}")
            continue
        if not connection_ret.ret.get("Success"):
            hub.log.debug(f"Unable to send public key to {instance_id}")
            continue

        hub.log.debug(
            f"Connecting to instance '{instance_id}' with ssh: {try_user}@{try_host}"
        )

        # Create a connection verify the ability to SSH to the instance
        ret = await hub.tunnel[tunnel_plugin].create(
            name=instance_id, target=copy.deepcopy(target)
        )
        if not ret:
            hub.log.debug(
                f"Unable to connect to the instance with SSH: {try_user}@{try_host}"
            )
            continue

        # Success!
        result["comment"] += [
            f"Successfully connected to instance with SSH: {try_user}@{try_host}"
        ]
        result["ret"] = target
        return result

    # There were no successful connections in the loop
    result["comment"] += [
        f"Unable to connect to instance with SSH",
        "Try troubleshooting: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html",
    ]
    result["result"] = False

    return result


async def start(hub, ctx, instance_id: (str, "alias=resource_id") = None):
    """
    Start the instance and wait for it to be running
    """
    result = dict(result=True, comment=[], ret={})

    ret = await hub.exec.boto3.client.ec2.start_instances(
        ctx, InstanceIds=[instance_id]
    )
    if ret.comment:
        result["comment"].append(ret.comment)
    if not ret.result:
        result["result"] &= ret.result
        return result

    resource = await hub.tool.boto3.resource.create(ctx, "ec2", "Instance", instance_id)
    await hub.tool.boto3.resource.exec(resource, "wait_until_running")

    return result


async def stop(hub, ctx, instance_id: (str, "alias=resource_id") = None):
    """
    Stop the instance and wait for it to be stopped.
    """
    result = dict(result=True, comment=[], ret={})

    ret = await hub.exec.boto3.client.ec2.stop_instances(
        ctx, InstanceIds=[instance_id], Hibernate=False, Force=False
    )
    if ret.comment:
        result["comment"].append(ret.comment)
    if not ret.result:
        result["result"] &= ret.result
        return result

    resource = await hub.tool.boto3.resource.create(ctx, "ec2", "Instance", instance_id)
    await hub.tool.boto3.resource.exec(resource, "wait_until_stopped")

    return result


async def get(
    hub,
    ctx,
    *,
    name=None,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """
    Args:
        name(str):
            The name of the Idem state.

        resource_id(str, Optional):
            AWS VPC id to identify the resource.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances.
    """
    result = dict(comment=[], ret=None, result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )
    if resource_id:
        ret = await hub.exec.boto3.client.ec2.describe_instances(
            ctx, InstanceIds=[resource_id], Filters=filters
        )
    else:
        ret = await hub.exec.boto3.client.ec2.describe_instances(
            ctx,
            Filters=filters,
        )

    if not ret["result"]:
        if "InvalidInstanceID.NotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ec2.instance", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    present_states = (
        await hub.tool.aws.ec2.instance.state.convert_instance_to_present_async(
            ctx, ret.ret, name=name
        )
    )

    # If the resource can't be found but there were no results then "result" is True and "ret" is None
    if not present_states:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.instance", name=name
            )
        )
        return result

    # return the first result as a plain dictionary
    result["ret"] = next(iter((present_states).values()))

    return result


async def list_(hub, ctx, *, name: str = None, filters: List = None) -> Dict:
    """
    Args:
        name(str, Optional):
            The name of the Idem state.

        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances.
    """
    result = dict(comment=[], ret=[], result=True)
    if filters:
        filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
            filters=filters
        )
    ret = await hub.exec.boto3.client.ec2.describe_instances(
        ctx,
        Filters=filters,
    )

    # If there was an error in the call then report failure
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    present_states = (
        await hub.tool.aws.ec2.instance.state.convert_instance_to_present_async(
            ctx, ret.ret
        )
    )
    if not present_states:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.instance", name=name
            )
        )
        return result

    # Return a list of dictionaries with details about all the instances
    result["ret"] = list(present_states.values())

    return result
