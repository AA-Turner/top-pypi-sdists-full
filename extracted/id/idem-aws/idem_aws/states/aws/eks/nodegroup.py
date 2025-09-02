"""State module for managing EKS Node groups."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ

__contracts__ = ["resource"]

TREQ = {
    "absent": {
        "require": [
            "aws.eks.cluster.absent",
        ],
    },
    "present": {
        "require": [
            "aws.eks.cluster.present",
        ],
    },
}
default_attempts = 120


async def present(
    hub,
    ctx,
    name: str,
    cluster_name: str,
    subnets: List[str],
    node_role: str,
    resource_id: str = None,
    scaling_config: make_dataclass(
        "NodegroupScalingConfig",
        [
            ("minSize", int, field(default=None)),
            ("maxSize", int, field(default=None)),
            ("desiredSize", int, field(default=None)),
        ],
    ) = None,
    disk_size: int = None,
    instance_types: List[str] = None,
    ami_type: str = None,
    remote_access: make_dataclass(
        "RemoteAccessConfig",
        [
            ("ec2SshKey", str, field(default=None)),
            ("sourceSecurityGroups", List[str], field(default=None)),
        ],
    ) = None,
    labels: Dict[str, str] = None,
    taints: List[
        make_dataclass(
            "Taint",
            [
                ("key", str, field(default=None)),
                ("value", str, field(default=None)),
                ("effect", str, field(default=None)),
            ],
        )
    ] = None,
    tags: Dict[str, str] = None,
    client_request_token: str = None,
    launch_template: make_dataclass(
        "LaunchTemplateSpecification",
        [
            ("name", str, field(default=None)),
            ("version", str, field(default=None)),
            ("id", str, field(default=None)),
        ],
    ) = None,
    update_config: make_dataclass(
        "NodegroupUpdateConfig",
        [
            ("maxUnavailable", int, field(default=None)),
            ("maxUnavailablePercentage", int, field(default=None)),
        ],
    ) = None,
    capacity_type: str = None,
    version: str = None,
    release_version: str = None,
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
) -> Dict[str, Any]:
    """Creates a managed node group for an Amazon EKS cluster.

    You can only create a node group for your cluster that is equal to the current Kubernetes version for the cluster.
    All node groups are created with the latest AMI release version for the respective minor Kubernetes version of the
    cluster, unless you deploy a custom AMI using a launch template. For more information about using launch templates,
    see Launch template support. An Amazon EKS managed node group is an Amazon EC2 Auto Scaling group and associated
    Amazon EC2 instances that are managed by Amazon Web Services for an Amazon EKS cluster. Each node group uses a version
    of the Amazon EKS optimized Amazon Linux 2 AMI. For more information, see Managed Node Groups in the Amazon EKS User Guide.

    Args:
        name(str):
            An Idem name of EKS Node group.

        cluster_name(str):
            The name of the cluster to create the node group in.

        subnets(list[str]):
            The subnets to use for the Auto Scaling group that is created for your node group. If you specify launchTemplate,
            then don't specify  SubnetId  in your launch template, or the node group deployment will fail. For more
            information about using launch templates with Amazon EKS, see Launch template support in the Amazon EKS User Guide.

        node_role(str):
            The Amazon Resource Name (ARN) of the IAM role to associate with your node group. The Amazon EKS worker node
            kubelet daemon makes calls to Amazon Web Services APIs on your behalf. Nodes receive permissions for these
            API calls through an IAM instance profile and associated policies. Before you can launch nodes and register
            them into a cluster, you must create an IAM role for those nodes to use when they are launched.

        resource_id(str, Optional):
            AWS EKS Node group name

        scaling_config(dict[str, Any], Optional):
            The scaling configuration details for the Auto Scaling group that is created for your node
            group. Defaults to None.

            * minSize (int, Optional):
                The minimum number of nodes that the managed node group can scale in to.

            * maxSize (int, Optional):
                The maximum number of nodes that the managed node group can scale out to. For information about
                the maximum number that you can specify, see Amazon EKS service quotas in the Amazon EKS User
                Guide.

            * desiredSize (int, Optional):
                The current number of nodes that the managed node group should maintain.  If you use Cluster
                Autoscaler, you shouldn't change the desiredSize value directly, as this can cause the Cluster
                Autoscaler to suddenly scale up or scale down.  Whenever this parameter changes, the number of
                worker nodes in the node group is updated to the specified size. If this parameter is given a
                value that is smaller than the current number of running worker nodes, the necessary number of
                worker nodes are terminated to match the given value. When using CloudFormation, no action
                occurs if you remove this parameter from your CFN template. This parameter can be different from
                minSize in some cases, such as when starting with extra hosts for testing. This parameter can
                also be different when you want to start with an estimated number of needed hosts, but let
                Cluster Autoscaler reduce the number if there are too many. When Cluster Autoscaler is used, the
                desiredSize parameter is altered by Cluster Autoscaler (but can be out-of-date for short periods
                of time). Cluster Autoscaler doesn't scale a managed node group lower than minSize or higher
                than maxSize.

        capacity_type(str, Optional):
            The capacity type for your node group

        disk_size(int, Optional):
            The root device disk size (in GiB) for your node group instances. The default
            disk size is 20 GiB.

        instance_types(list[str], Optional):
            Specify the instance types for a node group. If you specify a GPU instance type, be sure to specify AL2_x86_64_GPU
            with the amiType parameter. If you specify launchTemplate, then you can specify zero or one instance type in
            your launch template or you can specify 0-20 instance types for instanceTypes. If however, you specify an
            instance type in your launch template and specify any instanceTypes, the node group deployment will fail. If
            you don't specify an instance type in a launch template or for instanceTypes, then t3.medium is used, by default.
            If you specify Spot for capacityType, then we recommend specifying multiple values for instanceTypes. For more
            information, see Managed node group capacity types and Launch template support in the Amazon EKS
            User Guide. Defaults to None.

        ami_type(str, Optional):
            The AMI type for your node group. GPU instance types should use the AL2_x86_64_GPU AMI type. Non-GPU instances
            should use the AL2_x86_64 AMI type. Arm instances should use the AL2_ARM_64 AMI type.

        remote_access(dict[str, Any], Optional):
            The remote access (SSH) configuration to use with your node group. If you specify launchTemplate, then don't
            specify remoteAccess, or the node group deployment will fail. For more information about using launch templates
            with Amazon EKS, see Launch template support in the Amazon EKS User Guide. Defaults to None.

            * ec2SshKey (str, Optional):
                The Amazon EC2 SSH key that provides access for SSH communication with the nodes in the managed node group.
                For more information, see Amazon EC2 key pairs and Linux instances in the Amazon Elastic Compute Cloud User
                Guide for Linux Instances.

            * sourceSecurityGroups (list[str], Optional):
                The security groups that are allowed SSH access (port 22) to the nodes. If you specify an Amazon EC2 SSH
                key but do not specify a source security group when you create a managed node group, then port 22 on the
                nodes is opened to the internet (0.0.0.0/0). For more information, see Security Groups for Your VPC in
                the Amazon Virtual Private Cloud User Guide.

        labels(dict[str, str], Optional):
            The Kubernetes labels to be applied to the nodes in the node group when they are created. Defaults to None.

        taints(list[dict[str, Any]], Optional):
            The Kubernetes taints to be applied to the nodes in the node group. For more information, see
            Node taints on managed node groups. Defaults to None.
            * key (str, Optional): The key of the taint.
            * value (str, Optional): The value of the taint.
            * effect (str, Optional): The effect of the taint.

        tags(dict, Optional):
            The metadata to apply to the node group to assist with categorization and organization.
            Each tag consists of a key and an optional value. You define both. Node group tags do not propagate to any
            other resources associated with the node group, such as the Amazon EC2 instances or subnets.

        client_request_token(str, Optional):
            Unique, case-sensitive identifier that you provide to ensure the
            idempotency of the request.

        launch_template(dict[str, Any], Optional):
            An object representing a node group's launch template specification. If specified, then do not
            specify instanceTypes, diskSize, or remoteAccess and make sure that the launch template meets
            the requirements in launchTemplateSpecification. Defaults to None.

            * name (str, Optional):
                The name of the launch template.

            * version (str, Optional):
                The version of the launch template to use. If no version is specified, then the template's
                default version is used.

            * id (str, Optional):
                The ID of the launch template.

        update_config(dict[str, Any], Optional):
            The node group update configuration. Defaults to None.

            * maxUnavailable (int, Optional):
                The maximum number of nodes unavailable at once during a version update. Nodes will be updated
                in parallel. This value or maxUnavailablePercentage is required to have a value.The maximum
                number is 100.

            * maxUnavailablePercentage (int, Optional):
                The maximum percentage of nodes unavailable during a version update. This percentage of nodes
                will be updated in parallel, up to 100 nodes at once. This value or maxUnavailable is required
                to have a value.

        version(str, Optional):
            The Kubernetes version to use for your managed nodes. By default, the Kubernetes version of the
            cluster is used, and this is the only accepted specified value. If you specify launchTemplate,
            and your launch template uses a custom AMI, then don't specify version, or the node group
            deployment will fail. For more information about using launch templates with Amazon EKS, see
            Launch template support in the Amazon EKS User Guide. Defaults to None.

        release_version(str, Optional):
            The AMI version of the Amazon EKS optimized AMI to use with your node group. By default, the
            latest available AMI version for the node group's current Kubernetes version is used. For more
            information, see Amazon EKS optimized Amazon Linux 2 AMI versions in the Amazon EKS User Guide.
            If you specify launchTemplate, and your launch template uses a custom AMI, then don't specify
            releaseVersion, or the node group deployment will fail. For more information about using launch
            templates with Amazon EKS, see Launch template support in the Amazon EKS User Guide. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for creating or updating nodegroup.

            * create (dict):
                Timeout configuration for creating nodegroup
                * delay(int, default=30): The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=80): Customized timeout configuration containing delay and max attempts.

            * update (str):
                Timeout configuration for updating nodegroup
                * delay(int, default=30): The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=80): Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [eks-nodegroup-name]:
              aws.eks.nodegroup.present:
                - cluster_name: "string"
                - node_group_arn: "string"
                - version: "string"
                - release_version: "string"
                - resource_id: "string"
                - status: "string"
                - capacity_type: "ON_DEMAND|SPOT"
                - instance_types:
                  - string
                - subnets:
                  - string
                - ami_type: "string"
                - node_role: "string"
                - disk_size: integer
                - scaling_config:
                    desiredSize: integer
                    maxSize: integer
                    minSize: integer
                - update_config:
                    maxUnavailable: integer
                - tags:
                    - "string": "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            nodes1:
              aws.eks.nodegroup.present:
                - cluster_name: idem-test-cluster
                - node_group_arn: arn:aws:eks:us-west-2:000000000000:nodegroup/prod/idem-test-instance-e1a573b9-4e74-48f0-85c4-c214a8ec8ada/id123
                - version: '1.21'
                - release_version: 1.21.5-20220123
                - resource_id: 'idem-test-cluster-node-group'
                - status: ACTIVE
                - capacity_type: ON_DEMAND
                - instance_types:
                  - t1.micro
                - subnets:
                  - subnet-31813031
                - ami_type: AL2_x86_64
                - node_role: arn:aws:iam::000000000000:role/idem-test-role-2075a427-24c2-4021-abc3-9b542834addb
                - disk_size: 20
                - scaling_config:
                    desiredSize: 2
                    maxSize: 2
                    minSize: 2
                - update_config:
                    maxUnavailable: 1
                - tags:
                    - Name: idem-test-instance-e1a573b9-4e74-48f0-85c4-c214a8ec8ada


    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.eks.nodegroup", name=name
        )
        before = await hub.exec.boto3.client.eks.describe_nodegroup(
            ctx, clusterName=cluster_name, nodegroupName=resource_id
        )
        if not before["result"]:
            if not ("ResourceNotFoundException" in before["comment"][0]):
                result["result"] = False
                result["comment"] += before["comment"]
                return result
        if "CREATE_FAILED" == before["ret"]["nodegroup"].get("status"):
            result["result"] = False
            result["comment"] += (
                before["ret"]["nodegroup"].get("health", {}).get("issues")
            )
            return result

    if before and before["ret"]:
        try:
            result[
                "old_state"
            ] = hub.tool.aws.eks.conversion_utils.convert_raw_nodegroup_to_present(
                raw_resource=before["ret"]["nodegroup"], idem_resource_name=name
            )
            plan_state = copy.deepcopy(result["old_state"])
            client_request_token = result["old_state"].get("client_request_token", None)

            # update nodegroup
            update_ret = await hub.tool.aws.eks.nodegroup.update_nodegroup(
                ctx=ctx,
                name=name,
                before=result["old_state"],
                version=version,
                release_version=release_version,
                launch_template=launch_template,
                labels=labels,
                taints=taints,
                scaling_config=scaling_config,
                update_config=update_config,
                client_request_token=client_request_token,
                timeout=timeout,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = bool(update_ret["ret"])

            if update_ret["ret"] and ctx.get("test", False):
                result["comment"] += [f"Would update aws.eks.nodegroup '{name}'"]
                for nodegroup_param in update_ret["ret"]:
                    plan_state[nodegroup_param] = update_ret["ret"][nodegroup_param]

            # update tags
            update_tags_ret = await hub.tool.aws.eks.tag.update_eks_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("nodegroup_arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_tags_ret["comment"]
            result["result"] = result["result"] and update_tags_ret["result"]
            resource_updated = resource_updated or bool(update_tags_ret["ret"])
            if ctx.get("test", False) and update_tags_ret["ret"]:
                plan_state["tags"] = update_tags_ret["ret"].get("tags")
        except Exception as e1:
            result["comment"] += [f"{e1.__class__.__name__}: {e1}"]
            result["result"] = False
            return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "cluster_name": cluster_name,
                    "subnets": subnets,
                    "node_role": node_role,
                    "scaling_config": scaling_config,
                    "disk_size": disk_size,
                    "instance_types": instance_types,
                    "ami_type": ami_type,
                    "remote_access": remote_access,
                    "labels": labels,
                    "taints": taints,
                    "tags": tags,
                    "client_request_token": client_request_token,
                    "launch_template": launch_template,
                    "update_config": update_config,
                    "capacity_type": capacity_type,
                    "version": version,
                    "release_version": release_version,
                },
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.eks.nodegroup", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.eks.create_nodegroup(
                ctx,
                clusterName=cluster_name,
                nodegroupName=name,
                scalingConfig=scaling_config,
                diskSize=disk_size,
                subnets=subnets,
                instanceTypes=instance_types,
                amiType=ami_type,
                remoteAccess=remote_access,
                nodeRole=node_role,
                labels=labels,
                taints=taints,
                tags=tags,
                clientRequestToken=client_request_token,
                launchTemplate=launch_template,
                updateConfig=update_config,
                capacityType=capacity_type,
                version=version,
                releaseVersion=release_version,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result

            resource_id = ret["ret"]["nodegroup"]["nodegroupName"]
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=60,
                default_max_attempts=40,
                timeout_config=timeout.get("create") if timeout else None,
            )
            hub.log.debug(f"Waiting on creating aws.eks.nodegroup '{name}'")
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "eks",
                    "nodegroup_active",
                    nodegroupName=resource_id,
                    clusterName=cluster_name,
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
            result["comment"] += hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.eks.nodegroup", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.boto3.client.eks.describe_nodegroup(
                ctx, clusterName=cluster_name, nodegroupName=resource_id
            )
            result[
                "new_state"
            ] = hub.tool.aws.eks.conversion_utils.convert_raw_nodegroup_to_present(
                raw_resource=after["ret"]["nodegroup"], idem_resource_name=name
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
    cluster_name: str = None,
    resource_id: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """
    **Autogenerated function**

    Deletes an Amazon EKS node group for a cluster.

    Args:
        name(str):
            An Idem name of EKS Node group.

        cluster_name(str, None):
            The name of the cluster to create the node group in.

        resource_id(str, Optional):
            AWS EKS Node group name. Idem automatically considers this resource being absent
         if this field is not specified.

        timeout(dict, Optional):
            Timeout configuration for creating or updating cluster.

            * delete (dict):
                Timeout configuration for deleting cluster
                * delay: The amount of time in seconds to wait between attempts.
                * max_attempts: Customized timeout configuration containing delay and max attempts.
    Request Syntax:
        .. code-block:: sls

            [nodegroup-name]:
              aws.eks.nodegroup.absent:
                - cluster_name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            nodes1:
              aws.eks.nodegroup.absent:
                - cluster_name: idem-test-cluster
                - resource_id: idem-test-nodegroup
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.eks.nodegroup", name=name
        )
        return result
    if not cluster_name:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.eks.nodegroup", name=name, args=["cluster_name"]
        )
        result["result"] = False
        return result
    before = await hub.exec.boto3.client.eks.describe_nodegroup(
        ctx, clusterName=cluster_name, nodegroupName=resource_id
    )
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.eks.nodegroup", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.eks.conversion_utils.convert_raw_nodegroup_to_present(
            raw_resource=before["ret"]["nodegroup"], idem_resource_name=name
        )
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.eks.nodegroup", name=name
        )
        return result
    else:
        result[
            "old_state"
        ] = hub.tool.aws.eks.conversion_utils.convert_raw_nodegroup_to_present(
            raw_resource=before["ret"]["nodegroup"], idem_resource_name=name
        )
        try:
            ret = await hub.exec.boto3.client.eks.delete_nodegroup(
                ctx, clusterName=cluster_name, nodegroupName=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
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
                        "nodegroup_deleted",
                        nodegroupName=resource_id,
                        clusterName=cluster_name,
                        WaiterConfig=waiter_config,
                    )
                except Exception as e:
                    result["comment"] += [str(e)]
                    result["result"] = False
            result["comment"] += hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.eks.nodegroup", name=name
            )
        except Exception as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Lists the Amazon EKS managed node groups associated with the specified cluster in your Amazon Web Services
    account in the specified Region. Self-managed node groups are not listed.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.eks.nodegroup

    """

    result = {}
    cluster_ret = await hub.exec.boto3.client.eks.list_clusters(ctx)
    if not cluster_ret["result"]:
        hub.log.warning(f"Could not describe cluster {cluster_ret['comment']}")
        return {}
    cluster_node_groups = []
    try:
        for name in cluster_ret["ret"]["clusters"]:
            node_group_ret = await hub.exec.boto3.client.eks.list_nodegroups(
                ctx, clusterName=name
            )
            if not node_group_ret["result"]:
                result["comment"] = node_group_ret["comment"]
                return result
            for group in node_group_ret["ret"]["nodegroups"]:
                cluster_node_groups.append({"name": name, "group": group})
    except Exception as e:
        result["comment"] = str(e)
        result["result"] = False
        return result

    for node_groups in cluster_node_groups:
        cluster_name = node_groups["name"]
        node_group = node_groups["group"]
        describe_ret = await hub.exec.boto3.client.eks.describe_nodegroup(
            ctx, clusterName=cluster_name, nodegroupName=node_group
        )
        nodegroup = describe_ret["ret"]["nodegroup"]
        resource_id = f"{nodegroup['clusterName']}-{nodegroup['nodegroupName']}"
        resource_translated = (
            hub.tool.aws.eks.conversion_utils.convert_raw_nodegroup_to_present(
                raw_resource=nodegroup, idem_resource_name=resource_id
            )
        )
        result[resource_id] = {
            "aws.eks.nodegroup.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
