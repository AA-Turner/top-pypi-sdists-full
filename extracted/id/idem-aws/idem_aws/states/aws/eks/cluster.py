"""State module for managing EKS Cluster."""
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
            "aws.eks.nodegroup.absent",
            "aws.eks.addon.absent",
            "aws.eks.fargate_profile.absent",
        ],
    },
    "present": {
        "require": [
            "aws.ec2.subnet.present",
            "aws.iam.role.present",
        ],
    },
}

create_attempts = 60
update_attempts = 120


async def present(
    hub,
    ctx,
    name: str,
    role_arn: str,
    resources_vpc_config: make_dataclass(
        "VpcConfigRequest",
        [
            ("subnetIds", List[str], field(default=None)),
            ("securityGroupIds", List[str], field(default=None)),
            ("endpointPublicAccess", bool, field(default=None)),
            ("endpointPrivateAccess", bool, field(default=None)),
            ("publicAccessCidrs", List[str], field(default=None)),
        ],
    ),
    resource_id: str = None,
    version: str = None,
    kubernetes_network_config: make_dataclass(
        "KubernetesNetworkConfigRequest",
        [
            ("serviceIpv4Cidr", str, field(default=None)),
            ("ipFamily", str, field(default=None)),
        ],
    ) = None,
    logging: make_dataclass(
        "Logging",
        [
            (
                "clusterLogging",
                List[
                    make_dataclass(
                        "LogSetup",
                        [
                            ("types", List[str], field(default=None)),
                            ("enabled", bool, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            )
        ],
    ) = None,
    encryption_config: List[
        make_dataclass(
            "EncryptionConfig",
            [
                ("resources", List[str], field(default=None)),
                (
                    "provider",
                    make_dataclass("Provider", [("keyArn", str, field(default=None))]),
                    field(default=None),
                ),
            ],
        )
    ] = None,
    tags: Dict[str, str] = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=10)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=10)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    client_request_token: str = None,
    outpost_config: make_dataclass(
        "OutpostConfig",
        [
            (
                "outpostArns",
                List[str],
            ),
            ("controlPlaneInstanceType", str),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates an Amazon EKS control plane.

    The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as etcd and
    the API server. The control plane runs in an account managed by Amazon Web Services, and the Kubernetes API is
    exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique.
    It runs on its own set of Amazon EC2 instances. The cluster control plane is provisioned across multiple
    Availability Zones and fronted by an Elastic Load Balancing Network Load Balancer. Amazon EKS also provisions
    elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes
    (for example, to support kubectl exec, logs, and proxy data flows).

    Amazon EKS nodes run in your Amazon Web Services account and connect to your cluster's control plane over the
    Kubernetes API server endpoint and a certificate file that is created for your cluster. In most cases, it takes
    several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes
    tooling to communicate with the API server and launch nodes into your cluster. For more information, see
    Managing Cluster Authentication and Launching Amazon EKS nodes in the Amazon EKS User Guide.

    Args:

        name(str):
            The unique name to give to your cluster.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        version(str, Optional):
            The desired Kubernetes version for your cluster. If you don't specify a value here, the latest
            version available in Amazon EKS is used. Defaults to None.

        role_arn(str):
            The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes
            control plane to make calls to Amazon Web Services API operations on your behalf. For more
            information, see Amazon EKS Service IAM Role in the  Amazon EKS User Guide .

        resources_vpc_config(dict[str, Any]):
            The VPC configuration that's used by the cluster control plane. Amazon EKS VPC resources have
            specific requirements to work properly with Kubernetes. For more information, see Cluster VPC
            Considerations and Cluster Security Group Considerations in the Amazon EKS User Guide. You must
            specify at least two subnets. You can specify up to five security groups. However, we recommend
            that you use a dedicated security group for your cluster control plane.

            * subnetIds (list[str], Optional):
                Specify subnets for your Amazon EKS nodes. Amazon EKS creates cross-account elastic network
                interfaces in these subnets to allow communication between your nodes and the Kubernetes control
                plane.

            * securityGroupIds (list[str], Optional):
                Specify one or more security groups for the cross-account elastic network interfaces that Amazon
                EKS creates to use that allow communication between your nodes and the Kubernetes control plane.
                If you don't specify any security groups, then familiarize yourself with the difference between
                Amazon EKS defaults for clusters deployed with Kubernetes:   1.14 Amazon EKS platform version
                eks.2 and earlier   1.14 Amazon EKS platform version eks.3 and later    For more information,
                see Amazon EKS security group considerations in the  Amazon EKS User Guide.

            * endpointPublicAccess (bool, Optional):
                Set this value to false to disable public access to your cluster's Kubernetes API server
                endpoint. If you disable public access, your cluster's Kubernetes API server can only receive
                requests from within the cluster VPC. The default value for this parameter is true, which
                enables public access for your Kubernetes API server. For more information, see Amazon EKS
                cluster endpoint access control in the  Amazon EKS User Guide.

            * endpointPrivateAccess (bool, Optional):
                Set this value to true to enable private access for your cluster's Kubernetes API server
                endpoint. If you enable private access, Kubernetes API requests from within your cluster's VPC
                use the private VPC endpoint. The default value for this parameter is false, which disables
                private access for your Kubernetes API server. If you disable private access and you have nodes
                or Fargate pods in the cluster, then ensure that publicAccessCidrs includes the necessary CIDR
                blocks for communication with the nodes or Fargate pods. For more information, see Amazon EKS
                cluster endpoint access control in the  Amazon EKS User Guide.

            * publicAccessCidrs (list[str], Optional):
                The CIDR blocks that are allowed access to your cluster's public Kubernetes API server endpoint.
                Communication to the endpoint from addresses outside of the CIDR blocks that you specify is
                denied. The default value is 0.0.0.0/0. If you've disabled private endpoint access and you have
                nodes or Fargate pods in the cluster, then ensure that you specify the necessary CIDR blocks.
                For more information, see Amazon EKS cluster endpoint access control in the  Amazon EKS User
                Guide.

        kubernetes_network_config(dict[str, Any], Optional):
            The Kubernetes network configuration for the cluster. Defaults to None.

            * serviceIpv4Cidr (str, Optional):
                Don't specify a value if you select ipv6 for ipFamily. The CIDR block to assign Kubernetes
                service IP addresses from. If you don't specify a block, Kubernetes assigns addresses from
                either the 10.100.0.0/16 or 172.20.0.0/16 CIDR blocks. We recommend that you specify a block
                that does not overlap with resources in other networks that are peered or connected to your VPC.
                The block must meet the following requirements:   Within one of the following private IP address
                blocks: 10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16.   Doesn't overlap with any CIDR block
                assigned to the VPC that you selected for VPC.   Between /24 and /12.    You can only specify a
                custom CIDR block when you create a cluster and can't change this value once the cluster is
                created.

            * ipFamily (str, Optional):
                Specify which IP family is used to assign Kubernetes pod and service IP addresses. If you don't
                specify a value, ipv4 is used by default. You can only specify an IP family when you create a
                cluster and can't change this value once the cluster is created. If you specify ipv6, the VPC
                and subnets that you specify for cluster creation must have both IPv4 and IPv6 CIDR blocks
                assigned to them. You can't specify ipv6 for clusters in China Regions. You can only specify
                ipv6 for 1.21 and later clusters that use version 1.10.1 or later of the Amazon VPC CNI add-on.
                If you specify ipv6, then ensure that your VPC meets the requirements listed in the
                considerations listed in Assigning IPv6 addresses to pods and services in the Amazon EKS User
                Guide. Kubernetes assigns services IPv6 addresses from the unique local address range
                (fc00::/7). You can't specify a custom IPv6 CIDR block. Pod addresses are assigned from the
                subnet's IPv6 CIDR.

        logging(dict[str, Any], Optional):
            Enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch
            Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more
            information, see Amazon EKS Cluster control plane logs in the  Amazon EKS User Guide .
            CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control
            plane logs. For more information, see CloudWatch Pricing. Defaults to None.

            * clusterLogging (list[dict[str, Any]], Optional):
                The cluster control plane logging configuration for your cluster.

                * types (list[str], Optional):
                    The available cluster control plane log types.

                * enabled (bool, Optional):
                    If a log type is enabled, that log type exports its control plane logs to CloudWatch Logs. If a
                    log type isn't enabled, that log type doesn't export its control plane logs. Each individual log
                    type can be enabled or disabled independently.

        tags(dict[str, str], Optional):
            The metadata to apply to the cluster to assist with categorization and organization. Each tag
            consists of a key and an Optional value. You define both. Defaults to None.

        encryption_config(list[dict[str, Any]], Optional):
            The encryption configuration for the cluster. Defaults to None.

            * resources (list[str], Optional):
                Specifies the resources to be encrypted. The only supported value is "secrets".

            * provider (dict[str, Any], Optional):
                Key Management Service (KMS) key. Either the ARN or the alias can be used.

                * keyArn (str, Optional):
                    Amazon Resource Name (ARN) or alias of the KMS key. The KMS key must be symmetric, created in
                    the same region as the cluster, and if the KMS key was created in a different account, the user
                    must have access to the KMS key. For more information, see Allowing Users in Other Accounts to
                    Use a KMS key in the Key Management Service Developer Guide.

        timeout(dict, Optional):
            Timeout configuration for creating or updating cluster.

            * create (dict):
                Timeout configuration for creating cluster
                * delay(int, default=60): The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=40): Customized timeout configuration containing delay and max attempts.

            * update (str):
                Timeout configuration for updating cluster
                * delay(int, default=60): The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=40): Customized timeout configuration containing delay and max attempts.

        client_request_token(str, Optional):
            Unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

        outpost_config(dict, Optional):
            An object representing the configuration of your local Amazon EKS cluster on an Amazon Web Services Outpost.
            This object isn't available for creating Amazon EKS clusters on the Amazon Web Services cloud.

            * outpostArns(list) :
                The ARN of the Outpost that you want to use for your local Amazon EKS cluster on Outposts.
                Only a single Outpost ARN is supported.

            * controlPlaneInstanceType(str):
                The Amazon EC2 instance type that you want to use for your local Amazon EKS cluster on Outposts. The
                instance type that you specify is used for all Kubernetes control plane instances. The instance type
                can't be changed after cluster creation.
                Choose an instance type based on the number of nodes that your cluster will have.

                If your cluster will have:
                    * 1–20 nodes, then we recommend specifying a large instance type.
                    * 21–100 nodes, then we recommend specifying an xlarge instance type.
                    * 101–250 nodes, then we recommend specifying a 2xlarge instance type.

    Request Syntax:
        .. code-block:: sls

            [eks-cluster-resource-name]:
              aws.eks.cluster.present:
                - role_arn: 'string'
                - version: 'string'
                - resource_id: 'string'
                - resources_vpc_config:
                    endpointPrivateAccess: boolean
                    endpointPublicAccess: boolean
                    publicAccessCidrs: list
                    securityGroupIds:
                    - 'string'
                    subnetIds:
                    - 'string'
                    - 'string'
                - kubernetes_network_config:
                    ipFamily: 'string'
                    serviceIpv4Cidr: 'string'
                - logging:
                    clusterLogging:
                    - enabled: boolean
                      types:
                      - 'string'
                      - 'string'
                    - enabled: boolean
                      types:
                      - 'string'
                      - 'string'
                      - 'string'
                - tags:
                   'string': 'string'
                - timeout:
                     create:
                        delay: 'integer'
                        max_attempts: 'integer'
                     update:
                        delay: 'integer'
                        max_attempts: 'integer
                - client_request_token: string'
                - outpost_config:
                    ControlPlaneInstanceType: String
                    OutpostArns:
                      - String

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            my_cluster:
              aws.eks.cluster.present:
                - role_arn: arn:aws:iam::202236654445:role/ek1
                - version: '1.21'
                - resource_id: eks-e45k5n423
                - resources_vpc_config:
                    endpointPrivateAccess: true
                    endpointPublicAccess: false
                    publicAccessCidrs: []
                    securityGroupIds:
                    - sg-000b8c21b6b480577
                    subnetIds:
                    - subnet-07bc4715744fb7b39
                    - subnet-0aa66edffb00d8881
                - kubernetes_network_config:
                    ipFamily: ipv4
                    serviceIpv4Cidr: 172.20.0.0/16
                - logging:
                    clusterLogging:
                    - enabled: true
                      types:
                      - api
                      - audit
                    - enabled: false
                      types:
                      - authenticator
                      - controllerManager
                      - scheduler
                - tags:
                    Name: eks-cluster-name

    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.eks.cluster.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
    try:
        if before and before["ret"]:
            result["old_state"] = before["ret"]
            client_request_token = result["old_state"].get("client_request_token", None)
            plan_state = copy.deepcopy(result["old_state"])

            # update cluster
            update_ret = await hub.tool.aws.eks.cluster.update_cluster(
                ctx=ctx,
                name=name,
                before=result["old_state"],
                version=version,
                encryption_config=encryption_config,
                resources_vpc_config=resources_vpc_config,
                logging=logging,
                client_request_token=client_request_token,
                timeout=timeout,
            )
            result["comment"] = update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                result["comment"] += [f"Would update aws.eks.cluster '{name}'"]
                for cluster_param in update_ret["ret"]:
                    plan_state[cluster_param] = update_ret["ret"][cluster_param]
            # update tags
            if tags is not None:
                update_tags_ret = await hub.tool.aws.eks.tag.update_eks_tags(
                    ctx=ctx,
                    resource_arn=result["old_state"].get("arn"),
                    old_tags=result["old_state"].get("tags"),
                    new_tags=tags,
                )
                result["comment"] += update_tags_ret["comment"]
                result["result"] = result["result"] and update_tags_ret["result"]
                resource_updated = resource_updated or bool(update_tags_ret["ret"])

                if ctx.get("test", False) and update_tags_ret["ret"]:
                    plan_state["tags"] = update_tags_ret["ret"].get("tags")
        else:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "version": version,
                        "role_arn": role_arn,
                        "resources_vpc_config": resources_vpc_config,
                        "kubernetes_network_config": kubernetes_network_config,
                        "logging": logging,
                        "encryption_config": encryption_config,
                        "tags": tags,
                        "outpost_config": outpost_config,
                        "client_request_token": client_request_token,
                    },
                )
                result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.eks.cluster", name=name
                )
                return result

            try:
                ret = await hub.exec.boto3.client.eks.create_cluster(
                    ctx,
                    name=name,
                    version=version,
                    roleArn=role_arn,
                    resourcesVpcConfig=resources_vpc_config,
                    kubernetesNetworkConfig=kubernetes_network_config,
                    logging=logging,
                    encryptionConfig=encryption_config,
                    tags=tags,
                    clientRequestToken=client_request_token,
                    outpostConfig=outpost_config,
                )
                result["result"] = ret["result"]
                if not result["result"]:
                    result["comment"] = ret["comment"]
                    return result

                resource_id = ret["ret"]["cluster"]["name"]
                waiter_ret = await hub.tool.aws.eks.cluster.cluster_waiter(
                    ctx, name, resource_id, timeout, "create"
                )
                if not waiter_ret["result"]:
                    result["result"] = False
                    result["comment"] += waiter_ret["comment"]
                result["comment"] = hub.tool.aws.comment_utils.create_comment(
                    resource_type="aws.eks.cluster", name=name
                )
            except hub.tool.boto3.exception.ClientError as e:
                result["comment"] += [f"{e.__class__.__name__}: {e}"]
                result["result"] = False
    except Exception as e1:
        result["comment"] += [f"{e1.__class__.__name__}: {e1}"]
        result["result"] = False
        return result

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.eks.cluster.get(
                ctx, name=name, resource_id=resource_id
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
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
    timeout: Dict = None,
) -> Dict[str, Any]:
    """Deletes the Amazon EKS cluster control plane.

    If you have active services in your cluster that are associated with a load balancer, you must delete those services
    before deleting the cluster so that the load balancers are deleted properly. Otherwise, you can have orphaned resources
    in your VPC that prevent you from being able to delete the VPC. For more information, see Deleting a Cluster in the
    Amazon EKS User Guide. If you have managed node groups or Fargate profiles attached to the cluster, you must delete
    them first. For more information, see DeleteNodegroup and DeleteFargateProfile.

    Args:
        name(str):
            An Idem name of the EKS cluster resource.

        resource_id(str, Optional):
            AWS EKS cluster name. Idem automatically considers this resource being absent if this field is not specified.

        timeout(dict, Optional):
            Timeout configuration for deleting cluster.

            * delete (dict):
                Timeout configuration for deleting cluster

                * delay(int, default=60): The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=40): Customized timeout configuration containing delay and max attempts.


    Request syntax:
        .. code-block:: sls

            [eks_cluster_name]:
              aws.eks.cluster.absent:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            eks_cluster_prod:
              aws.eks.cluster.absent:
                - name: eks_cluster_prod
                - resource_id: eks_cluster_prod
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.eks.cluster", name=name
        )
        return result
    before = await hub.exec.aws.eks.cluster.get(ctx, name=name, resource_id=resource_id)

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.eks.cluster", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.eks.cluster", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]

        try:
            ret = await hub.exec.boto3.client.eks.delete_cluster(
                ctx,
                name=resource_id,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            else:
                waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                    default_delay=60,
                    default_max_attempts=40,
                    timeout_config=timeout.get("delete") if timeout else None,
                )
                try:
                    await hub.tool.boto3.client.wait(
                        ctx,
                        "eks",
                        "cluster_deleted",
                        name=resource_id,
                        WaiterConfig=waiter_config,
                    )
                except Exception as e:
                    result["comment"] += [str(e)]
                    result["result"] = False

            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.eks.cluster", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Lists the Amazon EKS clusters in your Amazon Web Services account in the specified Region.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.eks.cluster

    """

    result = {}
    ret = await hub.exec.boto3.client.eks.list_clusters(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not list clusters {ret['comment']}")
        return {}

    for name in ret["ret"]["clusters"]:
        get_ret = await hub.exec.aws.eks.cluster.get(ctx, name=name, resource_id=name)
        if not get_ret["result"] or not get_ret["ret"]:
            hub.log.warning(
                f"Could not get cluster {name}, Error:  {get_ret['comment']}"
            )
            continue
        resource_id = get_ret["ret"].get("resource_id")
        result[resource_id] = {
            "aws.eks.cluster.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in get_ret["ret"].items()
            ]
        }
    return result
